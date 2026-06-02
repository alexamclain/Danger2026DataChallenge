#!/usr/bin/env python3
"""Summarize the active p23 y-filtered nonsplit fallback probability window.

This helper is for the post-50B fallback shard.  It conditions on a clean
50B all-X1(16) miss and then models accepted nonsplit trials as multiplying
the all-X1 hazard by a chosen lift.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path


P = 100000000000000000000117
SQRT_P = 316227766016
BASE_EXPECTED = 34_600_000_000.0
DEFAULT_MISS_TRIALS = 50_000_000_000
DEFAULT_LIFTS = [1.3, 1.5, 2.1, 2.5]
DEFAULT_TARGETS = [5_000_000_000, 10_000_000_000, 25_000_000_000, 50_000_000_000, 75_000_000_000]
DEFAULT_SENSITIVITY_PRIORS = [(0.4, 1.2), (0.1, 1.2), (0.05, 1.0)]


def latest_trials_from_log(path: Path) -> int:
    latest = 0
    pat = re.compile(r"\btrials=(\d+)\b")
    try:
        for line in path.read_text(errors="replace").splitlines():
            match = pat.search(line)
            if match:
                latest = int(match.group(1))
    except FileNotFoundError:
        return 0
    return latest


def aggregate_trials(run_dir: Path) -> int:
    return sum(latest_trials_from_log(path) for path in sorted(run_dir.glob("worker*.log")))


def posterior_l_grid(
    all_x1_miss_trials: int,
    nonsplit_trials: int = 0,
    lift: float = 1.0,
    lo: float = 0.4,
    hi: float = 1.2,
    step: float = 0.01,
) -> list[tuple[float, float]]:
    """Uniform-grid posterior after no hit through all-X1 miss plus fallback."""
    values: list[tuple[float, float]] = []
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        L = lo + i * step
        exposure = all_x1_miss_trials + lift * nonsplit_trials
        likelihood = math.exp(-exposure * L / BASE_EXPECTED)
        values.append((L, likelihood))
    total = sum(w for _L, w in values)
    return [(L, w / total) for L, w in values]


def weighted_quantile(grid: list[tuple[float, float]], q: float) -> float:
    acc = 0.0
    for value, weight in grid:
        acc += weight
        if acc >= q:
            return value
    return grid[-1][0]


def posterior_summary(grid: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    mean = sum(L * w for L, w in grid)
    return (
        mean,
        weighted_quantile(grid, 0.10),
        weighted_quantile(grid, 0.50),
        weighted_quantile(grid, 0.90),
    )


def posterior_predictive_hit(grid: list[tuple[float, float]], accepted_trials: int, lift: float) -> float:
    return sum(
        w * (1.0 - math.exp(-accepted_trials * L * lift / BASE_EXPECTED))
        for L, w in grid
    )


def parse_prior_range(text: str) -> tuple[float, float]:
    if ":" not in text:
        raise argparse.ArgumentTypeError("prior ranges must be LO:HI")
    lo_s, hi_s = text.split(":", 1)
    try:
        lo = float(lo_s)
        hi = float(hi_s)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("prior ranges must be numeric LO:HI") from exc
    if lo <= 0 or hi <= lo:
        raise argparse.ArgumentTypeError("prior ranges require 0 < LO < HI")
    return lo, hi


def print_lift_table(
    *,
    all_x1_miss_trials: int,
    trials: int,
    lifts: list[float],
    targets: list[int],
    prior_lo: float,
    prior_hi: float,
    prior_step: float,
    label: str,
) -> None:
    print(f"prior={label} L~Uniform({prior_lo:.3g},{prior_hi:.3g})")
    print("lift no_hit_since_fallback hit_from_now_by_accepted_targets posterior_mean_L posterior_L_q10_q50_q90")
    for lift in lifts:
        miss_grid = posterior_l_grid(
            all_x1_miss_trials,
            lo=prior_lo,
            hi=prior_hi,
            step=prior_step,
        )
        no_hit_since_fallback = sum(
            w * math.exp(-trials * L * lift / BASE_EXPECTED)
            for L, w in miss_grid
        )
        current_grid = posterior_l_grid(
            all_x1_miss_trials,
            trials,
            lift,
            lo=prior_lo,
            hi=prior_hi,
            step=prior_step,
        )
        fields = []
        for target in targets:
            remaining = max(0, target - trials)
            conditional_hit = posterior_predictive_hit(current_grid, remaining, lift)
            fields.append(f"{target // 1_000_000_000}B:{conditional_hit:.4f}")

        mean, q10, q50, q90 = posterior_summary(current_grid)
        print(
            f"{lift:.2f} {no_hit_since_fallback:.4f} {' '.join(fields)} "
            f"{mean:.3f} {q10:.3f}/{q50:.3f}/{q90:.3f}"
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", nargs="?", type=Path, help="run directory; defaults to /tmp/p23_run_dir.txt")
    ap.add_argument("--all-x1-miss-trials", type=int, default=DEFAULT_MISS_TRIALS)
    ap.add_argument("--lifts", nargs="*", type=float, default=DEFAULT_LIFTS)
    ap.add_argument("--targets", nargs="*", type=int, default=DEFAULT_TARGETS)
    ap.add_argument("--prior-lo", type=float, default=0.4)
    ap.add_argument("--prior-hi", type=float, default=1.2)
    ap.add_argument("--prior-step", type=float, default=0.01)
    ap.add_argument(
        "--sensitivity",
        action="store_true",
        help="also print standing and pessimistic prior sensitivity ranges",
    )
    ap.add_argument(
        "--sensitivity-prior",
        action="append",
        type=parse_prior_range,
        default=[],
        metavar="LO:HI",
        help="extra prior range for --sensitivity; may be repeated",
    )
    args = ap.parse_args()
    if args.prior_lo <= 0 or args.prior_hi <= args.prior_lo:
        raise SystemExit("--prior-lo/--prior-hi require 0 < prior-lo < prior-hi")
    if args.prior_step <= 0:
        raise SystemExit("--prior-step must be positive")

    run_dir = args.run_dir
    if run_dir is None:
        txt = Path("/tmp/p23_run_dir.txt")
        if not txt.exists():
            raise SystemExit("/tmp/p23_run_dir.txt not found; pass run_dir explicitly")
        run_dir = Path(txt.read_text().strip())
    if not run_dir.is_dir():
        raise SystemExit(f"run directory not found: {run_dir}")

    trials = aggregate_trials(run_dir)
    print(f"run_dir={run_dir}")
    print(f"p={P}")
    print(f"accepted_nonsplit_trials={trials}")
    print(f"accepted_nonsplit_billions={trials / 1e9:.3f}")
    print(f"fraction_of_sqrt_p_accepted_trials={trials / SQRT_P:.6f}")
    print(f"conditioned_all_x1_miss_trials={args.all_x1_miss_trials}")
    print()
    print("model=E_all_x1_trials_34.6B_over_L_then_nonsplit_hazard_lift")
    print_lift_table(
        all_x1_miss_trials=args.all_x1_miss_trials,
        trials=trials,
        lifts=args.lifts,
        targets=args.targets,
        prior_lo=args.prior_lo,
        prior_hi=args.prior_hi,
        prior_step=args.prior_step,
        label="main",
    )

    if args.sensitivity:
        seen = {(args.prior_lo, args.prior_hi)}
        ranges = [*DEFAULT_SENSITIVITY_PRIORS, *args.sensitivity_prior]
        for prior_lo, prior_hi in ranges:
            if (prior_lo, prior_hi) in seen:
                continue
            seen.add((prior_lo, prior_hi))
            print()
            print_lift_table(
                all_x1_miss_trials=args.all_x1_miss_trials,
                trials=trials,
                lifts=args.lifts,
                targets=args.targets,
                prior_lo=prior_lo,
                prior_hi=prior_hi,
                prior_step=args.prior_step,
                label="sensitivity",
            )


if __name__ == "__main__":
    main()

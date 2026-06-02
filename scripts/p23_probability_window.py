#!/usr/bin/env python3
"""Summarize the current p23 X1(16) hit-probability window.

This is an interpretive helper for the active p23 search. It reads worker logs,
computes aggregate latest progress, and applies the local heuristic model:

    E[trials] ~= 34.6B / L

where L is the liftability factor from the X1(16)+halving notes.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path


P = 100000000000000000000117
SQRT_P = 316227766016
BASE_EXPECTED = 34_600_000_000.0
DEFAULT_L_VALUES = [1.0, 0.9, 0.8, 0.67, 0.5]
DEFAULT_TARGETS = [35_000_000_000, 45_000_000_000, 50_000_000_000, 75_000_000_000, 100_000_000_000]
DEFAULT_CONTINGENCY_AFTER = 50_000_000_000
DEFAULT_NONSPLIT_LIFTS = [1.3, 1.5, 2.1, 2.5]
DEFAULT_NONSPLIT_TARGETS = [25_000_000_000, 50_000_000_000, 75_000_000_000]


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


def posterior_l_grid(trials: int, lo: float = 0.4, hi: float = 1.2, step: float = 0.01) -> list[tuple[float, float]]:
    """Uniform-grid posterior after no hit, using likelihood exp(-trials/E[L])."""
    values: list[tuple[float, float]] = []
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        L = lo + i * step
        likelihood = math.exp(-trials * L / BASE_EXPECTED)
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


def posterior_predictive_hit(grid: list[tuple[float, float]], accepted_trials: int, hazard_lift: float = 1.0) -> float:
    """Predict hit probability for a future accepted-trial budget."""
    return sum(
        w * (1.0 - math.exp(-accepted_trials * L * hazard_lift / BASE_EXPECTED))
        for L, w in grid
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", nargs="?", type=Path, help="run directory; defaults to /tmp/p23_run_dir.txt")
    ap.add_argument("--l-values", nargs="*", type=float, default=DEFAULT_L_VALUES)
    ap.add_argument("--targets", nargs="*", type=int, default=DEFAULT_TARGETS)
    ap.add_argument("--contingency-after", type=int, default=DEFAULT_CONTINGENCY_AFTER)
    ap.add_argument("--nonsplit-lifts", nargs="*", type=float, default=DEFAULT_NONSPLIT_LIFTS)
    ap.add_argument("--nonsplit-targets", nargs="*", type=int, default=DEFAULT_NONSPLIT_TARGETS)
    args = ap.parse_args()

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
    print(f"aggregate_latest_trials={trials}")
    print(f"aggregate_latest_billions={trials / 1e9:.3f}")
    print(f"fraction_of_sqrt_p={trials / SQRT_P:.6f}")
    print()
    print("model=E_trials_34.6B_over_L")
    print("L expected_B no_hit_now conditional_hit_by_targets")
    for L in args.l_values:
        expected = BASE_EXPECTED / L
        no_hit_now = math.exp(-trials / expected)
        fields = []
        for target in args.targets:
            remaining = max(0, target - trials)
            conditional_hit = 1.0 - math.exp(-remaining / expected)
            fields.append(f"{target // 1_000_000_000}B:{conditional_hit:.4f}")
        print(f"{L:.2f} {expected / 1e9:.3f} {no_hit_now:.4f} {' '.join(fields)}")

    grid = posterior_l_grid(trials)
    mean, q10, q50, q90 = posterior_summary(grid)
    print()
    print("rough_uniform_grid_posterior_after_no_hit")
    print("prior_L_range=0.40..1.20")
    print(f"posterior_mean_L={mean:.3f}")
    print(f"posterior_L_q10={q10:.3f}")
    print(f"posterior_L_q50={q50:.3f}")
    print(f"posterior_L_q90={q90:.3f}")

    miss_grid = posterior_l_grid(args.contingency_after)
    miss_mean, miss_q10, miss_q50, miss_q90 = posterior_summary(miss_grid)
    print()
    print("contingency_after_all_x1_miss")
    print(f"conditioned_miss_trials={args.contingency_after}")
    print(f"posterior_mean_L={miss_mean:.3f}")
    print(f"posterior_L_q10={miss_q10:.3f}")
    print(f"posterior_L_q50={miss_q50:.3f}")
    print(f"posterior_L_q90={miss_q90:.3f}")
    print()
    print("next_nonsplit_shard_posterior_predictive")
    print("probabilities use accepted nonsplit trials; wall-clock speed also depends on accepted-trial rate")
    print("lift accepted_trial_targets")
    for lift in args.nonsplit_lifts:
        fields = []
        for target in args.nonsplit_targets:
            hit_prob = posterior_predictive_hit(miss_grid, target, lift)
            fields.append(f"{target // 1_000_000_000}B:{hit_prob:.4f}")
        print(f"{lift:.2f} {' '.join(fields)}")


if __name__ == "__main__":
    main()

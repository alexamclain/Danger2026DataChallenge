#!/usr/bin/env python3
"""Aggregate paired all-X1 and nonsplit branchstats logs.

The branchstats diagnostics print per-depth first-branch and all-branch
survival counts.  This helper combines paired holdouts and reports how much
the y-filtered nonsplit stream enriches bounded 2-adic survival.
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BranchLog:
    path: Path
    samples: int
    depths: dict[int, tuple[int, int]] = field(default_factory=dict)


def parse_branch_log(path: Path) -> BranchLog:
    samples = 0
    depths: dict[int, tuple[int, int]] = {}
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"samples = (\d+)$", line)
        if m:
            samples = int(m.group(1))
            continue
        parts = line.split()
        if len(parts) == 8 and parts[0].isdigit():
            depth = int(parts[0])
            first = int(parts[1])
            all_branch = int(parts[3])
            depths[depth] = (first, all_branch)
    if samples <= 0 or not depths:
        raise ValueError(f"could not parse branchstats log: {path}")
    return BranchLog(path=path, samples=samples, depths=depths)


def split_pair(text: str) -> tuple[Path, Path]:
    if ":" not in text:
        raise argparse.ArgumentTypeError("--pair must be ALL_LOG:NONSPLIT_LOG")
    left, right = text.split(":", 1)
    return Path(left), Path(right)


def ratio_ci(ratio: float, numerator_hits: int, denominator_hits: int, z: float = 1.96) -> tuple[float, float]:
    if ratio <= 0 or numerator_hits <= 0 or denominator_hits <= 0:
        return 0.0, float("inf")
    se = math.sqrt(1.0 / numerator_hits + 1.0 / denominator_hits)
    return ratio * math.exp(-z * se), ratio * math.exp(z * se)


def fmt_ci(lo: float, hi: float) -> str:
    if math.isinf(hi):
        return "[0,inf]"
    return f"[{lo:.3f},{hi:.3f}]"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--pair",
        action="append",
        type=split_pair,
        required=True,
        metavar="ALL_LOG:NONSPLIT_LOG",
        help="paired all-X1 and y-filtered nonsplit branchstats logs",
    )
    ap.add_argument("--depths", nargs="*", type=int, default=[12, 14, 16, 18, 20])
    args = ap.parse_args()

    totals: dict[int, dict[str, int]] = {}
    total_all_samples = 0
    total_nonsplit_samples = 0
    print("pairs:")
    for all_path, nonsplit_path in args.pair:
        all_log = parse_branch_log(all_path)
        nonsplit_log = parse_branch_log(nonsplit_path)
        total_all_samples += all_log.samples
        total_nonsplit_samples += nonsplit_log.samples
        print(f"  all={all_path}")
        print(f"  nonsplit={nonsplit_path}")
        for depth in set(all_log.depths) | set(nonsplit_log.depths):
            af, aa = all_log.depths.get(depth, (0, 0))
            nf, na = nonsplit_log.depths.get(depth, (0, 0))
            row = totals.setdefault(depth, {"af": 0, "aa": 0, "nf": 0, "na": 0})
            row["af"] += af
            row["aa"] += aa
            row["nf"] += nf
            row["na"] += na

    print()
    print(f"all_samples={total_all_samples}")
    print(f"nonsplit_samples={total_nonsplit_samples}")
    print(
        "depth all_first_rate all_all_rate nonsplit_first_rate nonsplit_all_rate "
        "lift_vs_all_first lift_vs_all_first_approx95 lift_vs_all_all lift_vs_all_all_approx95 "
        "nonsplit_first_equals_all"
    )
    for depth in args.depths:
        if depth not in totals:
            continue
        row = totals[depth]
        af, aa, nf, na = row["af"], row["aa"], row["nf"], row["na"]
        afr = af / total_all_samples if total_all_samples else 0.0
        aar = aa / total_all_samples if total_all_samples else 0.0
        nfr = nf / total_nonsplit_samples if total_nonsplit_samples else 0.0
        nar = na / total_nonsplit_samples if total_nonsplit_samples else 0.0
        lift_first = nfr / afr if afr else 0.0
        lift_all = nfr / aar if aar else 0.0
        lf_lo, lf_hi = ratio_ci(lift_first, nf, af)
        la_lo, la_hi = ratio_ci(lift_all, nf, aa)
        print(
            f"{depth} {afr:.9f} {aar:.9f} {nfr:.9f} {nar:.9f} "
            f"{lift_first:.3f} {fmt_ci(lf_lo, lf_hi)} "
            f"{lift_all:.3f} {fmt_ci(la_lo, la_hi)} {nf == na}"
        )


if __name__ == "__main__":
    main()

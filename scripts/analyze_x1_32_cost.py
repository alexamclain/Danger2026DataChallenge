#!/usr/bin/env python3
"""Compare X1(32) prototype survival against X1(16) baselines.

This reads logs from scripts/x1_32_small_prime_probe.py and matching
X1(16) branchstats logs.  It reports the density-side gain and the sampler-rate
bar a production X1(32) implementation would need to clear relative to the
active y-filtered nonsplit X1(16) baseline.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class X132Log:
    path: Path
    p: int
    target_depth: int
    mapped: int
    fibers_per_second: float
    roots_per_second: float
    survival: dict[int, tuple[int, float]]


@dataclass
class BranchLog:
    path: Path
    p: int
    samples: int
    first_rate: dict[int, float]
    all_rate: dict[int, float]


def parse_x1_32(path: Path) -> X132Log:
    p = 0
    target_depth = 0
    mapped = 0
    fibers_per_second = 0.0
    roots_per_second = 0.0
    survival: dict[int, tuple[int, float]] = {}
    in_survival = False
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("p="):
            p = int(line.split("=", 1)[1])
        elif line.startswith("target_depth="):
            target_depth = int(line.split("=", 1)[1])
        elif line.startswith("mapped_montgomery_tate="):
            mapped = int(line.split("=", 1)[1])
        elif line.startswith("fibers_per_second="):
            fibers_per_second = float(line.split("=", 1)[1])
        elif line.startswith("roots_per_second="):
            roots_per_second = float(line.split("=", 1)[1])
        elif line.startswith("first_branch_survival_tate depth count rate"):
            in_survival = True
        elif in_survival:
            parts = line.split()
            if len(parts) == 3 and parts[0].isdigit():
                survival[int(parts[0])] = (int(parts[1]), float(parts[2]))
            elif parts and not parts[0].isdigit():
                in_survival = False
    if not (p and target_depth and mapped and survival):
        raise ValueError(f"could not parse X1(32) log: {path}")
    return X132Log(path, p, target_depth, mapped, fibers_per_second, roots_per_second, survival)


def parse_branch(path: Path) -> BranchLog:
    p = 0
    samples = 0
    first_rate: dict[int, float] = {}
    all_rate: dict[int, float] = {}
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"p = (\d+)$", line)
        if m:
            p = int(m.group(1))
            continue
        m = re.match(r"samples = (\d+)$", line)
        if m:
            samples = int(m.group(1))
            continue
        parts = line.split()
        if len(parts) == 8 and parts[0].isdigit():
            depth = int(parts[0])
            first_rate[depth] = float(parts[2])
            all_rate[depth] = float(parts[4])
    if not (p and samples and first_rate):
        raise ValueError(f"could not parse branch log: {path}")
    return BranchLog(path, p, samples, first_rate, all_rate)


def split_pair(text: str) -> tuple[Path, Path]:
    if ":" not in text:
        raise argparse.ArgumentTypeError("--pair must be X132_LOG:X16_BRANCH_LOG")
    left, right = text.split(":", 1)
    return Path(left), Path(right)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", action="append", type=split_pair, required=True)
    ap.add_argument(
        "--nonsplit-lift",
        nargs="*",
        type=float,
        default=[1.5, 1.8, 2.1],
        help="scenario lifts of active nonsplit over all-X1 first branch",
    )
    args = ap.parse_args()

    print("pair p depth x132_rate x16_first_rate x16_all_rate x132_over_x16_first x132_over_x16_all")
    for i, (x132_path, x16_path) in enumerate(args.pair, 1):
        x132 = parse_x1_32(x132_path)
        x16 = parse_branch(x16_path)
        if x132.p != x16.p:
            raise SystemExit(f"p mismatch for pair {i}: {x132.p} vs {x16.p}")
        depth = x132.target_depth
        if depth not in x132.survival or depth not in x16.first_rate:
            raise SystemExit(f"depth {depth} missing for pair {i}")
        x132_rate = x132.survival[depth][1]
        x16_first = x16.first_rate[depth]
        x16_all = x16.all_rate.get(depth, 0.0)
        over_first = x132_rate / x16_first if x16_first else 0.0
        over_all = x132_rate / x16_all if x16_all else 0.0
        print(
            f"{i} {x132.p} {depth} {x132_rate:.9f} {x16_first:.9f} "
            f"{x16_all:.9f} {over_first:.3f} {over_all:.3f}"
        )
        print(
            f"  python_fibers_per_second={x132.fibers_per_second:.3f} "
            f"python_roots_per_second={x132.roots_per_second:.3f} mapped={x132.mapped}"
        )
        for lift in args.nonsplit_lift:
            ratio = over_first / lift if lift else 0.0
            print(
                f"  vs_active_nonsplit_lift_{lift:.2f}: "
                f"hazard_ratio_x132_over_nonsplit={ratio:.3f} "
                f"required_x132_sampler_rate_fraction_of_nonsplit={1.0 / ratio if ratio > 0 else 0.0:.3f}"
            )


if __name__ == "__main__":
    main()

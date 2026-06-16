#!/usr/bin/env python3
"""Summarize fast exact X1(16) trace-convolution calibration logs."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Row:
    path: Path
    p: int = 0
    elapsed: float = 0.0
    rows: int = 0
    all_L: float = 0.0
    nonsplit_L: float = 0.0
    split_L: float = 0.0
    nonsplit_rates: dict[int, float] = field(default_factory=dict)
    split_rates: dict[int, float] = field(default_factory=dict)


def parse_log(path: Path) -> Row:
    row = Row(path=path)
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("p="):
            row.p = int(line.split("=", 1)[1])
        elif line.startswith("elapsed_seconds="):
            row.elapsed = float(line.split("=", 1)[1])
        elif line.startswith("candidate_rows_with_root_multiplicity="):
            row.rows = int(line.split("=", 1)[1])
        elif line.startswith("all_x16 "):
            match = re.search(r"L_trace=([0-9.]+)", line)
            if match:
                row.all_L = float(match.group(1))
        elif line.startswith("nonsplit_x16 "):
            match = re.search(r"L_trace=([0-9.]+)", line)
            if match:
                row.nonsplit_L = float(match.group(1))
        elif line.startswith("split_x16 "):
            match = re.search(r"L_trace=([0-9.]+)", line)
            if match:
                row.split_L = float(match.group(1))
        elif line.startswith("nonsplit:ge"):
            parts = line.split()
            for part in parts:
                if part.startswith("nonsplit:ge"):
                    depth_s, rest = part.split("=", 1)
                    depth = int(depth_s.removeprefix("nonsplit:ge"))
                    rate = float(rest.rsplit(":", 1)[1])
                    row.nonsplit_rates[depth] = rate
                elif part.startswith("split:ge"):
                    depth_s, rest = part.split("=", 1)
                    depth = int(depth_s.removeprefix("split:ge"))
                    rate = float(rest.rsplit(":", 1)[1])
                    row.split_rates[depth] = rate
    return row


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    n = len(values)
    if n % 2:
        return values[n // 2]
    return 0.5 * (values[n // 2 - 1] + values[n // 2])


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+", type=Path)
    ap.add_argument("--large-threshold", type=int, default=50_000)
    ap.add_argument("--depths", nargs="*", type=int, default=[5, 6, 7, 8, 9, 10, 11, 12])
    args = ap.parse_args()

    rows = [parse_log(path) for path in args.logs]
    rows = [row for row in rows if row.p > 0 and row.rows > 0]
    rows.sort(key=lambda r: r.p)
    large = [row for row in rows if row.p >= args.large_threshold]

    print("X1(16) fast trace-convolution calibration rollup")
    print(f"logs={len(rows)}")
    print(f"large_threshold={args.large_threshold}")
    print()
    print("p rows elapsed_s all_L nonsplit_L split_L split_over_nonsplit")
    for row in rows:
        ratio = row.split_L / row.nonsplit_L if row.nonsplit_L else 0.0
        print(
            f"{row.p} {row.rows} {row.elapsed:.3f} "
            f"{row.all_L:.3f} {row.nonsplit_L:.3f} {row.split_L:.3f} {ratio:.3f}"
        )

    print()
    for label, subset in [("all_rows", rows), ("large_rows", large)]:
        ns = [row.nonsplit_L for row in subset]
        sp = [row.split_L for row in subset]
        ratios = [row.split_L / row.nonsplit_L for row in subset if row.nonsplit_L]
        print(f"group={label} count={len(subset)}")
        print(
            f"  nonsplit_L min/mean/median/max="
            f"{min(ns):.3f}/{mean(ns):.3f}/{median(ns):.3f}/{max(ns):.3f}"
            if ns else "  nonsplit_L none"
        )
        print(
            f"  split_L min/mean/median/max="
            f"{min(sp):.3f}/{mean(sp):.3f}/{median(sp):.3f}/{max(sp):.3f}"
            if sp else "  split_L none"
        )
        print(
            f"  split_over_nonsplit min/mean/median/max="
            f"{min(ratios):.3f}/{mean(ratios):.3f}/{median(ratios):.3f}/{max(ratios):.3f}"
            if ratios else "  split_over_nonsplit none"
        )
        print("  nonsplit_v2_geometric_ratios")
        for depth in args.depths:
            if depth < 4:
                continue
            baseline = 2.0 ** (4 - depth)
            vals = [
                row.nonsplit_rates[depth] / baseline
                for row in subset
                if depth in row.nonsplit_rates and baseline
            ]
            if vals:
                print(
                    f"    d={depth}: "
                    f"min/mean/median/max={min(vals):.3f}/{mean(vals):.3f}/"
                    f"{median(vals):.3f}/{max(vals):.3f}"
                )
        print()


if __name__ == "__main__":
    main()

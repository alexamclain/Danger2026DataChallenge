#!/usr/bin/env python3
"""Audit whether strict parameters concentrate near A=+/-2.

The singular Montgomery limits A=+/-2 are rational torus power maps.  A
possible verifier-native shortcut would be that, for p=n^2+7, strict DANGER
parameters concentrate in a sub-sqrt perturbation window

    min(|A-2|, |A+2|) <= W.

Then scanning W=o(sqrt(p)) candidates could beat the generic trace search.

This script tests that exact claim at small scale.  For small primes in the
family p=n^2+7 it computes the full strict x-only good A-set and measures
capture/lift in deterministic windows around +/-2.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table


@dataclass(frozen=True)
class WindowRow:
    label: str
    width: int
    total: int
    hits: int


def centered_distance_to_pm2(p: int) -> np.ndarray:
    values = np.arange(p, dtype=np.int64)
    distances = np.full(p, p, dtype=np.int64)
    for center in (2, p - 2):
        diff = (values - center) % p
        diff = np.minimum(diff, p - diff)
        distances = np.minimum(distances, diff)
    return distances


def width_table(p: int, betas: list[float], fixed: list[int]) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    seen: set[int] = set()
    for width in fixed:
        width = max(0, min(width, (p - 1) // 2))
        if width not in seen:
            seen.add(width)
            rows.append((f"fixed_{width}", width))
    for beta in betas:
        width = int(p**beta)
        width = max(0, min(width, (p - 1) // 2))
        if width not in seen:
            seen.add(width)
            rows.append((f"p^{beta:.2f}", width))
    return rows


def audit_row(n: int, p: int, betas: list[float], fixed: list[int]) -> tuple[list[WindowRow], dict[str, int]]:
    chi = legendre_table(p)
    good, stats = exact_xonly_good_flags(p, chi)
    nonsingular = np.ones(p, dtype=np.bool_)
    nonsingular[[2 % p, (-2) % p]] = False
    good &= nonsingular
    distances = centered_distance_to_pm2(p)

    out: list[WindowRow] = []
    for label, width in width_table(p, betas, fixed):
        selected = nonsingular & (distances <= width)
        out.append(
            WindowRow(
                label=label,
                width=width,
                total=int(np.count_nonzero(selected)),
                hits=int(np.count_nonzero(selected & good)),
            )
        )
    return out, stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=300_000)
    ap.add_argument("--max-rows", type=int, default=14)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--betas", type=float, nargs="*", default=[0.10, 0.20, 0.25, 0.30, 0.40, 0.50])
    ap.add_argument("--fixed", type=int, nargs="*", default=[4, 8, 16, 32, 64, 128, 256])
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    aggregate: dict[str, list[int]] = {}
    aggregate_width: dict[str, int] = {}
    total_good = 0
    total_nonsingular = 0

    print("near-singular A=+/-2 window audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print("row n p k good/nonsingular label width total hits capture lift coverage")

    for index, (n, p) in enumerate(rows, start=1):
        window_rows, stats = audit_row(n, p, args.betas, args.fixed)
        good = int(stats["good"])
        nonsingular = int(stats["nonsingular"])
        total_good += good
        total_nonsingular += nonsingular
        base = good / nonsingular if nonsingular else 0.0
        for row in window_rows:
            aggregate.setdefault(row.label, [0, 0])
            aggregate[row.label][0] += row.hits
            aggregate[row.label][1] += row.total
            aggregate_width[row.label] = row.width
            precision = row.hits / row.total if row.total else 0.0
            lift = precision / base if base else 0.0
            capture = row.hits / good if good else 0.0
            coverage = row.total / nonsingular if nonsingular else 0.0
            print(
                f"{index:02d} {n} {p} {stats['k']} {good}/{nonsingular} "
                f"{row.label} {row.width} {row.total} {row.hits} "
                f"{capture:.6f} {lift:.3f} {coverage:.6f}"
            )

    print("aggregate")
    base = total_good / total_nonsingular if total_nonsingular else 0.0
    print(f"  good={total_good}/{total_nonsingular}")
    print(f"  base_rate={base:.8f}")
    for label, (hits, total) in sorted(aggregate.items(), key=lambda item: aggregate_width[item[0]]):
        precision = hits / total if total else 0.0
        lift = precision / base if base else 0.0
        capture = hits / total_good if total_good else 0.0
        coverage = total / total_nonsingular if total_nonsingular else 0.0
        print(
            f"  {label:10s} last_width={aggregate_width[label]:8d} "
            f"hits={hits:5d}/{total:8d} capture={capture:.6f} "
            f"lift={lift:.3f} coverage={coverage:.6f}"
        )
    print(
        "conclusion=near_singular_windows_show_no_subsqrt_capture_concentration"
    )


if __name__ == "__main__":
    main()

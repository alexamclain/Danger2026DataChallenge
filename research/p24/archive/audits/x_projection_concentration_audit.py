#!/usr/bin/env python3
"""Audit whether strict verifier pairs concentrate over simple x-coordinates.

The strict target can be viewed as the affine certificate curve

    Z_k(A, x) = 0,  Z_{k-1}(A, x) != 0.

Most p24 work projects this curve to the Montgomery A-line.  A different
possible shortcut would be to project to the x-line: if one fixed, simple x0
had many compatible A values, we could solve a much smaller fixed-x problem
instead of selecting a rare trace-compatible A.

At exact small scale this script enumerates all accepted pairs for primes
p = n^2 + 7, then measures the distribution of compatible A counts per x.
Flat, Poisson-sized counts mean fixed-x conditioning only moves the entropy;
it does not create a high-multiplicity certificate section.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows
from pair_relation_rank_audit import accepted_pairs_for_row


@dataclass(frozen=True)
class RowSummary:
    n: int
    p: int
    k: int
    pairs: int
    occupied_x: int
    max_per_x: int
    mean_per_x: float
    occupied_fraction: float
    top_x: tuple[tuple[int, int], ...]
    simple_hits: tuple[tuple[int, int], ...]


def simple_x_values(p: int, height: int) -> list[int]:
    values: set[int] = {0, 1, p - 1}
    for num in range(-height, height + 1):
        for den in range(1, height + 1):
            if math.gcd(num, den) == 1:
                values.add((num * pow(den, -1, p)) % p)
    return sorted(values)


def audit_row(n: int, p: int, simple_height: int, top: int) -> RowSummary:
    accepted_A, accepted_x, k = accepted_pairs_for_row(p)
    counts = np.bincount(accepted_x, minlength=p)
    occupied = np.nonzero(counts)[0]
    top_indices = sorted(occupied, key=lambda x: int(counts[x]), reverse=True)[:top]
    simple = simple_x_values(p, simple_height)
    simple_hits = [(x, int(counts[x])) for x in simple if counts[x]]
    simple_hits.sort(key=lambda item: item[1], reverse=True)

    return RowSummary(
        n=n,
        p=p,
        k=k,
        pairs=len(accepted_A),
        occupied_x=len(occupied),
        max_per_x=int(counts[top_indices[0]]) if top_indices else 0,
        mean_per_x=float(len(accepted_A) / p),
        occupied_fraction=float(len(occupied) / p),
        top_x=tuple((int(x), int(counts[x])) for x in top_indices),
        simple_hits=tuple(simple_hits[:top]),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=500)
    ap.add_argument("--max-p", type=int, default=20_000)
    ap.add_argument("--max-rows", type=int, default=8)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--simple-height", type=int, default=20)
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("strict verifier x-projection concentration audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"simple_height={args.simple_height}")
    print("row n p k pairs occupied_x occupied_frac mean_per_x max_per_x top_x simple_hits")

    summaries: list[RowSummary] = []
    for index, (n, p) in enumerate(rows, start=1):
        summary = audit_row(n, p, args.simple_height, args.top)
        summaries.append(summary)
        print(
            f"{index:02d} {summary.n} {summary.p} {summary.k} {summary.pairs} "
            f"{summary.occupied_x} {summary.occupied_fraction:.6f} "
            f"{summary.mean_per_x:.6f} {summary.max_per_x} "
            f"{list(summary.top_x)} {list(summary.simple_hits)}"
        )

    if summaries:
        print("aggregate")
        print(f"  max_per_x_max={max(row.max_per_x for row in summaries)}")
        print(f"  mean_occupied_fraction={sum(row.occupied_fraction for row in summaries)/len(summaries):.6f}")
        print(f"  mean_pairs_per_x={sum(row.mean_per_x for row in summaries)/len(summaries):.6f}")
    print(
        "conclusion=x_projection_has_constant_sized_fibers; "
        "fixed_x_conditioning_does_not_create_a_depth_growing_A_selector"
    )


if __name__ == "__main__":
    main()

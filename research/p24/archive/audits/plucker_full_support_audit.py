#!/usr/bin/env python3
"""Audit full Pluecker support of the axis coefficient subspace.

The sliding-window product only checks cyclic interval minors.  A stronger
Grassmannian condition is full Pluecker support: every `r x r` coordinate minor
of the axis subspace is nonzero.  This is the finite-field analogue of a
uniform matroid/MDS generator matrix.

If full support holds generically in the same windows, then cyclic interval
minor success is even less CM-specific.  If it fails while interval minors
survive, then the interval theorem is genuinely weaker and more targeted.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from cyclic_superregular_random_baseline import (
    first_case,
    monomial_transforms,
    random_full_rank_vectors,
)


def det_mod(matrix: list[list[int]], q: int) -> int:
    mat = [row[:] for row in matrix]
    n = len(mat)
    det = 1
    sign = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            sign = -sign
        pivot_value = mat[col][col] % q
        det = (det * pivot_value) % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            factor = (mat[row][col] % q) * inv % q
            if factor:
                mat[row] = [
                    (left - factor * right) % q
                    for left, right in zip(mat[row], mat[col])
                ]
    return det if sign > 0 else (-det) % q


def plucker_counts(vectors: list[list[int]], q: int) -> tuple[int, int]:
    r = len(vectors)
    d = len(vectors[0]) if vectors else 0
    total = 0
    zeros = 0
    for cols in combinations(range(d), r):
        total += 1
        matrix = [[row[col] % q for col in cols] for row in vectors]
        if det_mod(matrix, q) == 0:
            zeros += 1
    return total, zeros


def interval_zero_count(vectors: list[list[int]], transforms: list[list[list[int]]], q: int) -> int:
    r = len(vectors)
    zeros = 0
    for transform in transforms:
        shifted = []
        for vector in vectors:
            out = [0] * len(vector)
            for coeff, image in zip(vector, transform):
                c = coeff % q
                if c:
                    out = [(left + c * right) % q for left, right in zip(out, image)]
            shifted.append(out)
        matrix = [[row[col] % q for col in range(r)] for row in shifted]
        zeros += int(det_mod(matrix, q) == 0)
    return zeros


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=12)
    parser.add_argument("--max-factor-degree", type=int, default=20)
    parser.add_argument("--max-plucker-total", type=int, default=10000)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    case = first_case(args)
    if case is None:
        raise SystemExit("no eligible case found")

    q = case.q
    r = len(case.vectors)
    d = case.factor.degree()
    import math

    plucker_total_est = math.comb(d, r)
    if plucker_total_est > args.max_plucker_total:
        raise SystemExit(
            f"too many Pluecker minors: C({d},{r})={plucker_total_est}; "
            "raise --max-plucker-total if intended"
        )

    transforms = monomial_transforms(case.factor, case.n, q)
    total, cm_zero = plucker_counts(case.vectors, q)
    cm_interval_zero = interval_zero_count(case.vectors, transforms, q)

    import random

    rng = random.Random(args.seed)
    random_full_support = 0
    random_plucker_zero_min: int | None = None
    random_plucker_zero_max = 0
    random_interval_failures = 0
    for _ in range(args.random_trials):
        vectors = random_full_rank_vectors(rng, r, d, q)
        _, zeros = plucker_counts(vectors, q)
        random_interval_zeros = interval_zero_count(vectors, transforms, q)
        random_full_support += int(zeros == 0)
        random_interval_failures += int(random_interval_zeros > 0)
        random_plucker_zero_min = zeros if random_plucker_zero_min is None else min(random_plucker_zero_min, zeros)
        random_plucker_zero_max = max(random_plucker_zero_max, zeros)

    print("Pluecker full-support audit")
    print(f"D={case.D}")
    print(f"q={case.q}")
    print(f"ell={case.ell}")
    print(f"h={case.h}")
    print(f"m={case.m}")
    print(f"n={case.n}")
    print(f"factor_degree={d}")
    print(f"axis_dim={r}")
    print(f"plucker_total={total}")
    print(f"random_trials={args.random_trials}")
    print()
    print("cm_axis")
    print(f"  plucker_zero_count={cm_zero}")
    print(f"  full_plucker_support={int(cm_zero == 0)}")
    print(f"  interval_zero_count={cm_interval_zero}")
    print()
    print("random_baseline")
    print(f"  full_plucker_support_trials={random_full_support}")
    print(f"  plucker_zero_min={random_plucker_zero_min if random_plucker_zero_min is not None else 'NA'}")
    print(f"  plucker_zero_max={random_plucker_zero_max}")
    print(f"  interval_failure_trials={random_interval_failures}")
    print()
    print("interpretation")
    print("  full_plucker_support_is_uniform_matroid_MDS_condition=1")
    print("  interval_support_only_is_weaker_cyclic_open_cell_condition=1")
    print("conclusion=reported_plucker_full_support_audit")


if __name__ == "__main__":
    main()

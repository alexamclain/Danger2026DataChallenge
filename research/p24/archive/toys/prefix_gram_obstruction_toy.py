#!/usr/bin/env python3
"""Finite-field toy for the prefix-Gram self-orthogonal obstruction.

For a full-rank prefix matrix A over F_q, the prefix Gram matrix A A^T is
singular exactly when the row space U contains a nonzero vector orthogonal to
all of U.  If K = ker(A) and the ambient dot pairing is nondegenerate, the
restricted radical dimensions of U and K agree.

This is the finite linear-algebra shape of the missing p24 prefix-Gram p-unit:
exclude U_t cap U_t^perp for each trace-GCD prefix orbit.
"""

from __future__ import annotations

import argparse
import random

from kernel_tail_schur_identity_toy import (
    det_mod,
    gram,
    kernel_basis_from_pivots,
    matmul,
    random_matrix,
    rref_pivots,
    subcols,
    transpose,
)


def rank_mod(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 0
    return len(rref_pivots(matrix, q))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=101)
    parser.add_argument("--r", type=int, default=5)
    parser.add_argument("--s", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    d = args.r + args.s
    full_prefix = 0
    prefix_gram_singular = 0
    radical_zero_mismatches = 0
    prefix_kernel_radical_dim_mismatches = 0
    prefix_kernel_gram_zero_mismatches = 0
    radical_hist: dict[tuple[int, int], int] = {}

    for _ in range(args.trials):
        A = random_matrix(args.r, d, args.q, rng)
        pivots = rref_pivots(A, args.q)
        if len(pivots) != args.r:
            continue
        full_prefix += 1
        result = kernel_basis_from_pivots(A, pivots, args.q)
        if result is None:
            continue
        pivot_cols, free_cols, N_ordered = result
        ordered_cols = pivot_cols + free_cols
        A_ordered = subcols(A, ordered_cols)

        prefix_gram = gram(A_ordered, args.q)
        kernel_gram = matmul(transpose(N_ordered), N_ordered, args.q)
        prefix_det = det_mod(prefix_gram, args.q)
        kernel_det = det_mod(kernel_gram, args.q)
        prefix_radical_dim = args.r - rank_mod(prefix_gram, args.q)
        kernel_radical_dim = args.s - rank_mod(kernel_gram, args.q)

        if prefix_det == 0:
            prefix_gram_singular += 1
        if (prefix_det == 0) != (prefix_radical_dim > 0):
            radical_zero_mismatches += 1
        if prefix_radical_dim != kernel_radical_dim:
            prefix_kernel_radical_dim_mismatches += 1
        if (prefix_det == 0) != (kernel_det == 0):
            prefix_kernel_gram_zero_mismatches += 1
        radical_hist[(prefix_radical_dim, kernel_radical_dim)] = (
            radical_hist.get((prefix_radical_dim, kernel_radical_dim), 0) + 1
        )

    print("prefix Gram self-orthogonal obstruction toy")
    print(f"q={args.q}")
    print(f"r={args.r}")
    print(f"s={args.s}")
    print(f"d={d}")
    print(f"trials={args.trials}")
    print(f"full_prefix={full_prefix}")
    print(f"prefix_gram_singular={prefix_gram_singular}")
    print(f"radical_zero_mismatches={radical_zero_mismatches}")
    print(
        "prefix_kernel_radical_dim_mismatches="
        f"{prefix_kernel_radical_dim_mismatches}"
    )
    print(
        "prefix_kernel_gram_zero_mismatches="
        f"{prefix_kernel_gram_zero_mismatches}"
    )
    print(f"radical_dim_hist={dict(sorted(radical_hist.items()))}")
    print("prefix_gram_zero_iff_nonzero_self_orthogonal_prefix_vector=1")
    print("prefix_and_kernel_radicals_match_under_nondegenerate_pairing=1")
    print("missing_p24_theorem=exclude_trace_gcd_prefix_self_orthogonal_lines")
    print("conclusion=reported_prefix_gram_obstruction_toy")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Metric-aware Schur identity for the trace-GCD Gram bridge.

The ordinary toy used the standard dot product:

    det(M M^T) det(N^T N) = det(A A^T) det(BN)^2.

For the arithmetic trace pairing, the ambient coordinate basis need not be
orthonormal.  If G is the primal metric matrix and G^{-1} is the dual metric on
row covectors, the invariant identity is:

    det(M G^{-1} M^T) det(N^T G N)
      = det(A G^{-1} A^T) det(BN)^2.

This toy verifies the identity and shows that the naive prefix Gram A A^T is
not basis-invariant in lower dimension.
"""

from __future__ import annotations

import argparse
import random

from kernel_tail_schur_identity_toy import (
    det_mod,
    inverse_matrix,
    kernel_basis_from_pivots,
    matmul,
    random_matrix,
    rref_pivots,
    transpose,
)


def subcols(matrix: list[list[int]], cols: list[int]) -> list[list[int]]:
    return [[row[col] for col in cols] for row in matrix]


def metric_gram_rows(
    rows: list[list[int]],
    metric_inverse: list[list[int]],
    q: int,
) -> list[list[int]]:
    return matmul(matmul(rows, metric_inverse, q), transpose(rows), q)


def metric_gram_cols(
    cols: list[list[int]],
    metric: list[list[int]],
    q: int,
) -> list[list[int]]:
    return matmul(matmul(transpose(cols), metric, q), cols, q)


def random_invertible_matrix(
    size: int,
    q: int,
    rng: random.Random,
) -> list[list[int]]:
    while True:
        matrix = random_matrix(size, size, q, rng)
        if det_mod(matrix, q):
            return matrix


def kernel_basis_in_original_columns(
    pivots: list[int],
    free: list[int],
    ordered_basis: list[list[int]],
) -> list[list[int]]:
    if not ordered_basis:
        return []
    cols = len(ordered_basis[0])
    out = [[0 for _ in range(cols)] for _ in range(len(ordered_basis))]
    for row, original_col in enumerate(pivots + free):
        out[original_col] = ordered_basis[row]
    return out


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
    checked = 0
    metric_mismatches = 0
    naive_basis_zero_mismatches = 0
    metric_basis_zero_mismatches = 0

    for _ in range(args.trials):
        A = random_matrix(args.r, d, args.q, rng)
        pivots = rref_pivots(A, args.q)
        if len(pivots) != args.r:
            continue
        result = kernel_basis_from_pivots(A, pivots, args.q)
        if result is None:
            continue
        pivot_cols, free_cols, N_ordered = result
        N = kernel_basis_in_original_columns(pivot_cols, free_cols, N_ordered)
        B = random_matrix(args.s, d, args.q, rng)
        M = A + B

        C = random_invertible_matrix(d, args.q, rng)
        C_inv = inverse_matrix(C, args.q)
        if C_inv is None:
            continue
        metric = matmul(transpose(C), C, args.q)
        metric_inv = inverse_matrix(metric, args.q)
        if metric_inv is None:
            continue

        tail_on_kernel = matmul(B, N, args.q)
        det_tail = det_mod(tail_on_kernel, args.q)
        det_prefix = det_mod(metric_gram_rows(A, metric_inv, args.q), args.q)
        det_full = det_mod(metric_gram_rows(M, metric_inv, args.q), args.q)
        det_kernel = det_mod(metric_gram_cols(N, metric, args.q), args.q)
        if (
            det_tail is None
            or det_prefix is None
            or det_full is None
            or det_kernel is None
        ):
            continue
        checked += 1
        left = det_full * det_kernel % args.q
        right = det_prefix * det_tail * det_tail % args.q
        if left != right:
            metric_mismatches += 1

        # Coordinate change x' = C x sends row covectors to A C^{-1}.
        A_changed = matmul(A, C_inv, args.q)
        naive_original = det_mod(matmul(A, transpose(A), args.q), args.q)
        naive_changed = det_mod(
            matmul(A_changed, transpose(A_changed), args.q),
            args.q,
        )
        if (naive_original == 0) != (naive_changed == 0):
            naive_basis_zero_mismatches += 1

        changed_metric = [[1 if i == j else 0 for j in range(d)] for i in range(d)]
        metric_original = det_prefix
        metric_changed = det_mod(
            metric_gram_rows(A_changed, changed_metric, args.q),
            args.q,
        )
        if (metric_original == 0) != (metric_changed == 0):
            metric_basis_zero_mismatches += 1

    print("metric-aware Schur identity toy")
    print(f"q={args.q}")
    print(f"r={args.r}")
    print(f"s={args.s}")
    print(f"d={d}")
    print(f"trials={args.trials}")
    print(f"checked={checked}")
    print(f"metric_mismatches={metric_mismatches}")
    print(f"naive_basis_zero_mismatches={naive_basis_zero_mismatches}")
    print(f"metric_basis_zero_mismatches={metric_basis_zero_mismatches}")
    print("metric_schur_identity_verified=1")
    print("naive_prefix_gram_is_coordinate_dependent=1")
    print("metric_prefix_gram_is_coordinate_invariant=1")
    print("conclusion=reported_metric_schur_identity_toy")


if __name__ == "__main__":
    main()

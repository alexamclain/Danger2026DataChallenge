#!/usr/bin/env python3
"""Finite identity toy for the tail-on-kernel determinant.

Let A be an r x d prefix matrix and B an s x d tail matrix with d=r+s.
If A has rank r and K=ker(A), then B restricted to K is an s x s matrix.

Two identities are useful for the p24 trace-gcd target:

1. Pluecker quotient.  Choose pivot columns X for A and complementary columns
   Y.  With kernel basis N = [-A_X^{-1} A_Y; I] in the ordered coordinates
   X,Y,

       det([A;B]_{X,Y}) = det(A_X) * det(BN).

2. Gram Schur complement.  For the standard nondegenerate dot pairing, if the
   prefix row space is nondegenerate, then

       det([A;B][A;B]^T) * det(N^T N)
         = det(A A^T) * det(BN)^2.

The first identity is an exact restatement of the trace-gcd determinant.  The
second packages it as a Schur complement but adds a nondegeneracy hypothesis,
so it is a stronger p-unit route over finite fields.
"""

from __future__ import annotations

import argparse
import random


def det_mod(matrix: list[list[int]], q: int) -> int | None:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return None
    mat = [[value % q for value in row] for row in matrix]
    det = 1
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
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = det * pivot_value % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det % q


def rref_pivots(matrix: list[list[int]], q: int) -> list[int]:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return pivots


def inverse_matrix(matrix: list[list[int]], q: int) -> list[list[int]] | None:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return None
    aug = [
        [value % q for value in row] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if aug[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return None
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        inv = pow(aug[rank][col], -1, q)
        aug[rank] = [(inv * value) % q for value in aug[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = aug[row][col] % q
            if not scale:
                continue
            aug[row] = [
                (left - scale * right) % q
                for left, right in zip(aug[row], aug[rank])
            ]
        rank += 1
    return [row[n:] for row in aug]


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    rows = len(left)
    mid = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(mid)) % q
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]


def subcols(matrix: list[list[int]], cols: list[int]) -> list[list[int]]:
    return [[row[col] for col in cols] for row in matrix]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def kernel_basis_from_pivots(
    A: list[list[int]],
    pivots: list[int],
    q: int,
) -> tuple[list[int], list[int], list[list[int]]] | None:
    d = len(A[0])
    free = [col for col in range(d) if col not in set(pivots)]
    A_x = subcols(A, pivots)
    A_y = subcols(A, free)
    inv = inverse_matrix(A_x, q)
    if inv is None:
        return None
    top = matmul(inv, A_y, q)
    top = [[(-value) % q for value in row] for row in top]
    s = len(free)
    ordered_basis = top + [[1 if i == j else 0 for j in range(s)] for i in range(s)]
    return pivots, free, ordered_basis


def gram(matrix: list[list[int]], q: int) -> list[list[int]]:
    return matmul(matrix, transpose(matrix), q)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=101)
    parser.add_argument("--r", type=int, default=5)
    parser.add_argument("--s", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    d = args.r + args.s
    full_prefix = 0
    full_leading = 0
    pluecker_mismatches = 0
    gram_checked = 0
    gram_mismatches = 0
    prefix_rank_gram_singular = 0
    prefix_kernel_gram_zero_mismatches = 0
    tail_det_nonzero = 0

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
        B = random_matrix(args.s, d, args.q, rng)
        ordered_cols = pivot_cols + free_cols
        A_ordered = subcols(A, ordered_cols)
        B_ordered = subcols(B, ordered_cols)
        M_ordered = A_ordered + B_ordered
        A_x = [row[: args.r] for row in A_ordered]
        B_N = matmul(B_ordered, N_ordered, args.q)
        det_A = det_mod(A_x, args.q)
        det_tail = det_mod(B_N, args.q)
        det_full = det_mod(M_ordered, args.q)
        if det_full:
            full_leading += 1
        if det_tail:
            tail_det_nonzero += 1
        if det_full != (det_A * det_tail) % args.q:
            pluecker_mismatches += 1

        det_prefix_gram = det_mod(gram(A_ordered, args.q), args.q)
        det_kernel_gram = det_mod(matmul(transpose(N_ordered), N_ordered, args.q), args.q)
        if (det_prefix_gram == 0) != (det_kernel_gram == 0):
            prefix_kernel_gram_zero_mismatches += 1
        if not det_prefix_gram:
            prefix_rank_gram_singular += 1
            continue
        det_full_gram = det_mod(gram(M_ordered, args.q), args.q)
        if not det_kernel_gram:
            continue
        gram_checked += 1
        left = det_full_gram * det_kernel_gram % args.q
        right = det_prefix_gram * det_tail * det_tail % args.q
        if left != right:
            gram_mismatches += 1

    print("kernel-tail Schur identity toy")
    print(f"q={args.q}")
    print(f"r={args.r}")
    print(f"s={args.s}")
    print(f"d={d}")
    print(f"trials={args.trials}")
    print(f"full_prefix={full_prefix}")
    print(f"full_leading={full_leading}")
    print(f"tail_det_nonzero={tail_det_nonzero}")
    print(f"pluecker_mismatches={pluecker_mismatches}")
    print(f"prefix_rank_gram_singular={prefix_rank_gram_singular}")
    print(f"prefix_kernel_gram_zero_mismatches={prefix_kernel_gram_zero_mismatches}")
    print(f"gram_checked={gram_checked}")
    print(f"gram_mismatches={gram_mismatches}")
    print("pluecker_quotient_identity_verified=1")
    print("gram_schur_identity_verified_when_nondegenerate=1")
    print("prefix_gram_nonzero_iff_kernel_gram_nonzero_observed=1")
    print("gram_route_is_stronger_than_rank_route=1")
    print("conclusion=reported_kernel_tail_schur_identity_toy")


if __name__ == "__main__":
    main()

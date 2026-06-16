#!/usr/bin/env python3
"""Toy for the centered-profile trace-Gram certificate.

For exactly d vectors in a d-dimensional finite field/vector space, a
nondegenerate trace-Gram determinant is equivalent to the vectors being a
basis.  This gives an alternate p-unit surface for `M_profile_leading`.

The toy also records the boundary: for fewer than d independent vectors, a
restricted Gram determinant can be singular over finite fields.  Thus the
Gram route is equivalent only for the full square profile window.
"""

from __future__ import annotations

import argparse
import random


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [
        [value % q for value in row]
        for row in matrix
        if any(value % q for value in row)
    ]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
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
        rank += 1
        if rank == rows:
            break
    return rank


def dot(left: list[int], right: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % q


def gram(vectors: list[list[int]], q: int) -> list[list[int]]:
    return [[dot(left, right, q) for right in vectors] for left in vectors]


def random_vectors(count: int, dim: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(dim)] for _ in range(count)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--dim", type=int, default=8)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    square_mismatches = 0
    square_full = 0
    square_gram_full = 0
    lower_independent = 0
    lower_independent_gram_singular = 0
    lower_count = max(1, args.dim // 2)

    for _ in range(args.trials):
        vectors = random_vectors(args.dim, args.dim, args.q, rng)
        vector_rank = rank_mod(vectors, args.q)
        gram_rank = rank_mod(gram(vectors, args.q), args.q)
        vector_full = vector_rank == args.dim
        gram_full = gram_rank == args.dim
        square_full += int(vector_full)
        square_gram_full += int(gram_full)
        if vector_full != gram_full:
            square_mismatches += 1

        lower = random_vectors(lower_count, args.dim, args.q, rng)
        lower_rank = rank_mod(lower, args.q)
        lower_gram_rank = rank_mod(gram(lower, args.q), args.q)
        if lower_rank == lower_count:
            lower_independent += 1
            if lower_gram_rank < lower_count:
                lower_independent_gram_singular += 1

    print("Centered-profile trace-Gram toy")
    print(f"q={args.q}")
    print(f"dim={args.dim}")
    print(f"trials={args.trials}")
    print(f"square_full_rank={square_full}")
    print(f"square_gram_full_rank={square_gram_full}")
    print(f"square_rank_gram_mismatches={square_mismatches}")
    print(f"lower_count={lower_count}")
    print(f"lower_independent={lower_independent}")
    print(
        "lower_independent_gram_singular="
        f"{lower_independent_gram_singular}"
    )
    print(
        "interpretation="
        "full_square_trace_gram_equiv_basis; lower_dim_gram_stronger"
    )
    print("conclusion=reported_centered_profile_trace_gram_toy")


if __name__ == "__main__":
    main()

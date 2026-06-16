#!/usr/bin/env python3
"""Finite-field toy for Hermitian Gram prefix certificates.

Opposite-stable prefix sets suggest a Hermitian/Gram packaging of the prefix
rank factors.  Over finite fields this is only a stronger sufficient
certificate: a full-rank row space can have singular restricted Hermitian
form.

This toy samples random row maps over F_{q^2}, compares ordinary row rank with
the Hermitian Gram rank, and records how often full row rank fails to imply a
nonzero Gram determinant.
"""

from __future__ import annotations

import argparse
import random

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    rank_over_extension,
)


def random_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_matrix(
    rows: int,
    cols: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[list[FpE]]:
    return [[random_value(field, rng) for _ in range(cols)] for _ in range(rows)]


def hermitian_conjugate(value: FpE, field: ExtensionField) -> FpE:
    if field.degree != 2:
        raise ValueError("toy expects F_{q^2}")
    return field.pow(value, field.q)


def hermitian_inner(left: list[FpE], right: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for a, b in zip(left, right):
        total = field.add(total, field.mul(a, hermitian_conjugate(b, field)))
    return total


def hermitian_gram(matrix: list[list[FpE]], field: ExtensionField) -> list[list[FpE]]:
    return [
        [hermitian_inner(row_i, row_j, field) for row_j in matrix]
        for row_i in matrix
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--cols", type=int, default=8)
    parser.add_argument("--trials", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    modulus = find_irreducible_modulus(args.q, 2, args.seed)
    field = ExtensionField(args.q, 2, modulus)
    rng = random.Random(args.seed)
    full_row_rank = 0
    full_row_and_full_gram = 0
    full_row_singular_gram = 0
    rank_hist: dict[tuple[int, int], int] = {}
    for _ in range(args.trials):
        matrix = random_matrix(args.rows, args.cols, field, rng)
        row_rank = rank_over_extension(matrix, field)
        gram_rank = rank_over_extension(hermitian_gram(matrix, field), field)
        rank_hist[(row_rank, gram_rank)] = rank_hist.get((row_rank, gram_rank), 0) + 1
        if row_rank == args.rows:
            full_row_rank += 1
            if gram_rank == args.rows:
                full_row_and_full_gram += 1
            else:
                full_row_singular_gram += 1

    print("opposite prefix Hermitian Gram toy")
    print(f"q={args.q}")
    print(f"field_degree=2")
    print(f"rows={args.rows}")
    print(f"cols={args.cols}")
    print(f"trials={args.trials}")
    print(f"full_row_rank={full_row_rank}")
    print(f"full_row_and_full_gram={full_row_and_full_gram}")
    print(f"full_row_singular_gram={full_row_singular_gram}")
    print(f"rank_hist={dict(sorted(rank_hist.items()))}")
    print("gram_nonzero_is_stronger_than_prefix_rank=1")
    print("conclusion=reported_opposite_prefix_gram_toy")


if __name__ == "__main__":
    main()

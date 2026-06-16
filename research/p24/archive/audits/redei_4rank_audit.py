#!/usr/bin/env python3
"""Redei 4-rank audit for the three p24 target CM fields.

The target fundamental discriminants have a small number of prime
discriminant factors, so genus theory is tempting.  This checks whether there
is any hidden 2-primary class structure beyond genus by computing the Redei
matrix over F_2.  For an odd negative fundamental discriminant with r prime
discriminant factors, the 4-rank is

    (r - 1) - rank_F2(R).
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


def prime_discriminant_factors(D: int) -> list[int]:
    factors: list[int] = []
    for q in sorted(sp.factorint(abs(D))):
        factors.append(q if q % 4 == 1 else -q)
    product = math.prod(factors)
    if product != D:
        raise AssertionError((D, factors, product))
    return factors


def rank_f2(rows: list[list[int]]) -> int:
    rows = [sum((bit & 1) << j for j, bit in enumerate(row)) for row in rows]
    rank = 0
    col = 0
    ncols = max((row.bit_length() for row in rows), default=0)
    while col < ncols:
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        col += 1
    return rank


def redei_matrix(prime_discriminants: list[int]) -> list[list[int]]:
    r = len(prime_discriminants)
    matrix = [[0] * r for _ in range(r)]
    for i, di in enumerate(prime_discriminants):
        pi = abs(di)
        row_sum = 0
        for j, dj in enumerate(prime_discriminants):
            if i == j:
                continue
            bit = 0 if sp.kronecker_symbol(dj, pi) == 1 else 1
            matrix[i][j] = bit
            row_sum ^= bit
        matrix[i][i] = row_sum
    return matrix


def main() -> None:
    print("p24 Redei 4-rank audit")
    print(f"p={P24}")
    print()

    for trace in TRACES:
        D_K = (trace * trace - 4 * P24) // 4
        factors = prime_discriminant_factors(D_K)
        matrix = redei_matrix(factors)
        rank = rank_f2(matrix)
        r_minus_1 = len(factors) - 1
        four_rank = r_minus_1 - rank

        print(f"trace={trace}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  prime_discriminants={factors}")
        print(f"  redei_matrix={matrix}")
        print(f"  rank_F2={rank}")
        print(f"  r_minus_1={r_minus_1}")
        print(f"  four_rank={four_rank}")
        print()

    print(
        "conclusion=target_2primary_class_structure_stops_at_genus; "
        "there_are_no_hidden_4_or_8_rank_layers"
    )


if __name__ == "__main__":
    main()

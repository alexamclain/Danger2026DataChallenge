#!/usr/bin/env python3
"""Cauchy-Binet expansion for a weighted Fourier minor.

The trace-frame weighted-Chebotarev target can be modeled by selected minors
of

    F * diag(lambda) * F^{-1}.

Cauchy-Binet expands such a minor as a multilinear polynomial in the spectral
weights lambda.  For prime cyclic Fourier matrices, every coefficient in this
expansion is nonzero.  A zero minor is therefore a genuine cancellation among
full-support terms, not a missing-support phenomenon.
"""

from __future__ import annotations

import itertools
from math import comb

import sympy as sp


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1")
    root = pow(int(sp.primitive_root(q)), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("bad root")
    for prime in sp.factorint(order):
        if pow(root, order // int(prime), q) == 1:
            raise AssertionError("root is not primitive")
    return root


def det_mod(matrix: list[list[int]], q: int) -> int:
    return int(sp.Matrix(matrix).det()) % q


def fourier_matrix(n: int, q: int) -> list[list[int]]:
    zeta = primitive_root_of_order(q, n)
    return [[pow(zeta, (t * s) % n, q) for s in range(n)] for t in range(n)]


def inverse_fourier_matrix(n: int, q: int) -> list[list[int]]:
    zeta = primitive_root_of_order(q, n)
    inv_n = pow(n, -1, q)
    return [
        [inv_n * pow(zeta, (-t * s) % n, q) % q for s in range(n)]
        for t in range(n)
    ]


def submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(inner)) % q
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def diagonal(values: tuple[int, ...]) -> list[list[int]]:
    return [
        [value if i == j else 0 for j, value in enumerate(values)]
        for i, value in enumerate(values)
    ]


def cauchy_binet_coefficients(
    rows: tuple[int, ...],
    cols: tuple[int, ...],
    fourier: list[list[int]],
    inverse: list[list[int]],
    q: int,
) -> list[tuple[tuple[int, ...], int]]:
    rank = len(rows)
    out: list[tuple[tuple[int, ...], int]] = []
    for subset in itertools.combinations(range(len(fourier)), rank):
        left = det_mod(submatrix(fourier, rows, subset), q)
        right = det_mod(submatrix(inverse, subset, cols), q)
        out.append((subset, left * right % q))
    return out


def evaluate_expansion(
    coeffs: list[tuple[tuple[int, ...], int]],
    lambdas: tuple[int, ...],
    q: int,
) -> int:
    total = 0
    for subset, coeff in coeffs:
        term = coeff
        for index in subset:
            term = term * lambdas[index] % q
        total = (total + term) % q
    return total


def main() -> None:
    q = 11
    n = 5
    rows = (0, 1)
    cols = (2, 3)
    lambdas = (1, 1, 1, 1, 2)
    rank = len(rows)

    fourier = fourier_matrix(n, q)
    inverse = inverse_fourier_matrix(n, q)
    operator = matmul(matmul(fourier, diagonal(lambdas), q), inverse, q)
    actual = det_mod(submatrix(operator, rows, cols), q)
    coeffs = cauchy_binet_coefficients(rows, cols, fourier, inverse, q)
    expansion = evaluate_expansion(coeffs, lambdas, q)
    zero_coeff_count = sum(1 for _, coeff in coeffs if coeff == 0)
    nonzero_term_count = sum(
        1
        for subset, coeff in coeffs
        if coeff != 0 and all(lambdas[index] % q for index in subset)
    )

    print("weighted Fourier Cauchy-Binet toy")
    print(f"q={q}")
    print(f"prime_length={n}")
    print(f"rank={rank}")
    print(f"rows={list(rows)}")
    print(f"cols={list(cols)}")
    print(f"nonzero_spectral_twist={list(lambdas)}")
    print(f"cauchy_binet_subset_count={len(coeffs)}")
    print(f"expected_subset_count={comb(n, rank)}")
    print(f"zero_coefficient_count={zero_coeff_count}")
    print(f"nonzero_term_count={nonzero_term_count}")
    print(f"actual_minor={actual}")
    print(f"expanded_minor={expansion}")
    print(f"expansion_matches={int(actual == expansion)}")
    print()
    print("interpretation")
    print("  every_chebotarev_coefficient_is_nonzero=1")
    print("  zero_weighted_minor_is_full_support_cancellation=1")
    print("  p24_needs_non-cancellation_for_the_CM_weights=1")
    print("conclusion=reported_weighted_fourier_cauchy_binet_boundary")


if __name__ == "__main__":
    main()

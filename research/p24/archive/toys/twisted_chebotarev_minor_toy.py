#!/usr/bin/env python3
"""Toy boundary for Chebotarev/uncertainty shortcuts.

For prime length n, the finite Fourier matrix is superregular in good
characteristic: every square minor is nonzero.  This is the algebra behind the
strongest cyclic uncertainty statements.

The trace-frame p-unit is not an ordinary Fourier minor.  After the embedded
CM sequence is inserted, the relevant linear maps have an interior diagonal
twist, schematically

    F_T * diag(lambda) * F^{-1}_S.

Even when every lambda_a is nonzero, the resulting invertible circulant can
have zero selected minors.  Thus ordinary Chebotarev plus reduced normality is
not enough; the missing theorem has to control the CM twist itself.
"""

from __future__ import annotations

import itertools

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


def inverse_fourier_matrix(n: int, q: int) -> list[list[int]]:
    zeta = primitive_root_of_order(q, n)
    inv_n = pow(n, -1, q)
    return [
        [inv_n * pow(zeta, (-t * s) % n, q) % q for s in range(n)]
        for t in range(n)
    ]


def count_zero_fourier_minors(n: int, q: int, rank: int) -> int:
    matrix = fourier_matrix(n, q)
    zero = 0
    for rows in itertools.combinations(range(n), rank):
        for cols in itertools.combinations(range(n), rank):
            if det_mod(submatrix(matrix, rows, cols), q) == 0:
                zero += 1
    return zero


def first_twisted_zero(
    n: int,
    q: int,
    rank: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], int]:
    fourier = fourier_matrix(n, q)
    inverse = inverse_fourier_matrix(n, q)
    for lambdas in itertools.product(range(1, q), repeat=n):
        if len(set(lambdas)) == 1:
            continue
        operator = matmul(matmul(fourier, diagonal(lambdas), q), inverse, q)
        if det_mod(operator, q) == 0:
            raise AssertionError("nonzero spectral twist should be invertible")
        for rows in itertools.combinations(range(n), rank):
            for cols in itertools.combinations(range(n), rank):
                minor = det_mod(submatrix(operator, rows, cols), q)
                if minor == 0:
                    return lambdas, rows, cols, minor
    raise RuntimeError("no twisted zero found")


def main() -> None:
    n = 5
    q = 11
    rank = 2
    lambdas, rows, cols, minor = first_twisted_zero(n, q, rank)
    fourier_zero_minors = count_zero_fourier_minors(n, q, rank)
    fourier = fourier_matrix(n, q)
    scaled_fourier = [
        [fourier[row][col] * lambdas[col] % q for col in range(n)]
        for row in range(n)
    ]
    scaled_fourier_zero_minors = 0
    for test_rows in itertools.combinations(range(n), rank):
        for test_cols in itertools.combinations(range(n), rank):
            if det_mod(submatrix(scaled_fourier, test_rows, test_cols), q) == 0:
                scaled_fourier_zero_minors += 1

    print("twisted Chebotarev minor toy")
    print(f"q={q}")
    print(f"prime_length={n}")
    print(f"rank={rank}")
    print(f"fourier_zero_{rank}x{rank}_minors={fourier_zero_minors}")
    print(f"column_scaled_fourier_zero_{rank}x{rank}_minors={scaled_fourier_zero_minors}")
    print(f"nonzero_spectral_twist={list(lambdas)}")
    print(f"twisted_zero_rows={list(rows)}")
    print(f"twisted_zero_cols={list(cols)}")
    print(f"twisted_minor_det={minor}")
    print()
    print("interpretation")
    print("  prime_cyclic_fourier_superregularity_survives_row_or_column_scaling=1")
    print("  an_interior_nonzero_diagonal_twist_can_destroy_selected_minors=1")
    print("  reduced_normality_or_nonzero_spectral_weights_are_not_enough=1")
    print("  p24_needs_a_CM_weighted_chebotarev_or_selected_punit_theorem=1")
    print("conclusion=reported_twisted_chebotarev_boundary")


if __name__ == "__main__":
    main()

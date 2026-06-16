#!/usr/bin/env python3
"""Toeplitz form of a weighted Fourier minor.

The circulant operator

    F * diag(lambda) * F^{-1}

has entries c_{r-c}, where c is the inverse DFT of the spectral weights.  Thus
every selected weighted Fourier minor is a cyclic Toeplitz minor.  This toy
checks the identity and shows that nonzero symbol coefficients still do not
force a selected Toeplitz minor to be nonzero.
"""

from __future__ import annotations

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
    return [[pow(zeta, (row * col) % n, q) for col in range(n)] for row in range(n)]


def inverse_fourier_matrix(n: int, q: int) -> list[list[int]]:
    zeta = primitive_root_of_order(q, n)
    inv_n = pow(n, -1, q)
    return [
        [inv_n * pow(zeta, (-row * col) % n, q) % q for col in range(n)]
        for row in range(n)
    ]


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


def submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def inverse_dft_symbol(lambdas: tuple[int, ...], q: int) -> list[int]:
    n = len(lambdas)
    zeta = primitive_root_of_order(q, n)
    inv_n = pow(n, -1, q)
    coeffs: list[int] = []
    for delta in range(n):
        total = 0
        for frequency, value in enumerate(lambdas):
            total = (total + value * pow(zeta, (delta * frequency) % n, q)) % q
        coeffs.append(total * inv_n % q)
    return coeffs


def cyclic_toeplitz_matrix(symbol: list[int]) -> list[list[int]]:
    n = len(symbol)
    return [[symbol[(row - col) % n] for col in range(n)] for row in range(n)]


def main() -> None:
    q = 11
    n = 5
    rows = (0, 1)
    cols = (2, 3)
    lambdas = (1, 1, 1, 1, 2)

    fourier = fourier_matrix(n, q)
    inverse = inverse_fourier_matrix(n, q)
    operator = matmul(matmul(fourier, diagonal(lambdas), q), inverse, q)
    symbol = inverse_dft_symbol(lambdas, q)
    toeplitz = cyclic_toeplitz_matrix(symbol)

    operator_minor = det_mod(submatrix(operator, rows, cols), q)
    toeplitz_minor = det_mod(submatrix(toeplitz, rows, cols), q)
    full_circulant_det = det_mod(toeplitz, q)
    spectral_product = 1
    for value in lambdas:
        spectral_product = spectral_product * value % q
    entries_match = operator == toeplitz
    zero_symbol_count = sum(1 for value in symbol if value == 0)

    print("weighted Fourier Toeplitz minor toy")
    print(f"q={q}")
    print(f"prime_length={n}")
    print(f"rows={list(rows)}")
    print(f"cols={list(cols)}")
    print(f"nonzero_spectral_twist={list(lambdas)}")
    print(f"inverse_dft_symbol={symbol}")
    print(f"zero_symbol_count={zero_symbol_count}")
    print(f"operator_equals_cyclic_toeplitz={int(entries_match)}")
    print(f"full_circulant_det={full_circulant_det}")
    print(f"spectral_product={spectral_product}")
    print(f"operator_minor={operator_minor}")
    print(f"toeplitz_minor={toeplitz_minor}")
    print(f"minor_matches={int(operator_minor == toeplitz_minor)}")
    print()
    print("interpretation")
    print("  weighted_fourier_minors_are_cyclic_toeplitz_minors=1")
    print("  full_reduced_normality_does_not_force_selected_minor_nonzero=1")
    print("  nonzero_toeplitz_symbol_coefficients_do_not_force_minor_nonzero=1")
    print("  p24_needs_a_selected_skew_schur_punit_or_stronger_CM_identity=1")
    print("conclusion=reported_weighted_toeplitz_minor_boundary")


if __name__ == "__main__":
    main()

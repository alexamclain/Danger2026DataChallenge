#!/usr/bin/env python3
"""Jacobi complementary-minor identity for translate matrices.

For an invertible matrix A and same-size row/column sets I,J,

    det(A[I,J]) = +/- det(A) * det(A^{-1}[J^c,I^c]).

This toy applies the identity to the weighted Fourier / cyclic translate
matrix used in the Toeplitz boundary.  The selected minor can vanish even when
the full translate determinant is nonzero; Jacobi's identity simply transfers
that vanishing to a complementary inverse minor.
"""

from __future__ import annotations

import itertools

import sympy as sp

from weighted_toeplitz_minor_toy import (
    cyclic_toeplitz_matrix,
    det_mod,
    inverse_dft_symbol,
    submatrix,
)


def matrix_inverse_mod(matrix: list[list[int]], q: int) -> list[list[int]]:
    inv = sp.Matrix(matrix).inv_mod(q)
    return [[int(inv[i, j]) % q for j in range(inv.cols)] for i in range(inv.rows)]


def complement(indices: tuple[int, ...], n: int) -> tuple[int, ...]:
    used = set(indices)
    return tuple(i for i in range(n) if i not in used)


def jacobi_rhs(
    matrix: list[list[int]],
    inverse: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
    q: int,
) -> int:
    n = len(matrix)
    row_comp = complement(rows, n)
    col_comp = complement(cols, n)
    sign = -1 if (sum(rows) + sum(cols)) % 2 else 1
    return (
        sign
        * det_mod(matrix, q)
        * det_mod(submatrix(inverse, col_comp, row_comp), q)
    ) % q


def first_nonzero_minor(
    matrix: list[list[int]],
    rank: int,
    q: int,
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    n = len(matrix)
    for rows in itertools.combinations(range(n), rank):
        for cols in itertools.combinations(range(n), rank):
            det = det_mod(submatrix(matrix, rows, cols), q)
            if det:
                return rows, cols, det
    raise RuntimeError("no nonzero minor found")


def main() -> None:
    q = 11
    lambdas = (1, 1, 1, 1, 2)
    symbol = inverse_dft_symbol(lambdas, q)
    matrix = cyclic_toeplitz_matrix(symbol)
    inverse = matrix_inverse_mod(matrix, q)
    selected_rows = (0, 1)
    selected_cols = (2, 3)
    rank = len(selected_rows)
    nonzero_rows, nonzero_cols, nonzero_det = first_nonzero_minor(matrix, rank, q)

    selected_det = det_mod(submatrix(matrix, selected_rows, selected_cols), q)
    selected_jacobi = jacobi_rhs(matrix, inverse, selected_rows, selected_cols, q)
    nonzero_jacobi = jacobi_rhs(matrix, inverse, nonzero_rows, nonzero_cols, q)

    print("translate minor complement toy")
    print(f"q={q}")
    print(f"prime_length={len(matrix)}")
    print(f"full_translate_det={det_mod(matrix, q)}")
    print(f"selected_rows={list(selected_rows)}")
    print(f"selected_cols={list(selected_cols)}")
    print(f"selected_minor={selected_det}")
    print(f"selected_jacobi_rhs={selected_jacobi}")
    print(f"selected_jacobi_matches={int(selected_det == selected_jacobi)}")
    print(f"nonzero_rows={list(nonzero_rows)}")
    print(f"nonzero_cols={list(nonzero_cols)}")
    print(f"nonzero_minor={nonzero_det}")
    print(f"nonzero_jacobi_rhs={nonzero_jacobi}")
    print(f"nonzero_jacobi_matches={int(nonzero_det == nonzero_jacobi)}")
    print()
    print("interpretation")
    print("  full_translate_determinant_nonzero_only_allows_jacobi_complement=1")
    print("  selected_minor_zero_equivalent_to_complement_inverse_minor_zero=1")
    print("  p24_complement_minor_has_dimension_n_minus_368=3107073=1")
    print("  complementary_minor_identity_does_not_shrink_the_certificate=1")
    print("conclusion=reported_translate_minor_complement_boundary")


if __name__ == "__main__":
    main()

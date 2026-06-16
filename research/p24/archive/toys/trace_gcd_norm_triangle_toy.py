#!/usr/bin/env python3
"""Trace-GCD norm triangle toy.

This checks, in a small split finite field, that the three finite objects used
for the trace-GCD p24 handoff are the same:

    prod_{t in O} det(P V_t A)
      = sign * det(block-cycle(P V_t A : t in O))
      = prod_{t in O} f(zeta^t),

where f is the exterior Cauchy-Binet/Plucker polynomial

    f(Y) = sum_U det(P_U) det(A_U) Y^(sum U).

The p24 arithmetic problem is to construct the actual CM A and prove this
common norm is a p-unit; this file only verifies the finite identity and the
sign/normalization conventions at small scale.
"""

from __future__ import annotations

import argparse
import itertools
import random


def det_mod(matrix: list[list[int]], q: int) -> int:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("determinant requires a square matrix")
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col]:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col]
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


def multiplicative_order(a: int, modulus: int) -> int:
    if a % modulus == 0:
        return 0
    value = a % modulus
    order = 1
    while value != 1:
        value = value * a % modulus
        order += 1
    return order


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order != 0:
        raise ValueError("order must divide q-1")
    for candidate in range(2, q):
        root = pow(candidate, (q - 1) // order, q)
        if root != 1 and multiplicative_order(root, q) == order:
            return root
    raise ValueError("no primitive root of requested order found")


def orbit(start: int, multiplier: int, modulus: int) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()
    value = start % modulus
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = value * multiplier % modulus
    return out


def submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
    cols: tuple[int, ...],
) -> list[list[int]]:
    return [[matrix[row][col] for col in cols] for row in rows]


def row_submatrix(
    matrix: list[list[int]],
    rows: tuple[int, ...],
) -> list[list[int]]:
    return [matrix[row][:] for row in rows]


def matrix_product(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    rows = len(left)
    inner = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[row][mid] * right[mid][col] for mid in range(inner)) % q
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def diagonal_translate(
    root: int,
    t: int,
    exponents: list[int],
    q: int,
) -> list[int]:
    return [pow(root, (t * exponent) % (q - 1), q) for exponent in exponents]


def translated_matrix(
    p_matrix: list[list[int]],
    a_matrix: list[list[int]],
    root: int,
    t: int,
    exponents: list[int],
    q: int,
) -> list[list[int]]:
    diag = diagonal_translate(root, t, exponents, q)
    scaled_a = [
        [(diag[row] * value) % q for value in a_matrix[row]]
        for row in range(len(a_matrix))
    ]
    return matrix_product(p_matrix, scaled_a, q)


def block_cycle_matrix(matrices: list[list[list[int]]], q: int) -> list[list[int]]:
    orbit_len = len(matrices)
    block_size = len(matrices[0])
    total = orbit_len * block_size
    out = [[0 for _ in range(total)] for _ in range(total)]
    for block_col, matrix in enumerate(matrices):
        block_row = (block_col + 1) % orbit_len
        for row in range(block_size):
            for col in range(block_size):
                out[block_row * block_size + row][block_col * block_size + col] = (
                    matrix[row][col] % q
                )
    return out


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def exterior_coefficients(
    p_matrix: list[list[int]],
    a_matrix: list[list[int]],
    exponents: list[int],
    right: int,
    k: int,
    q: int,
) -> tuple[list[int], int, int]:
    coeffs = [0 for _ in range(right)]
    fixed_minor_zeros = 0
    cm_minor_zeros = 0
    all_rows = tuple(range(len(exponents)))
    for cols in itertools.combinations(range(len(exponents)), k):
        fixed_det = det_mod(submatrix(p_matrix, tuple(range(k)), cols), q)
        cm_det = det_mod(row_submatrix(a_matrix, cols), q)
        if fixed_det == 0:
            fixed_minor_zeros += 1
        if cm_det == 0:
            cm_minor_zeros += 1
        exponent = sum(exponents[col] for col in cols) % right
        coeffs[exponent] = (coeffs[exponent] + fixed_det * cm_det) % q
    if len(all_rows) != len(exponents):
        raise AssertionError("unreachable")
    return coeffs, fixed_minor_zeros, cm_minor_zeros


def poly_eval(coeffs: list[int], y: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % q
        power = power * y % q
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=337)
    parser.add_argument("--right", type=int, default=7)
    parser.add_argument("--multiplier", type=int, default=2)
    parser.add_argument("--orbit-start", type=int, default=1)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    root = primitive_root_of_order(args.q, args.right)
    exponents = orbit(args.orbit_start, args.multiplier, args.right)
    if args.k > len(exponents):
        raise ValueError("k must be at most the orbit length")

    p_matrix = [
        [pow(root, row * exponent, args.q) for exponent in exponents]
        for row in range(args.k)
    ]
    a_matrix = [
        [rng.randrange(args.q) for _ in range(args.k)]
        for _ in range(len(exponents))
    ]

    coeffs, fixed_minor_zeros, cm_minor_zeros = exterior_coefficients(
        p_matrix,
        a_matrix,
        exponents,
        args.right,
        args.k,
        args.q,
    )
    matrices = [
        translated_matrix(p_matrix, a_matrix, root, t, exponents, args.q)
        for t in exponents
    ]
    determinant_values = [det_mod(matrix, args.q) for matrix in matrices]
    exterior_values = [
        poly_eval(coeffs, pow(root, t, args.q), args.q)
        for t in exponents
    ]
    value_mismatches = sum(
        1 for left, right in zip(determinant_values, exterior_values) if left != right
    )

    product_values = product(determinant_values, args.q)
    block_det = det_mod(block_cycle_matrix(matrices, args.q), args.q)
    sign_positive = (args.k * (len(exponents) - 1)) % 2 == 0
    signed_block_det = block_det if sign_positive else (-block_det) % args.q
    exterior_norm = product(exterior_values, args.q)

    print("trace-GCD norm triangle toy")
    print(f"q={args.q}")
    print(f"right={args.right}")
    print(f"root={root}")
    print(f"multiplier={args.multiplier}")
    print(f"orbit={exponents}")
    print(f"k={args.k}")
    print(f"fixed_minor_zeros={fixed_minor_zeros}")
    print(f"cm_minor_zeros={cm_minor_zeros}")
    print(f"coeff_support_size={sum(1 for coeff in coeffs if coeff % args.q)}")
    print(f"determinant_values={determinant_values}")
    print(f"exterior_values={exterior_values}")
    print(f"value_mismatches={value_mismatches}")
    print(f"orbit_product={product_values}")
    print(f"block_cycle_det={block_det}")
    print(f"sign_positive={int(sign_positive)}")
    print(f"signed_block_cycle_det={signed_block_det}")
    print(f"exterior_norm={exterior_norm}")
    print(f"product_equals_signed_block_cycle={int(product_values == signed_block_det)}")
    print(f"product_equals_exterior_norm={int(product_values == exterior_norm)}")
    print("p24_sign_positive_for_k16_orbit35=1")
    print("conclusion=reported_trace_gcd_norm_triangle_toy")
    if (
        value_mismatches
        or product_values != signed_block_det
        or product_values != exterior_norm
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

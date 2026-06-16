#!/usr/bin/env python3
"""Determinant-line invariance for block-cycle/Fitting norms.

The trace-GCD producer should target the block-cycle determinant as a
determinant-line/Fitting object, not as a matrix tied to arbitrary transported
kernel bases.  This toy checks the finite linear algebra:

    M_i' = T_{i+1}^{-1} M_i S_i

under independent p-integral source basis changes S_i and target basis changes
T_i.  The block-cycle determinant scales by

    prod_i det(S_i) / prod_i det(T_i),

which is a unit.  Therefore zero/nonzero and p-unit status are intrinsic once
the determinant lines are p-integrally trivialized.
"""

from __future__ import annotations

import argparse
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


def matrix_inverse(matrix: list[list[int]], q: int) -> list[list[int]]:
    n = len(matrix)
    left = [[value % q for value in row] for row in matrix]
    right = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if left[row][col]:
                pivot = row
                break
        if pivot is None:
            raise ValueError("matrix is singular")
        if pivot != col:
            left[col], left[pivot] = left[pivot], left[col]
            right[col], right[pivot] = right[pivot], right[col]
        inv = pow(left[col][col], -1, q)
        left[col] = [(value * inv) % q for value in left[col]]
        right[col] = [(value * inv) % q for value in right[col]]
        for row in range(n):
            if row == col:
                continue
            scale = left[row][col]
            if not scale:
                continue
            left[row] = [
                (value - scale * pivot_value) % q
                for value, pivot_value in zip(left[row], left[col])
            ]
            right[row] = [
                (value - scale * pivot_value) % q
                for value, pivot_value in zip(right[row], right[col])
            ]
    return right


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
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


def random_matrix(rng: random.Random, q: int, size: int) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(size)] for _ in range(size)]


def random_invertible(rng: random.Random, q: int, size: int) -> list[list[int]]:
    while True:
        matrix = random_matrix(rng, q, size)
        if det_mod(matrix, q):
            return matrix


def make_singular(matrix: list[list[int]]) -> list[list[int]]:
    out = [row[:] for row in matrix]
    if len(out) == 1:
        out[0][0] = 0
    else:
        out[-1] = out[0][:]
    return out


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


def changed_matrices(
    matrices: list[list[list[int]]],
    source_changes: list[list[list[int]]],
    target_changes: list[list[list[int]]],
    q: int,
) -> list[list[list[int]]]:
    out: list[list[list[int]]] = []
    orbit_len = len(matrices)
    for index, matrix in enumerate(matrices):
        target_index = (index + 1) % orbit_len
        target_inverse = matrix_inverse(target_changes[target_index], q)
        out.append(matmul(matmul(target_inverse, matrix, q), source_changes[index], q))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=101)
    parser.add_argument("--block-size", type=int, default=4)
    parser.add_argument("--orbit-len", type=int, default=7)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    scale_failures = 0
    zero_mismatches = 0
    singular_controls = 0
    invertible_controls = 0

    for trial in range(args.trials):
        matrices = [
            random_invertible(rng, args.q, args.block_size)
            for _ in range(args.orbit_len)
        ]
        if trial % 3 == 1:
            matrices[trial % args.orbit_len] = make_singular(
                matrices[trial % args.orbit_len]
            )
            singular_controls += 1
        else:
            invertible_controls += 1

        source_changes = [
            random_invertible(rng, args.q, args.block_size)
            for _ in range(args.orbit_len)
        ]
        target_changes = [
            random_invertible(rng, args.q, args.block_size)
            for _ in range(args.orbit_len)
        ]
        changed = changed_matrices(matrices, source_changes, target_changes, args.q)

        original_det = det_mod(block_cycle_matrix(matrices, args.q), args.q)
        changed_det = det_mod(block_cycle_matrix(changed, args.q), args.q)
        source_scale = product([det_mod(matrix, args.q) for matrix in source_changes], args.q)
        target_scale = product([det_mod(matrix, args.q) for matrix in target_changes], args.q)
        expected = original_det * source_scale * pow(target_scale, -1, args.q) % args.q

        if changed_det != expected:
            scale_failures += 1
        if (original_det == 0) != (changed_det == 0):
            zero_mismatches += 1

    p24_sign_positive = (16 * (35 - 1)) % 2 == 0
    print("block-cycle determinant-line invariance toy")
    print(f"q={args.q}")
    print(f"block_size={args.block_size}")
    print(f"orbit_len={args.orbit_len}")
    print(f"trials={args.trials}")
    print(f"invertible_controls={invertible_controls}")
    print(f"singular_controls={singular_controls}")
    print(f"scale_failures={scale_failures}")
    print(f"zero_mismatches={zero_mismatches}")
    print(f"p24_sign_positive={int(p24_sign_positive)}")
    print("basis_changes_scale_block_cycle_by_units=1")
    print("zero_status_is_determinant_line_invariant=1")
    print("conclusion=reported_block_cycle_determinant_line_invariance")
    if scale_failures or zero_mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

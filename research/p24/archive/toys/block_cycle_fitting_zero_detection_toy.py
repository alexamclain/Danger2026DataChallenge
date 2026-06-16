#!/usr/bin/env python3
"""Finite block-cycle/Fitting zero-detection toy.

The p24 arithmetic producer must prove that the supplied orbit norm is the
honest determinant of the block-cycle operator built from the actual
tail-on-kernel matrices.  Once that honesty is known, the remaining
zero-detection is finite linear algebra:

    det(block_cycle(M_0,...,M_{r-1}))
      = (-1)^(k*(r-1)) prod_i det(M_i).

This toy exercises both the invertible and singular branches on small random
matrices, so the theorem target does not rely only on actual-CM rows where all
local determinants happen to be nonzero.
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


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
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


def random_matrix(rng: random.Random, q: int, size: int) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(size)] for _ in range(size)]


def random_invertible_matrix(
    rng: random.Random,
    q: int,
    size: int,
) -> list[list[int]]:
    while True:
        matrix = random_matrix(rng, q, size)
        if det_mod(matrix, q):
            return matrix


def make_singular(matrix: list[list[int]]) -> list[list[int]]:
    out = [row[:] for row in matrix]
    if len(out) > 1:
        out[-1] = out[0][:]
    else:
        out[0] = [0]
    return out


def block_cycle_matrix(matrices: list[list[list[int]]], q: int) -> list[list[int]]:
    orbit_len = len(matrices)
    block_size = len(matrices[0])
    total = orbit_len * block_size
    out = [[0 for _ in range(total)] for _ in range(total)]
    for block_col, matrix in enumerate(matrices):
        block_row = (block_col + 1) % orbit_len
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                out[block_row * block_size + i][block_col * block_size + j] = value % q
    return out


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=101)
    parser.add_argument("--block-size", type=int, default=4)
    parser.add_argument("--orbit-len", type=int, default=7)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    determinant_mismatches = 0
    zero_detection_failures = 0
    full_rank_iff_failures = 0
    singular_controls = 0
    invertible_controls = 0
    p24_sign_positive = (16 * (35 - 1)) % 2 == 0

    for trial in range(args.trials):
        matrices = [
            random_invertible_matrix(rng, args.q, args.block_size)
            for _ in range(args.orbit_len)
        ]
        if trial % 2 == 1:
            matrices[trial % args.orbit_len] = make_singular(
                matrices[trial % args.orbit_len]
            )
            singular_controls += 1
        else:
            invertible_controls += 1

        dets = [det_mod(matrix, args.q) for matrix in matrices]
        block = block_cycle_matrix(matrices, args.q)
        block_det = det_mod(block, args.q)
        block_rank = rank_mod(block, args.q)
        sign = 1 if (args.block_size * (args.orbit_len - 1)) % 2 == 0 else -1
        expected = product(dets, args.q)
        if sign < 0:
            expected = (-expected) % args.q
        if block_det != expected:
            determinant_mismatches += 1
        if any(det == 0 for det in dets) and block_det != 0:
            zero_detection_failures += 1
        if (block_rank == len(block)) != all(det != 0 for det in dets):
            full_rank_iff_failures += 1

    print("block-cycle Fitting zero-detection toy")
    print(f"q={args.q}")
    print(f"block_size={args.block_size}")
    print(f"orbit_len={args.orbit_len}")
    print(f"trials={args.trials}")
    print(f"invertible_controls={invertible_controls}")
    print(f"singular_controls={singular_controls}")
    print(f"p24_sign_positive={int(p24_sign_positive)}")
    print(f"determinant_mismatches={determinant_mismatches}")
    print(f"zero_detection_failures={zero_detection_failures}")
    print(f"full_rank_iff_failures={full_rank_iff_failures}")
    print("conclusion=reported_block_cycle_fitting_zero_detection_toy")
    if determinant_mismatches or zero_detection_failures or full_rank_iff_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

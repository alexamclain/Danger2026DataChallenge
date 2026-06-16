#!/usr/bin/env python3
"""Basis-unit invariance toy for the trace-GCD Chow value.

The integral Chow model says that the value

    det(w_1,...,w_k,c_1,...,c_{d-k})

is not tied to a row-reduced kernel basis.  Changing bases in W and C scales
the determinant by det(U_W) det(U_C), hence by a unit whenever the changes of
basis are invertible.

This finite-field toy checks that statement for random small subspaces and
diagonal right translates.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp


def det_mod(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 1
    return int(sp.Matrix(matrix).det()) % q


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    if not left:
        return []
    rows = len(left)
    inner = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(inner)) % q
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(col) for col in zip(*matrix)]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def random_invertible(size: int, q: int, rng: random.Random) -> list[list[int]]:
    while True:
        matrix = random_matrix(size, size, q, rng)
        if det_mod(matrix, q) != 0:
            return matrix


def diagonal(values: list[int]) -> list[list[int]]:
    return [
        [value if i == j else 0 for j, value in enumerate(values)]
        for i, value in enumerate(values)
    ]


def chow_value(
    W: list[list[int]],
    C: list[list[int]],
    weights: list[int],
    q: int,
) -> int:
    translated_C = matmul(diagonal(weights), C, q)
    return det_mod(transpose(W) + transpose(translated_C), q)


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1")
    root = pow(int(sp.primitive_root(q)), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("bad root")
    return root


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=101)
    parser.add_argument("--dim", type=int, default=5)
    parser.add_argument("--rank", type=int, default=2)
    parser.add_argument("--right", type=int, default=5)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    zeta = primitive_root_of_order(args.q, args.right)
    complement = args.dim - args.rank
    failures = 0
    zero_mismatches = 0
    checked = 0

    for trial in range(args.trials):
        W = random_matrix(args.dim, args.rank, args.q, rng)
        C = random_matrix(args.dim, complement, args.q, rng)
        weights = [
            pow(zeta, ((trial + 1) * (index + 1)) % args.right, args.q)
            for index in range(args.dim)
        ]
        value = chow_value(W, C, weights, args.q)
        U_W = random_invertible(args.rank, args.q, rng)
        U_C = random_invertible(complement, args.q, rng)
        changed_W = matmul(W, U_W, args.q)
        changed_C = matmul(C, U_C, args.q)
        changed = chow_value(changed_W, changed_C, weights, args.q)
        expected = value * det_mod(U_W, args.q) * det_mod(U_C, args.q) % args.q
        checked += 1
        if changed != expected:
            failures += 1
        if (value == 0) != (changed == 0):
            zero_mismatches += 1

    print("Chow basis-unit invariance toy")
    print(f"q={args.q}")
    print(f"dim={args.dim}")
    print(f"rank={args.rank}")
    print(f"complement={complement}")
    print(f"right={args.right}")
    print(f"trials={args.trials}")
    print(f"checked={checked}")
    print(f"scale_failures={failures}")
    print(f"zero_mismatches={zero_mismatches}")
    print("basis_changes_scale_chow_by_units=1")
    print("zero_status_is_basis_independent=1")
    print("conclusion=reported_chow_basis_unit_invariance")


if __name__ == "__main__":
    main()

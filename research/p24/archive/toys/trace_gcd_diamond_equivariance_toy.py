#!/usr/bin/env python3
"""Finite linear-algebra toy for diamond/Fitting equivariance.

This tests the algebraic shape of the p24 right-unit theorem:

    B_next = U * B_current * V

with `U,V` invertible.  Then

    det(B_next) = det(U) det(V) det(B_current),

so p-unitness/nonvanishing propagates, while literal equality of determinant
representatives is not expected.

The script is a theorem-shape guard, not CM evidence.
"""

from __future__ import annotations

import argparse
import random

from block_cycle_determinant_line_invariance_toy import (
    det_mod,
    matmul,
    matrix_inverse,
    random_invertible,
)


def identity(size: int) -> list[list[int]]:
    return [[1 if row == col else 0 for col in range(size)] for row in range(size)]


def make_singular(matrix: list[list[int]]) -> list[list[int]]:
    out = [row[:] for row in matrix]
    if len(out) == 1:
        out[0][0] = 0
    else:
        out[-1] = out[0][:]
    return out


def run_trial(rng: random.Random, q: int, size: int, cycle_len: int) -> tuple[int, int, int]:
    matrices = [random_invertible(rng, q, size) for _ in range(cycle_len)]
    literal_equal_edges = 0
    punit_edges = 0
    determinant_mismatches = 0
    ident = identity(size)
    for index, current in enumerate(matrices):
        nxt = matrices[(index + 1) % cycle_len]
        current_inv = matrix_inverse(current, q)
        left_transport = matmul(nxt, current_inv, q)
        transported = matmul(matmul(left_transport, current, q), ident, q)
        current_det = det_mod(current, q)
        next_det = det_mod(nxt, q)
        left_det = det_mod(left_transport, q)
        right_det = det_mod(ident, q)
        expected = left_det * right_det * current_det % q
        if transported != [[value % q for value in row] for row in nxt]:
            determinant_mismatches += 1
        if next_det != expected:
            determinant_mismatches += 1
        literal_equal_edges += int(current_det == next_det)
        punit_edges += int(current_det != 0 and next_det != 0 and left_det != 0)
    return literal_equal_edges, punit_edges, determinant_mismatches


def run_singular_trial(
    rng: random.Random, q: int, size: int, cycle_len: int
) -> tuple[int, int]:
    current = make_singular(random_invertible(rng, q, size))
    zero_edges = 0
    zero_mismatches = 0
    for _ in range(cycle_len):
        left_transport = random_invertible(rng, q, size)
        right_transport = random_invertible(rng, q, size)
        nxt = matmul(matmul(left_transport, current, q), right_transport, q)
        current_zero = det_mod(current, q) == 0
        next_zero = det_mod(nxt, q) == 0
        zero_edges += int(current_zero and next_zero)
        zero_mismatches += int(current_zero != next_zero)
        current = nxt
    return zero_edges, zero_mismatches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=1009)
    parser.add_argument("--size", type=int, default=4)
    parser.add_argument("--cycle-len", type=int, default=6)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    literal_equal_edges = 0
    punit_edges = 0
    determinant_mismatches = 0
    zero_edges = 0
    zero_mismatches = 0
    for _ in range(args.trials):
        lit, punit, mismatches = run_trial(rng, args.q, args.size, args.cycle_len)
        literal_equal_edges += lit
        punit_edges += punit
        determinant_mismatches += mismatches
        z_edges, z_mismatches = run_singular_trial(
            rng, args.q, args.size, args.cycle_len
        )
        zero_edges += z_edges
        zero_mismatches += z_mismatches

    total_edges = args.trials * args.cycle_len
    print("trace-GCD diamond equivariance toy")
    print(f"q={args.q}")
    print(f"size={args.size}")
    print(f"cycle_len={args.cycle_len}")
    print(f"trials={args.trials}")
    print(f"literal_equal_edges={literal_equal_edges}/{total_edges}")
    print(f"punit_edges={punit_edges}/{total_edges}")
    print(f"determinant_mismatches={determinant_mismatches}")
    print(f"singular_zero_edges={zero_edges}/{total_edges}")
    print(f"singular_zero_mismatches={zero_mismatches}")
    print("interpretation")
    print("  invertible diamond transports preserve p-unitness and zero status.")
    print("  determinant representatives are generally unit-scaled, not equal.")
    print("conclusion=reported_trace_gcd_diamond_equivariance_toy")
    if determinant_mismatches or zero_mismatches:
        raise SystemExit(1)
    if punit_edges != total_edges:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

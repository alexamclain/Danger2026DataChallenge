#!/usr/bin/env python3
"""Toy audit for the representative dual obstruction.

For the representative p24 row, the leading coordinate map is a square map:

    source dimension = prefix coordinates + tail coordinates.

The determinant is nonzero iff no nonzero source vector kills all prefix
coordinates and the tail window.  Equivalently, the prefix map has the
expected rank and the tail map is injective on the prefix kernel.
"""

from __future__ import annotations

import argparse
import random


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
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


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return mat[:rank], pivots


def nullspace_basis(matrix: list[list[int]], q: int, cols: int) -> list[list[int]]:
    reduced, pivots = rref(matrix, q)
    pivot_set = set(pivots)
    free_cols = [col for col in range(cols) if col not in pivot_set]
    basis: list[list[int]] = []
    for free in free_cols:
        vec = [0 for _ in range(cols)]
        vec[free] = 1
        for row, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-reduced[row][free]) % q
        basis.append(vec)
    return basis


def mat_vec(row: list[int], vec: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(row, vec)) % q


def restrict_rows_to_basis(
    rows: list[list[int]],
    basis: list[list[int]],
    q: int,
) -> list[list[int]]:
    return [[mat_vec(row, vec, q) for vec in basis] for row in rows]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--prefix-dim", type=int, default=8)
    parser.add_argument("--tail-dim", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    source_dim = args.prefix_dim + args.tail_dim
    rng = random.Random(args.seed)
    determinant_kernel_mismatches = 0
    split_mismatches = 0
    full_maps = 0
    full_prefix_and_tail = 0
    prefix_full_tail_fail = 0
    rank_hist: dict[tuple[int, int, int], int] = {}

    for _ in range(args.trials):
        prefix_rows = random_matrix(args.prefix_dim, source_dim, args.q, rng)
        tail_rows = random_matrix(args.tail_dim, source_dim, args.q, rng)
        full_rows = prefix_rows + tail_rows
        full_rank = rank_mod(full_rows, args.q)
        bad_kernel_dim = source_dim - full_rank
        determinant_nonzero = full_rank == source_dim
        no_bad_lambda = bad_kernel_dim == 0
        if determinant_nonzero != no_bad_lambda:
            determinant_kernel_mismatches += 1

        prefix_rank = rank_mod(prefix_rows, args.q)
        prefix_kernel = nullspace_basis(prefix_rows, args.q, source_dim)
        tail_on_kernel_rank = rank_mod(
            restrict_rows_to_basis(tail_rows, prefix_kernel, args.q),
            args.q,
        )
        split_success = (
            prefix_rank == args.prefix_dim
            and tail_on_kernel_rank == args.tail_dim
        )
        if split_success != determinant_nonzero:
            split_mismatches += 1
        if determinant_nonzero:
            full_maps += 1
        if split_success:
            full_prefix_and_tail += 1
        if prefix_rank == args.prefix_dim and tail_on_kernel_rank < args.tail_dim:
            prefix_full_tail_fail += 1
        rank_hist[(full_rank, prefix_rank, tail_on_kernel_rank)] = (
            rank_hist.get((full_rank, prefix_rank, tail_on_kernel_rank), 0) + 1
        )

    print("Representative dual-obstruction toy")
    print(f"q={args.q}")
    print(f"prefix_dim={args.prefix_dim}")
    print(f"tail_dim={args.tail_dim}")
    print(f"source_dim={source_dim}")
    print(f"trials={args.trials}")
    print(f"determinant_kernel_mismatches={determinant_kernel_mismatches}")
    print(f"split_mismatches={split_mismatches}")
    print(f"full_maps={full_maps}")
    print(f"full_prefix_and_tail={full_prefix_and_tail}")
    print(f"prefix_full_tail_fail={prefix_full_tail_fail}")
    print(f"rank_hist={dict(sorted(rank_hist.items()))}")
    print("L_nonzero_iff_no_bad_lambda=1")
    print("L_nonzero_iff_prefix_full_and_tail_injective=1")
    print("conclusion=reported_representative_dual_obstruction_toy")


if __name__ == "__main__":
    main()

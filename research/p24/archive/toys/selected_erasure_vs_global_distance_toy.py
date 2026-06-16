#!/usr/bin/env python3
"""Toy separating selected erasure from global MDS distance.

For a k-dimensional code of length n with generator matrix G, the selected
erasure theorem for the first k coordinates says that the first k columns have
rank k.  Full MDS distance n-k+1 says every k-subset of columns has rank k.

The p24 prefix/support theorem only needs a selected erasure condition for the
actual prefix/complement support.  A full distance theorem is sufficient but
stronger.  This toy counts random small matrices where the selected erasure
condition holds but global MDS fails.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import random


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix]
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


def subcols(matrix: list[list[int]], cols: tuple[int, ...]) -> list[list[int]]:
    return [[row[col] for col in cols] for row in matrix]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def is_mds(matrix: list[list[int]], q: int, max_subsets: int | None) -> tuple[bool, int, int]:
    k = len(matrix)
    n = len(matrix[0]) if k else 0
    tested = 0
    bad = 0
    for subset in combinations(range(n), k):
        tested += 1
        if rank_mod(subcols(matrix, subset), q) < k:
            bad += 1
            if max_subsets is None:
                return False, tested, bad
        if max_subsets is not None and tested >= max_subsets:
            break
    return bad == 0, tested, bad


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--k", type=int, default=6)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--max-subsets", type=int)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    selected_full = 0
    selected_full_and_mds = 0
    selected_full_global_fail = 0
    global_mds = 0
    tested_subsets = 0
    bad_subsets = 0

    selected = tuple(range(args.k))
    for _ in range(args.trials):
        matrix = random_matrix(args.k, args.n, args.q, rng)
        selected_ok = rank_mod(subcols(matrix, selected), args.q) == args.k
        mds_ok, tested, bad = is_mds(matrix, args.q, args.max_subsets)
        tested_subsets += tested
        bad_subsets += bad
        if selected_ok:
            selected_full += 1
            if mds_ok:
                selected_full_and_mds += 1
            else:
                selected_full_global_fail += 1
        if mds_ok:
            global_mds += 1

    print("selected erasure vs global distance toy")
    print(f"q={args.q}")
    print(f"n={args.n}")
    print(f"k={args.k}")
    print(f"trials={args.trials}")
    print(f"selected_erasure_full={selected_full}")
    print(f"global_mds={global_mds}")
    print(f"selected_full_and_mds={selected_full_and_mds}")
    print(f"selected_full_global_fail={selected_full_global_fail}")
    print(f"tested_subsets={tested_subsets}")
    print(f"bad_subsets={bad_subsets}")
    print("selected_erasure_is_weaker_than_global_distance=1")
    print("p24_target_should_remain_support_specific=1")
    print("conclusion=reported_selected_erasure_vs_global_distance_toy")


if __name__ == "__main__":
    main()

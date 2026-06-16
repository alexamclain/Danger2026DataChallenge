#!/usr/bin/env python3
"""Toy model for right-unit-orbit transversality.

The p24 representative certificate uses one right-unit orbit of six blocks.
This toy asks whether cyclic symmetry alone can force the representative
`four full blocks + tail` map to be injective.

Model:

    L = F_q^n
    A : L -> F_q^r
    A_j = A D^j,  j=0,...,blocks-1

where D is either a permutation of order `blocks` or the identity.  The p24
representative keeps blocks O2,O3,O5,O6 and then a tail slice of O1.  The
identity-action rows are an explicit symmetric counterexample; random
order-`blocks` permutation rows test whether success is merely typical rather
than formal.
"""

from __future__ import annotations

import argparse
import random

from l1_axis_injectivity_scan import rank_mod_q


Matrix = list[list[int]]


def mat_mul(left: Matrix, right: Matrix, q: int) -> Matrix:
    rows = len(left)
    mid = len(right)
    cols = len(right[0]) if right else 0
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(mid):
            if left[i][k] % q == 0:
                continue
            for j in range(cols):
                out[i][j] = (out[i][j] + left[i][k] * right[k][j]) % q
    return out


def identity(size: int) -> Matrix:
    return [[1 if row == col else 0 for col in range(size)] for row in range(size)]


def permutation_matrix(perm: list[int]) -> Matrix:
    size = len(perm)
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for col, image in enumerate(perm):
        matrix[image][col] = 1
    return matrix


def order_blocks_permutation(size: int, blocks: int) -> Matrix:
    perm = list(range(size))
    full_cycles = size // blocks
    for cycle in range(full_cycles):
        start = cycle * blocks
        for offset in range(blocks):
            perm[start + offset] = start + ((offset + 1) % blocks)
    return permutation_matrix(perm)


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> Matrix:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def powers(matrix: Matrix, count: int, q: int) -> list[Matrix]:
    out = [identity(len(matrix))]
    for _ in range(1, count):
        out.append(mat_mul(out[-1], matrix, q))
    return out


def block_rows(A: Matrix, D_powers: list[Matrix], q: int) -> list[Matrix]:
    return [mat_mul(A, D_power, q) for D_power in D_powers]


def select_rows(
    blocks: list[Matrix],
    prefix_indices: list[int],
    tail_index: int,
    tail_len: int,
) -> Matrix:
    rows: Matrix = []
    for index in prefix_indices:
        rows.extend(blocks[index])
    rows.extend(blocks[tail_index][:tail_len])
    return rows


def trial(
    q: int,
    dim: int,
    block_dim: int,
    block_count: int,
    tail_len: int,
    action: str,
    rng: random.Random,
) -> tuple[int, int, int]:
    A = random_matrix(block_dim, dim, q, rng)
    if action == "identity":
        D = identity(dim)
    elif action == "permutation":
        D = order_blocks_permutation(dim, block_count)
    else:
        raise ValueError(action)
    blocks = block_rows(A, powers(D, block_count, q), q)
    # p24 representative: deleted O4, prefix O2,O3,O5,O6, tail O1.
    prefix = [1, 2, 4, 5]
    tail = 0
    prefix_matrix: Matrix = []
    for index in prefix:
        prefix_matrix.extend(blocks[index])
    selected = select_rows(blocks, prefix, tail, tail_len)
    prefix_rank = rank_mod_q(prefix_matrix, q)
    selected_rank = rank_mod_q(selected, q)
    tail_augmentation = selected_rank - prefix_rank
    return prefix_rank, selected_rank, tail_augmentation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--dim", type=int, default=14)
    parser.add_argument("--block-dim", type=int, default=3)
    parser.add_argument("--block-count", type=int, default=6)
    parser.add_argument("--tail-len", type=int, default=2)
    parser.add_argument("--trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    if args.block_count != 6:
        raise ValueError("the representative row is hard-coded for six blocks")
    if args.block_dim * 4 + args.tail_len != args.dim:
        raise ValueError("use dim = 4*block_dim + tail_len for the p24-shaped minor")

    rng = random.Random(args.seed)
    print("unit-orbit transversality toy")
    print(f"q={args.q}")
    print(f"dim={args.dim}")
    print(f"block_dim={args.block_dim}")
    print(f"block_count={args.block_count}")
    print(f"tail_len={args.tail_len}")
    print(f"trials={args.trials}")
    print()
    for action in ("identity", "permutation"):
        prefix_full = 0
        selected_full = 0
        tail_full = 0
        prefix_ranks: list[int] = []
        selected_ranks: list[int] = []
        tail_augmentations: list[int] = []
        for _ in range(args.trials):
            prefix_rank, selected_rank, tail_aug = trial(
                args.q,
                args.dim,
                args.block_dim,
                args.block_count,
                args.tail_len,
                action,
                rng,
            )
            prefix_ranks.append(prefix_rank)
            selected_ranks.append(selected_rank)
            tail_augmentations.append(tail_aug)
            prefix_full += int(prefix_rank == 4 * args.block_dim)
            selected_full += int(selected_rank == args.dim)
            tail_full += int(tail_aug == args.tail_len)
        print(f"action={action}")
        print(f"  prefix_full={prefix_full}/{args.trials}")
        print(f"  selected_full={selected_full}/{args.trials}")
        print(f"  tail_full={tail_full}/{args.trials}")
        print(f"  prefix_rank_range={min(prefix_ranks)}..{max(prefix_ranks)}")
        print(f"  selected_rank_range={min(selected_ranks)}..{max(selected_ranks)}")
        print(
            "  tail_augmentation_range="
            f"{min(tail_augmentations)}..{max(tail_augmentations)}"
        )
    print()
    print("interpretation")
    print("  identity_action_is_unit_symmetric_but_not_transverse=1")
    print("  permutation_action_success_is_typical_not_formal=1")
    print("  p24_still_needs_the_representative_punit_nonvanishing=1")
    print("conclusion=reported_unit_orbit_transversality_toy")


if __name__ == "__main__":
    main()

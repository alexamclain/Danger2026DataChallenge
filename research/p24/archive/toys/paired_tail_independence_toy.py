#!/usr/bin/env python3
"""Random linear toy for paired tail-factor independence.

The p24 paired certificate uses three four-block prefix maps.  Each prefix
excludes a pair of right orbits, and the same prefix kernel must be separated
by two different 16-coordinate tail maps, one for each deleted orbit in the
pair.

This toy asks whether one tail factor can force the other by finite linear
algebra alone.  It uses small random block matrices over F_q with the same
shape:

    source_dim = 4*block_len + tail_len,
    six right blocks of length block_len,
    three paired prefixes.

Rows are scalar coordinates of the block maps.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q


PAIRS = ((0, 1), (2, 3), (4, 5))


@dataclass(frozen=True)
class PairResult:
    trial: int
    pair: tuple[int, int]
    prefix_rank: int
    prefix_full: bool
    left_tail_aug: int
    right_tail_aug: int
    left_tail_full: bool
    right_tail_full: bool


def random_row(dim: int, q: int, rng: random.Random) -> list[int]:
    return [rng.randrange(q) for _ in range(dim)]


def random_blocks(
    block_count: int,
    block_len: int,
    source_dim: int,
    q: int,
    rng: random.Random,
) -> list[list[list[int]]]:
    return [
        [random_row(source_dim, q, rng) for _ in range(block_len)]
        for _ in range(block_count)
    ]


def pair_result(
    trial: int,
    pair: tuple[int, int],
    blocks: list[list[list[int]]],
    block_len: int,
    tail_len: int,
    source_dim: int,
    q: int,
) -> PairResult:
    prefix_indices = [
        index for index in range(len(blocks)) if index not in pair
    ]
    prefix_rows = [
        row for index in prefix_indices for row in blocks[index]
    ]
    prefix_rank = rank_mod_q(prefix_rows, q)
    prefix_full_dim = source_dim - tail_len
    left_tail = blocks[pair[0]][:tail_len]
    right_tail = blocks[pair[1]][:tail_len]
    left_aug = rank_mod_q(prefix_rows + left_tail, q) - prefix_rank
    right_aug = rank_mod_q(prefix_rows + right_tail, q) - prefix_rank
    return PairResult(
        trial=trial,
        pair=pair,
        prefix_rank=prefix_rank,
        prefix_full=(prefix_rank == prefix_full_dim),
        left_tail_aug=left_aug,
        right_tail_aug=right_aug,
        left_tail_full=(left_aug == tail_len),
        right_tail_full=(right_aug == tail_len),
    )


def format_result(row: PairResult) -> str:
    return (
        f"trial={row.trial} pair=({row.pair[0]},{row.pair[1]}) "
        f"prefix_rank={row.prefix_rank} prefix_full={int(row.prefix_full)} "
        f"left_tail_aug={row.left_tail_aug} "
        f"right_tail_aug={row.right_tail_aug} "
        f"left_full={int(row.left_tail_full)} "
        f"right_full={int(row.right_tail_full)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--block-len", type=int, default=3)
    parser.add_argument("--tail-len", type=int, default=2)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    source_dim = 4 * args.block_len + args.tail_len
    rng = random.Random(args.seed)
    rows: list[PairResult] = []
    for trial in range(args.trials):
        blocks = random_blocks(6, args.block_len, source_dim, args.q, rng)
        rows.extend(
            pair_result(
                trial,
                pair,
                blocks,
                args.block_len,
                args.tail_len,
                source_dim,
                args.q,
            )
            for pair in PAIRS
        )

    prefix_full = [row for row in rows if row.prefix_full]
    both_full = [
        row for row in prefix_full if row.left_tail_full and row.right_tail_full
    ]
    exactly_one_full = [
        row for row in prefix_full
        if row.left_tail_full != row.right_tail_full
    ]
    neither_full = [
        row for row in prefix_full
        if not row.left_tail_full and not row.right_tail_full
    ]

    print("paired tail independence toy")
    print(f"q={args.q}")
    print(f"block_len={args.block_len}")
    print(f"tail_len={args.tail_len}")
    print(f"source_dim={source_dim}")
    print(f"trials={args.trials}")
    print()
    if not args.summary_only:
        for row in rows[:80]:
            print(format_result(row))
    print()
    print("summary")
    print(f"  pair_tests={len(rows)}")
    print(f"  prefix_full_tests={len(prefix_full)}")
    print(f"  both_tail_full_tests={len(both_full)}")
    print(f"  exactly_one_tail_full_tests={len(exactly_one_full)}")
    print(f"  neither_tail_full_tests={len(neither_full)}")
    if prefix_full:
        print(
            "  max_tail_aug_sum_when_prefix_full="
            f"{max(row.left_tail_aug + row.right_tail_aug for row in prefix_full)}"
        )
    print()
    print("interpretation")
    print("  exactly_one_tail_full_shows_twin_tail_factors_do_not_imply_each_other=1")
    print("  both_tail_full_is_the_paired_certificate_success_condition=1")
    print("conclusion=reported_paired_tail_independence_toy")


if __name__ == "__main__":
    main()

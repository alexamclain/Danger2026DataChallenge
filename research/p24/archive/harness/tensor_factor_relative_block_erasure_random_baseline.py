#!/usr/bin/env python3
"""Random baseline for relative block-erasure audits.

This tests the same small shapes that appear in the trace-frame tensor audits,
but with random E-linear matrices.  It calibrates whether "all
dimension-sufficient block projections recover" is special in the small data
or just generic over the tested fields.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import random

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    rank_over_extension,
)


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_matrix(
    rows: int,
    relative_degree: int,
    subdegree: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[list[FpE]]:
    return [
        [
            random_element(field, rng)
            for _ in range(relative_degree * subdegree)
        ]
        for _ in range(rows)
    ]


def selected_columns(subdegree: int, indices: tuple[int, ...]) -> list[int]:
    out: list[int] = []
    for index in indices:
        out.extend(range(index * subdegree, (index + 1) * subdegree))
    return out


def projection_rank(
    matrix: list[list[FpE]],
    columns: list[int],
    field: ExtensionField,
) -> int:
    return rank_over_extension([[row[col] for col in columns] for row in matrix], field)


def trial_has_failure(
    matrix: list[list[FpE]],
    raw_rank: int,
    relative_degree: int,
    subdegree: int,
    blocks_needed: int,
    field: ExtensionField,
) -> bool:
    if rank_over_extension(matrix, field) < raw_rank:
        return True
    for indices in combinations(range(relative_degree), blocks_needed):
        if projection_rank(matrix, selected_columns(subdegree, indices), field) < raw_rank:
            return True
    return False


def run_shape(
    raw_rank: int,
    relative_degree: int,
    subdegree: int,
    field: ExtensionField,
    trials: int,
    rng: random.Random,
) -> tuple[int, int]:
    blocks_needed = (raw_rank + subdegree - 1) // subdegree
    failures = 0
    for _ in range(trials):
        matrix = random_matrix(raw_rank, relative_degree, subdegree, field, rng)
        if trial_has_failure(
            matrix,
            raw_rank,
            relative_degree,
            subdegree,
            blocks_needed,
            field,
        ):
            failures += 1
    return failures, blocks_needed


def parse_shapes(text: str) -> list[tuple[int, int, int]]:
    out: list[tuple[int, int, int]] = []
    for part in text.split(","):
        if not part:
            continue
        raw, rel, sub = part.split(":")
        out.append((int(raw), int(rel), int(sub)))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=11243)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument(
        "--shapes",
        default="6:3:2,4:3:2,3:3:2,6:2:3,4:2:3,3:2:3",
        help="comma-separated raw_rank:relative_degree:subdegree shapes",
    )
    args = parser.parse_args()

    modulus = find_irreducible_modulus(args.q, args.degree, args.seed)
    field = ExtensionField(args.q, args.degree, modulus)
    rng = random.Random(args.seed)

    print("relative block-erasure random baseline")
    print(f"q={args.q}")
    print(f"extension_degree={args.degree}")
    print(f"trials={args.trials}")
    print()
    total_failures = 0
    for raw_rank, relative_degree, subdegree in parse_shapes(args.shapes):
        failures, blocks_needed = run_shape(
            raw_rank,
            relative_degree,
            subdegree,
            field,
            args.trials,
            rng,
        )
        total_failures += failures
        print(
            f"shape raw_rank={raw_rank} relative_degree={relative_degree} "
            f"subdegree={subdegree} blocks_needed={blocks_needed} "
            f"failures={failures}/{args.trials}"
        )
    print()
    print("summary")
    print(f"  total_failures={total_failures}")
    print("interpretation")
    print("  zero_or_low_random_failures_means_small_erasure_success_is_generic=1")
    print("  p24_still_needs_arithmetic_msrd_or_punit_identity=1")
    print("conclusion=reported_relative_block_erasure_random_baseline")


if __name__ == "__main__":
    main()

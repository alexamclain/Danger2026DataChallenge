#!/usr/bin/env python3
"""Block-equivalence invariant audit for the hidden MSRD route.

The trace-frame local-unit theorem would follow from a much stronger theorem:
the relative coefficient code is p-unit block-equivalent to a high-distance
sum-rank/MSRD code.  Any such block-equivalence preserves the block support
profile:

* ranks of projections to block subsets;
* dimensions of shortenings to block subsets;
* generalized block-support weights.

This script checks those invariants on small CM tensor rows and compares them
with random controls of the same shape.  It is a falsifier for the hidden MSRD
strengthening, not a proof of the p24 certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
import math
import random

from k_character_tensor_rank_scan import ExtensionField, FpE, rank_over_extension
from tensor_factor_relative_block_structure_audit import (
    Matrix,
    prepare_case,
    random_matrix,
)


@dataclass(frozen=True)
class BlockSubsetStats:
    size: int
    subset_count: int
    rank_hist: dict[int, int]
    shortened_hist: dict[int, int]
    rank_defects: int
    shortened_defects: int


@dataclass(frozen=True)
class SupportProfile:
    full_rank: int
    relative_degree: int
    subdegree: int
    msrd_profile_ok: bool
    rank_defects: int
    shortened_defects: int
    max_rank_defect: int
    max_shortened_defect: int
    min_block_support: int | None
    generalized_block_weights: tuple[int | None, ...]
    by_size: tuple[BlockSubsetStats, ...]


def hist(values: list[object]) -> dict[object, int]:
    return dict(sorted(Counter(values).items(), key=lambda item: str(item[0])))


def block_columns(blocks: tuple[int, ...], subdegree: int) -> list[int]:
    out: list[int] = []
    for block in blocks:
        out.extend(range(block * subdegree, (block + 1) * subdegree))
    return out


def project_columns(matrix: Matrix, columns: list[int]) -> Matrix:
    return [[row[col] for col in columns] for row in matrix]


def projection_rank(
    matrix: Matrix,
    blocks: tuple[int, ...],
    subdegree: int,
    field: ExtensionField,
) -> int:
    if not blocks:
        return 0
    return rank_over_extension(project_columns(matrix, block_columns(blocks, subdegree)), field)


def complement(blocks: tuple[int, ...], relative_degree: int) -> tuple[int, ...]:
    block_set = set(blocks)
    return tuple(block for block in range(relative_degree) if block not in block_set)


def support_profile(
    matrix: Matrix,
    relative_degree: int,
    subdegree: int,
    field: ExtensionField,
    max_generalized_weight: int,
    max_subsets: int,
) -> SupportProfile:
    full_rank = rank_over_extension(matrix, field)
    by_size: list[BlockSubsetStats] = []
    rank_defects = 0
    shortened_defects = 0
    max_rank_defect = 0
    max_shortened_defect = 0
    shortened_pairs: list[tuple[int, int]] = []

    for size in range(relative_degree + 1):
        subset_count = math.comb(relative_degree, size)
        if subset_count > max_subsets:
            continue
        ranks: list[int] = []
        shortenings: list[int] = []
        size_rank_defects = 0
        size_shortened_defects = 0
        expected_rank = min(full_rank, size * subdegree)
        expected_shortened = max(0, full_rank - (relative_degree - size) * subdegree)
        for blocks in combinations(range(relative_degree), size):
            rank = projection_rank(matrix, blocks, subdegree, field)
            comp_rank = projection_rank(
                matrix,
                complement(blocks, relative_degree),
                subdegree,
                field,
            )
            shortened = full_rank - comp_rank
            ranks.append(rank)
            shortenings.append(shortened)
            shortened_pairs.append((size, shortened))
            if rank != expected_rank:
                size_rank_defects += 1
                max_rank_defect = max(max_rank_defect, expected_rank - rank)
            if shortened != expected_shortened:
                size_shortened_defects += 1
                max_shortened_defect = max(
                    max_shortened_defect,
                    expected_shortened - shortened,
                )
        rank_defects += size_rank_defects
        shortened_defects += size_shortened_defects
        by_size.append(
            BlockSubsetStats(
                size=size,
                subset_count=subset_count,
                rank_hist=hist(ranks),
                shortened_hist=hist(shortenings),
                rank_defects=size_rank_defects,
                shortened_defects=size_shortened_defects,
            )
        )

    min_block_support = None
    for size, shortened in sorted(shortened_pairs):
        if shortened > 0:
            min_block_support = size
            break

    weights: list[int | None] = []
    for target_dim in range(1, min(full_rank, max_generalized_weight) + 1):
        found = None
        for size, shortened in sorted(shortened_pairs):
            if shortened >= target_dim:
                found = size
                break
        weights.append(found)

    return SupportProfile(
        full_rank=full_rank,
        relative_degree=relative_degree,
        subdegree=subdegree,
        msrd_profile_ok=(rank_defects == 0 and shortened_defects == 0),
        rank_defects=rank_defects,
        shortened_defects=shortened_defects,
        max_rank_defect=max_rank_defect,
        max_shortened_defect=max_shortened_defect,
        min_block_support=min_block_support,
        generalized_block_weights=tuple(weights),
        by_size=tuple(by_size),
    )


def profile_signature(profile: SupportProfile) -> tuple[object, ...]:
    return (
        profile.msrd_profile_ok,
        profile.rank_defects,
        profile.shortened_defects,
        profile.min_block_support,
        profile.generalized_block_weights,
    )


def print_profile(label: str, profile: SupportProfile) -> None:
    print(label)
    print(f"  full_rank={profile.full_rank}")
    print(f"  relative_degree={profile.relative_degree}")
    print(f"  subdegree={profile.subdegree}")
    print(f"  msrd_profile_ok={int(profile.msrd_profile_ok)}")
    print(f"  rank_defects={profile.rank_defects}")
    print(f"  shortened_defects={profile.shortened_defects}")
    print(f"  max_rank_defect={profile.max_rank_defect}")
    print(f"  max_shortened_defect={profile.max_shortened_defect}")
    print(f"  min_block_support={profile.min_block_support}")
    print(f"  generalized_block_weights={profile.generalized_block_weights}")
    for stats in profile.by_size:
        print(
            f"    blocks={stats.size} subsets={stats.subset_count} "
            f"rank_hist={stats.rank_hist} "
            f"shortened_hist={stats.shortened_hist} "
            f"rank_defects={stats.rank_defects} "
            f"shortened_defects={stats.shortened_defects}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=100)
    parser.add_argument("--max-generalized-weight", type=int, default=12)
    parser.add_argument("--max-subsets", type=int, default=10000)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=48)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=2)
    parser.add_argument("--target", default="axis")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    prepared = prepare_case(args)
    cm_profile = support_profile(
        prepared.matrix,
        prepared.relative_degree,
        prepared.subdegree,
        prepared.field,
        args.max_generalized_weight,
        args.max_subsets,
    )

    rng = random.Random(args.seed + 9001)
    random_profiles = [
        support_profile(
            random_matrix(
                len(prepared.matrix),
                prepared.relative_degree * prepared.subdegree,
                prepared.field,
                rng,
            ),
            prepared.relative_degree,
            prepared.subdegree,
            prepared.field,
            args.max_generalized_weight,
            args.max_subsets,
        )
        for _ in range(args.random_trials)
    ]

    print("trace-frame hidden-MSRD invariant audit")
    print(f"D={prepared.D}")
    print(f"q={prepared.q}")
    print(f"ell={prepared.ell}")
    print(f"h={prepared.h}")
    print(f"m={prepared.m}")
    print(f"n={prepared.n}")
    print(f"factor_degree={prepared.factor_degree}")
    print(f"extension_degree={prepared.extension_degree}")
    print(f"tensor_factor_degree={prepared.tensor_factor_degree}")
    print(f"target={prepared.target}")
    print(f"rows={len(prepared.matrix)}")
    print(f"cols={len(prepared.matrix[0]) if prepared.matrix else 0}")
    print()
    print_profile("cm_profile", cm_profile)
    print()
    print("random_controls")
    print(f"  trials={args.random_trials}")
    print(
        "  msrd_profile_ok="
        f"{sum(int(profile.msrd_profile_ok) for profile in random_profiles)}/"
        f"{args.random_trials}"
    )
    print(
        "  signature_hist="
        + str(hist([profile_signature(profile) for profile in random_profiles]))
    )
    print(
        "  generalized_weight_hist="
        + str(hist([profile.generalized_block_weights for profile in random_profiles]))
    )
    print(
        "  min_block_support_hist="
        + str(hist([profile.min_block_support for profile in random_profiles]))
    )
    print()
    print("interpretation")
    print("  msrd_profile_ok=0 would falsify hidden_MSRD_profile_for_this_row=1")
    print("  matching_random_profiles_means_this_invariant_does_not_explain_the_punit=1")
    print("  p24_still_needs_explicit_block_equivalence_or_direct_fitting_punit=1")
    print("conclusion=reported_trace_frame_msrd_invariant_audit")


if __name__ == "__main__":
    main()

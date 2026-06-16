#!/usr/bin/env python3
"""Audit block-subspace-design behavior for actual Lang coordinates.

The p24 representative certificate can be viewed as an array-code/MDS
subspace statement.  Six right Frobenius orbits give six blocks of length 35
inside L = F_p(mu_157).  The representative row keeps four full blocks and a
16-coordinate tail from a fifth block.  A CS-theory proof would follow from a
strong block-subspace design theorem:

    block spans are in direct/general position, and
    the next block projects with the required quotient rank.

This script tests that theorem shape on small actual-CM Lang rows.  It is
cheaper and more targeted than enumerating all scalar subsets: it measures
block-subset ranks and the canonical delete-one prefix/tail augmentation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from math import gcd
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from k_character_tensor_rank_scan import FpE
from lang_arc_strength_audit import transformed_blocks_for_row
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class DeleteOneProfile:
    omitted: int
    kept_capacity: int
    prefix_block_count: int
    prefix_len: int
    tail_len: int
    prefix_rank: int
    tail_rank_gain: int
    leading_rank: int
    prefix_full: bool
    tail_full: bool
    leading_full: bool


@dataclass(frozen=True)
class BlockDesignRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_lengths: tuple[int, ...]
    block_count: int
    coordinate_count: int
    coordinate_rank: int
    block_subset_total: int
    block_subset_tested: int
    block_subset_generic: int
    block_subset_defective: int
    first_defective_subset: tuple[int, ...] | None
    delete_profiles: tuple[DeleteOneProfile, ...]
    random_trials: int
    random_all_block_generic: int
    random_all_delete_tail_full: int


def flatten(blocks: list[list[FpE]], subset: tuple[int, ...]) -> list[FpE]:
    out: list[FpE] = []
    for index in subset:
        out.extend(blocks[index])
    return out


def prefix_split(lengths: list[int], target: int) -> tuple[int, int, int]:
    prefix_len = 0
    block_count = 0
    for length in lengths:
        if prefix_len + length > target:
            break
        prefix_len += length
        block_count += 1
    return block_count, prefix_len, target - prefix_len


def delete_one_profile(
    blocks: list[list[FpE]],
    omitted: int,
    left_len: int,
    q: int,
) -> DeleteOneProfile:
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    lengths = [len(block) for block in kept]
    block_count, prefix_len, tail_len = prefix_split(lengths, left_len)
    values = [value for block in kept for value in block]
    prefix = values[:prefix_len]
    leading = values[:left_len]
    prefix_rank = fq_rank(prefix, q)
    leading_rank = fq_rank(leading, q)
    return DeleteOneProfile(
        omitted=omitted,
        kept_capacity=sum(lengths),
        prefix_block_count=block_count,
        prefix_len=prefix_len,
        tail_len=tail_len,
        prefix_rank=prefix_rank,
        tail_rank_gain=leading_rank - prefix_rank,
        leading_rank=leading_rank,
        prefix_full=(prefix_rank == min(prefix_len, left_len)),
        tail_full=(leading_rank - prefix_rank == tail_len),
        leading_full=(leading_rank == left_len),
    )


def random_blocks(
    q: int,
    left_len: int,
    lengths: tuple[int, ...],
    rng: random.Random,
) -> list[list[FpE]]:
    blocks: list[list[FpE]] = []
    for length in lengths:
        block: list[FpE] = []
        for _ in range(length):
            coords = [rng.randrange(q) for _ in range(left_len)]
            block.append(tuple(coords))
        blocks.append(block)
    return blocks


def audit_blocks(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    seed: int,
    random_trials: int,
) -> BlockDesignRow | None:
    try:
        extension_degree, _field, blocks = transformed_blocks_for_row(
            D, q, ell, cycle, m, factor, left, right, left_orbit, seed
        )
    except ValueError:
        return None

    left_len = len(left_orbit)
    values = [value for block in blocks for value in block]
    coordinate_rank = fq_rank(values, q)
    right_lengths = tuple(len(block) for block in blocks)

    subset_total = 0
    subset_tested = 0
    subset_generic = 0
    subset_defective = 0
    first_defective: tuple[int, ...] | None = None
    for size in range(1, len(blocks) + 1):
        for subset in combinations(range(len(blocks)), size):
            subset_total += 1
            expected = min(left_len, sum(right_lengths[index] for index in subset))
            rank = fq_rank(flatten(blocks, subset), q)
            subset_tested += 1
            if rank == expected:
                subset_generic += 1
            else:
                subset_defective += 1
                if first_defective is None:
                    first_defective = tuple(subset)

    delete_profiles = tuple(
        delete_one_profile(blocks, omitted, left_len, q)
        for omitted in range(len(blocks))
        if sum(len(block) for index, block in enumerate(blocks) if index != omitted)
        >= left_len
    )

    rng = random.Random(seed + 65537 * D + 257 * q + 19 * left + right)
    random_all_block_generic = 0
    random_all_delete_tail_full = 0
    for _trial in range(random_trials):
        trial_blocks = random_blocks(q, left_len, right_lengths, rng)
        all_generic = True
        for size in range(1, len(trial_blocks) + 1):
            for subset in combinations(range(len(trial_blocks)), size):
                expected = min(left_len, sum(right_lengths[index] for index in subset))
                if fq_rank(flatten(trial_blocks, subset), q) != expected:
                    all_generic = False
                    break
            if not all_generic:
                break
        random_all_block_generic += int(all_generic)
        trial_profiles = [
            delete_one_profile(trial_blocks, omitted, left_len, q)
            for omitted in range(len(trial_blocks))
            if sum(
                len(block)
                for index, block in enumerate(trial_blocks)
                if index != omitted
            )
            >= left_len
        ]
        random_all_delete_tail_full += int(
            bool(trial_profiles) and all(profile.tail_full for profile in trial_profiles)
        )

    return BlockDesignRow(
        D=D,
        q=q,
        ell=ell,
        h=len(cycle),
        m=m,
        n=len(cycle) // m,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=left_len,
        right_orbit_lengths=right_lengths,
        block_count=len(blocks),
        coordinate_count=len(values),
        coordinate_rank=coordinate_rank,
        block_subset_total=subset_total,
        block_subset_tested=subset_tested,
        block_subset_generic=subset_generic,
        block_subset_defective=subset_defective,
        first_defective_subset=first_defective,
        delete_profiles=delete_profiles,
        random_trials=random_trials,
        random_all_block_generic=random_all_block_generic,
        random_all_delete_tail_full=random_all_delete_tail_full,
    )


def scan(args: argparse.Namespace) -> list[BlockDesignRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[BlockDesignRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
        ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        case_had_cycle = False
        for q, roots in splits:
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            if min(len(orbit) for orbit in right_orbits) < args.min_right_orbit_len:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_blocks(
                                    D,
                                    q,
                                    ell,
                                    shifted,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args.seed,
                                    args.random_trials,
                                )
                                if row and row.coordinate_rank >= row.left_orbit_len:
                                    rows.append(row)
                                    if len(rows) >= args.max_rows:
                                        return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def profile_text(profile: DeleteOneProfile) -> str:
    return (
        f"omit{profile.omitted}:cap{profile.kept_capacity}:"
        f"blocks{profile.prefix_block_count}:tail{profile.tail_len}:"
        f"prefix{profile.prefix_rank}/{profile.prefix_len}:"
        f"gain{profile.tail_rank_gain}/{profile.tail_len}:"
        f"lead{profile.leading_rank}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--min-right-orbit-len", type=int, default=1)
    parser.add_argument("--random-trials", type=int, default=100)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("Lang block-subspace-design audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n deg ext pair left_orbit right_lengths "
        "rank block_generic delete_profiles random"
    )
    for row in rows:
        profiles = ";".join(profile_text(profile) for profile in row.delete_profiles)
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"deg={row.factor_degree} ext={row.extension_degree} "
            f"pair=({row.left},{row.right}) left={row.left_orbit_rep}:L{row.left_orbit_len} "
            f"right_lengths={list(row.right_orbit_lengths)} "
            f"rank={row.coordinate_rank}/{row.left_orbit_len} "
            f"block_generic={row.block_subset_generic}/{row.block_subset_total} "
            f"first_bad={row.first_defective_subset} "
            f"delete=[{profiles}] "
            f"random_block_generic={row.random_all_block_generic}/{row.random_trials} "
            f"random_delete_tail={row.random_all_delete_tail_full}/{row.random_trials}"
        )
    print()
    print("interpretation")
    print("  block_generic_tests_array_MDS_subspace_profile=1")
    print("  delete_profiles_test_full_blocks_plus_tail_recovery=1")
    print("  random_counts_measure_whether_success_is_special_or_generic=1")
    print("conclusion=reported_lang_block_subspace_design_audit")


if __name__ == "__main__":
    main()

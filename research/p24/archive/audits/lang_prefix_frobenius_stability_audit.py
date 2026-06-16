#!/usr/bin/env python3
"""Audit Frobenius-stability of Lang prefix spans.

One remaining CS/class-field shortcut is that the representative prefix kernel
`K` might be a Frobenius-component sum.  Since the prefix kernel is trace-dual
to the span of the prefix coordinates, this would force the prefix span to be
Frobenius-stable as an F_q-subspace of the left character field.

This script tests that necessary condition on small actual-CM Lang rows.  For
each delete-one canonical ordering it computes:

* the full-block prefix span before the tail begins;
* the leading span after adding the tail up to the left-orbit dimension;
* rank(span + Frobenius(span)) - rank(span).

A nonzero defect rules out a literal Frobenius-component explanation for that
prefix.  Random subfield controls with the same dimensions are included.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from hermitian_mixed_left_subfield_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import ExtensionField, FpE
from lang_arc_strength_audit import transformed_blocks_for_row
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class StabilityProfile:
    omitted: int
    kept_capacity: int
    prefix_block_count: int
    prefix_len: int
    tail_len: int
    prefix_rank: int
    leading_rank: int
    prefix_stability_defect: int
    leading_stability_defect: int
    random_prefix_stable: int
    random_leading_stable: int


@dataclass(frozen=True)
class StabilityRow:
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
    transformed_rank: int
    profiles: tuple[StabilityProfile, ...]
    random_trials: int


def prefix_split(lengths: list[int], target: int) -> tuple[int, int, int]:
    prefix_len = 0
    block_count = 0
    for length in lengths:
        if prefix_len + length > target:
            break
        prefix_len += length
        block_count += 1
    return block_count, prefix_len, target - prefix_len


def frobenius_values(values: list[FpE], field: ExtensionField) -> list[FpE]:
    return [field.pow(value, field.q) for value in values]


def stability_defect(values: list[FpE], q: int, field: ExtensionField) -> int:
    rank = fq_rank(values, q)
    joined_rank = fq_rank(values + frobenius_values(values, field), q)
    return joined_rank - rank


def random_subfield_values(
    count: int,
    basis: list[FpE],
    q: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[FpE]:
    out: list[FpE] = []
    for _ in range(count):
        total = field.zero
        for base in basis:
            coeff = rng.randrange(q)
            if coeff:
                total = field.add(total, field.scalar_mul(coeff, base))
        out.append(total)
    return out


def stability_profile(
    blocks: list[list[FpE]],
    omitted: int,
    left_len: int,
    q: int,
    field: ExtensionField,
    random_trials: int,
    seed: int,
) -> StabilityProfile | None:
    kept = [block for index, block in enumerate(blocks) if index != omitted]
    lengths = [len(block) for block in kept]
    if sum(lengths) < left_len:
        return None
    block_count, prefix_len, tail_len = prefix_split(lengths, left_len)
    values = [value for block in kept for value in block]
    prefix = values[:prefix_len]
    leading = values[:left_len]
    prefix_rank = fq_rank(prefix, q)
    leading_rank = fq_rank(leading, q)
    prefix_defect = stability_defect(prefix, q, field)
    leading_defect = stability_defect(leading, q, field)

    sub_basis = subfield_power_basis(q, left_len, field, seed)
    rng = random.Random(seed + 4099 * omitted + 17 * prefix_len + tail_len)
    random_prefix_stable = 0
    random_leading_stable = 0
    for _ in range(random_trials):
        random_prefix = random_subfield_values(prefix_len, sub_basis, q, field, rng)
        random_leading = random_subfield_values(left_len, sub_basis, q, field, rng)
        random_prefix_stable += int(stability_defect(random_prefix, q, field) == 0)
        random_leading_stable += int(stability_defect(random_leading, q, field) == 0)

    return StabilityProfile(
        omitted=omitted,
        kept_capacity=sum(lengths),
        prefix_block_count=block_count,
        prefix_len=prefix_len,
        tail_len=tail_len,
        prefix_rank=prefix_rank,
        leading_rank=leading_rank,
        prefix_stability_defect=prefix_defect,
        leading_stability_defect=leading_defect,
        random_prefix_stable=random_prefix_stable,
        random_leading_stable=random_leading_stable,
    )


def audit_row(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    args: argparse.Namespace,
) -> StabilityRow | None:
    try:
        extension_degree, field, blocks = transformed_blocks_for_row(
            D, q, ell, cycle, m, factor, left, right, left_orbit, args.seed
        )
    except ValueError:
        return None
    left_len = len(left_orbit)
    if field.degree % left_len:
        return None
    values = [value for block in blocks for value in block]
    profiles = tuple(
        profile
        for omitted in range(len(blocks))
        if (
            profile := stability_profile(
                blocks,
                omitted,
                left_len,
                q,
                field,
                args.random_trials,
                args.seed + 101 * D + q,
            )
        )
        is not None
    )
    if not profiles:
        return None
    return StabilityRow(
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
        right_orbit_lengths=tuple(len(block) for block in blocks),
        transformed_rank=fq_rank(values, q),
        profiles=profiles,
        random_trials=args.random_trials,
    )


def scan(args: argparse.Namespace) -> list[StabilityRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[StabilityRow] = []
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
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_row(
                                    D,
                                    q,
                                    ell,
                                    shifted,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args,
                                )
                                if row and row.transformed_rank >= row.left_orbit_len:
                                    rows.append(row)
                                    if len(rows) >= args.max_rows:
                                        return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def profile_text(profile: StabilityProfile, trials: int) -> str:
    return (
        f"omit{profile.omitted}:cap{profile.kept_capacity}:"
        f"blocks{profile.prefix_block_count}:tail{profile.tail_len}:"
        f"prank{profile.prefix_rank}/{profile.prefix_len}:"
        f"lead{profile.leading_rank}:"
        f"pdef{profile.prefix_stability_defect}:"
        f"ldef{profile.leading_stability_defect}:"
        f"randP{profile.random_prefix_stable}/{trials}:"
        f"randL{profile.random_leading_stable}/{trials}"
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
    print("Lang prefix Frobenius-stability audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n deg ext pair left right_lengths rank profiles"
    )
    for row in rows:
        profiles = ";".join(
            profile_text(profile, row.random_trials) for profile in row.profiles
        )
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"deg={row.factor_degree} ext={row.extension_degree} "
            f"pair=({row.left},{row.right}) left={row.left_orbit_rep}:L{row.left_orbit_len} "
            f"right_lengths={list(row.right_orbit_lengths)} "
            f"rank={row.transformed_rank}/{row.left_orbit_len} "
            f"profiles=[{profiles}]"
        )
    print()
    print("interpretation")
    print("  nonzero_prefix_defect_rules_out_Frobenius_component_prefix=1")
    print("  leading_defect_can_be_nonzero_even_when_leading_rank_is_full=1")
    print("  random_stability_counts_are_controls_inside_the_left_subfield=1")
    print("conclusion=reported_lang_prefix_frobenius_stability_audit")


if __name__ == "__main__":
    main()

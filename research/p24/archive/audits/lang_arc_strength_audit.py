#!/usr/bin/env python3
"""Audit whether actual Lang coordinates behave like a full Moore arc.

The representative p24 p-unit asks for one support-specific Moore determinant.
One attractive CS shortcut would be stronger: the transformed CM coordinates
form a Gabidulin/MDS-like arc, so every left-degree coordinate subset is
independent.  This script tests that stronger property on small actual-CM rows.

The value is mostly negative/falsifying.  If full-arc behavior already fails in
small rows where the selected leading minors work, then an MSRD/LRS import must
prove a support-specific equivalence, not a blanket "all subsets" theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, islice
from math import comb, gcd
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from hermitian_mixed_left_subfield_normality_audit import (
    transformed_coordinates_for_left_orbit,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class ArcAuditRow:
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
    coordinate_count: int
    coordinate_rank: int
    subset_size: int
    subset_total: int
    subset_tested: int
    subset_full: int
    subset_bad: int
    first_bad_subset: tuple[int, ...] | None
    random_trials: int
    random_full_arc_count: int
    random_bad_subset_min: int
    random_bad_subset_max: int
    delete_one_leading_full: tuple[int, ...]


def transformed_blocks_for_row(
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
) -> tuple[int, ExtensionField, list[list[FpE]]]:
    if factor.degree() % 2:
        raise ValueError("Hermitian packet factor degree must be even")
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        raise ValueError("packet factor is not Hermitian")
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    powers = zeta_powers(zeta, m, field)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    marginal = double_marginal(kernel, left, right, q)
    dft_matrix = dft_double_marginal(marginal, left, right, powers, m, field)
    right_orbits = q_orbits(right, q)
    transformed = transformed_coordinates_for_left_orbit(
        dft_matrix,
        left,
        right,
        left_orbit,
        right_orbits,
        q,
        field,
        seed,
    )
    blocks: list[list[FpE]] = []
    offset = 0
    for orbit in right_orbits:
        blocks.append(transformed[offset : offset + len(orbit)])
        offset += len(orbit)
    return extension_degree, field, blocks


def leading_values_after_deletion(
    blocks: list[list[FpE]],
    omitted: int,
    left_len: int,
) -> list[FpE]:
    values: list[FpE] = []
    for index, block in enumerate(blocks):
        if index == omitted:
            continue
        values.extend(block)
        if len(values) >= left_len:
            return values[:left_len]
    return values[:left_len]


def audit_arc(
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
    max_subsets: int,
    random_trials: int,
) -> ArcAuditRow | None:
    try:
        extension_degree, field, blocks = transformed_blocks_for_row(
            D, q, ell, cycle, m, factor, left, right, left_orbit, seed
        )
    except ValueError:
        return None
    values = [value for block in blocks for value in block]
    left_len = len(left_orbit)
    if len(values) < left_len:
        return None
    coordinate_rank = fq_rank(values, q)
    subset_total = comb(len(values), left_len)
    iterator = combinations(range(len(values)), left_len)
    if subset_total > max_subsets:
        iterator = islice(iterator, max_subsets)
    tested = 0
    full = 0
    bad = 0
    first_bad: tuple[int, ...] | None = None
    for subset in iterator:
        tested += 1
        rank = fq_rank([values[index] for index in subset], q)
        if rank >= left_len:
            full += 1
        else:
            bad += 1
            if first_bad is None:
                first_bad = tuple(subset)
    random_full_arc_count = 0
    random_bad_counts: list[int] = []
    rng = random.Random(seed + 65537 * D + 257 * q + 17 * left + right)
    for _ in range(random_trials):
        random_values: list[FpE] = []
        for _index in range(len(values)):
            coords = [0 for _ in range(field.degree)]
            for pos in range(left_len):
                coords[pos] = rng.randrange(q)
            random_values.append(tuple(coords))
        random_bad = 0
        random_iterator = combinations(range(len(values)), left_len)
        if subset_total > max_subsets:
            random_iterator = islice(random_iterator, max_subsets)
        for subset in random_iterator:
            rank = fq_rank([random_values[index] for index in subset], q)
            if rank < left_len:
                random_bad += 1
        random_bad_counts.append(random_bad)
        if random_bad == 0:
            random_full_arc_count += 1
    delete_full: list[int] = []
    for omitted in range(len(blocks)):
        leading = leading_values_after_deletion(blocks, omitted, left_len)
        delete_full.append(int(len(leading) == left_len and fq_rank(leading, q) >= left_len))
    return ArcAuditRow(
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
        right_orbit_lengths=tuple(len(orbit) for orbit in q_orbits(right, q)),
        coordinate_count=len(values),
        coordinate_rank=coordinate_rank,
        subset_size=left_len,
        subset_total=subset_total,
        subset_tested=tested,
        subset_full=full,
        subset_bad=bad,
        first_bad_subset=first_bad,
        random_trials=random_trials,
        random_full_arc_count=random_full_arc_count,
        random_bad_subset_min=min(random_bad_counts) if random_bad_counts else 0,
        random_bad_subset_max=max(random_bad_counts) if random_bad_counts else 0,
        delete_one_leading_full=tuple(delete_full),
    )


def scan(args: argparse.Namespace) -> ArcAuditRow | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
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
                    if factor.degree() > args.max_factor_degree:
                        continue
                    if factor.degree() < args.min_factor_degree:
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
                                row = audit_arc(
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
                                    args.max_subsets,
                                    args.random_trials,
                                )
                                if row and row.coordinate_rank >= row.left_orbit_len:
                                    return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
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
    parser.add_argument("--max-subsets", type=int, default=20000)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible actual-CM arc row found")

    print("Lang arc-strength audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit_rep={row.left_orbit_rep}")
    print(f"left_orbit_len={row.left_orbit_len}")
    print(f"right_orbit_lengths={list(row.right_orbit_lengths)}")
    print(f"coordinate_count={row.coordinate_count}")
    print(f"coordinate_rank={row.coordinate_rank}")
    print(f"subset_size={row.subset_size}")
    print(f"subset_total={row.subset_total}")
    print(f"subset_tested={row.subset_tested}")
    print(f"subset_full={row.subset_full}")
    print(f"subset_bad={row.subset_bad}")
    print(f"first_bad_subset={row.first_bad_subset}")
    print(f"random_trials={row.random_trials}")
    print(f"random_full_arc_count={row.random_full_arc_count}")
    print(f"random_bad_subset_range={row.random_bad_subset_min}..{row.random_bad_subset_max}")
    print(f"delete_one_leading_full={list(row.delete_one_leading_full)}")
    print()
    print("interpretation")
    print("  full_arc_success_would_support_a_blanket_MSRD_or_MDS_shortcut=1")
    print("  bad_subsets_mean_selected_minor_proof_must_be_support_specific=1")
    print("  delete_one_vector_records_the_current_leading_windows_only=1")
    print("conclusion=reported_lang_arc_strength_audit")


if __name__ == "__main__":
    main()

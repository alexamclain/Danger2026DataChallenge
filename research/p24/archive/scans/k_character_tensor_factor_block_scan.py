#!/usr/bin/env python3
"""Block-rank audit inside one K-character tensor factor.

The one-factor tensor theorem asks for full rank of the axis frequency set.
This script separates that into:

* internal rank of each component block;
* pairwise directness with the constant block;
* full directness of all component blocks.

It is a one-factor analogue of the earlier axis direct-sum scans.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    rank_in_factor,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


def frequency_blocks(m: int) -> list[tuple[str, list[int]]]:
    blocks = [("constant", [0])]
    for component in coprime_components(m):
        step = m // component
        blocks.append((str(component), [(j * step) % m for j in range(1, component)]))
    return blocks


def rows_for_frequencies(
    residue_vectors: list[list[int]],
    frequencies: list[int],
    zeta: FpE,
    field: ExtensionField,
) -> list[list[FpE]]:
    return character_rows(residue_vectors, frequencies, zeta, field)


@dataclass(frozen=True)
class BlockRankRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_count: int
    tensor_factor_degree: int
    axis_dim: int
    full_axis_rank: int
    block_ranks: tuple[tuple[str, int, int], ...]
    block_internal_failures: int
    block_internal_unforced_failures: int
    pair_directness_failures: int
    pair_directness_unforced_failures: int
    full_directness_failure: bool


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> BlockRankRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)

    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        seed,
    )
    selected_factor = factors[0]

    blocks = frequency_blocks(m)
    all_frequencies = [freq for _, freqs in blocks for freq in freqs]
    all_rows = rows_for_frequencies(residue_vectors, all_frequencies, zeta, field)
    full_rank = rank_in_factor(all_rows, selected_factor, field)

    block_ranks: list[tuple[str, int, int]] = []
    block_failures = 0
    block_unforced_failures = 0
    for name, freqs in blocks:
        rows = rows_for_frequencies(residue_vectors, freqs, zeta, field)
        rank = rank_in_factor(rows, selected_factor, field)
        expected = len(freqs)
        block_ranks.append((name, rank, expected))
        if rank < expected:
            block_failures += 1
            if expected <= tensor_factor_degree:
                block_unforced_failures += 1

    pair_failures = 0
    pair_unforced_failures = 0
    for index in range(1, len(blocks)):
        freqs = blocks[0][1] + blocks[index][1]
        rows = rows_for_frequencies(residue_vectors, freqs, zeta, field)
        rank = rank_in_factor(rows, selected_factor, field)
        if rank < len(freqs):
            pair_failures += 1
            if len(freqs) <= tensor_factor_degree:
                pair_unforced_failures += 1

    axis_dim = len(all_frequencies)
    return BlockRankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        tensor_factor_count=len(factors),
        tensor_factor_degree=tensor_factor_degree,
        axis_dim=axis_dim,
        full_axis_rank=full_rank,
        block_ranks=tuple(block_ranks),
        block_internal_failures=block_failures,
        block_internal_unforced_failures=block_unforced_failures,
        pair_directness_failures=pair_failures,
        pair_directness_unforced_failures=pair_unforced_failures,
        full_directness_failure=full_rank < axis_dim,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[BlockRankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[BlockRankRow] = []
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
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
        if args.max_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m <= args.max_m]
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
        if not splits:
            continue
        case_had_row = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
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
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    if factor.degree() // gcd_degree > args.max_tensor_factor_degree:
                        continue
                    rows.append(audit_packet(D, q, ell, cycle, m, factor, args.seed))
                    case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=10)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--max-m", type=int, default=40)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=40)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    dimension_possible = [
        row for row in rows if row.tensor_factor_degree >= row.axis_dim
    ]
    block_failure_rows = [row for row in rows if row.block_internal_failures]
    block_unforced_failure_rows = [
        row for row in rows if row.block_internal_unforced_failures
    ]
    pair_failure_rows = [row for row in rows if row.pair_directness_failures]
    pair_unforced_failure_rows = [
        row for row in rows if row.pair_directness_unforced_failures
    ]
    full_failure_rows = [row for row in rows if row.full_directness_failure]
    dimension_possible_full_failures = [
        row for row in dimension_possible if row.full_directness_failure
    ]
    dimension_possible_block_failures = [
        row for row in dimension_possible if row.block_internal_failures
    ]
    dimension_possible_pair_failures = [
        row for row in dimension_possible if row.pair_directness_failures
    ]

    print("K-character tensor factor block-rank scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_m={args.max_m}")
    print(f"max_factor_degree={args.max_factor_degree}")
    print(f"max_extension_degree={args.max_extension_degree}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext factor_deg axis full_rank "
            "block_ranks block_fail pair_fail full_fail"
        )
        display = dimension_possible_full_failures + rows[:60]
        seen_keys: set[tuple[int, int, int, int, int]] = set()
        for row in display[:80]:
            key = (row.D, row.q, row.m, row.n, row.factor_degree)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"factor_deg={row.tensor_factor_degree:3d} "
                f"axis={row.axis_dim:3d} full_rank={row.full_axis_rank:3d} "
                f"block_ranks={list(row.block_ranks)} "
                f"block_fail={row.block_internal_failures} "
                f"block_unforced={row.block_internal_unforced_failures} "
                f"pair_fail={row.pair_directness_failures} "
                f"pair_unforced={row.pair_directness_unforced_failures} "
                f"full_fail={int(row.full_directness_failure)}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  one_factor_dimension_possible_rows={len(dimension_possible)}")
    print(f"  block_internal_failure_rows={len(block_failure_rows)}")
    print(f"  block_internal_unforced_failure_rows={len(block_unforced_failure_rows)}")
    print(f"  pair_directness_failure_rows={len(pair_failure_rows)}")
    print(f"  pair_directness_unforced_failure_rows={len(pair_unforced_failure_rows)}")
    print(f"  full_directness_failure_rows={len(full_failure_rows)}")
    print(f"  dimension_possible_block_failure_rows={len(dimension_possible_block_failures)}")
    print(f"  dimension_possible_pair_failure_rows={len(dimension_possible_pair_failures)}")
    print(f"  dimension_possible_full_failure_rows={len(dimension_possible_full_failures)}")
    print()
    print("interpretation")
    print("  block_internal_failure_means_a_component_axis_is_not_normal_in_one_factor=1")
    print("  pair_failure_means_constant_plus_one_component_is_not_direct=1")
    print("  full_failure_means_cross-component directness fails or dimension bound bites=1")
    print("conclusion=reported_k_character_tensor_factor_block_scan")


if __name__ == "__main__":
    main()

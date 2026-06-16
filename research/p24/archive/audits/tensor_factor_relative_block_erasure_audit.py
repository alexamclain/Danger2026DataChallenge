#!/usr/bin/env python3
"""Relative coefficient-block erasure audit for the trace-frame target.

The trace-frame theorem uses the top three relative C-coefficients of
g'(theta)*x in B/C.  In sum-rank language this is one erasure pattern: keep a
few C-blocks, each of E-dimension [C:E], and recover the selected axis
subspace.

This audit checks small tensor rows for the stronger property that *any*
dimension-sufficient set of relative coefficient blocks recovers the target.
That is an MSRD/LRS-style strengthening; it is evidence only, but it separates
"top-of-basis accident" from a more invariant erasure-code profile.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
import math

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    PolyE,
    equal_degree_factors,
    poly_mod,
    rank_in_factor,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    axis_frequency_set,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from tensor_factor_dual_basis_window_audit import (
    discriminants,
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    solve_square,
)
from tensor_factor_moore_audit import b_is_zero, b_mul
from tensor_factor_subfield_trace_audit import divisors, element_row


@dataclass(frozen=True)
class BlockErasureTarget:
    name: str
    raw_rank: int
    subdegree: int
    relative_degree: int
    blocks_needed: int
    subset_tests: int
    subset_failures: int
    top_rank: int
    top_failure: bool


@dataclass(frozen=True)
class BlockErasureRow:
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
    targets: tuple[BlockErasureTarget, ...]


def coefficient_blocks(
    value: PolyE,
    subdegree: int,
    relative_degree: int,
    gprime_theta: PolyE,
    basis_columns: list[list[FpE]],
    factor: PolyE,
    field: ExtensionField,
) -> list[list[FpE]]:
    adjusted = b_mul(value, gprime_theta, factor, field)
    coords = solve_square(
        basis_columns,
        element_row(adjusted, factor, field),
        field,
    )
    return [
        coords[j * subdegree : (j + 1) * subdegree]
        for j in range(relative_degree)
    ]


def selected_block_vector(blocks: list[list[FpE]], indices: tuple[int, ...]) -> list[FpE]:
    out: list[FpE] = []
    for index in indices:
        out.extend(blocks[index])
    return out


def subset_rank(
    element_blocks: list[list[list[FpE]]],
    indices: tuple[int, ...],
    field: ExtensionField,
) -> int:
    return rank_over_extension(
        [selected_block_vector(blocks, indices) for blocks in element_blocks],
        field,
    )


def target_rows_for_m(
    residue_vectors: list[list[int]],
    m: int,
    zeta: FpE,
    field: ExtensionField,
) -> list[tuple[str, list[list[FpE]]]]:
    out: list[tuple[str, list[list[FpE]]]] = [
        ("axis", character_rows(residue_vectors, axis_frequency_set(m), zeta, field))
    ]
    for name, frequencies in frequency_blocks(m):
        rows = character_rows(residue_vectors, frequencies, zeta, field)
        out.append((name, rows))
        if name != "constant":
            out.append(
                (
                    f"constant_plus_{name}",
                    character_rows(
                        residue_vectors,
                        sorted(set([0] + frequencies)),
                        zeta,
                        field,
                    ),
                )
            )
    return out


def audit_target(
    name: str,
    rows: list[list[FpE]],
    subdegree: int,
    factor_degree: int,
    selected_factor: PolyE,
    field: ExtensionField,
    max_subsets: int,
) -> BlockErasureTarget | None:
    raw_rank = rank_in_factor(rows, selected_factor, field)
    if raw_rank == 0:
        return None
    relative_degree = factor_degree // subdegree
    blocks_needed = math.ceil(raw_rank / subdegree)
    if blocks_needed > relative_degree:
        return None
    subset_count = math.comb(relative_degree, blocks_needed)
    if subset_count > max_subsets:
        return None

    subfield_basis = normal_subfield_basis(
        subdegree,
        factor_degree,
        selected_factor,
        field,
    )
    basis_columns = relative_basis_columns(
        subfield_basis,
        relative_degree,
        selected_factor,
        field,
    )
    gprime_theta = relative_gprime_theta(
        subdegree,
        factor_degree,
        selected_factor,
        field,
    )
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    element_blocks = [
        coefficient_blocks(
            value,
            subdegree,
            relative_degree,
            gprime_theta,
            basis_columns,
            selected_factor,
            field,
        )
        for value in elements
    ]

    failures = 0
    tests = 0
    for indices in combinations(range(relative_degree), blocks_needed):
        tests += 1
        if subset_rank(element_blocks, indices, field) < raw_rank:
            failures += 1

    top_indices = tuple(range(relative_degree - blocks_needed, relative_degree))
    top_rank = subset_rank(element_blocks, top_indices, field)
    return BlockErasureTarget(
        name=name,
        raw_rank=raw_rank,
        subdegree=subdegree,
        relative_degree=relative_degree,
        blocks_needed=blocks_needed,
        subset_tests=tests,
        subset_failures=failures,
        top_rank=top_rank,
        top_failure=top_rank < raw_rank,
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    requested_subdegree: int | None,
    max_subsets: int,
) -> BlockErasureRow:
    h = len(cycle)
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
    subdegrees = [
        subdegree for subdegree in divisors(tensor_factor_degree)
        if subdegree not in (1, tensor_factor_degree)
    ]
    if requested_subdegree is not None:
        subdegrees = [subdegree for subdegree in subdegrees if subdegree == requested_subdegree]

    targets: list[BlockErasureTarget] = []
    for subdegree in subdegrees:
        for name, rows in target_rows_for_m(residue_vectors, m, zeta, field):
            target = audit_target(
                name,
                rows,
                subdegree,
                tensor_factor_degree,
                selected_factor,
                field,
                max_subsets,
            )
            if target is not None:
                targets.append(target)

    return BlockErasureRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=h // m,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        tensor_factor_count=len(factors),
        tensor_factor_degree=tensor_factor_degree,
        targets=tuple(targets),
    )


def scan(args: argparse.Namespace) -> list[BlockErasureRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[BlockErasureRow] = []
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
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
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
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    row = audit_packet(
                        D,
                        q,
                        ell,
                        cycle,
                        m,
                        factor,
                        args.seed,
                        args.subdegree,
                        args.max_subsets,
                    )
                    if row.targets:
                        rows.append(row)
                        case_had_row = True
                    if len(rows) >= args.max_rows:
                        return rows
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=8)
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
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int)
    parser.add_argument("--max-subsets", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    total_targets = 0
    total_subset_tests = 0
    total_subset_failures = 0
    total_top_failures = 0
    for row in rows:
        total_targets += len(row.targets)
        total_subset_tests += sum(target.subset_tests for target in row.targets)
        total_subset_failures += sum(target.subset_failures for target in row.targets)
        total_top_failures += sum(int(target.top_failure) for target in row.targets)

    print("tensor factor relative block-erasure audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"max_subsets={args.max_subsets}")
    print()
    if not args.summary_only:
        for row in rows:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"factors={row.tensor_factor_count:2d} "
                f"factor_deg={row.tensor_factor_degree:3d}"
            )
            for target in row.targets:
                print(
                    f"  target={target.name:16s} raw_rank={target.raw_rank:3d} "
                    f"subdegree={target.subdegree:3d} "
                    f"relative_degree={target.relative_degree:3d} "
                    f"blocks_needed={target.blocks_needed:2d} "
                    f"subset_failures={target.subset_failures:3d}/"
                    f"{target.subset_tests:3d} "
                    f"top_rank={target.top_rank:3d} "
                    f"top_failure={int(target.top_failure)}"
                )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  targets={total_targets}")
    print(f"  subset_tests={total_subset_tests}")
    print(f"  subset_failures={total_subset_failures}")
    print(f"  top_failures={total_top_failures}")
    print()
    print("interpretation")
    print("  zero_subset_failures_means_all_dimension_sufficient_block_sets_recover=1")
    print("  this_is_a_sum_rank_erasure_strengthening_of_the_top_window_theorem=1")
    print("conclusion=reported_tensor_factor_relative_block_erasure_audit")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Twisted trace-frame audit inside one tensor factor.

Let B/E be one tensor factor, and let C = F_{Q^r} be an intermediate subfield.
Plain trace B -> C is too small to certify full p24 axis rank, but a short
frame of twisted traces

    x |-> (Tr_{B/C}(x), Tr_{B/C}(theta*x), ..., Tr_{B/C}(theta^(k-1)*x))

can be injective on the selected axis span even when k*r is far smaller than
[B:E].  This script tests that phenomenon on small CM rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    PolyE,
    equal_degree_factors,
    poly_degree,
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
from tensor_factor_moore_audit import b_is_zero, b_mul
from tensor_factor_subfield_trace_audit import (
    divisors,
    element_row,
    trace_to_subfield,
)


@dataclass(frozen=True)
class TwistedTargetAudit:
    name: str
    size: int
    raw_rank: int
    ranks_by_subdegree: tuple[tuple[int, tuple[int, ...], int | None], ...]


@dataclass(frozen=True)
class TwistedTraceRow:
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
    proper_subdegrees: tuple[int, ...]
    targets: tuple[TwistedTargetAudit, ...]


def theta_powers(
    count: int,
    factor: PolyE,
    field: ExtensionField,
) -> list[PolyE]:
    theta = [field.zero, field.one]
    powers: list[PolyE] = [[field.one]]
    while len(powers) < count:
        powers.append(b_mul(powers[-1], theta, factor, field))
    return powers


def twisted_trace_rank(
    elements: list[PolyE],
    subdegree: int,
    twists: int,
    factor_degree: int,
    factor: PolyE,
    field: ExtensionField,
) -> int:
    powers = theta_powers(twists, factor, field)
    rows: list[list[FpE]] = []
    for value in elements:
        row: list[FpE] = []
        for power in powers:
            trace_value = trace_to_subfield(
                b_mul(power, value, factor, field),
                subdegree,
                factor_degree,
                factor,
                field,
            )
            row.extend(element_row(trace_value, factor, field))
        rows.append(row)
    return rank_over_extension(rows, field)


def audit_target(
    name: str,
    rows: list[list[FpE]],
    proper_subdegrees: list[int],
    factor_degree: int,
    selected_factor: PolyE,
    field: ExtensionField,
    max_twists: int | None,
) -> TwistedTargetAudit:
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    elements = [value for value in elements if not b_is_zero(value, field)]
    raw_rank = rank_in_factor(rows, selected_factor, field)
    by_subdegree: list[tuple[int, tuple[int, ...], int | None]] = []
    for subdegree in proper_subdegrees:
        relative_degree = factor_degree // subdegree
        limit = relative_degree if max_twists is None else min(max_twists, relative_degree)
        ranks: list[int] = []
        first_full: int | None = None
        for twists in range(1, limit + 1):
            rank = twisted_trace_rank(
                elements,
                subdegree,
                twists,
                factor_degree,
                selected_factor,
                field,
            )
            ranks.append(rank)
            if first_full is None and rank == raw_rank:
                first_full = twists
        by_subdegree.append((subdegree, tuple(ranks), first_full))
    return TwistedTargetAudit(
        name=name,
        size=len(rows),
        raw_rank=raw_rank,
        ranks_by_subdegree=tuple(by_subdegree),
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    max_twists: int | None,
) -> TwistedTraceRow:
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
    proper_subdegrees = [
        subdegree for subdegree in divisors(tensor_factor_degree)
        if subdegree not in (1, tensor_factor_degree)
    ]

    targets: list[TwistedTargetAudit] = []
    axis_rows = character_rows(
        residue_vectors,
        axis_frequency_set(m),
        zeta,
        field,
    )
    targets.append(
        audit_target(
            "axis",
            axis_rows,
            proper_subdegrees,
            tensor_factor_degree,
            selected_factor,
            field,
            max_twists,
        )
    )
    for name, frequencies in frequency_blocks(m):
        targets.append(
            audit_target(
                name,
                character_rows(residue_vectors, frequencies, zeta, field),
                proper_subdegrees,
                tensor_factor_degree,
                selected_factor,
                field,
                max_twists,
            )
        )
    return TwistedTraceRow(
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
        proper_subdegrees=tuple(proper_subdegrees),
        targets=tuple(targets),
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[TwistedTraceRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[TwistedTraceRow] = []
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
                    rows.append(
                        audit_packet(
                            D,
                            q,
                            ell,
                            cycle,
                            m,
                            factor,
                            args.seed,
                            args.max_twists,
                        )
                    )
                    case_had_row = True
                    if len(rows) >= args.max_rows:
                        return rows
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def format_ranks(ranks_by_subdegree: tuple[tuple[int, tuple[int, ...], int | None], ...]) -> str:
    parts = []
    for subdegree, ranks, first_full in ranks_by_subdegree:
        full = "none" if first_full is None else str(first_full)
        parts.append(f"{subdegree}:{list(ranks)} full_at={full}")
    return "; ".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=16)
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
    parser.add_argument("--max-twists", type=int)
    parser.add_argument("--seed", type=int, default=20260604)
    args = parser.parse_args()

    rows = scan(args)
    axis_full_rows = 0
    block_full_rows = 0
    for row in rows:
        for target in row.targets:
            full = any(first_full is not None for _, _, first_full in target.ranks_by_subdegree)
            if target.name == "axis" and full:
                axis_full_rows += 1
            elif target.name != "axis" and full:
                block_full_rows += 1

    print("tensor factor twisted trace-frame audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print("theta_source=X_mod_selected_factor")
    print()
    print("columns: D q ell h m n deg ext factors factor_deg proper_subdegrees")
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factors={row.tensor_factor_count:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"proper={list(row.proper_subdegrees)}"
        )
        for target in row.targets:
            print(
                f"  target={target.name:10s} size={target.size:3d} "
                f"raw_rank={target.raw_rank:3d} "
                f"twisted_trace_ranks=({format_ranks(target.ranks_by_subdegree)})"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  axis_rows_full_by_some_twisted_proper_trace_frame={axis_full_rows}")
    print(f"  nonaxis_target_rows_full_by_some_twisted_proper_trace_frame={block_full_rows}")
    print()
    print("interpretation")
    print("  twisted_trace_frame_rank_full_implies_original_one_factor_rank=1")
    print("  minimal_twists_to_subdegree_r_tests_ceiling(axis_dim/r)_style_certificate=1")
    print("conclusion=reported_tensor_factor_twisted_trace_frame_audit")


if __name__ == "__main__":
    main()

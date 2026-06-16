#!/usr/bin/env python3
"""Subfield membership and trace-rank audit inside one tensor factor.

For a tensor factor B/E of degree d, every subdegree r | d gives a unique
subfield F_{Q^r}.  This script checks, on small CM rows:

* whether selected axis resolvents already lie in proper subfields;
* whether trace maps B -> F_{Q^r} preserve block rank;
* whether joint proper-subfield traces can certify a block.

The point is not to compute p24 directly.  It tests whether the p24 split
5549 = 31 * 179 has a plausible finite-field identity analogue.
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
from tensor_factor_moore_audit import b_add, b_is_zero, b_pow, b_sub


@dataclass(frozen=True)
class TargetAudit:
    name: str
    size: int
    raw_rank: int
    zero_count: int
    fixed_counts: tuple[tuple[int, int], ...]
    trace_ranks: tuple[tuple[int, int], ...]
    joint_proper_trace_rank: int
    joint_all_trace_rank: int


@dataclass(frozen=True)
class SubfieldAuditRow:
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
    subdegrees: tuple[int, ...]
    proper_subdegrees: tuple[int, ...]
    targets: tuple[TargetAudit, ...]


def divisors(value: int) -> list[int]:
    out: list[int] = []
    for candidate in range(1, math.isqrt(value) + 1):
        if value % candidate:
            continue
        out.append(candidate)
        if candidate * candidate != value:
            out.append(value // candidate)
    return sorted(out)


def element_row(value: PolyE, modulus: PolyE, field: ExtensionField) -> list[FpE]:
    degree = poly_degree(modulus, field)
    reduced = poly_mod(value, modulus, field)
    return (reduced + [field.zero] * degree)[:degree]


def element_rank(elements: list[PolyE], modulus: PolyE, field: ExtensionField) -> int:
    return rank_over_extension(
        [element_row(value, modulus, field) for value in elements],
        field,
    )


def trace_to_subfield(
    value: PolyE,
    subdegree: int,
    factor_degree: int,
    modulus: PolyE,
    field: ExtensionField,
) -> PolyE:
    q_power = field.q ** field.degree
    frobenius_step = q_power**subdegree
    total = [field.zero]
    current = poly_mod(value, modulus, field)
    for _ in range(factor_degree // subdegree):
        total = b_add(total, current, modulus, field)
        current = b_pow(current, frobenius_step, modulus, field)
    return poly_mod(total, modulus, field)


def fixed_by_subfield(
    value: PolyE,
    subdegree: int,
    modulus: PolyE,
    field: ExtensionField,
) -> bool:
    q_power = field.q ** field.degree
    conjugate = b_pow(value, q_power**subdegree, modulus, field)
    return b_is_zero(b_sub(conjugate, value, modulus, field), field)


def joint_trace_rank(
    elements: list[PolyE],
    subdegrees: list[int],
    factor_degree: int,
    modulus: PolyE,
    field: ExtensionField,
) -> int:
    if not subdegrees:
        return 0
    rows: list[list[FpE]] = []
    for value in elements:
        row: list[FpE] = []
        for subdegree in subdegrees:
            trace_value = trace_to_subfield(
                value,
                subdegree,
                factor_degree,
                modulus,
                field,
            )
            row.extend(element_row(trace_value, modulus, field))
        rows.append(row)
    return rank_over_extension(rows, field)


def target_audit(
    name: str,
    rows: list[list[FpE]],
    subdegrees: list[int],
    proper_subdegrees: list[int],
    factor_degree: int,
    selected_factor: PolyE,
    field: ExtensionField,
) -> TargetAudit:
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    zero_count = sum(b_is_zero(value, field) for value in elements)
    raw_rank = rank_in_factor(rows, selected_factor, field)
    fixed_counts = tuple(
        (
            subdegree,
            sum(
                fixed_by_subfield(value, subdegree, selected_factor, field)
                for value in elements
            ),
        )
        for subdegree in subdegrees
    )
    trace_ranks = tuple(
        (
            subdegree,
            element_rank(
                [
                    trace_to_subfield(
                        value,
                        subdegree,
                        factor_degree,
                        selected_factor,
                        field,
                    )
                    for value in elements
                ],
                selected_factor,
                field,
            ),
        )
        for subdegree in subdegrees
    )
    return TargetAudit(
        name=name,
        size=len(rows),
        raw_rank=raw_rank,
        zero_count=zero_count,
        fixed_counts=fixed_counts,
        trace_ranks=trace_ranks,
        joint_proper_trace_rank=joint_trace_rank(
            elements,
            proper_subdegrees,
            factor_degree,
            selected_factor,
            field,
        ),
        joint_all_trace_rank=joint_trace_rank(
            elements,
            subdegrees,
            factor_degree,
            selected_factor,
            field,
        ),
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> SubfieldAuditRow:
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
    subdegrees = divisors(tensor_factor_degree)
    proper_subdegrees = [
        subdegree for subdegree in subdegrees
        if subdegree not in (1, tensor_factor_degree)
    ]

    targets: list[TargetAudit] = []
    axis_rows = character_rows(
        residue_vectors,
        axis_frequency_set(m),
        zeta,
        field,
    )
    targets.append(
        target_audit(
            "axis",
            axis_rows,
            subdegrees,
            proper_subdegrees,
            tensor_factor_degree,
            selected_factor,
            field,
        )
    )
    for name, frequencies in frequency_blocks(m):
        rows = character_rows(residue_vectors, frequencies, zeta, field)
        targets.append(
            target_audit(
                name,
                rows,
                subdegrees,
                proper_subdegrees,
                tensor_factor_degree,
                selected_factor,
                field,
            )
        )
    if len(coprime_components(m)) >= 2:
        prefix = [0]
        for component in coprime_components(m)[:-1]:
            step = m // component
            prefix.extend((j * step) % m for j in range(1, component))
        rows = character_rows(residue_vectors, sorted(set(prefix)), zeta, field)
        targets.append(
            target_audit(
                "constant_plus_all_but_last_component",
                rows,
                subdegrees,
                proper_subdegrees,
                tensor_factor_degree,
                selected_factor,
                field,
            )
        )

    return SubfieldAuditRow(
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
        subdegrees=tuple(subdegrees),
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


def scan(args: argparse.Namespace) -> list[SubfieldAuditRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[SubfieldAuditRow] = []
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
                    if (
                        not args.include_prime_tensor_factor_degree
                        and len(divisors(tensor_factor_degree)) <= 2
                    ):
                        continue
                    rows.append(audit_packet(D, q, ell, cycle, m, factor, args.seed))
                    case_had_row = True
                    if len(rows) >= args.max_rows:
                        return rows
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def fmt_pairs(pairs: tuple[tuple[int, int], ...]) -> str:
    return "{" + ", ".join(f"{degree}:{value}" for degree, value in pairs) + "}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=24)
    parser.add_argument("--max-cases", type=int, default=12)
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
    parser.add_argument("--include-prime-tensor-factor-degree", action="store_true")
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    any_fixed_proper = 0
    trace_full_blocks = 0
    joint_full_blocks = 0
    for row in rows:
        for target in row.targets:
            proper_fixed = [
                count for subdegree, count in target.fixed_counts
                if subdegree in row.proper_subdegrees
            ]
            if any(proper_fixed):
                any_fixed_proper += 1
            proper_trace_full = [
                rank for subdegree, rank in target.trace_ranks
                if subdegree in row.proper_subdegrees and rank == target.size
            ]
            if proper_trace_full:
                trace_full_blocks += 1
            if target.joint_proper_trace_rank == target.size:
                joint_full_blocks += 1

    print("tensor factor subfield trace audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_factor_degree={args.max_factor_degree}")
    print(f"max_tensor_factor_degree={args.max_tensor_factor_degree}")
    print()
    if not args.summary_only:
        print("columns: D q ell h m n deg ext factors factor_deg subdegrees proper")
        for row in rows:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"factors={row.tensor_factor_count:2d} "
                f"factor_deg={row.tensor_factor_degree:3d} "
                f"subdegrees={list(row.subdegrees)} "
                f"proper={list(row.proper_subdegrees)}"
            )
            for target in row.targets:
                print(
                    f"  target={target.name:36s} size={target.size:3d} "
                    f"raw_rank={target.raw_rank:3d} zeros={target.zero_count:2d} "
                    f"fixed={fmt_pairs(target.fixed_counts)} "
                    f"trace_rank={fmt_pairs(target.trace_ranks)} "
                    f"joint_proper={target.joint_proper_trace_rank:3d} "
                    f"joint_all={target.joint_all_trace_rank:3d}"
                )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  target_rows_with_any_proper_subfield_membership={any_fixed_proper}")
    print(f"  target_rows_full_by_single_proper_trace={trace_full_blocks}")
    print(f"  target_rows_full_by_joint_proper_traces={joint_full_blocks}")
    print()
    print("interpretation")
    print("  proper_subfield_membership_is_stronger_than_needed_and_usually_false=1")
    print("  full_proper_trace_rank_certifies_original_block_rank=1")
    print("  joint_proper_trace_rank_tests_split_trace_certificates_for_blocks=1")
    print("conclusion=reported_tensor_factor_subfield_trace_audit")


if __name__ == "__main__":
    main()

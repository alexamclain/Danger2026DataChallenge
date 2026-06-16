#!/usr/bin/env python3
"""Fourier form of the top-coefficient certificate.

For quotient fibers J_r and K-character resolvents

    R_s = sum_r zeta^(s*r) J_r,

linearity gives

    Top_k(R_s) = DFT_s( r |-> Top_k(J_r) ).

This script verifies that identity on small tensor-factor rows and measures
whether the output coordinates have sparse frequency support.  Sparse support
would suggest a block-diagonal/Vandermonde proof; dense support means the live
statement is a genuine Fourier anti-annihilator theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
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
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    top_window_coords,
)
from tensor_factor_moore_audit import b_mul
from tensor_factor_subfield_trace_audit import divisors


@dataclass(frozen=True)
class FourierTarget:
    name: str
    size: int
    rank: int


@dataclass(frozen=True)
class FourierAuditRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    subdegree: int
    windows: int
    dft_identity_failures: int
    full_frequency_support_counts: tuple[int, ...]
    axis_frequency_support_counts: tuple[int, ...]
    targets: tuple[FourierTarget, ...]


def vector_zero(length: int, field: ExtensionField) -> list[FpE]:
    return [field.zero for _ in range(length)]


def vector_add(left: list[FpE], right: list[FpE], field: ExtensionField) -> list[FpE]:
    return [field.add(a, b) for a, b in zip(left, right)]


def vector_scalar_mul(scalar: FpE, vector: list[FpE], field: ExtensionField) -> list[FpE]:
    if scalar == field.zero:
        return vector_zero(len(vector), field)
    return [field.mul(scalar, value) for value in vector]


def vector_is_zero(vector: list[FpE], field: ExtensionField) -> bool:
    return all(value == field.zero for value in vector)


def vector_equal(left: list[FpE], right: list[FpE]) -> bool:
    return left == right


def embedded_residue_vector(vector: list[int], field: ExtensionField) -> list[FpE]:
    return [field.embed(value) for value in vector]


def powers_of_zeta(zeta: FpE, m: int, field: ExtensionField) -> list[FpE]:
    powers = [field.one]
    for _ in range(1, m):
        powers.append(field.mul(powers[-1], zeta))
    return powers


def dft_value(
    sequence: list[list[FpE]],
    frequency: int,
    zeta_powers: list[FpE],
    field: ExtensionField,
) -> list[FpE]:
    out = vector_zero(len(sequence[0]), field)
    for r, value in enumerate(sequence):
        out = vector_add(
            out,
            vector_scalar_mul(zeta_powers[(frequency * r) % len(sequence)], value, field),
            field,
        )
    return out


def top_sequence_for_residues(
    residue_vectors: list[list[int]],
    selected_factor,
    field: ExtensionField,
    subdegree: int,
    windows: int,
    tensor_factor_degree: int,
) -> list[list[FpE]]:
    relative_degree = tensor_factor_degree // subdegree
    subfield_basis = normal_subfield_basis(
        subdegree,
        tensor_factor_degree,
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
        tensor_factor_degree,
        selected_factor,
        field,
    )
    out: list[list[FpE]] = []
    for vector in residue_vectors:
        value = poly_mod(row_to_poly(embedded_residue_vector(vector, field), field), selected_factor, field)
        out.append(
            top_window_coords(
                value,
                windows,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                selected_factor,
                field,
            )
        )
    return out


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
    requested_subdegree: int | None,
    windows: int,
) -> list[FourierAuditRow]:
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
    zeta_powers = powers_of_zeta(zeta, m, field)

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

    target_freqs: list[tuple[str, list[int]]] = [("axis", axis_frequency_set(m))]
    for name, frequencies in frequency_blocks(m):
        target_freqs.append((name, frequencies))
        if name != "constant":
            target_freqs.append((f"constant_plus_{name}", sorted(set([0] + frequencies))))

    out: list[FourierAuditRow] = []
    for subdegree in subdegrees:
        if windows > tensor_factor_degree // subdegree:
            continue
        sequence = top_sequence_for_residues(
            residue_vectors,
            selected_factor,
            field,
            subdegree,
            windows,
            tensor_factor_degree,
        )
        all_frequency_values = [
            dft_value(sequence, frequency, zeta_powers, field)
            for frequency in range(m)
        ]
        direct_rows = character_rows(residue_vectors, list(range(m)), zeta, field)
        failures = 0
        relative_degree = tensor_factor_degree // subdegree
        subfield_basis = normal_subfield_basis(
            subdegree,
            tensor_factor_degree,
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
            tensor_factor_degree,
            selected_factor,
            field,
        )
        for frequency, row in enumerate(direct_rows):
            value = poly_mod(row_to_poly(row, field), selected_factor, field)
            direct_top = top_window_coords(
                value,
                windows,
                subdegree,
                relative_degree,
                gprime_theta,
                basis_columns,
                selected_factor,
                field,
            )
            if not vector_equal(direct_top, all_frequency_values[frequency]):
                failures += 1

        coordinate_count = len(sequence[0])
        full_support_counts = []
        axis_support_counts = []
        axis_freqs = set(axis_frequency_set(m))
        for coord in range(coordinate_count):
            full_support_counts.append(
                sum(value[coord] != field.zero for value in all_frequency_values)
            )
            axis_support_counts.append(
                sum(
                    all_frequency_values[frequency][coord] != field.zero
                    for frequency in axis_freqs
                )
            )

        targets = []
        for name, frequencies in target_freqs:
            rows = [all_frequency_values[frequency] for frequency in frequencies]
            targets.append(FourierTarget(name=name, size=len(frequencies), rank=rank_over_extension(rows, field)))
        out.append(
            FourierAuditRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                m=m,
                n=n,
                factor_degree=factor.degree(),
                extension_degree=extension_degree,
                tensor_factor_degree=tensor_factor_degree,
                subdegree=subdegree,
                windows=windows,
                dft_identity_failures=failures,
                full_frequency_support_counts=tuple(full_support_counts),
                axis_frequency_support_counts=tuple(axis_support_counts),
                targets=tuple(targets),
            )
        )
    return out


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[FourierAuditRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[FourierAuditRow] = []
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
                    rows.extend(
                        audit_packet(
                            D,
                            q,
                            ell,
                            cycle,
                            m,
                            factor,
                            args.seed,
                            args.subdegree,
                            args.windows,
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
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int)
    parser.add_argument("--windows", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260604)
    args = parser.parse_args()

    rows = scan(args)
    print("tensor factor top-coefficient Fourier audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"windows={args.windows}")
    print()
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"subdegree={row.subdegree:3d} windows={row.windows:2d} "
            f"dft_failures={row.dft_identity_failures}"
        )
        print(f"  full_frequency_support_counts={list(row.full_frequency_support_counts)}")
        print(f"  axis_frequency_support_counts={list(row.axis_frequency_support_counts)}")
        for target in row.targets:
            print(f"  target={target.name:16s} size={target.size:3d} rank={target.rank:3d}")
    print()
    print("interpretation")
    print("  dft_failures_zero_confirms_top_coefficients_are_DFT_of_quotient_sequence=1")
    print("  dense_frequency_support_argues_against_simple_block_diagonal_factorization=1")
    print("conclusion=reported_tensor_factor_top_coefficient_fourier_audit")


if __name__ == "__main__":
    main()

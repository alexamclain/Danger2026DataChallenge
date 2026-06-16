#!/usr/bin/env python3
"""Relative coefficient profile after multiplying by g'(theta).

The top-coefficient theorem would be easier if the adjusted axis elements
`g'(theta) * R_s(theta)` had triangular or sparse support in the relative
`C`-basis of `B/C`.  This audit checks small rows for that structure.
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
    solve_square,
)
from tensor_factor_moore_audit import b_is_zero, b_mul
from tensor_factor_subfield_trace_audit import divisors, element_row


@dataclass(frozen=True)
class ProfileTarget:
    name: str
    size: int
    coefficient_ranks: tuple[int, ...]
    nonzero_support_sizes: tuple[int, ...]
    full_support_rows: int


@dataclass(frozen=True)
class ProfileRow:
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
    relative_degree: int
    targets: tuple[ProfileTarget, ...]


def relative_coefficients(
    value,
    subdegree: int,
    relative_degree: int,
    gprime_theta,
    basis_columns: list[list[FpE]],
    factor,
    field: ExtensionField,
) -> list[list[FpE]]:
    adjusted = b_mul(value, gprime_theta, factor, field)
    coords = solve_square(
        basis_columns,
        element_row(adjusted, factor, field),
        field,
    )
    return [
        coords[j * subdegree:(j + 1) * subdegree]
        for j in range(relative_degree)
    ]


def coefficient_profile(
    name: str,
    rows: list[list[FpE]],
    subdegree: int,
    relative_degree: int,
    gprime_theta,
    basis_columns: list[list[FpE]],
    selected_factor,
    field: ExtensionField,
) -> ProfileTarget:
    elements = [
        poly_mod(row_to_poly(row, field), selected_factor, field)
        for row in rows
    ]
    coefficient_rows: list[list[list[FpE]]] = [
        relative_coefficients(
            value,
            subdegree,
            relative_degree,
            gprime_theta,
            basis_columns,
            selected_factor,
            field,
        )
        for value in elements
        if not b_is_zero(value, field)
    ]
    coefficient_ranks = []
    for j in range(relative_degree):
        coefficient_ranks.append(
            rank_over_extension([coeffs[j] for coeffs in coefficient_rows], field)
        )
    support_sizes = []
    full_support_rows = 0
    for coeffs in coefficient_rows:
        support = sum(any(value != field.zero for value in coeff) for coeff in coeffs)
        support_sizes.append(support)
        if support == relative_degree:
            full_support_rows += 1
    return ProfileTarget(
        name=name,
        size=len(rows),
        coefficient_ranks=tuple(coefficient_ranks),
        nonzero_support_sizes=tuple(sorted(support_sizes)),
        full_support_rows=full_support_rows,
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
) -> list[ProfileRow]:
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
    subdegrees = [
        subdegree for subdegree in divisors(tensor_factor_degree)
        if subdegree not in (1, tensor_factor_degree)
    ]
    if requested_subdegree is not None:
        subdegrees = [subdegree for subdegree in subdegrees if subdegree == requested_subdegree]

    target_freqs: list[tuple[str, list[int]]] = [
        ("axis", axis_frequency_set(m)),
    ]
    for name, frequencies in frequency_blocks(m):
        target_freqs.append((name, frequencies))
        if name != "constant":
            target_freqs.append((f"constant_plus_{name}", sorted(set([0] + frequencies))))
    components = coprime_components(m)
    if len(components) >= 2:
        prefix = [0]
        for component in components[:-1]:
            step = m // component
            prefix.extend((j * step) % m for j in range(1, component))
            target_freqs.append((f"prefix_through_{component}", sorted(set(prefix))))

    out: list[ProfileRow] = []
    for subdegree in subdegrees:
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
        targets = []
        for name, frequencies in target_freqs:
            targets.append(
                coefficient_profile(
                    name,
                    character_rows(residue_vectors, frequencies, zeta, field),
                    subdegree,
                    relative_degree,
                    gprime_theta,
                    basis_columns,
                    selected_factor,
                    field,
                )
            )
        out.append(
            ProfileRow(
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
                relative_degree=relative_degree,
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


def scan(args: argparse.Namespace) -> list[ProfileRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ProfileRow] = []
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
    parser.add_argument("--seed", type=int, default=20260604)
    args = parser.parse_args()

    rows = scan(args)
    print("tensor factor relative coefficient profile")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print()
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
            f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
            f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
            f"factor_deg={row.tensor_factor_degree:3d} "
            f"subdegree={row.subdegree:3d} relative_degree={row.relative_degree:3d}"
        )
        for target in row.targets:
            print(
                f"  target={target.name:16s} size={target.size:3d} "
                f"coeff_ranks={list(target.coefficient_ranks)} "
                f"support_sizes={list(target.nonzero_support_sizes)} "
                f"full_support_rows={target.full_support_rows}/{target.size}"
            )
    print()
    print("interpretation")
    print("  sparse_or_triangular_support_would_support_a_degree_bound_proof=1")
    print("  full_support_rows_mean_top_coefficient_theorem_remains_a_rank theorem=1")
    print("conclusion=reported_tensor_factor_relative_coefficient_profile")


if __name__ == "__main__":
    main()

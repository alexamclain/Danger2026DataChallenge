#!/usr/bin/env python3
"""CRT marginal-rank audit for top-coefficient Fourier blocks.

For a vector-valued quotient sequence A(r)=Top_k(J_r), the component
frequencies s=t*m/c satisfy

    hat A(t*m/c) = sum_{a mod c} zeta_c^(t*a) M_a,
    M_a = sum_{r == a mod c} A(r).

This script checks the exact rank identities on small tensor-factor rows:

* nontrivial component DFT rank equals affine rank of the c marginals;
* constant-plus-component DFT rank equals ordinary span rank of the marginals.
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
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    rank_over_extension,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from tensor_factor_subfield_trace_audit import divisors
from tensor_factor_top_coefficient_fourier_audit import (
    dft_value,
    discriminants,
    powers_of_zeta,
    primitive_root_of_order,
    top_sequence_for_residues,
    vector_add,
    vector_scalar_mul,
    vector_zero,
)
from k_character_tensor_rank_scan import find_irreducible_modulus


@dataclass(frozen=True)
class ComponentMarginalRank:
    component: int
    marginal_span_rank: int
    marginal_affine_rank: int
    nontrivial_dft_rank: int
    constant_plus_dft_rank: int
    expected_nontrivial_rank: int
    expected_constant_plus_rank: int
    nontrivial_matches_affine: bool
    constant_plus_matches_span: bool


@dataclass(frozen=True)
class CombinedMarginalRank:
    name: str
    size: int
    rank: int
    expected_rank: int


@dataclass(frozen=True)
class MarginalAuditRow:
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
    coordinate_count: int
    components: tuple[ComponentMarginalRank, ...]
    combined: tuple[CombinedMarginalRank, ...]


def vector_sub(left, right, field: ExtensionField):
    return [field.sub(a, b) for a, b in zip(left, right)]


def component_marginals(sequence, component: int, field: ExtensionField):
    marginals = [vector_zero(len(sequence[0]), field) for _ in range(component)]
    for r, value in enumerate(sequence):
        residue = r % component
        marginals[residue] = vector_add(marginals[residue], value, field)
    return marginals


def vector_sum(sequence, field: ExtensionField):
    out = vector_zero(len(sequence[0]), field)
    for value in sequence:
        out = vector_add(out, value, field)
    return out


def combined_marginal_rank(
    sequence,
    selected_components: tuple[int, ...],
    include_constant: bool,
    field: ExtensionField,
) -> CombinedMarginalRank:
    rows = []
    if include_constant:
        rows.append(vector_sum(sequence, field))
    for component in selected_components:
        marginals = component_marginals(sequence, component, field)
        rows.extend(vector_sub(value, marginals[0], field) for value in marginals[1:])
    size = len(rows)
    name_parts = []
    if include_constant:
        name_parts.append("constant")
    name_parts.extend(str(component) for component in selected_components)
    name = "plus".join(name_parts) if name_parts else "empty"
    return CombinedMarginalRank(
        name=name,
        size=size,
        rank=rank_over_extension(rows, field),
        expected_rank=min(size, len(sequence[0])),
    )


def combined_targets(sequence, field: ExtensionField, m: int) -> tuple[CombinedMarginalRank, ...]:
    components = tuple(coprime_components(m))
    out: list[CombinedMarginalRank] = []
    seen_names: set[str] = set()
    def add(target: CombinedMarginalRank) -> None:
        if target.name in seen_names:
            return
        seen_names.add(target.name)
        out.append(target)

    for component in components:
        add(combined_marginal_rank(sequence, (component,), False, field))
        add(combined_marginal_rank(sequence, (component,), True, field))
    if len(components) >= 2:
        for i, left in enumerate(components):
            for right in components[i + 1:]:
                add(combined_marginal_rank(sequence, (left, right), True, field))
    add(combined_marginal_rank(sequence, components, True, field))
    return tuple(out)


def audit_component(
    sequence,
    component: int,
    m: int,
    zeta_powers,
    field: ExtensionField,
) -> ComponentMarginalRank:
    step = m // component
    frequencies = [(t * step) % m for t in range(1, component)]
    dft_rows = [dft_value(sequence, frequency, zeta_powers, field) for frequency in frequencies]
    constant_row = dft_value(sequence, 0, zeta_powers, field)

    marginals = component_marginals(sequence, component, field)
    differences = [vector_sub(value, marginals[0], field) for value in marginals[1:]]
    span_rank = rank_over_extension(marginals, field)
    affine_rank = rank_over_extension(differences, field)
    nontrivial_rank = rank_over_extension(dft_rows, field)
    constant_plus_rank = rank_over_extension([constant_row] + dft_rows, field)

    return ComponentMarginalRank(
        component=component,
        marginal_span_rank=span_rank,
        marginal_affine_rank=affine_rank,
        nontrivial_dft_rank=nontrivial_rank,
        constant_plus_dft_rank=constant_plus_rank,
        expected_nontrivial_rank=min(component - 1, len(sequence[0])),
        expected_constant_plus_rank=min(component, len(sequence[0])),
        nontrivial_matches_affine=(nontrivial_rank == affine_rank),
        constant_plus_matches_span=(constant_plus_rank == span_rank),
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
    windows: int,
) -> list[MarginalAuditRow]:
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

    out: list[MarginalAuditRow] = []
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
        components = tuple(
            audit_component(sequence, component, m, zeta_powers, field)
            for component in coprime_components(m)
        )
        combined = combined_targets(sequence, field, m)
        out.append(
            MarginalAuditRow(
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
                coordinate_count=len(sequence[0]),
                components=components,
                combined=combined,
            )
        )
    return out


def scan(args: argparse.Namespace) -> list[MarginalAuditRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[MarginalAuditRow] = []
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
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    print("tensor factor CRT marginal-rank audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_cases={args.max_cases}")
    print(f"windows={args.windows}")
    print()
    total_mismatches = 0
    total_components = 0
    capacity_full_seen = 0
    enough_coordinates_for_all_marginals = 0
    combined_targets = 0
    combined_capacity_targets = 0
    combined_capacity_failures = 0
    component_capacity_failures = 0
    displayed_failures: list[tuple[MarginalAuditRow, CombinedMarginalRank]] = []
    for row in rows:
        if not args.summary_only:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"factor_deg={row.tensor_factor_degree:3d} "
                f"subdegree={row.subdegree:3d} windows={row.windows:2d} "
                f"coords={row.coordinate_count:3d}"
            )
        for component in row.components:
            total_components += 1
            total_mismatches += int(not component.nontrivial_matches_affine)
            total_mismatches += int(not component.constant_plus_matches_span)
            if (
                component.marginal_affine_rank == component.expected_nontrivial_rank
                and component.marginal_span_rank == component.expected_constant_plus_rank
            ):
                capacity_full_seen += 1
            if row.coordinate_count >= component.component:
                enough_coordinates_for_all_marginals += 1
                if (
                    component.marginal_span_rank < component.expected_constant_plus_rank
                    or component.marginal_affine_rank < component.expected_nontrivial_rank
                ):
                    component_capacity_failures += 1
            if not args.summary_only:
                print(
                    f"  c={component.component:3d} "
                    f"marg_span={component.marginal_span_rank:3d}/"
                    f"{component.expected_constant_plus_rank:3d} "
                    f"marg_affine={component.marginal_affine_rank:3d}/"
                    f"{component.expected_nontrivial_rank:3d} "
                    f"dft_nontriv={component.nontrivial_dft_rank:3d} "
                    f"dft_const_plus={component.constant_plus_dft_rank:3d} "
                    f"matches=({int(component.nontrivial_matches_affine)},"
                    f"{int(component.constant_plus_matches_span)})"
                )
        for target in row.combined:
            combined_targets += 1
            if row.coordinate_count >= target.size:
                combined_capacity_targets += 1
                if target.rank < target.size:
                    combined_capacity_failures += 1
                    if len(displayed_failures) < 12:
                        displayed_failures.append((row, target))
            if not args.summary_only:
                print(
                    f"  combined={target.name:20s} "
                    f"size={target.size:3d} rank={target.rank:3d}/"
                    f"{target.expected_rank:3d}"
                )
    print()
    print("interpretation")
    print(f"rank_identity_mismatches={total_mismatches}")
    print(f"component_blocks_tested={total_components}")
    print(f"capacity_full_component_marginals_seen={capacity_full_seen}")
    print(f"blocks_with_enough_coordinates_for_all_marginals={enough_coordinates_for_all_marginals}")
    print(f"component_capacity_failures={component_capacity_failures}")
    print(f"combined_targets_tested={combined_targets}")
    print(f"combined_capacity_targets={combined_capacity_targets}")
    print(f"combined_capacity_failures={combined_capacity_failures}")
    if displayed_failures:
        print("displayed_combined_capacity_failures")
        for row, target in displayed_failures:
            print(
                f"  D={row.D} q={row.q} m={row.m} n={row.n} "
                f"subdegree={row.subdegree} windows={row.windows} "
                f"target={target.name} rank={target.rank}/{target.size}"
            )
    print("conclusion=reported_tensor_factor_crt_marginal_rank_audit")


if __name__ == "__main__":
    main()

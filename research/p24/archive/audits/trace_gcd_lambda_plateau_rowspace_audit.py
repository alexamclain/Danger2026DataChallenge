#!/usr/bin/env python3
"""Audit the lambda-level rowspace bridge from leading erasure to plateau.

The current dual-sparse route would close if every representative
leading-erasure bad lambda also made the centered profile word constant on
the selected plateau.  In linear algebra terms:

    ker(B_leading) subset ker(C_plateau)

or equivalently:

    rowspace(C_plateau) subset rowspace(B_leading).

Here B_leading is the selected trace-GCD Lang coordinate map, and C_plateau is
the quotient map f_lambda(s)-f_lambda(0) for the selected cyclic plateau.

This script checks that relation on small actual-CM rows and reports whether
the evidence is nonvacuous.  If B_leading already has full rank, there are no
bad lambdas; rowspace containment is then automatic in a d-dimensional source.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from hermitian_mixed_left_subfield_normality_audit import (
    centered_right_profile_for_left_orbit,
    trace_to_base,
)
from hermitian_mixed_subspace_polynomial_toy import base_value_or_none
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import section_fiber_polynomials


SEED = 20260605


@dataclass(frozen=True)
class RowspaceCase:
    label: str
    D: int
    q: int
    m: int
    left: int
    right: int


@dataclass(frozen=True)
class RowspaceResult:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    left_orbit: tuple[int, ...]
    omitted: int
    right_orbit_count: int
    source_dim: int
    plateau_rank: int
    leading_rank: int
    combined_rank: int
    bad_dim: int
    bad_not_plateau_rank: int
    rowspace_contains_plateau: bool
    containment_vacuous_full_leading_rank: bool


def hermitian_packet_factor(n: int, q: int) -> sp.Poly:
    for factor in packet_factors(n, q):
        if factor.degree() % 2:
            continue
        if pow(q, factor.degree() // 2, n) == n - 1:
            return factor
    raise ValueError("no Hermitian packet factor")


def base_trace(value: FpE, left_len: int, field: ExtensionField) -> int:
    base = base_value_or_none(trace_to_base(value, left_len, field), field)
    if base is None:
        raise ValueError("trace did not land in the base field")
    return base


def transpose_columns(columns: list[list[int]]) -> list[list[int]]:
    if not columns:
        return []
    return [
        [columns[col][row] for col in range(len(columns))]
        for row in range(len(columns[0]))
    ]


def plateau_matrix(
    lambda_basis: list[FpE],
    centered_profile: list[FpE],
    left_len: int,
    plateau_len: int,
    q: int,
    field: ExtensionField,
) -> list[list[int]]:
    columns: list[list[int]] = []
    for lam in lambda_basis:
        word = [
            base_trace(field.mul(lam, value), left_len, field)
            for value in centered_profile
        ]
        columns.append(
            [(word[s] - word[0]) % q for s in range(1, plateau_len)]
        )
    return transpose_columns(columns)


def leading_matrix(
    lambda_basis: list[FpE],
    dft_matrix: list[list[FpE]],
    left_orbit: list[int],
    right_orbits: list[list[int]],
    omitted: int,
    left: int,
    right: int,
    source_dim: int,
    q: int,
    field: ExtensionField,
) -> list[list[int]] | None:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    kept = [orbit for index, orbit in enumerate(right_orbits) if index != omitted]
    coords: list[FpE] = []
    for orbit in kept:
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in orbit
        ]
        coords.extend(
            matrix_vector_mul(
                lang_inverse_for_orbit(q, len(orbit), field, SEED),
                seed_vector,
                field,
            )
        )
    if len(coords) < source_dim:
        return None
    coords = coords[:source_dim]
    columns: list[list[int]] = []
    for lam in lambda_basis:
        columns.append(
            [
                base_trace(field.mul(lam, coord), source_dim, field)
                for coord in coords
            ]
        )
    return transpose_columns(columns)


def audit_case(case: RowspaceCase) -> list[RowspaceResult]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(case.D)
    h = int(pari.poldegree(hilbert))
    roots = [int(root) for root in pari.polrootsmod(hilbert, case.q)]
    ell, cycle = find_full_cycle_prime(roots, case.D, case.q)
    _ = ell
    n = h // case.m
    factor = hermitian_packet_factor(n, case.q)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, case.q, case.m, "complement")
    ]
    marginal = double_marginal(
        kernel_matrix(residues, factor, case.q),
        case.left,
        case.right,
        case.q,
    )

    extension_degree = int(sp.n_order(case.q % case.m, case.m))
    modulus = find_irreducible_modulus(case.q, extension_degree, SEED)
    field = ExtensionField(case.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, case.m, SEED)
    powers = zeta_powers(zeta, case.m, field)
    dft_matrix = dft_double_marginal(
        marginal, case.left, case.right, powers, case.m, field
    )
    right_orbits = q_orbits(case.right, case.q)

    out: list[RowspaceResult] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        if any(gcd(source_dim, len(orbit)) != 1 for orbit in right_orbits):
            continue
        lambda_basis = subfield_power_basis(
            case.q, source_dim, field, SEED + 157
        )
        centered_profile = centered_right_profile_for_left_orbit(
            marginal,
            case.left,
            case.right,
            left_orbit,
            case.m,
            powers,
            case.q,
            field,
        )
        c_matrix = plateau_matrix(
            lambda_basis,
            centered_profile,
            source_dim,
            case.left,
            case.q,
            field,
        )
        c_rank = rank_mod_q(c_matrix, case.q)
        for omitted in range(len(right_orbits)):
            b_matrix = leading_matrix(
                lambda_basis,
                dft_matrix,
                left_orbit,
                right_orbits,
                omitted,
                case.left,
                case.right,
                source_dim,
                case.q,
                field,
            )
            if b_matrix is None:
                continue
            b_rank = rank_mod_q(b_matrix, case.q)
            combined_rank = rank_mod_q(b_matrix + c_matrix, case.q)
            bad_dim = source_dim - b_rank
            bad_not_plateau_rank = combined_rank - b_rank
            out.append(
                RowspaceResult(
                    label=case.label,
                    D=case.D,
                    q=case.q,
                    h=h,
                    m=case.m,
                    n=n,
                    factor_degree=factor.degree(),
                    left=case.left,
                    right=case.right,
                    left_orbit=tuple(left_orbit),
                    omitted=omitted,
                    right_orbit_count=len(right_orbits),
                    source_dim=source_dim,
                    plateau_rank=c_rank,
                    leading_rank=b_rank,
                    combined_rank=combined_rank,
                    bad_dim=bad_dim,
                    bad_not_plateau_rank=bad_not_plateau_rank,
                    rowspace_contains_plateau=(combined_rank == b_rank),
                    containment_vacuous_full_leading_rank=(b_rank == source_dim),
                )
            )
    return out


def main() -> None:
    cases = [
        RowspaceCase("pinned", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_a", -4319, 4463, 28, 4, 7),
        RowspaceCase("same_geometry_b", -4319, 4643, 28, 4, 7),
        RowspaceCase("same_geometry_c", -4511, 4547, 28, 4, 7),
    ]
    rows = [row for case in cases for row in audit_case(case)]
    print("Trace-GCD lambda plateau rowspace audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "source_dim plateau_rank leading_rank combined_rank bad_dim "
        "bad_not_plateau_rank contains vacuous_full"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} right_orbit_count={row.right_orbit_count} "
            f"source_dim={row.source_dim} plateau_rank={row.plateau_rank} "
            f"leading_rank={row.leading_rank} combined_rank={row.combined_rank} "
            f"bad_dim={row.bad_dim} "
            f"bad_not_plateau_rank={row.bad_not_plateau_rank} "
            f"contains={int(row.rowspace_contains_plateau)} "
            f"vacuous_full={int(row.containment_vacuous_full_leading_rank)}"
        )
    failures = [row for row in rows if not row.rowspace_contains_plateau]
    nonvacuous = [
        row for row in rows
        if row.rowspace_contains_plateau
        and not row.containment_vacuous_full_leading_rank
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  rowspace_containment_failures={len(failures)}")
    print(f"  nonvacuous_containments={len(nonvacuous)}")
    print(
        "  vacuous_full_leading_rank="
        f"{sum(int(row.containment_vacuous_full_leading_rank) for row in rows)}/"
        f"{len(rows)}"
    )
    print(
        "  max_bad_not_plateau_rank="
        f"{max((row.bad_not_plateau_rank for row in rows), default=0)}"
    )
    print("interpretation")
    print("  rowspace_containment_is_bad_lambda_implies_plateau=1")
    print("  full_leading_rank_rows_support_punit_but_do_not_prove_bridge_identity=1")
    print("  nonvacuous_containment_would_be_the_needed_schur_bridge=1")
    print("conclusion=reported_trace_gcd_lambda_plateau_rowspace_audit")


if __name__ == "__main__":
    main()

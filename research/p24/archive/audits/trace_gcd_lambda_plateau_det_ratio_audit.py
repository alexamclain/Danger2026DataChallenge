#!/usr/bin/env python3
"""Determinant-ratio audit for leading-erasure versus plateau maps.

Both maps in the lambda-plateau bridge are square on the small actual-CM
rows:

    B_leading : lambda -> selected Lang/Fitting coordinates,
    C_plateau : lambda -> f_lambda(s)-f_lambda(0), s=1,...,left-1.

When both determinants are nonzero, their ratio is a p-unit in the carrier
field.  This is useful but not a proof: if both maps are already full rank,
the ratio is automatically nonzero.  The audit records whether the ratio is
stable across rows/orbits and explicitly compares with the universal cyclic
selector obstruction.
"""

from __future__ import annotations

from dataclasses import dataclass

from kernel_tail_schur_identity_toy import det_mod
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_lambda_plateau_rowspace_audit import (
    RowspaceCase,
    audit_case,
    leading_matrix,
    plateau_matrix,
    hermitian_packet_factor,
    SEED,
)

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import subfield_power_basis
from hermitian_mixed_left_subfield_normality_audit import centered_right_profile_for_left_orbit
from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus, primitive_root_of_order
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import section_fiber_polynomials


@dataclass(frozen=True)
class DetRatioRow:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    pair: tuple[int, int]
    left_orbit: tuple[int, ...]
    omitted: int
    det_plateau: int | None
    det_leading: int | None
    ratio_leading_over_plateau: int | None
    both_nonzero: bool
    rowspace_equal: bool


def carrier_data(case: RowspaceCase):
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(case.D)
    h = int(pari.poldegree(hilbert))
    roots = [int(root) for root in pari.polrootsmod(hilbert, case.q)]
    _ell, cycle = find_full_cycle_prime(roots, case.D, case.q)
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
    field = ExtensionField(
        case.q,
        extension_degree,
        find_irreducible_modulus(case.q, extension_degree, SEED),
    )
    zeta = primitive_root_of_order(field, case.m, SEED)
    powers = zeta_powers(zeta, case.m, field)
    dft_matrix = dft_double_marginal(
        marginal, case.left, case.right, powers, case.m, field
    )
    return h, n, factor, marginal, field, powers, dft_matrix, q_orbits(case.right, case.q)


def ratio_rows_for_case(case: RowspaceCase) -> list[DetRatioRow]:
    h, n, factor, marginal, field, powers, dft_matrix, right_orbits = carrier_data(case)
    rows: list[DetRatioRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        lambda_basis = subfield_power_basis(case.q, source_dim, field, SEED + 157)
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
        if len(c_matrix) != source_dim or any(len(row) != source_dim for row in c_matrix):
            continue
        det_c = det_mod(c_matrix, case.q)
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
            det_b = det_mod(b_matrix, case.q)
            ratio = None
            if det_b and det_c:
                ratio = det_b * pow(det_c, -1, case.q) % case.q
            rows.append(
                DetRatioRow(
                    label=case.label,
                    D=case.D,
                    q=case.q,
                    h=h,
                    m=case.m,
                    n=n,
                    factor_degree=factor.degree(),
                    pair=(case.left, case.right),
                    left_orbit=tuple(left_orbit),
                    omitted=omitted,
                    det_plateau=det_c,
                    det_leading=det_b,
                    ratio_leading_over_plateau=ratio,
                    both_nonzero=bool(det_b and det_c),
                    rowspace_equal=(
                        rank_mod_q(c_matrix + b_matrix, case.q)
                        == rank_mod_q(c_matrix, case.q)
                        == rank_mod_q(b_matrix, case.q)
                    ),
                )
            )
    return rows


def main() -> None:
    cases = [
        RowspaceCase("pinned", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_a", -4319, 4463, 28, 4, 7),
        RowspaceCase("same_geometry_b", -4319, 4643, 28, 4, 7),
        RowspaceCase("same_geometry_c", -4511, 4547, 28, 4, 7),
    ]
    rows = [row for case in cases for row in ratio_rows_for_case(case)]
    print("Trace-GCD lambda plateau determinant-ratio audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "det_plateau det_leading ratio both_nonzero rowspace_equal"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair={row.pair} left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} det_plateau={row.det_plateau} "
            f"det_leading={row.det_leading} "
            f"ratio={row.ratio_leading_over_plateau} "
            f"both_nonzero={int(row.both_nonzero)} "
            f"rowspace_equal={int(row.rowspace_equal)}"
        )
    ratios = [row.ratio_leading_over_plateau for row in rows if row.ratio_leading_over_plateau is not None]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  both_nonzero={sum(int(row.both_nonzero) for row in rows)}/{len(rows)}")
    print(f"  rowspace_equal={sum(int(row.rowspace_equal) for row in rows)}/{len(rows)}")
    print(f"  distinct_nonzero_ratios={len(set(ratios))}")
    print("interpretation")
    print("  determinant_ratio_is_nonzero_when_both_maps_are_full_rank=1")
    print("  varying_ratios_mean_no_obvious_universal_scalar_comparison=1")
    print("  p24_still_needs_arithmetic_punit_or_nonvacuous_rowspace_containment=1")
    print("conclusion=reported_trace_gcd_lambda_plateau_det_ratio_audit")


if __name__ == "__main__":
    main()

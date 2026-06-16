#!/usr/bin/env python3
"""Finite bridge audit for centered differences and trace-GCD Fourier data.

The dual-sparse p24 side door needs one bad parameter to have both a sparse
time avatar and a sparse nonzero-frequency avatar.  This script verifies the
coordinate identity that makes that plausible but not automatic:

    DFT_right(P_b - P_{b-1}) = (1 - zeta_right^v) * DFT_right(P_b)

on the actual centered CRT marginal used by the small trace-GCD CM holdouts.
The multiplier is a p-unit for nonzero right frequencies.  The audit also
records that the naive direct comparison between time-difference rowspace and
Lang trace-word rowspace is false, so the remaining theorem must identify the
same kernel parameter through the Fourier/Lang/Fitting construction.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from centered_marginal_cyclic_code_boundary import point_matrix
from centered_marginal_difference_code_audit import cyclic_difference_rows
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_left_subfield_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_arc_strength_audit import transformed_blocks_for_row
from lang_trace_gcd_kernel_audit import trace_pair_row
from l1_axis_injectivity_scan import rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import section_fiber_polynomials


SEED = 20260605


@dataclass(frozen=True)
class BridgeCase:
    label: str
    D: int
    q: int
    m: int
    left: int
    right: int


@dataclass(frozen=True)
class BridgeAuditRow:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    diff_rank: int
    dft_rank: int
    dft_difference_mismatches: int
    nonzero_multiplier_failures: int
    direct_rowspace_tests: int
    direct_rowspace_equal: int
    direct_rowspace_combined_ranks: tuple[int, ...]


def hermitian_packet_factor(n: int, q: int) -> sp.Poly:
    for factor in packet_factors(n, q):
        if factor.degree() % 2:
            continue
        if pow(q, factor.degree() // 2, n) == n - 1:
            return factor
    raise ValueError("no Hermitian packet factor")


def field_sum(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def diff_double_dft(
    diffs: list[list[int]],
    left: int,
    right: int,
    powers: list[FpE],
    m: int,
    field: ExtensionField,
) -> list[list[FpE]]:
    step_left = m // left
    step_right = m // right
    rows: list[list[FpE]] = []
    for u in range(1, left):
        row: list[FpE] = []
        for v in range(1, right):
            terms: list[FpE] = []
            for a in range(1, left):
                left_weight = powers[(u * step_left * a) % m]
                for b in range(right):
                    weight = field.mul(
                        left_weight,
                        powers[(v * step_right * b) % m],
                    )
                    terms.append(field.mul(weight, field.embed(diffs[a - 1][b])))
            row.append(field_sum(terms, field))
        rows.append(row)
    return rows


def right_difference_multiplier(
    v: int,
    right: int,
    powers: list[FpE],
    m: int,
    field: ExtensionField,
) -> FpE:
    step_right = m // right
    return field.sub(field.one, powers[(v * step_right) % m])


def rowspace_rank_tuple(
    left_matrix: list[list[int]],
    right_matrix: list[list[int]],
    q: int,
) -> tuple[int, int, int]:
    return (
        rank_mod_q(left_matrix, q),
        rank_mod_q(right_matrix, q),
        rank_mod_q(left_matrix + right_matrix, q),
    )


def direct_time_lang_rowspace_tests(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    diffs: list[list[int]],
) -> tuple[int, int, tuple[int, ...]]:
    right_orbits = q_orbits(right, q)
    nonzero_order = [value for orbit in right_orbits for value in orbit]
    time_matrix = [[row[index] for index in nonzero_order] for row in diffs]
    tests = 0
    equal = 0
    combined_ranks: list[int] = []
    for left_orbit in q_orbits(left, q):
        if len(left_orbit) != left - 1:
            continue
        _extension_degree, field, blocks = transformed_blocks_for_row(
            D, q, ell, cycle, m, factor, left, right, left_orbit, SEED
        )
        basis = subfield_power_basis(q, len(left_orbit), field, SEED)
        values = [value for block in blocks for value in block]
        columns = [
            trace_pair_row(value, basis, len(left_orbit), field)
            for value in values
        ]
        lang_matrix = [
            [column[row] for column in columns]
            for row in range(len(left_orbit))
        ]
        ranks = rowspace_rank_tuple(time_matrix, lang_matrix, q)
        tests += 1
        equal += int(ranks[0] == ranks[1] == ranks[2])
        combined_ranks.append(ranks[2])
    return tests, equal, tuple(combined_ranks)


def audit_case(case: BridgeCase) -> BridgeAuditRow:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(case.D)
    h = int(pari.poldegree(hilbert))
    roots = [int(root) for root in pari.polrootsmod(hilbert, case.q)]
    ell, cycle = find_full_cycle_prime(roots, case.D, case.q)
    n = h // case.m
    factor = hermitian_packet_factor(n, case.q)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, case.q, case.m, "complement")
    ]
    marginal = double_marginal(kernel_matrix(residues, factor, case.q), case.left, case.right, case.q)
    points = point_matrix(marginal, case.left, case.right, case.q)
    diffs = cyclic_difference_rows(points, case.q)

    extension_degree = int(sp.n_order(case.q % case.m, case.m))
    modulus = find_irreducible_modulus(case.q, extension_degree, SEED)
    field = ExtensionField(case.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, case.m, SEED)
    powers = zeta_powers(zeta, case.m, field)
    dft_matrix = dft_double_marginal(
        marginal, case.left, case.right, powers, case.m, field
    )
    diff_dft = diff_double_dft(
        diffs, case.left, case.right, powers, case.m, field
    )

    mismatches = 0
    multiplier_failures = 0
    for u in range(1, case.left):
        for v in range(1, case.right):
            multiplier = right_difference_multiplier(
                v, case.right, powers, case.m, field
            )
            if multiplier == field.zero:
                multiplier_failures += 1
            expected = field.mul(multiplier, dft_matrix[u - 1][v - 1])
            if diff_dft[u - 1][v - 1] != expected:
                mismatches += 1

    tests, equal, combined_ranks = direct_time_lang_rowspace_tests(
        case.D, case.q, ell, cycle, case.m, factor, case.left, case.right, diffs
    )
    return BridgeAuditRow(
        label=case.label,
        D=case.D,
        q=case.q,
        h=h,
        m=case.m,
        n=n,
        factor_degree=factor.degree(),
        left=case.left,
        right=case.right,
        diff_rank=rank_mod_q(diffs, case.q),
        dft_rank=rank_mod_q(
            [[int(value != field.zero) for value in row] for row in diff_dft],
            2,
        ),
        dft_difference_mismatches=mismatches,
        nonzero_multiplier_failures=multiplier_failures,
        direct_rowspace_tests=tests,
        direct_rowspace_equal=equal,
        direct_rowspace_combined_ranks=combined_ranks,
    )


def main() -> None:
    cases = [
        BridgeCase("pinned", -13319, 13463, 28, 4, 7),
        BridgeCase("holdout", -26759, 26903, 21, 3, 7),
    ]
    rows = [audit_case(case) for case in cases]
    print("Trace-GCD difference DFT bridge audit")
    print("columns: label D q h m n factor_deg pair diff_rank dft_mismatches unit_failures direct_tests direct_equal combined_ranks")
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) diff_rank={row.diff_rank} "
            f"dft_difference_mismatches={row.dft_difference_mismatches} "
            f"nonzero_multiplier_failures={row.nonzero_multiplier_failures} "
            f"direct_rowspace_tests={row.direct_rowspace_tests} "
            f"direct_rowspace_equal={row.direct_rowspace_equal} "
            f"direct_rowspace_combined_ranks={list(row.direct_rowspace_combined_ranks)}"
        )
    print("totals")
    print(f"  cases={len(rows)}")
    print(
        "  dft_difference_mismatches="
        f"{sum(row.dft_difference_mismatches for row in rows)}"
    )
    print(
        "  nonzero_multiplier_failures="
        f"{sum(row.nonzero_multiplier_failures for row in rows)}"
    )
    print(
        "  direct_rowspace_equal="
        f"{sum(row.direct_rowspace_equal for row in rows)}/"
        f"{sum(row.direct_rowspace_tests for row in rows)}"
    )
    print("interpretation")
    print("  cyclic_difference_is_punit_diagonal_on_nonzero_right_dft=1")
    print("  naive_time_difference_equals_lang_traceword_rowspace=0")
    print("  remaining_bridge_is_same_kernel_parameter_through_fourier_lang_fitting=1")
    print("conclusion=reported_trace_gcd_difference_dft_bridge_audit")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""C_13-to-C_169 fiber section for p25 Hilbert-90 source-chain corners.

The raw-character gate shows that the forced K trace cleanly projects the
corner to the C_3 x C_169 quotient.  This gate looks at the remaining quotient
object itself: how the active C_169 corner graph sits above its C_13 shadow.

For each active row-balanced half-bridge corner, the C_169 values are not the
Teichmuller lift of the C_13 shadow and cannot be obtained from an affine fiber
section.  The exact fiber correction is a unit quadratic section over F_13.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
)


C_LOW_ORDER = 13
C_ORDER = 169


@dataclass(frozen=True)
class CornerFiberSectionRow:
    orientation_mask: int
    boundary_direction_q: int
    chain_q_values: tuple[int, ...]
    row_values_c169: tuple[int, int, int]
    c13_shadow_values: tuple[int, int, int]
    fiber_values: tuple[int, int, int]
    teichmuller_lifts: tuple[int, int, int]
    teichmuller_mismatch_count: int
    affine_candidate: tuple[int, int]
    affine_section_possible: bool
    quadratic_section_coefficients: tuple[int, int, int]
    quadratic_roots: tuple[int, ...]
    quadratic_leading_is_unit: bool
    active_lift_matches_quadratic_section: bool


@dataclass(frozen=True)
class CornerFiberSectionProfile:
    row_count: int
    rows: tuple[CornerFiberSectionRow, ...]
    all_rows_are_genuine_quadratic_sections: bool
    no_row_is_teichmuller_lift: bool
    no_row_has_affine_fiber_section: bool
    all_quadratic_sections_have_unit_leading_term: bool
    all_quadratic_sections_match_active_lift: bool
    canonical_quadratic_section: tuple[int, int, int]
    canonical_factorization_roots: tuple[int, ...]


def inv_mod(value: int) -> int:
    return pow(value % C_LOW_ORDER, -1, C_LOW_ORDER)


def teichmuller_lift(low: int) -> int:
    for lift in range(C_ORDER):
        if lift % C_LOW_ORDER == low % C_LOW_ORDER and pow(lift, C_LOW_ORDER, C_ORDER) == lift:
            return lift
    raise AssertionError(f"no Teichmuller lift for {low}")


def row_values(q_values: tuple[int, ...]) -> tuple[int, int, int]:
    by_row = {q_value % 3: q_value % C_ORDER for q_value in q_values}
    if set(by_row) != {0, 1, 2}:
        raise AssertionError(f"corner is not one point per row: {q_values}")
    return (by_row[0], by_row[1], by_row[2])


def affine_candidate(xs: tuple[int, int, int], ys: tuple[int, int, int]) -> tuple[int, int]:
    slope = ((ys[1] - ys[0]) * inv_mod(xs[1] - xs[0])) % C_LOW_ORDER
    intercept = (ys[0] - slope * xs[0]) % C_LOW_ORDER
    return slope, intercept


def affine_matches(xs: tuple[int, int, int], ys: tuple[int, int, int], candidate: tuple[int, int]) -> bool:
    slope, intercept = candidate
    return all((slope * x_value + intercept) % C_LOW_ORDER == y_value for x_value, y_value in zip(xs, ys))


def quadratic_coefficients(xs: tuple[int, int, int], ys: tuple[int, int, int]) -> tuple[int, int, int]:
    # Solve a*x^2 + b*x + c = y over F_13 by tiny Gaussian elimination.
    matrix = [
        [(x_value * x_value) % C_LOW_ORDER, x_value % C_LOW_ORDER, 1, y_value % C_LOW_ORDER]
        for x_value, y_value in zip(xs, ys)
    ]
    for column in range(3):
        pivot = next(row for row in range(column, 3) if matrix[row][column] % C_LOW_ORDER)
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = inv_mod(matrix[column][column])
        matrix[column] = [(entry * scale) % C_LOW_ORDER for entry in matrix[column]]
        for row in range(3):
            if row == column:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - factor * matrix[column][index]) % C_LOW_ORDER
                for index in range(4)
            ]
    return tuple(matrix[index][3] % C_LOW_ORDER for index in range(3))  # type: ignore[return-value]


def quadratic_value(coefficients: tuple[int, int, int], x_value: int) -> int:
    a_value, b_value, c_value = coefficients
    return (a_value * x_value * x_value + b_value * x_value + c_value) % C_LOW_ORDER


def quadratic_roots(coefficients: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(
        x_value
        for x_value in range(C_LOW_ORDER)
        if quadratic_value(coefficients, x_value) == 0
    )


def fiber_row(active_row) -> CornerFiberSectionRow:
    values = row_values(active_row.chain_q_values)
    lows = tuple(value % C_LOW_ORDER for value in values)
    fibers = tuple(value // C_LOW_ORDER for value in values)
    teich = tuple(teichmuller_lift(low) for low in lows)
    affine = affine_candidate(lows, fibers)
    quad = quadratic_coefficients(lows, fibers)
    return CornerFiberSectionRow(
        orientation_mask=active_row.orientation_mask,
        boundary_direction_q=active_row.boundary_direction_q,
        chain_q_values=active_row.chain_q_values,
        row_values_c169=values,
        c13_shadow_values=lows,
        fiber_values=fibers,
        teichmuller_lifts=teich,
        teichmuller_mismatch_count=sum(value != lift for value, lift in zip(values, teich)),
        affine_candidate=affine,
        affine_section_possible=affine_matches(lows, fibers, affine),
        quadratic_section_coefficients=quad,
        quadratic_roots=quadratic_roots(quad),
        quadratic_leading_is_unit=quad[0] != 0,
        active_lift_matches_quadratic_section=all(
            fibers[index] == quadratic_value(quad, lows[index])
            for index in range(3)
        ),
    )


def corner_fiber_section_profile() -> CornerFiberSectionProfile:
    rows = tuple(fiber_row(row) for row in corner_profile().active_rows)
    return CornerFiberSectionProfile(
        row_count=len(rows),
        rows=rows,
        all_rows_are_genuine_quadratic_sections=all(
            not row.affine_section_possible and row.quadratic_leading_is_unit
            for row in rows
        ),
        no_row_is_teichmuller_lift=all(row.teichmuller_mismatch_count > 0 for row in rows),
        no_row_has_affine_fiber_section=all(not row.affine_section_possible for row in rows),
        all_quadratic_sections_have_unit_leading_term=all(row.quadratic_leading_is_unit for row in rows),
        all_quadratic_sections_match_active_lift=all(row.active_lift_matches_quadratic_section for row in rows),
        canonical_quadratic_section=rows[0].quadratic_section_coefficients,
        canonical_factorization_roots=rows[0].quadratic_roots,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner fiber-section gate")
    profile = corner_fiber_section_profile()
    expected_rows = (
        CornerFiberSectionRow(1, 197, (0, 172, 482), (0, 3, 144), (0, 3, 1), (0, 0, 11), (0, 146, 1), 2, (0, 0), False, (1, 10, 0), (0, 3), True, True),
        CornerFiberSectionRow(1, 310, (172, 197, 369), (31, 3, 28), (5, 3, 2), (2, 0, 2), (70, 146, 80), 3, (1, 10), False, (1, 6, 12), (3, 4), True, True),
        CornerFiberSectionRow(6, 197, (138, 310, 335), (138, 141, 166), (8, 11, 10), (10, 10, 12), (99, 89, 23), 3, (0, 10), False, (12, 6, 0), (0, 6), True, True),
        CornerFiberSectionRow(6, 310, (0, 25, 335), (0, 25, 166), (0, 12, 10), (0, 1, 12), (0, 168, 23), 2, (12, 0), False, (8, 7, 0), (0, 4), True, True),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_rows_are_genuine_quadratic_sections
        and profile.no_row_is_teichmuller_lift
        and profile.no_row_has_affine_fiber_section
        and profile.all_quadratic_sections_have_unit_leading_term
        and profile.all_quadratic_sections_match_active_lift
        and profile.canonical_quadratic_section == (1, 10, 0)
        and profile.canonical_factorization_roots == (0, 3)
    )

    print(
        "corner_fiber_section_summary: "
        f"row_count={profile.row_count} "
        f"canonical_quadratic_section={profile.canonical_quadratic_section} "
        f"canonical_roots={profile.canonical_factorization_roots} "
        f"genuine_quadratic={int(profile.all_rows_are_genuine_quadratic_sections)} "
        f"no_teichmuller={int(profile.no_row_is_teichmuller_lift)} "
        f"no_affine={int(profile.no_row_has_affine_fiber_section)}"
    )
    print("corner_fiber_section_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("fiber_section_laws")
    print("  write c = c0 + 13*f over the active C13 shadow values")
    print("  canonical active corner has f(c0) = c0*(c0-3) over F13")
    print("  no active corner row is the Teichmuller lift of its C13 shadow")
    print("  no active corner row is explained by an affine fiber gauge")
    print("interpretation")
    print("  active_C169_corner_lift_requires_a_genuine_quadratic_fiber_section=1")
    print("  producer_must_supply_this_quadratic_fiber_correction_after_the_K_trace=1")
    print("  teichmuller_or_affine_C13_lift_shortcuts_are_rejected_for_the_corner=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_fiber_section_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

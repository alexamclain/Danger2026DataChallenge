#!/usr/bin/env python3
"""Row-polynomial normal form for the p25 Hilbert-90 corner.

The fiber-covariance gate reduces the active corner lift to one canonical
quadratic section over the C_13 shadow:

    c = c0 + 13*f,    f(c0) = c0*(c0-3).

This gate rewrites that same object in the actual C_3 source-row coordinate.
For the canonical active corner, the C_13 shadow and the C_13 fiber are both
quadratic row polynomials:

    c0(r) = 4*r^2 - r,      f(r) = r*(1-r),      r = 0,1,2.

Thus the canonical C_169 graph is a single row-quadratic lift, not merely an
interpolated function of three C_13 shadow values.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_gate import (
    FiberCovarianceRow,
    fiber_covariance_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
    C_ORDER,
    quadratic_value,
)


RowPoly = tuple[int, int, int]


@dataclass(frozen=True)
class RowPolynomialRow:
    row: int
    c13_shadow: int
    fiber: int
    c169_value: int
    c13_from_row_poly: int
    fiber_from_row_poly: int
    c169_from_row_poly: int
    fiber_from_shadow_poly: int
    row_polynomial_matches: bool
    shadow_polynomial_matches: bool


@dataclass(frozen=True)
class RowPolynomialProfile:
    c13_row_polynomial: RowPoly
    fiber_row_polynomial: RowPoly
    fiber_shadow_polynomial: RowPoly
    row_count: int
    rows: tuple[RowPolynomialRow, ...]
    row_values_c169: tuple[int, int, int]
    q_values: tuple[int, int, int]
    c13_row_roots: tuple[int, ...]
    fiber_row_roots: tuple[int, ...]
    fiber_shadow_roots: tuple[int, ...]
    all_rows_match_row_polynomial: bool
    all_rows_match_shadow_polynomial: bool
    c13_row_polynomial_is_genuine_quadratic: bool
    fiber_row_polynomial_is_genuine_quadratic: bool
    row_graph_is_source_graph: bool
    covariance_rows_transport_this_row_polynomial: bool
    no_carry_transport_failure_count: int


def eval_poly(poly: RowPoly, value: int) -> int:
    a_value, b_value, c_value = poly
    return (a_value * value * value + b_value * value + c_value) % C_LOW_ORDER


def roots(poly: RowPoly) -> tuple[int, ...]:
    return tuple(value for value in range(C_LOW_ORDER) if eval_poly(poly, value) == 0)


def q_from_row_c(row: int, c_value: int) -> int:
    return (c_value + C_ORDER * ((row - c_value) % 3)) % (3 * C_ORDER)


def row_polynomial_profile() -> RowPolynomialProfile:
    covariance = fiber_covariance_profile()
    canonical = covariance.rows[0]
    c13_row_poly = (4, 12, 0)
    fiber_row_poly = (12, 1, 0)
    fiber_shadow_poly = covariance.canonical_quadratic_section
    rows: list[RowPolynomialRow] = []
    c_by_row = {
        q_value % 3: q_value % C_ORDER
        for q_value in canonical.target_chain_q_values
    }
    for row in range(3):
        c_value = c_by_row[row]
        c13_shadow = c_value % C_LOW_ORDER
        fiber = c_value // C_LOW_ORDER
        c13_from_row = eval_poly(c13_row_poly, row)
        fiber_from_row = eval_poly(fiber_row_poly, row)
        c169_from_row = c13_from_row + C_LOW_ORDER * fiber_from_row
        fiber_from_shadow = quadratic_value(fiber_shadow_poly, c13_shadow)
        rows.append(
            RowPolynomialRow(
                row=row,
                c13_shadow=c13_shadow,
                fiber=fiber,
                c169_value=c_value,
                c13_from_row_poly=c13_from_row,
                fiber_from_row_poly=fiber_from_row,
                c169_from_row_poly=c169_from_row,
                fiber_from_shadow_poly=fiber_from_shadow,
                row_polynomial_matches=c169_from_row == c_value,
                shadow_polynomial_matches=fiber_from_shadow == fiber,
            )
        )
    q_values = tuple(q_from_row_c(row, rows[row].c169_value) for row in range(3))
    return RowPolynomialProfile(
        c13_row_polynomial=c13_row_poly,
        fiber_row_polynomial=fiber_row_poly,
        fiber_shadow_polynomial=fiber_shadow_poly,
        row_count=len(rows),
        rows=tuple(rows),
        row_values_c169=tuple(row.c169_value for row in rows),
        q_values=q_values,  # type: ignore[arg-type]
        c13_row_roots=roots(c13_row_poly),
        fiber_row_roots=roots(fiber_row_poly),
        fiber_shadow_roots=roots(fiber_shadow_poly),
        all_rows_match_row_polynomial=all(row.row_polynomial_matches for row in rows),
        all_rows_match_shadow_polynomial=all(row.shadow_polynomial_matches for row in rows),
        c13_row_polynomial_is_genuine_quadratic=c13_row_poly[0] != 0,
        fiber_row_polynomial_is_genuine_quadratic=fiber_row_poly[0] != 0,
        row_graph_is_source_graph=q_values == canonical.target_chain_q_values,
        covariance_rows_transport_this_row_polynomial=all(
            isinstance(row, FiberCovarianceRow) and row.transformed_matches_target
            for row in covariance.rows
        ),
        no_carry_transport_failure_count=sum(not row.no_carry_matches_target for row in covariance.rows),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner row-polynomial gate")
    profile = row_polynomial_profile()
    expected_rows = (
        RowPolynomialRow(0, 0, 0, 0, 0, 0, 0, 0, True, True),
        RowPolynomialRow(1, 3, 0, 3, 3, 0, 3, 0, True, True),
        RowPolynomialRow(2, 1, 11, 144, 1, 11, 144, 11, True, True),
    )
    row_ok = (
        profile.c13_row_polynomial == (4, 12, 0)
        and profile.fiber_row_polynomial == (12, 1, 0)
        and profile.fiber_shadow_polynomial == (1, 10, 0)
        and profile.row_count == 3
        and profile.rows == expected_rows
        and profile.row_values_c169 == (0, 3, 144)
        and profile.q_values == (0, 172, 482)
        and profile.c13_row_roots == (0, 10)
        and profile.fiber_row_roots == (0, 1)
        and profile.fiber_shadow_roots == (0, 3)
        and profile.all_rows_match_row_polynomial
        and profile.all_rows_match_shadow_polynomial
        and profile.c13_row_polynomial_is_genuine_quadratic
        and profile.fiber_row_polynomial_is_genuine_quadratic
        and profile.row_graph_is_source_graph
        and profile.covariance_rows_transport_this_row_polynomial
        and profile.no_carry_transport_failure_count == 2
    )

    print(
        "corner_row_polynomial_summary: "
        f"c13_row_poly={profile.c13_row_polynomial} "
        f"fiber_row_poly={profile.fiber_row_polynomial} "
        f"fiber_shadow_poly={profile.fiber_shadow_polynomial} "
        f"row_values_c169={profile.row_values_c169} "
        f"q_values={profile.q_values} "
        f"no_carry_transport_failure_count={profile.no_carry_transport_failure_count}"
    )
    print(
        "roots: "
        f"c13_row_roots={profile.c13_row_roots} "
        f"fiber_row_roots={profile.fiber_row_roots} "
        f"fiber_shadow_roots={profile.fiber_shadow_roots}"
    )
    print("corner_row_polynomial_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("row_polynomial_laws")
    print("  canonical C13 shadow is c0(r)=4*r^2-r on source rows r=0,1,2")
    print("  canonical fiber is f(r)=r*(1-r) on source rows r=0,1,2")
    print("  equivalently f(c0)=c0*(c0-3) on the selected shadow values")
    print("interpretation")
    print("  canonical_corner_is_a_single_quadratic_row_graph_in_C169=1")
    print("  producer_target_can_be_stated_as_row_quadratic_plus_K_trace=1")
    print("  nonsplit_carry_still_needed_to_transport_the_row_polynomial_to_all_active_corners=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

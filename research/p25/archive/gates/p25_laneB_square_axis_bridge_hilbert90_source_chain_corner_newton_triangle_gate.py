#!/usr/bin/env python3
"""Newton-triangle normal form for p25 Hilbert-90 source-chain corners.

The row-polynomial gate writes the canonical active corner as a quadratic graph
in the source-row coordinate.  This gate ties that quadratic back to the
primitive D-coordinate corner:

    D-row points: 0, 1, 1 - 122

Equivalently, the row-edge cycle is the fixed triangle with primitive-D edge
steps 1, 121, and -122.  The quadratic fiber correction is therefore the
Newton curvature of the half-bridge corner, not a free interpolation choice.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
    q_from_d_residue,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_gate import (
    row_polynomial_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Triple = tuple[int, int, int]


EXPECTED_Q_EDGE_TRIANGLE = (25, 172, 310)
EXPECTED_C169_EDGE_TRIANGLE = (3, 25, 141)
EXPECTED_D_EDGE_TRIANGLE = (1, 121, 385)


@dataclass(frozen=True)
class RowNewtonTriangleRow:
    orientation_mask: int
    boundary_direction_q: int
    q_by_source_row: Triple
    c169_by_source_row: Triple
    d_by_source_row: Triple
    q_quadratic: Triple
    c169_quadratic: Triple
    d_quadratic: Triple
    q_cycle_edges: Triple
    c169_cycle_edges: Triple
    d_cycle_edges: Triple
    q_second_difference: int
    c169_second_difference: int
    d_second_difference: int
    edge_triangle_matches: bool


@dataclass(frozen=True)
class RowNewtonTriangleProfile:
    row_count: int
    rows: tuple[RowNewtonTriangleRow, ...]
    canonical_q_newton: Triple
    canonical_c169_newton: Triple
    canonical_d_newton: Triple
    d_edge_q_images: tuple[tuple[int, int], ...]
    canonical_row_polynomial_matches_corner: bool
    canonical_q_edges_are_unit_and_opposite_half: bool
    canonical_d_edges_are_unit_and_negative_half: bool
    all_rows_have_q_edge_triangle: bool
    all_rows_have_c169_edge_triangle: bool
    all_rows_have_d_edge_triangle: bool
    all_rows_are_the_same_newton_triangle: bool


def by_source_row(q_values: tuple[int, ...]) -> Triple:
    out: list[int] = []
    for row in range(3):
        hits = tuple(q_value for q_value in q_values if q_value % 3 == row)
        if len(hits) != 1:
            raise AssertionError(f"expected one q-value in source row {row}, got {hits}")
        out.append(hits[0])
    return tuple(out)  # type: ignore[return-value]


def quadratic_coefficients(values: Triple, modulus: int) -> Triple:
    inv2 = pow(2, -1, modulus)
    second = (values[2] - 2 * values[1] + values[0]) % modulus
    a_value = (second * inv2) % modulus
    b_value = (values[1] - values[0] - a_value) % modulus
    c_value = values[0] % modulus
    return a_value, b_value, c_value


def cycle_edges(values: Triple, modulus: int) -> Triple:
    return tuple((values[(index + 1) % 3] - values[index]) % modulus for index in range(3))  # type: ignore[return-value]


def second_difference(values: Triple, modulus: int) -> int:
    return (values[2] - 2 * values[1] + values[0]) % modulus


def newton_coefficients(values: Triple, modulus: int) -> Triple:
    return values[0] % modulus, (values[1] - values[0]) % modulus, second_difference(values, modulus)


def triangle_row(active_row) -> RowNewtonTriangleRow:
    q_values = by_source_row(active_row.chain_q_values)
    c_values = tuple(q_value % C_ORDER for q_value in q_values)
    d_values = tuple(d_residue_from_q(q_value) for q_value in q_values)
    q_edges = cycle_edges(q_values, QUOTIENT_ORDER)
    c_edges = cycle_edges(c_values, C_ORDER)
    d_edges = cycle_edges(d_values, QUOTIENT_ORDER)
    edge_triangle_matches = (
        tuple(sorted(q_edges)) == EXPECTED_Q_EDGE_TRIANGLE
        and tuple(sorted(c_edges)) == EXPECTED_C169_EDGE_TRIANGLE
        and tuple(sorted(d_edges)) == EXPECTED_D_EDGE_TRIANGLE
    )
    return RowNewtonTriangleRow(
        orientation_mask=active_row.orientation_mask,
        boundary_direction_q=active_row.boundary_direction_q,
        q_by_source_row=q_values,
        c169_by_source_row=c_values,  # type: ignore[arg-type]
        d_by_source_row=d_values,  # type: ignore[arg-type]
        q_quadratic=quadratic_coefficients(q_values, QUOTIENT_ORDER),
        c169_quadratic=quadratic_coefficients(c_values, C_ORDER),  # type: ignore[arg-type]
        d_quadratic=quadratic_coefficients(d_values, QUOTIENT_ORDER),  # type: ignore[arg-type]
        q_cycle_edges=q_edges,
        c169_cycle_edges=c_edges,
        d_cycle_edges=d_edges,
        q_second_difference=second_difference(q_values, QUOTIENT_ORDER),
        c169_second_difference=second_difference(c_values, C_ORDER),  # type: ignore[arg-type]
        d_second_difference=second_difference(d_values, QUOTIENT_ORDER),  # type: ignore[arg-type]
        edge_triangle_matches=edge_triangle_matches,
    )


def row_newton_triangle_profile() -> RowNewtonTriangleProfile:
    corners = corner_profile()
    rows = tuple(triangle_row(active) for active in corners.active_rows)
    canonical = rows[0]
    row_polynomial = row_polynomial_profile()
    d_edge_q_images = tuple((d_edge, q_from_d_residue(d_edge)) for d_edge in EXPECTED_D_EDGE_TRIANGLE)
    return RowNewtonTriangleProfile(
        row_count=len(rows),
        rows=rows,
        canonical_q_newton=newton_coefficients(canonical.q_by_source_row, QUOTIENT_ORDER),
        canonical_c169_newton=newton_coefficients(canonical.c169_by_source_row, C_ORDER),
        canonical_d_newton=newton_coefficients(canonical.d_by_source_row, QUOTIENT_ORDER),
        d_edge_q_images=d_edge_q_images,
        canonical_row_polynomial_matches_corner=(
            canonical.q_by_source_row == row_polynomial.q_values
            and canonical.c169_by_source_row == row_polynomial.row_values_c169
        ),
        canonical_q_edges_are_unit_and_opposite_half=(
            canonical.q_cycle_edges[:2] == (corners.unit_q, corners.opposite_half_q)
            and canonical.q_cycle_edges[2] == q_from_d_residue((corners.half_bridge_d - corners.unit_d) % QUOTIENT_ORDER)
        ),
        canonical_d_edges_are_unit_and_negative_half=(
            canonical.d_cycle_edges[:2] == (corners.unit_d, (-corners.half_bridge_d) % QUOTIENT_ORDER)
            and canonical.d_cycle_edges[2] == (corners.half_bridge_d - corners.unit_d) % QUOTIENT_ORDER
        ),
        all_rows_have_q_edge_triangle=all(tuple(sorted(row.q_cycle_edges)) == EXPECTED_Q_EDGE_TRIANGLE for row in rows),
        all_rows_have_c169_edge_triangle=all(
            tuple(sorted(row.c169_cycle_edges)) == EXPECTED_C169_EDGE_TRIANGLE for row in rows
        ),
        all_rows_have_d_edge_triangle=all(tuple(sorted(row.d_cycle_edges)) == EXPECTED_D_EDGE_TRIANGLE for row in rows),
        all_rows_are_the_same_newton_triangle=all(row.edge_triangle_matches for row in rows),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner Newton-triangle gate")
    profile = row_newton_triangle_profile()
    expected_rows = (
        RowNewtonTriangleRow(1, 197, (0, 172, 482), (0, 3, 144), (0, 1, 386), (69, 103, 0), (69, 103, 0), (192, 316, 0), (172, 310, 25), (3, 141, 25), (1, 385, 121), 138, 138, 384, True),
        RowNewtonTriangleRow(1, 310, (369, 172, 197), (31, 3, 28), (123, 1, 122), (111, 199, 369), (111, 30, 31), (375, 10, 123), (310, 25, 172), (141, 25, 3), (385, 121, 1), 222, 53, 243, True),
        RowNewtonTriangleRow(6, 197, (138, 310, 335), (138, 141, 166), (384, 385, 506), (180, 499, 138), (11, 161, 138), (60, 448, 384), (172, 25, 310), (3, 25, 141), (1, 121, 385), 360, 22, 120, True),
        RowNewtonTriangleRow(6, 310, (0, 25, 335), (0, 25, 166), (0, 121, 506), (396, 136, 0), (58, 136, 0), (132, 496, 0), (25, 310, 172), (25, 141, 3), (121, 385, 1), 285, 116, 264, True),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.canonical_q_newton == (0, 172, 138)
        and profile.canonical_c169_newton == (0, 3, 138)
        and profile.canonical_d_newton == (0, 1, 384)
        and profile.d_edge_q_images == ((1, 172), (121, 25), (385, 310))
        and profile.canonical_row_polynomial_matches_corner
        and profile.canonical_q_edges_are_unit_and_opposite_half
        and profile.canonical_d_edges_are_unit_and_negative_half
        and profile.all_rows_have_q_edge_triangle
        and profile.all_rows_have_c169_edge_triangle
        and profile.all_rows_have_d_edge_triangle
        and profile.all_rows_are_the_same_newton_triangle
    )

    print(
        "corner_newton_triangle_summary: "
        f"row_count={profile.row_count} "
        f"canonical_q_newton={profile.canonical_q_newton} "
        f"canonical_c169_newton={profile.canonical_c169_newton} "
        f"canonical_d_newton={profile.canonical_d_newton} "
        f"d_edge_q_images={profile.d_edge_q_images}"
    )
    print("corner_newton_triangle_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("newton_triangle_laws")
    print("  canonical q row graph is q(r)=69*r^2+103*r mod 507")
    print("  canonical primitive-D row graph is d(r)=192*r^2+316*r mod 507")
    print("  its D-edge cycle is unit, half-minus-unit, negative-half: 1,121,385")
    print("  all four active corners have the same D-edge triangle up to row rotation")
    print("interpretation")
    print("  row_quadratic_is_the_newton_curvature_of_the_half_bridge_corner=1")
    print("  producer_target_is_a_fixed_source_row_triangle_plus_the_raw_K_trace=1")
    print("  fiber_correction_is_not_an_independent_interpolation_parameter=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

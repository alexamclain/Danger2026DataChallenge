#!/usr/bin/env python3
"""Slope-one chord law for the p25 Hilbert-90 source corner.

The tangent-descent gate splits the recorded C_169 step into C_13 shadow plus
fiber tangent coordinates.  This gate ties that local tangent back to the
quadratic fiber section itself.

On every active row-quadratic corner, the directed half-bridge pair 197/310 is
exactly the pair of secants of the active C_13 fiber section with slope one:

    (fiber_to - fiber_from) / (shadow_to - shadow_from) = 1 in F_13.

The other four one-cancellation triangle edges are controls.  Thus a producer
can target a slope-one chord of the quadratic section first, then use the
tangent-descent law to orient it.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
    corner_fiber_section_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_tangent_descent_gate import (
    tangent_descent_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate import (
    TriangleDirectedEdge,
    triangle_edge_profile,
)


LowFiber = tuple[int, int]


@dataclass(frozen=True)
class SlopeOneChordEdge:
    direction_q: int
    from_row: int
    to_row: int
    from_low_fiber: LowFiber
    to_low_fiber: LowFiber
    low_step_mod13: int
    fiber_step_mod13: int
    secant_slope_mod13: int
    signed_secant_slope: int
    branch_role: str
    is_half_bridge_edge: bool
    is_slope_one: bool


@dataclass(frozen=True)
class SlopeOneChordRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    quadratic_section_coefficients: tuple[int, int, int]
    slope_one_direction_qs: tuple[int, ...]
    half_bridge_direction_qs: tuple[int, ...]
    recorded_direction_is_slope_one: bool
    opposite_direction_is_slope_one: bool
    recorded_weighted_tangent: tuple[int, int]
    recorded_oriented_by_negative_tangent: bool
    edges: tuple[SlopeOneChordEdge, ...]


@dataclass(frozen=True)
class SlopeOneChordProfile:
    row_count: int
    rows: tuple[SlopeOneChordRow, ...]
    all_slope_one_edges_are_half_bridge_edges: bool
    all_half_bridge_edges_are_slope_one_edges: bool
    all_recorded_edges_are_slope_one: bool
    all_opposite_edges_are_slope_one: bool
    all_recorded_edges_are_oriented_by_negative_tangent: bool


def signed_mod(value: int, modulus: int = C_LOW_ORDER) -> int:
    value %= modulus
    return value if value <= modulus // 2 else value - modulus


def low_fiber_by_source_row(fiber_row) -> dict[int, LowFiber]:
    return {
        row: (c_value % C_LOW_ORDER, c_value // C_LOW_ORDER)
        for row, c_value in enumerate(fiber_row.row_values_c169)
    }


def slope_edge(edge: TriangleDirectedEdge, pairs_by_row: dict[int, LowFiber]) -> SlopeOneChordEdge:
    from_pair = pairs_by_row[edge.from_row]
    to_pair = pairs_by_row[edge.to_row]
    low_step = (to_pair[0] - from_pair[0]) % C_LOW_ORDER
    fiber_step = (to_pair[1] - from_pair[1]) % C_LOW_ORDER
    if low_step == 0:
        raise AssertionError("active corner has repeated C_13 shadow value")
    slope = (fiber_step * pow(low_step, -1, C_LOW_ORDER)) % C_LOW_ORDER
    return SlopeOneChordEdge(
        direction_q=edge.direction_q,
        from_row=edge.from_row,
        to_row=edge.to_row,
        from_low_fiber=from_pair,
        to_low_fiber=to_pair,
        low_step_mod13=low_step,
        fiber_step_mod13=fiber_step,
        secant_slope_mod13=slope,
        signed_secant_slope=signed_mod(slope),
        branch_role=edge.branch_role,
        is_half_bridge_edge=edge.is_half_bridge_edge,
        is_slope_one=slope == 1,
    )


def slope_one_chord_profile() -> SlopeOneChordProfile:
    fiber_rows = corner_fiber_section_profile().rows
    triangle_rows = triangle_edge_profile().rows
    tangent_rows = tangent_descent_profile().rows
    rows: list[SlopeOneChordRow] = []
    for fiber_row, triangle_row, tangent_row in zip(fiber_rows, triangle_rows, tangent_rows):
        pairs_by_row = low_fiber_by_source_row(fiber_row)
        edges = tuple(slope_edge(edge, pairs_by_row) for edge in triangle_row.directed_edges)
        slope_one_qs = tuple(edge.direction_q for edge in edges if edge.is_slope_one)
        rows.append(
            SlopeOneChordRow(
                orientation_mask=triangle_row.orientation_mask,
                recorded_direction_q=triangle_row.recorded_direction_q,
                chain_coefficient=triangle_row.chain_coefficient,
                quadratic_section_coefficients=fiber_row.quadratic_section_coefficients,
                slope_one_direction_qs=slope_one_qs,
                half_bridge_direction_qs=triangle_row.half_bridge_edge_directions_q,
                recorded_direction_is_slope_one=any(
                    edge.direction_q == triangle_row.recorded_direction_q and edge.is_slope_one
                    for edge in edges
                ),
                opposite_direction_is_slope_one=any(
                    edge.direction_q == triangle_row.opposite_direction_q and edge.is_slope_one
                    for edge in edges
                ),
                recorded_weighted_tangent=tangent_row.coefficient_weighted_recorded_tangent,
                recorded_oriented_by_negative_tangent=(
                    tangent_row.coefficient_weighted_recorded_tangent == (-2, -2)
                ),
                edges=edges,
            )
        )
    rows_tuple = tuple(rows)
    return SlopeOneChordProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_slope_one_edges_are_half_bridge_edges=all(
            row.slope_one_direction_qs == row.half_bridge_direction_qs
            for row in rows_tuple
        ),
        all_half_bridge_edges_are_slope_one_edges=all(
            row.half_bridge_direction_qs == (197, 310)
            for row in rows_tuple
        ),
        all_recorded_edges_are_slope_one=all(row.recorded_direction_is_slope_one for row in rows_tuple),
        all_opposite_edges_are_slope_one=all(row.opposite_direction_is_slope_one for row in rows_tuple),
        all_recorded_edges_are_oriented_by_negative_tangent=all(
            row.recorded_oriented_by_negative_tangent
            for row in rows_tuple
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner slope-one chord gate")
    profile = slope_one_chord_profile()
    expected_rows = (
        SlopeOneChordRow(
            1, 197, -1, (1, 10, 0), (197, 310), (197, 310), True, True, (-2, -2), True,
            (
                SlopeOneChordEdge(25, 2, 0, (1, 11), (0, 0), 12, 2, 11, -2, "other_one_cancellation", False, False),
                SlopeOneChordEdge(172, 0, 1, (0, 0), (3, 0), 3, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(197, 2, 1, (1, 11), (3, 0), 2, 2, 1, 1, "recorded", True, True),
                SlopeOneChordEdge(310, 1, 2, (3, 0), (1, 11), 11, 11, 1, 1, "opposite_short", True, True),
                SlopeOneChordEdge(335, 1, 0, (3, 0), (0, 0), 10, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(482, 0, 2, (0, 0), (1, 11), 1, 11, 11, -2, "other_one_cancellation", False, False),
            ),
        ),
        SlopeOneChordRow(
            1, 310, 1, (1, 6, 12), (197, 310), (197, 310), True, True, (-2, -2), True,
            (
                SlopeOneChordEdge(25, 1, 2, (3, 0), (2, 2), 12, 2, 11, -2, "other_one_cancellation", False, False),
                SlopeOneChordEdge(172, 2, 0, (2, 2), (5, 2), 3, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(197, 1, 0, (3, 0), (5, 2), 2, 2, 1, 1, "opposite_short", True, True),
                SlopeOneChordEdge(310, 0, 1, (5, 2), (3, 0), 11, 11, 1, 1, "recorded", True, True),
                SlopeOneChordEdge(335, 0, 2, (5, 2), (2, 2), 10, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(482, 2, 1, (2, 2), (3, 0), 1, 11, 11, -2, "other_one_cancellation", False, False),
            ),
        ),
        SlopeOneChordRow(
            6, 197, -1, (12, 6, 0), (197, 310), (197, 310), True, True, (-2, -2), True,
            (
                SlopeOneChordEdge(25, 1, 2, (11, 10), (10, 12), 12, 2, 11, -2, "other_one_cancellation", False, False),
                SlopeOneChordEdge(172, 0, 1, (8, 10), (11, 10), 3, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(197, 0, 2, (8, 10), (10, 12), 2, 2, 1, 1, "recorded", True, True),
                SlopeOneChordEdge(310, 2, 0, (10, 12), (8, 10), 11, 11, 1, 1, "opposite_short", True, True),
                SlopeOneChordEdge(335, 1, 0, (11, 10), (8, 10), 10, 0, 0, 0, "other_one_cancellation", False, False),
                SlopeOneChordEdge(482, 2, 1, (10, 12), (11, 10), 1, 11, 11, -2, "other_one_cancellation", False, False),
            ),
        ),
        SlopeOneChordRow(
            6, 310, 1, (8, 7, 0), (197, 310), (197, 310), True, True, (-2, -2), True,
            (
                SlopeOneChordEdge(25, 0, 1, (0, 0), (12, 1), 12, 1, 12, -1, "other_one_cancellation", False, False),
                SlopeOneChordEdge(172, 2, 0, (10, 12), (0, 0), 3, 1, 9, -4, "other_one_cancellation", False, False),
                SlopeOneChordEdge(197, 2, 1, (10, 12), (12, 1), 2, 2, 1, 1, "opposite_short", True, True),
                SlopeOneChordEdge(310, 1, 2, (12, 1), (10, 12), 11, 11, 1, 1, "recorded", True, True),
                SlopeOneChordEdge(335, 0, 2, (0, 0), (10, 12), 10, 12, 9, -4, "other_one_cancellation", False, False),
                SlopeOneChordEdge(482, 1, 0, (12, 1), (0, 0), 1, 12, 12, -1, "other_one_cancellation", False, False),
            ),
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_slope_one_edges_are_half_bridge_edges
        and profile.all_half_bridge_edges_are_slope_one_edges
        and profile.all_recorded_edges_are_slope_one
        and profile.all_opposite_edges_are_slope_one
        and profile.all_recorded_edges_are_oriented_by_negative_tangent
    )

    print(
        "corner_slope_one_chord_summary: "
        f"slope_one_qs={tuple(row.slope_one_direction_qs for row in profile.rows)} "
        f"half_bridge_qs={tuple(row.half_bridge_direction_qs for row in profile.rows)} "
        f"recorded_weighted_tangents={tuple(row.recorded_weighted_tangent for row in profile.rows)}"
    )
    print("corner_slope_one_chord_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("slope_one_chord_laws")
    print("  directed q=197 and q=310 are exactly the slope-one secants of the active quadratic fiber section")
    print("  the other four one-cancellation triangle edges have non-one secant slopes")
    print("  tangent descent orients this slope-one chord by coefficient-weighted tangent (-2,-2)")
    print("interpretation")
    print("  half_bridge_edge_can_be_selected_as_a_slope_one_chord_before_orientation=1")
    print("  producer_can_target_the_quadratic_section_secant_condition_before_full_C169_edge_scan=1")
    print("  non_half_bridge_triangle_edges_are_explicit_secant_slope_controls=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

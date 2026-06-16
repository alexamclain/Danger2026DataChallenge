#!/usr/bin/env python3
"""Cancellation-line law for the p25 Hilbert-90 source corner.

The slope-line factor gate shows that the half-bridge endpoints are the roots
of a quadratic fiber section after subtracting a slope-one line.  This gate
removes the remaining apparent choice of line.

The slope-one line is forced by the Hilbert-90 cancellation vertex.  If the
cancellation point is c = c0 + 13*f, then the line is:

    f = c0 + (f - c0).

The other half-bridge endpoint is the coefficient-selected neighbor

    (c0, f) + 2*coefficient*(1, 1)

and the recorded edge points from that neighbor back to the cancellation
vertex.  After multiplying by the chain coefficient, the recorded tangent is
always (-2, -2).
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
    C_ORDER,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    corner_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_gate import (
    slope_line_factor_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_gate import (
    slope_one_chord_profile,
)


LowFiber = tuple[int, int]


@dataclass(frozen=True)
class CancellationLineRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    cancellation_vertex_q: int
    cancellation_low_fiber: LowFiber
    slope_one_line_intercept: int
    intercept_from_cancellation: int
    coefficient_neighbor_low_fiber: LowFiber
    residual_roots: tuple[int, ...]
    roots_from_cancellation_and_neighbor: tuple[int, ...]
    recorded_edge_from_low_fiber: LowFiber
    recorded_edge_to_low_fiber: LowFiber
    recorded_edge_points_to_cancellation: bool
    recorded_signed_tangent: LowFiber
    coefficient_weighted_recorded_tangent: LowFiber
    line_is_forced_by_cancellation_vertex: bool
    roots_are_cancellation_and_coefficient_neighbor: bool


@dataclass(frozen=True)
class CancellationLineProfile:
    row_count: int
    rows: tuple[CancellationLineRow, ...]
    all_lines_forced_by_cancellation_vertex: bool
    all_roots_are_cancellation_and_coefficient_neighbor: bool
    all_recorded_edges_point_to_cancellation: bool
    all_recorded_tangents_weight_to_negative_diagonal: bool
    line_intercepts_by_orientation_mask: tuple[tuple[int, int], ...]


def signed_mod(value: int, modulus: int = C_LOW_ORDER) -> int:
    value %= modulus
    return value if value <= modulus // 2 else value - modulus


def split_c169(c_value: int) -> LowFiber:
    return c_value % C_LOW_ORDER, c_value // C_LOW_ORDER


def cancellation_line_profile() -> CancellationLineProfile:
    active_rows = corner_profile().active_rows
    factor_rows = slope_line_factor_profile().rows
    chord_rows = slope_one_chord_profile().rows
    rows: list[CancellationLineRow] = []
    for active_row, factor_row, chord_row in zip(active_rows, factor_rows, chord_rows):
        cancellation = split_c169(active_row.cancellation_vertex_q % C_ORDER)
        intercept = (cancellation[1] - cancellation[0]) % C_LOW_ORDER
        neighbor = (
            (cancellation[0] + 2 * factor_row.chain_coefficient) % C_LOW_ORDER,
            (cancellation[1] + 2 * factor_row.chain_coefficient) % C_LOW_ORDER,
        )
        expected_roots = tuple(sorted((cancellation[0], neighbor[0])))
        recorded_edge = next(
            edge for edge in chord_row.edges
            if edge.direction_q == factor_row.recorded_direction_q
        )
        signed_tangent = (
            signed_mod(recorded_edge.to_low_fiber[0] - recorded_edge.from_low_fiber[0]),
            signed_mod(recorded_edge.to_low_fiber[1] - recorded_edge.from_low_fiber[1]),
        )
        weighted_tangent = (
            factor_row.chain_coefficient * signed_tangent[0],
            factor_row.chain_coefficient * signed_tangent[1],
        )
        rows.append(
            CancellationLineRow(
                orientation_mask=factor_row.orientation_mask,
                recorded_direction_q=factor_row.recorded_direction_q,
                chain_coefficient=factor_row.chain_coefficient,
                cancellation_vertex_q=active_row.cancellation_vertex_q,
                cancellation_low_fiber=cancellation,
                slope_one_line_intercept=factor_row.slope_one_line_intercept,
                intercept_from_cancellation=intercept,
                coefficient_neighbor_low_fiber=neighbor,
                residual_roots=factor_row.residual_roots,
                roots_from_cancellation_and_neighbor=expected_roots,
                recorded_edge_from_low_fiber=recorded_edge.from_low_fiber,
                recorded_edge_to_low_fiber=recorded_edge.to_low_fiber,
                recorded_edge_points_to_cancellation=(
                    recorded_edge.from_low_fiber == neighbor
                    and recorded_edge.to_low_fiber == cancellation
                ),
                recorded_signed_tangent=signed_tangent,
                coefficient_weighted_recorded_tangent=weighted_tangent,
                line_is_forced_by_cancellation_vertex=(
                    factor_row.slope_one_line_intercept == intercept
                ),
                roots_are_cancellation_and_coefficient_neighbor=(
                    factor_row.residual_roots == expected_roots
                ),
            )
        )
    rows_tuple = tuple(rows)
    intercepts_by_mask = tuple(sorted({
        (row.orientation_mask, row.slope_one_line_intercept)
        for row in rows_tuple
    }))
    return CancellationLineProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_lines_forced_by_cancellation_vertex=all(
            row.line_is_forced_by_cancellation_vertex for row in rows_tuple
        ),
        all_roots_are_cancellation_and_coefficient_neighbor=all(
            row.roots_are_cancellation_and_coefficient_neighbor for row in rows_tuple
        ),
        all_recorded_edges_point_to_cancellation=all(
            row.recorded_edge_points_to_cancellation for row in rows_tuple
        ),
        all_recorded_tangents_weight_to_negative_diagonal=all(
            row.coefficient_weighted_recorded_tangent == (-2, -2)
            for row in rows_tuple
        ),
        line_intercepts_by_orientation_mask=intercepts_by_mask,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner cancellation-line gate")
    profile = cancellation_line_profile()
    expected_rows = (
        CancellationLineRow(
            1, 197, -1, 172, (3, 0), 10, 10, (1, 11), (1, 3), (1, 3),
            (1, 11), (3, 0), True, (2, 2), (-2, -2), True, True,
        ),
        CancellationLineRow(
            1, 310, 1, 172, (3, 0), 10, 10, (5, 2), (3, 5), (3, 5),
            (5, 2), (3, 0), True, (-2, -2), (-2, -2), True, True,
        ),
        CancellationLineRow(
            6, 197, -1, 335, (10, 12), 2, 2, (8, 10), (8, 10), (8, 10),
            (8, 10), (10, 12), True, (2, 2), (-2, -2), True, True,
        ),
        CancellationLineRow(
            6, 310, 1, 335, (10, 12), 2, 2, (12, 1), (10, 12), (10, 12),
            (12, 1), (10, 12), True, (-2, -2), (-2, -2), True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_lines_forced_by_cancellation_vertex
        and profile.all_roots_are_cancellation_and_coefficient_neighbor
        and profile.all_recorded_edges_point_to_cancellation
        and profile.all_recorded_tangents_weight_to_negative_diagonal
        and profile.line_intercepts_by_orientation_mask == ((1, 10), (6, 2))
    )

    print(
        "corner_cancellation_line_summary: "
        f"line_intercepts_by_orientation_mask={profile.line_intercepts_by_orientation_mask} "
        f"cancellation_low_fibers={tuple(row.cancellation_low_fiber for row in profile.rows)} "
        f"coefficient_neighbors={tuple(row.coefficient_neighbor_low_fiber for row in profile.rows)} "
        f"weighted_tangents={tuple(row.coefficient_weighted_recorded_tangent for row in profile.rows)}"
    )
    print("corner_cancellation_line_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("cancellation_line_laws")
    print("  slope-one line intercept is f_cancel-c0_cancel")
    print("  residual roots are cancellation shadow and c0_cancel+2*coefficient")
    print("  recorded edge points from the coefficient-selected neighbor back to the cancellation vertex")
    print("interpretation")
    print("  slope_line_factor_has_no_free_line_choice_after_the_Hilbert90_cancellation_vertex=1")
    print("  half_bridge_endpoint_pair_is_cancellation_plus_coefficient_selected_diagonal_neighbor=1")
    print("  coefficient_weighted_recorded_tangent_is_forced_to_negative_diagonal=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_cancellation_line_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_cancellation_line_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

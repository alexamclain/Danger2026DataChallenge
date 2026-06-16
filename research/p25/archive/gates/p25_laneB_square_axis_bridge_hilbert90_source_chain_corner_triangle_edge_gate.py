#!/usr/bin/env python3
"""Triangle-edge law for the p25 Hilbert-90 corner branch selector.

The C-axis polarity gate simplifies the skew-orientation score to a signed
C_169 component.  This gate ties that component back to the geometry of the
three-point source corner.

For every active corner, the six one-cancellation first-boundary directions
are exactly the six directed edges between the three row-graph points.  Their
directed C steps are the three edge lengths +/-3, +/-25, and +/-28.  The
recorded branch is the directed half-bridge edge with coefficient-weighted
signed C-step -28; the opposite short branch is the same undirected edge with
polarity +28.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_c_axis_polarity_gate import (
    c_axis_polarity_profile,
    signed_c,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_gate import (
    chain_by_source_row,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class TriangleDirectedEdge:
    direction_q: int
    direction_d: int
    from_row: int
    to_row: int
    row_step: int
    signed_row_step: int
    from_c: int
    to_c: int
    c_step: int
    signed_c_step: int
    coefficient_weighted_signed_c_step: int
    branch_role: str
    is_half_bridge_edge: bool


@dataclass(frozen=True)
class TriangleEdgeRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    chain_coefficient: int
    chain_q_by_row: tuple[int, int, int]
    chain_c_by_row: tuple[int, int, int]
    directed_edge_directions_q: tuple[int, ...]
    one_cancellation_directions_q: tuple[int, ...]
    undirected_c_edge_lengths: tuple[int, ...]
    half_bridge_edge_directions_q: tuple[int, ...]
    recorded_edge: TriangleDirectedEdge
    opposite_edge: TriangleDirectedEdge
    directed_edges: tuple[TriangleDirectedEdge, ...]


@dataclass(frozen=True)
class TriangleEdgeProfile:
    row_count: int
    all_one_cancellations_are_directed_triangle_edges: bool
    all_directed_triangle_edges_are_one_cancellations: bool
    all_rows_have_standard_directed_edge_set: bool
    all_rows_have_c_edge_lengths_3_25_28: bool
    all_half_bridge_edges_are_197_310: bool
    all_recorded_edges_are_negative_half_bridge_polarity: bool
    all_opposite_edges_are_positive_half_bridge_polarity: bool
    rows: tuple[TriangleEdgeRow, ...]


def signed_row_step(step: int) -> int:
    step %= RIGHT_DEGREE
    return step if step <= RIGHT_DEGREE // 2 else step - RIGHT_DEGREE


def q_from_source_step(row_step: int, c_step: int) -> int:
    return (c_step + SQUARE_C * ((row_step - c_step) % RIGHT_DEGREE)) % QUOTIENT_ORDER


def triangle_edges(active_row, polarity_row) -> TriangleEdgeRow:
    chain = dict(zip(active_row.q_values, active_row.recorded_coefficients))
    rows_by_source = chain_by_source_row(chain)
    q_by_row = tuple(rows_by_source[row][0] for row in range(RIGHT_DEGREE))
    c_by_row = tuple(rows_by_source[row][1] for row in range(RIGHT_DEGREE))
    polarity_by_direction = {
        direction.direction_q: direction
        for direction in polarity_row.polarity_direction_rows
    }
    edges: list[TriangleDirectedEdge] = []
    for from_row in range(RIGHT_DEGREE):
        for to_row in range(RIGHT_DEGREE):
            if from_row == to_row:
                continue
            row_step = (to_row - from_row) % RIGHT_DEGREE
            c_step = (c_by_row[to_row] - c_by_row[from_row]) % SQUARE_C
            direction_q = q_from_source_step(row_step, c_step)
            polarity = polarity_by_direction[direction_q]
            edges.append(
                TriangleDirectedEdge(
                    direction_q=direction_q,
                    direction_d=d_residue_from_q(direction_q),
                    from_row=from_row,
                    to_row=to_row,
                    row_step=row_step,
                    signed_row_step=signed_row_step(row_step),
                    from_c=c_by_row[from_row],
                    to_c=c_by_row[to_row],
                    c_step=c_step,
                    signed_c_step=signed_c(c_step),
                    coefficient_weighted_signed_c_step=polarity.coefficient_weighted_signed_c_step,
                    branch_role=polarity.branch_role,
                    is_half_bridge_edge=direction_q in (197, 310),
                )
            )
    edges_tuple = tuple(sorted(edges, key=lambda edge: edge.direction_q))
    recorded = tuple(edge for edge in edges_tuple if edge.direction_q == active_row.boundary_direction_q)
    opposite = tuple(edge for edge in edges_tuple if edge.branch_role == "opposite_short")
    if len(recorded) != 1 or len(opposite) != 1:
        raise AssertionError("expected one recorded edge and one opposite edge")
    return TriangleEdgeRow(
        orientation_mask=active_row.orientation_mask,
        recorded_direction_q=active_row.boundary_direction_q,
        opposite_direction_q=opposite[0].direction_q,
        chain_coefficient=polarity_row.chain_coefficient,
        chain_q_by_row=q_by_row,  # type: ignore[arg-type]
        chain_c_by_row=c_by_row,  # type: ignore[arg-type]
        directed_edge_directions_q=tuple(edge.direction_q for edge in edges_tuple),
        one_cancellation_directions_q=tuple(direction.direction_q for direction in polarity_row.polarity_direction_rows),
        undirected_c_edge_lengths=tuple(
            sorted({abs(edge.signed_c_step) for edge in edges_tuple})
        ),
        half_bridge_edge_directions_q=tuple(
            edge.direction_q for edge in edges_tuple if edge.is_half_bridge_edge
        ),
        recorded_edge=recorded[0],
        opposite_edge=opposite[0],
        directed_edges=edges_tuple,
    )


def triangle_edge_profile() -> TriangleEdgeProfile:
    polarity_by_key = {
        (row.orientation_mask, row.recorded_direction_q): row
        for row in c_axis_polarity_profile().rows
    }
    rows = tuple(
        triangle_edges(active, polarity_by_key[(active.orientation_mask, active.boundary_direction_q)])
        for active in coefficient_rigidity_profile().rows
    )
    return TriangleEdgeProfile(
        row_count=len(rows),
        all_one_cancellations_are_directed_triangle_edges=all(
            row.one_cancellation_directions_q == row.directed_edge_directions_q
            for row in rows
        ),
        all_directed_triangle_edges_are_one_cancellations=all(
            len(row.directed_edges) == len(row.one_cancellation_directions_q) == 6
            for row in rows
        ),
        all_rows_have_standard_directed_edge_set=all(
            row.directed_edge_directions_q == (25, 172, 197, 310, 335, 482)
            for row in rows
        ),
        all_rows_have_c_edge_lengths_3_25_28=all(
            row.undirected_c_edge_lengths == (3, 25, 28)
            for row in rows
        ),
        all_half_bridge_edges_are_197_310=all(
            row.half_bridge_edge_directions_q == (197, 310)
            for row in rows
        ),
        all_recorded_edges_are_negative_half_bridge_polarity=all(
            row.recorded_edge.is_half_bridge_edge
            and row.recorded_edge.coefficient_weighted_signed_c_step == -28
            and row.recorded_edge.branch_role == "recorded"
            for row in rows
        ),
        all_opposite_edges_are_positive_half_bridge_polarity=all(
            row.opposite_edge.is_half_bridge_edge
            and row.opposite_edge.coefficient_weighted_signed_c_step == 28
            and row.opposite_edge.branch_role == "opposite_short"
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner triangle-edge gate")
    profile = triangle_edge_profile()
    expected_rows = (
        TriangleEdgeRow(
            1, 197, 310, -1, (0, 172, 482), (0, 3, 144), (25, 172, 197, 310, 335, 482),
            (25, 172, 197, 310, 335, 482), (3, 25, 28), (197, 310),
            TriangleDirectedEdge(197, 122, 2, 1, 2, -1, 144, 3, 28, 28, -28, "recorded", True),
            TriangleDirectedEdge(310, 385, 1, 2, 1, 1, 3, 144, 141, -28, 28, "opposite_short", True),
            (
                TriangleDirectedEdge(25, 121, 2, 0, 1, 1, 144, 0, 25, 25, -25, "other_one_cancellation", False),
                TriangleDirectedEdge(172, 1, 0, 1, 1, 1, 0, 3, 3, 3, -3, "other_one_cancellation", False),
                TriangleDirectedEdge(197, 122, 2, 1, 2, -1, 144, 3, 28, 28, -28, "recorded", True),
                TriangleDirectedEdge(310, 385, 1, 2, 1, 1, 3, 144, 141, -28, 28, "opposite_short", True),
                TriangleDirectedEdge(335, 506, 1, 0, 2, -1, 3, 0, 166, -3, 3, "other_one_cancellation", False),
                TriangleDirectedEdge(482, 386, 0, 2, 2, -1, 0, 144, 144, -25, 25, "other_one_cancellation", False),
            ),
        ),
        TriangleEdgeRow(
            1, 310, 197, 1, (369, 172, 197), (31, 3, 28), (25, 172, 197, 310, 335, 482),
            (25, 172, 197, 310, 335, 482), (3, 25, 28), (197, 310),
            TriangleDirectedEdge(310, 385, 0, 1, 1, 1, 31, 3, 141, -28, -28, "recorded", True),
            TriangleDirectedEdge(197, 122, 1, 0, 2, -1, 3, 31, 28, 28, 28, "opposite_short", True),
            (
                TriangleDirectedEdge(25, 121, 1, 2, 1, 1, 3, 28, 25, 25, 25, "other_one_cancellation", False),
                TriangleDirectedEdge(172, 1, 2, 0, 1, 1, 28, 31, 3, 3, 3, "other_one_cancellation", False),
                TriangleDirectedEdge(197, 122, 1, 0, 2, -1, 3, 31, 28, 28, 28, "opposite_short", True),
                TriangleDirectedEdge(310, 385, 0, 1, 1, 1, 31, 3, 141, -28, -28, "recorded", True),
                TriangleDirectedEdge(335, 506, 0, 2, 2, -1, 31, 28, 166, -3, -3, "other_one_cancellation", False),
                TriangleDirectedEdge(482, 386, 2, 1, 2, -1, 28, 3, 144, -25, -25, "other_one_cancellation", False),
            ),
        ),
        TriangleEdgeRow(
            6, 197, 310, -1, (138, 310, 335), (138, 141, 166), (25, 172, 197, 310, 335, 482),
            (25, 172, 197, 310, 335, 482), (3, 25, 28), (197, 310),
            TriangleDirectedEdge(197, 122, 0, 2, 2, -1, 138, 166, 28, 28, -28, "recorded", True),
            TriangleDirectedEdge(310, 385, 2, 0, 1, 1, 166, 138, 141, -28, 28, "opposite_short", True),
            (
                TriangleDirectedEdge(25, 121, 1, 2, 1, 1, 141, 166, 25, 25, -25, "other_one_cancellation", False),
                TriangleDirectedEdge(172, 1, 0, 1, 1, 1, 138, 141, 3, 3, -3, "other_one_cancellation", False),
                TriangleDirectedEdge(197, 122, 0, 2, 2, -1, 138, 166, 28, 28, -28, "recorded", True),
                TriangleDirectedEdge(310, 385, 2, 0, 1, 1, 166, 138, 141, -28, 28, "opposite_short", True),
                TriangleDirectedEdge(335, 506, 1, 0, 2, -1, 141, 138, 166, -3, 3, "other_one_cancellation", False),
                TriangleDirectedEdge(482, 386, 2, 1, 2, -1, 166, 141, 144, -25, 25, "other_one_cancellation", False),
            ),
        ),
        TriangleEdgeRow(
            6, 310, 197, 1, (0, 25, 335), (0, 25, 166), (25, 172, 197, 310, 335, 482),
            (25, 172, 197, 310, 335, 482), (3, 25, 28), (197, 310),
            TriangleDirectedEdge(310, 385, 1, 2, 1, 1, 25, 166, 141, -28, -28, "recorded", True),
            TriangleDirectedEdge(197, 122, 2, 1, 2, -1, 166, 25, 28, 28, 28, "opposite_short", True),
            (
                TriangleDirectedEdge(25, 121, 0, 1, 1, 1, 0, 25, 25, 25, 25, "other_one_cancellation", False),
                TriangleDirectedEdge(172, 1, 2, 0, 1, 1, 166, 0, 3, 3, 3, "other_one_cancellation", False),
                TriangleDirectedEdge(197, 122, 2, 1, 2, -1, 166, 25, 28, 28, 28, "opposite_short", True),
                TriangleDirectedEdge(310, 385, 1, 2, 1, 1, 25, 166, 141, -28, -28, "recorded", True),
                TriangleDirectedEdge(335, 506, 0, 2, 2, -1, 0, 166, 166, -3, -3, "other_one_cancellation", False),
                TriangleDirectedEdge(482, 386, 1, 0, 2, -1, 25, 0, 144, -25, -25, "other_one_cancellation", False),
            ),
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_one_cancellations_are_directed_triangle_edges
        and profile.all_directed_triangle_edges_are_one_cancellations
        and profile.all_rows_have_standard_directed_edge_set
        and profile.all_rows_have_c_edge_lengths_3_25_28
        and profile.all_half_bridge_edges_are_197_310
        and profile.all_recorded_edges_are_negative_half_bridge_polarity
        and profile.all_opposite_edges_are_positive_half_bridge_polarity
        and profile.rows == expected_rows
    )

    print(
        "corner_triangle_edge_summary: "
        f"directed_edge_sets={tuple(row.directed_edge_directions_q for row in profile.rows)} "
        f"c_edge_lengths={tuple(row.undirected_c_edge_lengths for row in profile.rows)} "
        f"recorded_edges={tuple(row.recorded_edge.direction_q for row in profile.rows)} "
        f"recorded_weighted_c={tuple(row.recorded_edge.coefficient_weighted_signed_c_step for row in profile.rows)}"
    )
    print("corner_triangle_edge_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("triangle_edge_laws")
    print("  one-cancellation first-boundary directions are exactly directed edges of the row-quadratic corner")
    print("  the three undirected C-edge lengths are 3, 25, and 28")
    print("  the half-bridge edge is the 197/310 pair with C-edge length 28")
    print("interpretation")
    print("  C_axis_polarity_is_a_directed_triangle_edge_selector=1")
    print("  producer_can_target_the_negative_polarity_half_bridge_edge_of_the_row_graph=1")
    print("  opposite_short_branch_is_the_same_undirected_edge_with_positive_polarity=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

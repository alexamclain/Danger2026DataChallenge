#!/usr/bin/env python3
"""Row-cycle descent law for the p25 Hilbert-90 source corner.

The monotone-edge gate identifies the half-bridge edge as the unique monotone
long edge of the row-quadratic source triangle.  This gate rewrites the same
selector in the fixed source-row cycle 0 -> 1 -> 2 -> 0.

Across all active corners, the C_169 row-cycle increments are two ascents and
one descent:

    {3, 25, -28}.

The unique descent is always the q=310 edge, and its reverse is q=197.  The
recorded branch is the orientation with coefficient-weighted signed C-step
-28: the descent itself for coefficient +1, and the reverse descent for
coefficient -1.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate import (
    TriangleDirectedEdge,
    TriangleEdgeRow,
    triangle_edge_profile,
)


@dataclass(frozen=True)
class RowCycleEdge:
    from_row: int
    to_row: int
    direction_q: int
    signed_c_step: int
    coefficient_weighted_signed_c_step: int
    branch_role: str


@dataclass(frozen=True)
class RowCycleDescentRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    chain_c_by_row: tuple[int, int, int]
    cycle_edges: tuple[RowCycleEdge, RowCycleEdge, RowCycleEdge]
    cycle_direction_qs: tuple[int, int, int]
    cycle_signed_c_steps: tuple[int, int, int]
    ascent_direction_qs: tuple[int, ...]
    descent_direction_q: int
    descent_branch_role: str
    reverse_descent_direction_q: int
    recorded_is_descent_when_coefficient_positive: bool
    recorded_is_reverse_descent_when_coefficient_negative: bool
    recorded_has_negative_weighted_descent: bool


@dataclass(frozen=True)
class RowCycleDescentProfile:
    row_count: int
    all_rows_have_two_ascents_and_one_descent: bool
    all_descent_edges_are_q310: bool
    all_reverse_descent_edges_are_q197: bool
    all_recorded_branches_have_negative_weighted_descent: bool
    rows: tuple[RowCycleDescentRow, ...]


def edge_by_pair(row: TriangleEdgeRow) -> dict[tuple[int, int], TriangleDirectedEdge]:
    return {(edge.from_row, edge.to_row): edge for edge in row.directed_edges}


def cycle_edge(edge: TriangleDirectedEdge) -> RowCycleEdge:
    return RowCycleEdge(
        from_row=edge.from_row,
        to_row=edge.to_row,
        direction_q=edge.direction_q,
        signed_c_step=edge.signed_c_step,
        coefficient_weighted_signed_c_step=edge.coefficient_weighted_signed_c_step,
        branch_role=edge.branch_role,
    )


def row_cycle_descent(row: TriangleEdgeRow) -> RowCycleDescentRow:
    by_pair = edge_by_pair(row)
    cycle = (
        cycle_edge(by_pair[(0, 1)]),
        cycle_edge(by_pair[(1, 2)]),
        cycle_edge(by_pair[(2, 0)]),
    )
    descents = tuple(edge for edge in cycle if edge.signed_c_step < 0)
    ascents = tuple(edge for edge in cycle if edge.signed_c_step > 0)
    if len(descents) != 1 or len(ascents) != 2:
        raise AssertionError(f"expected one descent and two ascents, got {cycle}")
    descent = descents[0]
    reverse_descent = by_pair[(descent.to_row, descent.from_row)]
    recorded = tuple(edge for edge in row.directed_edges if edge.direction_q == row.recorded_direction_q)
    if len(recorded) != 1:
        raise AssertionError("recorded edge missing from row-cycle scan")
    return RowCycleDescentRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.recorded_direction_q,
        chain_coefficient=row.chain_coefficient,
        chain_c_by_row=row.chain_c_by_row,
        cycle_edges=cycle,
        cycle_direction_qs=tuple(edge.direction_q for edge in cycle),  # type: ignore[arg-type]
        cycle_signed_c_steps=tuple(edge.signed_c_step for edge in cycle),  # type: ignore[arg-type]
        ascent_direction_qs=tuple(edge.direction_q for edge in ascents),
        descent_direction_q=descent.direction_q,
        descent_branch_role=descent.branch_role,
        reverse_descent_direction_q=reverse_descent.direction_q,
        recorded_is_descent_when_coefficient_positive=(
            row.chain_coefficient == 1 and row.recorded_direction_q == descent.direction_q
        ),
        recorded_is_reverse_descent_when_coefficient_negative=(
            row.chain_coefficient == -1 and row.recorded_direction_q == reverse_descent.direction_q
        ),
        recorded_has_negative_weighted_descent=(
            recorded[0].coefficient_weighted_signed_c_step == -28
        ),
    )


def row_cycle_descent_profile() -> RowCycleDescentProfile:
    rows = tuple(row_cycle_descent(row) for row in triangle_edge_profile().rows)
    return RowCycleDescentProfile(
        row_count=len(rows),
        all_rows_have_two_ascents_and_one_descent=all(
            sorted(row.cycle_signed_c_steps) == [-28, 3, 25]
            for row in rows
        ),
        all_descent_edges_are_q310=all(row.descent_direction_q == 310 for row in rows),
        all_reverse_descent_edges_are_q197=all(row.reverse_descent_direction_q == 197 for row in rows),
        all_recorded_branches_have_negative_weighted_descent=all(
            row.recorded_has_negative_weighted_descent
            and (
                row.recorded_is_descent_when_coefficient_positive
                or row.recorded_is_reverse_descent_when_coefficient_negative
            )
            for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner row-cycle descent gate")
    profile = row_cycle_descent_profile()
    expected_rows = (
        RowCycleDescentRow(
            1, 197, -1, (0, 3, 144),
            (
                RowCycleEdge(0, 1, 172, 3, -3, "other_one_cancellation"),
                RowCycleEdge(1, 2, 310, -28, 28, "opposite_short"),
                RowCycleEdge(2, 0, 25, 25, -25, "other_one_cancellation"),
            ),
            (172, 310, 25), (3, -28, 25), (172, 25), 310, "opposite_short", 197,
            False, True, True,
        ),
        RowCycleDescentRow(
            1, 310, 1, (31, 3, 28),
            (
                RowCycleEdge(0, 1, 310, -28, -28, "recorded"),
                RowCycleEdge(1, 2, 25, 25, 25, "other_one_cancellation"),
                RowCycleEdge(2, 0, 172, 3, 3, "other_one_cancellation"),
            ),
            (310, 25, 172), (-28, 25, 3), (25, 172), 310, "recorded", 197,
            True, False, True,
        ),
        RowCycleDescentRow(
            6, 197, -1, (138, 141, 166),
            (
                RowCycleEdge(0, 1, 172, 3, -3, "other_one_cancellation"),
                RowCycleEdge(1, 2, 25, 25, -25, "other_one_cancellation"),
                RowCycleEdge(2, 0, 310, -28, 28, "opposite_short"),
            ),
            (172, 25, 310), (3, 25, -28), (172, 25), 310, "opposite_short", 197,
            False, True, True,
        ),
        RowCycleDescentRow(
            6, 310, 1, (0, 25, 166),
            (
                RowCycleEdge(0, 1, 25, 25, 25, "other_one_cancellation"),
                RowCycleEdge(1, 2, 310, -28, -28, "recorded"),
                RowCycleEdge(2, 0, 172, 3, 3, "other_one_cancellation"),
            ),
            (25, 310, 172), (25, -28, 3), (25, 172), 310, "recorded", 197,
            True, False, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_have_two_ascents_and_one_descent
        and profile.all_descent_edges_are_q310
        and profile.all_reverse_descent_edges_are_q197
        and profile.all_recorded_branches_have_negative_weighted_descent
        and profile.rows == expected_rows
    )

    print(
        "corner_row_cycle_descent_summary: "
        f"cycle_steps={tuple(row.cycle_signed_c_steps for row in profile.rows)} "
        f"descent_q={tuple(row.descent_direction_q for row in profile.rows)} "
        f"recorded_q={tuple(row.recorded_direction_q for row in profile.rows)} "
        f"coefficients={tuple(row.chain_coefficient for row in profile.rows)}"
    )
    print("corner_row_cycle_descent_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("row_cycle_descent_laws")
    print("  source-row cycle has C-axis increments {-28,3,25}: two ascents and one descent")
    print("  the q=310 edge is always the unique descent; q=197 is its reverse")
    print("  the recorded branch is the coefficient-negative orientation of the descent")
    print("interpretation")
    print("  producer_can_target_a_row_cycle_with_one_descent_of_size_28=1")
    print("  coefficient_sign_selects_descent_or_reverse_descent=1")
    print("  monotone_long_edge_selector_is_equivalent_to_fixed_row_cycle_descent=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_row_cycle_descent_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_cycle_descent_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

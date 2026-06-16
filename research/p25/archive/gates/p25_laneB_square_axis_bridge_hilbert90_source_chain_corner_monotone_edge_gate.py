#!/usr/bin/env python3
"""Monotone long-edge law for the p25 Hilbert-90 source corner.

The triangle-edge gate identifies the six one-cancellation directions with
the six directed edges of the three-point row-quadratic corner.  This gate
separates the half-bridge edge from the other two undirected edges by a local
C-axis monotonicity law.

For the half-bridge edge, the two-leg path through the third corner vertex has
same-sign centered C_169 increments:

    25 + 3 = 28        or        -25 - 3 = -28.

The edges of C-length 3 or 25 have mixed-sign two-leg decompositions.  Thus
the recorded branch is the negative-polarity orientation of the unique
monotone long edge of the source triangle.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_triangle_edge_gate import (
    TriangleDirectedEdge,
    TriangleEdgeRow,
    triangle_edge_profile,
)


@dataclass(frozen=True)
class MonotoneEdgeDirectionRow:
    direction_q: int
    branch_role: str
    from_row: int
    to_row: int
    third_row: int
    direct_signed_c_step: int
    path_signed_c_steps: tuple[int, int]
    path_abs_c_steps: tuple[int, int]
    path_sum: int
    same_sign_path: bool
    is_monotone_long_edge: bool
    coefficient_weighted_signed_c_step: int


@dataclass(frozen=True)
class MonotoneEdgeRow:
    orientation_mask: int
    recorded_direction_q: int
    opposite_direction_q: int
    monotone_edge_directions_q: tuple[int, ...]
    monotone_edge_roles: tuple[str, ...]
    recorded_is_negative_monotone_long_edge: bool
    opposite_is_positive_monotone_long_edge: bool
    nonmonotone_edges_have_mixed_sign_paths: bool
    direction_rows: tuple[MonotoneEdgeDirectionRow, ...]


@dataclass(frozen=True)
class MonotoneEdgeProfile:
    row_count: int
    all_rows_have_exactly_two_monotone_long_edges: bool
    all_monotone_edges_are_197_310: bool
    all_recorded_edges_are_negative_monotone: bool
    all_opposite_edges_are_positive_monotone: bool
    all_nonmonotone_edges_have_mixed_sign_paths: bool
    rows: tuple[MonotoneEdgeRow, ...]


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def edge_by_pair(row: TriangleEdgeRow) -> dict[tuple[int, int], TriangleDirectedEdge]:
    return {(edge.from_row, edge.to_row): edge for edge in row.directed_edges}


def monotone_direction(row: TriangleEdgeRow, edge: TriangleDirectedEdge) -> MonotoneEdgeDirectionRow:
    by_pair = edge_by_pair(row)
    third = next(source_row for source_row in range(3) if source_row not in (edge.from_row, edge.to_row))
    first_leg = by_pair[(edge.from_row, third)]
    second_leg = by_pair[(third, edge.to_row)]
    path_steps = (first_leg.signed_c_step, second_leg.signed_c_step)
    same_sign = sign(path_steps[0]) == sign(path_steps[1])
    path_sum = sum(path_steps)
    is_monotone = (
        same_sign
        and path_sum == edge.signed_c_step
        and tuple(sorted(abs(step) for step in path_steps)) == (3, 25)
        and abs(edge.signed_c_step) == 28
    )
    return MonotoneEdgeDirectionRow(
        direction_q=edge.direction_q,
        branch_role=edge.branch_role,
        from_row=edge.from_row,
        to_row=edge.to_row,
        third_row=third,
        direct_signed_c_step=edge.signed_c_step,
        path_signed_c_steps=path_steps,
        path_abs_c_steps=tuple(sorted(abs(step) for step in path_steps)),  # type: ignore[arg-type]
        path_sum=path_sum,
        same_sign_path=same_sign,
        is_monotone_long_edge=is_monotone,
        coefficient_weighted_signed_c_step=edge.coefficient_weighted_signed_c_step,
    )


def monotone_row(row: TriangleEdgeRow) -> MonotoneEdgeRow:
    direction_rows = tuple(monotone_direction(row, edge) for edge in row.directed_edges)
    monotone_edges = tuple(direction for direction in direction_rows if direction.is_monotone_long_edge)
    recorded = tuple(direction for direction in direction_rows if direction.direction_q == row.recorded_direction_q)
    opposite = tuple(direction for direction in direction_rows if direction.direction_q == row.opposite_direction_q)
    if len(recorded) != 1 or len(opposite) != 1:
        raise AssertionError("recorded/opposite direction missing from monotone scan")
    return MonotoneEdgeRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.recorded_direction_q,
        opposite_direction_q=row.opposite_direction_q,
        monotone_edge_directions_q=tuple(direction.direction_q for direction in monotone_edges),
        monotone_edge_roles=tuple(direction.branch_role for direction in monotone_edges),
        recorded_is_negative_monotone_long_edge=(
            recorded[0].is_monotone_long_edge
            and recorded[0].coefficient_weighted_signed_c_step == -28
        ),
        opposite_is_positive_monotone_long_edge=(
            opposite[0].is_monotone_long_edge
            and opposite[0].coefficient_weighted_signed_c_step == 28
        ),
        nonmonotone_edges_have_mixed_sign_paths=all(
            direction.same_sign_path is False
            for direction in direction_rows
            if not direction.is_monotone_long_edge
        ),
        direction_rows=direction_rows,
    )


def monotone_edge_profile() -> MonotoneEdgeProfile:
    rows = tuple(monotone_row(row) for row in triangle_edge_profile().rows)
    return MonotoneEdgeProfile(
        row_count=len(rows),
        all_rows_have_exactly_two_monotone_long_edges=all(
            len(row.monotone_edge_directions_q) == 2 for row in rows
        ),
        all_monotone_edges_are_197_310=all(
            row.monotone_edge_directions_q == (197, 310) for row in rows
        ),
        all_recorded_edges_are_negative_monotone=all(
            row.recorded_is_negative_monotone_long_edge for row in rows
        ),
        all_opposite_edges_are_positive_monotone=all(
            row.opposite_is_positive_monotone_long_edge for row in rows
        ),
        all_nonmonotone_edges_have_mixed_sign_paths=all(
            row.nonmonotone_edges_have_mixed_sign_paths for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner monotone-edge gate")
    profile = monotone_edge_profile()
    expected_rows = (
        MonotoneEdgeRow(
            1, 197, 310, (197, 310), ("recorded", "opposite_short"), True, True, True,
            (
                MonotoneEdgeDirectionRow(25, "other_one_cancellation", 2, 0, 1, 25, (28, -3), (3, 28), 25, False, False, -25),
                MonotoneEdgeDirectionRow(172, "other_one_cancellation", 0, 1, 2, 3, (-25, 28), (25, 28), 3, False, False, -3),
                MonotoneEdgeDirectionRow(197, "recorded", 2, 1, 0, 28, (25, 3), (3, 25), 28, True, True, -28),
                MonotoneEdgeDirectionRow(310, "opposite_short", 1, 2, 0, -28, (-3, -25), (3, 25), -28, True, True, 28),
                MonotoneEdgeDirectionRow(335, "other_one_cancellation", 1, 0, 2, -3, (-28, 25), (25, 28), -3, False, False, 3),
                MonotoneEdgeDirectionRow(482, "other_one_cancellation", 0, 2, 1, -25, (3, -28), (3, 28), -25, False, False, 25),
            ),
        ),
        MonotoneEdgeRow(
            1, 310, 197, (197, 310), ("opposite_short", "recorded"), True, True, True,
            (
                MonotoneEdgeDirectionRow(25, "other_one_cancellation", 1, 2, 0, 25, (28, -3), (3, 28), 25, False, False, 25),
                MonotoneEdgeDirectionRow(172, "other_one_cancellation", 2, 0, 1, 3, (-25, 28), (25, 28), 3, False, False, 3),
                MonotoneEdgeDirectionRow(197, "opposite_short", 1, 0, 2, 28, (25, 3), (3, 25), 28, True, True, 28),
                MonotoneEdgeDirectionRow(310, "recorded", 0, 1, 2, -28, (-3, -25), (3, 25), -28, True, True, -28),
                MonotoneEdgeDirectionRow(335, "other_one_cancellation", 0, 2, 1, -3, (-28, 25), (25, 28), -3, False, False, -3),
                MonotoneEdgeDirectionRow(482, "other_one_cancellation", 2, 1, 0, -25, (3, -28), (3, 28), -25, False, False, -25),
            ),
        ),
        MonotoneEdgeRow(
            6, 197, 310, (197, 310), ("recorded", "opposite_short"), True, True, True,
            (
                MonotoneEdgeDirectionRow(25, "other_one_cancellation", 1, 2, 0, 25, (-3, 28), (3, 28), 25, False, False, -25),
                MonotoneEdgeDirectionRow(172, "other_one_cancellation", 0, 1, 2, 3, (28, -25), (25, 28), 3, False, False, -3),
                MonotoneEdgeDirectionRow(197, "recorded", 0, 2, 1, 28, (3, 25), (3, 25), 28, True, True, -28),
                MonotoneEdgeDirectionRow(310, "opposite_short", 2, 0, 1, -28, (-25, -3), (3, 25), -28, True, True, 28),
                MonotoneEdgeDirectionRow(335, "other_one_cancellation", 1, 0, 2, -3, (25, -28), (25, 28), -3, False, False, 3),
                MonotoneEdgeDirectionRow(482, "other_one_cancellation", 2, 1, 0, -25, (-28, 3), (3, 28), -25, False, False, 25),
            ),
        ),
        MonotoneEdgeRow(
            6, 310, 197, (197, 310), ("opposite_short", "recorded"), True, True, True,
            (
                MonotoneEdgeDirectionRow(25, "other_one_cancellation", 0, 1, 2, 25, (-3, 28), (3, 28), 25, False, False, 25),
                MonotoneEdgeDirectionRow(172, "other_one_cancellation", 2, 0, 1, 3, (28, -25), (25, 28), 3, False, False, 3),
                MonotoneEdgeDirectionRow(197, "opposite_short", 2, 1, 0, 28, (3, 25), (3, 25), 28, True, True, 28),
                MonotoneEdgeDirectionRow(310, "recorded", 1, 2, 0, -28, (-25, -3), (3, 25), -28, True, True, -28),
                MonotoneEdgeDirectionRow(335, "other_one_cancellation", 0, 2, 1, -3, (25, -28), (25, 28), -3, False, False, -3),
                MonotoneEdgeDirectionRow(482, "other_one_cancellation", 1, 0, 2, -25, (-28, 3), (3, 28), -25, False, False, -25),
            ),
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_have_exactly_two_monotone_long_edges
        and profile.all_monotone_edges_are_197_310
        and profile.all_recorded_edges_are_negative_monotone
        and profile.all_opposite_edges_are_positive_monotone
        and profile.all_nonmonotone_edges_have_mixed_sign_paths
        and profile.rows == expected_rows
    )

    print(
        "corner_monotone_edge_summary: "
        f"monotone_edges={tuple(row.monotone_edge_directions_q for row in profile.rows)} "
        f"monotone_roles={tuple(row.monotone_edge_roles for row in profile.rows)} "
        f"recorded_negative={tuple(row.recorded_is_negative_monotone_long_edge for row in profile.rows)}"
    )
    print("corner_monotone_edge_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("monotone_edge_laws")
    print("  the half-bridge edge is the unique C-axis monotone long edge of the source triangle")
    print("  its same-sign two-leg decompositions are 25+3=28 and -25-3=-28")
    print("  C-length 3 and C-length 25 edges have mixed-sign two-leg decompositions")
    print("interpretation")
    print("  producer_can_target_the_negative_orientation_of_the_monotone_long_edge=1")
    print("  opposite_short_branch_is_the_positive_orientation_of_the_same_monotone_long_edge=1")
    print("  non_half_bridge_triangle_edges_are_not_monotone_long_edges=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_monotone_edge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_monotone_edge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

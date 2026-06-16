#!/usr/bin/env python3
"""Source-edge alignment of the p25 Hilbert-90 corner half-potential.

The half-potential gate selected the unique support-four boundary containing
the q=0 fixed block and one correctly oriented representative from each bridge
inversion pair.  This gate rewrites that selected half-potential in actual
source coordinates C_3 x C_169.

The selected half-potential is a two-row source-edge object.  The q=0 fixed
block is an endpoint of one edge, the two primitive C_169 short steps are 31
and 53, and the bridge-pair orientation is what removes the remaining
ambiguity when the opposite half-boundary direction has the same q=0/two-edge
step profile.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_minimal_source_edge_gate import (
    RowEdge,
    row_edges,
)
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import boundary
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_potential_gate import (
    bridge_pairs,
    half_potential_representatives,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]
SourceItems = tuple[tuple[Coord, int], ...]


@dataclass(frozen=True)
class HalfSourceEdgeRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    fixed_q0_coefficient: int
    half_potential_q_items: tuple[tuple[int, int], ...]
    source_values: SourceItems
    active_source_rows: tuple[int, ...]
    missing_source_rows: tuple[int, ...]
    row_edges: tuple[RowEdge, ...]
    row_edge_short_steps: tuple[int, ...]
    row_edge_short_steps_mod13: tuple[int, ...]
    q0_edge_sign: int
    selected_pair_representatives: tuple[int, ...]
    q0_two_edge_3153_directions_q: tuple[int, ...]
    q0_two_edge_3153_directions_d: tuple[int, ...]
    exact_half_source_edge_directions_q: tuple[int, ...]
    exact_half_source_edge_directions_d: tuple[int, ...]
    ambiguous_two_edge_direction_count: int


@dataclass(frozen=True)
class HalfSourceEdgeProfile:
    row_count: int
    all_rows_have_two_primitive_edges: bool
    all_rows_have_short_steps_31_53: bool
    all_q0_blocks_are_edge_endpoints: bool
    all_exact_half_source_edges_are_recorded: bool
    two_edge_profile_is_not_always_sufficient: bool
    rows: tuple[HalfSourceEdgeRow, ...]


def source_coord(q_value: int) -> Coord:
    return (q_value % RIGHT_DEGREE, q_value % SQUARE_C)


def source_mask(poly: dict[int, int]) -> dict[Coord, int]:
    return {source_coord(q_value): coefficient for q_value, coefficient in poly.items()}


def source_items(poly: dict[int, int]) -> SourceItems:
    return tuple(sorted(source_mask(poly).items()))


def short_steps(edges: tuple[RowEdge, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            min(edge.positive_to_negative_step, edge.negative_to_positive_step)
            for edge in edges
        )
    )


def short_steps_mod13(edges: tuple[RowEdge, ...]) -> tuple[int, ...]:
    return tuple(sorted(step % 13 for step in short_steps(edges)))


def active_rows(edges: tuple[RowEdge, ...]) -> tuple[int, ...]:
    return tuple(edge.row for edge in edges)


def missing_rows(edges: tuple[RowEdge, ...]) -> tuple[int, ...]:
    active = set(active_rows(edges))
    return tuple(row for row in range(RIGHT_DEGREE) if row not in active)


def q0_edge_sign(poly: dict[int, int], edges: tuple[RowEdge, ...]) -> int:
    if 0 not in poly:
        raise AssertionError("q=0 is absent from half-potential")
    q0_coord = source_coord(0)
    if q0_coord not in source_mask(poly):
        raise AssertionError("q=0 source coordinate is absent")
    q0_row = q0_coord[0]
    if q0_row not in active_rows(edges):
        raise AssertionError("q=0 is not on a source edge")
    return poly[0]


def q0_two_edge_3153(poly: dict[int, int]) -> bool:
    if len(poly) != 4 or 0 not in poly:
        return False
    edges = row_edges(source_mask(poly))
    return (
        len(edges) == 2
        and all(edge.primitive_c169_steps for edge in edges)
        and short_steps(edges) == (31, 53)
    )


def scan_row(row, pairs: tuple[tuple[int, int], ...]) -> HalfSourceEdgeRow:
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    q0_two_edge_directions: list[int] = []
    exact_directions: list[int] = []
    exact_by_direction: dict[int, dict[int, int]] = {}

    for direction in range(1, QUOTIENT_ORDER):
        first = boundary(chain, direction)
        if q0_two_edge_3153(first):
            q0_two_edge_directions.append(direction)
        if half_potential_representatives(first, pairs) is not None:
            exact_directions.append(direction)
            exact_by_direction[direction] = first

    if len(exact_directions) != 1:
        raise AssertionError(f"expected one exact half source edge, got {exact_directions}")
    exact_direction = exact_directions[0]
    half = exact_by_direction[exact_direction]
    edges = row_edges(source_mask(half))
    representatives = half_potential_representatives(half, pairs)
    if representatives is None:
        raise AssertionError("exact direction lost half-potential representatives")

    return HalfSourceEdgeRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.boundary_direction_q,
        recorded_direction_d=d_residue_from_q(row.boundary_direction_q),
        fixed_q0_coefficient=half[0],
        half_potential_q_items=tuple(sorted(half.items())),
        source_values=source_items(half),
        active_source_rows=active_rows(edges),
        missing_source_rows=missing_rows(edges),
        row_edges=edges,
        row_edge_short_steps=short_steps(edges),
        row_edge_short_steps_mod13=short_steps_mod13(edges),
        q0_edge_sign=q0_edge_sign(half, edges),
        selected_pair_representatives=representatives,
        q0_two_edge_3153_directions_q=tuple(q0_two_edge_directions),
        q0_two_edge_3153_directions_d=tuple(
            d_residue_from_q(direction) for direction in q0_two_edge_directions
        ),
        exact_half_source_edge_directions_q=tuple(exact_directions),
        exact_half_source_edge_directions_d=tuple(
            d_residue_from_q(direction) for direction in exact_directions
        ),
        ambiguous_two_edge_direction_count=len(q0_two_edge_directions) - len(exact_directions),
    )


def half_source_edge_profile() -> HalfSourceEdgeProfile:
    pairs = bridge_pairs()
    rows = tuple(scan_row(row, pairs) for row in coefficient_rigidity_profile().rows)
    return HalfSourceEdgeProfile(
        row_count=len(rows),
        all_rows_have_two_primitive_edges=all(
            len(row.row_edges) == 2
            and all(edge.primitive_c169_steps for edge in row.row_edges)
            for row in rows
        ),
        all_rows_have_short_steps_31_53=all(
            row.row_edge_short_steps == (31, 53)
            and row.row_edge_short_steps_mod13 == (1, 5)
            for row in rows
        ),
        all_q0_blocks_are_edge_endpoints=all(row.q0_edge_sign == row.fixed_q0_coefficient for row in rows),
        all_exact_half_source_edges_are_recorded=all(
            row.exact_half_source_edge_directions_q == (row.recorded_direction_q,)
            and row.exact_half_source_edge_directions_d == (row.recorded_direction_d,)
            for row in rows
        ),
        two_edge_profile_is_not_always_sufficient=any(
            row.ambiguous_two_edge_direction_count > 0 for row in rows
        ),
        rows=rows,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner half-source-edge gate")
    profile = half_source_edge_profile()
    edge_a = RowEdge(0, 31, 0, 138, 31, 8, 5, True)
    edge_b = RowEdge(2, 28, 144, 116, 53, 12, 1, True)
    edge_c = RowEdge(0, 0, 138, 138, 31, 8, 5, True)
    edge_d = RowEdge(1, 25, 141, 116, 53, 12, 1, True)
    expected_rows = (
        HalfSourceEdgeRow(1, 197, 122, -1, ((0, -1), (197, 1), (369, 1), (482, -1)), (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)), (0, 2), (1,), (edge_a, edge_b), (31, 53), (1, 5), -1, (482, 197, 369), (197, 310), (122, 385), (197,), (122,), 1),
        HalfSourceEdgeRow(1, 310, 385, -1, ((0, -1), (197, 1), (369, 1), (482, -1)), (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)), (0, 2), (1,), (edge_a, edge_b), (31, 53), (1, 5), -1, (482, 197, 369), (310,), (385,), (310,), (385,), 0),
        HalfSourceEdgeRow(6, 197, 122, 1, ((0, 1), (25, 1), (138, -1), (310, -1)), (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)), (0, 1), (2,), (edge_c, edge_d), (31, 53), (1, 5), 1, (25, 310, 138), (197,), (122,), (197,), (122,), 0),
        HalfSourceEdgeRow(6, 310, 385, 1, ((0, 1), (25, 1), (138, -1), (310, -1)), (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)), (0, 1), (2,), (edge_c, edge_d), (31, 53), (1, 5), 1, (25, 310, 138), (197, 310), (122, 385), (310,), (385,), 1),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_rows_have_two_primitive_edges
        and profile.all_rows_have_short_steps_31_53
        and profile.all_q0_blocks_are_edge_endpoints
        and profile.all_exact_half_source_edges_are_recorded
        and profile.two_edge_profile_is_not_always_sufficient
        and profile.rows == expected_rows
    )

    print(
        "corner_half_source_edge_summary: "
        f"active_rows={tuple(row.active_source_rows for row in profile.rows)} "
        f"missing_rows={tuple(row.missing_source_rows for row in profile.rows)} "
        f"q0_two_edge_hits={tuple(row.q0_two_edge_3153_directions_q for row in profile.rows)} "
        f"exact_hits={tuple(row.exact_half_source_edge_directions_q for row in profile.rows)}"
    )
    print("corner_half_source_edge_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("selector_laws")
    print("  the selected half-potential is two primitive row-local C169 edges")
    print("  q=0 is an endpoint of one source edge with the fixed-block sign")
    print("  the row-edge short steps are exactly 31 and 53 with C13 shadows 5 and 1")
    print("  q0/two-edge/31-53 shape alone can be ambiguous; bridge-pair orientation selects the recorded direction")
    print("interpretation")
    print("  producer_must_realize_the_half_potential_as_oriented_source_edges=1")
    print("  primitive_row_edge_shape_without_bridge_pair_orientation_is_too_weak=1")
    print("  half_source_edge_alignment_links_q0_repair_to_the_curved_corner_boundary=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

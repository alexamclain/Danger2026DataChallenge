#!/usr/bin/env python3
"""Tangent-plane descent law for the p25 Hilbert-90 source corner.

The row-cycle descent gate reduces the half-bridge selector to the unique
C_169 descent in the fixed source-row cycle.  This gate splits that descent
into its C_13 shadow and C_13 fiber tangent:

    -28 = -2 + 13*(-2).

Thus the selected branch can be phrased before the full C_169 scalar as the
coefficient-weighted negative diagonal tangent (-2,-2).  The other row-cycle
edges are a pure-shadow step (3,0) and a mixed step (-1,2).
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_row_cycle_descent_gate import (
    RowCycleDescentRow,
    row_cycle_descent_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
)


TangentPair = tuple[int, int]


@dataclass(frozen=True)
class TangentEdge:
    direction_q: int
    signed_c_step: int
    signed_c13_step: int
    signed_fiber_step: int
    tangent_pair: TangentPair
    tangent_role: str


@dataclass(frozen=True)
class TangentDescentRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    cycle_tangent_edges: tuple[TangentEdge, TangentEdge, TangentEdge]
    cycle_tangent_pairs: tuple[TangentPair, TangentPair, TangentPair]
    descent_tangent_edge: TangentEdge
    reverse_descent_tangent_edge: TangentEdge
    recorded_tangent_edge: TangentEdge
    coefficient_weighted_recorded_tangent: TangentPair
    cycle_has_pure_shadow_mixed_and_negative_diagonal: bool
    descent_is_negative_diagonal: bool
    reverse_descent_is_positive_diagonal: bool
    recorded_is_coefficient_weighted_negative_diagonal: bool


@dataclass(frozen=True)
class TangentDescentProfile:
    row_count: int
    rows: tuple[TangentDescentRow, ...]
    all_cycle_rows_have_standard_tangent_set: bool
    all_descent_edges_are_negative_diagonal: bool
    all_reverse_descent_edges_are_positive_diagonal: bool
    all_recorded_branches_are_coefficient_weighted_negative_diagonal: bool
    standard_cycle_tangent_set: tuple[TangentPair, ...]


def centered_mod(value: int, modulus: int) -> int:
    value %= modulus
    return value if value <= modulus // 2 else value - modulus


def tangent_role(pair: TangentPair) -> str:
    low_step, fiber_step = pair
    if low_step == fiber_step and low_step < 0:
        return "negative_diagonal"
    if low_step == fiber_step and low_step > 0:
        return "positive_diagonal"
    if fiber_step == 0:
        return "pure_shadow"
    if (low_step < 0 < fiber_step) or (fiber_step < 0 < low_step):
        return "mixed"
    return "other"


def tangent_edge(direction_q: int, signed_c_step: int) -> TangentEdge:
    signed_c13_step = centered_mod(signed_c_step, C_LOW_ORDER)
    if (signed_c_step - signed_c13_step) % C_LOW_ORDER:
        raise AssertionError("C_169 step does not split into C_13 plus fiber tangent")
    signed_fiber_step = (signed_c_step - signed_c13_step) // C_LOW_ORDER
    pair = (signed_c13_step, signed_fiber_step)
    return TangentEdge(
        direction_q=direction_q,
        signed_c_step=signed_c_step,
        signed_c13_step=signed_c13_step,
        signed_fiber_step=signed_fiber_step,
        tangent_pair=pair,
        tangent_role=tangent_role(pair),
    )


def signed_c_step_for_direction(row: RowCycleDescentRow, direction_q: int) -> int:
    for edge in row.cycle_edges:
        if edge.direction_q == direction_q:
            return edge.signed_c_step
    if direction_q == row.reverse_descent_direction_q:
        descent = next(edge for edge in row.cycle_edges if edge.direction_q == row.descent_direction_q)
        return -descent.signed_c_step
    raise AssertionError(f"direction {direction_q} is not a cycle or reverse-descent edge")


def tangent_descent_row(row: RowCycleDescentRow) -> TangentDescentRow:
    cycle = tuple(tangent_edge(edge.direction_q, edge.signed_c_step) for edge in row.cycle_edges)
    descent = tangent_edge(
        row.descent_direction_q,
        signed_c_step_for_direction(row, row.descent_direction_q),
    )
    reverse_descent = tangent_edge(
        row.reverse_descent_direction_q,
        signed_c_step_for_direction(row, row.reverse_descent_direction_q),
    )
    recorded = tangent_edge(
        row.recorded_direction_q,
        signed_c_step_for_direction(row, row.recorded_direction_q),
    )
    weighted_recorded = (
        row.chain_coefficient * recorded.signed_c13_step,
        row.chain_coefficient * recorded.signed_fiber_step,
    )
    standard_set = ((-2, -2), (-1, 2), (3, 0))
    return TangentDescentRow(
        orientation_mask=row.orientation_mask,
        recorded_direction_q=row.recorded_direction_q,
        chain_coefficient=row.chain_coefficient,
        cycle_tangent_edges=cycle,  # type: ignore[arg-type]
        cycle_tangent_pairs=tuple(edge.tangent_pair for edge in cycle),  # type: ignore[arg-type]
        descent_tangent_edge=descent,
        reverse_descent_tangent_edge=reverse_descent,
        recorded_tangent_edge=recorded,
        coefficient_weighted_recorded_tangent=weighted_recorded,
        cycle_has_pure_shadow_mixed_and_negative_diagonal=tuple(sorted(edge.tangent_pair for edge in cycle)) == standard_set,
        descent_is_negative_diagonal=descent.tangent_role == "negative_diagonal",
        reverse_descent_is_positive_diagonal=reverse_descent.tangent_role == "positive_diagonal",
        recorded_is_coefficient_weighted_negative_diagonal=weighted_recorded == (-2, -2),
    )


def tangent_descent_profile() -> TangentDescentProfile:
    rows = tuple(tangent_descent_row(row) for row in row_cycle_descent_profile().rows)
    standard_set = ((-2, -2), (-1, 2), (3, 0))
    return TangentDescentProfile(
        row_count=len(rows),
        rows=rows,
        all_cycle_rows_have_standard_tangent_set=all(
            row.cycle_has_pure_shadow_mixed_and_negative_diagonal
            for row in rows
        ),
        all_descent_edges_are_negative_diagonal=all(row.descent_is_negative_diagonal for row in rows),
        all_reverse_descent_edges_are_positive_diagonal=all(row.reverse_descent_is_positive_diagonal for row in rows),
        all_recorded_branches_are_coefficient_weighted_negative_diagonal=all(
            row.recorded_is_coefficient_weighted_negative_diagonal
            for row in rows
        ),
        standard_cycle_tangent_set=standard_set,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner tangent-descent gate")
    profile = tangent_descent_profile()
    expected_rows = (
        TangentDescentRow(
            1, 197, -1,
            (
                TangentEdge(172, 3, 3, 0, (3, 0), "pure_shadow"),
                TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
                TangentEdge(25, 25, -1, 2, (-1, 2), "mixed"),
            ),
            ((3, 0), (-2, -2), (-1, 2)),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            (-2, -2), True, True, True, True,
        ),
        TangentDescentRow(
            1, 310, 1,
            (
                TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
                TangentEdge(25, 25, -1, 2, (-1, 2), "mixed"),
                TangentEdge(172, 3, 3, 0, (3, 0), "pure_shadow"),
            ),
            ((-2, -2), (-1, 2), (3, 0)),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            (-2, -2), True, True, True, True,
        ),
        TangentDescentRow(
            6, 197, -1,
            (
                TangentEdge(172, 3, 3, 0, (3, 0), "pure_shadow"),
                TangentEdge(25, 25, -1, 2, (-1, 2), "mixed"),
                TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            ),
            ((3, 0), (-1, 2), (-2, -2)),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            (-2, -2), True, True, True, True,
        ),
        TangentDescentRow(
            6, 310, 1,
            (
                TangentEdge(25, 25, -1, 2, (-1, 2), "mixed"),
                TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
                TangentEdge(172, 3, 3, 0, (3, 0), "pure_shadow"),
            ),
            ((-1, 2), (-2, -2), (3, 0)),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            TangentEdge(197, 28, 2, 2, (2, 2), "positive_diagonal"),
            TangentEdge(310, -28, -2, -2, (-2, -2), "negative_diagonal"),
            (-2, -2), True, True, True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_cycle_rows_have_standard_tangent_set
        and profile.all_descent_edges_are_negative_diagonal
        and profile.all_reverse_descent_edges_are_positive_diagonal
        and profile.all_recorded_branches_are_coefficient_weighted_negative_diagonal
        and profile.standard_cycle_tangent_set == ((-2, -2), (-1, 2), (3, 0))
    )

    print(
        "corner_tangent_descent_summary: "
        f"standard_cycle_tangent_set={profile.standard_cycle_tangent_set} "
        f"recorded_weighted_tangents={tuple(row.coefficient_weighted_recorded_tangent for row in profile.rows)} "
        f"descent_tangents={tuple(row.descent_tangent_edge.tangent_pair for row in profile.rows)} "
        f"reverse_descent_tangents={tuple(row.reverse_descent_tangent_edge.tangent_pair for row in profile.rows)}"
    )
    print("corner_tangent_descent_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("tangent_descent_laws")
    print("  row-cycle tangent set is {(-2,-2),(-1,2),(3,0)}")
    print("  q=310 is the unique negative diagonal tangent (-2,-2)")
    print("  q=197 is the reverse positive diagonal tangent (2,2)")
    print("  the recorded branch is always coefficient-weighted tangent (-2,-2)")
    print("interpretation")
    print("  descent_selector_lives_in_C13_shadow_plus_fiber_tangent_coordinates=1")
    print("  producer_can_target_a_negative_diagonal_tangent_before_full_C169_scalar=1")
    print("  mixed_and_pure_shadow_cycle_edges_are_controls_for_the_half_bridge_edge=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_tangent_descent_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_tangent_descent_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Skew-derivative law for the p25 Hilbert-90 corner half-source-edge.

The half-source-edge gate records the selected half-potential as two primitive
row-local C_169 edges.  This gate ties those two edges back to the curved
three-point source graph.

For each active corner, applying the recorded first-boundary translation to
the source-row graph is a skew row derivative:

    delta_c(R) = c(R - d_row) + d_c - c(R)  in C_169.

Exactly one row has delta_c = 0, so one Newton vertex cancels.  The two
surviving row residuals are precisely the selected short C_169 edges with
short lengths 31 and 53.  Thus the half-potential is not an independent
two-edge object; it is the visible nonzero residual of the row-quadratic
corner under the rigid 197/310 boundary.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import boundary
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_gate import (
    SourceItems,
    half_source_edge_profile,
    source_coord,
    source_items,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    d_residue_from_q,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]
SignedSourceItems = tuple[tuple[Coord, int], ...]


@dataclass(frozen=True)
class SkewResidualRow:
    target_row: int
    shifted_from_row: int
    original_c: int
    shifted_c: int
    delta_c: int
    short_step: int
    short_step_mod13: int
    cancels: bool
    row_items: SignedSourceItems


@dataclass(frozen=True)
class CornerSkewDerivativeRow:
    orientation_mask: int
    recorded_direction_q: int
    recorded_direction_d: int
    direction_source_step: Coord
    chain_coefficient: int
    chain_source_graph: SourceItems
    cancellation_source_row: int
    cancellation_source_coord: Coord
    active_source_rows: tuple[int, ...]
    residual_delta_values: tuple[int, ...]
    residual_short_steps: tuple[int, ...]
    residual_short_steps_mod13: tuple[int, ...]
    row_residuals: tuple[SkewResidualRow, ...]
    reconstructed_half_source_values: SourceItems
    recorded_half_source_values: SourceItems
    reconstructed_matches_recorded: bool
    missing_row_matches_cancellation: bool


@dataclass(frozen=True)
class CornerSkewDerivativeProfile:
    row_count: int
    all_reconstructions_match_recorded: bool
    all_missing_rows_are_cancellations: bool
    all_rows_have_one_zero_residual: bool
    all_rows_have_short_residuals_31_53: bool
    all_rows_use_recorded_197_310_boundary: bool
    rows: tuple[CornerSkewDerivativeRow, ...]


def signed_short_step(value: int) -> int:
    return min(value % SQUARE_C, (-value) % SQUARE_C)


def sorted_source_items(items: list[tuple[Coord, int]]) -> SignedSourceItems:
    return tuple(sorted((coord, coefficient) for coord, coefficient in items if coefficient))


def source_graph_items(chain: dict[int, int]) -> SourceItems:
    return tuple(sorted((source_coord(q_value), coefficient) for q_value, coefficient in chain.items()))


def chain_by_source_row(chain: dict[int, int]) -> dict[int, tuple[int, int, int]]:
    out: dict[int, tuple[int, int, int]] = {}
    for q_value, coefficient in chain.items():
        row, c_value = source_coord(q_value)
        if row in out:
            raise AssertionError(f"source row {row} has more than one chain point")
        out[row] = (q_value, c_value, coefficient)
    if sorted(out) != list(range(RIGHT_DEGREE)):
        raise AssertionError(f"source graph does not cover all rows: {sorted(out)}")
    return out


def reconstructed_from_residuals(residuals: tuple[SkewResidualRow, ...]) -> SourceItems:
    by_coord: dict[Coord, int] = defaultdict(int)
    for residual in residuals:
        for coord, coefficient in residual.row_items:
            by_coord[coord] += coefficient
    return tuple(sorted((coord, coefficient) for coord, coefficient in by_coord.items() if coefficient))


def skew_derivative_row(active_row, recorded_half: SourceItems, missing_row: int) -> CornerSkewDerivativeRow:
    chain = dict(zip(active_row.q_values, active_row.recorded_coefficients))
    chain_rows = chain_by_source_row(chain)
    coefficients = {coefficient for _q, _c, coefficient in chain_rows.values()}
    if len(coefficients) != 1:
        raise AssertionError(f"expected all-equal chain coefficients, got {coefficients}")
    chain_coefficient = next(iter(coefficients))
    direction_q = active_row.boundary_direction_q
    direction_source_step = source_coord(direction_q)
    direction_row, direction_c = direction_source_step

    residuals: list[SkewResidualRow] = []
    for target_row in range(RIGHT_DEGREE):
        shifted_from_row = (target_row - direction_row) % RIGHT_DEGREE
        _orig_q, original_c, original_coeff = chain_rows[target_row]
        _shift_q, shift_source_c, shift_coeff = chain_rows[shifted_from_row]
        shifted_c = (shift_source_c + direction_c) % SQUARE_C
        shifted_coeff = -shift_coeff
        if original_coeff != chain_coefficient:
            raise AssertionError("nonuniform coefficient slipped through")
        row_items = sorted_source_items(
            [
                ((target_row, original_c), original_coeff),
                ((target_row, shifted_c), shifted_coeff),
            ]
        )
        delta = (shifted_c - original_c) % SQUARE_C
        residuals.append(
            SkewResidualRow(
                target_row=target_row,
                shifted_from_row=shifted_from_row,
                original_c=original_c,
                shifted_c=shifted_c,
                delta_c=delta,
                short_step=signed_short_step(delta),
                short_step_mod13=signed_short_step(delta) % 13,
                cancels=delta == 0,
                row_items=row_items,
            )
        )

    reconstructed = reconstructed_from_residuals(tuple(residuals))
    boundary_source_values = source_items(boundary(chain, direction_q))
    if reconstructed != boundary_source_values:
        raise AssertionError("skew derivative reconstruction does not match quotient boundary")
    cancellation_rows = tuple(row.target_row for row in residuals if row.cancels)
    if len(cancellation_rows) != 1:
        raise AssertionError(f"expected one cancellation row, got {cancellation_rows}")
    cancellation_row = cancellation_rows[0]
    cancellation_coord = (cancellation_row, chain_rows[cancellation_row][1])
    active_source_rows = tuple(row.target_row for row in residuals if not row.cancels)

    return CornerSkewDerivativeRow(
        orientation_mask=active_row.orientation_mask,
        recorded_direction_q=direction_q,
        recorded_direction_d=d_residue_from_q(direction_q),
        direction_source_step=direction_source_step,
        chain_coefficient=chain_coefficient,
        chain_source_graph=source_graph_items(chain),
        cancellation_source_row=cancellation_row,
        cancellation_source_coord=cancellation_coord,
        active_source_rows=active_source_rows,
        residual_delta_values=tuple(row.delta_c for row in residuals),
        residual_short_steps=tuple(sorted(row.short_step for row in residuals if not row.cancels)),
        residual_short_steps_mod13=tuple(sorted(row.short_step_mod13 for row in residuals if not row.cancels)),
        row_residuals=tuple(residuals),
        reconstructed_half_source_values=reconstructed,
        recorded_half_source_values=recorded_half,
        reconstructed_matches_recorded=reconstructed == recorded_half,
        missing_row_matches_cancellation=(missing_row == cancellation_row),
    )


def skew_derivative_profile() -> CornerSkewDerivativeProfile:
    half_edges = half_source_edge_profile()
    half_by_key = {
        (row.orientation_mask, row.recorded_direction_q): row
        for row in half_edges.rows
    }
    rows = []
    for active_row in coefficient_rigidity_profile().rows:
        half_row = half_by_key[(active_row.orientation_mask, active_row.boundary_direction_q)]
        if len(half_row.missing_source_rows) != 1:
            raise AssertionError(f"expected one missing source row, got {half_row.missing_source_rows}")
        rows.append(
            skew_derivative_row(
                active_row,
                half_row.source_values,
                half_row.missing_source_rows[0],
            )
        )
    rows_tuple = tuple(rows)
    return CornerSkewDerivativeProfile(
        row_count=len(rows_tuple),
        all_reconstructions_match_recorded=all(row.reconstructed_matches_recorded for row in rows_tuple),
        all_missing_rows_are_cancellations=all(row.missing_row_matches_cancellation for row in rows_tuple),
        all_rows_have_one_zero_residual=all(
            sum(residual.cancels for residual in row.row_residuals) == 1
            for row in rows_tuple
        ),
        all_rows_have_short_residuals_31_53=all(
            row.residual_short_steps == (31, 53)
            and row.residual_short_steps_mod13 == (1, 5)
            for row in rows_tuple
        ),
        all_rows_use_recorded_197_310_boundary=all(
            row.recorded_direction_q in (197, 310)
            and row.recorded_direction_d in (122, 385)
            for row in rows_tuple
        ),
        rows=rows_tuple,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner skew-derivative gate")
    profile = skew_derivative_profile()
    expected_rows = (
        CornerSkewDerivativeRow(
            1, 197, 122, (2, 28), -1,
            (((0, 0), -1), ((1, 3), -1), ((2, 144), -1)),
            1, (1, 3), (0, 2), (31, 0, 53), (31, 53), (1, 5),
            (
                SkewResidualRow(0, 1, 0, 31, 31, 31, 5, False, (((0, 0), -1), ((0, 31), 1))),
                SkewResidualRow(1, 2, 3, 3, 0, 0, 0, True, (((1, 3), -1), ((1, 3), 1))),
                SkewResidualRow(2, 0, 144, 28, 53, 53, 1, False, (((2, 28), 1), ((2, 144), -1))),
            ),
            (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)),
            (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)),
            True, True,
        ),
        CornerSkewDerivativeRow(
            1, 310, 385, (1, 141), 1,
            (((0, 31), 1), ((1, 3), 1), ((2, 28), 1)),
            1, (1, 3), (0, 2), (138, 0, 116), (31, 53), (1, 5),
            (
                SkewResidualRow(0, 2, 31, 0, 138, 31, 5, False, (((0, 0), -1), ((0, 31), 1))),
                SkewResidualRow(1, 0, 3, 3, 0, 0, 0, True, (((1, 3), -1), ((1, 3), 1))),
                SkewResidualRow(2, 1, 28, 144, 116, 53, 1, False, (((2, 28), 1), ((2, 144), -1))),
            ),
            (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)),
            (((0, 0), -1), ((0, 31), 1), ((2, 28), 1), ((2, 144), -1)),
            True, True,
        ),
        CornerSkewDerivativeRow(
            6, 197, 122, (2, 28), -1,
            (((0, 138), -1), ((1, 141), -1), ((2, 166), -1)),
            2, (2, 166), (0, 1), (31, 53, 0), (31, 53), (1, 5),
            (
                SkewResidualRow(0, 1, 138, 0, 31, 31, 5, False, (((0, 0), 1), ((0, 138), -1))),
                SkewResidualRow(1, 2, 141, 25, 53, 53, 1, False, (((1, 25), 1), ((1, 141), -1))),
                SkewResidualRow(2, 0, 166, 166, 0, 0, 0, True, (((2, 166), -1), ((2, 166), 1))),
            ),
            (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)),
            (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)),
            True, True,
        ),
        CornerSkewDerivativeRow(
            6, 310, 385, (1, 141), 1,
            (((0, 0), 1), ((1, 25), 1), ((2, 166), 1)),
            2, (2, 166), (0, 1), (138, 116, 0), (31, 53), (1, 5),
            (
                SkewResidualRow(0, 2, 0, 138, 138, 31, 5, False, (((0, 0), 1), ((0, 138), -1))),
                SkewResidualRow(1, 0, 25, 141, 116, 53, 1, False, (((1, 25), 1), ((1, 141), -1))),
                SkewResidualRow(2, 1, 166, 166, 0, 0, 0, True, (((2, 166), -1), ((2, 166), 1))),
            ),
            (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)),
            (((0, 0), 1), ((0, 138), -1), ((1, 25), 1), ((1, 141), -1)),
            True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.all_reconstructions_match_recorded
        and profile.all_missing_rows_are_cancellations
        and profile.all_rows_have_one_zero_residual
        and profile.all_rows_have_short_residuals_31_53
        and profile.all_rows_use_recorded_197_310_boundary
        and profile.rows == expected_rows
    )

    print(
        "corner_skew_derivative_summary: "
        f"directions={tuple(row.recorded_direction_q for row in profile.rows)} "
        f"direction_steps={tuple(row.direction_source_step for row in profile.rows)} "
        f"cancellation_rows={tuple(row.cancellation_source_row for row in profile.rows)} "
        f"residual_shorts={tuple(row.residual_short_steps for row in profile.rows)}"
    )
    print("corner_skew_derivative_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("skew_derivative_laws")
    print("  the recorded 197/310 first boundary is a skew row derivative of the source graph")
    print("  exactly one Newton vertex cancels, giving the missing source row")
    print("  the two nonzero row residuals are exactly the selected 31/53 half-source edges")
    print("interpretation")
    print("  half_source_edge_is_forced_by_row_quadratic_plus_recorded_boundary=1")
    print("  producer_must_realize_the_skew_derivative_not_an_independent_two_edge_mask=1")
    print("  cancellation_row_identifies_the_fixed_q0_half_potential_orientation=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

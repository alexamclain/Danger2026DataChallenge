#!/usr/bin/env python3
"""Slope-one line factorization for the p25 Hilbert-90 source corner.

The slope-one chord gate identifies the half-bridge pair 197/310 as the
unique slope-one secants of the active quadratic fiber section.  This gate
rewrites the same selection as a factored line intersection.

For each active corner, write the C_169 source values as c = c0 + 13*f.  There
is a slope-one line

    f = c0 + s

whose intersection with the active quadratic fiber section has exactly the two
half-bridge endpoints as roots.  The remaining selected row point is off that
line.  Thus a producer can target a line-subtracted quadratic residual before
choosing the oriented Hilbert-90 boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
    corner_fiber_section_profile,
    quadratic_value,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_one_chord_gate import (
    slope_one_chord_profile,
)


Quad = tuple[int, int, int]


@dataclass(frozen=True)
class LineResidualPoint:
    source_row: int
    c13_shadow: int
    fiber: int
    line_residual: int
    lies_on_slope_one_line: bool


@dataclass(frozen=True)
class SlopeLineFactorRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    quadratic_section_coefficients: Quad
    slope_one_line_intercept: int
    residual_coefficients: Quad
    residual_roots: tuple[int, ...]
    slope_one_shadow_roots: tuple[int, ...]
    selected_points: tuple[LineResidualPoint, LineResidualPoint, LineResidualPoint]
    selected_on_line_rows: tuple[int, ...]
    selected_off_line_rows: tuple[int, ...]
    residual_roots_match_slope_one_chord: bool
    exactly_two_selected_points_on_line: bool
    off_line_point_is_nonroot_control: bool


@dataclass(frozen=True)
class SlopeLineFactorProfile:
    row_count: int
    rows: tuple[SlopeLineFactorRow, ...]
    all_residual_roots_match_slope_one_chords: bool
    all_rows_have_exactly_two_selected_points_on_line: bool
    all_off_line_points_are_nonroot_controls: bool
    line_intercepts_by_orientation_mask: tuple[tuple[int, int], ...]


def residual_coefficients(quadratic: Quad, intercept: int) -> Quad:
    a_value, b_value, c_value = quadratic
    return a_value, (b_value - 1) % C_LOW_ORDER, (c_value - intercept) % C_LOW_ORDER


def roots(quadratic: Quad) -> tuple[int, ...]:
    return tuple(
        value
        for value in range(C_LOW_ORDER)
        if quadratic_value(quadratic, value) == 0
    )


def line_residual(fiber: int, c13_shadow: int, intercept: int) -> int:
    return (fiber - c13_shadow - intercept) % C_LOW_ORDER


def slope_line_factor_profile() -> SlopeLineFactorProfile:
    fiber_rows = corner_fiber_section_profile().rows
    chord_rows = slope_one_chord_profile().rows
    rows: list[SlopeLineFactorRow] = []
    for fiber_row, chord_row in zip(fiber_rows, chord_rows):
        slope_one_edges = tuple(
            edge for row_edge in chord_row.edges for edge in (row_edge,) if edge.is_slope_one
        )
        intercepts = {
            (edge.from_low_fiber[1] - edge.from_low_fiber[0]) % C_LOW_ORDER
            for edge in slope_one_edges
        } | {
            (edge.to_low_fiber[1] - edge.to_low_fiber[0]) % C_LOW_ORDER
            for edge in slope_one_edges
        }
        if len(intercepts) != 1:
            raise AssertionError(f"slope-one chord endpoints do not lie on one line: {intercepts}")
        intercept = next(iter(intercepts))
        slope_one_roots = tuple(
            sorted(
                {
                    edge.from_low_fiber[0]
                    for edge in slope_one_edges
                } | {
                    edge.to_low_fiber[0]
                    for edge in slope_one_edges
                }
            )
        )
        residual = residual_coefficients(fiber_row.quadratic_section_coefficients, intercept)
        residual_roots = roots(residual)
        selected: list[LineResidualPoint] = []
        for source_row, c_value in enumerate(fiber_row.row_values_c169):
            c13_shadow = c_value % C_LOW_ORDER
            fiber = c_value // C_LOW_ORDER
            value = line_residual(fiber, c13_shadow, intercept)
            selected.append(
                LineResidualPoint(
                    source_row=source_row,
                    c13_shadow=c13_shadow,
                    fiber=fiber,
                    line_residual=value,
                    lies_on_slope_one_line=value == 0,
                )
            )
        on_rows = tuple(point.source_row for point in selected if point.lies_on_slope_one_line)
        off_rows = tuple(point.source_row for point in selected if not point.lies_on_slope_one_line)
        rows.append(
            SlopeLineFactorRow(
                orientation_mask=chord_row.orientation_mask,
                recorded_direction_q=chord_row.recorded_direction_q,
                chain_coefficient=chord_row.chain_coefficient,
                quadratic_section_coefficients=fiber_row.quadratic_section_coefficients,
                slope_one_line_intercept=intercept,
                residual_coefficients=residual,
                residual_roots=residual_roots,
                slope_one_shadow_roots=slope_one_roots,
                selected_points=tuple(selected),  # type: ignore[arg-type]
                selected_on_line_rows=on_rows,
                selected_off_line_rows=off_rows,
                residual_roots_match_slope_one_chord=residual_roots == slope_one_roots,
                exactly_two_selected_points_on_line=len(on_rows) == 2,
                off_line_point_is_nonroot_control=(
                    len(off_rows) == 1
                    and selected[off_rows[0]].c13_shadow not in residual_roots
                    and selected[off_rows[0]].line_residual != 0
                ),
            )
        )
    rows_tuple = tuple(rows)
    intercepts_by_mask = tuple(
        sorted({(row.orientation_mask, row.slope_one_line_intercept) for row in rows_tuple})
    )
    return SlopeLineFactorProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_residual_roots_match_slope_one_chords=all(
            row.residual_roots_match_slope_one_chord for row in rows_tuple
        ),
        all_rows_have_exactly_two_selected_points_on_line=all(
            row.exactly_two_selected_points_on_line for row in rows_tuple
        ),
        all_off_line_points_are_nonroot_controls=all(
            row.off_line_point_is_nonroot_control for row in rows_tuple
        ),
        line_intercepts_by_orientation_mask=intercepts_by_mask,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner slope-line factor gate")
    profile = slope_line_factor_profile()
    expected_rows = (
        SlopeLineFactorRow(
            1, 197, -1, (1, 10, 0), 10, (1, 9, 3), (1, 3), (1, 3),
            (
                LineResidualPoint(0, 0, 0, 3, False),
                LineResidualPoint(1, 3, 0, 0, True),
                LineResidualPoint(2, 1, 11, 0, True),
            ),
            (1, 2), (0,), True, True, True,
        ),
        SlopeLineFactorRow(
            1, 310, 1, (1, 6, 12), 10, (1, 5, 2), (3, 5), (3, 5),
            (
                LineResidualPoint(0, 5, 2, 0, True),
                LineResidualPoint(1, 3, 0, 0, True),
                LineResidualPoint(2, 2, 2, 3, False),
            ),
            (0, 1), (2,), True, True, True,
        ),
        SlopeLineFactorRow(
            6, 197, -1, (12, 6, 0), 2, (12, 5, 11), (8, 10), (8, 10),
            (
                LineResidualPoint(0, 8, 10, 0, True),
                LineResidualPoint(1, 11, 10, 10, False),
                LineResidualPoint(2, 10, 12, 0, True),
            ),
            (0, 2), (1,), True, True, True,
        ),
        SlopeLineFactorRow(
            6, 310, 1, (8, 7, 0), 2, (8, 6, 11), (10, 12), (10, 12),
            (
                LineResidualPoint(0, 0, 0, 11, False),
                LineResidualPoint(1, 12, 1, 0, True),
                LineResidualPoint(2, 10, 12, 0, True),
            ),
            (1, 2), (0,), True, True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_residual_roots_match_slope_one_chords
        and profile.all_rows_have_exactly_two_selected_points_on_line
        and profile.all_off_line_points_are_nonroot_controls
        and profile.line_intercepts_by_orientation_mask == ((1, 10), (6, 2))
    )

    print(
        "corner_slope_line_factor_summary: "
        f"line_intercepts_by_orientation_mask={profile.line_intercepts_by_orientation_mask} "
        f"residual_roots={tuple(row.residual_roots for row in profile.rows)} "
        f"selected_on_line_rows={tuple(row.selected_on_line_rows for row in profile.rows)}"
    )
    print("corner_slope_line_factor_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("slope_line_factor_laws")
    print("  subtracting the slope-one line f=c0+s gives a quadratic residual")
    print("  residual roots are exactly the C13 shadows of the half-bridge endpoints")
    print("  the remaining selected row point is an explicit off-line control")
    print("interpretation")
    print("  half_bridge_edge_is_a_line_intersection_of_the_active_quadratic_fiber_section=1")
    print("  producer_can_target_a_factored_quadratic_minus_line_before_edge_orientation=1")
    print("  slope_one_chord_selector_is_equivalent_to_the_two_roots_of_this_residual=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

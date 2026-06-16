#!/usr/bin/env python3
"""Two-sign row triangle law for the p25 Hilbert-90 corner.

The unit-quadratic gate forces the whole line-subtracted residual from the
primitive unit sign eps and branch coefficient a.  This gate checks that those
same signs also force the row-labeled active triangle, including the selected
off-line control point.

In signed F_13 coordinates:

    cancellation = (3*eps, (eps - 1)/2)
    neighbor     = cancellation + 2*a*(1, 1)
    off_line_x   = eps + a

The off-line fiber is obtained from the same two-sign residual:

    off_line_y = off_line_x + s + R_{eps,a}(off_line_x)

The source rows are also forced:

    cancel_row  = (3 - eps)/2
    neighbor_row = cancel_row - a  (mod 3)
    off_row      = cancel_row + a  (mod 3)

Thus a producer cannot recover only the roots or scalar; it must place the
third point in the correct source row.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_gate import (
    LineResidualPoint,
    slope_line_factor_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_quadratic_gate import (
    MODULUS,
    UnitQuadraticRow,
    mod13,
    residual_scalar,
    unit_quadratic_profile,
)


LowFiber = tuple[int, int]
ResidualsByRow = tuple[int, int, int]
PointsByRow = tuple[LowFiber, LowFiber, LowFiber]


@dataclass(frozen=True)
class UnitTriangleRow:
    orientation_mask: int
    recorded_direction_q: int
    primitive_unit_sign: int
    branch_coefficient: int
    cancellation_source_row: int
    neighbor_source_row: int
    off_line_source_row: int
    cancellation_low_fiber: LowFiber
    neighbor_low_fiber: LowFiber
    off_line_low_fiber: LowFiber
    off_line_residual: int
    expected_points_by_source_row: PointsByRow
    actual_points_by_source_row: PointsByRow
    expected_line_residuals_by_source_row: ResidualsByRow
    actual_line_residuals_by_source_row: ResidualsByRow
    source_rows_forced_by_unit_sign_and_branch: bool
    points_forced_by_unit_sign_and_branch: bool
    line_residuals_forced_by_unit_sign_and_branch: bool


@dataclass(frozen=True)
class UnitTriangleProfile:
    row_count: int
    rows: tuple[UnitTriangleRow, ...]
    all_source_rows_forced_by_unit_sign_and_branch: bool
    all_points_forced_by_unit_sign_and_branch: bool
    all_line_residuals_forced_by_unit_sign_and_branch: bool
    off_line_rows_by_unit_sign_and_branch: tuple[tuple[int, int, int], ...]
    off_line_points_by_unit_sign_and_branch: tuple[tuple[int, int, LowFiber], ...]


def line_residual_at(unit_row: UnitQuadraticRow, x_value: int) -> int:
    scalar = residual_scalar(unit_row.primitive_unit_sign, unit_row.branch_coefficient)
    return mod13(
        scalar
        * (x_value - unit_row.signed_cancellation_x)
        * (x_value - unit_row.signed_neighbor_x)
    )


def line_value(unit_row: UnitQuadraticRow, x_value: int) -> int:
    return mod13(x_value + unit_row.signed_line_intercept)


def actual_points_by_row(points: tuple[LineResidualPoint, ...]) -> PointsByRow:
    by_row = {
        point.source_row: (point.c13_shadow, point.fiber)
        for point in points
    }
    return by_row[0], by_row[1], by_row[2]


def actual_residuals_by_row(points: tuple[LineResidualPoint, ...]) -> ResidualsByRow:
    by_row = {
        point.source_row: point.line_residual
        for point in points
    }
    return by_row[0], by_row[1], by_row[2]


def expected_triangle_row(unit_row: UnitQuadraticRow) -> tuple[int, int, int, LowFiber, LowFiber, LowFiber, int, PointsByRow, ResidualsByRow]:
    eps = unit_row.primitive_unit_sign
    branch = unit_row.branch_coefficient
    cancel_row = (3 - eps) // 2
    neighbor_row = (cancel_row - branch) % 3
    off_row = (cancel_row + branch) % 3

    cancellation = (
        mod13(unit_row.signed_cancellation_x),
        mod13((eps - 1) // 2),
    )
    neighbor = (
        mod13(unit_row.signed_neighbor_x),
        line_value(unit_row, unit_row.signed_neighbor_x),
    )
    off_x = eps + branch
    off_residual = line_residual_at(unit_row, off_x)
    off_point = (
        mod13(off_x),
        mod13(line_value(unit_row, off_x) + off_residual),
    )

    points: list[LowFiber | None] = [None, None, None]
    residuals: list[int | None] = [None, None, None]
    points[cancel_row] = cancellation
    points[neighbor_row] = neighbor
    points[off_row] = off_point
    residuals[cancel_row] = 0
    residuals[neighbor_row] = 0
    residuals[off_row] = off_residual
    if any(point is None for point in points) or any(value is None for value in residuals):
        raise AssertionError("unit signs did not assign all source rows")
    return (
        cancel_row,
        neighbor_row,
        off_row,
        cancellation,
        neighbor,
        off_point,
        off_residual,
        tuple(points),  # type: ignore[arg-type]
        tuple(residuals),  # type: ignore[arg-type]
    )


def unit_triangle_profile() -> UnitTriangleProfile:
    unit_rows = unit_quadratic_profile().rows
    factor_rows = slope_line_factor_profile().rows
    rows: list[UnitTriangleRow] = []
    for unit_row, factor_row in zip(unit_rows, factor_rows):
        (
            cancel_row,
            neighbor_row,
            off_row,
            cancellation,
            neighbor,
            off_point,
            off_residual,
            expected_points,
            expected_residuals,
        ) = expected_triangle_row(unit_row)
        actual_points = actual_points_by_row(factor_row.selected_points)
        actual_residuals = actual_residuals_by_row(factor_row.selected_points)
        rows.append(
            UnitTriangleRow(
                orientation_mask=unit_row.orientation_mask,
                recorded_direction_q=unit_row.recorded_direction_q,
                primitive_unit_sign=unit_row.primitive_unit_sign,
                branch_coefficient=unit_row.branch_coefficient,
                cancellation_source_row=cancel_row,
                neighbor_source_row=neighbor_row,
                off_line_source_row=off_row,
                cancellation_low_fiber=cancellation,
                neighbor_low_fiber=neighbor,
                off_line_low_fiber=off_point,
                off_line_residual=off_residual,
                expected_points_by_source_row=expected_points,
                actual_points_by_source_row=actual_points,
                expected_line_residuals_by_source_row=expected_residuals,
                actual_line_residuals_by_source_row=actual_residuals,
                source_rows_forced_by_unit_sign_and_branch=(
                    tuple(sorted((cancel_row, neighbor_row, off_row))) == (0, 1, 2)
                ),
                points_forced_by_unit_sign_and_branch=actual_points == expected_points,
                line_residuals_forced_by_unit_sign_and_branch=actual_residuals == expected_residuals,
            )
        )
    rows_tuple = tuple(rows)
    off_rows = tuple(sorted({
        (row.primitive_unit_sign, row.branch_coefficient, row.off_line_source_row)
        for row in rows_tuple
    }))
    off_points = tuple(sorted({
        (row.primitive_unit_sign, row.branch_coefficient, row.off_line_low_fiber)
        for row in rows_tuple
    }))
    return UnitTriangleProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_source_rows_forced_by_unit_sign_and_branch=all(
            row.source_rows_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        all_points_forced_by_unit_sign_and_branch=all(
            row.points_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        all_line_residuals_forced_by_unit_sign_and_branch=all(
            row.line_residuals_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        off_line_rows_by_unit_sign_and_branch=off_rows,
        off_line_points_by_unit_sign_and_branch=off_points,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner unit-triangle gate")
    profile = unit_triangle_profile()
    expected_rows = (
        UnitTriangleRow(
            1, 197, 1, -1, 1, 2, 0, (3, 0), (1, 11), (0, 0), 3,
            ((0, 0), (3, 0), (1, 11)), ((0, 0), (3, 0), (1, 11)),
            (3, 0, 0), (3, 0, 0), True, True, True,
        ),
        UnitTriangleRow(
            1, 310, 1, 1, 1, 0, 2, (3, 0), (5, 2), (2, 2), 3,
            ((5, 2), (3, 0), (2, 2)), ((5, 2), (3, 0), (2, 2)),
            (0, 0, 3), (0, 0, 3), True, True, True,
        ),
        UnitTriangleRow(
            6, 197, -1, -1, 2, 0, 1, (10, 12), (8, 10), (11, 10), 10,
            ((8, 10), (11, 10), (10, 12)), ((8, 10), (11, 10), (10, 12)),
            (0, 10, 0), (0, 10, 0), True, True, True,
        ),
        UnitTriangleRow(
            6, 310, -1, 1, 2, 1, 0, (10, 12), (12, 1), (0, 0), 11,
            ((0, 0), (12, 1), (10, 12)), ((0, 0), (12, 1), (10, 12)),
            (11, 0, 0), (11, 0, 0), True, True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_source_rows_forced_by_unit_sign_and_branch
        and profile.all_points_forced_by_unit_sign_and_branch
        and profile.all_line_residuals_forced_by_unit_sign_and_branch
        and profile.off_line_rows_by_unit_sign_and_branch == (
            (-1, -1, 1),
            (-1, 1, 0),
            (1, -1, 0),
            (1, 1, 2),
        )
        and profile.off_line_points_by_unit_sign_and_branch == (
            (-1, -1, (11, 10)),
            (-1, 1, (0, 0)),
            (1, -1, (0, 0)),
            (1, 1, (2, 2)),
        )
    )

    print(
        "corner_unit_triangle_summary: "
        f"off_line_rows_by_unit_sign_and_branch={profile.off_line_rows_by_unit_sign_and_branch} "
        f"off_line_points_by_unit_sign_and_branch={profile.off_line_points_by_unit_sign_and_branch} "
        f"points_by_row={tuple(row.actual_points_by_source_row for row in profile.rows)}"
    )
    print("corner_unit_triangle_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("unit_triangle_laws")
    print("  cancel_row=(3-eps)/2, neighbor_row=cancel_row-a, off_row=cancel_row+a mod 3")
    print("  off_line_x=eps+a and off_line_y=off_line_x+s+R_eps,a(off_line_x)")
    print("  the roots and off-line control point fill exactly one point in each source row")
    print("interpretation")
    print("  active_row_labeled_triangle_is_forced_by_unit_sign_and_branch=1")
    print("  producer_must_place_the_off_line_control_in_the_correct_source_row=1")
    print("  roots_scalar_and_third_point_are_not_independent_choices=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

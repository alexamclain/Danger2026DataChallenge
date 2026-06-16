#!/usr/bin/env python3
"""Unit-fiber law for the p25 Hilbert-90 cancellation corner.

The cancellation-line gate shows that the slope-one line is forced by the
Hilbert-90 cancellation vertex.  This gate removes one more degree of freedom:
the low/fiber coordinates of that vertex and its coefficient-selected neighbor
are already determined by two signs.

Let eps be the primitive D-coordinate sign of the cancellation unit vertex:

    eps = +1 for q=172, eps = -1 for q=335.

Let a be the chain coefficient, so a=-1 on the q=197 branch and a=+1 on the
q=310 branch.  In signed F_13 low/fiber coordinates the whole local line model
is:

    cancellation = (3*eps, (eps - 1)/2)
    intercept    = fiber - low
    neighbor     = cancellation + 2*a*(1, 1)
    tangent      = -2*a*(1, 1)

Thus a producer can target a primitive unit vertex plus branch sign, rather
than separately fitting the line, residual roots, and tangent.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_cancellation_line_gate import (
    LowFiber,
    cancellation_line_profile,
    signed_mod,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate import (
    N,
    d_residue_from_q,
)


SignedFiber = tuple[int, int]


@dataclass(frozen=True)
class UnitFiberRow:
    orientation_mask: int
    recorded_direction_q: int
    chain_coefficient: int
    cancellation_vertex_q: int
    cancellation_vertex_d: int
    primitive_unit_sign: int
    cancellation_low_fiber: LowFiber
    signed_cancellation_low_fiber: SignedFiber
    expected_signed_cancellation_low_fiber: SignedFiber
    slope_one_line_intercept: int
    signed_intercept: int
    expected_signed_intercept: int
    coefficient_neighbor_low_fiber: LowFiber
    signed_coefficient_neighbor_low_fiber: SignedFiber
    expected_signed_coefficient_neighbor_low_fiber: SignedFiber
    recorded_signed_tangent: SignedFiber
    expected_recorded_signed_tangent: SignedFiber
    coefficient_weighted_recorded_tangent: SignedFiber
    unit_vertex_forces_cancellation_low_fiber: bool
    unit_vertex_forces_line_intercept: bool
    branch_coefficient_forces_neighbor: bool
    branch_coefficient_forces_recorded_tangent: bool


@dataclass(frozen=True)
class UnitFiberProfile:
    row_count: int
    rows: tuple[UnitFiberRow, ...]
    all_cancellation_vertices_are_primitive_units: bool
    all_unit_vertices_force_cancellation_low_fiber: bool
    all_unit_vertices_force_line_intercept: bool
    all_branch_coefficients_force_neighbors: bool
    all_branch_coefficients_force_recorded_tangents: bool
    all_weighted_tangents_are_negative_diagonal: bool
    unit_signs_by_orientation_mask: tuple[tuple[int, int], ...]
    branch_coefficients_by_recorded_direction_q: tuple[tuple[int, int], ...]


def signed_pair(pair: LowFiber) -> SignedFiber:
    return signed_mod(pair[0]), signed_mod(pair[1])


def unit_sign_from_d(d_value: int) -> int:
    if d_value % N == 1:
        return 1
    if d_value % N == N - 1:
        return -1
    return 0


def expected_cancellation(unit_sign: int) -> SignedFiber:
    # The numerator is always even for unit_sign in {+1, -1}.
    return 3 * unit_sign, (unit_sign - 1) // 2


def expected_neighbor(cancellation: SignedFiber, coefficient: int) -> SignedFiber:
    return cancellation[0] + 2 * coefficient, cancellation[1] + 2 * coefficient


def unit_fiber_profile() -> UnitFiberProfile:
    rows: list[UnitFiberRow] = []
    for cancellation_row in cancellation_line_profile().rows:
        d_value = d_residue_from_q(cancellation_row.cancellation_vertex_q)
        unit_sign = unit_sign_from_d(d_value)
        expected_cancel = expected_cancellation(unit_sign)
        expected_intercept = expected_cancel[1] - expected_cancel[0]
        expected_neighbor_pair = expected_neighbor(expected_cancel, cancellation_row.chain_coefficient)
        expected_tangent = (
            -2 * cancellation_row.chain_coefficient,
            -2 * cancellation_row.chain_coefficient,
        )
        signed_cancel = signed_pair(cancellation_row.cancellation_low_fiber)
        signed_neighbor = signed_pair(cancellation_row.coefficient_neighbor_low_fiber)
        signed_intercept = signed_mod(cancellation_row.slope_one_line_intercept)
        rows.append(
            UnitFiberRow(
                orientation_mask=cancellation_row.orientation_mask,
                recorded_direction_q=cancellation_row.recorded_direction_q,
                chain_coefficient=cancellation_row.chain_coefficient,
                cancellation_vertex_q=cancellation_row.cancellation_vertex_q,
                cancellation_vertex_d=d_value,
                primitive_unit_sign=unit_sign,
                cancellation_low_fiber=cancellation_row.cancellation_low_fiber,
                signed_cancellation_low_fiber=signed_cancel,
                expected_signed_cancellation_low_fiber=expected_cancel,
                slope_one_line_intercept=cancellation_row.slope_one_line_intercept,
                signed_intercept=signed_intercept,
                expected_signed_intercept=expected_intercept,
                coefficient_neighbor_low_fiber=cancellation_row.coefficient_neighbor_low_fiber,
                signed_coefficient_neighbor_low_fiber=signed_neighbor,
                expected_signed_coefficient_neighbor_low_fiber=expected_neighbor_pair,
                recorded_signed_tangent=cancellation_row.recorded_signed_tangent,
                expected_recorded_signed_tangent=expected_tangent,
                coefficient_weighted_recorded_tangent=cancellation_row.coefficient_weighted_recorded_tangent,
                unit_vertex_forces_cancellation_low_fiber=signed_cancel == expected_cancel,
                unit_vertex_forces_line_intercept=signed_intercept == expected_intercept,
                branch_coefficient_forces_neighbor=signed_neighbor == expected_neighbor_pair,
                branch_coefficient_forces_recorded_tangent=(
                    cancellation_row.recorded_signed_tangent == expected_tangent
                ),
            )
        )
    rows_tuple = tuple(rows)
    unit_signs = tuple(sorted({
        (row.orientation_mask, row.primitive_unit_sign)
        for row in rows_tuple
    }))
    coefficients = tuple(sorted({
        (row.recorded_direction_q, row.chain_coefficient)
        for row in rows_tuple
    }))
    return UnitFiberProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_cancellation_vertices_are_primitive_units=all(
            row.primitive_unit_sign in (-1, 1) for row in rows_tuple
        ),
        all_unit_vertices_force_cancellation_low_fiber=all(
            row.unit_vertex_forces_cancellation_low_fiber for row in rows_tuple
        ),
        all_unit_vertices_force_line_intercept=all(
            row.unit_vertex_forces_line_intercept for row in rows_tuple
        ),
        all_branch_coefficients_force_neighbors=all(
            row.branch_coefficient_forces_neighbor for row in rows_tuple
        ),
        all_branch_coefficients_force_recorded_tangents=all(
            row.branch_coefficient_forces_recorded_tangent for row in rows_tuple
        ),
        all_weighted_tangents_are_negative_diagonal=all(
            row.coefficient_weighted_recorded_tangent == (-2, -2)
            for row in rows_tuple
        ),
        unit_signs_by_orientation_mask=unit_signs,
        branch_coefficients_by_recorded_direction_q=coefficients,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner unit-fiber gate")
    profile = unit_fiber_profile()
    expected_rows = (
        UnitFiberRow(
            1, 197, -1, 172, 1, 1, (3, 0), (3, 0), (3, 0), 10, -3, -3,
            (1, 11), (1, -2), (1, -2), (2, 2), (2, 2), (-2, -2),
            True, True, True, True,
        ),
        UnitFiberRow(
            1, 310, 1, 172, 1, 1, (3, 0), (3, 0), (3, 0), 10, -3, -3,
            (5, 2), (5, 2), (5, 2), (-2, -2), (-2, -2), (-2, -2),
            True, True, True, True,
        ),
        UnitFiberRow(
            6, 197, -1, 335, 506, -1, (10, 12), (-3, -1), (-3, -1), 2, 2, 2,
            (8, 10), (-5, -3), (-5, -3), (2, 2), (2, 2), (-2, -2),
            True, True, True, True,
        ),
        UnitFiberRow(
            6, 310, 1, 335, 506, -1, (10, 12), (-3, -1), (-3, -1), 2, 2, 2,
            (12, 1), (-1, 1), (-1, 1), (-2, -2), (-2, -2), (-2, -2),
            True, True, True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_cancellation_vertices_are_primitive_units
        and profile.all_unit_vertices_force_cancellation_low_fiber
        and profile.all_unit_vertices_force_line_intercept
        and profile.all_branch_coefficients_force_neighbors
        and profile.all_branch_coefficients_force_recorded_tangents
        and profile.all_weighted_tangents_are_negative_diagonal
        and profile.unit_signs_by_orientation_mask == ((1, 1), (6, -1))
        and profile.branch_coefficients_by_recorded_direction_q == ((197, -1), (310, 1))
    )

    print(
        "corner_unit_fiber_summary: "
        f"unit_signs_by_orientation_mask={profile.unit_signs_by_orientation_mask} "
        f"branch_coefficients_by_recorded_direction_q={profile.branch_coefficients_by_recorded_direction_q} "
        f"signed_cancellations={tuple(row.signed_cancellation_low_fiber for row in profile.rows)} "
        f"signed_neighbors={tuple(row.signed_coefficient_neighbor_low_fiber for row in profile.rows)}"
    )
    print("corner_unit_fiber_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("unit_fiber_laws")
    print("  primitive D-unit sign eps forces cancellation=(3*eps,(eps-1)/2)")
    print("  line intercept is fiber-low from that unit vertex")
    print("  branch coefficient a forces neighbor=cancellation+2*a*(1,1)")
    print("  recorded tangent is -2*a*(1,1), so coefficient-weighted tangent is (-2,-2)")
    print("interpretation")
    print("  cancellation_line_law_reduces_to_unit_sign_plus_branch_coefficient=1")
    print("  producer_can_target_the_primitive_unit_vertex_before_line_fitting=1")
    print("  separate_neighbor_or_tangent_choices_are_rejected=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_unit_fiber_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_fiber_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

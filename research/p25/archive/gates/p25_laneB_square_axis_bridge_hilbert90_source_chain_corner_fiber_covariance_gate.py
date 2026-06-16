#!/usr/bin/env python3
"""Covariance of the p25 Hilbert-90 corner fiber section.

The fiber-section gate showed that each active half-bridge corner uses a unit
quadratic section over its C_13 shadow.  This gate checks that the four
quadratics are not four unrelated interpolations: they are the selected-support
images of the canonical section under the actual product-affine source maps on
C_3 x C_169.

The C_169 carry matters.  Two reversal-side maps need the nonsplit carry term
in c = c0 + 13*f; dropping it gives the wrong selected fibers.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate import (
    C_LOW_ORDER,
    C_ORDER,
    CornerFiberSectionRow,
    corner_fiber_section_profile,
    quadratic_coefficients,
    quadratic_value,
)


AffineMap = tuple[int, int, int, int]
FiberPair = tuple[int, int]


@dataclass(frozen=True)
class FiberCovarianceRow:
    orientation_mask: int
    boundary_direction_q: int
    source_affine_map: AffineMap
    target_chain_q_values: tuple[int, ...]
    transformed_chain_q_values: tuple[int, ...]
    transformed_low_fiber_pairs: tuple[FiberPair, ...]
    target_low_fiber_pairs: tuple[FiberPair, ...]
    carry_values_on_selected_shadow: tuple[int, int, int]
    no_carry_low_fiber_pairs: tuple[FiberPair, ...]
    no_carry_matches_target: bool
    transformed_quadratic_coefficients: tuple[int, int, int]
    target_quadratic_coefficients: tuple[int, int, int]
    transformed_matches_target: bool


@dataclass(frozen=True)
class FiberCovarianceProfile:
    row_count: int
    rows: tuple[FiberCovarianceRow, ...]
    all_rows_are_source_affine_images: bool
    all_quadratic_sections_transport_correctly: bool
    nonsplit_carry_needed_row_count: int
    no_carry_success_row_count: int
    canonical_source_section: tuple[FiberPair, ...]
    canonical_quadratic_section: tuple[int, int, int]


def split_c(value: int) -> FiberPair:
    return value % C_LOW_ORDER, value // C_LOW_ORDER


def q_from_coord(right: int, c_value: int) -> int:
    c_value %= C_ORDER
    lift = (right - c_value) % 3
    return c_value + C_ORDER * lift


def selected_pairs(row: CornerFiberSectionRow) -> tuple[FiberPair, ...]:
    return tuple(sorted(zip(row.c13_shadow_values, row.fiber_values)))


def transform_point(q_value: int, section_pair: FiberPair, affine_map: AffineMap) -> tuple[int, FiberPair, int, FiberPair]:
    alpha, beta, unit, shift = affine_map
    right = q_value % 3
    low, fiber = section_pair
    unit_low = unit % C_LOW_ORDER
    unit_fiber = ((unit - unit_low) // C_LOW_ORDER) % C_LOW_ORDER
    shift_low = shift % C_LOW_ORDER
    shift_fiber = ((shift - shift_low) // C_LOW_ORDER) % C_LOW_ORDER
    total_low = unit_low * low + shift_low
    carry = total_low // C_LOW_ORDER
    new_low = total_low % C_LOW_ORDER
    new_fiber = (unit_low * fiber + unit_fiber * low + shift_fiber + carry) % C_LOW_ORDER
    no_carry_fiber = (unit_low * fiber + unit_fiber * low + shift_fiber) % C_LOW_ORDER
    new_right = (alpha * right + beta) % 3
    new_q = q_from_coord(new_right, new_low + C_LOW_ORDER * new_fiber)
    return new_q, (new_low, new_fiber), carry, (new_low, no_carry_fiber)


def covariance_row(
    canonical: CornerFiberSectionRow,
    target: CornerFiberSectionRow,
    affine_map: AffineMap,
) -> FiberCovarianceRow:
    transformed = tuple(
        transform_point(q_value, pair, affine_map)
        for q_value, pair in zip(
            canonical.chain_q_values,
            zip(canonical.c13_shadow_values, canonical.fiber_values),
        )
    )
    transformed_pairs = tuple(sorted(item[1] for item in transformed))
    no_carry_pairs = tuple(sorted(item[3] for item in transformed))
    transformed_coefficients = quadratic_coefficients(
        tuple(item[0] for item in transformed_pairs),
        tuple(item[1] for item in transformed_pairs),
    )
    target_pairs = selected_pairs(target)
    return FiberCovarianceRow(
        orientation_mask=target.orientation_mask,
        boundary_direction_q=target.boundary_direction_q,
        source_affine_map=affine_map,
        target_chain_q_values=target.chain_q_values,
        transformed_chain_q_values=tuple(sorted(item[0] for item in transformed)),
        transformed_low_fiber_pairs=transformed_pairs,
        target_low_fiber_pairs=target_pairs,
        carry_values_on_selected_shadow=tuple(item[2] for item in transformed),  # type: ignore[return-value]
        no_carry_low_fiber_pairs=no_carry_pairs,
        no_carry_matches_target=no_carry_pairs == target_pairs,
        transformed_quadratic_coefficients=transformed_coefficients,
        target_quadratic_coefficients=target.quadratic_section_coefficients,
        transformed_matches_target=(
            tuple(sorted(item[0] for item in transformed)) == target.chain_q_values
            and transformed_pairs == target_pairs
            and transformed_coefficients == target.quadratic_section_coefficients
        ),
    )


def fiber_covariance_profile() -> FiberCovarianceProfile:
    rows = corner_fiber_section_profile().rows
    canonical = rows[0]
    # These are the product-affine maps from the source-chain curvature gate,
    # sending the canonical active support to the four active corner supports.
    source_affine_maps = (
        (1, 0, 1, 0),
        (1, 2, 1, 28),
        (2, 1, 168, 141),
        (2, 0, 168, 0),
    )
    covariance_rows = tuple(
        covariance_row(canonical, target, affine_map)
        for target, affine_map in zip(rows, source_affine_maps)
    )
    return FiberCovarianceProfile(
        row_count=len(covariance_rows),
        rows=covariance_rows,
        all_rows_are_source_affine_images=all(
            row.transformed_chain_q_values == row.target_chain_q_values
            and row.transformed_low_fiber_pairs == row.target_low_fiber_pairs
            for row in covariance_rows
        ),
        all_quadratic_sections_transport_correctly=all(
            row.transformed_quadratic_coefficients == row.target_quadratic_coefficients
            and all(
                quadratic_value(row.transformed_quadratic_coefficients, low) == fiber
                for low, fiber in row.target_low_fiber_pairs
            )
            for row in covariance_rows
        ),
        nonsplit_carry_needed_row_count=sum(not row.no_carry_matches_target for row in covariance_rows),
        no_carry_success_row_count=sum(row.no_carry_matches_target for row in covariance_rows),
        canonical_source_section=tuple(zip(canonical.c13_shadow_values, canonical.fiber_values)),
        canonical_quadratic_section=canonical.quadratic_section_coefficients,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner fiber-covariance gate")
    profile = fiber_covariance_profile()
    expected_rows = (
        FiberCovarianceRow(1, 197, (1, 0, 1, 0), (0, 172, 482), (0, 172, 482), ((0, 0), (1, 11), (3, 0)), ((0, 0), (1, 11), (3, 0)), (0, 0, 0), ((0, 0), (1, 11), (3, 0)), True, (1, 10, 0), (1, 10, 0), True),
        FiberCovarianceRow(1, 310, (1, 2, 1, 28), (172, 197, 369), (172, 197, 369), ((2, 2), (3, 0), (5, 2)), ((2, 2), (3, 0), (5, 2)), (0, 0, 0), ((2, 2), (3, 0), (5, 2)), True, (1, 6, 12), (1, 6, 12), True),
        FiberCovarianceRow(6, 197, (2, 1, 168, 141), (138, 310, 335), (138, 310, 335), ((8, 10), (10, 12), (11, 10)), ((8, 10), (10, 12), (11, 10)), (0, 3, 1), ((8, 7), (10, 11), (11, 10)), False, (12, 6, 0), (12, 6, 0), True),
        FiberCovarianceRow(6, 310, (2, 0, 168, 0), (0, 25, 335), (0, 25, 335), ((0, 0), (10, 12), (12, 1)), ((0, 0), (10, 12), (12, 1)), (0, 2, 0), ((0, 0), (10, 10), (12, 1)), False, (8, 7, 0), (8, 7, 0), True),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_rows_are_source_affine_images
        and profile.all_quadratic_sections_transport_correctly
        and profile.nonsplit_carry_needed_row_count == 2
        and profile.no_carry_success_row_count == 2
        and profile.canonical_source_section == ((0, 0), (3, 0), (1, 11))
        and profile.canonical_quadratic_section == (1, 10, 0)
    )

    print(
        "corner_fiber_covariance_summary: "
        f"row_count={profile.row_count} "
        f"canonical_source_section={profile.canonical_source_section} "
        f"canonical_quadratic={profile.canonical_quadratic_section} "
        f"source_affine_images={int(profile.all_rows_are_source_affine_images)} "
        f"quadratics_transport={int(profile.all_quadratic_sections_transport_correctly)} "
        f"nonsplit_carry_needed_rows={profile.nonsplit_carry_needed_row_count} "
        f"no_carry_success_rows={profile.no_carry_success_row_count}"
    )
    print("corner_fiber_covariance_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("covariance_laws")
    print("  the four active fiber quadratics are selected-support source-affine images of the canonical section")
    print("  canonical section is f(c0)=c0*(c0-3) on shadow values (0,3,1)")
    print("  reversal-side source-affine maps require the nonsplit C169 carry term")
    print("interpretation")
    print("  active_quadratic_fiber_correction_is_one_covariant_object_not_four_unrelated_interpolations=1")
    print("  split_no_carry_C13xC13_fiber_transport_fails_on_two_active_corner_rows=1")
    print("  producer_must_realize_the_quadratic_section_with_the_actual_C169_carry_law=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_covariance_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

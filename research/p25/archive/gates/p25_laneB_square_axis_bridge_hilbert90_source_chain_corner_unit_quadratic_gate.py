#!/usr/bin/env python3
"""Two-sign quadratic residual law for the p25 Hilbert-90 corner.

The unit-fiber gate reduces the cancellation line to a primitive unit sign
eps and a branch coefficient a.  This gate checks that the entire quadratic
residual after subtracting that line is forced by the same two signs.

In signed F_13 coordinates, write:

    x_c = 3*eps
    y_c = (eps - 1)/2
    x_n = x_c + 2*a
    s   = y_c - x_c

Then the line-subtracted residual is:

    R_{eps,a}(x) = lambda_{eps,a} * (x - x_c) * (x - x_n)

with:

    lambda_{eps,a} = -1 + 2*eps - a + eps*a.

Adding the forced line back,

    f_{eps,a}(x) = x + s + R_{eps,a}(x),

recovers each active C_13-to-C_169 fiber quadratic.  Thus a producer target is
now a two-sign quadratic polynomial, not just a fitted line plus two roots.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_slope_line_factor_gate import (
    Quad,
    slope_line_factor_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_fiber_gate import (
    unit_fiber_profile,
)


MODULUS = 13


@dataclass(frozen=True)
class UnitQuadraticRow:
    orientation_mask: int
    recorded_direction_q: int
    primitive_unit_sign: int
    branch_coefficient: int
    signed_cancellation_x: int
    signed_neighbor_x: int
    signed_line_intercept: int
    residual_scalar_signed: int
    residual_scalar_mod13: int
    expected_residual_coefficients: Quad
    actual_residual_coefficients: Quad
    expected_quadratic_coefficients: Quad
    actual_quadratic_coefficients: Quad
    expected_residual_roots: tuple[int, ...]
    actual_residual_roots: tuple[int, ...]
    residual_polynomial_forced_by_unit_sign_and_branch: bool
    quadratic_section_forced_by_unit_sign_and_branch: bool
    residual_roots_forced_by_unit_sign_and_branch: bool


@dataclass(frozen=True)
class UnitQuadraticProfile:
    row_count: int
    rows: tuple[UnitQuadraticRow, ...]
    all_residual_polynomials_forced_by_unit_sign_and_branch: bool
    all_quadratic_sections_forced_by_unit_sign_and_branch: bool
    all_residual_roots_forced_by_unit_sign_and_branch: bool
    residual_scalars_by_unit_sign_and_branch: tuple[tuple[int, int, int], ...]


def mod13(value: int) -> int:
    return value % MODULUS


def signed_mod13(value: int) -> int:
    value %= MODULUS
    return value if value <= MODULUS // 2 else value - MODULUS


def residual_scalar(unit_sign: int, branch_coefficient: int) -> int:
    return -1 + 2 * unit_sign - branch_coefficient + unit_sign * branch_coefficient


def product_residual_coefficients(scalar: int, root_a: int, root_b: int) -> Quad:
    scalar_mod = mod13(scalar)
    root_a_mod = mod13(root_a)
    root_b_mod = mod13(root_b)
    return (
        scalar_mod,
        mod13(-scalar_mod * (root_a_mod + root_b_mod)),
        mod13(scalar_mod * root_a_mod * root_b_mod),
    )


def add_forced_line(residual: Quad, intercept: int) -> Quad:
    a_value, b_value, c_value = residual
    return a_value, mod13(b_value + 1), mod13(c_value + intercept)


def unit_quadratic_profile() -> UnitQuadraticProfile:
    unit_rows = unit_fiber_profile().rows
    factor_rows = slope_line_factor_profile().rows
    rows: list[UnitQuadraticRow] = []
    for unit_row, factor_row in zip(unit_rows, factor_rows):
        unit_sign = unit_row.primitive_unit_sign
        branch = unit_row.chain_coefficient
        cancellation_x = unit_row.signed_cancellation_low_fiber[0]
        neighbor_x = unit_row.signed_coefficient_neighbor_low_fiber[0]
        intercept = unit_row.signed_intercept
        scalar = residual_scalar(unit_sign, branch)
        expected_residual = product_residual_coefficients(scalar, cancellation_x, neighbor_x)
        expected_quadratic = add_forced_line(expected_residual, intercept)
        expected_roots = tuple(sorted((mod13(cancellation_x), mod13(neighbor_x))))
        rows.append(
            UnitQuadraticRow(
                orientation_mask=unit_row.orientation_mask,
                recorded_direction_q=unit_row.recorded_direction_q,
                primitive_unit_sign=unit_sign,
                branch_coefficient=branch,
                signed_cancellation_x=cancellation_x,
                signed_neighbor_x=neighbor_x,
                signed_line_intercept=intercept,
                residual_scalar_signed=signed_mod13(scalar),
                residual_scalar_mod13=mod13(scalar),
                expected_residual_coefficients=expected_residual,
                actual_residual_coefficients=factor_row.residual_coefficients,
                expected_quadratic_coefficients=expected_quadratic,
                actual_quadratic_coefficients=factor_row.quadratic_section_coefficients,
                expected_residual_roots=expected_roots,
                actual_residual_roots=factor_row.residual_roots,
                residual_polynomial_forced_by_unit_sign_and_branch=(
                    factor_row.residual_coefficients == expected_residual
                ),
                quadratic_section_forced_by_unit_sign_and_branch=(
                    factor_row.quadratic_section_coefficients == expected_quadratic
                ),
                residual_roots_forced_by_unit_sign_and_branch=(
                    factor_row.residual_roots == expected_roots
                ),
            )
        )
    rows_tuple = tuple(rows)
    scalars = tuple(sorted({
        (row.primitive_unit_sign, row.branch_coefficient, row.residual_scalar_signed)
        for row in rows_tuple
    }))
    return UnitQuadraticProfile(
        row_count=len(rows_tuple),
        rows=rows_tuple,
        all_residual_polynomials_forced_by_unit_sign_and_branch=all(
            row.residual_polynomial_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        all_quadratic_sections_forced_by_unit_sign_and_branch=all(
            row.quadratic_section_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        all_residual_roots_forced_by_unit_sign_and_branch=all(
            row.residual_roots_forced_by_unit_sign_and_branch for row in rows_tuple
        ),
        residual_scalars_by_unit_sign_and_branch=scalars,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner unit-quadratic gate")
    profile = unit_quadratic_profile()
    expected_rows = (
        UnitQuadraticRow(
            1, 197, 1, -1, 3, 1, -3, 1, 1,
            (1, 9, 3), (1, 9, 3), (1, 10, 0), (1, 10, 0),
            (1, 3), (1, 3), True, True, True,
        ),
        UnitQuadraticRow(
            1, 310, 1, 1, 3, 5, -3, 1, 1,
            (1, 5, 2), (1, 5, 2), (1, 6, 12), (1, 6, 12),
            (3, 5), (3, 5), True, True, True,
        ),
        UnitQuadraticRow(
            6, 197, -1, -1, -3, -5, 2, -1, 12,
            (12, 5, 11), (12, 5, 11), (12, 6, 0), (12, 6, 0),
            (8, 10), (8, 10), True, True, True,
        ),
        UnitQuadraticRow(
            6, 310, -1, 1, -3, -1, 2, -5, 8,
            (8, 6, 11), (8, 6, 11), (8, 7, 0), (8, 7, 0),
            (10, 12), (10, 12), True, True, True,
        ),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_residual_polynomials_forced_by_unit_sign_and_branch
        and profile.all_quadratic_sections_forced_by_unit_sign_and_branch
        and profile.all_residual_roots_forced_by_unit_sign_and_branch
        and profile.residual_scalars_by_unit_sign_and_branch == (
            (-1, -1, -1),
            (-1, 1, -5),
            (1, -1, 1),
            (1, 1, 1),
        )
    )

    print(
        "corner_unit_quadratic_summary: "
        f"residual_scalars_by_unit_sign_and_branch={profile.residual_scalars_by_unit_sign_and_branch} "
        f"residual_coefficients={tuple(row.actual_residual_coefficients for row in profile.rows)} "
        f"quadratic_coefficients={tuple(row.actual_quadratic_coefficients for row in profile.rows)}"
    )
    print("corner_unit_quadratic_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("unit_quadratic_laws")
    print("  R_eps,a(x)=lambda_eps,a*(x-3*eps)*(x-(3*eps+2*a))")
    print("  lambda_eps,a=-1+2*eps-a+eps*a")
    print("  f_eps,a(x)=x+((eps-1)/2-3*eps)+R_eps,a(x)")
    print("interpretation")
    print("  active_quadratic_fiber_section_is_forced_by_unit_sign_and_branch=1")
    print("  residual_roots_and_scalar_are_not_independent_choices=1")
    print("  producer_can_target_a_two_sign_quadratic_before_Hilbert90_image=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_unit_quadratic_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_quadratic_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

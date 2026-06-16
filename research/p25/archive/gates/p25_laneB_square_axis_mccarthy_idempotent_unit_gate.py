#!/usr/bin/env python3
"""Idempotent-unit structure of the powered McCarthy quotient.

After q-power projection and coefficient transport, the finite McCarthy target
is the point projector at q=138.  Equivalently, before subtracting and
normalizing, the powered quotient is the pointwise unit

    U(q) = 1 + (zeta_39^5 - 1) * e_138(q)

in the function algebra on C_507 over F_2029.

This gate records the exact algebraic structure:

* e_138 is an idempotent.
* U has pointwise order 39 and inverse
  `1 + (zeta_39^-5 - 1) * e_138`.
* `(U - 1)/(zeta_39^5 - 1) = e_138`.
* e_138, U-1, and U are Fourier-dense on C_507.

So the live route is theorem endpoint / point-delta production.  A candidate
that tries to realize the same object as an ordinary group-ring convolution
filter must pay dense 507-frequency support before the already-recorded raw-Y
lift.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate import (
    mccarthy_power_transport_raw_y_profile,
)
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import TARGET_Q_EXP
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class McCarthyIdempotentUnitProfile:
    modulus: int
    quotient_order: int
    target_q_exp: int
    zeta39_5: int
    zeta39_5_minus_one: int
    zeta39_5_minus_one_inverse: int
    point_idempotent_support: int
    point_idempotent_degree: int
    point_idempotent_is_idempotent: bool
    powered_unit_support: int
    powered_unit_minus_one_support: int
    powered_unit_order: int
    powered_unit_inverse_support: int
    powered_unit_inverse_law: bool
    normalized_projector_is_point_idempotent: bool
    point_idempotent_fourier_support: int
    powered_unit_minus_one_fourier_support: int
    powered_unit_fourier_support: int
    fourier_filter_dense: bool
    theorem_endpoint_route_required: bool


def pointwise_mul(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [l_value * r_value % modulus for l_value, r_value in zip(left, right)]


def support_count(vector: list[int]) -> int:
    return sum(1 for value in vector if value)


def dft_support_count(vector: list[int], modulus: int) -> int:
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // QUOTIENT_ORDER, modulus)
    nonzero = 0
    for frequency in range(QUOTIENT_ORDER):
        ratio = pow(zeta, frequency, modulus)
        power = 1
        total = 0
        for value in vector:
            total = (total + value * power) % modulus
            power = power * ratio % modulus
        nonzero += int(total != 0)
    return nonzero


def pointwise_order(vector: list[int], modulus: int, limit: int) -> int:
    current = [1] * len(vector)
    for exponent in range(1, limit + 1):
        current = pointwise_mul(current, vector, modulus)
        if all(value == 1 for value in current):
            return exponent
    raise AssertionError("pointwise order exceeds limit")


def mccarthy_idempotent_unit_profile() -> McCarthyIdempotentUnitProfile:
    transport = mccarthy_power_transport_raw_y_profile()
    modulus = split_prime_for(RIGHT_DEGREE * 169)
    coefficient = transport.transported_power_value
    coefficient_minus_one = transport.transported_minus_one
    coefficient_inverse = transport.transported_minus_one_inverse

    point = [0] * QUOTIENT_ORDER
    point[TARGET_Q_EXP] = 1
    unit = [1] * QUOTIENT_ORDER
    unit[TARGET_Q_EXP] = coefficient
    unit_minus_one = [(value - 1) % modulus for value in unit]
    inverse_unit = [1] * QUOTIENT_ORDER
    inverse_unit[TARGET_Q_EXP] = pow(coefficient, -1, modulus)
    normalized = [value * coefficient_inverse % modulus for value in unit_minus_one]

    return McCarthyIdempotentUnitProfile(
        modulus=modulus,
        quotient_order=QUOTIENT_ORDER,
        target_q_exp=TARGET_Q_EXP,
        zeta39_5=coefficient,
        zeta39_5_minus_one=coefficient_minus_one,
        zeta39_5_minus_one_inverse=coefficient_inverse,
        point_idempotent_support=support_count(point),
        point_idempotent_degree=sum(point) % modulus,
        point_idempotent_is_idempotent=pointwise_mul(point, point, modulus) == point,
        powered_unit_support=support_count(unit),
        powered_unit_minus_one_support=support_count(unit_minus_one),
        powered_unit_order=pointwise_order(unit, modulus, 39),
        powered_unit_inverse_support=support_count(inverse_unit),
        powered_unit_inverse_law=pointwise_mul(unit, inverse_unit, modulus)
        == [1] * QUOTIENT_ORDER,
        normalized_projector_is_point_idempotent=normalized == point,
        point_idempotent_fourier_support=dft_support_count(point, modulus),
        powered_unit_minus_one_fourier_support=dft_support_count(unit_minus_one, modulus),
        powered_unit_fourier_support=dft_support_count(unit, modulus),
        fourier_filter_dense=(
            dft_support_count(point, modulus) == QUOTIENT_ORDER
            and dft_support_count(unit_minus_one, modulus) == QUOTIENT_ORDER
            and dft_support_count(unit, modulus) == QUOTIENT_ORDER
        ),
        theorem_endpoint_route_required=True,
    )


def main() -> int:
    print("p25 Lane B McCarthy idempotent-unit gate")
    profile = mccarthy_idempotent_unit_profile()
    row_ok = (
        profile.modulus == 2029
        and profile.quotient_order == 507
        and profile.target_q_exp == 138
        and profile.zeta39_5 == 1376
        and profile.zeta39_5_minus_one == 1375
        and profile.zeta39_5_minus_one_inverse == 636
        and profile.point_idempotent_support == 1
        and profile.point_idempotent_degree == 1
        and profile.point_idempotent_is_idempotent
        and profile.powered_unit_support == 507
        and profile.powered_unit_minus_one_support == 1
        and profile.powered_unit_order == 39
        and profile.powered_unit_inverse_support == 507
        and profile.powered_unit_inverse_law
        and profile.normalized_projector_is_point_idempotent
        and profile.point_idempotent_fourier_support == 507
        and profile.powered_unit_minus_one_fourier_support == 507
        and profile.powered_unit_fourier_support == 507
        and profile.fourier_filter_dense
        and profile.theorem_endpoint_route_required
    )

    print(f"mccarthy_idempotent_unit_profile={profile}")
    print("idempotent_unit_laws")
    print("  normalized_powered_quotient_is_the_point_idempotent_e_138=1")
    print("  powered_quotient_is_1_plus_zeta39_5_minus_1_times_e_138=1")
    print("  powered_quotient_has_pointwise_order_39=1")
    print("  inverse_is_1_plus_zeta39_minus5_minus_1_times_e_138=1")
    print("  point_idempotent_and_powered_unit_are_fourier_dense_on_C507=1")
    print("interpretation")
    print("  theorem_endpoint_delta_route_remains_live=1")
    print("  ordinary_group_ring_fourier_filter_route_is_dense=1")
    print(f"square_axis_mccarthy_idempotent_unit_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_idempotent_unit_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

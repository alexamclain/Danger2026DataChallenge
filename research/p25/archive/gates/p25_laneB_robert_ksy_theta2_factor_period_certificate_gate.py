#!/usr/bin/env python3
"""Factor-level period certificate for the p25 KSY theta2 route.

The telescoping certificate checks `[2]^156 bridge = bridge` by pushing the
expanded bridge/theta2 supports.  This gate proves the period-fixing part from
the formal factors

    base * K_trace * D_segment * (1 - T).

At period 156 the doubling scale is `(61, 1)` on `C_75 x C_169`.  It fixes the
base and the C-coordinate, preserves the 25-point K trace, and moves `D` and
`T` only by right-coordinate elements already absorbed by that K trace.  Thus
the bridge is fixed for factor reasons, while every proper divisor of 156 fails
the expanded bridge/theta2 fixedness check.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_support_resolvent_gate import SUPPORT_PERIOD
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    proper_divisors,
    pushforward_power,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import scale_ring
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    edge_factor,
    geometric_factor,
    monomial,
    multiply_factors,
    multiply_ring,
    scale_coord,
    translate_ring,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class ProperDivisorFixednessRow:
    period: int
    right_scale: int
    c_scale: int
    c_scale_is_one: bool
    bridge_fixed: bool
    theta2_fixed: bool


@dataclass(frozen=True)
class KsyTheta2FactorPeriodCertificateProfile:
    support_period: int
    period_scale: Coord
    base_fixed: bool
    k_generator_multiplier: int
    k_generator_multiplier_coprime_to_25: bool
    k_trace_fixed: bool
    d_drift: Coord
    d_drift_k_index: int
    t_drift: Coord
    t_drift_k_index: int
    d_drift_absorbed_by_k_trace: bool
    t_drift_absorbed_by_k_trace: bool
    k_times_d_segment_fixed: bool
    full_factor_product_fixed: bool
    bridge_fixed_by_factor_certificate: bool
    theta2_fixed_by_bridge_certificate: bool
    proper_divisor_rows: tuple[ProperDivisorFixednessRow, ...]
    proper_divisors_all_fail_to_fix_theta2: bool
    factor_support_budget: int
    telescoping_period_subcheck_budget: int
    budget_floor_improvement_factor: int
    row_ok: bool


def period_scale(period: int) -> Coord:
    return (pow(2, period, RIGHT_ORDER), pow(2, period, C_ORDER))


def push_coord(coord: Coord, period: int) -> Coord:
    right_scale, c_scale = period_scale(period)
    return ((right_scale * coord[0]) % RIGHT_ORDER, (c_scale * coord[1]) % C_ORDER)


def coord_delta(left: Coord, right: Coord) -> Coord:
    return ((left[0] - right[0]) % RIGHT_ORDER, (left[1] - right[1]) % C_ORDER)


def k_index(coord: Coord) -> int | None:
    for index in range(25):
        if scale_coord(KERNEL_SHIFT, index) == coord:
            return index
    return None


def require_k_index(coord: Coord) -> int:
    index = k_index(coord)
    if index is None:
        raise AssertionError(f"{coord} is not in the K trace subgroup")
    return index


def push_factor(ring: Ring, period: int) -> Ring:
    return pushforward_power(ring, period)


def proper_divisor_row(period: int, bridge: Ring, theta2: Ring) -> ProperDivisorFixednessRow:
    right_scale, c_scale = period_scale(period)
    return ProperDivisorFixednessRow(
        period=period,
        right_scale=right_scale,
        c_scale=c_scale,
        c_scale_is_one=c_scale == 1,
        bridge_fixed=pushforward_power(bridge, period) == bridge,
        theta2_fixed=pushforward_power(theta2, period) == theta2,
    )


def profile_factor_period_certificate() -> KsyTheta2FactorPeriodCertificateProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2_inverse = normalized_y_exponent_footprint(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    theta2 = scale_ring(theta2_inverse, -1)

    base = monomial(BASE_POINT)
    k_trace = geometric_factor(KERNEL_SHIFT, 25)
    d_segment = geometric_factor(D_SHIFT, 3)
    edge = edge_factor(BRIDGE_SHIFT)
    factors = (
        ("base", base),
        ("K_trace", k_trace),
        ("D_segment", d_segment),
        ("bridge_edge", edge),
    )
    product = multiply_factors(factors)

    scale = period_scale(SUPPORT_PERIOD)
    pushed_k_generator = push_coord(KERNEL_SHIFT, SUPPORT_PERIOD)
    k_multiplier = require_k_index(pushed_k_generator)
    pushed_d = push_coord(D_SHIFT, SUPPORT_PERIOD)
    pushed_t = push_coord(BRIDGE_SHIFT, SUPPORT_PERIOD)
    d_drift = coord_delta(pushed_d, D_SHIFT)
    t_drift = coord_delta(pushed_t, BRIDGE_SHIFT)
    d_drift_index = require_k_index(d_drift)
    t_drift_index = require_k_index(t_drift)

    pushed_k_trace = push_factor(k_trace, SUPPORT_PERIOD)
    pushed_d_segment = push_factor(d_segment, SUPPORT_PERIOD)
    pushed_edge = push_factor(edge, SUPPORT_PERIOD)
    k_times_d = multiply_ring(k_trace, d_segment)
    pushed_k_times_d = multiply_ring(pushed_k_trace, pushed_d_segment)
    full_product_fixed = push_factor(product, SUPPORT_PERIOD) == product
    bridge_fixed = pushforward_power(bridge, SUPPORT_PERIOD) == bridge
    theta2_fixed = pushforward_power(theta2, SUPPORT_PERIOD) == theta2
    proper_rows = tuple(
        proper_divisor_row(period, bridge, theta2)
        for period in proper_divisors(SUPPORT_PERIOD)
    )
    factor_support_budget = sum(len(factor) for _name, factor in factors)
    telescoping_subcheck_budget = len(bridge) + len(theta2) + len(
        pushforward_power(bridge, SUPPORT_PERIOD)
    ) + len(pushforward_power(theta2, SUPPORT_PERIOD))

    row_ok = (
        SUPPORT_PERIOD == 156
        and scale == (61, 1)
        and push_coord(BASE_POINT, SUPPORT_PERIOD) == BASE_POINT
        and pushed_k_generator == (27, 0)
        and k_multiplier == 11
        and gcd(k_multiplier, 25) == 1
        and pushed_k_trace == k_trace
        and d_drift == (45, 0)
        and d_drift_index == 10
        and t_drift == (30, 0)
        and t_drift_index == 15
        and translate_ring(k_trace, d_drift) == k_trace
        and translate_ring(k_trace, t_drift) == k_trace
        and pushed_k_times_d == k_times_d
        and multiply_ring(pushed_k_times_d, pushed_edge) == multiply_ring(k_times_d, edge)
        and product == bridge
        and full_product_fixed
        and bridge_fixed
        and theta2_fixed
        and all(not row.bridge_fixed and not row.theta2_fixed for row in proper_rows)
        and all(not row.c_scale_is_one for row in proper_rows)
        and factor_support_budget == 31
        and telescoping_subcheck_budget == 900
        and telescoping_subcheck_budget // factor_support_budget == 29
    )
    return KsyTheta2FactorPeriodCertificateProfile(
        support_period=SUPPORT_PERIOD,
        period_scale=scale,
        base_fixed=push_coord(BASE_POINT, SUPPORT_PERIOD) == BASE_POINT,
        k_generator_multiplier=k_multiplier,
        k_generator_multiplier_coprime_to_25=gcd(k_multiplier, 25) == 1,
        k_trace_fixed=pushed_k_trace == k_trace,
        d_drift=d_drift,
        d_drift_k_index=d_drift_index,
        t_drift=t_drift,
        t_drift_k_index=t_drift_index,
        d_drift_absorbed_by_k_trace=translate_ring(k_trace, d_drift) == k_trace,
        t_drift_absorbed_by_k_trace=translate_ring(k_trace, t_drift) == k_trace,
        k_times_d_segment_fixed=pushed_k_times_d == k_times_d,
        full_factor_product_fixed=full_product_fixed,
        bridge_fixed_by_factor_certificate=bridge_fixed,
        theta2_fixed_by_bridge_certificate=theta2_fixed,
        proper_divisor_rows=proper_rows,
        proper_divisors_all_fail_to_fix_theta2=all(not row.theta2_fixed for row in proper_rows),
        factor_support_budget=factor_support_budget,
        telescoping_period_subcheck_budget=telescoping_subcheck_budget,
        budget_floor_improvement_factor=telescoping_subcheck_budget // factor_support_budget,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/theta2 factor-period certificate gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} base={BASE_POINT} "
        f"K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile = profile_factor_period_certificate()
    print(f"ksy_theta2_factor_period_certificate_profile={profile}")
    print("factor_period_laws")
    print("  doubling_power_156_has_scale_61_1_on_C75xC169=1")
    print("  base_is_fixed_and_K_trace_is_preserved_as_a_25_point_subgroup=1")
    print("  D_drift_is_10K_and_T_drift_is_15K=1")
    print("  K_trace_absorbs_the_D_and_T_drifts=1")
    print("  bridge_factor_product_is_fixed_by_doubling_power_156=1")
    print("  theta2_fixedness_follows_from_bridge_fixedness_and_theta2_4_minus_2_bridge=1")
    print("  proper_divisors_of_156_fail_the_bridge_and_theta2_fixedness_checks=1")
    print("interpretation")
    print("  period_part_of_telescoping_certificate_can_be_checked_at_factor_level=1")
    print("  this_reduces_the_period_subcheck_from_900_expanded_cells_to_31_factor_cells=1")
    print(f"robert_ksy_theta2_factor_period_certificate_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_factor_period_certificate_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

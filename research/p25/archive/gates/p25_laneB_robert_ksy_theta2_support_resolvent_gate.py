#!/usr/bin/env python3
"""Support-period theta2 resolvent for the p25 KSY route.

The first theta2 resolvent used the ambient doubling order 780 on
C_75 x C_169.  The actual bridge/theta2 support has smaller doubling period
156.  Therefore the finite inverse of `(4 - [2])` can use

    (4^155 + 4^154[2] + ... + [2]^155) / (4^156 - 1)

instead of the ambient 780-term version.

This gate proves the shorter period, rejects all proper period-divisor
shortcuts, and records the improved cost and normalization facts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm

from p25_laneB_robert_ksy_theta2_resolvent_gate import (
    P25,
    SQRT_FLOOR,
    exact_division_possible,
    weighted_resolvent_numerator,
)
from p25_laneB_robert_ksy_y_doubling_distribution_gate import (
    divide_ring_exact,
    multiplicative_order,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import double_pushforward, scale_ring
from p25_laneB_square_axis_bridge_candidate_harness_gate import MODULUS as AUX_MODULUS
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER
from p25_selected_defect_value_gate import split_prime_for


SUPPORT_PERIOD = 156
SMALL_AUX_MODULUS = split_prime_for(3 * 13 * 13)


@dataclass(frozen=True)
class PeriodShortcutRow:
    period: int
    returns_to_theta2: bool
    union_support: int
    term_budget: int
    numerator_support: int
    exact_divisible: bool
    recovers_bridge: bool


@dataclass(frozen=True)
class KsyTheta2SupportResolventProfile:
    ambient_doubling_order: int
    bridge_orbit_period: int
    theta2_orbit_period: int
    support_denominator_bit_length: int
    support_denominator_nonzero_mod_p25: bool
    support_denominator_gcd_p25_minus_1: int
    support_denominator_gcd_p25_plus_1: int
    support_denominator_gcd_aux126751_minus_1: int
    support_denominator_gcd_aux2029_minus_1: int
    support_resolvent_union_support: int
    support_resolvent_term_budget: int
    support_weighted_bit_budget: int
    recovered_profile_ok: bool
    recovered_equals_bridge: bool
    proper_period_shortcuts: tuple[PeriodShortcutRow, ...]
    proper_period_shortcuts_all_fail: bool
    old_ambient_term_budget: int
    term_budget_improvement_factor: int
    term_budget_below_sqrt: bool
    weighted_bit_budget_below_sqrt: bool
    row_ok: bool


def divisors(value: int) -> tuple[int, ...]:
    return tuple(index for index in range(1, value + 1) if value % index == 0)


def orbit_period(ring: Ring, limit: int) -> int:
    current = ring
    for period in range(1, limit + 1):
        current = double_pushforward(current)
        if current == ring:
            return period
    raise AssertionError("orbit period exceeds limit")


def weighted_exponent_bit_budget(theta2_support: int, order: int) -> int:
    return theta2_support * sum((4 ** exponent).bit_length() for exponent in range(order))


def shortcut_row(theta2: Ring, bridge: Ring, period: int) -> PeriodShortcutRow:
    denominator = 4 ** period - 1
    numerator, union_support, returns_to_theta2, term_budget = weighted_resolvent_numerator(
        theta2,
        period,
    )
    exact_divisible = exact_division_possible(numerator, denominator)
    recovers_bridge = False
    if exact_divisible:
        recovered = divide_ring_exact(numerator, denominator)
        recovers_bridge = recovered == bridge
    return PeriodShortcutRow(
        period=period,
        returns_to_theta2=returns_to_theta2,
        union_support=union_support,
        term_budget=term_budget,
        numerator_support=len(numerator),
        exact_divisible=exact_divisible,
        recovers_bridge=recovers_bridge,
    )


def theta2_support_resolvent_profile() -> KsyTheta2SupportResolventProfile:
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

    ambient_order = lcm(
        multiplicative_order(2, RIGHT_ORDER),
        multiplicative_order(2, C_ORDER),
    )
    bridge_period = orbit_period(bridge, ambient_order)
    theta2_period = orbit_period(theta2, ambient_order)
    denominator = 4 ** SUPPORT_PERIOD - 1
    numerator, union_support, returns_to_theta2, term_budget = weighted_resolvent_numerator(
        theta2,
        SUPPORT_PERIOD,
    )
    recovered = divide_ring_exact(numerator, denominator)
    recovered_profile = bridge_profile("ksy_theta2_support_resolvent_recovered_bridge", recovered)
    proper_rows = tuple(
        shortcut_row(theta2, bridge, period)
        for period in divisors(SUPPORT_PERIOD)
        if period < SUPPORT_PERIOD
    )
    proper_fail = all(not row.recovers_bridge for row in proper_rows)
    weighted_bits = weighted_exponent_bit_budget(len(theta2), SUPPORT_PERIOD)

    row_ok = (
        ambient_order == 780
        and bridge_period == SUPPORT_PERIOD
        and theta2_period == SUPPORT_PERIOD
        and denominator.bit_length() == 312
        and denominator % P25 != 0
        and gcd(denominator, P25 - 1) == 1
        and gcd(denominator, P25 + 1) == 3
        and gcd(denominator, AUX_MODULUS - 1) == 2535
        and gcd(denominator, SMALL_AUX_MODULUS - 1) == 507
        and returns_to_theta2
        and union_support == 11700
        and term_budget == 46800
        and weighted_bits == 7_300_800
        and recovered == bridge
        and recovered_profile.ok
        and len(numerator) == 150
        and proper_fail
        and all(not row.exact_divisible for row in proper_rows)
        and 234000 // term_budget == 5
        and term_budget < SQRT_FLOOR
        and weighted_bits < SQRT_FLOOR
    )
    return KsyTheta2SupportResolventProfile(
        ambient_doubling_order=ambient_order,
        bridge_orbit_period=bridge_period,
        theta2_orbit_period=theta2_period,
        support_denominator_bit_length=denominator.bit_length(),
        support_denominator_nonzero_mod_p25=denominator % P25 != 0,
        support_denominator_gcd_p25_minus_1=gcd(denominator, P25 - 1),
        support_denominator_gcd_p25_plus_1=gcd(denominator, P25 + 1),
        support_denominator_gcd_aux126751_minus_1=gcd(denominator, AUX_MODULUS - 1),
        support_denominator_gcd_aux2029_minus_1=gcd(denominator, SMALL_AUX_MODULUS - 1),
        support_resolvent_union_support=union_support,
        support_resolvent_term_budget=term_budget,
        support_weighted_bit_budget=weighted_bits,
        recovered_profile_ok=recovered_profile.ok,
        recovered_equals_bridge=recovered == bridge,
        proper_period_shortcuts=proper_rows,
        proper_period_shortcuts_all_fail=proper_fail,
        old_ambient_term_budget=234000,
        term_budget_improvement_factor=234000 // term_budget,
        term_budget_below_sqrt=term_budget < SQRT_FLOOR,
        weighted_bit_budget_below_sqrt=weighted_bits < SQRT_FLOOR,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel theta2 support-resolvent gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = theta2_support_resolvent_profile()
    print(f"ksy_theta2_support_resolvent_profile={profile}")
    print("support_resolvent_laws")
    print("  ambient_doubling_order_on_source_group_is_780=1")
    print("  bridge_and_theta2_doubling_orbit_period_is_156=1")
    print("  inverse_operator_uses_4^155_plus_..._plus_[2]^155_over_4^156_minus_1=1")
    print("  denominator_has_312_bits_and_is_nonzero_mod_p25=1")
    print("  denominator_exponent_is_invertible_on_Fp_star_gcd_1=1")
    print("  shifted_theta2_term_budget_improves_from_234000_to_46800=1")
    print("  weighted_exponent_bit_budget_7300800_below_sqrt=1")
    print("  proper_divisors_of_156_do_not_recover_bridge=1")
    print("interpretation")
    print("  theta2_resolvent_should_use_support_period_156_not_ambient_order_780=1")
    print("  Fp_star_value_level_root_ambiguity_is_removed_for_the_support_resolvent=1")
    print(f"robert_ksy_theta2_support_resolvent_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_support_resolvent_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

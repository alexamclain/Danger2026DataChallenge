#!/usr/bin/env python3
"""Doubling-resolvent recovery gate for the p25 KSY theta2 route.

The even-D theta2 gate shows

    theta2 = 4*bridge - [2]bridge,

where `[2]` is the doubling automorphism on C_75 x C_169.  Since `[2]` has
order 780 on this source group, the operator `(4 - [2])` is invertible by the
finite geometric resolvent

    (4 - [2])^-1 =
      (4^779 + 4^778[2] + ... + [2]^779) / (4^780 - 1).

This gate checks the exact finite identity and records its cost.  It does not
prove that a Kato-Siegel theorem emits theta2, but it shows that if theta2 is
available as an arithmetic object, the doubled layer can be removed by a
sub-sqrt finite operator rather than by an unexplained hand subtraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

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
from p25_laneB_robert_ksy_y_projection_gate import add_rings, double_pushforward, scale_ring
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER


P25 = 10_000_000_000_000_000_000_000_013
SQRT_FLOOR = 3_162_277_660_168


@dataclass(frozen=True)
class KsyTheta2ResolventProfile:
    doubling_order: int
    denominator_bit_length: int
    denominator_nonzero_mod_p25: bool
    theta2_support: int
    shifted_theta2_union_support: int
    shifted_theta2_term_budget: int
    weighted_sum_support: int
    weighted_sum_divisible_by_denominator: bool
    recovered_profile: CandidateProfile
    recovered_equals_bridge: bool
    theta2_inverse_resolvent_equals_negative_bridge: bool
    current_returns_after_full_order: bool
    term_budget_below_sqrt: bool
    union_support_below_sqrt: bool
    row_ok: bool


def add_ring_entry(ring: Ring, coord: tuple[int, int], coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def weighted_resolvent_numerator(theta2: Ring, order: int) -> tuple[Ring, int, bool, int]:
    """Return sum 4^(order-1-i) [2]^i theta2 and union support."""

    out: Ring = {}
    shifted_union: set[tuple[int, int]] = set()
    current = theta2
    weight = 4 ** (order - 1)
    for _index in range(order):
        shifted_union.update(current)
        for coord, coefficient in current.items():
            add_ring_entry(out, coord, weight * coefficient)
        current = double_pushforward(current)
        weight //= 4
    return dict(sorted(out.items())), len(shifted_union), current == theta2, order * len(theta2)


def exact_division_possible(ring: Ring, divisor: int) -> bool:
    return all(coefficient % divisor == 0 for coefficient in ring.values())


def profile_theta2_resolvent() -> KsyTheta2ResolventProfile:
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

    right_order = multiplicative_order(2, RIGHT_ORDER)
    c_order = multiplicative_order(2, C_ORDER)
    source_order = lcm(right_order, c_order)
    denominator = 4 ** source_order - 1

    numerator, union_support, returns_after_order, term_budget = weighted_resolvent_numerator(
        theta2,
        source_order,
    )
    recovered = divide_ring_exact(numerator, denominator)
    recovered_profile = bridge_profile("ksy_theta2_resolvent_recovered_bridge", recovered)

    inverse_numerator, _inverse_union, inverse_returns, _inverse_budget = weighted_resolvent_numerator(
        theta2_inverse,
        source_order,
    )
    inverse_recovered = divide_ring_exact(inverse_numerator, denominator)

    row_ok = (
        source_order == 780
        and denominator.bit_length() == 1560
        and denominator % P25 != 0
        and theta2 == add_rings(scale_ring(bridge, 4), scale_ring(double_pushforward(bridge), -1))
        and len(theta2) == 300
        and union_support == 11700
        and term_budget == 234000
        and len(numerator) == 150
        and exact_division_possible(numerator, denominator)
        and recovered == bridge
        and recovered_profile.ok
        and inverse_recovered == scale_ring(bridge, -1)
        and returns_after_order
        and inverse_returns
        and term_budget < SQRT_FLOOR
        and union_support < SQRT_FLOOR
    )
    return KsyTheta2ResolventProfile(
        doubling_order=source_order,
        denominator_bit_length=denominator.bit_length(),
        denominator_nonzero_mod_p25=denominator % P25 != 0,
        theta2_support=len(theta2),
        shifted_theta2_union_support=union_support,
        shifted_theta2_term_budget=term_budget,
        weighted_sum_support=len(numerator),
        weighted_sum_divisible_by_denominator=exact_division_possible(numerator, denominator),
        recovered_profile=recovered_profile,
        recovered_equals_bridge=recovered == bridge,
        theta2_inverse_resolvent_equals_negative_bridge=inverse_recovered == scale_ring(bridge, -1),
        current_returns_after_full_order=returns_after_order and inverse_returns,
        term_budget_below_sqrt=term_budget < SQRT_FLOOR,
        union_support_below_sqrt=union_support < SQRT_FLOOR,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel theta2 resolvent gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_theta2_resolvent()
    print(f"ksy_theta2_resolvent_profile={profile}")
    print("theta2_resolvent_laws")
    print("  theta2 = (4 - [2]) * bridge")
    print("  [2]_on_C75xC169_has_order_780=1")
    print("  inverse_operator = (4^779 + 4^778[2] + ... + [2]^779) / (4^780 - 1)")
    print("  denominator_has_1560_bits_and_is_nonzero_mod_p25=1")
    print("  shifted_theta2_term_budget_234000_below_sqrt_p=1")
    print("  shifted_theta2_union_support_11700_below_sqrt_p=1")
    print("  weighted_resolvent_numerator_collapses_to_150_cells=1")
    print("  exact_division_by_denominator_recovers_bridge=1")
    print("interpretation")
    print("  theta2_route_can_remove_doubled_layer_by_finite_resolvent_if_theta2_is_arithmetic=1")
    print("  remaining_debt_is_arithmetic_theta2_producer_and_legitimate_scalar_normalization=1")
    print(f"robert_ksy_theta2_resolvent_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_resolvent_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

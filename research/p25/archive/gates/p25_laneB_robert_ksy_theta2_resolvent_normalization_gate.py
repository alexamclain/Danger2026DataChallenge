#!/usr/bin/env python3
"""Normalization gate for the p25 KSY theta2 resolvent.

The theta2 resolvent gate proves the integer divisor identity

    numerator = (4^780 - 1) * bridge.

This gate separates the allowed normalizations.  As an additive/divisor or
linear coefficient operation, division by `4^780 - 1` is harmless modulo p25
and the auxiliary coefficient primes used by local gates.  As a multiplicative
finite-field exponent operation, it is not free: the denominator is not
invertible on F_p^* or the auxiliary multiplicative groups, so extracting a
root would require a theorem-supplied branch/root selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_resolvent_gate import (
    P25,
    SQRT_FLOOR,
    weighted_resolvent_numerator,
)
from p25_laneB_robert_ksy_y_doubling_distribution_gate import divide_ring_exact
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    normalized_y_exponent_footprint,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import scale_ring
from p25_laneB_square_axis_bridge_candidate_harness_gate import MODULUS as AUX_MODULUS
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER
from p25_selected_defect_value_gate import split_prime_for


DOUBLING_ORDER = 780
DENOMINATOR = 4 ** DOUBLING_ORDER - 1
SMALL_AUX_MODULUS = split_prime_for(3 * 13 * 13)


@dataclass(frozen=True)
class KsyTheta2ResolventNormalizationProfile:
    denominator_bit_length: int
    denominator_mod_p25_nonzero: bool
    denominator_mod_aux126751_nonzero: bool
    denominator_mod_aux2029_nonzero: bool
    integer_exact_division_recovers_bridge: bool
    additive_p25_scaling_recovers_bridge: bool
    additive_aux126751_scaling_recovers_bridge: bool
    additive_aux2029_scaling_recovers_bridge: bool
    multiplicative_fp_star_gcd: int
    multiplicative_fp2_norm_gcd: int
    multiplicative_aux126751_gcd: int
    multiplicative_aux2029_gcd: int
    exponent_inverse_available_fp_star: bool
    exponent_inverse_available_aux126751: bool
    weighted_exponent_bit_budget: int
    weighted_exponent_bit_budget_below_sqrt: bool
    largest_weight_bit_length: int
    scalar_inverse_bit_length_p25: int
    normalization_debt: str
    row_ok: bool


def mod_scaled_ring(ring: Ring, scalar: int, modulus: int) -> dict[tuple[int, int], int]:
    return {
        coord: (coefficient * scalar) % modulus
        for coord, coefficient in sorted(ring.items())
        if (coefficient * scalar) % modulus
    }


def ring_mod(ring: Ring, modulus: int) -> dict[tuple[int, int], int]:
    return {
        coord: coefficient % modulus
        for coord, coefficient in sorted(ring.items())
        if coefficient % modulus
    }


def weighted_exponent_bit_budget(theta2_support: int, order: int) -> int:
    # weights are 4^779, 4^778, ..., 1, with bit lengths 1559, 1557, ..., 1.
    return theta2_support * sum((4 ** exponent).bit_length() for exponent in range(order))


def profile_theta2_resolvent_normalization() -> KsyTheta2ResolventNormalizationProfile:
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
    numerator, _union_support, _returns_after_order, _term_budget = weighted_resolvent_numerator(
        theta2,
        DOUBLING_ORDER,
    )
    recovered = divide_ring_exact(numerator, DENOMINATOR)

    inv_p25 = pow(DENOMINATOR % P25, -1, P25)
    inv_aux = pow(DENOMINATOR % AUX_MODULUS, -1, AUX_MODULUS)
    inv_small_aux = pow(DENOMINATOR % SMALL_AUX_MODULUS, -1, SMALL_AUX_MODULUS)
    bit_budget = weighted_exponent_bit_budget(len(theta2), DOUBLING_ORDER)

    row_ok = (
        DENOMINATOR.bit_length() == 1560
        and DENOMINATOR % P25 != 0
        and DENOMINATOR % AUX_MODULUS != 0
        and DENOMINATOR % SMALL_AUX_MODULUS != 0
        and recovered == bridge
        and mod_scaled_ring(numerator, inv_p25, P25) == ring_mod(bridge, P25)
        and mod_scaled_ring(numerator, inv_aux, AUX_MODULUS) == ring_mod(bridge, AUX_MODULUS)
        and mod_scaled_ring(numerator, inv_small_aux, SMALL_AUX_MODULUS)
        == ring_mod(bridge, SMALL_AUX_MODULUS)
        and gcd(DENOMINATOR, P25 - 1) == 11
        and gcd(DENOMINATOR, P25 + 1) == 3
        and gcd(DENOMINATOR, AUX_MODULUS - 1) == 12675
        and gcd(DENOMINATOR, SMALL_AUX_MODULUS - 1) == 507
        and bit_budget == 182_520_000
        and bit_budget < SQRT_FLOOR
    )
    return KsyTheta2ResolventNormalizationProfile(
        denominator_bit_length=DENOMINATOR.bit_length(),
        denominator_mod_p25_nonzero=DENOMINATOR % P25 != 0,
        denominator_mod_aux126751_nonzero=DENOMINATOR % AUX_MODULUS != 0,
        denominator_mod_aux2029_nonzero=DENOMINATOR % SMALL_AUX_MODULUS != 0,
        integer_exact_division_recovers_bridge=recovered == bridge,
        additive_p25_scaling_recovers_bridge=(
            mod_scaled_ring(numerator, inv_p25, P25) == ring_mod(bridge, P25)
        ),
        additive_aux126751_scaling_recovers_bridge=(
            mod_scaled_ring(numerator, inv_aux, AUX_MODULUS) == ring_mod(bridge, AUX_MODULUS)
        ),
        additive_aux2029_scaling_recovers_bridge=(
            mod_scaled_ring(numerator, inv_small_aux, SMALL_AUX_MODULUS)
            == ring_mod(bridge, SMALL_AUX_MODULUS)
        ),
        multiplicative_fp_star_gcd=gcd(DENOMINATOR, P25 - 1),
        multiplicative_fp2_norm_gcd=gcd(DENOMINATOR, P25 + 1),
        multiplicative_aux126751_gcd=gcd(DENOMINATOR, AUX_MODULUS - 1),
        multiplicative_aux2029_gcd=gcd(DENOMINATOR, SMALL_AUX_MODULUS - 1),
        exponent_inverse_available_fp_star=gcd(DENOMINATOR, P25 - 1) == 1,
        exponent_inverse_available_aux126751=gcd(DENOMINATOR, AUX_MODULUS - 1) == 1,
        weighted_exponent_bit_budget=bit_budget,
        weighted_exponent_bit_budget_below_sqrt=bit_budget < SQRT_FLOOR,
        largest_weight_bit_length=(4 ** (DOUBLING_ORDER - 1)).bit_length(),
        scalar_inverse_bit_length_p25=inv_p25.bit_length(),
        normalization_debt=(
            "additive/divisor scaling is finite; multiplicative unit root "
            "selection still needs a theorem because the denominator exponent "
            "is not invertible on the relevant unit groups"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel theta2 resolvent-normalization gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_theta2_resolvent_normalization()
    print(f"ksy_theta2_resolvent_normalization_profile={profile}")
    print("normalization_laws")
    print("  integer_division_of_resolvent_numerator_recovers_bridge=1")
    print("  denominator_is_nonzero_mod_p25_aux126751_aux2029=1")
    print("  additive_scalar_scaling_recovers_bridge_mod_p25_aux126751_aux2029=1")
    print("  denominator_exponent_not_invertible_on_Fp_star_gcd_11=1")
    print("  denominator_exponent_not_invertible_on_Fp2_norm_gcd_3=1")
    print("  denominator_exponent_not_invertible_on_aux_unit_groups=1")
    print("  weighted_exponent_bit_budget_182520000_below_sqrt=1")
    print("interpretation")
    print("  theta2_resolvent_is_valid_as_additive_or_divisor_normalization=1")
    print("  multiplicative_unit_route_still_needs_theorem_supplied_root_selection=1")
    print(f"robert_ksy_theta2_resolvent_normalization_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_resolvent_normalization_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

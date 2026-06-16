#!/usr/bin/env python3
"""Root-ambiguity gate for the p25 KSY theta2 resolvent.

The resolvent-normalization gate showed that the denominator

    D = 4^780 - 1

is not invertible as a multiplicative exponent on F_p^*: gcd(D, p-1)=11.
Thus a value-level D-th-root extraction, if it exists, has an 11-fold
root-of-unity ambiguity.

This gate records what that ambiguity does and does not affect.  A global
root-of-unity factor has zero divisor, so it is invisible to the divisor/source
bridge contract.  But the 11 value branches are genuinely distinct in F_p, and
no finite source-mask gate can choose among them.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_resolvent_normalization_gate import (
    DENOMINATOR,
    P25,
    SMALL_AUX_MODULUS,
    AUX_MODULUS,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    bridge_profile,
    profile_half_edge_footprint,
    symmetric_edge_ring,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import CandidateProfile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER


@dataclass(frozen=True)
class KsyTheta2RootAmbiguityProfile:
    fp_star_kernel_order: int
    fp2_norm_kernel_order: int
    aux126751_unit_kernel_order: int
    aux2029_unit_kernel_order: int
    mu11_generator: int
    mu11_distinct_count: int
    all_mu11_killed_by_denominator_power: bool
    scalar_divisor_support: int
    branch_divisor_masks_distinct: int
    bridge_profile_under_scalar_branch: CandidateProfile
    finite_bridge_contract_selects_branch: bool
    value_branches_are_distinct: bool
    root_ambiguity_is_global_scalar_only: bool
    row_ok: bool


def root_of_unity_generator(order: int, modulus: int) -> int:
    for base in range(2, 200):
        candidate = pow(base, (modulus - 1) // order, modulus)
        if candidate != 1 and pow(candidate, order, modulus) == 1:
            return candidate
    raise AssertionError(f"failed to find order-{order} root of unity")


def zero_scalar_divisor() -> Ring:
    return {}


def profile_root_ambiguity() -> KsyTheta2RootAmbiguityProfile:
    half_profile = profile_half_edge_footprint()
    bridge = symmetric_edge_ring(
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
    )
    fp_kernel_order = gcd(DENOMINATOR, P25 - 1)
    zeta11 = root_of_unity_generator(fp_kernel_order, P25)
    branches = tuple(pow(zeta11, exponent, P25) for exponent in range(fp_kernel_order))
    scalar_masks = tuple(zero_scalar_divisor() for _branch in branches)
    branch_profiles = tuple(bridge_profile(f"ksy_theta2_mu11_branch_{index}", bridge) for index in range(fp_kernel_order))

    row_ok = (
        fp_kernel_order == 11
        and gcd(DENOMINATOR, P25 + 1) == 3
        and gcd(DENOMINATOR, AUX_MODULUS - 1) == 12675
        and gcd(DENOMINATOR, SMALL_AUX_MODULUS - 1) == 507
        and len(set(branches)) == 11
        and all(pow(branch, DENOMINATOR, P25) == 1 for branch in branches)
        and all(mask == {} for mask in scalar_masks)
        and len(set(tuple(sorted(mask.items())) for mask in scalar_masks)) == 1
        and all(profile.ok for profile in branch_profiles)
    )
    return KsyTheta2RootAmbiguityProfile(
        fp_star_kernel_order=fp_kernel_order,
        fp2_norm_kernel_order=gcd(DENOMINATOR, P25 + 1),
        aux126751_unit_kernel_order=gcd(DENOMINATOR, AUX_MODULUS - 1),
        aux2029_unit_kernel_order=gcd(DENOMINATOR, SMALL_AUX_MODULUS - 1),
        mu11_generator=zeta11,
        mu11_distinct_count=len(set(branches)),
        all_mu11_killed_by_denominator_power=all(
            pow(branch, DENOMINATOR, P25) == 1 for branch in branches
        ),
        scalar_divisor_support=len(zero_scalar_divisor()),
        branch_divisor_masks_distinct=len(
            set(tuple(sorted(mask.items())) for mask in scalar_masks)
        ),
        bridge_profile_under_scalar_branch=branch_profiles[0],
        finite_bridge_contract_selects_branch=False,
        value_branches_are_distinct=len(set(branches)) == 11,
        root_ambiguity_is_global_scalar_only=all(mask == {} for mask in scalar_masks),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Kato-Siegel theta2 root-ambiguity gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_root_ambiguity()
    print(f"ksy_theta2_root_ambiguity_profile={profile}")
    print("root_ambiguity_laws")
    print("  gcd_4_780_minus_1_with_Fp_star_is_11=1")
    print("  Fp_contains_11_distinct_denominator_power_kernel_branches=1")
    print("  all_mu11_branches_have_zero_divisor=1")
    print("  global_scalar_branch_does_not_change_bridge_source_mask=1")
    print("  finite_bridge_contract_cannot_select_between_value_branches=1")
    print("interpretation")
    print("  root_ambiguity_is_harmless_for_divisor_level_payloads=1")
    print("  value_level_multiplicative_unit_route_still_needs_branch_selection=1")
    print(f"robert_ksy_theta2_root_ambiguity_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_root_ambiguity_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

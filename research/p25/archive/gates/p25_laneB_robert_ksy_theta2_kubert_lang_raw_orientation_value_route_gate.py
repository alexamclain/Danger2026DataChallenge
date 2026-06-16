#!/usr/bin/env python3
"""Value-level route for raw oriented KL/KSY product theorem hits.

The raw orientation certificate-router gate handles divisor/additive payloads:
an accepted raw product emits theta2 or theta2 inverse, then the finite
support-period resolvent recovers the bridge.

If a theorem emits finite-field unit values instead, the normalization question
is sharper.  The ambient 780-period denominator has an 11-fold F_p^* branch
ambiguity, but the actual theta2 support period is 156 and

    gcd(4^156 - 1, p - 1) = 1.

So a value-level theorem hit is viable only if it supplies the period-156
theta2 context/telescoping/fixedness.  Then the F_p^* root is unique; without
that context, the ambient value route still has the mu_11 ambiguity.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate import (
    RawOrientationCertificateRoute,
    profile_raw_orientation_certificate_router,
)
from p25_laneB_robert_ksy_theta2_resolvent_gate import P25
from p25_laneB_robert_ksy_theta2_resolvent_normalization_gate import (
    DENOMINATOR as AMBIENT_DENOMINATOR,
)
from p25_laneB_robert_ksy_theta2_root_ambiguity_gate import profile_root_ambiguity
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import (
    SUPPORT_PERIOD,
    theta2_support_resolvent_profile,
)


@dataclass(frozen=True)
class RawOrientationValueBranch:
    route_name: str
    emitted_payload: str
    recovered_sign: int
    divisor_route_ok: bool
    support_period_value_root_unique_fp: bool
    value_route_requires_period_context: bool


@dataclass(frozen=True)
class RawOrientationValueRouteProfile:
    raw_orientation_router_ok: bool
    support_period: int
    ambient_period: int
    support_denominator_bit_length: int
    support_denominator_gcd_fp_star: int
    support_denominator_gcd_fp2_norm: int
    support_denominator_gcd_aux126751: int
    support_denominator_gcd_aux2029: int
    support_value_root_unique_fp_star: bool
    ambient_denominator_gcd_fp_star: int
    ambient_value_branch_count_fp_star: int
    ambient_value_route_has_mu11_ambiguity: bool
    proper_period_shortcuts_all_fail: bool
    branch_value_routes: tuple[RawOrientationValueBranch, ...]
    theta2_inverse_value_routes: int
    theta2_value_routes: int
    value_level_obligation: str
    row_ok: bool


def value_branch(route: RawOrientationCertificateRoute) -> RawOrientationValueBranch:
    return RawOrientationValueBranch(
        route_name=route.name,
        emitted_payload=route.emitted_payload,
        recovered_sign=route.theta2_candidate_profile.recovered_sign,
        divisor_route_ok=route.certificate_path_ok,
        support_period_value_root_unique_fp=True,
        value_route_requires_period_context=True,
    )


def profile_raw_orientation_value_route() -> RawOrientationValueRouteProfile:
    router = profile_raw_orientation_certificate_router()
    support = theta2_support_resolvent_profile()
    root = profile_root_ambiguity()
    branches = tuple(value_branch(route) for route in router.branch_routes)
    support_denominator = 4**SUPPORT_PERIOD - 1
    ambient_gcd = gcd(AMBIENT_DENOMINATOR, P25 - 1)
    row_ok = (
        router.row_ok
        and support.row_ok
        and root.row_ok
        and SUPPORT_PERIOD == 156
        and support.support_denominator_bit_length == 312
        and support.support_denominator_gcd_p25_minus_1 == 1
        and gcd(support_denominator, P25 - 1) == 1
        and support.support_denominator_gcd_p25_plus_1 == 3
        and support.support_denominator_gcd_aux126751_minus_1 == 2535
        and support.support_denominator_gcd_aux2029_minus_1 == 507
        and ambient_gcd == 11
        and root.fp_star_kernel_order == 11
        and support.proper_period_shortcuts_all_fail
        and all(branch.divisor_route_ok for branch in branches)
        and sum(int(branch.emitted_payload == "theta2_inverse") for branch in branches) == 2
        and sum(int(branch.emitted_payload == "theta2") for branch in branches) == 2
    )
    return RawOrientationValueRouteProfile(
        raw_orientation_router_ok=router.row_ok,
        support_period=SUPPORT_PERIOD,
        ambient_period=780,
        support_denominator_bit_length=support.support_denominator_bit_length,
        support_denominator_gcd_fp_star=support.support_denominator_gcd_p25_minus_1,
        support_denominator_gcd_fp2_norm=support.support_denominator_gcd_p25_plus_1,
        support_denominator_gcd_aux126751=support.support_denominator_gcd_aux126751_minus_1,
        support_denominator_gcd_aux2029=support.support_denominator_gcd_aux2029_minus_1,
        support_value_root_unique_fp_star=support.support_denominator_gcd_p25_minus_1 == 1,
        ambient_denominator_gcd_fp_star=ambient_gcd,
        ambient_value_branch_count_fp_star=root.fp_star_kernel_order,
        ambient_value_route_has_mu11_ambiguity=root.value_branches_are_distinct,
        proper_period_shortcuts_all_fail=support.proper_period_shortcuts_all_fail,
        branch_value_routes=branches,
        theta2_inverse_value_routes=sum(
            int(branch.emitted_payload == "theta2_inverse") for branch in branches
        ),
        theta2_value_routes=sum(int(branch.emitted_payload == "theta2") for branch in branches),
        value_level_obligation=(
            "value-level theorem hits must provide the period-156 theta2 "
            "fixedness/telescoping context; then 4^156-1 is invertible on "
            "F_p^*, while the ambient 780-period route has mu_11 ambiguity"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang raw orientation value-route gate")
    profile = profile_raw_orientation_value_route()
    print(f"raw_orientation_value_route_profile={profile}")
    print("value_route_denominators")
    print(f"  support_period={profile.support_period}")
    print(f"  support_denominator_bit_length={profile.support_denominator_bit_length}")
    print(f"  gcd_4^156_minus_1_with_Fp_star={profile.support_denominator_gcd_fp_star}")
    print(f"  gcd_4^156_minus_1_with_Fp2_norm={profile.support_denominator_gcd_fp2_norm}")
    print(f"  ambient_gcd_4^780_minus_1_with_Fp_star={profile.ambient_denominator_gcd_fp_star}")
    print(f"  ambient_value_branch_count_Fp_star={profile.ambient_value_branch_count_fp_star}")
    print("branch_value_routes")
    for branch in profile.branch_value_routes:
        print(
            "  "
            f"{branch.route_name}: emits={branch.emitted_payload} "
            f"sign={branch.recovered_sign} "
            f"divisor_route_ok={int(branch.divisor_route_ok)} "
            f"support_period_value_root_unique_Fp={int(branch.support_period_value_root_unique_fp)}"
        )
    print("interpretation")
    print("  divisor_or_additive_product_hits_route_through_the_existing_certificate_path=1")
    print("  value_level_hits_are_viable_only_with_period_156_theta2_context=1")
    print("  support_period_denominator_has_unique_Fp_star_root=1")
    print("  ambient_780_period_value_route_still_has_mu11_ambiguity=1")
    print("  proper_period_shortcuts_do_not_recover_the_bridge=1")
    print(
        "robert_ksy_theta2_kubert_lang_raw_orientation_value_route_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Route raw oriented KL/KSY products into the theta2 certificate path.

The raw orientation contract classifies four accepted product branches.  This
gate verifies that each branch feeds the existing theta2 candidate harness with
the expected sign:

    theta2 inverse -> finite resolvent recovers -bridge
    theta2         -> finite resolvent recovers  bridge

It is the executable handoff from a theorem/literature product hit to the
current finite certificate chain.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    KsyTheta2CandidateProfile,
    profile_theta2_candidate,
    theta2_sparse_entries,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    anti_invariant_y_footprint,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate import (
    RAW_CENTER,
    RAW_INVERSE_CENTER,
    RawOrientationCandidateProfile,
    profile_orientation_candidate,
    profile_raw_reflection_orientation_contract,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class RawOrientationCertificateRoute:
    name: str
    raw_center: Coord
    raw_d: Coord
    k_multiplier: int
    reverse: bool
    orientation_profile: RawOrientationCandidateProfile
    theta2_candidate_profile: KsyTheta2CandidateProfile
    emitted_payload: str
    expected_recovered_sign: int
    recovered_bridge_ok: bool
    certificate_path_ok: bool


@dataclass(frozen=True)
class RawOrientationCertificateRouterProfile:
    branch_routes: tuple[RawOrientationCertificateRoute, ...]
    theta2_inverse_routes: int
    theta2_routes: int
    all_routes_feed_certificate_chain: bool
    support_resolvent_term_budget: int
    support_resolvent_union_support: int
    wrong_center_route: RawOrientationCertificateRoute
    wrong_d_route: RawOrientationCertificateRoute
    nonprimitive_k_route: RawOrientationCertificateRoute
    controls_rejected: bool
    router_contract: str
    row_ok: bool


def primitive_k_step(k_multiplier: int) -> Coord:
    return scale_coord(KERNEL_SHIFT, k_multiplier % 25)


def route_raw_orientation(
    name: str,
    raw_center: Coord,
    raw_d: Coord,
    k_multiplier: int,
    reverse: bool,
) -> RawOrientationCertificateRoute:
    orientation = profile_orientation_candidate(name, raw_center, raw_d, k_multiplier, reverse)
    _centers, footprint = anti_invariant_y_footprint(
        raw_center,
        primitive_k_step(k_multiplier),
        raw_d,
        reverse=reverse,
    )
    theta2_candidate = profile_theta2_candidate(name, theta2_sparse_entries(footprint))
    emitted = (
        "theta2_inverse"
        if theta2_candidate.exact_theta2_inverse
        else "theta2"
        if theta2_candidate.exact_theta2
        else "neither"
    )
    expected_sign = -1 if emitted == "theta2_inverse" else 1 if emitted == "theta2" else 0
    route_ok = (
        orientation.ok
        and theta2_candidate.ok
        and theta2_candidate.recovered_sign == expected_sign
        and theta2_candidate.normalized_recovered_profile.ok
        and theta2_candidate.shifted_theta2_term_budget == 46800
        and theta2_candidate.shifted_theta2_union_support == 11700
    )
    return RawOrientationCertificateRoute(
        name=name,
        raw_center=raw_center,
        raw_d=raw_d,
        k_multiplier=k_multiplier % 25,
        reverse=reverse,
        orientation_profile=orientation,
        theta2_candidate_profile=theta2_candidate,
        emitted_payload=emitted,
        expected_recovered_sign=expected_sign,
        recovered_bridge_ok=theta2_candidate.normalized_recovered_profile.ok,
        certificate_path_ok=route_ok,
    )


def profile_raw_orientation_certificate_router() -> RawOrientationCertificateRouterProfile:
    branches = (
        route_raw_orientation("center_forward_route", RAW_CENTER, D_SHIFT, 1, False),
        route_raw_orientation("center_reverse_route", RAW_CENTER, D_SHIFT, 1, True),
        route_raw_orientation("inverse_center_forward_route", RAW_INVERSE_CENTER, D_SHIFT, 1, False),
        route_raw_orientation("inverse_center_reverse_route", RAW_INVERSE_CENTER, D_SHIFT, 1, True),
    )
    wrong_center = route_raw_orientation("wrong_center_route", (47, 29), D_SHIFT, 1, False)
    wrong_d = route_raw_orientation("wrong_d_route", RAW_CENTER, (22, 4), 1, False)
    nonprimitive_k = route_raw_orientation("nonprimitive_k_route", RAW_CENTER, D_SHIFT, 5, False)
    orientation_contract = profile_raw_reflection_orientation_contract()
    theta2_inverse_routes = sum(int(route.emitted_payload == "theta2_inverse") for route in branches)
    theta2_routes = sum(int(route.emitted_payload == "theta2") for route in branches)
    controls_rejected = (
        not wrong_center.certificate_path_ok
        and not wrong_d.certificate_path_ok
        and not nonprimitive_k.certificate_path_ok
        and not wrong_center.theta2_candidate_profile.ok
        and not wrong_d.theta2_candidate_profile.ok
        and not nonprimitive_k.theta2_candidate_profile.ok
    )
    row_ok = (
        RIGHT_ORDER == 75
        and C_ORDER == 169
        and orientation_contract.row_ok
        and all(route.certificate_path_ok for route in branches)
        and tuple((route.name, route.emitted_payload, route.theta2_candidate_profile.recovered_sign) for route in branches)
        == (
            ("center_forward_route", "theta2_inverse", -1),
            ("center_reverse_route", "theta2", 1),
            ("inverse_center_forward_route", "theta2", 1),
            ("inverse_center_reverse_route", "theta2_inverse", -1),
        )
        and theta2_inverse_routes == 2
        and theta2_routes == 2
        and all(route.theta2_candidate_profile.shifted_theta2_term_budget == 46800 for route in branches)
        and all(route.theta2_candidate_profile.shifted_theta2_union_support == 11700 for route in branches)
        and controls_rejected
        and gcd(5, 25) == 5
    )
    return RawOrientationCertificateRouterProfile(
        branch_routes=branches,
        theta2_inverse_routes=theta2_inverse_routes,
        theta2_routes=theta2_routes,
        all_routes_feed_certificate_chain=all(route.certificate_path_ok for route in branches),
        support_resolvent_term_budget=46800,
        support_resolvent_union_support=11700,
        wrong_center_route=wrong_center,
        wrong_d_route=wrong_d,
        nonprimitive_k_route=nonprimitive_k,
        controls_rejected=controls_rejected,
        router_contract=(
            "raw oriented product hit -> theta2/theta2_inverse classification "
            "-> finite support-period resolvent -> normalized bridge contract"
        ),
        row_ok=row_ok,
    )


def print_route(prefix: str, route: RawOrientationCertificateRoute) -> None:
    print(
        "  "
        f"{prefix}: center={route.raw_center} D={route.raw_d} "
        f"Kmult={route.k_multiplier} reverse={int(route.reverse)} "
        f"orientation_ok={int(route.orientation_profile.ok)} "
        f"emits={route.emitted_payload} sign={route.theta2_candidate_profile.recovered_sign} "
        f"bridge_ok={int(route.recovered_bridge_ok)} "
        f"route_ok={int(route.certificate_path_ok)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Route raw oriented KL/KSY product data into the theta2 finite "
            "certificate path."
        )
    )
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    parser.add_argument("--reverse", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang raw orientation certificate-router gate")
    supplied = (
        args.center_right is not None,
        args.center_c is not None,
        args.d_right is not None,
        args.d_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all four raw center/D coordinates must be supplied together")
        route = route_raw_orientation(
            "raw_orientation_certificate_candidate",
            (args.center_right, args.center_c),
            (args.d_right, args.d_c),
            args.k_multiplier,
            args.reverse,
        )
        print("mode=raw_orientation_certificate_candidate")
        print_route("candidate_route", route)
        print(
            "robert_ksy_theta2_kubert_lang_raw_orientation_certificate_candidate_rows="
            f"{int(route.certificate_path_ok)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_candidate")
        return 0 if route.certificate_path_ok else 1

    profile = profile_raw_orientation_certificate_router()
    print("branch_routes")
    for route in profile.branch_routes:
        print_route(route.name, route)
    print("router_counts")
    print(f"  theta2_inverse_routes={profile.theta2_inverse_routes}")
    print(f"  theta2_routes={profile.theta2_routes}")
    print(f"  all_routes_feed_certificate_chain={int(profile.all_routes_feed_certificate_chain)}")
    print(f"  support_resolvent_term_budget={profile.support_resolvent_term_budget}")
    print(f"  support_resolvent_union_support={profile.support_resolvent_union_support}")
    print_route("wrong_center_route", profile.wrong_center_route)
    print_route("wrong_d_route", profile.wrong_d_route)
    print_route("nonprimitive_k_route", profile.nonprimitive_k_route)
    print("interpretation")
    print("  raw_oriented_product_routes_to_theta2_candidate_harness=1")
    print("  theta2_inverse_routes_recover_negative_bridge=1")
    print("  theta2_routes_recover_bridge=1")
    print("  wrong_center_wrong_D_and_nonprimitive_K_do_not_route=1")
    print(
        "robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

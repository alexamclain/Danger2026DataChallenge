#!/usr/bin/env python3
"""Top-level theorem-hit router for the p25 KL/KSY anti-invariant target.

The finite spine intake handles several already-normalized verifier payloads.
The later raw KL/KSY gates added a stronger theorem-facing object:

    raw C, raw D, primitive K, and product orientation.

This router is the one-page executable landing pad for a future literature or
formula hit.  It classifies the hit by output type, then delegates the actual
checks to the specialized gates:

* finite-spine payloads go to the universal finite intake;
* raw divisor/additive products go to the raw orientation certificate router;
* raw finite-field values need the period-156 theta2 context before they are
  acceptable;
* ambient value-only and raw exponent-balance-only claims remain rejected.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate import (
    profile_anti_invariant_producer_contract,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_gate import (
    profile_anti_invariant_source_boundary,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate import (
    RawOrientationCertificateRoute,
    profile_raw_orientation_certificate_router,
    route_raw_orientation,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate import (
    profile_raw_orientation_value_route,
)
from p25_laneB_robert_ksy_theta2_universal_producer_intake import (
    default_universal_producer_intake_profile,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class TheoremHitRouterRow:
    name: str
    output_kind: str
    routed_by: str
    finite_accepts: bool
    theorem_status: str
    first_obligation_or_falsifier: str


@dataclass(frozen=True)
class TheoremHitRouterCandidate:
    output_type: str
    route: RawOrientationCertificateRoute
    period_156_context_supplied: bool
    finite_accepts: bool
    value_route_obligation_satisfied: bool
    decision: str
    first_obligation_or_falsifier: str


@dataclass(frozen=True)
class TheoremHitRouterProfile:
    finite_spine_intake_ok: bool
    anti_invariant_contract_ok: bool
    source_boundary_ok: bool
    raw_orientation_router_ok: bool
    raw_value_route_ok: bool
    accepted_rows: tuple[TheoremHitRouterRow, ...]
    rejected_or_conditional_rows: tuple[TheoremHitRouterRow, ...]
    raw_theta2_inverse_routes: int
    raw_theta2_routes: int
    value_support_period: int
    value_support_root_unique_fp: bool
    ambient_value_branch_count_fp: int
    compact_router_contract: str
    row_ok: bool


def profile_theorem_hit_router() -> TheoremHitRouterProfile:
    finite_spine = default_universal_producer_intake_profile()
    contract = profile_anti_invariant_producer_contract()
    source_boundary = profile_anti_invariant_source_boundary()
    raw_router = profile_raw_orientation_certificate_router()
    value_route = profile_raw_orientation_value_route()

    accepted = (
        TheoremHitRouterRow(
            "finite_spine_payload",
            "already-normalized finite verifier payload",
            "p25_laneB_robert_ksy_theta2_universal_producer_intake.py",
            finite_spine.row_ok,
            "accepted finite intake, not an arithmetic proof by itself",
            "must be accompanied by a challenge-legal arithmetic source",
        ),
        TheoremHitRouterRow(
            "raw_divisor_or_additive_product",
            "raw anti-invariant product emitting theta2/theta2^-1 data",
            "p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py",
            raw_router.row_ok,
            "accepted theorem-output type",
            "must satisfy exact raw C/D/primitive-K/orientation contract",
        ),
        TheoremHitRouterRow(
            "raw_value_product_with_period_156_context",
            "finite-field unit values for the raw product",
            "p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py",
            value_route.row_ok and value_route.support_value_root_unique_fp_star,
            "accepted only with explicit period-156 theta2 fixedness/telescoping",
            "without period-156 context this downgrades to the ambient value route",
        ),
    )

    rejected = (
        TheoremHitRouterRow(
            "ambient_780_value_only",
            "finite-field unit value on the ambient 780-period orbit",
            "p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py",
            not value_route.ambient_value_route_has_mu11_ambiguity,
            "rejected as a complete certificate route",
            "ambient route has mu_11 ambiguity over F_p^*",
        ),
        TheoremHitRouterRow(
            "wrong_raw_geometry",
            "raw product with wrong center, wrong D, or nonprimitive K",
            "p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py",
            not raw_router.controls_rejected,
            "rejected finite control",
            "does not emit theta2 or theta2^-1 for the bridge certificate",
        ),
        TheoremHitRouterRow(
            "raw_kl_exponent_balance_only",
            "Kubert-Lang exponent congruences without finite intake geometry",
            "p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate.py",
            not contract.raw_exponent_screen_saturated,
            "rejected as a producer claim",
            "raw exponent sums are saturated by many wrong anti-invariant packets",
        ),
        TheoremHitRouterRow(
            "generic_source_family_claim",
            "broad Robert/Siegel/KSY source without exact C/D/K payload",
            "p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_gate.py",
            False,
            "not accepted until instantiated",
            source_boundary.next_probe,
        ),
    )

    accepted_ok = all(row.finite_accepts for row in accepted)
    rejected_ok = all(not row.finite_accepts for row in rejected)
    row_ok = (
        finite_spine.row_ok
        and contract.row_ok
        and source_boundary.row_ok
        and raw_router.row_ok
        and value_route.row_ok
        and accepted_ok
        and rejected_ok
        and raw_router.theta2_inverse_routes == 2
        and raw_router.theta2_routes == 2
        and value_route.support_period == 156
        and value_route.support_value_root_unique_fp_star
        and value_route.ambient_value_branch_count_fp_star == 11
        and value_route.ambient_value_route_has_mu11_ambiguity
    )
    return TheoremHitRouterProfile(
        finite_spine_intake_ok=finite_spine.row_ok,
        anti_invariant_contract_ok=contract.row_ok,
        source_boundary_ok=source_boundary.row_ok,
        raw_orientation_router_ok=raw_router.row_ok,
        raw_value_route_ok=value_route.row_ok,
        accepted_rows=accepted,
        rejected_or_conditional_rows=rejected,
        raw_theta2_inverse_routes=raw_router.theta2_inverse_routes,
        raw_theta2_routes=raw_router.theta2_routes,
        value_support_period=value_route.support_period,
        value_support_root_unique_fp=value_route.support_value_root_unique_fp_star,
        ambient_value_branch_count_fp=value_route.ambient_value_branch_count_fp_star,
        compact_router_contract=(
            "theorem hit -> output type -> finite spine, raw divisor/additive "
            "router, or raw value route with period-156 theta2 context"
        ),
        row_ok=row_ok,
    )


def profile_theorem_hit_candidate(
    output_type: str,
    raw_center: Coord,
    raw_d: Coord,
    k_multiplier: int,
    reverse: bool,
    period_156_context_supplied: bool,
) -> TheoremHitRouterCandidate:
    route = route_raw_orientation(
        "theorem_hit_router_candidate",
        raw_center,
        raw_d,
        k_multiplier,
        reverse,
    )
    value_route = profile_raw_orientation_value_route()
    value_obligation_ok = (
        period_156_context_supplied
        and value_route.support_value_root_unique_fp_star
        and value_route.support_period == 156
    )

    if output_type in ("raw-divisor", "raw-additive"):
        ok = route.certificate_path_ok
        decision = "accept" if ok else "reject"
        falsifier = (
            "raw product routes to theta2/theta2^-1 certificate path"
            if ok
            else "raw product fails exact C/D/primitive-K/orientation route"
        )
    elif output_type == "raw-value":
        ok = route.certificate_path_ok and value_obligation_ok
        decision = "accept" if ok else "conditional_or_reject"
        falsifier = (
            "period-156 theta2 context supplied, so the F_p^* value root is unique"
            if ok
            else "value-level hit must include period-156 theta2 fixedness/telescoping"
        )
    elif output_type == "ambient-value":
        ok = False
        decision = "reject"
        falsifier = "ambient 780-period value route has mu_11 ambiguity"
    else:
        raise SystemExit(f"unsupported output type: {output_type}")

    return TheoremHitRouterCandidate(
        output_type=output_type,
        route=route,
        period_156_context_supplied=period_156_context_supplied,
        finite_accepts=ok,
        value_route_obligation_satisfied=value_obligation_ok,
        decision=decision,
        first_obligation_or_falsifier=falsifier,
    )


def require(value: int | None, name: str) -> int:
    if value is None:
        raise SystemExit(f"{name} is required for candidate mode")
    return value


def print_row(prefix: str, row: TheoremHitRouterRow) -> None:
    print(
        "  "
        f"{prefix}: kind={row.output_kind} accepts={int(row.finite_accepts)} "
        f"status={row.theorem_status} routed_by={row.routed_by}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Route p25 KL/KSY theorem hits by output type."
    )
    parser.add_argument(
        "--output-type",
        choices=("raw-divisor", "raw-additive", "raw-value", "ambient-value"),
    )
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--period-156-context", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang theorem-hit router gate")
    if args.output_type is not None:
        candidate = profile_theorem_hit_candidate(
            args.output_type,
            (require(args.center_right, "--center-right"), require(args.center_c, "--center-c")),
            (require(args.d_right, "--d-right"), require(args.d_c, "--d-c")),
            args.k_multiplier,
            args.reverse,
            args.period_156_context,
        )
        route = candidate.route
        print("mode=theorem_hit_router_candidate")
        print(
            "candidate_route="
            f"center={route.raw_center} D={route.raw_d} "
            f"Kmult={route.k_multiplier} reverse={int(route.reverse)} "
            f"emits={route.emitted_payload} sign={route.theta2_candidate_profile.recovered_sign} "
            f"route_ok={int(route.certificate_path_ok)}"
        )
        print(
            "candidate_decision="
            f"output_type={candidate.output_type} decision={candidate.decision} "
            f"value_period_context={int(candidate.period_156_context_supplied)} "
            f"accepts={int(candidate.finite_accepts)}"
        )
        print(f"first_obligation_or_falsifier={candidate.first_obligation_or_falsifier}")
        print(
            "robert_ksy_theta2_kubert_lang_theorem_hit_router_candidate_rows="
            f"{int(candidate.finite_accepts)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_candidate")
        return 0 if candidate.finite_accepts else 1

    profile = profile_theorem_hit_router()
    print(f"theorem_hit_router_profile={profile}")
    print("accepted_or_obligation_output_types")
    for row in profile.accepted_rows:
        print_row(row.name, row)
    print("rejected_or_not_yet_instantiated_output_types")
    for row in profile.rejected_or_conditional_rows:
        print_row(row.name, row)
    print("router_counts")
    print(f"  raw_theta2_inverse_routes={profile.raw_theta2_inverse_routes}")
    print(f"  raw_theta2_routes={profile.raw_theta2_routes}")
    print(f"  value_support_period={profile.value_support_period}")
    print(f"  value_support_root_unique_Fp={int(profile.value_support_root_unique_fp)}")
    print(f"  ambient_value_branch_count_Fp={profile.ambient_value_branch_count_fp}")
    print("interpretation")
    print("  future_lit_hits_should_be_classified_by_output_type_before_falsification=1")
    print("  divisor_or_additive_raw_products_route_directly_to_certificate_path=1")
    print("  value_level_raw_products_need_period_156_theta2_context=1")
    print("  ambient_value_only_and_raw_exponent_balance_only_claims_are_rejected=1")
    print(
        "robert_ksy_theta2_kubert_lang_theorem_hit_router_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Claim-intake classifier for p25 KSY-y source-anchor hits.

Use this gate when a literature scout, theorem snippet, or Drew-policy answer
arrives.  It classifies the claim against the closure-template requirements:

* exact divisor/additive identity for P closes the route;
* exact value identity for P closes only with period-156 context;
* policy acceptance helps but is not a theorem;
* generic field generation, ambient values, and exponent hygiene alone do not
  count as moonshot progress.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_gate import (
    profile_primary_source_anchor_packet,
)


LIVE_ANCHORS = {
    "ksy_theorem_5_3_ray_class_generation",
    "ksy_normalized_y_siegel_formula",
    "siegel_robert_value_units",
    "sprang_prop_5_4_kato_siegel_dlog",
    "kubert_lang_siegel_functions_generators",
    "danger3_policy_finite_field_identity",
}


@dataclass(frozen=True)
class SourceClaim:
    name: str
    anchor_name: str
    output_kind: str
    exact_product_p: bool
    mixed_graph_selector: bool
    period_156_context: bool
    finite_field_identity: bool
    divisor_or_additive: bool
    policy_accepts_finite_identity: bool


@dataclass(frozen=True)
class SourceClaimDecision:
    claim: SourceClaim
    anchor_known: bool
    decision: str
    closes_route: bool
    unblocks_policy: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class SourceClaimIntakeProfile:
    anchor_packet_ok: bool
    regression_claims: tuple[SourceClaimDecision, ...]
    closing_claims: int
    conditional_claims: int
    policy_only_claims: int
    rejected_claims: int
    row_ok: bool


def classify_claim(claim: SourceClaim) -> SourceClaimDecision:
    anchor_known = claim.anchor_name in LIVE_ANCHORS or claim.anchor_name == "generic_field_generation_or_ambient_value"

    if not anchor_known:
        return SourceClaimDecision(
            claim=claim,
            anchor_known=False,
            decision="reject_unknown_anchor",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="claim does not name a known anchor row",
            next_action="map the claim to a named primary-source anchor before spending theory effort",
            row_ok=True,
        )

    if claim.output_kind == "field-generation" or claim.anchor_name == "generic_field_generation_or_ambient_value":
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_not_closure_theorem",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="not an exact finite-field identity for P",
            next_action="discard unless reframed as exact product or exact value with period-156 context",
            row_ok=True,
        )

    if claim.output_kind == "exponent-hygiene":
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_exponent_hygiene_only",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="mixed C_75 x C_169 graph selector and finite intake",
            next_action="ask for exact graph selection, not only Kubert-Lang congruence conditions",
            row_ok=True,
        )

    if claim.anchor_name == "danger3_policy_finite_field_identity":
        if claim.policy_accepts_finite_identity:
            return SourceClaimDecision(
                claim=claim,
                anchor_known=True,
                decision="policy_unblocked_not_theorem",
                closes_route=False,
                unblocks_policy=True,
                first_missing_clause="a closing source theorem for P is still required",
                next_action="continue on exact product/value theorem with policy ambiguity removed",
                row_ok=True,
            )
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="policy_still_unknown",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="DANGER3 acceptance boundary not answered",
            next_action="ask whether a finite-field identity for P is challenge-legal",
            row_ok=True,
        )

    if not claim.exact_product_p:
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_exact_product",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="exact product P with C=(47,28), D=(22,3), K=(57,0)",
            next_action="ask the anchor to emit exact P, not a broad source statement",
            row_ok=True,
        )

    if not claim.mixed_graph_selector:
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_mixed_graph",
            closes_route=False,
            unblocks_policy=False,
            first_missing_clause="mixed C_75 x C_169 graph selector",
            next_action="ask for preservation of the exact 75 atoms and mixed source graph",
            row_ok=True,
        )

    if claim.divisor_or_additive or claim.output_kind == "divisor-additive":
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="closing_divisor_or_additive_identity",
            closes_route=True,
            unblocks_policy=False,
            first_missing_clause="none",
            next_action="route through theta2-inverse certificate path and DANGER3 policy check if needed",
            row_ok=True,
        )

    if claim.output_kind == "value":
        if not claim.finite_field_identity:
            return SourceClaimDecision(
                claim=claim,
                anchor_known=True,
                decision="conditional_missing_finite_field_identity",
                closes_route=False,
                unblocks_policy=False,
                first_missing_clause="finite-field identity for P",
                next_action="ask for a finite-field value identity, not ambient complex/class-field data",
                row_ok=True,
            )
        if not claim.period_156_context:
            return SourceClaimDecision(
                claim=claim,
                anchor_known=True,
                decision="conditional_missing_period_156_context",
                closes_route=False,
                unblocks_policy=False,
                first_missing_clause="period-156 branch/root/telescoping context",
                next_action="ask for support-period fixedness so the F_p^* root is unique",
                row_ok=True,
            )
        return SourceClaimDecision(
            claim=claim,
            anchor_known=True,
            decision="closing_value_identity_with_period_156",
            closes_route=True,
            unblocks_policy=False,
            first_missing_clause="none",
            next_action="route through value-with-period certificate path and DANGER3 policy check if needed",
            row_ok=True,
        )

    return SourceClaimDecision(
        claim=claim,
        anchor_known=True,
        decision="conditional_unclassified_output_kind",
        closes_route=False,
        unblocks_policy=False,
        first_missing_clause="output kind must be divisor-additive or value-with-period",
        next_action="restate the claim in closure-template terms",
        row_ok=True,
    )


def regression_claims() -> tuple[SourceClaim, ...]:
    return (
        SourceClaim(
            "ksy_exact_product_divisor",
            "ksy_normalized_y_siegel_formula",
            "divisor-additive",
            True,
            True,
            False,
            False,
            True,
            False,
        ),
        SourceClaim(
            "siegel_value_with_period",
            "ksy_normalized_y_siegel_formula",
            "value",
            True,
            True,
            True,
            True,
            False,
            False,
        ),
        SourceClaim(
            "exact_value_without_period",
            "siegel_robert_value_units",
            "value",
            True,
            True,
            False,
            True,
            False,
            False,
        ),
        SourceClaim(
            "ksy_generic_field_generation",
            "ksy_theorem_5_3_ray_class_generation",
            "field-generation",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        SourceClaim(
            "kubert_lang_exponent_only",
            "kubert_lang_siegel_functions_generators",
            "exponent-hygiene",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        SourceClaim(
            "danger3_policy_yes",
            "danger3_policy_finite_field_identity",
            "policy",
            False,
            False,
            False,
            False,
            False,
            True,
        ),
        SourceClaim(
            "unknown_anchor_control",
            "unnamed_relevant_source",
            "divisor-additive",
            True,
            True,
            False,
            False,
            True,
            False,
        ),
    )


def profile_source_claim_intake() -> SourceClaimIntakeProfile:
    anchor_packet = profile_primary_source_anchor_packet()
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    closing = sum(int(decision.closes_route) for decision in decisions)
    policy_only = sum(int(decision.unblocks_policy and not decision.closes_route) for decision in decisions)
    rejected = sum(int(decision.decision.startswith("reject")) for decision in decisions)
    conditional = len(decisions) - closing - policy_only - rejected

    expected_decisions = {
        "ksy_exact_product_divisor": "closing_divisor_or_additive_identity",
        "siegel_value_with_period": "closing_value_identity_with_period_156",
        "exact_value_without_period": "conditional_missing_period_156_context",
        "ksy_generic_field_generation": "reject_not_closure_theorem",
        "kubert_lang_exponent_only": "reject_exponent_hygiene_only",
        "danger3_policy_yes": "policy_unblocked_not_theorem",
        "unknown_anchor_control": "reject_unknown_anchor",
    }
    row_ok = (
        anchor_packet.row_ok
        and len(decisions) == 7
        and closing == 2
        and conditional == 1
        and policy_only == 1
        and rejected == 3
        and all(decision.row_ok for decision in decisions)
        and all(
            decision.decision == expected_decisions[decision.claim.name]
            for decision in decisions
        )
    )
    return SourceClaimIntakeProfile(
        anchor_packet_ok=anchor_packet.row_ok,
        regression_claims=decisions,
        closing_claims=closing,
        conditional_claims=conditional,
        policy_only_claims=policy_only,
        rejected_claims=rejected,
        row_ok=row_ok,
    )


def claim_from_args(args: argparse.Namespace) -> SourceClaim:
    return SourceClaim(
        name=args.name,
        anchor_name=args.anchor,
        output_kind=args.output_kind,
        exact_product_p=args.exact_product,
        mixed_graph_selector=args.mixed_graph,
        period_156_context=args.period_156,
        finite_field_identity=args.finite_field_identity,
        divisor_or_additive=args.divisor_additive,
        policy_accepts_finite_identity=args.policy_accepts_finite_identity,
    )


def print_decision(decision: SourceClaimDecision) -> None:
    print(
        "  "
        f"{decision.claim.name}: decision={decision.decision} "
        f"closes={int(decision.closes_route)} "
        f"policy={int(decision.unblocks_policy)} "
        f"missing={decision.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--anchor", default="ksy_normalized_y_siegel_formula")
    parser.add_argument(
        "--output-kind",
        default="value",
        choices=("divisor-additive", "value", "field-generation", "exponent-hygiene", "policy"),
    )
    parser.add_argument("--exact-product", action="store_true")
    parser.add_argument("--mixed-graph", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--finite-field-identity", action="store_true")
    parser.add_argument("--divisor-additive", action="store_true")
    parser.add_argument("--policy-accepts-finite-identity", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang KSY-y source-claim intake gate")
    if args.candidate:
        decision = classify_claim(claim_from_args(args))
        print(f"source_claim_candidate_decision={decision}")
        print_decision(decision)
        print(
            "robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_candidate_rows="
            f"{int(decision.row_ok)}/1"
        )
        return 0 if decision.row_ok else 1

    profile = profile_source_claim_intake()
    print(f"source_claim_intake_profile={profile}")
    print("regression_claims")
    for decision in profile.regression_claims:
        print_decision(decision)
    print("claim_counts")
    print(f"  closing_claims={profile.closing_claims}")
    print(f"  conditional_claims={profile.conditional_claims}")
    print(f"  policy_only_claims={profile.policy_only_claims}")
    print(f"  rejected_claims={profile.rejected_claims}")
    print("interpretation")
    print("  exact_divisor_additive_claim_closes=1")
    print("  exact_value_claim_closes_only_with_period_156=1")
    print("  policy_yes_is_not_a_theorem=1")
    print("  generic_generation_and_exponent_hygiene_are_rejected=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

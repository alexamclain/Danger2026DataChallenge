#!/usr/bin/env python3
"""Exact-product intake gate for p25 KSY-y producer claims.

The period-value gate handles finite-field value claims.  This gate handles
the stronger route: a source theorem that emits the exact divisor/additive
KSY-y product identity.  Such a theorem can feed the existing theta2 certificate
path without solving the value-root branch problem.

The gate is intentionally lightweight.  It encodes the upstream finite
contract and p24 transfer lesson as an intake classifier:

* exact P, mixed graph, equal weights, orientation, arithmetic producer, and
  challenge-legal framing close;
* formula language or finite verifier payloads without a producer are
  conditional;
* generic field generation, subgroup shortcuts, exponent hygiene, and wrong
  geometry are rejected.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


LIVE_PRODUCT_ANCHORS = {
    "ksy_normalized_y_siegel_formula",
    "sprang_prop_5_4_kato_siegel_dlog",
    "kubert_lang_siegel_functions_generators",
    "siegel_robert_value_units",
    "danger3_policy_finite_field_identity",
}


@dataclass(frozen=True)
class ExactProductClaim:
    name: str
    anchor_name: str
    output_kind: str
    exact_product_p: bool
    mixed_graph_selector: bool
    equal_weight_atoms: bool
    orientation_branch: bool
    arithmetic_producer: bool
    challenge_legal: bool
    finite_intake_geometry: bool


@dataclass(frozen=True)
class ExactProductDecision:
    claim: ExactProductClaim
    anchor_known: bool
    decision: str
    closes_route: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class ExactProductIntakeProfile:
    product_contract: str
    finite_budget: str
    regression_claims: tuple[ExactProductDecision, ...]
    closing_product_claims: int
    conditional_product_claims: int
    rejected_product_claims: int
    row_ok: bool


def classify_claim(claim: ExactProductClaim) -> ExactProductDecision:
    anchor_known = claim.anchor_name in LIVE_PRODUCT_ANCHORS
    if not anchor_known:
        return ExactProductDecision(
            claim=claim,
            anchor_known=False,
            decision="reject_unknown_anchor",
            closes_route=False,
            first_missing_clause="claim does not name a known product anchor",
            next_action="map the claim to KSY, Sprang, Kubert-Lang, Siegel-Robert, or DANGER3 policy",
            row_ok=True,
        )

    if claim.output_kind == "field-generation":
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_field_generation_not_product_identity",
            closes_route=False,
            first_missing_clause="exact divisor/additive identity for P",
            next_action="discard unless reframed as an exact finite product identity",
            row_ok=True,
        )

    if claim.output_kind == "subgroup":
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_literal_subgroup_shortcut",
            closes_route=False,
            first_missing_clause="non-subgroup D segment and K-trace support",
            next_action="discard literal Robert/Kato subgroup support for this D segment",
            row_ok=True,
        )

    if claim.output_kind == "exponent-hygiene":
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_exponent_hygiene_not_selector",
            closes_route=False,
            first_missing_clause="finite intake geometry and exact mixed row graph",
            next_action="ask for product geometry, not only KL congruences",
            row_ok=True,
        )

    if claim.output_kind == "finite-verifier":
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_verifier_without_arithmetic_producer",
            closes_route=False,
            first_missing_clause="challenge-legal arithmetic producer theorem",
            next_action="keep as verifier payload; require a source theorem before closure",
            row_ok=True,
        )

    if claim.output_kind == "formula-language" and not claim.arithmetic_producer:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_formula_language_without_product_proof",
            closes_route=False,
            first_missing_clause="proof that the formula emits exact P",
            next_action="specialize the formula to exact C,D,K atoms and product orientation",
            row_ok=True,
        )

    if not claim.exact_product_p:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_exact_product",
            closes_route=False,
            first_missing_clause="exact product P with C=(47,28), D=(22,3), K=(57,0)",
            next_action="ask for exact P, not a nearby product family",
            row_ok=True,
        )

    if not claim.mixed_graph_selector:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_mixed_graph",
            closes_route=False,
            first_missing_clause="mixed C_75 x C_169 graph selector",
            next_action="ask for row/C graph preservation, not a C-axis projection",
            row_ok=True,
        )

    if not claim.finite_intake_geometry:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_finite_intake_geometry",
            closes_route=False,
            first_missing_clause="finite theta2/source-packet intake geometry",
            next_action="feed the claimed product through source-packet or theta2 intake",
            row_ok=True,
        )

    if not claim.equal_weight_atoms:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="reject_nonuniform_atom_weights",
            closes_route=False,
            first_missing_clause="equal weights on all 75 atoms",
            next_action="discard missing, doubled, mixed-sign, or nonuniform K-layer variants",
            row_ok=True,
        )

    if not claim.orientation_branch:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_orientation",
            closes_route=False,
            first_missing_clause="theta2/theta2-inverse orientation branch",
            next_action="record whether the theorem emits theta2 or theta2 inverse",
            row_ok=True,
        )

    if not claim.arithmetic_producer:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_missing_arithmetic_producer",
            closes_route=False,
            first_missing_clause="arithmetic theorem, not only local finite equality",
            next_action="attach a source theorem that produces the product identity",
            row_ok=True,
        )

    if not claim.challenge_legal:
        return ExactProductDecision(
            claim=claim,
            anchor_known=True,
            decision="conditional_policy_or_framing_missing",
            closes_route=False,
            first_missing_clause="DANGER3-legal non-CM or finite-field framing",
            next_action="ask whether this finite-field product identity avoids the no-CM concern",
            row_ok=True,
        )

    return ExactProductDecision(
        claim=claim,
        anchor_known=True,
        decision="closing_exact_product_identity",
        closes_route=True,
        first_missing_clause="none",
        next_action="route through theta2/theta2-inverse certificate path",
        row_ok=True,
    )


def regression_claims() -> tuple[ExactProductClaim, ...]:
    return (
        ExactProductClaim(
            "ksy_exact_divisor_identity",
            "ksy_normalized_y_siegel_formula",
            "divisor-additive",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
        ExactProductClaim(
            "sprang_d2_exact_additive_identity",
            "sprang_prop_5_4_kato_siegel_dlog",
            "divisor-additive",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
        ExactProductClaim(
            "kubert_lang_exact_mixed_product_identity",
            "kubert_lang_siegel_functions_generators",
            "divisor-additive",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ),
        ExactProductClaim(
            "ksy_formula_language_only",
            "ksy_normalized_y_siegel_formula",
            "formula-language",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        ExactProductClaim(
            "finite_theta2_payload_without_source",
            "ksy_normalized_y_siegel_formula",
            "finite-verifier",
            True,
            True,
            True,
            True,
            False,
            True,
            True,
        ),
        ExactProductClaim(
            "exact_product_policy_unknown",
            "danger3_policy_finite_field_identity",
            "divisor-additive",
            True,
            True,
            True,
            True,
            True,
            False,
            True,
        ),
        ExactProductClaim(
            "generic_ksy_ray_class_generation",
            "ksy_normalized_y_siegel_formula",
            "field-generation",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        ExactProductClaim(
            "literal_robert_subgroup_support",
            "siegel_robert_value_units",
            "subgroup",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        ExactProductClaim(
            "kl_exponent_hygiene_only",
            "kubert_lang_siegel_functions_generators",
            "exponent-hygiene",
            False,
            False,
            False,
            False,
            False,
            True,
            False,
        ),
        ExactProductClaim(
            "nonuniform_weighted_product",
            "ksy_normalized_y_siegel_formula",
            "divisor-additive",
            True,
            True,
            False,
            True,
            True,
            True,
            True,
        ),
    )


def profile_exact_product_intake() -> ExactProductIntakeProfile:
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    closing = sum(int(row.closes_route) for row in decisions)
    conditional = sum(int(row.decision.startswith("conditional")) for row in decisions)
    rejected = sum(int(row.decision.startswith("reject")) for row in decisions)
    row_ok = (
        len(decisions) == 10
        and closing == 3
        and conditional == 3
        and rejected == 4
        and all(row.anchor_known for row in decisions)
        and all(row.row_ok for row in decisions)
        and all(
            not row.closes_route
            for row in decisions
            if row.claim.output_kind
            in ("field-generation", "subgroup", "exponent-hygiene", "finite-verifier")
        )
    )
    return ExactProductIntakeProfile(
        product_contract=(
            "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
            "C=(47,28), D=(22,3), K=(57,0), equal weights, orientation recorded"
        ),
        finite_budget="75 atoms, 300-term theta2 footprint, 31-cell factor budget, 975-cell compact witness",
        regression_claims=decisions,
        closing_product_claims=closing,
        conditional_product_claims=conditional,
        rejected_product_claims=rejected,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> ExactProductClaim:
    return ExactProductClaim(
        name=args.name,
        anchor_name=args.anchor,
        output_kind=args.output_kind,
        exact_product_p=args.exact_product,
        mixed_graph_selector=args.mixed_graph,
        equal_weight_atoms=args.equal_weight,
        orientation_branch=args.orientation,
        arithmetic_producer=args.arithmetic_producer,
        challenge_legal=args.challenge_legal,
        finite_intake_geometry=args.finite_intake,
    )


def print_decision(row: ExactProductDecision) -> None:
    claim = row.claim
    print(
        "  "
        f"{claim.name}: anchor={claim.anchor_name} kind={claim.output_kind} "
        f"exactP={int(claim.exact_product_p)} graph={int(claim.mixed_graph_selector)} "
        f"equal={int(claim.equal_weight_atoms)} orient={int(claim.orientation_branch)} "
        f"producer={int(claim.arithmetic_producer)} legal={int(claim.challenge_legal)} "
        f"finite={int(claim.finite_intake_geometry)} closes={int(row.closes_route)} "
        f"decision={row.decision} missing={row.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify exact-product KSY-y producer claims.")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--anchor", default="ksy_normalized_y_siegel_formula")
    parser.add_argument(
        "--output-kind",
        choices=(
            "divisor-additive",
            "formula-language",
            "finite-verifier",
            "field-generation",
            "subgroup",
            "exponent-hygiene",
        ),
        default="divisor-additive",
    )
    parser.add_argument("--exact-product", action="store_true")
    parser.add_argument("--mixed-graph", action="store_true")
    parser.add_argument("--equal-weight", action="store_true")
    parser.add_argument("--orientation", action="store_true")
    parser.add_argument("--arithmetic-producer", action="store_true")
    parser.add_argument("--challenge-legal", action="store_true")
    parser.add_argument("--finite-intake", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang KSY-y exact-product intake gate")
    if args.candidate:
        decision = classify_claim(candidate_from_args(args))
        print("mode=exact_product_candidate")
        print_decision(decision)
        print(
            "robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_candidate_rows="
            f"{int(decision.closes_route)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_candidate")
        return 0 if decision.closes_route else 1

    profile = profile_exact_product_intake()
    print(f"exact_product_intake_profile={profile}")
    print("product_contract")
    print(f"  {profile.product_contract}")
    print(f"  finite_budget={profile.finite_budget}")
    print("regression_rows")
    for row in profile.regression_claims:
        print_decision(row)
    print("counts")
    print(f"  closing_product_claims={profile.closing_product_claims}")
    print(f"  conditional_product_claims={profile.conditional_product_claims}")
    print(f"  rejected_product_claims={profile.rejected_product_claims}")
    print("interpretation")
    print("  exact_product_identity_closes_divisor_additive_route=1")
    print("  formula_language_without_producer_is_conditional=1")
    print("  finite_verifier_payload_without_source_theorem_is_conditional=1")
    print("  field_generation_subgroup_and_exponent_hygiene_shortcuts_are_rejected=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

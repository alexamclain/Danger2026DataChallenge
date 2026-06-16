#!/usr/bin/env python3
"""Koo-Shin theorem-clause intake for the p25 KSY-y moonshot.

This gate is the handoff target for a future full-text/OCR/subagent result for
Koo-Shin 2010 Theorem 5.2.  It classifies theorem clauses by what they actually
emit, so "odd-prime product theorem" or "Kubert-Lang congruence criterion" does
not accidentally become an exact p25 source theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    ClosingTheoremClaim,
    classify_claim as classify_closing_theorem,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate import (
    ExactProductClaim,
    classify_claim as classify_exact_product,
)


@dataclass(frozen=True)
class KooShinTheoremClauseClaim:
    name: str
    theorem_body_verified: bool
    product_or_distribution_theorem: bool
    modularity_hygiene_only: bool
    odd_prime_or_prime_power_only: bool
    mixed_level_lift: bool
    exact_product_p: bool
    mixed_graph_selector: bool
    equal_weight_atoms: bool
    orientation_branch: bool
    arithmetic_producer: bool
    output_kind: str
    finite_field_identity_for_p: bool
    period_156_context: bool
    danger3_framing: bool
    extraction_to_A_x0: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class KooShinTheoremClauseDecision:
    claim: KooShinTheoremClauseClaim
    decision: str
    exact_product_decision: str | None
    closing_theorem_decision: str | None
    source_theorem_closed: bool
    danger3_route_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class KooShinTheoremClauseIntakeProfile:
    regression_rows: tuple[KooShinTheoremClauseDecision, ...]
    theorem_body_rows: int
    hygiene_only_rows: int
    prime_power_only_rows: int
    exact_p_rows: int
    mixed_graph_rows: int
    source_theorem_closed_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_rows: int
    conditional_rows: int
    row_ok: bool


def exact_product_decision_for(claim: KooShinTheoremClauseClaim) -> str:
    exact_claim = ExactProductClaim(
        name=claim.name,
        anchor_name="kubert_lang_siegel_functions_generators",
        output_kind=claim.output_kind,
        exact_product_p=claim.exact_product_p,
        mixed_graph_selector=claim.mixed_graph_selector,
        equal_weight_atoms=claim.equal_weight_atoms,
        orientation_branch=claim.orientation_branch,
        arithmetic_producer=claim.arithmetic_producer,
        challenge_legal=claim.danger3_framing,
        finite_intake_geometry=claim.mixed_level_lift,
    )
    return classify_exact_product(exact_claim).decision


def closing_claim_for(claim: KooShinTheoremClauseClaim) -> ClosingTheoremClaim:
    return ClosingTheoremClaim(
        name=claim.name,
        source_family="Koo-Shin 2010 / Kubert-Lang",
        emits_exact_p=claim.exact_product_p,
        preserves_mixed_graph=claim.mixed_graph_selector,
        equal_weight_atoms=claim.equal_weight_atoms,
        orientation_recorded=claim.orientation_branch,
        arithmetic_source_theorem=claim.arithmetic_producer,
        output_kind=claim.output_kind,
        finite_field_identity_for_p=claim.finite_field_identity_for_p,
        period_156_context=claim.period_156_context,
        danger3_policy_or_non_cm_framing=claim.danger3_framing,
        extraction_to_A_x0=claim.extraction_to_A_x0,
        concrete_vpp_verified_triple=claim.concrete_vpp_verified_triple,
    )


def classify_claim(claim: KooShinTheoremClauseClaim) -> KooShinTheoremClauseDecision:
    if not claim.theorem_body_verified:
        return KooShinTheoremClauseDecision(
            claim=claim,
            decision="reject_no_theorem_body",
            exact_product_decision=None,
            closing_theorem_decision=None,
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="full Koo-Shin theorem statement/OCR",
            next_action="retrieve theorem body before using the lead",
            row_ok=True,
        )

    if not claim.product_or_distribution_theorem:
        return KooShinTheoremClauseDecision(
            claim=claim,
            decision="reject_not_product_distribution_theorem",
            exact_product_decision=None,
            closing_theorem_decision=None,
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="product/distribution theorem for Siegel functions",
            next_action="keep as context only",
            row_ok=True,
        )

    if claim.modularity_hygiene_only:
        exact_decision = exact_product_decision_for(claim)
        return KooShinTheoremClauseDecision(
            claim=claim,
            decision="reject_modularity_hygiene_only",
            exact_product_decision=exact_decision,
            closing_theorem_decision=None,
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact product P and mixed row graph, not only congruence criteria",
            next_action="use as a necessary screen; do not treat as producer",
            row_ok=exact_decision.startswith("reject_"),
        )

    if claim.odd_prime_or_prime_power_only and not claim.mixed_level_lift:
        exact_decision = exact_product_decision_for(claim)
        return KooShinTheoremClauseDecision(
            claim=claim,
            decision="reject_prime_power_only_missing_mixed_lift",
            exact_product_decision=exact_decision,
            closing_theorem_decision=None,
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="mixed-level lift preserving C_3 row graph and T edge",
            next_action="ask whether the theorem lifts from odd-prime/prime-power data to levels 507 and 12675",
            row_ok=exact_decision in {
                "conditional_missing_exact_product",
                "conditional_missing_mixed_graph",
                "conditional_missing_finite_intake_geometry",
            },
        )

    exact_decision = exact_product_decision_for(claim)
    closing = classify_closing_theorem(closing_claim_for(claim))
    if not claim.exact_product_p:
        decision = "conditional_product_theorem_not_exact_p"
    elif not claim.mixed_graph_selector:
        decision = "reject_exact_product_missing_mixed_graph"
    elif not claim.equal_weight_atoms:
        decision = "reject_exact_product_nonuniform_atoms"
    elif not claim.orientation_branch:
        decision = "conditional_exact_product_missing_orientation"
    elif not claim.arithmetic_producer:
        decision = "conditional_exact_product_missing_arithmetic_producer"
    elif closing.source_theorem_closed and not closing.danger3_route_unblocked:
        decision = "source_theorem_closed_policy_or_framing_missing"
    elif closing.danger3_route_unblocked and not closing.extraction_ready:
        decision = "danger3_unblocked_extraction_missing"
    elif closing.extraction_ready and not closing.submission_ready:
        decision = "ready_to_extract_and_verify_concrete_triple"
    elif closing.submission_ready:
        decision = "submission_ready_verified_triple"
    else:
        decision = closing.decision

    return KooShinTheoremClauseDecision(
        claim=claim,
        decision=decision,
        exact_product_decision=exact_decision,
        closing_theorem_decision=closing.decision,
        source_theorem_closed=closing.source_theorem_closed,
        danger3_route_unblocked=closing.danger3_route_unblocked,
        extraction_ready=closing.extraction_ready,
        submission_ready=closing.submission_ready,
        first_missing_clause=closing.first_missing_clause,
        next_action=closing.next_action,
        row_ok=True,
    )


def regression_claims() -> tuple[KooShinTheoremClauseClaim, ...]:
    base = {
        "theorem_body_verified": True,
        "product_or_distribution_theorem": True,
        "modularity_hygiene_only": False,
        "odd_prime_or_prime_power_only": False,
        "mixed_level_lift": True,
        "exact_product_p": True,
        "mixed_graph_selector": True,
        "equal_weight_atoms": True,
        "orientation_branch": True,
        "arithmetic_producer": True,
        "output_kind": "divisor-additive",
        "finite_field_identity_for_p": True,
        "period_156_context": False,
        "danger3_framing": True,
        "extraction_to_A_x0": True,
        "concrete_vpp_verified_triple": False,
    }
    return (
        KooShinTheoremClauseClaim(
            "search_snippet_only",
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            "divisor-additive",
            False,
            False,
            False,
            False,
            False,
        ),
        KooShinTheoremClauseClaim(
            "kl_modularity_criterion_only",
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "exponent-hygiene",
            False,
            False,
            False,
            False,
            False,
        ),
        KooShinTheoremClauseClaim(
            "odd_prime_c169_product_only",
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            True,
            "divisor-additive",
            False,
            False,
            False,
            False,
            False,
        ),
        KooShinTheoremClauseClaim(
            "exact_p_missing_orientation",
            **{**base, "orientation_branch": False},
        ),
        KooShinTheoremClauseClaim(
            "exact_p_no_arithmetic_producer",
            **{**base, "arithmetic_producer": False},
        ),
        KooShinTheoremClauseClaim(
            "exact_product_policy_unknown",
            **{**base, "danger3_framing": False, "extraction_to_A_x0": False},
        ),
        KooShinTheoremClauseClaim(
            "period_value_missing_period_context",
            **{**base, "output_kind": "period-value", "period_156_context": False},
        ),
        KooShinTheoremClauseClaim(
            "period_value_with_policy_no_extraction",
            **{**base, "output_kind": "period-value", "period_156_context": True, "extraction_to_A_x0": False},
        ),
        KooShinTheoremClauseClaim("full_theorem_ready_for_vpp", **base),
        KooShinTheoremClauseClaim(
            "verified_p25_triple",
            **{**base, "concrete_vpp_verified_triple": True},
        ),
    )


def profile_koo_shin_theorem_clause_intake() -> KooShinTheoremClauseIntakeProfile:
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    theorem_body_rows = sum(row.claim.theorem_body_verified for row in decisions)
    hygiene_only_rows = sum(row.decision == "reject_modularity_hygiene_only" for row in decisions)
    prime_power_only_rows = sum(
        row.decision == "reject_prime_power_only_missing_mixed_lift" for row in decisions
    )
    exact_p_rows = sum(row.claim.exact_product_p for row in decisions)
    mixed_graph_rows = sum(row.claim.mixed_graph_selector for row in decisions)
    source_theorem_closed_rows = sum(row.source_theorem_closed for row in decisions)
    danger3_unblocked_rows = sum(row.danger3_route_unblocked for row in decisions)
    extraction_ready_rows = sum(row.extraction_ready for row in decisions)
    submission_ready_rows = sum(row.submission_ready for row in decisions)
    rejected_rows = sum(row.decision.startswith("reject_") for row in decisions)
    conditional_rows = sum(
        row.decision.startswith(("conditional_", "source_theorem_", "danger3_", "ready_"))
        for row in decisions
    )
    expected_decisions = (
        "reject_no_theorem_body",
        "reject_modularity_hygiene_only",
        "reject_prime_power_only_missing_mixed_lift",
        "conditional_exact_product_missing_orientation",
        "conditional_exact_product_missing_arithmetic_producer",
        "source_theorem_closed_policy_or_framing_missing",
        "conditional_value_missing_period_156",
        "danger3_unblocked_extraction_missing",
        "ready_to_extract_and_verify_concrete_triple",
        "submission_ready_verified_triple",
    )
    row_ok = (
        len(decisions) == 10
        and theorem_body_rows == 9
        and hygiene_only_rows == 1
        and prime_power_only_rows == 1
        and exact_p_rows == 8
        and mixed_graph_rows == 7
        and source_theorem_closed_rows == 4
        and danger3_unblocked_rows == 3
        and extraction_ready_rows == 2
        and submission_ready_rows == 1
        and rejected_rows == 3
        and conditional_rows == 6
        and tuple(row.decision for row in decisions) == expected_decisions
        and all(row.row_ok for row in decisions)
    )
    return KooShinTheoremClauseIntakeProfile(
        regression_rows=decisions,
        theorem_body_rows=theorem_body_rows,
        hygiene_only_rows=hygiene_only_rows,
        prime_power_only_rows=prime_power_only_rows,
        exact_p_rows=exact_p_rows,
        mixed_graph_rows=mixed_graph_rows,
        source_theorem_closed_rows=source_theorem_closed_rows,
        danger3_unblocked_rows=danger3_unblocked_rows,
        extraction_ready_rows=extraction_ready_rows,
        submission_ready_rows=submission_ready_rows,
        rejected_rows=rejected_rows,
        conditional_rows=conditional_rows,
        row_ok=row_ok,
    )


def build_candidate(args: argparse.Namespace) -> KooShinTheoremClauseClaim:
    return KooShinTheoremClauseClaim(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        product_or_distribution_theorem=args.product_distribution,
        modularity_hygiene_only=args.hygiene_only,
        odd_prime_or_prime_power_only=args.prime_power_only,
        mixed_level_lift=args.mixed_level_lift,
        exact_product_p=args.exact_p,
        mixed_graph_selector=args.mixed_graph,
        equal_weight_atoms=args.equal_weight,
        orientation_branch=args.orientation,
        arithmetic_producer=args.arithmetic_producer,
        output_kind=args.output_kind,
        finite_field_identity_for_p=args.finite_identity,
        period_156_context=args.period_156,
        danger3_framing=args.danger3_framing,
        extraction_to_A_x0=args.extraction,
        concrete_vpp_verified_triple=args.vpp_verified,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--product-distribution", action="store_true")
    parser.add_argument("--hygiene-only", action="store_true")
    parser.add_argument("--prime-power-only", action="store_true")
    parser.add_argument("--mixed-level-lift", action="store_true")
    parser.add_argument("--exact-p", action="store_true")
    parser.add_argument("--mixed-graph", action="store_true")
    parser.add_argument("--equal-weight", action="store_true")
    parser.add_argument("--orientation", action="store_true")
    parser.add_argument("--arithmetic-producer", action="store_true")
    parser.add_argument(
        "--output-kind",
        default="divisor-additive",
        choices=("divisor-additive", "raw-product", "theta2-divisor", "value", "finite-field-value", "period-value", "exponent-hygiene", "field-generation"),
    )
    parser.add_argument("--finite-identity", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--extraction", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    return parser.parse_args()


def print_decision(decision: KooShinTheoremClauseDecision) -> None:
    print(
        "  "
        f"{decision.claim.name}: decision={decision.decision} "
        f"exact_product={decision.exact_product_decision} "
        f"closing={decision.closing_theorem_decision} "
        f"source_closed={int(decision.source_theorem_closed)} "
        f"danger3={int(decision.danger3_route_unblocked)} "
        f"extraction={int(decision.extraction_ready)} "
        f"submission={int(decision.submission_ready)} "
        f"missing={decision.first_missing_clause}"
    )


def main() -> int:
    args = parse_args()
    if args.candidate:
        decision = classify_claim(build_candidate(args))
        print("p25 KSY-y Koo-Shin theorem-clause candidate intake")
        print_decision(decision)
        print(f"ksy_y_koo_shin_theorem_clause_intake_candidate_rows={int(decision.row_ok)}/1")
        return 0 if decision.row_ok else 1

    profile = profile_koo_shin_theorem_clause_intake()
    print("p25 KSY-y Koo-Shin theorem-clause intake gate")
    print("regression_rows")
    for decision in profile.regression_rows:
        print_decision(decision)
    print("counts")
    print(f"  theorem_body_rows={profile.theorem_body_rows}")
    print(f"  hygiene_only_rows={profile.hygiene_only_rows}")
    print(f"  prime_power_only_rows={profile.prime_power_only_rows}")
    print(f"  exact_p_rows={profile.exact_p_rows}")
    print(f"  mixed_graph_rows={profile.mixed_graph_rows}")
    print(f"  source_theorem_closed_rows={profile.source_theorem_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  theorem_body_is_required_before_source_use=1")
    print("  hygiene_or_prime_power_product_alone_is_rejected=1")
    print("  exact_mixed_product_can_close_source_side_but_not_submission=1")
    print("  vpp_verified_triple_is_still_final_submission_gate=1")
    print(f"ksy_y_koo_shin_theorem_clause_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin theorem-clause intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

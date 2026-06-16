#!/usr/bin/env python3
"""Closing-theorem obligation gate for the p25 KSY-y moonshot.

Earlier gates made the finite payload, source-parameter hygiene, mixed graph,
and submission-extraction boundaries executable.  This gate consolidates those
boundaries into the minimal theorem contract a future proof/literature hit must
satisfy before it can be treated as a true moonshot closure rather than a
finite verifier shadow.

The final DANGER3 submission still requires a concrete `vpp.py`-verified
`(p,A,x0)` triple.  This gate classifies theorem statements on the way there.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


P25 = 10000000000000000000000013
RAW_C = (47, 28)
RAW_D = (22, 3)
RAW_K = (57, 0)
QUOTIENT_C = (2, 28)
QUOTIENT_D = (1, 3)
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780


@dataclass(frozen=True)
class ClosingTheoremClaim:
    name: str
    source_family: str
    emits_exact_p: bool
    preserves_mixed_graph: bool
    equal_weight_atoms: bool
    orientation_recorded: bool
    arithmetic_source_theorem: bool
    output_kind: str
    finite_field_identity_for_p: bool
    period_156_context: bool
    danger3_policy_or_non_cm_framing: bool
    extraction_to_A_x0: bool
    concrete_vpp_verified_triple: bool


@dataclass(frozen=True)
class ClosingTheoremDecision:
    claim: ClosingTheoremClaim
    decision: str
    source_theorem_closed: bool
    danger3_route_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class ClosingTheoremObligationProfile:
    p: int
    raw_product: str
    quotient_reflection_center: str
    support_period: int
    ambient_period: int
    regression_rows: tuple[ClosingTheoremDecision, ...]
    source_theorem_closed_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    conditional_rows: int
    rejected_rows: int
    row_ok: bool


def is_product_output(kind: str) -> bool:
    return kind in {"divisor-additive", "raw-product", "theta2-divisor"}


def is_value_output(kind: str) -> bool:
    return kind in {"value", "finite-field-value", "period-value"}


def classify_claim(claim: ClosingTheoremClaim) -> ClosingTheoremDecision:
    if claim.concrete_vpp_verified_triple:
        return ClosingTheoremDecision(
            claim=claim,
            decision="submission_ready_verified_triple",
            source_theorem_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_clause="none",
            next_action="archive vpp output and generate Lean certificate",
            row_ok=True,
        )

    if not claim.emits_exact_p:
        return ClosingTheoremDecision(
            claim=claim,
            decision="reject_not_exact_p",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="exact P over C=(47,28), D=(22,3), K=(57,0)",
            next_action="discard or reframe as the exact K-traced anti-invariant product P",
            row_ok=True,
        )

    if not claim.preserves_mixed_graph:
        return ClosingTheoremDecision(
            claim=claim,
            decision="reject_missing_mixed_graph",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="mixed C_3 x C_169 row graph / reflection-center payload",
            next_action="run mixed-graph obligation gate; C169 projection is only a screen",
            row_ok=True,
        )

    if not claim.equal_weight_atoms:
        return ClosingTheoremDecision(
            claim=claim,
            decision="reject_nonuniform_product",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="equal weights on all 75 K-traced atoms",
            next_action="discard missing, doubled, mixed-sign, or nonuniform variants",
            row_ok=True,
        )

    if not claim.orientation_recorded:
        return ClosingTheoremDecision(
            claim=claim,
            decision="conditional_missing_orientation",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="theta2/theta2-inverse orientation branch",
            next_action="record which raw orientation branch the theorem emits",
            row_ok=True,
        )

    if not claim.arithmetic_source_theorem:
        return ClosingTheoremDecision(
            claim=claim,
            decision="conditional_finite_payload_without_source_theorem",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="challenge-legal arithmetic source theorem",
            next_action="keep as verifier payload; require a theorem source",
            row_ok=True,
        )

    if is_value_output(claim.output_kind) and not claim.period_156_context:
        return ClosingTheoremDecision(
            claim=claim,
            decision="conditional_value_missing_period_156",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="period-156 fixedness/telescoping for value output",
            next_action="attach support-period branch/root context; ambient 780 has 11 branches",
            row_ok=True,
        )

    if not (is_product_output(claim.output_kind) or is_value_output(claim.output_kind)):
        return ClosingTheoremDecision(
            claim=claim,
            decision="reject_unknown_output_kind",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="divisor/additive product or period-156 value identity",
            next_action="classify output through exact-product or period-value intake",
            row_ok=True,
        )

    source_closed = claim.finite_field_identity_for_p or is_product_output(claim.output_kind)
    if not source_closed:
        return ClosingTheoremDecision(
            claim=claim,
            decision="conditional_missing_finite_field_identity",
            source_theorem_closed=False,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field identity for exact P",
            next_action="state the theorem as an identity for the p25 finite payload",
            row_ok=True,
        )

    if not claim.danger3_policy_or_non_cm_framing:
        return ClosingTheoremDecision(
            claim=claim,
            decision="source_theorem_closed_policy_or_framing_missing",
            source_theorem_closed=True,
            danger3_route_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            next_action="ask whether this finite-field identity is challenge-legal",
            row_ok=True,
        )

    if not claim.extraction_to_A_x0:
        return ClosingTheoremDecision(
            claim=claim,
            decision="danger3_unblocked_extraction_missing",
            source_theorem_closed=True,
            danger3_route_unblocked=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="concrete A,x0 extraction or accepted submission framing",
            next_action="derive A,x0 from the finite identity, then run vpp.py",
            row_ok=True,
        )

    return ClosingTheoremDecision(
        claim=claim,
        decision="ready_to_extract_and_verify_concrete_triple",
        source_theorem_closed=True,
        danger3_route_unblocked=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_clause="actual vpp.py-verified (p,A,x0)",
        next_action="run extraction; verify p,A,x0 with official vpp.py",
        row_ok=True,
    )


def regression_claims() -> tuple[ClosingTheoremClaim, ...]:
    base = {
        "source_family": "KSY/Kubert-Lang/Sprang",
        "emits_exact_p": True,
        "preserves_mixed_graph": True,
        "equal_weight_atoms": True,
        "orientation_recorded": True,
        "arithmetic_source_theorem": True,
        "output_kind": "divisor-additive",
        "finite_field_identity_for_p": True,
        "period_156_context": False,
        "danger3_policy_or_non_cm_framing": True,
        "extraction_to_A_x0": True,
        "concrete_vpp_verified_triple": False,
    }
    rows = [
        ClosingTheoremClaim("generic_field_generation", "KSY", False, False, False, False, False, "field-generation", False, False, False, False, False),
        ClosingTheoremClaim("c169_projection_only", "Kubert-Lang", True, False, True, True, False, "divisor-additive", False, False, False, False, False),
        ClosingTheoremClaim("finite_payload_no_source", "finite harness", True, True, True, True, False, "divisor-additive", True, False, False, False, False),
        ClosingTheoremClaim("value_without_period", "Siegel-Robert", True, True, True, True, True, "value", True, False, False, False, False),
        ClosingTheoremClaim("exact_product_policy_unknown", **{**base, "danger3_policy_or_non_cm_framing": False, "extraction_to_A_x0": False}),
        ClosingTheoremClaim("period_value_policy_yes_no_extraction", **{**base, "output_kind": "period-value", "period_156_context": True, "extraction_to_A_x0": False}),
        ClosingTheoremClaim("full_theorem_with_extraction_algorithm", **base),
        ClosingTheoremClaim("verified_p25_triple", **{**base, "concrete_vpp_verified_triple": True}),
    ]
    return tuple(rows)


def profile_closing_theorem_obligation() -> ClosingTheoremObligationProfile:
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    source_rows = sum(int(row.source_theorem_closed) for row in decisions)
    danger3_rows = sum(int(row.danger3_route_unblocked) for row in decisions)
    extraction_rows = sum(int(row.extraction_ready) for row in decisions)
    submission_rows = sum(int(row.submission_ready) for row in decisions)
    conditional_rows = sum(
        int(row.decision.startswith(("conditional_", "source_theorem_", "danger3_", "ready_")))
        for row in decisions
    )
    rejected_rows = sum(int(row.decision.startswith("reject_")) for row in decisions)
    row_ok = (
        source_rows == 4
        and danger3_rows == 3
        and extraction_rows == 2
        and submission_rows == 1
        and conditional_rows == 5
        and rejected_rows == 2
        and tuple(row.decision for row in decisions)
        == (
            "reject_not_exact_p",
            "reject_missing_mixed_graph",
            "conditional_finite_payload_without_source_theorem",
            "conditional_value_missing_period_156",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "ready_to_extract_and_verify_concrete_triple",
            "submission_ready_verified_triple",
        )
        and all(row.row_ok for row in decisions)
    )
    return ClosingTheoremObligationProfile(
        p=P25,
        raw_product=(
            "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
            f"C={RAW_C}, D={RAW_D}, K={RAW_K}"
        ),
        quotient_reflection_center=f"C={QUOTIENT_C}, D={QUOTIENT_D}, T=-2C",
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        regression_rows=decisions,
        source_theorem_closed_rows=source_rows,
        danger3_unblocked_rows=danger3_rows,
        extraction_ready_rows=extraction_rows,
        submission_ready_rows=submission_rows,
        conditional_rows=conditional_rows,
        rejected_rows=rejected_rows,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> ClosingTheoremClaim:
    return ClosingTheoremClaim(
        name=args.name,
        source_family=args.source_family,
        emits_exact_p=args.exact_p,
        preserves_mixed_graph=args.mixed_graph,
        equal_weight_atoms=args.equal_weight,
        orientation_recorded=args.orientation,
        arithmetic_source_theorem=args.arithmetic_source,
        output_kind=args.output_kind,
        finite_field_identity_for_p=args.finite_identity,
        period_156_context=args.period_156,
        danger3_policy_or_non_cm_framing=args.danger3_framing,
        extraction_to_A_x0=args.extraction,
        concrete_vpp_verified_triple=args.vpp_verified_triple,
    )


def print_decision(decision: ClosingTheoremDecision) -> None:
    claim = decision.claim
    print(
        "  "
        f"{claim.name}: source={claim.source_family} "
        f"exactP={int(claim.emits_exact_p)} mixed={int(claim.preserves_mixed_graph)} "
        f"equal={int(claim.equal_weight_atoms)} orient={int(claim.orientation_recorded)} "
        f"arith={int(claim.arithmetic_source_theorem)} kind={claim.output_kind} "
        f"finite_identity={int(claim.finite_field_identity_for_p)} "
        f"period156={int(claim.period_156_context)} "
        f"danger3={int(claim.danger3_policy_or_non_cm_framing)} "
        f"extract={int(claim.extraction_to_A_x0)} "
        f"vpp={int(claim.concrete_vpp_verified_triple)} "
        f"decision={decision.decision} "
        f"source_closed={int(decision.source_theorem_closed)} "
        f"danger3_unblocked={int(decision.danger3_route_unblocked)} "
        f"extraction_ready={int(decision.extraction_ready)} "
        f"submission_ready={int(decision.submission_ready)} "
        f"missing={decision.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify p25 KSY-y closing theorem obligations."
    )
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--source-family", default="unspecified")
    parser.add_argument("--output-kind", default="divisor-additive")
    parser.add_argument("--exact-p", action="store_true")
    parser.add_argument("--mixed-graph", action="store_true")
    parser.add_argument("--equal-weight", action="store_true")
    parser.add_argument("--orientation", action="store_true")
    parser.add_argument("--arithmetic-source", action="store_true")
    parser.add_argument("--finite-identity", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--extraction", action="store_true")
    parser.add_argument("--vpp-verified-triple", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang KSY-y closing-theorem obligation gate")
    if args.candidate:
        decision = classify_claim(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(
            "robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_candidate_rows="
            f"{int(decision.row_ok)}/1"
        )
        return 0 if not decision.decision.startswith("reject_") else 1

    profile = profile_closing_theorem_obligation()
    print(f"closing_theorem_obligation_profile={profile}")
    print("obligation")
    print(f"  p={profile.p}")
    print(f"  raw_product={profile.raw_product}")
    print(f"  quotient_reflection_center={profile.quotient_reflection_center}")
    print(f"  support_period={profile.support_period}")
    print(f"  ambient_period={profile.ambient_period}")
    print("regression_rows")
    for decision in profile.regression_rows:
        print_decision(decision)
    print("counts")
    print(f"  source_theorem_closed_rows={profile.source_theorem_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  exact_P_mixed_graph_equal_weight_orientation_are_required=1")
    print("  value_route_requires_period_156_context=1")
    print("  source_theorem_closure_is_not_submission_readiness=1")
    print("  verified_vpp_triple_is_the_only_submission_ready_state=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("closing-theorem obligation regression failed")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

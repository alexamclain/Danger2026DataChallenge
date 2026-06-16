#!/usr/bin/env python3
"""Submission/extraction gate for the p25 KSY-y moonshot.

The finite producer gates now identify several sub-sqrt payload interfaces.
The DANGER3 challenge surface is still concrete: a submitted hit is a
Pomerance triple `(p,A,x0)` verified by `vpp.py` / `lean_vpp.py`.

This gate separates four states that are easy to blur:

* finite payload accepted by the local KSY/theta spine;
* arithmetic source theorem for the exact p25 product;
* extraction of a concrete `(A,x0)` or policy acceptance of a finite-field
  identity framing;
* official `vpp.py` verification of the concrete triple.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate import (
    profile_arithmetic_producer_contract,
)
from p25_laneB_robert_ksy_theta2_universal_producer_intake import (
    default_universal_producer_intake_profile,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate import (
    P25,
    profile_danger3_framing,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
from vpp import pp_verify  # noqa: E402


P24 = 1000000000000000000000007
P24_A = 38923582678463553756710
P24_X0 = 843367907077058108520461


@dataclass(frozen=True)
class SubmissionExtractionClaim:
    name: str
    has_finite_payload: bool
    has_arithmetic_source_theorem: bool
    exact_product_or_value_theorem: bool
    period_156_context: bool
    finite_field_identity_for_p: bool
    danger3_policy_accepts_identity: bool
    has_extraction_algorithm_to_A_x0: bool
    has_concrete_triple: bool
    vpp_verified: bool
    lean_generatable: bool


@dataclass(frozen=True)
class SubmissionExtractionDecision:
    claim: SubmissionExtractionClaim
    decision: str
    finite_route_live: bool
    source_route_closed: bool
    submission_ready: bool
    first_missing_clause: str
    next_action: str
    row_ok: bool


@dataclass(frozen=True)
class VppRegressionProfile:
    known_p24_triple_verified: bool
    p24_x0_plus_one_rejected: bool
    row_ok: bool


@dataclass(frozen=True)
class SubmissionExtractionProfile:
    universal_intake_ok: bool
    arithmetic_producer_contract_ok: bool
    danger3_framing_ok: bool
    vpp_regression: VppRegressionProfile
    regression_rows: tuple[SubmissionExtractionDecision, ...]
    finite_live_rows: int
    source_closed_rows: int
    submission_ready_rows: int
    conditional_rows: int
    rejected_rows: int
    row_ok: bool


def vpp_regression_profile() -> VppRegressionProfile:
    good = pp_verify(P24, P24_A, P24_X0)
    bad = not pp_verify(P24, P24_A, P24_X0 + 1)
    return VppRegressionProfile(
        known_p24_triple_verified=good,
        p24_x0_plus_one_rejected=bad,
        row_ok=good and bad,
    )


def classify_claim(claim: SubmissionExtractionClaim) -> SubmissionExtractionDecision:
    if claim.has_concrete_triple:
        if claim.vpp_verified:
            return SubmissionExtractionDecision(
                claim=claim,
                decision="closing_vpp_verified_submission",
                finite_route_live=True,
                source_route_closed=True,
                submission_ready=True,
                first_missing_clause="none",
                next_action="archive vpp output, generate Lean certificate, and record/submit the triple",
                row_ok=True,
            )
        return SubmissionExtractionDecision(
            claim=claim,
            decision="reject_concrete_triple_fails_vpp",
            finite_route_live=False,
            source_route_closed=False,
            submission_ready=False,
            first_missing_clause="official vpp.py verification",
            next_action="discard or debug; do not treat as a hit",
            row_ok=True,
        )

    if not claim.has_finite_payload:
        return SubmissionExtractionDecision(
            claim=claim,
            decision="reject_no_finite_payload_or_triple",
            finite_route_live=False,
            source_route_closed=False,
            submission_ready=False,
            first_missing_clause="finite payload or concrete verified triple",
            next_action="route through universal intake or vpp.py",
            row_ok=True,
        )

    if not claim.has_arithmetic_source_theorem:
        return SubmissionExtractionDecision(
            claim=claim,
            decision="finite_payload_only_not_source_theorem",
            finite_route_live=True,
            source_route_closed=False,
            submission_ready=False,
            first_missing_clause="challenge-legal arithmetic source theorem",
            next_action="attach a theorem producing the accepted finite payload",
            row_ok=True,
        )

    source_theorem_ok = (
        claim.exact_product_or_value_theorem
        and (not claim.period_156_context or claim.finite_field_identity_for_p)
    )
    if not source_theorem_ok:
        return SubmissionExtractionDecision(
            claim=claim,
            decision="conditional_source_theorem_shape_incomplete",
            finite_route_live=True,
            source_route_closed=False,
            submission_ready=False,
            first_missing_clause="exact product theorem or value theorem with period-156 finite identity",
            next_action="classify through exact-product or period-value intake",
            row_ok=True,
        )

    if claim.has_extraction_algorithm_to_A_x0:
        return SubmissionExtractionDecision(
            claim=claim,
            decision="extraction_algorithm_needs_concrete_vpp_output",
            finite_route_live=True,
            source_route_closed=True,
            submission_ready=False,
            first_missing_clause="actual (A,x0) output and official vpp.py verification",
            next_action="run extraction, then verify p,A,x0 with vpp.py",
            row_ok=True,
        )

    if claim.danger3_policy_accepts_identity and claim.finite_field_identity_for_p:
        return SubmissionExtractionDecision(
            claim=claim,
            decision="policy_unblocked_but_extraction_missing",
            finite_route_live=True,
            source_route_closed=True,
            submission_ready=False,
            first_missing_clause="concrete (A,x0) derivation or accepted submission framing",
            next_action="ask/derive how the finite identity produces the vpp-verified triple",
            row_ok=True,
        )

    return SubmissionExtractionDecision(
        claim=claim,
        decision="source_theorem_but_policy_or_extraction_missing",
        finite_route_live=True,
        source_route_closed=True,
        submission_ready=False,
        first_missing_clause="DANGER3 policy framing or A,x0 extraction",
        next_action="resolve finite-identity acceptance and derive a concrete triple",
        row_ok=True,
    )


def regression_claims() -> tuple[SubmissionExtractionClaim, ...]:
    return (
        SubmissionExtractionClaim(
            "finite_payload_only",
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        SubmissionExtractionClaim(
            "raw_product_source_theorem_no_policy_or_extraction",
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        SubmissionExtractionClaim(
            "period_value_theorem_policy_yes_no_extraction",
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ),
        SubmissionExtractionClaim(
            "source_theorem_with_extraction_algorithm_no_output",
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            False,
            False,
        ),
        SubmissionExtractionClaim(
            "claimed_p25_triple_fails_vpp",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
        ),
        SubmissionExtractionClaim(
            "verified_p25_triple",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
        ),
    )


def profile_submission_extraction() -> SubmissionExtractionProfile:
    universal = default_universal_producer_intake_profile()
    producer = profile_arithmetic_producer_contract()
    danger3 = profile_danger3_framing()
    vpp_regression = vpp_regression_profile()
    decisions = tuple(classify_claim(claim) for claim in regression_claims())
    finite_live = sum(int(row.finite_route_live) for row in decisions)
    source_closed = sum(int(row.source_route_closed) for row in decisions)
    submission_ready = sum(int(row.submission_ready) for row in decisions)
    conditional = sum(int(row.decision.startswith(("finite_", "source_", "policy_", "extraction_", "conditional_"))) for row in decisions)
    rejected = sum(int(row.decision.startswith("reject_")) for row in decisions)
    row_ok = (
        universal.row_ok
        and producer.row_ok
        and danger3.row_ok
        and vpp_regression.row_ok
        and finite_live == 5
        and source_closed == 4
        and submission_ready == 1
        and conditional == 4
        and rejected == 1
        and tuple(row.decision for row in decisions)
        == (
            "finite_payload_only_not_source_theorem",
            "source_theorem_but_policy_or_extraction_missing",
            "policy_unblocked_but_extraction_missing",
            "extraction_algorithm_needs_concrete_vpp_output",
            "reject_concrete_triple_fails_vpp",
            "closing_vpp_verified_submission",
        )
        and all(row.row_ok for row in decisions)
    )
    return SubmissionExtractionProfile(
        universal_intake_ok=universal.row_ok,
        arithmetic_producer_contract_ok=producer.row_ok,
        danger3_framing_ok=danger3.row_ok,
        vpp_regression=vpp_regression,
        regression_rows=decisions,
        finite_live_rows=finite_live,
        source_closed_rows=source_closed,
        submission_ready_rows=submission_ready,
        conditional_rows=conditional,
        rejected_rows=rejected,
        row_ok=row_ok,
    )


def candidate_claim_from_triple(p: int, a: int, x0: int) -> SubmissionExtractionClaim:
    verified = pp_verify(p, a, x0)
    return SubmissionExtractionClaim(
        name="candidate_triple",
        has_finite_payload=False,
        has_arithmetic_source_theorem=False,
        exact_product_or_value_theorem=False,
        period_156_context=False,
        finite_field_identity_for_p=False,
        danger3_policy_accepts_identity=False,
        has_extraction_algorithm_to_A_x0=False,
        has_concrete_triple=True,
        vpp_verified=verified,
        lean_generatable=verified,
    )


def print_decision(decision: SubmissionExtractionDecision) -> None:
    claim = decision.claim
    print(
        "  "
        f"{claim.name}: finite_payload={int(claim.has_finite_payload)} "
        f"source_theorem={int(claim.has_arithmetic_source_theorem)} "
        f"exact_theorem={int(claim.exact_product_or_value_theorem)} "
        f"period156={int(claim.period_156_context)} "
        f"finite_identity={int(claim.finite_field_identity_for_p)} "
        f"policy={int(claim.danger3_policy_accepts_identity)} "
        f"extractor={int(claim.has_extraction_algorithm_to_A_x0)} "
        f"triple={int(claim.has_concrete_triple)} "
        f"vpp={int(claim.vpp_verified)} "
        f"decision={decision.decision} "
        f"finite_live={int(decision.finite_route_live)} "
        f"source_closed={int(decision.source_route_closed)} "
        f"submission_ready={int(decision.submission_ready)} "
        f"missing={decision.first_missing_clause}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify p25 KSY-y finite/theorem/extraction/submission claims."
    )
    parser.add_argument("--p", type=int)
    parser.add_argument("--A", type=int)
    parser.add_argument("--x0", type=int)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang KSY-y submission-extraction gate")
    if args.p is not None or args.A is not None or args.x0 is not None:
        if args.p is None or args.A is None or args.x0 is None:
            raise SystemExit("--p, --A, and --x0 must be supplied together")
        decision = classify_claim(candidate_claim_from_triple(args.p, args.A, args.x0))
        print("candidate_triple_decision")
        print_decision(decision)
        print(
            "robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_candidate_rows="
            f"{int(decision.row_ok)}/1"
        )
        return 0 if decision.submission_ready else 1

    profile = profile_submission_extraction()
    print(f"submission_extraction_profile={profile}")
    print("dependency_gates")
    print(f"  universal_intake_ok={int(profile.universal_intake_ok)}")
    print(f"  arithmetic_producer_contract_ok={int(profile.arithmetic_producer_contract_ok)}")
    print(f"  danger3_framing_ok={int(profile.danger3_framing_ok)}")
    print(f"  known_p24_triple_verified={int(profile.vpp_regression.known_p24_triple_verified)}")
    print(f"  p24_x0_plus_one_rejected={int(profile.vpp_regression.p24_x0_plus_one_rejected)}")
    print("regression_rows")
    for decision in profile.regression_rows:
        print_decision(decision)
    print("counts")
    print(f"  finite_live_rows={profile.finite_live_rows}")
    print(f"  source_closed_rows={profile.source_closed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  finite_payload_acceptance_is_not_submission_readiness=1")
    print("  source_theorem_still_needs_policy_or_A_x0_extraction=1")
    print("  concrete_triple_must_pass_official_vpp=1")
    print("  p24_vpp_regression_positive_and_negative_controls_pass=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("submission-extraction regression failed")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

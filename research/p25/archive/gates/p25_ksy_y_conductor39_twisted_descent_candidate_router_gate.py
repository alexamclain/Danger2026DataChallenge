#!/usr/bin/env python3
"""Candidate router for conductor-39 twisted-descent theorem claims.

The decision packet records the fixed facts: the pure degree-6 norm cancels,
while twisted quotient/ratio/Hilbert-90 structures are live helpers.  This
gate is the intake form for future expert or literature claims phrased as
"take a norm", "take a ratio", or "use Hilbert 90".
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class TwistedDescentCandidate:
    name: str
    theorem_body_verified: bool
    uses_degree6_orbit: bool
    uses_pure_norm: bool
    uses_pair_sum: bool
    uses_signed_shadow: bool
    uses_quotient_or_ratio: bool
    uses_hilbert90_boundary: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    arithmetic_source_theorem: bool
    danger3_framing: bool
    extraction_to_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class TwistedDescentCandidateDecision:
    candidate: TwistedDescentCandidate
    decision: str
    helper_only: bool
    source_stage_closed: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class TwistedDescentCandidateRouter:
    decision_packet_marker_present: bool
    conductor39_intake_marker_present: bool
    h90_intake_marker_present: bool
    two_conjugate_sum_support: int
    six_conjugate_sum_support: int
    pure_character_degree6_norm_cancels: bool
    q_value_frobenius_inverse_contract: bool
    w_value_frobenius_inverse_contract: bool
    balanced_h90_support: int
    sparse_h90_support: int
    rows: tuple[TwistedDescentCandidateDecision, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_closing_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def artifact_present(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def marker_present(path: Path, marker: str) -> bool:
    return artifact_present(path) and marker in path.read_text()


def classify_candidate(candidate: TwistedDescentCandidate) -> TwistedDescentCandidateDecision:
    if candidate.official_vpp and candidate.extraction_to_A_x0:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="submission_ready_verified_triple",
            helper_only=False,
            source_stage_closed=True,
            danger3_unblocked=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_or_falsifier="none",
            next_action="archive vpp output, command, environment, and Lean certificate",
            ok=True,
        )

    if not candidate.theorem_body_verified:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="reject_no_theorem_body",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="obtain theorem text before routing the claim",
            ok=True,
        )

    if not candidate.uses_degree6_orbit:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="conditional_missing_degree6_orbit_context",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="degree-6 Frobenius orbit of the conductor-39 character",
            next_action="attach the order-39/degree-6 descent context",
            ok=True,
        )

    if candidate.uses_pair_sum:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="reject_pair_sum_cancels",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="Frob_p(W)=-W, so W+Frob_p(W) has support zero",
            next_action="discard the pair-sum route",
            ok=True,
        )

    if candidate.uses_pure_norm:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="reject_pure_degree6_norm_cancels",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="six-conjugate additive norm of the pure character word is zero",
            next_action="ask for a twisted ratio, quotient, or Hilbert-90 boundary instead",
            ok=True,
        )

    if not (candidate.uses_signed_shadow or candidate.uses_quotient_or_ratio or candidate.uses_hilbert90_boundary):
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="conditional_missing_twisted_descent_structure",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="twisted trace, quotient/ratio, or Hilbert-90 boundary",
            next_action="reject naive norm language until the twisted structure is named",
            ok=True,
        )

    if not candidate.finite_value_or_divisor_theorem:
        if candidate.uses_hilbert90_boundary:
            decision = "helper_only_hilbert90_boundary_value_theorem_missing"
            missing = "boundary shape still lacks finite value/divisor theorem"
        elif candidate.uses_quotient_or_ratio:
            decision = "helper_only_ratio_boundary_value_theorem_missing"
            missing = "Frobenius-inverse quotient gives descent contract but no finite value"
        else:
            decision = "helper_only_signed_orbit_shadow_value_theorem_missing"
            missing = "signed orbit law is source certification, not a finite value/divisor theorem"
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision=decision,
            helper_only=True,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier=missing,
            next_action="keep as helper; ask for finite value/divisor theorem",
            ok=True,
        )

    if not candidate.period156_context:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="conditional_value_theorem_missing_period156_context",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="period-156 branch/root/telescoping context",
            next_action="ask for support-period fixedness before trusting the F_p value branch",
            ok=True,
        )

    if not candidate.arithmetic_source_theorem:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="conditional_finite_payload_without_source_theorem",
            helper_only=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            next_action="keep as verifier payload only",
            ok=True,
        )

    if not candidate.danger3_framing:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="source_theorem_closed_policy_or_framing_missing",
            helper_only=False,
            source_stage_closed=True,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            next_action="settle challenge framing, then derive concrete A and x0",
            ok=True,
        )

    if not candidate.extraction_to_A_x0:
        return TwistedDescentCandidateDecision(
            candidate=candidate,
            decision="danger3_unblocked_extraction_missing",
            helper_only=False,
            source_stage_closed=True,
            danger3_unblocked=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="extraction algorithm for concrete (A,x0)",
            next_action="derive the DANGER3 triple and run official vpp.py",
            ok=True,
        )

    return TwistedDescentCandidateDecision(
        candidate=candidate,
        decision="extraction_ready_vpp_missing",
        helper_only=False,
        source_stage_closed=True,
        danger3_unblocked=True,
        extraction_ready=True,
        submission_ready=False,
        first_missing_or_falsifier="official vpp.py verification of concrete (A,x0)",
        next_action="run official vpp.py",
        ok=True,
    )


def regression_candidates() -> tuple[TwistedDescentCandidate, ...]:
    base = {
        "theorem_body_verified": True,
        "uses_degree6_orbit": True,
        "uses_pure_norm": False,
        "uses_pair_sum": False,
        "uses_signed_shadow": False,
        "uses_quotient_or_ratio": False,
        "uses_hilbert90_boundary": False,
        "finite_value_or_divisor_theorem": False,
        "period156_context": False,
        "arithmetic_source_theorem": False,
        "danger3_framing": False,
        "extraction_to_A_x0": False,
        "official_vpp": False,
    }
    return (
        TwistedDescentCandidate("no_theorem_body", **{**base, "theorem_body_verified": False}),
        TwistedDescentCandidate("no_degree6_context", **{**base, "uses_degree6_orbit": False}),
        TwistedDescentCandidate("pure_degree6_norm", **{**base, "uses_pure_norm": True}),
        TwistedDescentCandidate("two_conjugate_pair_sum", **{**base, "uses_pair_sum": True}),
        TwistedDescentCandidate("degree6_without_twist", **base),
        TwistedDescentCandidate("signed_shadow_only", **{**base, "uses_signed_shadow": True}),
        TwistedDescentCandidate("quotient_ratio_only", **{**base, "uses_quotient_or_ratio": True}),
        TwistedDescentCandidate("h90_boundary_only", **{**base, "uses_hilbert90_boundary": True}),
        TwistedDescentCandidate(
            "twisted_value_no_period156",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
            },
        ),
        TwistedDescentCandidate(
            "twisted_period156_value_no_source",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
            },
        ),
        TwistedDescentCandidate(
            "twisted_period156_source_no_framing",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
            },
        ),
        TwistedDescentCandidate(
            "danger3_framed_no_extraction",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
            },
        ),
        TwistedDescentCandidate(
            "extraction_ready_no_vpp",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "extraction_to_A_x0": True,
            },
        ),
        TwistedDescentCandidate(
            "official_vpp_verified",
            **{
                **base,
                "uses_quotient_or_ratio": True,
                "uses_hilbert90_boundary": True,
                "finite_value_or_divisor_theorem": True,
                "period156_context": True,
                "arithmetic_source_theorem": True,
                "danger3_framing": True,
                "extraction_to_A_x0": True,
                "official_vpp": True,
            },
        ),
    )


def profile_twisted_descent_candidate_router() -> TwistedDescentCandidateRouter:
    decision_marker = marker_present(
        RESEARCH / "p25_ksy_y_conductor39_twisted_descent_decision_packet_20260614.md",
        "ksy_y_conductor39_twisted_descent_decision_packet_rows=1/1",
    )
    conductor39_marker = marker_present(
        RESEARCH / "p25_ksy_y_conductor39_source_theorem_intake_20260614.md",
        "ksy_y_conductor39_source_theorem_intake_rows=1/1",
    )
    h90_marker = marker_present(
        RESEARCH / "p25_ksy_y_h90_value_theorem_intake_20260614.md",
        "ksy_y_h90_value_theorem_intake_rows=1/1",
    )
    decisions = tuple(classify_candidate(candidate) for candidate in regression_candidates())
    rejected = sum(row.decision.startswith("reject_") for row in decisions)
    helper = sum(row.helper_only for row in decisions)
    conditional = sum(row.decision.startswith("conditional_") for row in decisions)
    closing = sum(row.source_stage_closed for row in decisions)
    danger3 = sum(row.danger3_unblocked for row in decisions)
    extraction = sum(row.extraction_ready for row in decisions)
    submission = sum(row.submission_ready for row in decisions)
    row_ok = (
        decision_marker
        and conductor39_marker
        and h90_marker
        and len(decisions) == 14
        and rejected == 3
        and helper == 3
        and conditional == 4
        and closing == 4
        and danger3 == 3
        and extraction == 2
        and submission == 1
        and tuple(row.decision for row in decisions)
        == (
            "reject_no_theorem_body",
            "conditional_missing_degree6_orbit_context",
            "reject_pure_degree6_norm_cancels",
            "reject_pair_sum_cancels",
            "conditional_missing_twisted_descent_structure",
            "helper_only_signed_orbit_shadow_value_theorem_missing",
            "helper_only_ratio_boundary_value_theorem_missing",
            "helper_only_hilbert90_boundary_value_theorem_missing",
            "conditional_value_theorem_missing_period156_context",
            "conditional_finite_payload_without_source_theorem",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "extraction_ready_vpp_missing",
            "submission_ready_verified_triple",
        )
        and all(row.ok for row in decisions)
    )
    return TwistedDescentCandidateRouter(
        decision_packet_marker_present=decision_marker,
        conductor39_intake_marker_present=conductor39_marker,
        h90_intake_marker_present=h90_marker,
        two_conjugate_sum_support=0,
        six_conjugate_sum_support=0,
        pure_character_degree6_norm_cancels=True,
        q_value_frobenius_inverse_contract=True,
        w_value_frobenius_inverse_contract=True,
        balanced_h90_support=24,
        sparse_h90_support=12,
        rows=decisions,
        row_count=len(decisions),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_closing_rows=closing,
        danger3_unblocked_rows=danger3,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def candidate_from_args(args: argparse.Namespace) -> TwistedDescentCandidate:
    return TwistedDescentCandidate(
        name=args.name,
        theorem_body_verified=args.theorem_body,
        uses_degree6_orbit=args.degree6,
        uses_pure_norm=args.pure_norm,
        uses_pair_sum=args.pair_sum,
        uses_signed_shadow=args.signed_shadow,
        uses_quotient_or_ratio=args.ratio,
        uses_hilbert90_boundary=args.h90_boundary,
        finite_value_or_divisor_theorem=args.finite_or_divisor,
        period156_context=args.period_156,
        arithmetic_source_theorem=args.arithmetic_source,
        danger3_framing=args.danger3_framing,
        extraction_to_A_x0=args.extraction,
        official_vpp=args.vpp_verified,
    )


def print_decision(decision: TwistedDescentCandidateDecision) -> None:
    candidate = decision.candidate
    print(
        "  "
        f"{candidate.name}: theorem={int(candidate.theorem_body_verified)} "
        f"degree6={int(candidate.uses_degree6_orbit)} "
        f"pure_norm={int(candidate.uses_pure_norm)} "
        f"pair_sum={int(candidate.uses_pair_sum)} "
        f"signed={int(candidate.uses_signed_shadow)} "
        f"ratio={int(candidate.uses_quotient_or_ratio)} "
        f"h90={int(candidate.uses_hilbert90_boundary)} "
        f"finite={int(candidate.finite_value_or_divisor_theorem)} "
        f"period156={int(candidate.period156_context)} "
        f"source={int(candidate.arithmetic_source_theorem)} "
        f"danger3={int(candidate.danger3_framing)} "
        f"extract={int(candidate.extraction_to_A_x0)} "
        f"vpp={int(candidate.official_vpp)} "
        f"decision={decision.decision} "
        f"helper={int(decision.helper_only)} "
        f"source_closed={int(decision.source_stage_closed)} "
        f"submission={int(decision.submission_ready)} "
        f"missing={decision.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify conductor-39 twisted-descent candidates.")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="candidate")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--degree6", action="store_true")
    parser.add_argument("--pure-norm", action="store_true")
    parser.add_argument("--pair-sum", action="store_true")
    parser.add_argument("--signed-shadow", action="store_true")
    parser.add_argument("--ratio", action="store_true")
    parser.add_argument("--h90-boundary", action="store_true")
    parser.add_argument("--finite-or-divisor", action="store_true")
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--arithmetic-source", action="store_true")
    parser.add_argument("--danger3-framing", action="store_true")
    parser.add_argument("--extraction", action="store_true")
    parser.add_argument("--vpp-verified", action="store_true")
    args = parser.parse_args()

    print("p25 KSY-y conductor-39 twisted-descent candidate router gate")
    if args.candidate:
        decision = classify_candidate(candidate_from_args(args))
        print("candidate_decision")
        print_decision(decision)
        print(f"ksy_y_conductor39_twisted_descent_candidate_router_candidate_rows={int(decision.ok)}/1")
        return 0 if decision.ok else 1

    profile = profile_twisted_descent_candidate_router()
    print("dependencies")
    print(f"  decision_packet_marker_present={int(profile.decision_packet_marker_present)}")
    print(f"  conductor39_intake_marker_present={int(profile.conductor39_intake_marker_present)}")
    print(f"  h90_intake_marker_present={int(profile.h90_intake_marker_present)}")
    print("fixed_facts")
    print(f"  two_conjugate_sum_support={profile.two_conjugate_sum_support}")
    print(f"  six_conjugate_sum_support={profile.six_conjugate_sum_support}")
    print(f"  pure_character_degree6_norm_cancels={int(profile.pure_character_degree6_norm_cancels)}")
    print(f"  q_value_frobenius_inverse_contract={int(profile.q_value_frobenius_inverse_contract)}")
    print(f"  w_value_frobenius_inverse_contract={int(profile.w_value_frobenius_inverse_contract)}")
    print(f"  balanced_h90_support={profile.balanced_h90_support}")
    print(f"  sparse_h90_support={profile.sparse_h90_support}")
    print("regression_rows")
    for decision in profile.rows:
        print_decision(decision)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  pure_norm_and_pair_sum_language_is_rejected=1")
    print("  signed_shadow_ratio_and_h90_boundary_are_helpers_until_value_theorem=1")
    print("  period156_finite_value_or_divisor_source_theorem_closes_source_stage=1")
    print("  vpp_verified_A_x0_is_the_only_submission_ready_state=1")
    print(f"ksy_y_conductor39_twisted_descent_candidate_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 twisted-descent candidate router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

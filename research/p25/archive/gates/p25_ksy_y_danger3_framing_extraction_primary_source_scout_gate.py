#!/usr/bin/env python3
"""DANGER3 framing/extraction primary-source scout for the p25 KSY-y moonshot.

The official challenge source is the DANGER3 repository.  It gives a concrete
submission surface: verify a Pomerance triple with vpp.py, and optionally
generate a Lean certificate with lean_vpp.py.  The KSY-y theorem route is only
useful for the challenge after it either produces such a triple or gets an
accepted finite-field framing plus an extraction path to (A, x0).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate import (
    REMOTE_DANGER3_HEAD_CHECKED,
    profile_danger3_framing,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate import (
    SubmissionExtractionClaim,
    classify_claim as classify_submission_claim,
    profile_submission_extraction,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
REMOTE_HEAD_OBSERVED = "a65658b7b194546957fa62f40d60ca63efc37f93"
OFFICIAL_REPO = "https://github.com/AndrewVSutherland/DANGER3"


@dataclass(frozen=True)
class Danger3ScoutObservation:
    name: str
    source_clause: str
    source_handle: str
    submission_claim: SubmissionExtractionClaim | None
    framing_decision: str | None
    expected_submission_decision: str | None
    expected_framing_decision: str | None
    matched_clause: str
    first_missing_clause: str


@dataclass(frozen=True)
class Danger3ScoutProfile:
    official_repo: str
    remote_head_observed: str
    remote_head_matches_framing_gate: bool
    local_vpp_available: bool
    local_lean_vpp_available: bool
    official_lean_vpp_observed: bool
    danger3_framing_ok: bool
    submission_extraction_ok: bool
    observations: tuple[Danger3ScoutObservation, ...]
    direct_submission_rows: int
    conditional_rows: int
    policy_only_rows: int
    rejected_rows: int
    hypothetical_submission_rows: int
    row_ok: bool


def observations() -> tuple[Danger3ScoutObservation, ...]:
    return (
        Danger3ScoutObservation(
            name="official_danger3_submission_surface",
            source_clause="README / vpp.py / lean_vpp.py",
            source_handle="AndrewVSutherland/DANGER3 main",
            submission_claim=None,
            framing_decision=None,
            expected_submission_decision=None,
            expected_framing_decision=None,
            matched_clause="official challenge asks for a concrete Pomerance triple",
            first_missing_clause="concrete p25 (A,x0) passing official vpp.py",
        ),
        Danger3ScoutObservation(
            name="finite_identity_theorem_policy_unknown",
            source_clause="exact finite-field theorem route before policy answer",
            source_handle="local DANGER3 framing gate",
            submission_claim=SubmissionExtractionClaim(
                "finite_identity_theorem_policy_unknown",
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
            framing_decision="conditional_policy_or_framing_missing",
            expected_submission_decision="source_theorem_but_policy_or_extraction_missing",
            expected_framing_decision="conditional_policy_or_framing_missing",
            matched_clause="exact theorem route could be meaningful",
            first_missing_clause="DANGER3 acceptance of finite-field identity framing or A,x0 extraction",
        ),
        Danger3ScoutObservation(
            name="policy_unblocked_theorem_no_extraction",
            source_clause="policy yes plus theorem but no concrete triple",
            source_handle="local submission-extraction gate",
            submission_claim=SubmissionExtractionClaim(
                "policy_unblocked_theorem_no_extraction",
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
            framing_decision="policy_unblocked_theorem_route_not_submission",
            expected_submission_decision="policy_unblocked_but_extraction_missing",
            expected_framing_decision="policy_unblocked_theorem_route_not_submission",
            matched_clause="policy yes can unblock the theorem route",
            first_missing_clause="concrete (A,x0) derivation or accepted submission framing",
        ),
        Danger3ScoutObservation(
            name="extraction_algorithm_without_output",
            source_clause="claimed extraction algorithm before producing a triple",
            source_handle="local submission-extraction gate",
            submission_claim=SubmissionExtractionClaim(
                "extraction_algorithm_without_output",
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
            framing_decision=None,
            expected_submission_decision="extraction_algorithm_needs_concrete_vpp_output",
            expected_framing_decision=None,
            matched_clause="extraction is the right next stage after theorem/policy",
            first_missing_clause="actual (A,x0) output and official vpp.py verification",
        ),
        Danger3ScoutObservation(
            name="policy_yes_only",
            source_clause="policy answer without theorem",
            source_handle="local DANGER3 framing gate",
            submission_claim=None,
            framing_decision="policy_only_not_theorem",
            expected_submission_decision=None,
            expected_framing_decision="policy_only_not_theorem",
            matched_clause="would resolve one ambiguity",
            first_missing_clause="exact product theorem or value theorem with period-156 context",
        ),
        Danger3ScoutObservation(
            name="generic_cm_lang_generation",
            source_clause="CM/Lang provenance without finite identity",
            source_handle="local DANGER3 framing gate",
            submission_claim=None,
            framing_decision="reject_cm_provenance_without_finite_identity",
            expected_submission_decision=None,
            expected_framing_decision="reject_cm_provenance_without_finite_identity",
            matched_clause="records no-CM/provenance danger boundary",
            first_missing_clause="finite-field identity for P or concrete verified triple",
        ),
        Danger3ScoutObservation(
            name="claimed_triple_fails_vpp",
            source_clause="concrete triple negative control",
            source_handle="local submission-extraction gate",
            submission_claim=SubmissionExtractionClaim(
                "claimed_triple_fails_vpp",
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
            framing_decision="reject_unverified_triple",
            expected_submission_decision="reject_concrete_triple_fails_vpp",
            expected_framing_decision="reject_unverified_triple",
            matched_clause="concrete triples are accepted only through vpp.py",
            first_missing_clause="official vpp.py verification",
        ),
        Danger3ScoutObservation(
            name="verified_p25_triple_hypothetical",
            source_clause="closing calibration row",
            source_handle="local submission-extraction gate",
            submission_claim=SubmissionExtractionClaim(
                "verified_p25_triple_hypothetical",
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
            framing_decision="closing_verified_pomerance_triple",
            expected_submission_decision="closing_vpp_verified_submission",
            expected_framing_decision="closing_verified_pomerance_triple",
            matched_clause="would close the challenge side",
            first_missing_clause="none",
        ),
    )


def profile_danger3_framing_extraction_scout() -> Danger3ScoutProfile:
    rows = observations()
    framing = profile_danger3_framing()
    submission = profile_submission_extraction()

    submission_decisions = tuple(
        classify_submission_claim(row.submission_claim)
        if row.submission_claim is not None
        else None
        for row in rows
    )

    direct_submission = 0
    hypothetical_submission = sum(
        int(
            decision is not None
            and decision.submission_ready
            and "hypothetical" in row.name
        )
        for row, decision in zip(rows, submission_decisions)
    )
    policy_only = sum(int(row.framing_decision == "policy_only_not_theorem") for row in rows)
    rejected = sum(
        int(
            (decision is not None and decision.decision.startswith("reject_"))
            or (row.framing_decision is not None and row.framing_decision.startswith("reject_"))
        )
        for row, decision in zip(rows, submission_decisions)
    )
    conditional = len(rows) - 1 - direct_submission - hypothetical_submission - policy_only - rejected

    local_vpp = (REPO_ROOT / "src" / "vpp.py").exists()
    local_lean = (REPO_ROOT / "src" / "lean_vpp.py").exists()
    remote_match = (
        REMOTE_HEAD_OBSERVED == REMOTE_DANGER3_HEAD_CHECKED == framing.danger3_remote_head_checked
    )

    row_ok = (
        remote_match
        and local_vpp
        and framing.row_ok
        and submission.row_ok
        and len(rows) == 8
        and direct_submission == 0
        and conditional == 3
        and policy_only == 1
        and rejected == 2
        and hypothetical_submission == 1
        and all(
            row.expected_submission_decision is None
            or (
                decision is not None
                and decision.decision == row.expected_submission_decision
            )
            for row, decision in zip(rows, submission_decisions)
        )
        and all(
            row.expected_framing_decision is None
            or row.framing_decision == row.expected_framing_decision
            for row in rows
        )
    )

    return Danger3ScoutProfile(
        official_repo=OFFICIAL_REPO,
        remote_head_observed=REMOTE_HEAD_OBSERVED,
        remote_head_matches_framing_gate=remote_match,
        local_vpp_available=local_vpp,
        local_lean_vpp_available=local_lean,
        official_lean_vpp_observed=True,
        danger3_framing_ok=framing.row_ok,
        submission_extraction_ok=submission.row_ok,
        observations=rows,
        direct_submission_rows=direct_submission,
        conditional_rows=conditional,
        policy_only_rows=policy_only,
        rejected_rows=rejected,
        hypothetical_submission_rows=hypothetical_submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_danger3_framing_extraction_scout()
    print("p25 KSY-y DANGER3 framing/extraction primary-source scout gate")
    print(f"official_repo={profile.official_repo}")
    print(f"remote_head_observed={profile.remote_head_observed}")
    print(f"remote_head_matches_framing_gate={int(profile.remote_head_matches_framing_gate)}")
    print(f"local_vpp_available={int(profile.local_vpp_available)}")
    print(f"local_lean_vpp_available={int(profile.local_lean_vpp_available)}")
    print(f"official_lean_vpp_observed={int(profile.official_lean_vpp_observed)}")
    print(f"danger3_framing_ok={int(profile.danger3_framing_ok)}")
    print(f"submission_extraction_ok={int(profile.submission_extraction_ok)}")
    print("observations")
    for row in profile.observations:
        submission_decision = (
            classify_submission_claim(row.submission_claim).decision
            if row.submission_claim is not None
            else "not_run"
        )
        print(
            "  "
            f"{row.name}: clause={row.source_clause} handle={row.source_handle} "
            f"submission_decision={submission_decision} "
            f"framing_decision={row.framing_decision or 'not_run'} "
            f"matched={row.matched_clause} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  direct_submission_rows={profile.direct_submission_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  policy_only_rows={profile.policy_only_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  hypothetical_submission_rows={profile.hypothetical_submission_rows}")
    print("interpretation")
    print("  concrete_vpp_verified_triple_is_the_submission_surface=1")
    print("  finite_identity_policy_yes_does_not_replace_A_x0_extraction=1")
    print("  theorem_only_progress_is_not_submission_ready=1")
    print("  generic_CM_provenance_without_finite_identity_is_rejected=1")
    print(
        "ksy_y_danger3_framing_extraction_primary_source_scout_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("DANGER3 framing/extraction primary-source scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

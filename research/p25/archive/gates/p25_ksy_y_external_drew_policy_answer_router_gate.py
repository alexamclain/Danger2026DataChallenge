#!/usr/bin/env python3
"""Answer router for external Drew finite-identity policy replies.

This is the answer-side companion to the external Drew policy question packet.
It includes the exact 75-atom product as a first-class policy-yes branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_danger3_finite_identity_framing_router_gate import (
    FiniteIdentityFramingCandidate,
    FiniteIdentityFramingDecision,
    classify_candidate,
)
from p25_ksy_y_external_drew_policy_question_packet_gate import (
    profile_external_drew_policy_question_packet,
)
from p25_ksy_y_external_post_source_danger3_handoff_gate import (
    profile_external_post_source_danger3_handoff,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_drew_policy_question_packet_20260614.md",
        "ksy_y_external_drew_policy_question_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_post_source_danger3_handoff_20260614.md",
        "ksy_y_external_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalDrewPolicyAnswerRow:
    name: str
    answer_family: str
    drew_answer_shape: str
    expected_decision: str
    decision: FiniteIdentityFramingDecision
    recommendation: str
    route_state: str
    exact75_relevant: bool
    current_evidence: bool
    submission_boundary: bool
    current_submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExternalDrewPolicyAnswerRouter:
    dependency_markers_present: int
    dependency_markers_total: int
    question_packet_ok: bool
    external_handoff_ok: bool
    rows: tuple[ExternalDrewPolicyAnswerRow, ...]
    row_count: int
    current_evidence_rows: int
    policy_unblocks_rows: int
    exact75_policy_rows: int
    rewrite_required_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    rejected_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def candidate(
    name: str,
    *,
    has_source_theorem: bool = True,
    finite_identity: bool = True,
    generic_cm: bool = False,
    non_cm: bool = False,
    policy_yes: bool = False,
    same_j: bool = False,
    x16: bool = False,
    x0: bool = False,
    vpp: bool = False,
) -> FiniteIdentityFramingCandidate:
    return FiniteIdentityFramingCandidate(
        name=name,
        has_source_theorem=has_source_theorem,
        finite_field_identity_for_p=finite_identity,
        generic_cm_or_class_field_generation=generic_cm,
        explicit_non_cm_finite_field_framing=non_cm,
        danger3_policy_accepts_identity=policy_yes,
        same_j_x18112_bridge=same_j,
        x16_surface_or_A_xP16=x16,
        concrete_A_x0=x0,
        official_vpp=vpp,
    )


def answer_row(
    *,
    name: str,
    family: str,
    answer_shape: str,
    expected_decision: str,
    recommendation: str,
    route_state: str,
    candidate_kwargs: dict[str, bool],
    exact75: bool = False,
    current_evidence: bool = False,
    submission_boundary: bool = False,
    current_submission_ready: bool = False,
) -> ExternalDrewPolicyAnswerRow:
    decision = classify_candidate(candidate(name, **candidate_kwargs))
    return ExternalDrewPolicyAnswerRow(
        name=name,
        answer_family=family,
        drew_answer_shape=answer_shape,
        expected_decision=expected_decision,
        decision=decision,
        recommendation=recommendation,
        route_state=route_state,
        exact75_relevant=exact75,
        current_evidence=current_evidence,
        submission_boundary=submission_boundary,
        current_submission_ready=current_submission_ready,
        ok=decision.ok
        and decision.decision == expected_decision
        and not current_submission_ready,
    )


def answer_rows() -> tuple[ExternalDrewPolicyAnswerRow, ...]:
    return (
        answer_row(
            name="no_policy_ruling_yet",
            family="hold",
            answer_shape="Drew does not settle the finite-identity framing boundary",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            recommendation="keep source theorem as upstream progress; do not spend extraction effort yet",
            route_state="source stage may close, DANGER3 remains blocked",
            candidate_kwargs={},
            exact75=True,
        ),
        answer_row(
            name="explicit_non_cm_finite_identity_yes",
            family="continue",
            answer_shape="explicit p-specialized finite-field/non-CM identity language is acceptable",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            recommendation="continue to same-j X_1(8112) bridge construction",
            route_state="DANGER3 framing unblocked; bridge missing",
            candidate_kwargs={"non_cm": True},
        ),
        answer_row(
            name="external_policy_yes_for_frontdoor_identities",
            family="continue",
            answer_shape=(
                "Drew gives policy yes for p-specialized KSY/Kubert-Lang/"
                "Yang/H90/curved-corner identities"
            ),
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            recommendation="continue to same-j X_1(8112) bridge construction",
            route_state="DANGER3 framing unblocked; bridge missing",
            candidate_kwargs={"policy_yes": True},
            exact75=True,
        ),
        answer_row(
            name="exact75_policy_yes",
            family="continue",
            answer_shape="Drew says the exact 75-atom product identity may use the same DANGER3 ladder",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            recommendation="continue exact P through same-j X_1(8112), then X_1(16)",
            route_state="DANGER3 framing unblocked for exact P; bridge missing",
            candidate_kwargs={"policy_yes": True},
            exact75=True,
        ),
        answer_row(
            name="generic_cm_requires_rewrite",
            family="rewrite",
            answer_shape="generic CM/class-field generation alone is not acceptable",
            expected_decision="reject_generic_cm_generation_not_framing",
            recommendation="rewrite as an explicit finite-field identity for this p or kill the route",
            route_state="generic provenance rejected as DANGER3 framing",
            candidate_kwargs={"generic_cm": True},
        ),
        answer_row(
            name="same_j_bridge_yes_no_x16",
            family="continue",
            answer_shape="same-j X_1(8112) bridge evidence is accepted, but no practical X_1(16) surface yet",
            expected_decision="cross_level_target_identified_specialization_missing",
            recommendation="specialize to X_1(16) and expose y/x or A,xP16",
            route_state="cross-level target identified; X_1(16) surface missing",
            candidate_kwargs={"policy_yes": True, "same_j": True},
        ),
        answer_row(
            name="x16_payload_yes_no_halving",
            family="continue",
            answer_shape="A,xP16 or y plus model root x is accepted as the active X_1(16) payload",
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            recommendation="derive halving chain or direct x0, then run official vpp.py",
            route_state="X_1(16) surface reached; halving/x0 missing",
            candidate_kwargs={"policy_yes": True, "same_j": True, "x16": True},
        ),
        answer_row(
            name="concrete_A_x0_no_vpp",
            family="verify",
            answer_shape="concrete A,x0 is supplied but official DANGER3 vpp.py has not passed",
            expected_decision="extraction_ready_vpp_missing",
            recommendation="run official vpp.py immediately and archive output",
            route_state="extraction ready; verifier missing",
            candidate_kwargs={"policy_yes": True, "same_j": True, "x16": True, "x0": True},
        ),
        answer_row(
            name="official_vpp_verified_boundary",
            family="boundary",
            answer_shape="concrete p25 A,x0 passes official DANGER3 vpp.py",
            expected_decision="submission_ready",
            recommendation="archive command, logs, environment, and certificate",
            route_state="submission boundary reached",
            candidate_kwargs={
                "has_source_theorem": False,
                "finite_identity": False,
                "x0": True,
                "vpp": True,
            },
            submission_boundary=True,
        ),
    )


def profile_external_drew_policy_answer_router() -> ExternalDrewPolicyAnswerRouter:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    question_packet = profile_external_drew_policy_question_packet()
    handoff = profile_external_post_source_danger3_handoff()
    rows = answer_rows()
    current = sum(row.current_evidence for row in rows)
    policy_unblocks = sum(
        row.decision.decision == "danger3_unblocked_cross_level_bridge_missing"
        for row in rows
    )
    exact75 = sum(row.exact75_relevant and row.answer_family in {"hold", "continue"} for row in rows)
    rewrite_required = sum(row.answer_family == "rewrite" for row in rows)
    same_j = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16 = sum(row.decision.x16_surface_reached for row in rows)
    extraction = sum(row.decision.extraction_ready for row in rows)
    submission_boundary = sum(row.submission_boundary for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.decision.decision.startswith("reject_") for row in rows)
    decisions = tuple(row.decision.decision for row in rows)
    expected_decisions = (
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "reject_generic_cm_generation_not_framing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and question_packet.row_ok
        and handoff.row_ok
        and handoff.external_source_yes_rows == 5
        and handoff.exact75_source_yes_rows == 1
        and len(rows) == 9
        and current == 0
        and policy_unblocks == 3
        and exact75 == 3
        and rewrite_required == 1
        and same_j == 4
        and x16 == 3
        and extraction == 2
        and submission_boundary == 1
        and current_submission == 0
        and rejected == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalDrewPolicyAnswerRouter(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        question_packet_ok=question_packet.row_ok,
        external_handoff_ok=handoff.row_ok,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        policy_unblocks_rows=policy_unblocks,
        exact75_policy_rows=exact75,
        rewrite_required_rows=rewrite_required,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_boundary_rows=submission_boundary,
        current_submission_ready_rows=current_submission,
        rejected_rows=rejected,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_drew_policy_answer_router()
    print("p25 KSY-y external Drew policy answer router gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  question_packet_ok={int(profile.question_packet_ok)}")
    print(f"  external_handoff_ok={int(profile.external_handoff_ok)}")
    print("answer_rows")
    for row in profile.rows:
        decision = row.decision
        print(
            "  "
            f"{row.name}: family={row.answer_family} decision={decision.decision} "
            f"danger3={int(decision.danger3_unblocked)} "
            f"same_j={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"extract={int(decision.extraction_ready)} "
            f"submission_boundary={int(row.submission_boundary)} "
            f"exact75={int(row.exact75_relevant)} "
            f"current={int(row.current_evidence)}"
        )
        print(f"    answer={row.drew_answer_shape}")
        print(f"    route={row.route_state}")
        print(f"    next={row.recommendation}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  policy_unblocks_rows={profile.policy_unblocks_rows}")
    print(f"  exact75_policy_rows={profile.exact75_policy_rows}")
    print(f"  rewrite_required_rows={profile.rewrite_required_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  exact75_policy_yes_routes_to_same_j_bridge=1")
    print("  drew_policy_yes_routes_to_same_j_bridge=1")
    print("  drew_generic_cm_no_routes_to_rewrite_or_kill=1")
    print("  concrete_A_x0_routes_to_official_vpp=1")
    print("  official_vpp_boundary_is_not_current_evidence=1")
    print(
        "ksy_y_external_drew_policy_answer_router_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external Drew policy answer router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

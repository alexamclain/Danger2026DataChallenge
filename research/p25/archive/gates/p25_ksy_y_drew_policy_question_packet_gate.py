#!/usr/bin/env python3
"""Drew-facing policy question packet for p25 finite identities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_danger3_finite_identity_framing_router_gate import (
    FiniteIdentityFramingCandidate,
    FiniteIdentityFramingDecision,
    classify_candidate,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_priority1_post_source_danger3_handoff_20260614.md",
        "ksy_y_priority1_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_source_query_packet_20260614.md",
        "ksy_y_priority1_source_query_packet_rows=1/1",
    ),
)


@dataclass(frozen=True)
class DrewPolicyQuestionRow:
    name: str
    question_for_drew: str
    answer_that_advances: str
    local_route_if_answer_yes: str
    decision: FiniteIdentityFramingDecision
    ok: bool


@dataclass(frozen=True)
class DrewPolicyQuestionPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    rows: tuple[DrewPolicyQuestionRow, ...]
    row_count: int
    pre_policy_rows: int
    policy_yes_rows: int
    rejected_rows: int
    danger3_unblocked_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    submission_boundary_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def candidate(
    name: str,
    *,
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
        has_source_theorem=True,
        finite_field_identity_for_p=True,
        generic_cm_or_class_field_generation=generic_cm,
        explicit_non_cm_finite_field_framing=non_cm,
        danger3_policy_accepts_identity=policy_yes,
        same_j_x18112_bridge=same_j,
        x16_surface_or_A_xP16=x16,
        concrete_A_x0=x0,
        official_vpp=vpp,
    )


def row(
    *,
    name: str,
    question: str,
    advances: str,
    local_route: str,
    expected_decision: str,
    candidate_kwargs: dict[str, bool],
) -> DrewPolicyQuestionRow:
    decision = classify_candidate(candidate(name, **candidate_kwargs))
    return DrewPolicyQuestionRow(
        name=name,
        question_for_drew=question,
        answer_that_advances=advances,
        local_route_if_answer_yes=local_route,
        decision=decision,
        ok=decision.decision == expected_decision and decision.ok,
    )


def question_rows() -> tuple[DrewPolicyQuestionRow, ...]:
    return (
        row(
            name="finite_identity_policy_boundary",
            question=(
                "If we have an exact p25 finite divisor/additive identity for "
                "H0, conductor-39 U_chi/W, or the twisted H90 object, what "
                "additional wording makes it DANGER3-compatible?"
            ),
            advances="explicit non-CM finite-field identity language, or Drew says the identity is acceptable",
            local_route="source theorem closed; DANGER3 policy/framing still missing",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            candidate_kwargs={},
        ),
        row(
            name="explicit_non_cm_finite_field_framing",
            question=(
                "Would an identity stated purely as a finite-field identity for "
                "this p, with no generic CM/class-field generation step, clear "
                "the DANGER3 framing boundary?"
            ),
            advances="yes, this is acceptable finite-field/non-CM framing",
            local_route="DANGER3 unblocked; same-j X_1(8112) bridge becomes next missing item",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            candidate_kwargs={"non_cm": True},
        ),
        row(
            name="external_policy_yes",
            question=(
                "If the theorem is naturally KSY/Kubert-Lang/Hilbert-90, can "
                "Drew give a policy yes that lets us treat the p-specialized "
                "finite identity as challenge-legal?"
            ),
            advances="yes, route this identity as acceptable despite its provenance",
            local_route="DANGER3 unblocked; same-j X_1(8112) bridge becomes next missing item",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            candidate_kwargs={"policy_yes": True},
        ),
        row(
            name="generic_cm_generation_falsifier",
            question=(
                "Is generic CM/class-field generation still disallowed unless "
                "it is reframed as an explicit p-specialized finite-field identity?"
            ),
            advances="yes, generic generation alone remains outside the accepted route",
            local_route="kill or rewrite the claim as a finite-field identity for this p",
            expected_decision="reject_generic_cm_generation_not_framing",
            candidate_kwargs={"generic_cm": True},
        ),
        row(
            name="same_j_bridge_evidence",
            question=(
                "What evidence is enough for the same-j X_1(8112) bridge: an "
                "abstract fiber-product theorem, explicit curve data, or a "
                "normalized order-8112 point with projections?"
            ),
            advances="same-j bridge accepted for the odd identity and production X_1(16) side",
            local_route="cross-level target identified; practical X_1(16) surface missing",
            expected_decision="cross_level_target_identified_specialization_missing",
            candidate_kwargs={"policy_yes": True, "same_j": True},
        ),
        row(
            name="x16_surface_payload_evidence",
            question=(
                "If the bridge emits production A,xP16, or y plus model root x, "
                "is that sufficient to enter the practical halving stage?"
            ),
            advances="yes, A,xP16 or y/x is accepted as the active X_1(16) payload",
            local_route="X_1(16) surface reached; halving chain or x0 missing",
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            candidate_kwargs={"policy_yes": True, "same_j": True, "x16": True},
        ),
        row(
            name="official_vpp_boundary",
            question=(
                "If we have concrete p25 A,x0 passing official DANGER3 vpp.py, "
                "does that settle the submission boundary independent of the "
                "upstream source story?"
            ),
            advances="yes, archive official vpp output, command, environment, and certificate",
            local_route="submission ready",
            expected_decision="submission_ready",
            candidate_kwargs={
                "policy_yes": True,
                "same_j": True,
                "x16": True,
                "x0": True,
                "vpp": True,
            },
        ),
    )


def profile_drew_policy_question_packet() -> DrewPolicyQuestionPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = question_rows()
    pre_policy = sum(
        row.decision.decision == "source_theorem_closed_policy_or_framing_missing"
        for row in rows
    )
    policy_yes = sum(
        row.name in {"explicit_non_cm_finite_field_framing", "external_policy_yes"}
        for row in rows
    )
    rejected = sum(row.decision.decision.startswith("reject_") for row in rows)
    danger3 = sum(row.decision.danger3_unblocked for row in rows)
    same_j = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16 = sum(row.decision.x16_surface_reached for row in rows)
    submission = sum(row.decision.submission_ready for row in rows)
    decisions = tuple(row.decision.decision for row in rows)
    expected_decisions = (
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "danger3_unblocked_cross_level_bridge_missing",
        "reject_generic_cm_generation_not_framing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 7
        and pre_policy == 1
        and policy_yes == 2
        and rejected == 1
        and danger3 == 5
        and same_j == 3
        and x16 == 2
        and submission == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return DrewPolicyQuestionPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        rows=rows,
        row_count=len(rows),
        pre_policy_rows=pre_policy,
        policy_yes_rows=policy_yes,
        rejected_rows=rejected,
        danger3_unblocked_rows=danger3,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        submission_boundary_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_drew_policy_question_packet()
    print("p25 KSY-y Drew policy question packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("question_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: decision={row.decision.decision} "
            f"danger3={int(row.decision.danger3_unblocked)} "
            f"same_j={int(row.decision.cross_level_bridge_identified)} "
            f"x16={int(row.decision.x16_surface_reached)} "
            f"submission={int(row.decision.submission_ready)}"
        )
        print(f"    question={row.question_for_drew}")
        print(f"    advances={row.answer_that_advances}")
        print(f"    route={row.local_route_if_answer_yes}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  pre_policy_rows={profile.pre_policy_rows}")
    print(f"  policy_yes_rows={profile.policy_yes_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print("interpretation")
    print("  ask_drew_for_policy_yes_or_non_cm_finite_identity_boundary=1")
    print("  ask_drew_what_same_j_bridge_evidence_counts=1")
    print("  official_vpp_verified_A_x0_remains_the_submission_boundary=1")
    print(f"ksy_y_drew_policy_question_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Drew policy question packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Drew-facing policy question packet for external front-door finite identities.

The external source handoff has five possible source-stage yes answers: H0,
conductor-39, twisted/H90, curved-corner, and the exact 75-atom product.  This packet asks
the finite-identity/DANGER3 policy questions that apply after any of those
source theorems lands.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_danger3_finite_identity_framing_router_gate import (
    FiniteIdentityFramingCandidate,
    FiniteIdentityFramingDecision,
    classify_candidate,
)
from p25_ksy_y_external_post_source_danger3_handoff_gate import (
    profile_external_post_source_danger3_handoff,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_post_source_danger3_handoff_20260614.md",
        "ksy_y_external_post_source_danger3_handoff_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_answer_router_20260614.md",
        "ksy_y_external_frontdoor_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalDrewPolicyQuestionRow:
    name: str
    question_for_drew: str
    answer_that_advances: str
    local_route_if_answer_yes: str
    exact75_relevant: bool
    decision: FiniteIdentityFramingDecision
    ok: bool


@dataclass(frozen=True)
class ExternalDrewPolicyQuestionPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    external_handoff_ok: bool
    rows: tuple[ExternalDrewPolicyQuestionRow, ...]
    row_count: int
    pre_policy_rows: int
    policy_yes_rows: int
    exact75_relevant_rows: int
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
    exact75: bool = False,
) -> ExternalDrewPolicyQuestionRow:
    decision = classify_candidate(candidate(name, **candidate_kwargs))
    return ExternalDrewPolicyQuestionRow(
        name=name,
        question_for_drew=question,
        answer_that_advances=advances,
        local_route_if_answer_yes=local_route,
        exact75_relevant=exact75,
        decision=decision,
        ok=decision.decision == expected_decision and decision.ok,
    )


def question_rows() -> tuple[ExternalDrewPolicyQuestionRow, ...]:
    return (
        row(
            name="external_finite_identity_policy_boundary",
            question=(
                "If we have an exact p25 finite divisor/additive identity for "
                "H0, conductor-39 U_chi/W, twisted H90, the curved corner, "
                "or the exact 75-atom product P, what wording makes it "
                "DANGER3-compatible?"
            ),
            advances="explicit non-CM finite-field identity language, or Drew says the identity is acceptable",
            local_route="source theorem closed; DANGER3 policy/framing still missing",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            candidate_kwargs={},
            exact75=True,
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
            name="external_policy_yes_for_frontdoor_identities",
            question=(
                "Can Drew give a policy yes for p-specialized KSY/Kubert-Lang/"
                "Yang/H90/curved-corner identities, including exact P, when "
                "stated as finite identities for this p?"
            ),
            advances="yes, route these identities as challenge-legal despite provenance",
            local_route="DANGER3 unblocked; same-j X_1(8112) bridge becomes next missing item",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            candidate_kwargs={"policy_yes": True},
            exact75=True,
        ),
        row(
            name="exact75_specific_policy_yes",
            question=(
                "If the exact 75-atom normalized-y product identity is proved "
                "directly, does that identity receive the same policy treatment "
                "as H0/Yang/H90/curved-corner?"
            ),
            advances="yes, exact P is allowed to enter the same DANGER3 ladder",
            local_route="DANGER3 unblocked; same-j X_1(8112) bridge becomes next missing item",
            expected_decision="danger3_unblocked_cross_level_bridge_missing",
            candidate_kwargs={"policy_yes": True},
            exact75=True,
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
                "What evidence is enough for the same-j X_1(8112) bridge after "
                "a front-door identity clears policy?"
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


def profile_external_drew_policy_question_packet() -> ExternalDrewPolicyQuestionPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    handoff = profile_external_post_source_danger3_handoff()
    rows = question_rows()
    pre_policy = sum(
        row.decision.decision == "source_theorem_closed_policy_or_framing_missing"
        for row in rows
    )
    policy_yes = sum(
        row.name
        in {
            "explicit_non_cm_finite_field_framing",
            "external_policy_yes_for_frontdoor_identities",
            "exact75_specific_policy_yes",
        }
        for row in rows
    )
    exact75 = sum(row.exact75_relevant for row in rows)
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
        "danger3_unblocked_cross_level_bridge_missing",
        "reject_generic_cm_generation_not_framing",
        "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and handoff.row_ok
        and handoff.external_source_yes_rows == 5
        and handoff.exact75_source_yes_rows == 1
        and len(rows) == 8
        and pre_policy == 1
        and policy_yes == 3
        and exact75 == 3
        and rejected == 1
        and danger3 == 6
        and same_j == 3
        and x16 == 2
        and submission == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalDrewPolicyQuestionPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_handoff_ok=handoff.row_ok,
        rows=rows,
        row_count=len(rows),
        pre_policy_rows=pre_policy,
        policy_yes_rows=policy_yes,
        exact75_relevant_rows=exact75,
        rejected_rows=rejected,
        danger3_unblocked_rows=danger3,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        submission_boundary_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_drew_policy_question_packet()
    print("p25 KSY-y external Drew policy question packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_handoff_ok={int(profile.external_handoff_ok)}")
    print("question_rows")
    for row in profile.rows:
        decision = row.decision
        print(
            "  "
            f"{row.name}: decision={decision.decision} "
            f"danger3={int(decision.danger3_unblocked)} "
            f"same_j={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"submission={int(decision.submission_ready)} "
            f"exact75={int(row.exact75_relevant)}"
        )
        print(f"    question={row.question_for_drew}")
        print(f"    advances={row.answer_that_advances}")
        print(f"    route={row.local_route_if_answer_yes}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  pre_policy_rows={profile.pre_policy_rows}")
    print(f"  policy_yes_rows={profile.policy_yes_rows}")
    print(f"  exact75_relevant_rows={profile.exact75_relevant_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print("interpretation")
    print("  exact75_policy_questions_are_first_class=1")
    print("  drew_policy_yes_routes_to_same_j_bridge=1")
    print("  generic_cm_generation_remains_a_falsifier=1")
    print("  official_vpp_boundary_bypasses_source_debate=1")
    print(
        "ksy_y_external_drew_policy_question_packet_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external Drew policy question packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

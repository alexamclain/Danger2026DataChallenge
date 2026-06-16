#!/usr/bin/env python3
"""Post-source DANGER3 handoff for external front-door source wins.

The external front-door answer router has five source-stage yes answers:
H0, conductor-39, twisted/H90, curved-corner, and the exact 75-atom product.
This gate attaches all five to the already-owned DANGER3 framing, same-j bridge,
X_1(16), halving, and official-vpp ladder.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_danger3_finite_identity_framing_router_gate import (
    FiniteIdentityFramingCandidate,
    FiniteIdentityFramingDecision,
    classify_candidate,
)
from p25_ksy_y_external_frontdoor_answer_router_gate import (
    ExternalFrontdoorAnswerRow,
    profile_external_frontdoor_answer_router,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_answer_router_20260614.md",
        "ksy_y_external_frontdoor_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_cross_level_bridge_source_route_packet_20260614.md",
        "ksy_y_cross_level_bridge_source_route_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_extraction_surface_20260614.md",
        "ksy_y_danger3_extraction_surface_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_cross_level_extraction_gap_20260614.md",
        "ksy_y_cross_level_extraction_gap_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_20260614.md",
        "ksy_y_x1_8112_bridge_theorem_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_8112_torsion_gluing_contract_20260614.md",
        "ksy_y_x1_8112_torsion_gluing_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_chain_contract_20260614.md",
        "ksy_y_x1_16_halving_chain_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalPostSourceDANGER3Row:
    name: str
    source_family: str
    source_query_name: str
    source_answer_name: str
    route_stage: str
    framing_decision: FiniteIdentityFramingDecision
    current_source_theorem_exists: bool
    source_stage_yes_answer: bool
    exact75_source_answer: bool
    fixture_source_answer: bool
    submission_boundary: bool
    current_submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExternalPostSourceDANGER3Handoff:
    dependency_markers_present: int
    dependency_markers_total: int
    external_answer_router_ok: bool
    rows: tuple[ExternalPostSourceDANGER3Row, ...]
    row_count: int
    external_source_yes_rows: int
    exact75_source_yes_rows: int
    fixture_source_yes_rows: int
    current_source_theorem_rows: int
    source_stage_closed_rows: int
    policy_or_framing_missing_rows: int
    danger3_unblocked_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    rejected_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def source_candidate(name: str) -> FiniteIdentityFramingCandidate:
    return FiniteIdentityFramingCandidate(
        name=name,
        has_source_theorem=True,
        finite_field_identity_for_p=True,
        generic_cm_or_class_field_generation=False,
        explicit_non_cm_finite_field_framing=False,
        danger3_policy_accepts_identity=False,
        same_j_x18112_bridge=False,
        x16_surface_or_A_xP16=False,
        concrete_A_x0=False,
        official_vpp=False,
    )


def downstream_candidate(
    name: str,
    *,
    generic_cm: bool = False,
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
        explicit_non_cm_finite_field_framing=False,
        danger3_policy_accepts_identity=policy_yes,
        same_j_x18112_bridge=same_j,
        x16_surface_or_A_xP16=x16,
        concrete_A_x0=x0,
        official_vpp=vpp,
    )


def row_from_source_answer(answer: ExternalFrontdoorAnswerRow) -> ExternalPostSourceDANGER3Row:
    decision = classify_candidate(source_candidate(f"{answer.source_query_name}_external_post_source"))
    return ExternalPostSourceDANGER3Row(
        name=f"post_source_{answer.source_query_name}",
        source_family=answer.source_family,
        source_query_name=answer.source_query_name,
        source_answer_name=answer.name,
        route_stage="source_yes_needs_danger3_framing",
        framing_decision=decision,
        current_source_theorem_exists=answer.current_source_theorem_exists,
        source_stage_yes_answer=answer.continue_to_danger3,
        exact75_source_answer=answer.exact75,
        fixture_source_answer=answer.fixture_backed,
        submission_boundary=False,
        current_submission_ready=False,
        ok=answer.continue_to_danger3
        and answer.source_stage_closes
        and not answer.current_source_theorem_exists
        and decision.decision == "source_theorem_closed_policy_or_framing_missing"
        and decision.ok,
    )


def downstream_rows() -> tuple[ExternalPostSourceDANGER3Row, ...]:
    cases = (
        (
            "generic_cm_generation_not_framing",
            "reject_generic_cm_generation_not_framing",
            {"generic_cm": True},
            "reject_generic_cm_generation_not_framing",
            False,
        ),
        (
            "policy_yes_no_same_j_bridge",
            "danger3_unblocked_cross_level_bridge_missing",
            {"policy_yes": True},
            "danger3_unblocked_cross_level_bridge_missing",
            False,
        ),
        (
            "same_j_bridge_no_x16_surface",
            "cross_level_target_identified_specialization_missing",
            {"policy_yes": True, "same_j": True},
            "cross_level_target_identified_specialization_missing",
            False,
        ),
        (
            "x16_surface_no_x0",
            "x16_surface_reached_halving_or_vpp_missing",
            {"policy_yes": True, "same_j": True, "x16": True},
            "x16_surface_reached_halving_or_vpp_missing",
            False,
        ),
        (
            "concrete_A_x0_no_vpp",
            "extraction_ready_vpp_missing",
            {"policy_yes": True, "same_j": True, "x16": True, "x0": True},
            "extraction_ready_vpp_missing",
            False,
        ),
        (
            "official_vpp_verified_boundary",
            "submission_ready",
            {"policy_yes": True, "same_j": True, "x16": True, "x0": True, "vpp": True},
            "submission_ready",
            True,
        ),
    )
    rows = []
    for name, stage, kwargs, expected, submission_boundary in cases:
        decision = classify_candidate(downstream_candidate(name, **kwargs))
        rows.append(
            ExternalPostSourceDANGER3Row(
                name=name,
                source_family="generic_post_source_ladder",
                source_query_name="not_frontdoor_specific",
                source_answer_name="not_frontdoor_specific",
                route_stage=stage,
                framing_decision=decision,
                current_source_theorem_exists=False,
                source_stage_yes_answer=False,
                exact75_source_answer=False,
                fixture_source_answer=False,
                submission_boundary=submission_boundary,
                current_submission_ready=False,
                ok=decision.decision == expected and decision.ok,
            )
        )
    return tuple(rows)


def profile_external_post_source_danger3_handoff() -> ExternalPostSourceDANGER3Handoff:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    answer_router = profile_external_frontdoor_answer_router()
    source_yes_rows = tuple(
        row_from_source_answer(answer)
        for answer in answer_router.rows
        if answer.continue_to_danger3
    )
    rows = source_yes_rows + downstream_rows()
    current_source = sum(row.current_source_theorem_exists for row in rows)
    source_stage_closed = sum(row.framing_decision.source_stage_closed for row in rows)
    policy_missing = sum(
        row.framing_decision.decision == "source_theorem_closed_policy_or_framing_missing"
        for row in rows
    )
    danger3_unblocked = sum(row.framing_decision.danger3_unblocked for row in rows)
    same_j = sum(row.framing_decision.cross_level_bridge_identified for row in rows)
    x16 = sum(row.framing_decision.x16_surface_reached for row in rows)
    extraction = sum(row.framing_decision.extraction_ready for row in rows)
    submission_boundary = sum(row.submission_boundary for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.framing_decision.decision.startswith("reject_") for row in rows)
    source_yes = sum(row.source_stage_yes_answer for row in rows)
    exact75_yes = sum(row.exact75_source_answer for row in rows)
    fixture_yes = sum(row.fixture_source_answer for row in rows)
    decisions = tuple(row.framing_decision.decision for row in rows)
    expected_decisions = (
        "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "reject_generic_cm_generation_not_framing",
            "danger3_unblocked_cross_level_bridge_missing",
            "cross_level_target_identified_specialization_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and answer_router.row_ok
        and len(source_yes_rows) == 5
        and len(rows) == 11
        and source_yes == 5
        and exact75_yes == 1
        and fixture_yes == 4
        and current_source == 0
        and source_stage_closed == 10
        and policy_missing == 5
        and danger3_unblocked == 5
        and same_j == 4
        and x16 == 3
        and extraction == 2
        and submission_boundary == 1
        and current_submission == 0
        and rejected == 1
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalPostSourceDANGER3Handoff(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_answer_router_ok=answer_router.row_ok,
        rows=rows,
        row_count=len(rows),
        external_source_yes_rows=source_yes,
        exact75_source_yes_rows=exact75_yes,
        fixture_source_yes_rows=fixture_yes,
        current_source_theorem_rows=current_source,
        source_stage_closed_rows=source_stage_closed,
        policy_or_framing_missing_rows=policy_missing,
        danger3_unblocked_rows=danger3_unblocked,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_boundary_rows=submission_boundary,
        current_submission_ready_rows=current_submission,
        rejected_rows=rejected,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_post_source_danger3_handoff()
    print("p25 KSY-y external post-source DANGER3 handoff gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_answer_router_ok={int(profile.external_answer_router_ok)}")
    print("handoff_rows")
    for row in profile.rows:
        decision = row.framing_decision
        print(
            "  "
            f"{row.name}: source={row.source_family} stage={row.route_stage} "
            f"decision={decision.decision} "
            f"source_yes={int(row.source_stage_yes_answer)} "
            f"exact75={int(row.exact75_source_answer)} "
            f"fixture={int(row.fixture_source_answer)} "
            f"current_source={int(row.current_source_theorem_exists)} "
            f"danger3={int(decision.danger3_unblocked)} "
            f"same_j={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"extract={int(decision.extraction_ready)} "
            f"submission_boundary={int(row.submission_boundary)} "
            f"current_submission={int(row.current_submission_ready)}"
        )
        print(f"    query={row.source_query_name}")
        print(f"    missing={decision.first_missing_or_falsifier}")
        print(f"    next={decision.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  external_source_yes_rows={profile.external_source_yes_rows}")
    print(f"  exact75_source_yes_rows={profile.exact75_source_yes_rows}")
    print(f"  fixture_source_yes_rows={profile.fixture_source_yes_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  policy_or_framing_missing_rows={profile.policy_or_framing_missing_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print("interpretation")
    print("  external_source_yes_is_not_submission_ready=1")
    print("  exact75_source_yes_uses_the_same_danger3_ladder=1")
    print("  source_yes_first_routes_to_danger3_finite_identity_framing=1")
    print("  generic_cm_generation_remains_rejected_as_framing=1")
    print("  submission_boundary_requires_official_vpp_verified_A_x0=1")
    print(
        "ksy_y_external_post_source_danger3_handoff_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external post-source DANGER3 handoff regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

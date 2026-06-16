#!/usr/bin/env python3
"""Answer-side router for external same-j X_1(8112) bridge questions.

The query packet asks five live external front doors for a same-j bridge from
their odd target to the production X_1(16) side.  This companion gate records
how such answers should be consumed.  A bridge-stage yes is progress to X_1(16)
specialization only; an X_1(16) surface yes still needs halving or direct x0;
shortcut answers without odd payload, same-j gluing, or a known target are
repaired or killed before they can affect the production run.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_x18112_bridge_query_packet_gate import (
    ExternalX18112BridgeQueryRow,
    profile_external_x18112_bridge_query_packet,
)
from p25_ksy_y_post_bridge_x16_surface_intake_gate import (
    profile_post_bridge_x16_surface_intake,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_x18112_bridge_query_packet_20260614.md",
        "ksy_y_external_x18112_bridge_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_post_bridge_x16_surface_intake_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalX18112BridgeAnswerRow:
    name: str
    source_query_name: str
    query_kind: str
    source_lane: str
    odd_payload_object: str
    answer_family: str
    expected_decision: str
    actual_decision: str
    recommendation: str
    first_missing_or_falsifier: str
    continue_to_x16: bool
    continue_to_halving: bool
    repair_or_rewrite: bool
    kill_route: bool
    exact75: bool
    curved_corner: bool
    current_evidence: bool
    current_submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExternalX18112BridgeAnswerRouter:
    dependency_markers_present: int
    dependency_markers_total: int
    query_packet_ok: bool
    post_bridge_surface_intake_ok: bool
    rows: tuple[ExternalX18112BridgeAnswerRow, ...]
    row_count: int
    bridge_stage_yes_rows: int
    x16_surface_yes_rows: int
    hard_falsifier_rows: int
    upstream_only_repair_rows: int
    rewrite_required_rows: int
    continue_to_x16_rows: int
    continue_to_halving_rows: int
    repair_or_rewrite_rows: int
    kill_rows: int
    exact75_rows: int
    curved_corner_rows: int
    current_evidence_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def answer_family_for(row: ExternalX18112BridgeQueryRow) -> str:
    decision = row.decision.decision
    if row.query_kind == "bridge_query" and row.decision.cross_level_bridge_identified:
        return "bridge_stage_yes"
    if row.name == "downstream_x16_surface_no_halving":
        return "x16_surface_yes"
    if decision.startswith("reject_"):
        return "hard_falsifier"
    if decision == "conditional_unknown_odd_target":
        return "rewrite_required"
    if decision == "upstream_odd_value_no_cross_level_bridge":
        return "upstream_only_repair"
    return "unclassified"


def recommendation_for(row: ExternalX18112BridgeQueryRow, answer_family: str) -> str:
    if answer_family == "bridge_stage_yes":
        return "continue_to_X16_surface_specialization"
    if answer_family == "x16_surface_yes":
        return "continue_to_halving_or_direct_x0_then_official_vpp"
    if answer_family == "upstream_only_repair":
        return "repair_missing_same_j_bridge_or_keep_as_source_progress"
    if answer_family == "rewrite_required":
        return "rewrite_onto_accepted_p25_odd_target_before_bridge_work"
    if row.name == "falsify_unglued_level16_level507_components":
        return "kill_unless_same_j_gluing_is_supplied"
    if row.name == "falsify_generic_x16_without_odd_payload":
        return "kill_unless_p25_odd_payload_is_supplied"
    return "kill_or_rewrite_unclassified_answer"


def answer_row(row: ExternalX18112BridgeQueryRow) -> ExternalX18112BridgeAnswerRow:
    family = answer_family_for(row)
    recommendation = recommendation_for(row, family)
    continue_to_x16 = family == "bridge_stage_yes"
    continue_to_halving = family == "x16_surface_yes"
    repair_or_rewrite = family in {"upstream_only_repair", "rewrite_required"}
    kill_route = family == "hard_falsifier"
    ok = (
        row.ok
        and family
        in {
            "bridge_stage_yes",
            "x16_surface_yes",
            "hard_falsifier",
            "upstream_only_repair",
            "rewrite_required",
        }
        and continue_to_x16 == (
            row.query_kind == "bridge_query"
            and row.decision.cross_level_bridge_identified
            and not row.decision.x16_surface_reached
        )
        and continue_to_halving == (
            row.name == "downstream_x16_surface_no_halving"
            and row.decision.x16_surface_reached
        )
        and repair_or_rewrite == row.repair_or_rewrite
        and kill_route == row.kill_route
    )
    return ExternalX18112BridgeAnswerRow(
        name=f"answer_{row.name}",
        source_query_name=row.name,
        query_kind=row.query_kind,
        source_lane=row.source_lane,
        odd_payload_object=row.odd_payload_object,
        answer_family=family,
        expected_decision=row.expected_decision,
        actual_decision=row.decision.decision,
        recommendation=recommendation,
        first_missing_or_falsifier=row.decision.first_missing_clause,
        continue_to_x16=continue_to_x16,
        continue_to_halving=continue_to_halving,
        repair_or_rewrite=repair_or_rewrite,
        kill_route=kill_route,
        exact75=row.exact75,
        curved_corner=row.curved_corner,
        current_evidence=False,
        current_submission_ready=False,
        ok=ok,
    )


def profile_external_x18112_bridge_answer_router() -> ExternalX18112BridgeAnswerRouter:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    query_packet = profile_external_x18112_bridge_query_packet()
    post_bridge = profile_post_bridge_x16_surface_intake()
    rows = tuple(answer_row(row) for row in query_packet.rows)
    bridge_stage = sum(row.answer_family == "bridge_stage_yes" for row in rows)
    x16_surface = sum(row.answer_family == "x16_surface_yes" for row in rows)
    hard_falsifier = sum(row.answer_family == "hard_falsifier" for row in rows)
    upstream_repair = sum(row.answer_family == "upstream_only_repair" for row in rows)
    rewrite = sum(row.answer_family == "rewrite_required" for row in rows)
    continue_x16 = sum(row.continue_to_x16 for row in rows)
    continue_halving = sum(row.continue_to_halving for row in rows)
    repair = sum(row.repair_or_rewrite for row in rows)
    kill = sum(row.kill_route for row in rows)
    exact75 = sum(row.exact75 for row in rows)
    curved = sum(row.curved_corner for row in rows)
    current = sum(row.current_evidence for row in rows)
    submission = sum(row.current_submission_ready for row in rows)
    families = tuple(row.answer_family for row in rows)
    expected_families = (
        "bridge_stage_yes",
        "bridge_stage_yes",
        "bridge_stage_yes",
        "bridge_stage_yes",
        "bridge_stage_yes",
        "upstream_only_repair",
        "hard_falsifier",
        "rewrite_required",
        "hard_falsifier",
        "x16_surface_yes",
    )
    recommendations = tuple(row.recommendation for row in rows)
    expected_recommendations = (
        "continue_to_X16_surface_specialization",
        "continue_to_X16_surface_specialization",
        "continue_to_X16_surface_specialization",
        "continue_to_X16_surface_specialization",
        "continue_to_X16_surface_specialization",
        "repair_missing_same_j_bridge_or_keep_as_source_progress",
        "kill_unless_same_j_gluing_is_supplied",
        "rewrite_onto_accepted_p25_odd_target_before_bridge_work",
        "kill_unless_p25_odd_payload_is_supplied",
        "continue_to_halving_or_direct_x0_then_official_vpp",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and query_packet.row_ok
        and post_bridge.row_ok
        and post_bridge.current_evidence_rows == 0
        and post_bridge.submission_ready_rows == 1
        and post_bridge.current_evidence_rows < post_bridge.submission_ready_rows
        and len(rows) == 10
        and bridge_stage == 5
        and x16_surface == 1
        and hard_falsifier == 2
        and upstream_repair == 1
        and rewrite == 1
        and continue_x16 == 5
        and continue_halving == 1
        and repair == 2
        and kill == 2
        and exact75 == 4
        and curved == 1
        and current == 0
        and submission == 0
        and families == expected_families
        and recommendations == expected_recommendations
        and all(row.ok for row in rows)
    )
    return ExternalX18112BridgeAnswerRouter(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        query_packet_ok=query_packet.row_ok,
        post_bridge_surface_intake_ok=post_bridge.row_ok,
        rows=rows,
        row_count=len(rows),
        bridge_stage_yes_rows=bridge_stage,
        x16_surface_yes_rows=x16_surface,
        hard_falsifier_rows=hard_falsifier,
        upstream_only_repair_rows=upstream_repair,
        rewrite_required_rows=rewrite,
        continue_to_x16_rows=continue_x16,
        continue_to_halving_rows=continue_halving,
        repair_or_rewrite_rows=repair,
        kill_rows=kill,
        exact75_rows=exact75,
        curved_corner_rows=curved,
        current_evidence_rows=current,
        current_submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_x18112_bridge_answer_router()
    print("p25 KSY-y external same-j X1(8112) bridge answer router gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  query_packet_ok={int(profile.query_packet_ok)}")
    print(f"  post_bridge_surface_intake_ok={int(profile.post_bridge_surface_intake_ok)}")
    print("answer_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: query={row.source_query_name} kind={row.query_kind} "
            f"lane={row.source_lane} odd={row.odd_payload_object} "
            f"family={row.answer_family} decision={row.actual_decision} "
            f"to_x16={int(row.continue_to_x16)} "
            f"to_halving={int(row.continue_to_halving)} "
            f"repair={int(row.repair_or_rewrite)} kill={int(row.kill_route)} "
            f"exact75={int(row.exact75)} curved={int(row.curved_corner)} "
            f"current={int(row.current_evidence)} "
            f"submission={int(row.current_submission_ready)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
        print(f"    recommendation={row.recommendation}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  bridge_stage_yes_rows={profile.bridge_stage_yes_rows}")
    print(f"  x16_surface_yes_rows={profile.x16_surface_yes_rows}")
    print(f"  hard_falsifier_rows={profile.hard_falsifier_rows}")
    print(f"  upstream_only_repair_rows={profile.upstream_only_repair_rows}")
    print(f"  rewrite_required_rows={profile.rewrite_required_rows}")
    print(f"  continue_to_x16_rows={profile.continue_to_x16_rows}")
    print(f"  continue_to_halving_rows={profile.continue_to_halving_rows}")
    print(f"  repair_or_rewrite_rows={profile.repair_or_rewrite_rows}")
    print(f"  kill_rows={profile.kill_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  curved_corner_rows={profile.curved_corner_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  positive_external_bridge_answer_routes_to_X16_specialization_not_submission=1")
    print("  upstream_odd_theorem_without_same_j_bridge_is_source_progress_only=1")
    print("  unglued_or_generic_X16_shortcuts_are_killed=1")
    print("  X16_surface_answer_still_needs_halving_or_direct_x0_and_official_vpp=1")
    print(
        "ksy_y_external_x18112_bridge_answer_router_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external X1(8112) bridge answer router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Answer router for the external front-door KSY-y source packet.

The query packet names five possible closing answers and five falsifiers.  This
gate turns returned expert/literature answers into one of three actions:
continue to DANGER3 framing, repair a missing clause, or kill/rewrite the
claim.  It deliberately reuses the existing source classifiers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_external_frontdoor_query_packet_gate import (
    ExternalFrontdoorQueryRow,
    profile_external_frontdoor_query_packet,
)
from p25_ksy_y_priority1_divisor_additive_intake_gate import (
    Priority1DivisorAdditiveRow,
    classify_packet,
    packet_from_mapping,
)
from p25_ksy_y_priority1_source_answer_router_gate import (
    profile_priority1_source_answer_router,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    ClosingTheoremClaim,
    ClosingTheoremDecision,
    classify_claim as classify_exact_product_claim,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_query_packet_20260614.md",
        "ksy_y_external_frontdoor_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_source_answer_router_20260614.md",
        "ksy_y_priority1_source_answer_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH
        / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation.md",
        "robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalFrontdoorAnswerRow:
    name: str
    source_query_name: str
    query_kind: str
    answer_family: str
    source_family: str
    expected_decision: str
    actual_decision: str
    source_stage_closes: bool
    current_source_theorem_exists: bool
    recommendation: str
    continue_to_danger3: bool
    repair_needed: bool
    kill_route: bool
    exact75: bool
    fixture_backed: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class ExternalFrontdoorAnswerRouter:
    dependency_markers_present: int
    dependency_markers_total: int
    query_packet_ok: bool
    priority1_answer_router_ok: bool
    rows: tuple[ExternalFrontdoorAnswerRow, ...]
    row_count: int
    source_closing_rows: int
    current_source_theorem_rows: int
    continue_to_danger3_rows: int
    repair_needed_rows: int
    kill_route_rows: int
    exact75_rows: int
    fixture_backed_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def read_packet(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: packet JSON must be an object")
    return data


def fixture_path_from_command(command: str) -> Path:
    for token in command.split():
        if "priority1_divisor_additive_packet_fixtures" in token and token.endswith(".json"):
            return Path(token)
    raise ValueError(f"no priority-1 fixture path in command: {command}")


def exact_product_claim(query: ExternalFrontdoorQueryRow) -> ClosingTheoremClaim:
    output_kind = "value" if "value_without_period156" in query.name else "divisor-additive"
    return ClosingTheoremClaim(
        name=query.name,
        source_family=query.source_family,
        emits_exact_p=True,
        preserves_mixed_graph=True,
        equal_weight_atoms=True,
        orientation_recorded=True,
        arithmetic_source_theorem=True,
        output_kind=output_kind,
        finite_field_identity_for_p=True,
        period_156_context=False,
        danger3_policy_or_non_cm_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def recommendation_for(actual_decision: str, source_stage_closes: bool) -> tuple[str, bool, bool, bool]:
    if source_stage_closes:
        return (
            "continue_to_DANGER3_framing_and_same_j_extraction",
            True,
            False,
            False,
        )
    if actual_decision.startswith("reject_"):
        return ("kill_or_rewrite_source_claim", False, False, True)
    if actual_decision == "conditional_value_missing_period_156":
        return ("repair_missing_period156_then_resubmit_packet", False, True, False)
    return ("repair_missing_clause_then_resubmit_packet", False, True, False)


def answer_family(
    query: ExternalFrontdoorQueryRow,
    actual_decision: str,
    source_stage_closes: bool,
) -> str:
    if source_stage_closes:
        return "source_stage_yes"
    if actual_decision.startswith("reject_"):
        return "hard_falsifier"
    if query.query_kind == "falsifier":
        return "expected_near_miss"
    return "conditional_near_miss"


def row_from_priority1_decision(
    query: ExternalFrontdoorQueryRow,
    decision: Priority1DivisorAdditiveRow,
) -> ExternalFrontdoorAnswerRow:
    recommendation, continue_to_danger3, repair_needed, kill_route = recommendation_for(
        decision.actual_decision,
        decision.source_stage_closes,
    )
    return ExternalFrontdoorAnswerRow(
        name=f"answer_{query.name}",
        source_query_name=query.name,
        query_kind=query.query_kind,
        answer_family=answer_family(query, decision.actual_decision, decision.source_stage_closes),
        source_family=query.source_family,
        expected_decision=query.expected_decision,
        actual_decision=decision.actual_decision,
        source_stage_closes=decision.source_stage_closes,
        current_source_theorem_exists=False,
        recommendation=recommendation,
        continue_to_danger3=continue_to_danger3,
        repair_needed=repair_needed,
        kill_route=kill_route,
        exact75=False,
        fixture_backed=True,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        next_action=decision.next_action,
        ok=decision.ok and decision.actual_decision == query.expected_decision,
    )


def row_from_exact75_decision(
    query: ExternalFrontdoorQueryRow,
    decision: ClosingTheoremDecision,
) -> ExternalFrontdoorAnswerRow:
    recommendation, continue_to_danger3, repair_needed, kill_route = recommendation_for(
        decision.decision,
        decision.source_theorem_closed,
    )
    return ExternalFrontdoorAnswerRow(
        name=f"answer_{query.name}",
        source_query_name=query.name,
        query_kind=query.query_kind,
        answer_family=answer_family(query, decision.decision, decision.source_theorem_closed),
        source_family=query.source_family,
        expected_decision=query.expected_decision,
        actual_decision=decision.decision,
        source_stage_closes=decision.source_theorem_closed,
        current_source_theorem_exists=False,
        recommendation=recommendation,
        continue_to_danger3=continue_to_danger3,
        repair_needed=repair_needed,
        kill_route=kill_route,
        exact75=True,
        fixture_backed=False,
        first_missing_or_falsifier=decision.first_missing_clause,
        next_action=decision.next_action,
        ok=decision.row_ok and decision.decision == query.expected_decision,
    )


def answer_row(query: ExternalFrontdoorQueryRow) -> ExternalFrontdoorAnswerRow:
    if "exact_75" in query.name:
        return row_from_exact75_decision(
            query,
            classify_exact_product_claim(exact_product_claim(query)),
        )

    fixture_path = fixture_path_from_command(query.local_command)
    packet = packet_from_mapping(read_packet(fixture_path))
    return row_from_priority1_decision(query, classify_packet(packet))


def profile_external_frontdoor_answer_router() -> ExternalFrontdoorAnswerRouter:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    query = profile_external_frontdoor_query_packet()
    priority1 = profile_priority1_source_answer_router()
    rows = tuple(answer_row(row) for row in query.rows)
    source_closing = sum(row.source_stage_closes for row in rows)
    current_source = sum(row.current_source_theorem_exists for row in rows)
    continue_rows = sum(row.continue_to_danger3 for row in rows)
    repair = sum(row.repair_needed for row in rows)
    kill = sum(row.kill_route for row in rows)
    exact75 = sum(row.exact75 for row in rows)
    fixture_backed = sum(row.fixture_backed for row in rows)
    expected = (
        "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_divisor_identity_missing_h90_boundary",
            "reject_loses_mixed_tensor",
            "conditional_value_theorem_missing_period156_context",
            "conditional_missing_period156_context",
            "conditional_value_missing_period_156",
        )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and query.row_ok
        and priority1.row_ok
        and len(rows) == 10
        and source_closing == 5
        and current_source == 0
        and continue_rows == 5
        and repair == 4
        and kill == 1
        and exact75 == 2
        and fixture_backed == 8
        and tuple(row.actual_decision for row in rows) == expected
        and tuple(row.expected_decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    return ExternalFrontdoorAnswerRouter(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        query_packet_ok=query.row_ok,
        priority1_answer_router_ok=priority1.row_ok,
        rows=rows,
        row_count=len(rows),
        source_closing_rows=source_closing,
        current_source_theorem_rows=current_source,
        continue_to_danger3_rows=continue_rows,
        repair_needed_rows=repair,
        kill_route_rows=kill,
        exact75_rows=exact75,
        fixture_backed_rows=fixture_backed,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_frontdoor_answer_router()
    print("p25 KSY-y external front-door answer router gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  query_packet_ok={int(profile.query_packet_ok)}")
    print(f"  priority1_answer_router_ok={int(profile.priority1_answer_router_ok)}")
    print("answer_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: query={row.source_query_name} kind={row.query_kind} "
            f"family={row.answer_family} decision={row.actual_decision} "
            f"closes={int(row.source_stage_closes)} current_source={int(row.current_source_theorem_exists)} "
            f"continue={int(row.continue_to_danger3)} repair={int(row.repair_needed)} "
            f"kill={int(row.kill_route)} exact75={int(row.exact75)} "
            f"fixture={int(row.fixture_backed)} recommendation={row.recommendation}"
        )
        print(f"    source={row.source_family}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  continue_to_danger3_rows={profile.continue_to_danger3_rows}")
    print(f"  repair_needed_rows={profile.repair_needed_rows}")
    print(f"  kill_route_rows={profile.kill_route_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  fixture_backed_rows={profile.fixture_backed_rows}")
    print("interpretation")
    print("  five_source_stage_yes_answers_continue_to_DANGER3_not_submission=1")
    print("  exact75_answers_route_through_closing_theorem_obligation=1")
    print("  near_misses_return_repair_clauses=1")
    print("  projection_or_axis_only_answers_are_killed=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_external_frontdoor_answer_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("external front-door answer router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

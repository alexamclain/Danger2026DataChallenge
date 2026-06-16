#!/usr/bin/env python3
"""Answer router for priority-1 divisor/additive source claims."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_priority1_divisor_additive_intake_gate import (
    Priority1DivisorAdditiveRow,
    classify_packet,
    packet_from_mapping,
)
from p25_ksy_y_priority1_source_query_packet_gate import (
    Priority1SourceQueryRow,
    profile_priority1_source_query_packet,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_priority1_source_query_packet_20260614.md",
        "ksy_y_priority1_source_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_packet_fixture_export_rows=1/1",
    ),
)


@dataclass(frozen=True)
class Priority1SourceAnswerRow:
    name: str
    source_query_name: str
    answer_family: str
    fixture_path: Path
    expected_decision: str
    actual_decision: str
    source_stage_closes: bool
    current_source_theorem_exists: bool
    recommendation: str
    continue_to_danger3: bool
    repair_needed: bool
    kill_route: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class Priority1SourceAnswerRouter:
    dependency_markers_present: int
    dependency_markers_total: int
    query_packet_ok: bool
    rows: tuple[Priority1SourceAnswerRow, ...]
    row_count: int
    source_closing_rows: int
    current_source_theorem_rows: int
    continue_to_danger3_rows: int
    repair_needed_rows: int
    kill_route_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def read_packet(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: packet JSON must be an object")
    return data


def recommendation_for(decision: Priority1DivisorAdditiveRow) -> tuple[str, bool, bool, bool]:
    if decision.source_stage_closes:
        return (
            "continue_to_DANGER3_framing_and_same_j_extraction",
            True,
            False,
            False,
        )
    if decision.rejected:
        return ("kill_or_rewrite_source_claim", False, False, True)
    return ("repair_missing_clause_then_resubmit_packet", False, True, False)


def answer_family(query: Priority1SourceQueryRow, decision: Priority1DivisorAdditiveRow) -> str:
    if decision.source_stage_closes:
        return "source_stage_yes"
    if decision.rejected:
        return "hard_falsifier"
    if query.query_kind == "falsifier":
        return "expected_near_miss"
    return "conditional_near_miss"


def answer_row(query: Priority1SourceQueryRow) -> Priority1SourceAnswerRow:
    packet = packet_from_mapping(read_packet(query.fixture_path))
    decision = classify_packet(packet)
    recommendation, continue_to_danger3, repair_needed, kill_route = recommendation_for(decision)
    return Priority1SourceAnswerRow(
        name=f"answer_{query.name}",
        source_query_name=query.name,
        answer_family=answer_family(query, decision),
        fixture_path=query.fixture_path,
        expected_decision=query.expected_decision,
        actual_decision=decision.actual_decision,
        source_stage_closes=decision.source_stage_closes,
        current_source_theorem_exists=decision.current_source_theorem_exists,
        recommendation=recommendation,
        continue_to_danger3=continue_to_danger3,
        repair_needed=repair_needed,
        kill_route=kill_route,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        next_action=decision.next_action,
        ok=decision.ok and decision.actual_decision == query.expected_decision,
    )


def profile_priority1_source_answer_router() -> Priority1SourceAnswerRouter:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    query = profile_priority1_source_query_packet()
    rows = tuple(answer_row(row) for row in query.query_rows)
    source_closing = sum(row.source_stage_closes for row in rows)
    current_source = sum(row.current_source_theorem_exists for row in rows)
    continue_rows = sum(row.continue_to_danger3 for row in rows)
    repair = sum(row.repair_needed for row in rows)
    kill = sum(row.kill_route for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and query.row_ok
        and len(rows) == 8
        and source_closing == 4
        and current_source == 0
        and continue_rows == 4
        and repair == 3
        and kill == 1
        and tuple(row.actual_decision for row in rows)
        == (
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_divisor_identity_missing_h90_boundary",
            "reject_loses_mixed_tensor",
            "conditional_value_theorem_missing_period156_context",
            "conditional_missing_period156_context",
        )
        and all(row.ok for row in rows)
    )
    return Priority1SourceAnswerRouter(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        query_packet_ok=query.row_ok,
        rows=rows,
        row_count=len(rows),
        source_closing_rows=source_closing,
        current_source_theorem_rows=current_source,
        continue_to_danger3_rows=continue_rows,
        repair_needed_rows=repair,
        kill_route_rows=kill,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_priority1_source_answer_router()
    print("p25 KSY-y priority-1 source-answer router gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  query_packet_ok={int(profile.query_packet_ok)}")
    print("answer_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: query={row.source_query_name} family={row.answer_family} "
            f"decision={row.actual_decision} closes={int(row.source_stage_closes)} "
            f"current_source={int(row.current_source_theorem_exists)} "
            f"continue={int(row.continue_to_danger3)} repair={int(row.repair_needed)} "
            f"kill={int(row.kill_route)} recommendation={row.recommendation}"
        )
        print(f"    fixture={row.fixture_path}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  continue_to_danger3_rows={profile.continue_to_danger3_rows}")
    print(f"  repair_needed_rows={profile.repair_needed_rows}")
    print(f"  kill_route_rows={profile.kill_route_rows}")
    print("interpretation")
    print("  source_stage_yes_answers_continue_to_DANGER3_not_submission=1")
    print("  near_misses_return_a_repair_clause=1")
    print("  projection_or_axis_only_answers_are_killed=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_priority1_source_answer_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 source-answer router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

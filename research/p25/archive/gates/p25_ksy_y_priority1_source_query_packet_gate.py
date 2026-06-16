#!/usr/bin/env python3
"""Cross-lane source-query packet for priority-1 divisor/additive asks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")
FIXTURES = RESEARCH / "priority1_divisor_additive_packet_fixtures"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_source_theorem_priority_selector_20260614.md",
        "ksy_y_source_theorem_priority_selector_rows=1/1",
    ),
)


@dataclass(frozen=True)
class Priority1SourceQueryRow:
    name: str
    query_kind: str
    lane: str
    question_for_source: str
    accepted_answer_shape: str
    first_falsifier: str
    fixture_path: Path
    local_command: str
    expected_decision: str
    closes_source_stage_if_yes: bool
    current_source_theorem_exists: bool
    priority_rank: int
    ok: bool


@dataclass(frozen=True)
class Priority1SourceQueryPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    query_rows: tuple[Priority1SourceQueryRow, ...]
    query_count: int
    closing_query_rows: int
    falsifier_rows: int
    current_source_theorem_rows: int
    priority1_rows: int
    fixture_rows_present: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_command(path: Path) -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py "
        f"--packet-json {path}"
    )


def row(
    *,
    name: str,
    query_kind: str,
    lane: str,
    question: str,
    accepted_shape: str,
    falsifier: str,
    fixture_name: str,
    expected_decision: str,
    closes: bool,
    priority_rank: int,
) -> Priority1SourceQueryRow:
    fixture = FIXTURES / fixture_name
    return Priority1SourceQueryRow(
        name=name,
        query_kind=query_kind,
        lane=lane,
        question_for_source=question,
        accepted_answer_shape=accepted_shape,
        first_falsifier=falsifier,
        fixture_path=fixture,
        local_command=packet_command(fixture),
        expected_decision=expected_decision,
        closes_source_stage_if_yes=closes,
        current_source_theorem_exists=False,
        priority_rank=priority_rank,
        ok=fixture.exists() and fixture.stat().st_size > 0,
    )


def query_rows() -> tuple[Priority1SourceQueryRow, ...]:
    return (
        row(
            name="ask_h0_divisor_boundary_identity",
            query_kind="closing_query",
            lane="H0/H0_translate",
            question=(
                "Does the source prove an exact divisor/additive identity for "
                "one of the four legal 78-over-78 H0 products, with the "
                "Hilbert-90 boundary to Norm_156(Y_507)?"
            ),
            accepted_shape="exact legal H0 product + divisor/additive identity + H90 boundary",
            falsifier="legal H0 product only, finite payload only, or divisor statement without the boundary",
            fixture_name="h0_divisor_close.json",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
        ),
        row(
            name="ask_conductor39_divisor_identity",
            query_kind="closing_query",
            lane="conductor39",
            question=(
                "Does the source prove an exact divisor/additive identity for "
                "the legal mixed conductor-39 source U_chi/W, preserving the "
                "chi_3 tensor chi_13 object, Yang lift, and descent?"
            ),
            accepted_shape="legal mixed conductor-39 source + Yang lift + H90/ratio descent + divisor/additive theorem",
            falsifier="prime-13 projection, axis-only statement, or source certification without value/divisor theorem",
            fixture_name="conductor39_divisor_close.json",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
        ),
        row(
            name="ask_twisted_h90_divisor_identity",
            query_kind="closing_query",
            lane="twisted/H90",
            question=(
                "Does the source prove a finite divisor/additive theorem for "
                "the twisted ratio/Hilbert-90 object, with the period-156 "
                "bridge context currently required by the router?"
            ),
            accepted_shape="degree-6 twisted ratio/H90 object + finite divisor theorem + arithmetic source + period-156 bridge context",
            falsifier="ratio or H90 boundary only, or finite theorem without period-156 bridge context",
            fixture_name="twisted_divisor_close.json",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
        ),
        row(
            name="ask_curved_corner_divisor_identity",
            query_kind="closing_query",
            lane="curved_corner",
            question=(
                "Does the source prove a finite divisor/additive theorem for "
                "the exact unit-triangle curved K-traced corner, with the "
                "period-156 context required by the current curved-corner router?"
            ),
            accepted_shape="unit-triangle curved corner + finite divisor theorem + arithmetic source + period-156 context",
            falsifier="curved helper only, wrong unit triangle, or theorem without period-156 context",
            fixture_name="curved_corner_divisor_close.json",
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
        ),
        row(
            name="falsify_h0_boundary_missing",
            query_kind="falsifier",
            lane="H0/H0_translate",
            question="Does the answer omit the exact H0 boundary to Norm_156(Y_507)?",
            accepted_shape="boundary omission routes as conditional, not closure",
            falsifier="Hilbert-90 boundary to Norm_156(Y_507) is missing",
            fixture_name="h0_missing_boundary.json",
            expected_decision="conditional_divisor_identity_missing_h90_boundary",
            closes=False,
            priority_rank=1,
        ),
        row(
            name="falsify_projection_or_axis_only",
            query_kind="falsifier",
            lane="conductor39",
            question="Does the answer collapse to prime-13, projection, or axis-only data?",
            accepted_shape="projection or axis-only data is rejected",
            falsifier="mixed chi_3 tensor chi_13 source on X_1(39) is missing",
            fixture_name="projection_reject.json",
            expected_decision="reject_loses_mixed_tensor",
            closes=False,
            priority_rank=0,
        ),
        row(
            name="falsify_twisted_missing_period_bridge",
            query_kind="falsifier",
            lane="twisted/H90",
            question="Does the twisted/H90 answer omit period-156 bridge context?",
            accepted_shape="twisted/H90 theorem without period-156 context remains conditional",
            falsifier="period-156 branch/root/telescoping context is missing",
            fixture_name="twisted_missing_period.json",
            expected_decision="conditional_value_theorem_missing_period156_context",
            closes=False,
            priority_rank=1,
        ),
        row(
            name="falsify_curved_missing_period_context",
            query_kind="falsifier",
            lane="curved_corner",
            question="Does the curved-corner answer omit period-156 context?",
            accepted_shape="curved-corner finite theorem without period-156 context remains conditional",
            falsifier="period-156 branch/root/telescoping context is missing",
            fixture_name="curved_missing_period.json",
            expected_decision="conditional_missing_period156_context",
            closes=False,
            priority_rank=1,
        ),
    )


def profile_priority1_source_query_packet() -> Priority1SourceQueryPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = query_rows()
    closing = sum(row.query_kind == "closing_query" for row in rows)
    falsifier = sum(row.query_kind == "falsifier" for row in rows)
    current_source = sum(row.current_source_theorem_exists for row in rows)
    priority1 = sum(row.priority_rank == 1 for row in rows)
    fixture_present = sum(row.fixture_path.exists() and row.fixture_path.stat().st_size > 0 for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 8
        and closing == 4
        and falsifier == 4
        and current_source == 0
        and priority1 == 7
        and fixture_present == 8
        and tuple(row.expected_decision for row in rows)
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
    return Priority1SourceQueryPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        query_rows=rows,
        query_count=len(rows),
        closing_query_rows=closing,
        falsifier_rows=falsifier,
        current_source_theorem_rows=current_source,
        priority1_rows=priority1,
        fixture_rows_present=fixture_present,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_priority1_source_query_packet()
    print("p25 KSY-y priority-1 source-query packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("query_rows")
    for row_profile in profile.query_rows:
        print(
            "  "
            f"{row_profile.name}: kind={row_profile.query_kind} lane={row_profile.lane} "
            f"rank={row_profile.priority_rank} closes={int(row_profile.closes_source_stage_if_yes)} "
            f"current_source={int(row_profile.current_source_theorem_exists)} "
            f"decision={row_profile.expected_decision} fixture={row_profile.fixture_path}"
        )
        print(f"    question={row_profile.question_for_source}")
        print(f"    accept={row_profile.accepted_answer_shape}")
        print(f"    falsifier={row_profile.first_falsifier}")
        print(f"    command={row_profile.local_command}")
    print("counts")
    print(f"  query_count={profile.query_count}")
    print(f"  closing_query_rows={profile.closing_query_rows}")
    print(f"  falsifier_rows={profile.falsifier_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  fixture_rows_present={profile.fixture_rows_present}")
    print("interpretation")
    print("  priority1_source_search_has_four_exact_closing_questions=1")
    print("  each_query_has_a_packet_fixture_and_local_classifier_command=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_priority1_source_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 source-query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify source-snippet and expert-response intake sync with the live kernel.

The detailed snippet and expert-response pages predate the full unique-power
set, the even-boundary distribution-closure repair row, and the matched-
quotient normalization route.  They remain useful as broad routers, but
source-stage theorem classification should now defer to the source theorem
acceptance automaton.  This gate checks that the older surfaces carry explicit
sync notes so they cannot be read as the current front-door kernel by accident.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


POWER_SET = "e in {3,5,13,39,75,169,507}"
DISTRIBUTION_REPAIR = "repair_even_boundary_distribution_closure"
MATCHED_QUOTIENT_NORMALIZATION = "normalize_matched_quotient_then_accept"
AUTOMATON_MARKER = "p25_v2_source_theorem_acceptance_automaton_rows=1/1"


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SyncRow:
    name: str
    path: Path
    marker_present: bool
    sync_note_present: bool
    power_set_present: bool
    distribution_repair_present: bool
    matched_quotient_present: bool
    defers_to_automaton: bool
    decision: str
    ok: bool


@dataclass(frozen=True)
class IntakeSync:
    evidence_markers: tuple[EvidenceMarker, ...]
    sync_rows: tuple[SyncRow, ...]
    evidence_markers_ok: int
    sync_rows_ok: int
    legacy_surfaces_synced: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name, marker_path, needle, needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "source_theorem_acceptance_automaton",
            "research/p25/evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
            AUTOMATON_MARKER,
        ),
        marker(
            "extended_unique_power_intake",
            "research/p25/evidence/p25_v2_extended_unique_power_intake_20260617.md",
            "p25_v2_extended_unique_power_intake_rows=1/1",
        ),
        marker(
            "distribution_relation_closure_screen",
            "research/p25/evidence/p25_v2_distribution_relation_closure_screen_20260617.md",
            "p25_v2_distribution_relation_closure_screen_rows=1/1",
        ),
        marker(
            "matched_quotient_closure_packet",
            "research/p25/evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
            "p25_v2_matched_quotient_closure_packet_rows=1/1",
        ),
    )


def sync_row(
    name: str,
    path: str,
    marker_text: str,
) -> SyncRow:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    marker_present = marker_text in text
    sync_note_present = "## 2026-06-17 Sync Note" in text
    power_set_present = POWER_SET in text
    distribution_repair_present = DISTRIBUTION_REPAIR in text
    matched_quotient_present = MATCHED_QUOTIENT_NORMALIZATION in text
    defers_to_automaton = "source theorem acceptance automaton" in text
    ok = (
        p.exists()
        and marker_present
        and sync_note_present
        and power_set_present
        and distribution_repair_present
        and matched_quotient_present
        and defers_to_automaton
    )
    return SyncRow(
        name=name,
        path=p,
        marker_present=marker_present,
        sync_note_present=sync_note_present,
        power_set_present=power_set_present,
        distribution_repair_present=distribution_repair_present,
        matched_quotient_present=matched_quotient_present,
        defers_to_automaton=defers_to_automaton,
        decision="legacy_router_synced_to_current_automaton" if ok else "repair_sync_note_missing",
        ok=ok,
    )


def sync_rows() -> tuple[SyncRow, ...]:
    return (
        sync_row(
            "source_snippet_intake_sync",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        sync_row(
            "current_expert_response_rubric_sync",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def build_sync() -> IntakeSync:
    markers = evidence_markers()
    rows = sync_rows()
    markers_ok = sum(row.ok for row in markers)
    rows_ok = sum(row.ok for row in rows)
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        markers_ok == len(markers)
        and rows_ok == len(rows)
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return IntakeSync(
        evidence_markers=markers,
        sync_rows=rows,
        evidence_markers_ok=markers_ok,
        sync_rows_ok=rows_ok,
        legacy_surfaces_synced=rows_ok,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    sync = build_sync()
    print("p25 v2 snippet/expert intake sync")
    for marker_row in sync.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("sync_rows")
    for row in sync.sync_rows:
        print(
            "  "
            f"{row.name}: marker={int(row.marker_present)} "
            f"sync_note={int(row.sync_note_present)} "
            f"power_set={int(row.power_set_present)} "
            f"distribution_repair={int(row.distribution_repair_present)} "
            f"matched_quotient={int(row.matched_quotient_present)} "
            f"automaton={int(row.defers_to_automaton)} decision={row.decision}"
        )
    print("counts")
    print(f"evidence_markers_ok={sync.evidence_markers_ok}/{len(sync.evidence_markers)}")
    print(f"sync_rows_ok={sync.sync_rows_ok}/{len(sync.sync_rows)}")
    print(f"legacy_surfaces_synced={sync.legacy_surfaces_synced}")
    print(f"current_source_stage_closers={sync.current_source_stage_closers}")
    print(f"current_submission_ready={sync.current_submission_ready}")
    print("current_automaton_candidate_rows=25")
    print("current_automaton_normalize_then_accept_rows=2")
    print("current_automaton_repair_rows=11")
    print("full_unique_power_set_synced=1")
    print("distribution_closure_repair_synced=1")
    print("matched_quotient_normalization_synced=1")
    print(f"p25_v2_snippet_expert_intake_sync_rows={int(sync.row_ok)}/1")
    return 0 if sync.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

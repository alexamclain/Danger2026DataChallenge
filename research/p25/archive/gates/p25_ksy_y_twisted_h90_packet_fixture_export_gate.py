#!/usr/bin/env python3
"""Fixture audit for twisted/H90 candidate-packet JSON files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from p25_ksy_y_twisted_h90_candidate_packet_intake_gate import (
    TwistedH90CandidatePacket,
    TwistedH90CandidatePacketDecision,
    classify_packet,
    packet_from_mapping,
)


REPO = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO / "research" / "p25" / "twisted_h90_candidate_packet_fixtures"

EXPECTED_DECISIONS = (
    ("pure_degree6_norm_reject.json", "reject_pure_degree6_norm_cancels"),
    ("minimal_source_yes_no_framing.json", "source_theorem_closed_policy_or_framing_missing"),
    ("policy_yes_no_bridge.json", "danger3_unblocked_cross_level_bridge_missing"),
    ("same_j_bridge_no_x16.json", "cross_level_target_identified_specialization_missing"),
    ("official_vpp_verified_boundary.json", "submission_ready"),
)


@dataclass(frozen=True)
class PacketFixtureRow:
    filename: str
    raw_sha256: str
    canonical_sha256: str
    packet: TwistedH90CandidatePacket
    decision: TwistedH90CandidatePacketDecision
    expected_decision: str
    field_count: int
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    ok: bool


@dataclass(frozen=True)
class TwistedH90PacketFixtureExportProfile:
    fixture_dir_present: bool
    expected_fixture_count: int
    fixture_count: int
    rows: tuple[PacketFixtureRow, ...]
    exact_field_rows: int
    decision_match_rows: int
    rejected_rows: int
    source_stage_closed_rows: int
    danger3_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: top-level JSON must be an object")
    return data, text


def fixture_row(filename: str, expected_decision: str) -> PacketFixtureRow:
    path = FIXTURE_DIR / filename
    data, raw_text = read_json(path)
    expected_fields = set(TwistedH90CandidatePacket.__dataclass_fields__)
    actual_fields = set(data)
    missing = tuple(sorted(expected_fields - actual_fields))
    unknown = tuple(sorted(actual_fields - expected_fields))
    packet = packet_from_mapping(data)
    decision = classify_packet(packet)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n"
    ok = (
        path.exists()
        and not missing
        and not unknown
        and len(data) == len(expected_fields)
        and decision.decision == expected_decision
        and decision.ok
    )
    return PacketFixtureRow(
        filename=filename,
        raw_sha256=sha256(raw_text.encode()).hexdigest(),
        canonical_sha256=sha256(canonical.encode()).hexdigest(),
        packet=packet,
        decision=decision,
        expected_decision=expected_decision,
        field_count=len(data),
        missing_fields=missing,
        unknown_fields=unknown,
        ok=ok,
    )


def profile_twisted_h90_packet_fixture_export() -> TwistedH90PacketFixtureExportProfile:
    rows = tuple(fixture_row(filename, decision) for filename, decision in EXPECTED_DECISIONS)
    exact_fields = sum(not row.missing_fields and not row.unknown_fields for row in rows)
    decision_matches = sum(row.decision.decision == row.expected_decision for row in rows)
    rejected = sum(row.decision.rejected for row in rows)
    source_closed = sum(row.decision.source_stage_closed for row in rows)
    danger3 = sum(row.decision.danger3_unblocked for row in rows)
    cross_level = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16 = sum(row.decision.x16_surface_reached for row in rows)
    extraction = sum(row.decision.extraction_ready for row in rows)
    submission = sum(row.decision.submission_ready for row in rows)
    fixture_count = sum((FIXTURE_DIR / filename).exists() for filename, _decision in EXPECTED_DECISIONS)
    row_ok = (
        FIXTURE_DIR.exists()
        and fixture_count == 5
        and len(rows) == 5
        and exact_fields == 5
        and decision_matches == 5
        and rejected == 1
        and source_closed == 4
        and danger3 == 3
        and cross_level == 2
        and x16 == 1
        and extraction == 1
        and submission == 1
        and all(row.ok for row in rows)
    )
    return TwistedH90PacketFixtureExportProfile(
        fixture_dir_present=FIXTURE_DIR.exists(),
        expected_fixture_count=len(EXPECTED_DECISIONS),
        fixture_count=fixture_count,
        rows=rows,
        exact_field_rows=exact_fields,
        decision_match_rows=decision_matches,
        rejected_rows=rejected,
        source_stage_closed_rows=source_closed,
        danger3_unblocked_rows=danger3,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_twisted_h90_packet_fixture_export()
    print("p25 KSY-y twisted/H90 packet fixture export gate")
    print("fixtures")
    print(f"  fixture_dir={FIXTURE_DIR}")
    print(f"  fixture_dir_present={int(profile.fixture_dir_present)}")
    print(f"  expected_fixture_count={profile.expected_fixture_count}")
    print(f"  fixture_count={profile.fixture_count}")
    print("fixture_rows")
    for row in profile.rows:
        decision = row.decision
        print(
            "  "
            f"{row.filename}: decision={decision.decision} "
            f"expected={row.expected_decision} "
            f"fields={row.field_count} "
            f"source_closed={int(decision.source_stage_closed)} "
            f"danger3={int(decision.danger3_unblocked)} "
            f"same_j={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"extraction={int(decision.extraction_ready)} "
            f"submission={int(decision.submission_ready)}"
        )
        print(f"    raw_sha256={row.raw_sha256}")
        print(f"    canonical_sha256={row.canonical_sha256}")
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"  exact_field_rows={profile.exact_field_rows}")
    print(f"  decision_match_rows={profile.decision_match_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  twisted_h90_packet_fixtures_are_stable_json_intake_examples=1")
    print("  fixtures_cover_kill_source_policy_bridge_and_submission_boundaries=1")
    print(f"ksy_y_twisted_h90_packet_fixture_export_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("twisted/H90 packet fixture export regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

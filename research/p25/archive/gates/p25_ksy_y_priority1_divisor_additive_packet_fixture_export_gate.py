#!/usr/bin/env python3
"""Fixture audit for priority-1 divisor/additive packet JSON files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from p25_ksy_y_priority1_divisor_additive_intake_gate import (
    Priority1DivisorAdditivePacket,
    Priority1DivisorAdditiveRow,
    classify_packet,
    packet_from_mapping,
)


REPO = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO / "research" / "p25" / "priority1_divisor_additive_packet_fixtures"

EXPECTED_DECISIONS = (
    ("h0_divisor_close.json", "source_theorem_closed_policy_or_framing_missing"),
    ("h0_missing_boundary.json", "conditional_divisor_identity_missing_h90_boundary"),
    ("conductor39_divisor_close.json", "source_theorem_closed_policy_or_framing_missing"),
    ("twisted_divisor_close.json", "source_theorem_closed_policy_or_framing_missing"),
    ("twisted_missing_period.json", "conditional_value_theorem_missing_period156_context"),
    ("curved_corner_divisor_close.json", "source_theorem_closed_policy_or_framing_missing"),
    ("curved_missing_period.json", "conditional_missing_period156_context"),
    ("projection_reject.json", "reject_loses_mixed_tensor"),
)


@dataclass(frozen=True)
class Priority1PacketFixtureRow:
    filename: str
    raw_sha256: str
    canonical_sha256: str
    packet: Priority1DivisorAdditivePacket
    decision: Priority1DivisorAdditiveRow
    expected_decision: str
    field_count: int
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    ok: bool


@dataclass(frozen=True)
class Priority1PacketFixtureExportProfile:
    fixture_dir_present: bool
    expected_fixture_count: int
    fixture_count: int
    rows: tuple[Priority1PacketFixtureRow, ...]
    exact_field_rows: int
    decision_match_rows: int
    priority1_rows: int
    source_stage_closing_rows: int
    current_source_theorem_rows: int
    avoids_value_branch_rows: int
    period156_bridge_context_rows: int
    rejected_rows: int
    conditional_rows: int
    row_ok: bool


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: top-level JSON must be an object")
    return data, text


def fixture_row(filename: str, expected_decision: str) -> Priority1PacketFixtureRow:
    path = FIXTURE_DIR / filename
    data, raw_text = read_json(path)
    expected_fields = set(Priority1DivisorAdditivePacket.__dataclass_fields__)
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
        and decision.actual_decision == expected_decision
        and decision.ok
    )
    return Priority1PacketFixtureRow(
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


def profile_priority1_packet_fixture_export() -> Priority1PacketFixtureExportProfile:
    rows = tuple(fixture_row(filename, decision) for filename, decision in EXPECTED_DECISIONS)
    exact_fields = sum(not row.missing_fields and not row.unknown_fields for row in rows)
    decision_matches = sum(row.decision.actual_decision == row.expected_decision for row in rows)
    priority1 = sum(row.decision.priority_rank == 1 for row in rows)
    source_closing = sum(row.decision.source_stage_closes for row in rows)
    current_source = sum(row.decision.current_source_theorem_exists for row in rows)
    avoids_value = sum(row.decision.avoids_finite_value_branch for row in rows)
    period_context = sum(row.decision.needs_period156_bridge_context for row in rows)
    rejected = sum(row.decision.rejected for row in rows)
    conditional = sum(row.decision.conditional for row in rows)
    fixture_count = sum((FIXTURE_DIR / filename).exists() for filename, _decision in EXPECTED_DECISIONS)
    row_ok = (
        FIXTURE_DIR.exists()
        and fixture_count == 8
        and len(rows) == 8
        and exact_fields == 8
        and decision_matches == 8
        and priority1 == 8
        and source_closing == 4
        and current_source == 0
        and avoids_value == 8
        and period_context == 4
        and rejected == 1
        and conditional == 3
        and all(row.ok for row in rows)
    )
    return Priority1PacketFixtureExportProfile(
        fixture_dir_present=FIXTURE_DIR.exists(),
        expected_fixture_count=len(EXPECTED_DECISIONS),
        fixture_count=fixture_count,
        rows=rows,
        exact_field_rows=exact_fields,
        decision_match_rows=decision_matches,
        priority1_rows=priority1,
        source_stage_closing_rows=source_closing,
        current_source_theorem_rows=current_source,
        avoids_value_branch_rows=avoids_value,
        period156_bridge_context_rows=period_context,
        rejected_rows=rejected,
        conditional_rows=conditional,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_priority1_packet_fixture_export()
    print("p25 KSY-y priority-1 divisor/additive packet fixture export gate")
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
            f"{row.filename}: decision={decision.actual_decision} "
            f"expected={row.expected_decision} fields={row.field_count} "
            f"lane={decision.lane} rank={decision.priority_rank} "
            f"closes={int(decision.source_stage_closes)} "
            f"current_source={int(decision.current_source_theorem_exists)} "
            f"conditional={int(decision.conditional)} "
            f"rejected={int(decision.rejected)}"
        )
        print(f"    raw_sha256={row.raw_sha256}")
        print(f"    canonical_sha256={row.canonical_sha256}")
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"  exact_field_rows={profile.exact_field_rows}")
    print(f"  decision_match_rows={profile.decision_match_rows}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  source_stage_closing_rows={profile.source_stage_closing_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  avoids_value_branch_rows={profile.avoids_value_branch_rows}")
    print(f"  period156_bridge_context_rows={profile.period156_bridge_context_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  priority1_packet_fixtures_are_stable_theorem_snippet_intake_examples=1")
    print("  fixtures_cover_H0_conductor39_twisted_curved_and_projection_boundaries=1")
    print("  fixture_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_priority1_divisor_additive_packet_fixture_export_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("priority-1 divisor/additive packet fixture export regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

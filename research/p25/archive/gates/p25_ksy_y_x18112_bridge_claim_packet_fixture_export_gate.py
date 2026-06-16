#!/usr/bin/env python3
"""Fixture audit for X_1(8112) bridge-claim packet JSON files."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremClaim,
    X18112BridgeTheoremDecision,
    classify_claim,
)


REPO = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO / "research" / "p25" / "x18112_bridge_claim_packet_fixtures"

EXPECTED_DECISIONS = (
    ("odd_theorem_only_control.json", "upstream_odd_value_no_cross_level_bridge"),
    ("unglued_components_reject.json", "reject_unvalidated_fiber_product_gluing"),
    ("same_curve_bridge.json", "cross_level_target_identified_specialization_missing"),
    ("order8112_generator_bridge.json", "cross_level_target_identified_specialization_missing"),
    ("curved_corner_bridge.json", "cross_level_target_identified_specialization_missing"),
    ("bridge_surface_no_halving.json", "x16_surface_reached_halving_or_vpp_missing"),
    ("x0_payload_vpp_missing.json", "extraction_ready_vpp_missing"),
    ("official_vpp_verified_boundary.json", "submission_ready_verified_triple"),
)


@dataclass(frozen=True)
class BridgeClaimPacketFixtureRow:
    filename: str
    raw_sha256: str
    canonical_sha256: str
    claim: X18112BridgeTheoremClaim
    decision: X18112BridgeTheoremDecision
    expected_decision: str
    field_count: int
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    ok: bool


@dataclass(frozen=True)
class BridgeClaimPacketFixtureExportProfile:
    fixture_dir_present: bool
    expected_fixture_count: int
    fixture_count: int
    rows: tuple[BridgeClaimPacketFixtureRow, ...]
    exact_field_rows: int
    decision_match_rows: int
    bridge_target_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    upstream_only_rows: int
    rejected_rows: int
    boundary_rows: int
    current_evidence_rows: int
    row_ok: bool


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: top-level JSON must be an object")
    return data, text


def packet_from_mapping(data: dict[str, Any]) -> X18112BridgeTheoremClaim:
    fields = X18112BridgeTheoremClaim.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {name: False for name in allowed}
    defaults.update({"name": "candidate", "odd_payload_object": "canonical_H0"})
    defaults.update(data)
    return X18112BridgeTheoremClaim(**{name: defaults[name] for name in fields})


def fixture_row(filename: str, expected_decision: str) -> BridgeClaimPacketFixtureRow:
    path = FIXTURE_DIR / filename
    data, raw_text = read_json(path)
    expected_fields = set(X18112BridgeTheoremClaim.__dataclass_fields__)
    actual_fields = set(data)
    missing = tuple(sorted(expected_fields - actual_fields))
    unknown = tuple(sorted(actual_fields - expected_fields))
    claim = packet_from_mapping(data)
    decision = classify_claim(claim)
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n"
    ok = (
        path.exists()
        and not missing
        and not unknown
        and len(data) == len(expected_fields)
        and decision.decision == expected_decision
        and decision.row_ok
    )
    return BridgeClaimPacketFixtureRow(
        filename=filename,
        raw_sha256=sha256(raw_text.encode()).hexdigest(),
        canonical_sha256=sha256(canonical.encode()).hexdigest(),
        claim=claim,
        decision=decision,
        expected_decision=expected_decision,
        field_count=len(data),
        missing_fields=missing,
        unknown_fields=unknown,
        ok=ok,
    )


def profile_bridge_claim_packet_fixture_export() -> BridgeClaimPacketFixtureExportProfile:
    rows = tuple(fixture_row(filename, decision) for filename, decision in EXPECTED_DECISIONS)
    exact_fields = sum(not row.missing_fields and not row.unknown_fields for row in rows)
    decision_matches = sum(row.decision.decision == row.expected_decision for row in rows)
    bridge_target = sum(row.decision.cross_level_bridge_identified for row in rows)
    x16_surface = sum(row.decision.x16_surface_reached for row in rows)
    extraction = sum(row.decision.extraction_ready for row in rows)
    submission = sum(row.decision.submission_ready for row in rows)
    upstream_only = sum(
        row.decision.decision == "upstream_odd_value_no_cross_level_bridge"
        for row in rows
    )
    rejected = sum(row.decision.decision.startswith("reject_") for row in rows)
    boundary = sum(row.decision.decision == "submission_ready_verified_triple" for row in rows)
    current = 0
    fixture_count = sum((FIXTURE_DIR / filename).exists() for filename, _decision in EXPECTED_DECISIONS)
    row_ok = (
        FIXTURE_DIR.exists()
        and fixture_count == 8
        and len(rows) == 8
        and exact_fields == 8
        and decision_matches == 8
        and bridge_target == 6
        and x16_surface == 3
        and extraction == 2
        and submission == 1
        and upstream_only == 1
        and rejected == 1
        and boundary == 1
        and current == 0
        and all(row.ok for row in rows)
    )
    return BridgeClaimPacketFixtureExportProfile(
        fixture_dir_present=FIXTURE_DIR.exists(),
        expected_fixture_count=len(EXPECTED_DECISIONS),
        fixture_count=fixture_count,
        rows=rows,
        exact_field_rows=exact_fields,
        decision_match_rows=decision_matches,
        bridge_target_rows=bridge_target,
        x16_surface_rows=x16_surface,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        upstream_only_rows=upstream_only,
        rejected_rows=rejected,
        boundary_rows=boundary,
        current_evidence_rows=current,
        row_ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json", type=Path)
    args = parser.parse_args()

    if args.packet_json:
        data, _raw_text = read_json(args.packet_json)
        claim = packet_from_mapping(data)
        decision = classify_claim(claim)
        print("p25 KSY-y X1(8112) bridge-claim packet candidate")
        print(f"packet={args.packet_json}")
        print(f"name={claim.name}")
        print(f"decision={decision.decision}")
        print(f"odd_target_identified={int(decision.odd_target_identified)}")
        print(f"cross_level_bridge_identified={int(decision.cross_level_bridge_identified)}")
        print(f"x16_surface_reached={int(decision.x16_surface_reached)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"missing={decision.first_missing_clause}")
        print(f"next={decision.next_action}")
        print(
            "ksy_y_x18112_bridge_claim_packet_candidate_rows="
            f"{int(decision.row_ok)}/1"
        )
        if not decision.row_ok:
            raise SystemExit("X1(8112) bridge-claim packet candidate failed")
        return 0

    profile = profile_bridge_claim_packet_fixture_export()
    print("p25 KSY-y X1(8112) bridge-claim packet fixture export gate")
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
            f"expected={row.expected_decision} fields={row.field_count} "
            f"bridge={int(decision.cross_level_bridge_identified)} "
            f"x16={int(decision.x16_surface_reached)} "
            f"extract={int(decision.extraction_ready)} "
            f"submission={int(decision.submission_ready)}"
        )
        print(f"    raw_sha256={row.raw_sha256}")
        print(f"    canonical_sha256={row.canonical_sha256}")
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"  exact_field_rows={profile.exact_field_rows}")
    print(f"  decision_match_rows={profile.decision_match_rows}")
    print(f"  bridge_target_rows={profile.bridge_target_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  upstream_only_rows={profile.upstream_only_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  boundary_rows={profile.boundary_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print("interpretation")
    print("  bridge_claim_fixtures_are_stable_x18112_intake_examples=1")
    print("  fixtures_cover_upstream_kill_bridge_surface_extraction_and_vpp_boundaries=1")
    print("  official_vpp_fixture_is_boundary_not_current_evidence=1")
    print(f"ksy_y_x18112_bridge_claim_packet_fixture_export_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(8112) bridge-claim fixture export regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

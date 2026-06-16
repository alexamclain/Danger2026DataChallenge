#!/usr/bin/env python3
"""Exact-P post-bridge X_1(16) surface intake.

This gate starts after the exact-P X_1(8112) bridge packet stage.  Each sample
packet names the exact-P bridge fixture it came from, then routes through the
generic post-bridge X_1(16) surface classifier.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from p25_ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_gate import (
    FIXTURE_DIR as EXACTP_BRIDGE_FIXTURE_DIR,
    packet_from_mapping as bridge_packet_from_mapping,
)
from p25_ksy_y_post_bridge_x16_surface_intake_gate import (
    PostBridgeX16SurfaceDecision,
    PostBridgeX16SurfacePacket,
    classify_packet as classify_surface_packet,
    profile_post_bridge_x16_surface_intake,
)
from p25_ksy_y_x1_8112_bridge_theorem_intake_gate import (
    X18112BridgeTheoremDecision,
    classify_claim as classify_bridge_claim,
)


REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research" / "p25"
SAMPLE_DIR = RESEARCH / "exactp_post_bridge_x16_surface_packet_samples"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_20260614.md",
        "ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_post_bridge_x16_surface_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
        "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_chain_contract_20260614.md",
        "ksy_y_x1_16_halving_chain_contract_rows=1/1",
    ),
)

EXPECTED_DECISIONS = (
    ("exactP_bridge_only_control.json", "abstract_p16_not_practical_chart"),
    ("exactP_y_only.json", "y_chart_missing_model_root"),
    ("exactP_direct_A_xP16_surface.json", "active_surface_reached_halving_missing"),
    ("exactP_y_model_root_surface.json", "active_surface_reached_halving_missing"),
    ("exactP_optional_dgate_surface.json", "optional_depth5_surface_reached_halving_missing"),
    ("exactP_x0_payload_vpp_missing.json", "x0_extracted_official_vpp_missing"),
    ("official_vpp_verified_boundary.json", "submission_ready"),
)


@dataclass(frozen=True)
class ExactPPostBridgeX16SurfacePacket:
    name: str
    bridge_fixture_filename: str
    current_evidence: bool
    same_j_bridge_accepted: bool
    same_curve_p16: bool
    y_parameter: bool
    model_root_x: bool
    A_and_xP16: bool
    optional_first_half_dgate: bool
    active_first_branch_chain: bool
    any_valid_halving_chain: bool
    direct_x0: bool
    internal_verify: bool
    official_vpp: bool


@dataclass(frozen=True)
class ExactPPostBridgeX16SurfaceRow:
    filename: str
    raw_sha256: str
    packet: ExactPPostBridgeX16SurfacePacket
    bridge_decision: X18112BridgeTheoremDecision
    surface_decision: PostBridgeX16SurfaceDecision
    expected_decision: str
    field_count: int
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    exact_p_bridge_fixture: bool
    boundary_row: bool
    ok: bool


@dataclass(frozen=True)
class ExactPPostBridgeX16SurfaceIntake:
    dependency_markers_present: int
    dependency_markers_total: int
    generic_surface_intake_ok: bool
    sample_dir_present: bool
    expected_sample_count: int
    sample_count: int
    rows: tuple[ExactPPostBridgeX16SurfaceRow, ...]
    exact_field_rows: int
    decision_match_rows: int
    exact_p_bridge_fixture_rows: int
    bridge_established_rows: int
    active_surface_rows: int
    optional_dgate_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    boundary_rows: int
    current_evidence_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: top-level JSON must be an object")
    return data, text


def packet_from_mapping(data: dict[str, Any]) -> ExactPPostBridgeX16SurfacePacket:
    fields = ExactPPostBridgeX16SurfacePacket.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown exact-P surface packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {name: False for name in allowed}
    defaults.update(
        {
            "name": "candidate",
            "bridge_fixture_filename": "exactP_same_curve_bridge.json",
        }
    )
    defaults.update(data)
    return ExactPPostBridgeX16SurfacePacket(**{name: defaults[name] for name in fields})


def surface_packet_from_exact(packet: ExactPPostBridgeX16SurfacePacket) -> PostBridgeX16SurfacePacket:
    return PostBridgeX16SurfacePacket(
        name=packet.name,
        current_evidence=packet.current_evidence,
        same_j_bridge_accepted=packet.same_j_bridge_accepted,
        same_curve_p16=packet.same_curve_p16,
        y_parameter=packet.y_parameter,
        model_root_x=packet.model_root_x,
        A_and_xP16=packet.A_and_xP16,
        optional_first_half_dgate=packet.optional_first_half_dgate,
        active_first_branch_chain=packet.active_first_branch_chain,
        any_valid_halving_chain=packet.any_valid_halving_chain,
        direct_x0=packet.direct_x0,
        internal_verify=packet.internal_verify,
        official_vpp=packet.official_vpp,
    )


def bridge_decision_for(filename: str) -> X18112BridgeTheoremDecision:
    data, _raw = read_json(EXACTP_BRIDGE_FIXTURE_DIR / filename)
    return classify_bridge_claim(bridge_packet_from_mapping(data))


def sample_row(filename: str, expected_decision: str) -> ExactPPostBridgeX16SurfaceRow:
    path = SAMPLE_DIR / filename
    data, raw_text = read_json(path)
    expected_fields = set(ExactPPostBridgeX16SurfacePacket.__dataclass_fields__)
    actual_fields = set(data)
    missing = tuple(sorted(expected_fields - actual_fields))
    unknown = tuple(sorted(actual_fields - expected_fields))
    packet = packet_from_mapping(data)
    bridge_decision = bridge_decision_for(packet.bridge_fixture_filename)
    surface_decision = classify_surface_packet(surface_packet_from_exact(packet))
    exact_p_bridge = bridge_decision.claim.odd_payload_object == "exact_P"
    boundary = surface_decision.submission_ready
    ok = (
        path.exists()
        and not missing
        and not unknown
        and len(data) == len(expected_fields)
        and surface_decision.decision == expected_decision
        and surface_decision.ok
        and bridge_decision.row_ok
        and (exact_p_bridge or boundary)
        and (bridge_decision.cross_level_bridge_identified or boundary)
    )
    return ExactPPostBridgeX16SurfaceRow(
        filename=filename,
        raw_sha256=sha256(raw_text.encode()).hexdigest(),
        packet=packet,
        bridge_decision=bridge_decision,
        surface_decision=surface_decision,
        expected_decision=expected_decision,
        field_count=len(data),
        missing_fields=missing,
        unknown_fields=unknown,
        exact_p_bridge_fixture=exact_p_bridge,
        boundary_row=boundary,
        ok=ok,
    )


def profile_exactp_post_bridge_x16_surface_intake() -> ExactPPostBridgeX16SurfaceIntake:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    generic = profile_post_bridge_x16_surface_intake()
    rows = tuple(sample_row(filename, decision) for filename, decision in EXPECTED_DECISIONS)
    exact_fields = sum(not row.missing_fields and not row.unknown_fields for row in rows)
    decision_matches = sum(row.surface_decision.decision == row.expected_decision for row in rows)
    exact_p_bridge = sum(row.exact_p_bridge_fixture for row in rows)
    bridge = sum(row.surface_decision.bridge_established for row in rows)
    active = sum(row.surface_decision.active_x16_surface_reached for row in rows)
    optional = sum(row.surface_decision.optional_dgate_surface_reached for row in rows)
    extraction = sum(row.surface_decision.extraction_ready for row in rows)
    submission = sum(row.surface_decision.submission_ready for row in rows)
    boundary = sum(row.boundary_row for row in rows)
    current = sum(row.packet.current_evidence for row in rows)
    sample_count = sum((SAMPLE_DIR / filename).exists() for filename, _decision in EXPECTED_DECISIONS)
    decisions = tuple(row.surface_decision.decision for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and generic.row_ok
        and SAMPLE_DIR.exists()
        and sample_count == 7
        and len(rows) == 7
        and exact_fields == 7
        and decision_matches == 7
        and exact_p_bridge == 6
        and bridge == 7
        and active == 5
        and optional == 1
        and extraction == 2
        and submission == 1
        and boundary == 1
        and current == 0
        and decisions == tuple(decision for _filename, decision in EXPECTED_DECISIONS)
        and all(row.ok for row in rows)
    )
    return ExactPPostBridgeX16SurfaceIntake(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        generic_surface_intake_ok=generic.row_ok,
        sample_dir_present=SAMPLE_DIR.exists(),
        expected_sample_count=len(EXPECTED_DECISIONS),
        sample_count=sample_count,
        rows=rows,
        exact_field_rows=exact_fields,
        decision_match_rows=decision_matches,
        exact_p_bridge_fixture_rows=exact_p_bridge,
        bridge_established_rows=bridge,
        active_surface_rows=active,
        optional_dgate_rows=optional,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        boundary_rows=boundary,
        current_evidence_rows=current,
        row_ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json", type=Path)
    args = parser.parse_args()

    if args.packet_json:
        data, _raw = read_json(args.packet_json)
        packet = packet_from_mapping(data)
        bridge_decision = bridge_decision_for(packet.bridge_fixture_filename)
        surface_decision = classify_surface_packet(surface_packet_from_exact(packet))
        print("p25 KSY-y exact-P post-bridge X1(16) surface packet candidate")
        print(f"packet={args.packet_json}")
        print(f"name={packet.name}")
        print(f"bridge_fixture={packet.bridge_fixture_filename}")
        print(f"bridge_odd_payload={bridge_decision.claim.odd_payload_object}")
        print(f"bridge_decision={bridge_decision.decision}")
        print(f"surface_decision={surface_decision.decision}")
        print(f"bridge_established={int(surface_decision.bridge_established)}")
        print(f"active_x16_surface_reached={int(surface_decision.active_x16_surface_reached)}")
        print(f"optional_dgate_surface_reached={int(surface_decision.optional_dgate_surface_reached)}")
        print(f"extraction_ready={int(surface_decision.extraction_ready)}")
        print(f"submission_ready={int(surface_decision.submission_ready)}")
        print(f"missing={surface_decision.first_missing_or_falsifier}")
        print(f"next={surface_decision.next_action}")
        ok = (
            bridge_decision.row_ok
            and surface_decision.ok
            and (
                bridge_decision.claim.odd_payload_object == "exact_P"
                or surface_decision.submission_ready
            )
        )
        print(f"ksy_y_exactp_post_bridge_x16_surface_packet_candidate_rows={int(ok)}/1")
        if not ok:
            raise SystemExit("exact-P post-bridge X1(16) surface packet candidate failed")
        return 0

    profile = profile_exactp_post_bridge_x16_surface_intake()
    print("p25 KSY-y exact-P post-bridge X1(16) surface intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  generic_surface_intake_ok={int(profile.generic_surface_intake_ok)}")
    print("samples")
    print(f"  sample_dir={SAMPLE_DIR}")
    print(f"  sample_dir_present={int(profile.sample_dir_present)}")
    print(f"  expected_sample_count={profile.expected_sample_count}")
    print(f"  sample_count={profile.sample_count}")
    print("surface_rows")
    for row in profile.rows:
        surface = row.surface_decision
        bridge = row.bridge_decision
        print(
            "  "
            f"{row.filename}: bridge_odd={bridge.claim.odd_payload_object} "
            f"bridge_decision={bridge.decision} "
            f"surface_decision={surface.decision} expected={row.expected_decision} "
            f"fields={row.field_count} exactP={int(row.exact_p_bridge_fixture)} "
            f"bridge={int(surface.bridge_established)} "
            f"active={int(surface.active_x16_surface_reached)} "
            f"dgate={int(surface.optional_dgate_surface_reached)} "
            f"extract={int(surface.extraction_ready)} "
            f"submission={int(surface.submission_ready)}"
        )
        print(f"    raw_sha256={row.raw_sha256}")
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"  exact_field_rows={profile.exact_field_rows}")
    print(f"  decision_match_rows={profile.decision_match_rows}")
    print(f"  exact_p_bridge_fixture_rows={profile.exact_p_bridge_fixture_rows}")
    print(f"  bridge_established_rows={profile.bridge_established_rows}")
    print(f"  active_surface_rows={profile.active_surface_rows}")
    print(f"  optional_dgate_rows={profile.optional_dgate_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  boundary_rows={profile.boundary_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print("interpretation")
    print("  exactP_post_bridge_samples_route_to_active_x16_surface_intake=1")
    print("  exactP_bridge_only_is_not_surface_reached=1")
    print("  exactP_surface_still_needs_halving_or_direct_x0=1")
    print("  official_vpp_sample_is_boundary_not_current_evidence=1")
    print(f"ksy_y_exactp_post_bridge_x16_surface_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("exact-P post-bridge X1(16) surface intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

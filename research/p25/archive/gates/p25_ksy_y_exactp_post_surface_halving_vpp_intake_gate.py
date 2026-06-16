#!/usr/bin/env python3
"""Exact-P post-surface halving/vpp intake.

This gate starts after an exact-P post-bridge X_1(16) surface sample reaches
the active surface or a direct x0 boundary.  It then routes concrete halving
payloads through the numeric halving/vpp classifier.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from p25_ksy_y_exactp_post_bridge_x16_surface_intake_gate import (
    SAMPLE_DIR as EXACTP_SURFACE_SAMPLE_DIR,
    packet_from_mapping as exactp_surface_packet_from_mapping,
    surface_packet_from_exact,
)
from p25_ksy_y_post_bridge_x16_surface_intake_gate import (
    classify_packet as classify_surface_packet,
)
from p25_ksy_y_post_surface_halving_vpp_intake_gate import (
    PostSurfaceHalvingDecision,
    PostSurfaceHalvingPacket,
    classify_packet as classify_halving_packet,
    profile_post_surface_halving_vpp_intake,
)


REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research" / "p25"
SAMPLE_DIR = RESEARCH / "exactp_post_surface_halving_vpp_packet_samples"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_exactp_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_exactp_post_bridge_x16_surface_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_surface_halving_vpp_intake_20260614.md",
        "ksy_y_post_surface_halving_vpp_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    ),
)

EXPECTED_DECISIONS = (
    ("exactP_surface_only.json", "surface_reached_certificate_missing"),
    ("exactP_one_link_verified_prefix.json", "partial_x_chain_verified_not_extraction"),
    ("exactP_chain_without_xP16.json", "conditional_chain_without_xP16_start"),
    ("exactP_chain_start_mismatch.json", "reject_chain_start_mismatch"),
    ("exactP_chain_link_mismatch.json", "reject_chain_link_mismatch"),
    ("exactP_chain_x0_tail_mismatch.json", "reject_x0_tail_mismatch"),
    ("exactP_direct_A_x0_no_vpp.json", "direct_x0_vpp_missing"),
    ("exactP_direct_A_x0_vpp_fails.json", "reject_vpp_failed"),
    ("exactP_missing_A.json", "reject_missing_A"),
)


@dataclass(frozen=True)
class ExactPPostSurfaceHalvingPacket:
    name: str
    surface_sample_filename: str
    current_evidence: bool
    A: int | None
    xP16: int | None
    chain: tuple[int, ...]
    x0: int | None
    start_depth: int
    final_depth: int
    run_vpp: bool


@dataclass(frozen=True)
class ExactPPostSurfaceHalvingRow:
    filename: str
    raw_sha256: str
    packet: ExactPPostSurfaceHalvingPacket
    source_surface_decision: str
    halving_decision: PostSurfaceHalvingDecision
    expected_decision: str
    field_count: int
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    source_surface_ready: bool
    source_extraction_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExactPPostSurfaceHalvingVppIntake:
    dependency_markers_present: int
    dependency_markers_total: int
    generic_halving_intake_ok: bool
    sample_dir_present: bool
    expected_sample_count: int
    sample_count: int
    rows: tuple[ExactPPostSurfaceHalvingRow, ...]
    exact_field_rows: int
    decision_match_rows: int
    source_surface_ready_rows: int
    source_extraction_ready_rows: int
    surface_missing_rows: int
    partial_chain_rows: int
    full_chain_rows: int
    direct_x0_rows: int
    extraction_ready_rows: int
    vpp_executed_rows: int
    submission_ready_rows: int
    rejected_rows: int
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


def packet_from_mapping(data: dict[str, Any]) -> ExactPPostSurfaceHalvingPacket:
    fields = ExactPPostSurfaceHalvingPacket.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown exact-P halving packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {
        "name": "candidate",
        "surface_sample_filename": "exactP_direct_A_xP16_surface.json",
        "current_evidence": False,
        "A": None,
        "xP16": None,
        "chain": (),
        "x0": None,
        "start_depth": 4,
        "final_depth": 42,
        "run_vpp": False,
    }
    defaults.update(data)
    chain = defaults["chain"]
    if chain is None:
        chain = ()
    defaults["chain"] = tuple(int(value) for value in chain)
    return ExactPPostSurfaceHalvingPacket(**{name: defaults[name] for name in fields})


def halving_packet_from_exact(packet: ExactPPostSurfaceHalvingPacket) -> PostSurfaceHalvingPacket:
    return PostSurfaceHalvingPacket(
        name=packet.name,
        current_evidence=packet.current_evidence,
        A=packet.A,
        xP16=packet.xP16,
        chain=packet.chain,
        x0=packet.x0,
        start_depth=packet.start_depth,
        final_depth=packet.final_depth,
        run_vpp=packet.run_vpp,
    )


def source_surface_decision_for(filename: str):
    data, _raw = read_json(EXACTP_SURFACE_SAMPLE_DIR / filename)
    packet = exactp_surface_packet_from_mapping(data)
    return classify_surface_packet(surface_packet_from_exact(packet))


def sample_row(filename: str, expected_decision: str) -> ExactPPostSurfaceHalvingRow:
    path = SAMPLE_DIR / filename
    data, raw_text = read_json(path)
    expected_fields = set(ExactPPostSurfaceHalvingPacket.__dataclass_fields__)
    actual_fields = set(data)
    missing = tuple(sorted(expected_fields - actual_fields))
    unknown = tuple(sorted(actual_fields - expected_fields))
    packet = packet_from_mapping(data)
    source_surface = source_surface_decision_for(packet.surface_sample_filename)
    halving = classify_halving_packet(halving_packet_from_exact(packet))
    source_ready = source_surface.active_x16_surface_reached
    source_extraction_ready = source_surface.extraction_ready
    ok = (
        path.exists()
        and not missing
        and not unknown
        and len(data) == len(expected_fields)
        and source_surface.ok
        and source_ready
        and halving.decision == expected_decision
        and halving.ok
        and not packet.current_evidence
    )
    return ExactPPostSurfaceHalvingRow(
        filename=filename,
        raw_sha256=sha256(raw_text.encode()).hexdigest(),
        packet=packet,
        source_surface_decision=source_surface.decision,
        halving_decision=halving,
        expected_decision=expected_decision,
        field_count=len(data),
        missing_fields=missing,
        unknown_fields=unknown,
        source_surface_ready=source_ready,
        source_extraction_ready=source_extraction_ready,
        ok=ok,
    )


def profile_exactp_post_surface_halving_vpp_intake() -> ExactPPostSurfaceHalvingVppIntake:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    generic = profile_post_surface_halving_vpp_intake()
    rows = tuple(sample_row(filename, decision) for filename, decision in EXPECTED_DECISIONS)
    exact_fields = sum(not row.missing_fields and not row.unknown_fields for row in rows)
    decision_matches = sum(row.halving_decision.decision == row.expected_decision for row in rows)
    source_ready = sum(row.source_surface_ready for row in rows)
    source_extraction = sum(row.source_extraction_ready for row in rows)
    surface_missing = sum(row.halving_decision.decision == "surface_reached_certificate_missing" for row in rows)
    partial = sum(row.halving_decision.decision == "partial_x_chain_verified_not_extraction" for row in rows)
    full = sum(row.halving_decision.decision == "checkable_x_chain_vpp_missing" for row in rows)
    direct = sum(row.halving_decision.decision == "direct_x0_vpp_missing" for row in rows)
    extraction = sum(row.halving_decision.extraction_ready for row in rows)
    vpp_executed = sum(row.halving_decision.halving_decision.audit.vpp_executed for row in rows)
    submission = sum(row.halving_decision.submission_ready for row in rows)
    rejected = sum(row.halving_decision.decision.startswith("reject_") for row in rows)
    boundary = sum(row.halving_decision.boundary_only for row in rows)
    current = sum(row.packet.current_evidence for row in rows)
    sample_count = sum((SAMPLE_DIR / filename).exists() for filename, _decision in EXPECTED_DECISIONS)
    decisions = tuple(row.halving_decision.decision for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and generic.row_ok
        and SAMPLE_DIR.exists()
        and sample_count == 9
        and len(rows) == 9
        and exact_fields == 9
        and decision_matches == 9
        and source_ready == 9
        and source_extraction == 2
        and surface_missing == 1
        and partial == 1
        and full == 0
        and direct == 1
        and extraction == 1
        and vpp_executed == 1
        and submission == 0
        and rejected == 5
        and boundary == 0
        and current == 0
        and decisions == tuple(decision for _filename, decision in EXPECTED_DECISIONS)
        and all(row.ok for row in rows)
    )
    return ExactPPostSurfaceHalvingVppIntake(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        generic_halving_intake_ok=generic.row_ok,
        sample_dir_present=SAMPLE_DIR.exists(),
        expected_sample_count=len(EXPECTED_DECISIONS),
        sample_count=sample_count,
        rows=rows,
        exact_field_rows=exact_fields,
        decision_match_rows=decision_matches,
        source_surface_ready_rows=source_ready,
        source_extraction_ready_rows=source_extraction,
        surface_missing_rows=surface_missing,
        partial_chain_rows=partial,
        full_chain_rows=full,
        direct_x0_rows=direct,
        extraction_ready_rows=extraction,
        vpp_executed_rows=vpp_executed,
        submission_ready_rows=submission,
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
        data, _raw = read_json(args.packet_json)
        packet = packet_from_mapping(data)
        source_surface = source_surface_decision_for(packet.surface_sample_filename)
        row = classify_halving_packet(halving_packet_from_exact(packet))
        audit = row.halving_decision.audit
        print("p25 KSY-y exact-P post-surface halving/vpp packet candidate")
        print(f"packet={args.packet_json}")
        print(f"name={packet.name}")
        print(f"surface_sample={packet.surface_sample_filename}")
        print(f"source_surface_decision={source_surface.decision}")
        print(f"halving_decision={row.decision}")
        print(f"chain_len={audit.chain_len}/{audit.expected_chain_len}")
        print(f"links={audit.links_ok}/{audit.links_checked}")
        print(f"partial_chain_verified={int(row.partial_chain_verified)}")
        print(f"extraction_ready={int(row.extraction_ready)}")
        print(f"submission_ready={int(row.submission_ready)}")
        print(f"missing={row.first_missing_or_falsifier}")
        print(f"next={row.next_action}")
        ok = source_surface.ok and source_surface.active_x16_surface_reached and row.ok
        print(f"ksy_y_exactp_post_surface_halving_vpp_packet_candidate_rows={int(ok)}/1")
        if not ok:
            raise SystemExit("exact-P post-surface halving/vpp packet candidate failed")
        return 0

    profile = profile_exactp_post_surface_halving_vpp_intake()
    print("p25 KSY-y exact-P post-surface halving/vpp intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  generic_halving_intake_ok={int(profile.generic_halving_intake_ok)}")
    print("samples")
    print(f"  sample_dir={SAMPLE_DIR}")
    print(f"  sample_dir_present={int(profile.sample_dir_present)}")
    print(f"  expected_sample_count={profile.expected_sample_count}")
    print(f"  sample_count={profile.sample_count}")
    print("halving_rows")
    for row in profile.rows:
        halving = row.halving_decision
        audit = halving.halving_decision.audit
        print(
            "  "
            f"{row.filename}: source_surface={row.source_surface_decision} "
            f"halving={halving.decision} expected={row.expected_decision} "
            f"fields={row.field_count} source_ready={int(row.source_surface_ready)} "
            f"source_extract={int(row.source_extraction_ready)} "
            f"links={audit.links_ok}/{audit.links_checked} "
            f"partial={int(halving.partial_chain_verified)} "
            f"extract={int(halving.extraction_ready)} "
            f"submission={int(halving.submission_ready)}"
        )
        print(f"    raw_sha256={row.raw_sha256}")
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"  exact_field_rows={profile.exact_field_rows}")
    print(f"  decision_match_rows={profile.decision_match_rows}")
    print(f"  source_surface_ready_rows={profile.source_surface_ready_rows}")
    print(f"  source_extraction_ready_rows={profile.source_extraction_ready_rows}")
    print(f"  surface_missing_rows={profile.surface_missing_rows}")
    print(f"  partial_chain_rows={profile.partial_chain_rows}")
    print(f"  full_chain_rows={profile.full_chain_rows}")
    print(f"  direct_x0_rows={profile.direct_x0_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  vpp_executed_rows={profile.vpp_executed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  boundary_rows={profile.boundary_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print("interpretation")
    print("  exactP_surface_payload_still_needs_full_chain_or_direct_x0=1")
    print("  exactP_one_link_prefix_is_checked_but_not_extraction_ready=1")
    print("  exactP_direct_A_x0_routes_to_official_vpp=1")
    print("  exactP_failed_vpp_rejects_payload=1")
    print(f"ksy_y_exactp_post_surface_halving_vpp_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("exact-P post-surface halving/vpp intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

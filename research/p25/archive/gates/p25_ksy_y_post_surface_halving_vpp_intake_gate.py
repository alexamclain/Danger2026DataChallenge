#!/usr/bin/env python3
"""Post-surface halving/vpp intake for p25 X_1(16) payloads."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_h0_x16_chart_payload_intake_gate import (
    SAMPLE_A,
    SAMPLE_X32,
    SAMPLE_XP16,
)
from p25_ksy_y_h0_x16_halving_chain_payload_intake_gate import (
    FINAL_DEPTH,
    START_DEPTH,
    HalvingChainDecision,
    HalvingChainPayloadClaim,
    classify_claim,
    profile_halving_chain_payload_intake,
)
from p25_ksy_y_post_bridge_x16_surface_intake_gate import (
    profile_post_bridge_x16_surface_intake,
)
from p25_ksy_y_x1_16_halving_certificate_payload_gate import (
    HALVING_LINKS,
    X_CHAIN_POINTS,
    profile_halving_certificate_payload_contract,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_post_bridge_x16_surface_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_x16_halving_chain_payload_intake_20260614.md",
        "ksy_y_h0_x16_halving_chain_payload_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    ),
)


@dataclass(frozen=True)
class PostSurfaceHalvingPacket:
    name: str
    current_evidence: bool
    A: int | None
    xP16: int | None
    chain: tuple[int, ...]
    x0: int | None
    start_depth: int
    final_depth: int
    run_vpp: bool


@dataclass(frozen=True)
class PostSurfaceHalvingDecision:
    packet: PostSurfaceHalvingPacket
    halving_decision: HalvingChainDecision
    decision: str
    current_evidence: bool
    partial_chain_verified: bool
    extraction_ready: bool
    submission_ready: bool
    boundary_only: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class PostSurfaceHalvingVppIntake:
    dependency_markers_present: int
    dependency_markers_total: int
    post_bridge_surface_ok: bool
    h0_numeric_intake_ok: bool
    certificate_contract_ok: bool
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    rows: tuple[PostSurfaceHalvingDecision, ...]
    row_count: int
    current_evidence_rows: int
    surface_missing_rows: int
    partial_chain_rows: int
    full_chain_rows: int
    direct_x0_rows: int
    extraction_ready_rows: int
    vpp_executed_rows: int
    submission_ready_rows: int
    rejected_rows: int
    boundary_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_from_mapping(data: dict[str, Any]) -> PostSurfaceHalvingPacket:
    allowed = set(PostSurfaceHalvingPacket.__dataclass_fields__)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {
        "name": "candidate",
        "current_evidence": False,
        "A": None,
        "xP16": None,
        "chain": (),
        "x0": None,
        "start_depth": START_DEPTH,
        "final_depth": FINAL_DEPTH,
        "run_vpp": False,
    }
    defaults.update(data)
    chain = defaults["chain"]
    if chain is None:
        chain = ()
    defaults["chain"] = tuple(int(value) for value in chain)
    return PostSurfaceHalvingPacket(**defaults)


def claim_from_packet(packet: PostSurfaceHalvingPacket) -> HalvingChainPayloadClaim:
    return HalvingChainPayloadClaim(
        name=packet.name,
        A=packet.A,
        xP16=packet.xP16,
        chain=packet.chain,
        x0=packet.x0,
        start_depth=packet.start_depth,
        final_depth=packet.final_depth,
        run_vpp=packet.run_vpp,
    )


def classify_packet(packet: PostSurfaceHalvingPacket) -> PostSurfaceHalvingDecision:
    halving = classify_claim(claim_from_packet(packet))
    boundary_only = halving.decision == "submission_ready" and not packet.current_evidence
    return PostSurfaceHalvingDecision(
        packet=packet,
        halving_decision=halving,
        decision=halving.decision,
        current_evidence=packet.current_evidence,
        partial_chain_verified=halving.partial_chain_verified,
        extraction_ready=halving.extraction_ready,
        submission_ready=halving.submission_ready,
        boundary_only=boundary_only,
        first_missing_or_falsifier=halving.first_missing_or_falsifier,
        next_action=halving.next_action,
        ok=halving.ok and not packet.current_evidence,
    )


def packet(
    name: str,
    *,
    A: int | None = SAMPLE_A,
    xP16: int | None = SAMPLE_XP16,
    chain: tuple[int, ...] = (),
    x0: int | None = None,
    run_vpp: bool = False,
) -> PostSurfaceHalvingPacket:
    return PostSurfaceHalvingPacket(
        name=name,
        current_evidence=False,
        A=A,
        xP16=xP16,
        chain=chain,
        x0=x0,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        run_vpp=run_vpp,
    )


def regression_packets() -> tuple[PostSurfaceHalvingPacket, ...]:
    return (
        packet("surface_only"),
        packet("one_link_verified_prefix", chain=(SAMPLE_XP16, SAMPLE_X32)),
        packet("chain_without_xP16", xP16=None, chain=(SAMPLE_XP16, SAMPLE_X32)),
        packet("chain_start_mismatch", chain=(SAMPLE_X32, SAMPLE_XP16)),
        packet("chain_link_mismatch", chain=(SAMPLE_XP16, SAMPLE_X32 + 1)),
        packet("chain_x0_tail_mismatch", chain=(SAMPLE_XP16, SAMPLE_X32), x0=42),
        packet("direct_A_x0_no_vpp", xP16=None, x0=42),
        packet("direct_A_x0_vpp_fails", xP16=None, x0=42, run_vpp=True),
        packet("missing_A", A=None, chain=(SAMPLE_XP16, SAMPLE_X32)),
    )


def profile_post_surface_halving_vpp_intake() -> PostSurfaceHalvingVppIntake:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    post_bridge = profile_post_bridge_x16_surface_intake()
    h0_numeric = profile_halving_chain_payload_intake()
    certificate = profile_halving_certificate_payload_contract()
    rows = tuple(classify_packet(row) for row in regression_packets())
    decisions = tuple(row.decision for row in rows)
    expected = (
        "surface_reached_certificate_missing",
        "partial_x_chain_verified_not_extraction",
        "conditional_chain_without_xP16_start",
        "reject_chain_start_mismatch",
        "reject_chain_link_mismatch",
        "reject_x0_tail_mismatch",
        "direct_x0_vpp_missing",
        "reject_vpp_failed",
        "reject_missing_A",
    )
    current = sum(row.current_evidence for row in rows)
    surface_missing = sum(row.decision == "surface_reached_certificate_missing" for row in rows)
    partial = sum(row.decision == "partial_x_chain_verified_not_extraction" for row in rows)
    full = sum(row.decision == "checkable_x_chain_vpp_missing" for row in rows)
    direct = sum(row.decision == "direct_x0_vpp_missing" for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    vpp_executed = sum(row.halving_decision.audit.vpp_executed for row in rows)
    submission = sum(row.submission_ready for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    boundary = sum(row.boundary_only for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and post_bridge.row_ok
        and h0_numeric.row_ok
        and certificate.row_ok
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and HALVING_LINKS == 38
        and X_CHAIN_POINTS == 39
        and len(rows) == 9
        and current == 0
        and surface_missing == 1
        and partial == 1
        and full == 0
        and direct == 1
        and extraction == 1
        and vpp_executed == 1
        and submission == 0
        and rejected == 5
        and boundary == 0
        and decisions == expected
        and rows[1].halving_decision.audit.links_checked == 1
        and rows[1].halving_decision.audit.links_ok == 1
        and all(row.ok for row in rows)
    )
    return PostSurfaceHalvingVppIntake(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        post_bridge_surface_ok=post_bridge.row_ok,
        h0_numeric_intake_ok=h0_numeric.row_ok,
        certificate_contract_ok=certificate.row_ok,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        x_chain_points=X_CHAIN_POINTS,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        surface_missing_rows=surface_missing,
        partial_chain_rows=partial,
        full_chain_rows=full,
        direct_x0_rows=direct,
        extraction_ready_rows=extraction,
        vpp_executed_rows=vpp_executed,
        submission_ready_rows=submission,
        rejected_rows=rejected,
        boundary_rows=boundary,
        row_ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json", type=Path)
    args = parser.parse_args()

    if args.packet_json:
        data = json.loads(args.packet_json.read_text())
        if not isinstance(data, dict):
            raise SystemExit("packet JSON must be an object")
        row = classify_packet(packet_from_mapping(data))
        audit = row.halving_decision.audit
        print("p25 KSY-y post-surface halving/vpp packet candidate")
        print(f"packet={args.packet_json}")
        print(f"name={row.packet.name}")
        print(f"decision={row.decision}")
        print(f"chain_len={audit.chain_len}/{audit.expected_chain_len}")
        print(f"links={audit.links_ok}/{audit.links_checked}")
        print(f"partial_chain_verified={int(row.partial_chain_verified)}")
        print(f"extraction_ready={int(row.extraction_ready)}")
        print(f"submission_ready={int(row.submission_ready)}")
        print(f"missing={row.first_missing_or_falsifier}")
        print(f"next={row.next_action}")
        print(f"ksy_y_post_surface_halving_vpp_packet_candidate_rows={int(row.ok)}/1")
        if not row.ok:
            raise SystemExit("post-surface halving/vpp packet candidate failed")
        return 0

    profile = profile_post_surface_halving_vpp_intake()
    print("p25 KSY-y post-surface halving/vpp intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  post_bridge_surface_ok={int(profile.post_bridge_surface_ok)}")
    print(f"  h0_numeric_intake_ok={int(profile.h0_numeric_intake_ok)}")
    print(f"  certificate_contract_ok={int(profile.certificate_contract_ok)}")
    print("shape")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print("halving_rows")
    for row in profile.rows:
        audit = row.halving_decision.audit
        print(
            "  "
            f"{row.packet.name}: decision={row.decision} "
            f"len={audit.chain_len}/{audit.expected_chain_len} "
            f"links={audit.links_ok}/{audit.links_checked} "
            f"partial={int(row.partial_chain_verified)} "
            f"extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  surface_missing_rows={profile.surface_missing_rows}")
    print(f"  partial_chain_rows={profile.partial_chain_rows}")
    print(f"  full_chain_rows={profile.full_chain_rows}")
    print(f"  direct_x0_rows={profile.direct_x0_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  vpp_executed_rows={profile.vpp_executed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  boundary_rows={profile.boundary_rows}")
    print("interpretation")
    print("  one_link_prefix_is_checked_but_not_extraction_ready=1")
    print("  direct_A_x0_routes_to_official_vpp=1")
    print("  failed_vpp_rejects_payload=1")
    print("  full_x_chain_or_direct_x0_still_requires_official_vpp=1")
    print(f"ksy_y_post_surface_halving_vpp_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-surface halving/vpp intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

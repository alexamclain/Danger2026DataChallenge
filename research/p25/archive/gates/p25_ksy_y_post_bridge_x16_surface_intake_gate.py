#!/usr/bin/env python3
"""Post-bridge X_1(16) surface intake for the p25 KSY-y moonshot."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_x1_16_halving_chain_contract_gate import (
    profile_x1_16_halving_chain_contract,
)
from p25_ksy_y_x1_16_montgomery_chart_contract_gate import (
    ACTIVE_PRODUCTION_MODE,
    DGATE_START_DEPTH,
    OPTIONAL_DGATE_MODE,
    X16_START_DEPTH,
    profile_x1_16_montgomery_chart_contract,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_x18112_bridge_claim_packet_fixture_export_20260614.md",
        "ksy_y_x18112_bridge_claim_packet_fixture_export_rows=1/1",
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


@dataclass(frozen=True)
class PostBridgeX16SurfacePacket:
    name: str
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
class PostBridgeX16SurfaceDecision:
    packet: PostBridgeX16SurfacePacket
    decision: str
    bridge_established: bool
    active_x16_surface_reached: bool
    optional_dgate_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class PostBridgeX16SurfaceIntake:
    dependency_markers_present: int
    dependency_markers_total: int
    chart_contract_ok: bool
    halving_contract_ok: bool
    active_mode: str
    active_start_depth: int
    optional_dgate_mode: str
    optional_dgate_start_depth: int
    rows: tuple[PostBridgeX16SurfaceDecision, ...]
    row_count: int
    current_evidence_rows: int
    bridge_established_rows: int
    active_surface_rows: int
    optional_dgate_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    rejected_rows: int
    conditional_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_from_mapping(data: dict[str, Any]) -> PostBridgeX16SurfacePacket:
    fields = PostBridgeX16SurfacePacket.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {name: False for name in allowed}
    defaults.update({"name": "candidate"})
    defaults.update(data)
    return PostBridgeX16SurfacePacket(**{name: defaults[name] for name in fields})


def classify_packet(packet: PostBridgeX16SurfacePacket) -> PostBridgeX16SurfaceDecision:
    if packet.official_vpp:
        if packet.direct_x0:
            return PostBridgeX16SurfaceDecision(
                packet=packet,
                decision="submission_ready",
                bridge_established=True,
                active_x16_surface_reached=True,
                optional_dgate_surface_reached=packet.optional_first_half_dgate,
                extraction_ready=True,
                submission_ready=True,
                first_missing_or_falsifier="none",
                next_action="archive official vpp.py output, command, environment, and certificate",
                ok=True,
            )
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="reject_vpp_without_direct_x0",
            bridge_established=False,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="concrete x0 accompanying official vpp.py",
            next_action="recover the verified A,x0 payload or discard the vpp claim",
            ok=True,
        )

    if not packet.same_j_bridge_accepted:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="conditional_same_j_bridge_missing",
            bridge_established=False,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="accepted same-j X_1(8112) bridge",
            next_action="return to the post-policy X_1(8112) work order",
            ok=True,
        )

    if not packet.same_curve_p16:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="conditional_same_curve_p16_missing",
            bridge_established=False,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="same-curve 16-torsion component P16",
            next_action="project the X_1(8112) bridge to P16 or supply same-curve P16",
            ok=True,
        )

    if not packet.y_parameter and not packet.A_and_xP16:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="abstract_p16_not_practical_chart",
            bridge_established=True,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="X_1(16) y-chart parameter or direct A,xP16",
            next_action="specialize the bridge to the production Montgomery chart",
            ok=True,
        )

    if packet.y_parameter and not packet.model_root_x and not packet.A_and_xP16:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="y_chart_missing_model_root",
            bridge_established=True,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="model root x satisfying the X_1(16) quadratic",
            next_action="derive x, then A and xP16",
            ok=True,
        )

    if packet.optional_first_half_dgate and not packet.A_and_xP16:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="reject_dgate_without_active_surface",
            bridge_established=True,
            active_x16_surface_reached=False,
            optional_dgate_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier="active A,xP16 surface underneath the optional d-gate",
            next_action="derive the active surface first; d-gate data is optional",
            ok=True,
        )

    if not packet.direct_x0 and not packet.any_valid_halving_chain:
        optional = packet.optional_first_half_dgate
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision=(
                "optional_depth5_surface_reached_halving_missing"
                if optional
                else "active_surface_reached_halving_missing"
            ),
            bridge_established=True,
            active_x16_surface_reached=True,
            optional_dgate_surface_reached=optional,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier=(
                "halve chain from x32 at depth 5 to x0"
                if optional
                else "halve chain from xP16 at depth 4 to x0"
            ),
            next_action="derive the halving chain or direct x0, then run official vpp.py",
            ok=True,
        )

    if packet.direct_x0 and not packet.internal_verify:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="direct_x0_official_vpp_missing",
            bridge_established=True,
            active_x16_surface_reached=True,
            optional_dgate_surface_reached=packet.optional_first_half_dgate,
            extraction_ready=True,
            submission_ready=False,
            first_missing_or_falsifier="official vpp.py verification",
            next_action="run official vpp.py on the concrete A,x0 payload",
            ok=True,
        )

    if packet.active_first_branch_chain:
        return PostBridgeX16SurfaceDecision(
            packet=packet,
            decision="x0_extracted_official_vpp_missing",
            bridge_established=True,
            active_x16_surface_reached=True,
            optional_dgate_surface_reached=packet.optional_first_half_dgate,
            extraction_ready=True,
            submission_ready=False,
            first_missing_or_falsifier="official vpp.py verification",
            next_action="run official vpp.py and archive output",
            ok=True,
        )

    return PostBridgeX16SurfaceDecision(
        packet=packet,
        decision="x0_extracted_not_active_path_vpp_missing",
        bridge_established=True,
        active_x16_surface_reached=True,
        optional_dgate_surface_reached=packet.optional_first_half_dgate,
        extraction_ready=True,
        submission_ready=False,
        first_missing_or_falsifier="official vpp.py verification; active-path provenance optional",
        next_action="run official vpp.py; retain chain provenance if available",
        ok=True,
    )


def regression_packets() -> tuple[PostBridgeX16SurfacePacket, ...]:
    base = {
        "current_evidence": False,
        "same_j_bridge_accepted": True,
        "same_curve_p16": True,
        "y_parameter": False,
        "model_root_x": False,
        "A_and_xP16": False,
        "optional_first_half_dgate": False,
        "active_first_branch_chain": False,
        "any_valid_halving_chain": False,
        "direct_x0": False,
        "internal_verify": False,
        "official_vpp": False,
    }
    return (
        PostBridgeX16SurfacePacket("no_same_j_bridge", **{**base, "same_j_bridge_accepted": False}),
        PostBridgeX16SurfacePacket("same_j_no_p16", **{**base, "same_curve_p16": False}),
        PostBridgeX16SurfacePacket("abstract_p16", **base),
        PostBridgeX16SurfacePacket("x16_y_only", **{**base, "y_parameter": True}),
        PostBridgeX16SurfacePacket(
            "x16_y_and_model_root",
            **{**base, "y_parameter": True, "model_root_x": True, "A_and_xP16": True},
        ),
        PostBridgeX16SurfacePacket("direct_A_xP16", **{**base, "A_and_xP16": True}),
        PostBridgeX16SurfacePacket(
            "dgate_first_half_surface",
            **{
                **base,
                "y_parameter": True,
                "model_root_x": True,
                "A_and_xP16": True,
                "optional_first_half_dgate": True,
            },
        ),
        PostBridgeX16SurfacePacket(
            "active_first_branch_chain_to_x0",
            **{
                **base,
                "A_and_xP16": True,
                "active_first_branch_chain": True,
                "any_valid_halving_chain": True,
                "direct_x0": True,
                "internal_verify": True,
            },
        ),
        PostBridgeX16SurfacePacket(
            "any_valid_chain_to_x0",
            **{
                **base,
                "A_and_xP16": True,
                "any_valid_halving_chain": True,
                "direct_x0": True,
                "internal_verify": True,
            },
        ),
        PostBridgeX16SurfacePacket(
            "direct_x0_without_chain",
            **{**base, "A_and_xP16": True, "direct_x0": True},
        ),
        PostBridgeX16SurfacePacket(
            "official_vpp_verified_boundary",
            **{**base, "A_and_xP16": True, "direct_x0": True, "official_vpp": True},
        ),
    )


def profile_post_bridge_x16_surface_intake() -> PostBridgeX16SurfaceIntake:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    chart = profile_x1_16_montgomery_chart_contract()
    halving = profile_x1_16_halving_chain_contract()
    rows = tuple(classify_packet(packet) for packet in regression_packets())
    decisions = tuple(row.decision for row in rows)
    expected = (
        "conditional_same_j_bridge_missing",
        "conditional_same_curve_p16_missing",
        "abstract_p16_not_practical_chart",
        "y_chart_missing_model_root",
        "active_surface_reached_halving_missing",
        "active_surface_reached_halving_missing",
        "optional_depth5_surface_reached_halving_missing",
        "x0_extracted_official_vpp_missing",
        "x0_extracted_not_active_path_vpp_missing",
        "direct_x0_official_vpp_missing",
        "submission_ready",
    )
    current = sum(row.packet.current_evidence for row in rows)
    bridge = sum(row.bridge_established for row in rows)
    active = sum(row.active_x16_surface_reached for row in rows)
    optional = sum(row.optional_dgate_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    conditional = sum(row.decision.startswith("conditional_") for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and chart.row_ok
        and halving.row_ok
        and ACTIVE_PRODUCTION_MODE == "x16halvenonsplit"
        and X16_START_DEPTH == 4
        and OPTIONAL_DGATE_MODE == "x16halvenonsplitdgate"
        and DGATE_START_DEPTH == 5
        and len(rows) == 11
        and current == 0
        and bridge == 9
        and active == 7
        and optional == 1
        and extraction == 4
        and submission == 1
        and rejected == 0
        and conditional == 2
        and decisions == expected
        and all(row.ok for row in rows)
    )
    return PostBridgeX16SurfaceIntake(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        chart_contract_ok=chart.row_ok,
        halving_contract_ok=halving.row_ok,
        active_mode=ACTIVE_PRODUCTION_MODE,
        active_start_depth=X16_START_DEPTH,
        optional_dgate_mode=OPTIONAL_DGATE_MODE,
        optional_dgate_start_depth=DGATE_START_DEPTH,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        bridge_established_rows=bridge,
        active_surface_rows=active,
        optional_dgate_rows=optional,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        rejected_rows=rejected,
        conditional_rows=conditional,
        row_ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json", type=Path)
    args = parser.parse_args()

    if args.packet_json:
        text = args.packet_json.read_text()
        data = json.loads(text)
        if not isinstance(data, dict):
            raise SystemExit("packet JSON must be an object")
        decision = classify_packet(packet_from_mapping(data))
        print("p25 KSY-y post-bridge X1(16) surface packet candidate")
        print(f"packet={args.packet_json}")
        print(f"name={decision.packet.name}")
        print(f"decision={decision.decision}")
        print(f"bridge_established={int(decision.bridge_established)}")
        print(f"active_x16_surface_reached={int(decision.active_x16_surface_reached)}")
        print(f"optional_dgate_surface_reached={int(decision.optional_dgate_surface_reached)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"missing={decision.first_missing_or_falsifier}")
        print(f"next={decision.next_action}")
        print(f"ksy_y_post_bridge_x16_surface_packet_candidate_rows={int(decision.ok)}/1")
        if not decision.ok:
            raise SystemExit("post-bridge X1(16) surface packet candidate failed")
        return 0

    profile = profile_post_bridge_x16_surface_intake()
    print("p25 KSY-y post-bridge X1(16) surface intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  chart_contract_ok={int(profile.chart_contract_ok)}")
    print(f"  halving_contract_ok={int(profile.halving_contract_ok)}")
    print("production")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  optional_dgate_mode={profile.optional_dgate_mode}")
    print(f"  optional_dgate_start_depth={profile.optional_dgate_start_depth}")
    print("surface_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.packet.name}: decision={row.decision} "
            f"bridge={int(row.bridge_established)} "
            f"active_surface={int(row.active_x16_surface_reached)} "
            f"dgate={int(row.optional_dgate_surface_reached)} "
            f"extract={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  bridge_established_rows={profile.bridge_established_rows}")
    print(f"  active_surface_rows={profile.active_surface_rows}")
    print(f"  optional_dgate_rows={profile.optional_dgate_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print("interpretation")
    print("  post_bridge_claim_must_reach_active_A_xP16_surface_before_halving=1")
    print("  optional_dgate_is_not_required_for_active_x16halvenonsplit=1")
    print("  direct_or_chain_x0_still_needs_official_vpp=1")
    print(f"ksy_y_post_bridge_x16_surface_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("post-bridge X1(16) surface intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

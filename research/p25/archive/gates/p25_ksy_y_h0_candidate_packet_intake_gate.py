#!/usr/bin/env python3
"""End-to-end H0 candidate-packet intake for the p25 moonshot.

This composes the executable H0 intake layers:

* exact H0 product-file/source-theorem intake;
* same-j/order-8112 bridge-component intake;
* numeric X_1(16) chart-payload intake; and
* numeric halving-chain/direct-x0 intake.

It is meant for a future expert/subagent answer that arrives as one packet.
The packet can be a JSON file, but the default regression rows are in-memory
controls so the gate remains self-contained.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_h0_product_file_claim_intake_gate import (
    FIXTURE_DIR,
    ProductFileClaim,
    ProductFileDecision,
    classify_product_file_claim,
)
from p25_ksy_y_h0_translate_exact_product_query_packet_gate import (
    profile_h0_translate_exact_product_query_packet,
)
from p25_ksy_y_h0_x18112_bridge_component_claim_intake_gate import (
    H0X18112BridgeComponentClaim,
    H0X18112BridgeComponentDecision,
    classify_component_claim,
)
from p25_ksy_y_h0_x16_chart_payload_intake_gate import (
    SAMPLE_A,
    SAMPLE_X,
    SAMPLE_X32,
    SAMPLE_XP16,
    SAMPLE_Y,
    X16ChartPayloadClaim,
    X16ChartPayloadDecision,
    decision_from_audit as classify_chart_payload,
)
from p25_ksy_y_h0_x16_halving_chain_payload_intake_gate import (
    HalvingChainPayloadClaim,
    HalvingChainDecision,
    classify_claim as classify_halving_chain,
    parse_chain_file,
)


@dataclass(frozen=True)
class H0CandidatePacket:
    name: str
    product_file: Path | None
    theorem_body_verified: bool
    arithmetic_source_theorem: bool
    output_kind: str
    period156_context: bool
    h90_boundary: bool
    danger3_framing: bool
    same_curve_p16: bool
    same_curve_q507: bool
    same_j_or_curve: bool
    order8112_generator: bool
    y: int | None
    x: int | None
    A: int | None
    xP16: int | None
    z: int | None
    x32: int | None
    chain: tuple[int, ...]
    x0: int | None
    run_vpp: bool


@dataclass(frozen=True)
class H0CandidatePacketDecision:
    packet: H0CandidatePacket
    product_decision: ProductFileDecision | None
    bridge_decision: H0X18112BridgeComponentDecision | None
    chart_decision: X16ChartPayloadDecision | None
    chain_decision: HalvingChainDecision | None
    decision: str
    source_stage_closed: bool
    danger3_framed: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    partial_chain_verified: bool
    extraction_ready: bool
    vpp_executed: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0CandidatePacketIntakeProfile:
    exact_product_query_ok: bool
    regression_rows: tuple[H0CandidatePacketDecision, ...]
    row_count: int
    rejected_rows: int
    source_stage_closed_rows: int
    danger3_framed_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    partial_chain_rows: int
    extraction_ready_rows: int
    vpp_executed_rows: int
    submission_ready_rows: int
    row_ok: bool


def fixture_path(name: str) -> Path:
    return FIXTURE_DIR / name


def product_claim(packet: H0CandidatePacket) -> ProductFileClaim | None:
    if packet.product_file is None:
        return None
    return ProductFileClaim(
        name=packet.name,
        product_file=packet.product_file,
        theorem_body_verified=packet.theorem_body_verified,
        arithmetic_source_theorem=packet.arithmetic_source_theorem,
        output_kind=packet.output_kind,
        period156_context=packet.period156_context,
        h90_boundary=packet.h90_boundary,
        danger3_framing=packet.danger3_framing,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_x0=False,
        official_vpp=False,
    )


def bridge_claim(packet: H0CandidatePacket) -> H0X18112BridgeComponentClaim:
    return H0X18112BridgeComponentClaim(
        name=packet.name,
        theorem_body_verified=True,
        h0_source_payload=True,
        same_curve_p16=packet.same_curve_p16,
        same_curve_q507=packet.same_curve_q507,
        same_j_or_curve=packet.same_j_or_curve,
        order8112_generator=packet.order8112_generator,
        x16_surface_relation=packet.y is not None or packet.A is not None,
        emits_x16_y=packet.y is not None,
        emits_model_root_or_xp16=packet.x is not None or packet.xP16 is not None or packet.A is not None,
        emits_halving_chain_or_x0=bool(packet.chain) or packet.x0 is not None,
        danger3_framing=packet.danger3_framing,
        concrete_vpp_verified_triple=False,
    )


def chart_claim(packet: H0CandidatePacket) -> X16ChartPayloadClaim:
    return X16ChartPayloadClaim(
        name=packet.name,
        has_h0_order8112_bridge=True,
        y=packet.y,
        x=packet.x,
        A=packet.A,
        xP16=packet.xP16,
        z=packet.z,
        x32=packet.x32,
        x0=packet.x0,
        run_vpp=packet.run_vpp,
    )


def chain_claim(packet: H0CandidatePacket, chart: X16ChartPayloadDecision | None) -> HalvingChainPayloadClaim:
    A = packet.A
    xP16 = packet.xP16
    if chart is not None:
        if A is None and chart.audit.computed_A is not None:
            A = chart.audit.computed_A
        if xP16 is None and chart.audit.computed_xP16 is not None:
            xP16 = chart.audit.computed_xP16
    return HalvingChainPayloadClaim(
        name=packet.name,
        A=A,
        xP16=xP16,
        chain=packet.chain,
        x0=packet.x0,
        start_depth=4,
        final_depth=42,
        run_vpp=packet.run_vpp,
    )


def has_any_chart_payload(packet: H0CandidatePacket) -> bool:
    return any(
        value is not None
        for value in (packet.y, packet.x, packet.A, packet.xP16, packet.z, packet.x32, packet.x0)
    )


def packet_decision(
    packet: H0CandidatePacket,
    target_rows: Any,
) -> H0CandidatePacketDecision:
    product = product_claim(packet)
    if product is None:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=None,
            bridge_decision=None,
            chart_decision=None,
            chain_decision=None,
            decision="reject_missing_h0_product_file",
            source_stage_closed=False,
            danger3_framed=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=False,
            submission_ready=False,
            first_missing_or_falsifier="exact H0 product file",
            next_action="supply one of the stable h0_product_fixtures files",
            ok=True,
        )

    product_row = classify_product_file_claim(product, target_rows)
    product_source_closed = product_row.source_stage_closed
    if not product_source_closed:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=None,
            chart_decision=None,
            chain_decision=None,
            decision=product_row.decision,
            source_stage_closed=False,
            danger3_framed=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=False,
            submission_ready=False,
            first_missing_or_falsifier=product_row.first_missing_or_falsifier,
            next_action=product_row.next_action,
            ok=product_row.ok,
        )

    if not packet.danger3_framing:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=None,
            chart_decision=None,
            chain_decision=None,
            decision="source_theorem_closed_policy_or_framing_missing",
            source_stage_closed=True,
            danger3_framed=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=False,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            next_action="resolve challenge framing before cross-level extraction",
            ok=True,
        )

    bridge_row = classify_component_claim(bridge_claim(packet))
    if not bridge_row.cross_level_bridge_identified:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=bridge_row,
            chart_decision=None,
            chain_decision=None,
            decision=bridge_row.decision,
            source_stage_closed=True,
            danger3_framed=True,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=False,
            submission_ready=False,
            first_missing_or_falsifier=bridge_row.first_missing_or_falsifier,
            next_action=bridge_row.next_action,
            ok=bridge_row.ok,
        )

    if not has_any_chart_payload(packet):
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=bridge_row,
            chart_decision=None,
            chain_decision=None,
            decision="cross_level_target_identified_specialization_missing",
            source_stage_closed=True,
            danger3_framed=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=False,
            submission_ready=False,
            first_missing_or_falsifier="X_1(16) y/x/A/xP16 chart payload or direct A,x0",
            next_action="specialize the same-j bridge to the production X_1(16) chart",
            ok=True,
        )

    chart_row = classify_chart_payload(chart_claim(packet))
    if chart_row.submission_ready:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=bridge_row,
            chart_decision=chart_row,
            chain_decision=None,
            decision=chart_row.decision,
            source_stage_closed=True,
            danger3_framed=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=chart_row.x16_surface_reached,
            partial_chain_verified=False,
            extraction_ready=True,
            vpp_executed=chart_row.audit.vpp_executed,
            submission_ready=True,
            first_missing_or_falsifier=chart_row.first_missing_or_falsifier,
            next_action=chart_row.next_action,
            ok=chart_row.ok,
        )
    if chart_row.decision.startswith("reject_"):
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=bridge_row,
            chart_decision=chart_row,
            chain_decision=None,
            decision=chart_row.decision,
            source_stage_closed=True,
            danger3_framed=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=chart_row.audit.vpp_executed,
            submission_ready=False,
            first_missing_or_falsifier=chart_row.first_missing_or_falsifier,
            next_action=chart_row.next_action,
            ok=chart_row.ok,
        )

    if not chart_row.x16_surface_reached and not chart_row.extraction_ready:
        return H0CandidatePacketDecision(
            packet=packet,
            product_decision=product_row,
            bridge_decision=bridge_row,
            chart_decision=chart_row,
            chain_decision=None,
            decision=chart_row.decision,
            source_stage_closed=True,
            danger3_framed=True,
            cross_level_bridge_identified=True,
            x16_surface_reached=False,
            partial_chain_verified=False,
            extraction_ready=False,
            vpp_executed=chart_row.audit.vpp_executed,
            submission_ready=False,
            first_missing_or_falsifier=chart_row.first_missing_or_falsifier,
            next_action=chart_row.next_action,
            ok=chart_row.ok,
        )

    chain_row = classify_halving_chain(chain_claim(packet, chart_row))
    return H0CandidatePacketDecision(
        packet=packet,
        product_decision=product_row,
        bridge_decision=bridge_row,
        chart_decision=chart_row,
        chain_decision=chain_row,
        decision=chain_row.decision,
        source_stage_closed=True,
        danger3_framed=True,
        cross_level_bridge_identified=True,
        x16_surface_reached=chart_row.x16_surface_reached,
        partial_chain_verified=chain_row.partial_chain_verified,
        extraction_ready=chain_row.extraction_ready,
        vpp_executed=chain_row.audit.vpp_executed,
        submission_ready=chain_row.submission_ready,
        first_missing_or_falsifier=chain_row.first_missing_or_falsifier,
        next_action=chain_row.next_action,
        ok=chain_row.ok,
    )


def base_packet(name: str, **overrides: object) -> H0CandidatePacket:
    values = {
        "product_file": fixture_path("h0_m2_translate_lifted_product.txt"),
        "theorem_body_verified": True,
        "arithmetic_source_theorem": True,
        "output_kind": "value",
        "period156_context": True,
        "h90_boundary": True,
        "danger3_framing": True,
        "same_curve_p16": False,
        "same_curve_q507": False,
        "same_j_or_curve": False,
        "order8112_generator": False,
        "y": None,
        "x": None,
        "A": None,
        "xP16": None,
        "z": None,
        "x32": None,
        "chain": (),
        "x0": None,
        "run_vpp": False,
    }
    values.update(overrides)
    return H0CandidatePacket(name=name, **values)


def regression_packets() -> tuple[H0CandidatePacket, ...]:
    bridge = {"order8112_generator": True, "same_j_or_curve": True}
    chart = {"y": SAMPLE_Y, "x": SAMPLE_X}
    return (
        base_packet("missing_product_file", product_file=None),
        base_packet(
            "source_certification_only",
            product_file=fixture_path("h0_m1_canonical_lifted_product.txt"),
            output_kind="source-certification",
            danger3_framing=False,
        ),
        base_packet("source_value_no_danger3", danger3_framing=False),
        base_packet("danger3_no_bridge"),
        base_packet("unglued_p16_q507", same_curve_p16=True, same_curve_q507=True),
        base_packet("bridge_no_chart", **bridge),
        base_packet("chart_no_chain", **bridge, **chart),
        base_packet(
            "one_link_chain_prefix",
            **bridge,
            **chart,
            chain=(SAMPLE_XP16, SAMPLE_X32),
        ),
        base_packet("direct_A_x0_no_vpp", **bridge, A=SAMPLE_A, x0=42),
        base_packet("direct_A_x0_vpp_fails", **bridge, A=SAMPLE_A, x0=42, run_vpp=True),
    )


def profile_h0_candidate_packet_intake() -> H0CandidatePacketIntakeProfile:
    query = profile_h0_translate_exact_product_query_packet()
    rows = tuple(packet_decision(packet, query.exact_product_rows) for packet in regression_packets())
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    danger3 = sum(row.danger3_framed for row in rows)
    bridge = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    partial = sum(row.partial_chain_verified for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    vpp_executed = sum(row.vpp_executed for row in rows)
    submission = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "reject_missing_h0_product_file",
        "source_certified_value_or_divisor_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "upstream_odd_value_no_cross_level_bridge",
        "reject_unglued_components",
        "cross_level_target_identified_specialization_missing",
        "surface_reached_certificate_missing",
        "partial_x_chain_verified_not_extraction",
        "direct_x0_vpp_missing",
        "reject_vpp_failed",
    )
    row_ok = (
        query.row_ok
        and len(rows) == 10
        and rejected == 3
        and source_closed == 8
        and danger3 == 7
        and bridge == 5
        and x16 == 2
        and partial == 1
        and extraction == 1
        and vpp_executed == 1
        and submission == 0
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return H0CandidatePacketIntakeProfile(
        exact_product_query_ok=query.row_ok,
        regression_rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        source_stage_closed_rows=source_closed,
        danger3_framed_rows=danger3,
        cross_level_bridge_rows=bridge,
        x16_surface_rows=x16,
        partial_chain_rows=partial,
        extraction_ready_rows=extraction,
        vpp_executed_rows=vpp_executed,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def packet_from_json(path: Path) -> H0CandidatePacket:
    data = json.loads(path.read_text())
    chain: tuple[int, ...]
    if data.get("chain_file"):
        chain = parse_chain_file(Path(data["chain_file"]), int(data.get("start_depth", 4)))
    else:
        chain = tuple(int(value) for value in data.get("chain", ()))
    product = data.get("product_file")
    return H0CandidatePacket(
        name=str(data.get("name", path.stem)),
        product_file=Path(product) if product else None,
        theorem_body_verified=bool(data.get("theorem_body_verified", False)),
        arithmetic_source_theorem=bool(data.get("arithmetic_source_theorem", False)),
        output_kind=str(data.get("output_kind", "source-certification")),
        period156_context=bool(data.get("period156_context", False)),
        h90_boundary=bool(data.get("h90_boundary", False)),
        danger3_framing=bool(data.get("danger3_framing", False)),
        same_curve_p16=bool(data.get("same_curve_p16", False)),
        same_curve_q507=bool(data.get("same_curve_q507", False)),
        same_j_or_curve=bool(data.get("same_j_or_curve", False)),
        order8112_generator=bool(data.get("order8112_generator", False)),
        y=data.get("y"),
        x=data.get("x"),
        A=data.get("A"),
        xP16=data.get("xP16"),
        z=data.get("z"),
        x32=data.get("x32"),
        chain=chain,
        x0=data.get("x0"),
        run_vpp=bool(data.get("run_vpp", False)),
    )


def print_decision(row: H0CandidatePacketDecision) -> None:
    print(
        "  "
        f"{row.packet.name}: decision={row.decision} "
        f"source={int(row.source_stage_closed)} danger3={int(row.danger3_framed)} "
        f"bridge={int(row.cross_level_bridge_identified)} "
        f"x16={int(row.x16_surface_reached)} "
        f"partial_chain={int(row.partial_chain_verified)} "
        f"extract={int(row.extraction_ready)} "
        f"vpp_run={int(row.vpp_executed)} submission={int(row.submission_ready)} "
        f"missing={row.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json")
    args = parser.parse_args()

    query = profile_h0_translate_exact_product_query_packet()
    if args.packet_json:
        row = packet_decision(packet_from_json(Path(args.packet_json)), query.exact_product_rows)
        print("p25 KSY-y H0 candidate-packet intake candidate")
        print_decision(row)
        print(f"next_action={row.next_action}")
        print(f"ksy_y_h0_candidate_packet_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_h0_candidate_packet_intake()
    print("p25 KSY-y H0 candidate-packet intake gate")
    print("dependencies")
    print(f"  exact_product_query_ok={int(profile.exact_product_query_ok)}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  danger3_framed_rows={profile.danger3_framed_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  partial_chain_rows={profile.partial_chain_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  vpp_executed_rows={profile.vpp_executed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  packet_must_pass_source_bridge_chart_chain_in_order=1")
    print("  verified_chain_prefix_is_not_extraction_ready=1")
    print("  extraction_ready_payload_still_needs_official_vpp=1")
    print(f"ksy_y_h0_candidate_packet_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 candidate-packet intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

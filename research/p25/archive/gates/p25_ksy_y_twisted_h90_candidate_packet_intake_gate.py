#!/usr/bin/env python3
"""Unified candidate-packet intake for the twisted/H90 moonshot route.

The minimal closing ask says what source theorem would matter.  This gate is
the practical intake boundary for future theorem snippets, expert answers, or
subagent packets: it routes one candidate through the twisted/H90 source
classifier and then, only after source closure, through DANGER3 framing and
cross-level extraction.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from p25_ksy_y_conductor39_twisted_descent_candidate_router_gate import (
    TwistedDescentCandidate,
    classify_candidate as classify_twisted_candidate,
)
from p25_ksy_y_danger3_finite_identity_framing_router_gate import (
    FiniteIdentityFramingCandidate,
    classify_candidate as classify_framing_candidate,
)


REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research" / "p25"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_twisted_h90_minimal_closing_ask_packet_20260614.md",
        "ksy_y_twisted_h90_minimal_closing_ask_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_danger3_finite_identity_framing_router_20260614.md",
        "ksy_y_danger3_finite_identity_framing_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_cross_level_bridge_source_route_packet_20260614.md",
        "ksy_y_cross_level_bridge_source_route_packet_rows=1/1",
    ),
)


@dataclass(frozen=True)
class TwistedH90CandidatePacket:
    name: str
    theorem_body_verified: bool
    uses_degree6_orbit: bool
    uses_pure_norm: bool
    uses_pair_sum: bool
    uses_signed_shadow: bool
    uses_quotient_or_ratio: bool
    uses_hilbert90_boundary: bool
    finite_value_or_divisor_theorem: bool
    period156_context: bool
    arithmetic_source_theorem: bool
    finite_field_identity_for_p: bool
    generic_cm_or_class_field_generation: bool
    explicit_non_cm_finite_field_framing: bool
    danger3_policy_accepts_identity: bool
    same_j_x18112_bridge: bool
    x16_surface_or_A_xP16: bool
    concrete_A_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class TwistedH90CandidatePacketDecision:
    packet: TwistedH90CandidatePacket
    decision: str
    source_decision: str
    framing_decision: str
    rejected: bool
    helper_only: bool
    conditional: bool
    source_shape_missing: bool
    policy_or_framing_missing: bool
    source_stage_closed: bool
    danger3_unblocked: bool
    cross_level_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class TwistedH90CandidatePacketIntakeProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    rows: tuple[TwistedH90CandidatePacketDecision, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_shape_missing_rows: int
    policy_or_framing_missing_rows: int
    source_stage_closed_rows: int
    danger3_unblocked_rows: int
    cross_level_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_from_mapping(data: dict[str, Any]) -> TwistedH90CandidatePacket:
    fields = TwistedH90CandidatePacket.__dataclass_fields__
    allowed = set(fields)
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown packet fields: {', '.join(unknown)}")
    defaults: dict[str, Any] = {name: False for name in allowed}
    defaults["name"] = "candidate"
    defaults.update(data)
    return TwistedH90CandidatePacket(**{name: defaults[name] for name in fields})


def source_candidate(packet: TwistedH90CandidatePacket) -> TwistedDescentCandidate:
    return TwistedDescentCandidate(
        name=packet.name,
        theorem_body_verified=packet.theorem_body_verified,
        uses_degree6_orbit=packet.uses_degree6_orbit,
        uses_pure_norm=packet.uses_pure_norm,
        uses_pair_sum=packet.uses_pair_sum,
        uses_signed_shadow=packet.uses_signed_shadow,
        uses_quotient_or_ratio=packet.uses_quotient_or_ratio,
        uses_hilbert90_boundary=packet.uses_hilbert90_boundary,
        finite_value_or_divisor_theorem=packet.finite_value_or_divisor_theorem,
        period156_context=packet.period156_context,
        arithmetic_source_theorem=packet.arithmetic_source_theorem,
        danger3_framing=False,
        extraction_to_A_x0=False,
        official_vpp=False,
    )


def framing_candidate(packet: TwistedH90CandidatePacket) -> FiniteIdentityFramingCandidate:
    return FiniteIdentityFramingCandidate(
        name=packet.name,
        has_source_theorem=packet.arithmetic_source_theorem,
        finite_field_identity_for_p=packet.finite_field_identity_for_p,
        generic_cm_or_class_field_generation=packet.generic_cm_or_class_field_generation,
        explicit_non_cm_finite_field_framing=packet.explicit_non_cm_finite_field_framing,
        danger3_policy_accepts_identity=packet.danger3_policy_accepts_identity,
        same_j_x18112_bridge=packet.same_j_x18112_bridge,
        x16_surface_or_A_xP16=packet.x16_surface_or_A_xP16,
        concrete_A_x0=packet.concrete_A_x0,
        official_vpp=packet.official_vpp,
    )


def classify_packet(packet: TwistedH90CandidatePacket) -> TwistedH90CandidatePacketDecision:
    source = classify_twisted_candidate(source_candidate(packet))

    if packet.official_vpp and packet.concrete_A_x0:
        framing = classify_framing_candidate(framing_candidate(packet))
        return decision_from_framing(packet, source.decision, framing)

    if not source.source_stage_closed:
        return TwistedH90CandidatePacketDecision(
            packet=packet,
            decision=source.decision,
            source_decision=source.decision,
            framing_decision="not_reached",
            rejected=source.decision.startswith("reject_"),
            helper_only=source.helper_only,
            conditional=source.decision.startswith("conditional_"),
            source_shape_missing=False,
            policy_or_framing_missing=False,
            source_stage_closed=False,
            danger3_unblocked=False,
            cross_level_bridge_identified=False,
            x16_surface_reached=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_or_falsifier=source.first_missing_or_falsifier,
            next_action=source.next_action,
            ok=source.ok,
        )

    framing = classify_framing_candidate(framing_candidate(packet))
    return decision_from_framing(packet, source.decision, framing)


def decision_from_framing(
    packet: TwistedH90CandidatePacket,
    source_decision: str,
    framing: Any,
) -> TwistedH90CandidatePacketDecision:
    decision = framing.decision
    return TwistedH90CandidatePacketDecision(
        packet=packet,
        decision=decision,
        source_decision=source_decision,
        framing_decision=decision,
        rejected=decision.startswith("reject_"),
        helper_only=False,
        conditional=decision.startswith("conditional_"),
        source_shape_missing=decision == "source_theorem_value_shape_missing_finite_identity",
        policy_or_framing_missing=decision == "source_theorem_closed_policy_or_framing_missing",
        source_stage_closed=framing.source_stage_closed,
        danger3_unblocked=framing.danger3_unblocked,
        cross_level_bridge_identified=framing.cross_level_bridge_identified,
        x16_surface_reached=framing.x16_surface_reached,
        extraction_ready=framing.extraction_ready,
        submission_ready=framing.submission_ready,
        first_missing_or_falsifier=framing.first_missing_or_falsifier,
        next_action=framing.next_action,
        ok=framing.ok,
    )


def base_packet(name: str) -> dict[str, Any]:
    return {
        "name": name,
        "theorem_body_verified": True,
        "uses_degree6_orbit": True,
        "uses_pure_norm": False,
        "uses_pair_sum": False,
        "uses_signed_shadow": False,
        "uses_quotient_or_ratio": True,
        "uses_hilbert90_boundary": True,
        "finite_value_or_divisor_theorem": True,
        "period156_context": True,
        "arithmetic_source_theorem": True,
        "finite_field_identity_for_p": True,
        "generic_cm_or_class_field_generation": False,
        "explicit_non_cm_finite_field_framing": False,
        "danger3_policy_accepts_identity": False,
        "same_j_x18112_bridge": False,
        "x16_surface_or_A_xP16": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }


def regression_packets() -> tuple[TwistedH90CandidatePacket, ...]:
    return (
        packet_from_mapping({**base_packet("no_theorem_body"), "theorem_body_verified": False}),
        packet_from_mapping({**base_packet("pure_degree6_norm"), "uses_pure_norm": True, "uses_quotient_or_ratio": False, "uses_hilbert90_boundary": False}),
        packet_from_mapping({**base_packet("h90_boundary_only"), "finite_value_or_divisor_theorem": False, "arithmetic_source_theorem": False, "finite_field_identity_for_p": False}),
        packet_from_mapping({**base_packet("twisted_value_no_period156"), "period156_context": False, "arithmetic_source_theorem": False, "finite_field_identity_for_p": False}),
        packet_from_mapping({**base_packet("twisted_period156_payload_no_source"), "arithmetic_source_theorem": False, "finite_field_identity_for_p": False}),
        packet_from_mapping({**base_packet("source_theorem_not_p_finite_identity"), "finite_field_identity_for_p": False}),
        packet_from_mapping({**base_packet("generic_cm_not_framing"), "generic_cm_or_class_field_generation": True}),
        packet_from_mapping(base_packet("source_finite_identity_no_framing")),
        packet_from_mapping({**base_packet("policy_yes_no_bridge"), "danger3_policy_accepts_identity": True}),
        packet_from_mapping({**base_packet("same_j_bridge_no_x16"), "danger3_policy_accepts_identity": True, "same_j_x18112_bridge": True}),
        packet_from_mapping({**base_packet("x16_surface_no_x0"), "danger3_policy_accepts_identity": True, "same_j_x18112_bridge": True, "x16_surface_or_A_xP16": True}),
        packet_from_mapping({**base_packet("concrete_A_x0_no_vpp"), "danger3_policy_accepts_identity": True, "same_j_x18112_bridge": True, "x16_surface_or_A_xP16": True, "concrete_A_x0": True}),
        packet_from_mapping({**base_packet("official_vpp_verified"), "danger3_policy_accepts_identity": True, "same_j_x18112_bridge": True, "x16_surface_or_A_xP16": True, "concrete_A_x0": True, "official_vpp": True}),
    )


def profile_twisted_h90_candidate_packet_intake() -> TwistedH90CandidatePacketIntakeProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = tuple(classify_packet(packet) for packet in regression_packets())
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.rejected for row in rows)
    helper = sum(row.helper_only for row in rows)
    conditional = sum(row.conditional for row in rows)
    source_shape_missing = sum(row.source_shape_missing for row in rows)
    policy_missing = sum(row.policy_or_framing_missing for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    cross_level = sum(row.cross_level_bridge_identified for row in rows)
    x16 = sum(row.x16_surface_reached for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 13
        and rejected == 3
        and helper == 1
        and conditional == 2
        and source_shape_missing == 1
        and policy_missing == 1
        and source_closed == 6
        and danger3 == 5
        and cross_level == 4
        and x16 == 3
        and extraction == 2
        and submission == 1
        and decisions
        == (
            "reject_no_theorem_body",
            "reject_pure_degree6_norm_cancels",
            "helper_only_hilbert90_boundary_value_theorem_missing",
            "conditional_value_theorem_missing_period156_context",
            "conditional_finite_payload_without_source_theorem",
            "source_theorem_value_shape_missing_finite_identity",
            "reject_generic_cm_generation_not_framing",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_cross_level_bridge_missing",
            "cross_level_target_identified_specialization_missing",
            "x16_surface_reached_halving_or_vpp_missing",
            "extraction_ready_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in rows)
    )
    return TwistedH90CandidatePacketIntakeProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_shape_missing_rows=source_shape_missing,
        policy_or_framing_missing_rows=policy_missing,
        source_stage_closed_rows=source_closed,
        danger3_unblocked_rows=danger3,
        cross_level_bridge_rows=cross_level,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def print_decision(row: TwistedH90CandidatePacketDecision) -> None:
    packet = row.packet
    print(
        "  "
        f"{packet.name}: decision={row.decision} "
        f"source={row.source_decision} framing={row.framing_decision} "
        f"degree6={int(packet.uses_degree6_orbit)} "
        f"pure_norm={int(packet.uses_pure_norm)} "
        f"pair_sum={int(packet.uses_pair_sum)} "
        f"ratio={int(packet.uses_quotient_or_ratio)} "
        f"h90={int(packet.uses_hilbert90_boundary)} "
        f"finite={int(packet.finite_value_or_divisor_theorem)} "
        f"period156={int(packet.period156_context)} "
        f"source_theorem={int(packet.arithmetic_source_theorem)} "
        f"finite_p={int(packet.finite_field_identity_for_p)} "
        f"policy={int(packet.danger3_policy_accepts_identity)} "
        f"same_j={int(packet.same_j_x18112_bridge)} "
        f"x16={int(packet.x16_surface_or_A_xP16)} "
        f"x0={int(packet.concrete_A_x0)} "
        f"vpp={int(packet.official_vpp)} "
        f"missing={row.first_missing_or_falsifier}"
    )
    print(f"    next={row.next_action}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet-json")
    args = parser.parse_args()

    if args.packet_json:
        with Path(args.packet_json).open() as f:
            packet = packet_from_mapping(json.load(f))
        decision = classify_packet(packet)
        print("p25 KSY-y twisted/H90 candidate-packet intake")
        print_decision(decision)
        print(f"source_stage_closed={int(decision.source_stage_closed)}")
        print(f"danger3_unblocked={int(decision.danger3_unblocked)}")
        print(f"cross_level_bridge_identified={int(decision.cross_level_bridge_identified)}")
        print(f"x16_surface_reached={int(decision.x16_surface_reached)}")
        print(f"extraction_ready={int(decision.extraction_ready)}")
        print(f"submission_ready={int(decision.submission_ready)}")
        print(f"ksy_y_twisted_h90_candidate_packet_intake_candidate_rows={int(decision.ok)}/1")
        if not decision.ok:
            raise SystemExit("twisted/H90 candidate-packet intake failed")
        return 0

    profile = profile_twisted_h90_candidate_packet_intake()
    print("p25 KSY-y twisted/H90 candidate-packet intake gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("regression_rows")
    for row in profile.rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_shape_missing_rows={profile.source_shape_missing_rows}")
    print(f"  policy_or_framing_missing_rows={profile.policy_or_framing_missing_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  cross_level_bridge_rows={profile.cross_level_bridge_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  packet_intake_routes_source_theorem_to_danger3_and_extraction=1")
    print("  first_missing_stage_is_explicit_for_future_expert_or_subagent_reports=1")
    print("  official_vpp_verified_A_x0_is_the_only_submission_ready_state=1")
    print(f"ksy_y_twisted_h90_candidate_packet_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("twisted/H90 candidate-packet intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

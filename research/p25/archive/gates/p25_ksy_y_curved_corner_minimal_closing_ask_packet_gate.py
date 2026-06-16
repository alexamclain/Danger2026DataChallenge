#!/usr/bin/env python3
"""Minimal closing-ask packet for the curved Hilbert-90 corner route.

The curved-corner producer intake has become a strict finite-shape gate:
unit-triangle row placement is now mandatory before a local answer receives
helper credit.  This packet records the smallest theorem upgrade that would
move that helper route: a finite value/divisor theorem with period-156 context
and a challenge-legal arithmetic source theorem, followed by the usual
DANGER3 framing and extraction boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_atom_terminology_guardrail_gate import (
    profile_atom_terminology_guardrail,
)
from p25_ksy_y_h90_value_theorem_intake_gate import (
    H90ValueTheoremClaim,
    classify_claim as classify_h90_value_claim,
    profile_h90_value_theorem_intake,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate import (
    CornerProducerCandidate,
    classify_candidate as classify_corner_candidate,
    profile_corner_producer_intake,
)


@dataclass(frozen=True)
class CurvedCornerClosingAskRow:
    name: str
    surface: str
    ask: str
    candidate_command: str
    decision: str
    rejected: bool
    helper_only: bool
    conditional: bool
    source_theorem_closes: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    continue_or_kill: str
    ok: bool


@dataclass(frozen=True)
class CurvedCornerMinimalClosingAskPacket:
    atom_guardrail_ok: bool
    corner_intake_ok: bool
    h90_value_intake_ok: bool
    atom_count: int
    atoms_are_search_candidates: bool
    corner_payload_size: int
    h90_positive_factor_count: int
    h90_negative_factor_count: int
    rows: tuple[CurvedCornerClosingAskRow, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_theorem_closing_rows: int
    submission_ready_rows: int
    row_ok: bool


def corner_command(name: str, *, unit_triangle: bool, finite: bool = False, period: bool = False, source: bool = False, danger3: bool = False, x0: bool = False, vpp: bool = False) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py",
        "--candidate",
        f"--name {name}",
        "--theorem-body",
        "--triangle",
        "--curvature",
        "--half-bridge-edge",
        "--full-k-trace",
        "--raw-relation",
        "--raw-kernel-trace",
        "--primitive-c169",
        "--active-c169-lift",
        "--quadratic-fiber",
        "--nonsplit-carry",
    ]
    if unit_triangle:
        parts.append("--unit-triangle")
    if finite:
        parts.append("--finite-or-divisor")
    if period:
        parts.append("--period-156")
    if source:
        parts.append("--arithmetic-source")
    if danger3:
        parts.append("--danger3-framing")
    if x0:
        parts.append("--x0")
    if vpp:
        parts.append("--vpp")
    return " ".join(parts)


def h90_command(name: str, *, target: str = "canonical_H0", output_kind: str = "divisor-additive", finite: bool, period: bool = True, source: bool = False, danger3: bool = False, extraction: bool = False, vpp: bool = False) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--target-object {target}",
        f"--output-kind {output_kind}",
        "--theorem-body",
        "--exact-target",
        "--bridge-spine",
        "--legal-yang-h90",
        "--boundary-context",
    ]
    if finite:
        parts.append("--finite-or-divisor")
    if period:
        parts.append("--period-156")
    if source:
        parts.append("--arithmetic-source")
    if danger3:
        parts.append("--danger3-framing")
    if extraction:
        parts.append("--extraction")
    if vpp:
        parts.append("--vpp-verified")
    return " ".join(parts)


def corner_candidate(name: str, *, unit_triangle: bool, finite: bool = False, period: bool = False, source: bool = False, danger3: bool = False, same_j: bool = False, x16: bool = False, x0: bool = False, vpp: bool = False) -> CornerProducerCandidate:
    return CornerProducerCandidate(
        name=name,
        theorem_body_verified=True,
        exact_curved_row_triangle=True,
        primitive_newton_curvature=True,
        recorded_half_bridge_edge=True,
        full_order25_k_trace=True,
        raw_d3_y_relation=True,
        raw_kernel_trace_accounted=True,
        primitive_c169_motion=True,
        active_c169_lift_selected=True,
        quadratic_fiber_section=True,
        nonsplit_c169_carry_transport=True,
        unit_triangle_law=unit_triangle,
        finite_value_or_divisor_theorem=finite,
        period156_context=period,
        arithmetic_source_theorem=source,
        danger3_framing=danger3,
        same_j_x18112_bridge=same_j,
        x16_surface=x16,
        concrete_A_x0=x0,
        official_vpp=vpp,
    )


def h90_claim(name: str, *, target: str = "canonical_H0", output_kind: str = "divisor-additive", finite: bool, period: bool = True, source: bool = False, danger3: bool = False, extraction: bool = False, vpp: bool = False) -> H90ValueTheoremClaim:
    return H90ValueTheoremClaim(
        name=name,
        theorem_body_verified=True,
        target_object=target,
        output_kind=output_kind,
        exact_target=True,
        bridge_spine_preserved=True,
        legal_yang_or_h90_object=True,
        boundary_or_period_norm_context=True,
        finite_field_identity_or_divisor=finite,
        period_156_context=period,
        arithmetic_source_theorem=source,
        danger3_framing=danger3,
        extraction_to_A_x0=extraction,
        concrete_vpp_verified_triple=vpp,
    )


def row_from_corner(
    name: str,
    *,
    ask: str,
    unit_triangle: bool,
    finite: bool = False,
    period: bool = False,
    source: bool = False,
    danger3: bool = False,
    continue_or_kill: str,
) -> CurvedCornerClosingAskRow:
    decision = classify_corner_candidate(
        corner_candidate(
            name,
            unit_triangle=unit_triangle,
            finite=finite,
            period=period,
            source=source,
            danger3=danger3,
        )
    )
    return CurvedCornerClosingAskRow(
        name=name,
        surface="curved_corner_intake",
        ask=ask,
        candidate_command=corner_command(
            name,
            unit_triangle=unit_triangle,
            finite=finite,
            period=period,
            source=source,
            danger3=danger3,
        ),
        decision=decision.decision,
        rejected=decision.decision.startswith("reject_"),
        helper_only=decision.decision.startswith("helper_only_"),
        conditional=decision.decision.startswith("conditional_"),
        source_theorem_closes=decision.source_stage_closed,
        submission_ready=decision.submission_ready,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        continue_or_kill=continue_or_kill,
        ok=decision.ok,
    )


def row_from_h90(
    name: str,
    *,
    ask: str,
    target: str = "canonical_H0",
    output_kind: str = "divisor-additive",
    finite: bool,
    period: bool = True,
    source: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
    continue_or_kill: str,
) -> CurvedCornerClosingAskRow:
    decision = classify_h90_value_claim(
        h90_claim(
            name,
            target=target,
            output_kind=output_kind,
            finite=finite,
            period=period,
            source=source,
            danger3=danger3,
            extraction=extraction,
            vpp=vpp,
        )
    )
    conditional = decision.decision.startswith(("conditional_", "live_target_identified_"))
    return CurvedCornerClosingAskRow(
        name=name,
        surface="h90_y507_value_intake",
        ask=ask,
        candidate_command=h90_command(
            name,
            target=target,
            output_kind=output_kind,
            finite=finite,
            period=period,
            source=source,
            danger3=danger3,
            extraction=extraction,
            vpp=vpp,
        ),
        decision=decision.decision,
        rejected=decision.decision.startswith("reject_"),
        helper_only=False,
        conditional=conditional,
        source_theorem_closes=decision.theorem_source_closed,
        submission_ready=decision.submission_ready,
        first_missing_or_falsifier=decision.first_missing_clause,
        continue_or_kill=continue_or_kill,
        ok=decision.row_ok,
    )


def closing_rows() -> tuple[CurvedCornerClosingAskRow, ...]:
    return (
        row_from_corner(
            "curved_corner_without_unit_triangle",
            ask="Does a curved-corner local answer without unit-triangle row placement count?",
            unit_triangle=False,
            continue_or_kill="kill or reroute through the current curved-corner intake",
        ),
        row_from_corner(
            "unit_triangle_corner_helper_only",
            ask="Does the full unit-triangle curved corner close the route by itself?",
            unit_triangle=True,
            continue_or_kill="keep as finite helper; ask for value/divisor theorem",
        ),
        row_from_corner(
            "unit_triangle_value_no_period156",
            ask="Does a curved-corner finite value without period-156 context close?",
            unit_triangle=True,
            finite=True,
            continue_or_kill="ask for support-period branch/root/telescoping",
        ),
        row_from_corner(
            "unit_triangle_period156_no_source",
            ask="Does period-156 finite payload without an arithmetic source theorem close?",
            unit_triangle=True,
            finite=True,
            period=True,
            continue_or_kill="keep as verifier payload until a theorem emits it",
        ),
        row_from_corner(
            "unit_triangle_source_no_danger3",
            ask="What is the first stop after a period-156 arithmetic source theorem?",
            unit_triangle=True,
            finite=True,
            period=True,
            source=True,
            continue_or_kill="route to DANGER3 finite-identity/non-CM framing",
        ),
        row_from_h90(
            "h90_live_target_no_value",
            ask="What does the corresponding H0/Y507 route still need at the value layer?",
            finite=False,
            continue_or_kill="ask for exact finite-field value or divisor/additive theorem",
        ),
        row_from_h90(
            "h90_period156_value_source_no_danger3",
            ask="What H0/Y507 answer would close the source stage?",
            output_kind="value",
            finite=True,
            period=True,
            source=True,
            continue_or_kill="route to DANGER3 framing and extraction",
        ),
        row_from_h90(
            "verified_triple_boundary",
            ask="What is the only submission-ready endpoint?",
            target="exact_P",
            output_kind="value",
            finite=True,
            period=True,
            source=True,
            danger3=True,
            extraction=True,
            vpp=True,
            continue_or_kill="archive official vpp.py output and certificate",
        ),
    )


def profile_curved_corner_minimal_closing_ask_packet() -> CurvedCornerMinimalClosingAskPacket:
    atom = profile_atom_terminology_guardrail()
    corner = profile_corner_producer_intake()
    h90 = profile_h90_value_theorem_intake()
    rows = closing_rows()
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.rejected for row in rows)
    helper = sum(row.helper_only for row in rows)
    conditional = sum(row.conditional for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    row_ok = (
        atom.row_ok
        and corner.row_ok
        and h90.row_ok
        and atom.atom_count == 75
        and not atom.atoms_are_search_candidates
        and corner.finite_shape_rows == 9
        and h90.h90_positive_factor_count == 78
        and h90.h90_negative_factor_count == 78
        and len(rows) == 8
        and decisions
        == (
            "reject_passive_or_wrong_unit_triangle",
            "helper_only_curved_triangle_value_theorem_missing",
            "conditional_missing_period156_context",
            "conditional_finite_payload_without_source_theorem",
            "source_theorem_closed_policy_or_framing_missing",
            "live_target_identified_value_or_divisor_theorem_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "submission_ready_verified_triple",
        )
        and rejected == 1
        and helper == 1
        and conditional == 3
        and source_closing == 3
        and submission_ready == 1
        and all(row.ok for row in rows)
    )
    return CurvedCornerMinimalClosingAskPacket(
        atom_guardrail_ok=atom.row_ok,
        corner_intake_ok=corner.row_ok,
        h90_value_intake_ok=h90.row_ok,
        atom_count=atom.atom_count,
        atoms_are_search_candidates=atom.atoms_are_search_candidates,
        corner_payload_size=75,
        h90_positive_factor_count=h90.h90_positive_factor_count,
        h90_negative_factor_count=h90.h90_negative_factor_count,
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_theorem_closing_rows=source_closing,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_curved_corner_minimal_closing_ask_packet()
    print("p25 KSY-y curved-corner minimal closing-ask packet gate")
    print("dependencies")
    print(f"  atom_guardrail_ok={int(profile.atom_guardrail_ok)}")
    print(f"  corner_intake_ok={int(profile.corner_intake_ok)}")
    print(f"  h90_value_intake_ok={int(profile.h90_value_intake_ok)}")
    print("payloads")
    print(f"  atom_count={profile.atom_count}")
    print(f"  atoms_are_search_candidates={int(profile.atoms_are_search_candidates)}")
    print(f"  corner_payload_size={profile.corner_payload_size}")
    print(f"  h90_positive_factor_count={profile.h90_positive_factor_count}")
    print(f"  h90_negative_factor_count={profile.h90_negative_factor_count}")
    print("closing_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: surface={row.surface} decision={row.decision} "
            f"source_closes={int(row.source_theorem_closes)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    ask={row.ask}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
        print(f"    next={row.continue_or_kill}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  unit_triangle_curved_corner_is_helper_not_closure=1")
    print("  smallest_closing_yes_is_period156_value_or_divisor_arithmetic_source=1")
    print("  h90_y507_route_has_same_value_theorem_boundary=1")
    print("  official_vpp_verified_triple_is_only_submission_boundary=1")
    print(
        "ksy_y_curved_corner_minimal_closing_ask_packet_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("curved-corner minimal closing-ask packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

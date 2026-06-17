#!/usr/bin/env python3
"""Reality ledger for p25 finite payload claims.

The v2 cockpit now has strong source-intake and extraction contracts.  This
gate keeps the most common over-crediting failure mode explicit: finite
fixtures and pinned products are useful evidence, but they are not arithmetic
source theorems, and a source theorem is still not a DANGER3 submission.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RealityRow:
    name: str
    evidence_kind: str
    decision: str
    current_evidence_exists: bool
    source_stage_closes_if_theorem_present: bool
    current_source_theorem_exists: bool
    computed_payload_only: bool
    rejected: bool
    conditional: bool
    submission_boundary: bool
    current_submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class RealityLedger:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[RealityRow, ...]
    evidence_markers_ok: int
    current_evidence_rows: int
    source_closing_shape_rows: int
    current_source_theorem_rows: int
    computed_payload_only_rows: int
    rejected_rows: int
    conditional_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_finite_geometry_rigidity",
            "research/p25/evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
            "theta2_inverse_solution = all 75 weights +1",
        ),
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "candidate_packet_intake_reorg",
            "research/p25/evidence/p25_v2_candidate_packet_intake_reorg_20260616.md",
            "p25_v2_candidate_packet_intake_reorg_rows=1/1",
        ),
        marker(
            "constructive_value_payload_contract",
            "research/p25/evidence/p25_v2_constructive_value_payload_contract_20260616.md",
            "p25_v2_constructive_value_payload_contract_rows=1/1",
        ),
        marker(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "danger3_finite_identity_framing",
            "research/p25/evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
            "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
        ),
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "extraction_minimal_hook",
            "research/p25/evidence/p25_v2_extraction_minimal_hook_20260616.md",
            "p25_v2_extraction_minimal_hook_rows=1/1",
        ),
    )


def reality_rows() -> tuple[RealityRow, ...]:
    return (
        RealityRow(
            name="fixed_75_atom_product",
            evidence_kind="exactp_finite_geometry",
            decision="fixed_payload_factors_not_search_candidates",
            current_evidence_exists=True,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="arithmetic theorem selecting the exact equal-weight 75-atom product",
            next_action="do not enumerate atoms; route exact-P leads through the minimal hook",
            ok=True,
        ),
        RealityRow(
            name="stable_h0_conductor39_product_rows",
            evidence_kind="finite_target",
            decision="pinned_finite_target_not_arithmetic_source_theorem",
            current_evidence_exists=True,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=True,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem from an arithmetic source",
            next_action="use row hashes and products as exact verifier targets for future theorem hits",
            ok=True,
        ),
        RealityRow(
            name="local_fixture_or_packet_payload",
            evidence_kind="computed_packet_or_fixture",
            decision="finite_payload_without_source_theorem",
            current_evidence_exists=True,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=True,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem for the payload",
            next_action="treat as regression or intake data, not as a source close",
            ok=True,
        ),
        RealityRow(
            name="h0_conductor39_divisor_additive_theorem_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_first_pass_source_stage_then_need_extraction",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="finite divisor/additive theorem for one legal support-156 row with Norm_156(Y_507) boundary",
            next_action="classify through unified value/divisor interface and post-theorem router",
            ok=True,
        ),
        RealityRow(
            name="period156_value_theorem_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_value_source_stage_then_need_extraction",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="support-period-156 value theorem with branch/root/telescoping context",
            next_action="classify through period-156 value branch and source-hook screens",
            ok=True,
        ),
        RealityRow(
            name="exactp_upstream_theorem_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_heavy_source_stage_then_need_extraction",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="compact C,D,K,orientation theorem, exact 75-atom theorem, or accepted theta2 payload",
            next_action="classify through exact-P minimal hook before spending first-pass reading budget",
            ok=True,
        ),
        RealityRow(
            name="constructive_packetizable_source_payload",
            evidence_kind="source_theorem_plus_payload",
            decision="would_enter_packet_intake_then_need_danger3_framing",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=True,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity framing, same-j bridge, X_1(16), halving or direct x0, then vpp.py",
            next_action="route through candidate-packet intake and post-theorem extraction",
            ok=True,
        ),
        RealityRow(
            name="ambient_780_value_shadow",
            evidence_kind="rejected_shadow",
            decision="reject_or_repair_ambient_mu11_value",
            current_evidence_exists=True,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=True,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="ambient period 780 leaves mu_11 ambiguity unless it descends to support period 156",
            next_action="discard or repair with explicit period-156 branch/root/telescoping data",
            ok=True,
        ),
        RealityRow(
            name="generic_class_field_generation_or_cm_shadow",
            evidence_kind="rejected_shadow",
            decision="reject_generic_generation_not_selected_finite_identity",
            current_evidence_exists=True,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=True,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="one exact p25 finite product/value/divisor identity with row and scalar data",
            next_action="use as vocabulary only; do not count as a theorem closer",
            ok=True,
        ),
        RealityRow(
            name="source_closed_no_extraction",
            evidence_kind="post_source_stage",
            decision="theorem_win_not_submission_until_extraction",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=True,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="DANGER3 framing, same-j X_1(8112), practical X_1(16), halving or direct x0",
            next_action="celebrate the math win, then keep routing through extraction",
            ok=True,
        ),
        RealityRow(
            name="official_vpp_boundary",
            evidence_kind="submission_boundary",
            decision="submission_ready_only_after_official_vpp_triple",
            current_evidence_exists=False,
            source_stage_closes_if_theorem_present=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=True,
            current_submission_ready=False,
            first_missing_or_falsifier="concrete p25 (A,x0) passing official DANGER3 vpp.py",
            next_action="verify immediately if practical search or extraction emits a candidate triple",
            ok=True,
        ),
    )


def build_ledger() -> RealityLedger:
    markers = evidence_markers()
    rows = reality_rows()
    expected_decisions = (
        "fixed_payload_factors_not_search_candidates",
        "pinned_finite_target_not_arithmetic_source_theorem",
        "finite_payload_without_source_theorem",
        "would_close_first_pass_source_stage_then_need_extraction",
        "would_close_value_source_stage_then_need_extraction",
        "would_close_heavy_source_stage_then_need_extraction",
        "would_enter_packet_intake_then_need_danger3_framing",
        "reject_or_repair_ambient_mu11_value",
        "reject_generic_generation_not_selected_finite_identity",
        "theorem_win_not_submission_until_extraction",
        "submission_ready_only_after_official_vpp_triple",
    )
    current_evidence = sum(row.current_evidence_exists for row in rows)
    source_shapes = sum(row.source_stage_closes_if_theorem_present for row in rows)
    current_source = sum(row.current_source_theorem_exists for row in rows)
    computed_only = sum(row.computed_payload_only for row in rows)
    rejected = sum(row.rejected for row in rows)
    conditional = sum(row.conditional for row in rows)
    submission_boundary = sum(row.submission_boundary for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 11
        and tuple(row.decision for row in rows) == expected_decisions
        and current_evidence == 5
        and source_shapes == 4
        and current_source == 0
        and computed_only == 2
        and rejected == 2
        and conditional == 2
        and submission_boundary == 1
        and current_submission == 0
        and all(row.ok for row in rows)
    )
    return RealityLedger(
        evidence_markers=markers,
        rows=rows,
        evidence_markers_ok=sum(row.ok for row in markers),
        current_evidence_rows=current_evidence,
        source_closing_shape_rows=source_shapes,
        current_source_theorem_rows=current_source,
        computed_payload_only_rows=computed_only,
        rejected_rows=rejected,
        conditional_rows=conditional,
        submission_boundary_rows=submission_boundary,
        current_submission_ready_rows=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    ledger = build_ledger()
    print("p25 v2 value payload reality ledger")
    for marker_row in ledger.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in ledger.rows:
        print(
            f"  {row.name}: decision={row.decision} "
            f"evidence={int(row.current_evidence_exists)} "
            f"source_shape={int(row.source_stage_closes_if_theorem_present)} "
            f"current_source={int(row.current_source_theorem_exists)} "
            f"computed_only={int(row.computed_payload_only)} "
            f"rejected={int(row.rejected)} conditional={int(row.conditional)} "
            f"submission_boundary={int(row.submission_boundary)}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
        print(f"    next_action={row.next_action}")
    print("counts")
    print(f"  evidence_markers_ok={ledger.evidence_markers_ok}/{len(ledger.evidence_markers)}")
    print(f"  current_evidence_rows={ledger.current_evidence_rows}")
    print(f"  source_closing_shape_rows={ledger.source_closing_shape_rows}")
    print(f"  current_source_theorem_rows={ledger.current_source_theorem_rows}")
    print(f"  computed_payload_only_rows={ledger.computed_payload_only_rows}")
    print(f"  rejected_rows={ledger.rejected_rows}")
    print(f"  conditional_rows={ledger.conditional_rows}")
    print(f"  submission_boundary_rows={ledger.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={ledger.current_submission_ready_rows}")
    print("interpretation")
    print("  finite_fixtures_are_not_source_theorems=1")
    print("  source_theorem_is_not_submission_without_extraction=1")
    print(f"p25_v2_value_payload_reality_ledger_rows={int(ledger.row_ok)}/1")
    return 0 if ledger.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

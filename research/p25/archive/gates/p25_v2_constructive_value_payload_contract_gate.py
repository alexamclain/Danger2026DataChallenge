#!/usr/bin/env python3
"""Constructive payload contract for p25 source-theorem hits.

The first-pass theorem target is now narrow enough that a future answer can be
screened before reopening the archive: it must not only name the legal row and
fix the scalar, it must also give deterministic finite data that can enter the
candidate-packet and post-theorem extraction ladders.
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
class PayloadRow:
    name: str
    has_arithmetic_source: bool
    selects_legal_row: bool
    fixes_fp_scalar: bool
    has_deterministic_evaluation: bool
    enters_packet_intake: bool
    source_stage_candidate_if_theorem_present: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ConstructivePayloadContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[PayloadRow, ...]
    evidence_markers_ok: int
    packetizable_source_shapes: int
    repair_rows: int
    reject_rows: int
    current_packetizable_payloads: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "period156_value_source_hook",
            "research/p25/evidence/p25_v2_period156_value_source_hook_20260616.md",
            "p25_v2_period156_value_source_hook_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "candidate_packet_intake_reorg",
            "research/p25/evidence/p25_v2_candidate_packet_intake_reorg_20260616.md",
            "p25_v2_candidate_packet_intake_reorg_rows=1/1",
        ),
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "danger3_finite_identity_framing",
            "research/p25/evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
            "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
        ),
        marker(
            "unified_submission_extraction",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
    )


def payload_rows() -> tuple[PayloadRow, ...]:
    return (
        PayloadRow(
            name="exact_fp_row_value_from_source",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=True,
            source_stage_candidate_if_theorem_present=True,
            decision="source_stage_packetizable_danger3_framing_missing",
            first_missing_or_falsifier="DANGER3 finite-identity framing, then same-j/X_1(16)/halving extraction",
            ok=True,
        ),
        PayloadRow(
            name="finite_additive_or_telescoping_formula",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=True,
            source_stage_candidate_if_theorem_present=True,
            decision="source_stage_packetizable_danger3_framing_missing",
            first_missing_or_falsifier="DANGER3 finite-identity framing, then same-j/X_1(16)/halving extraction",
            ok=True,
        ),
        PayloadRow(
            name="period156_value_with_branch_payload",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=True,
            source_stage_candidate_if_theorem_present=True,
            decision="source_stage_packetizable_danger3_framing_missing",
            first_missing_or_falsifier="DANGER3 finite-identity framing, then same-j/X_1(16)/halving extraction",
            ok=True,
        ),
        PayloadRow(
            name="exact_product_file_plus_source_theorem",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=True,
            source_stage_candidate_if_theorem_present=True,
            decision="source_stage_packetizable_danger3_framing_missing",
            first_missing_or_falsifier="DANGER3 finite-identity framing, then same-j/X_1(16)/halving extraction",
            ok=True,
        ),
        PayloadRow(
            name="scalar_fixed_theorem_no_evaluation_rule",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=False,
            enters_packet_intake=False,
            source_stage_candidate_if_theorem_present=False,
            decision="repair_constructive_evaluation_missing",
            first_missing_or_falsifier="deterministic finite formula, basepoint, telescoping product, branch data, or exact product packet",
            ok=True,
        ),
        PayloadRow(
            name="class_field_generation_or_existence_only",
            has_arithmetic_source=True,
            selects_legal_row=False,
            fixes_fp_scalar=False,
            has_deterministic_evaluation=False,
            enters_packet_intake=False,
            source_stage_candidate_if_theorem_present=False,
            decision="repair_selected_constructive_row_missing",
            first_missing_or_falsifier="one legal support-156 row plus scalar-fixed finite evaluation data",
            ok=True,
        ),
        PayloadRow(
            name="local_finite_payload_no_source",
            has_arithmetic_source=False,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=False,
            source_stage_candidate_if_theorem_present=False,
            decision="repair_arithmetic_source_theorem_missing",
            first_missing_or_falsifier="challenge-legal arithmetic source theorem for the finite payload",
            ok=True,
        ),
        PayloadRow(
            name="direct_vpp_from_row_value",
            has_arithmetic_source=True,
            selects_legal_row=True,
            fixes_fp_scalar=True,
            has_deterministic_evaluation=True,
            enters_packet_intake=False,
            source_stage_candidate_if_theorem_present=False,
            decision="reject_row_value_is_not_A_x0",
            first_missing_or_falsifier="vpp.py verifies (p,A,x0), not a modular-unit row value",
            ok=True,
        ),
    )


def build_contract() -> ConstructivePayloadContract:
    markers = evidence_markers()
    rows = payload_rows()
    packetizable = sum(row.source_stage_candidate_if_theorem_present for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    rejects = sum(row.decision.startswith("reject_") for row in rows)
    current_packetizable = 0
    current_submission = 0
    expected = (
        "source_stage_packetizable_danger3_framing_missing",
        "source_stage_packetizable_danger3_framing_missing",
        "source_stage_packetizable_danger3_framing_missing",
        "source_stage_packetizable_danger3_framing_missing",
        "repair_constructive_evaluation_missing",
        "repair_selected_constructive_row_missing",
        "repair_arithmetic_source_theorem_missing",
        "reject_row_value_is_not_A_x0",
    )
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 8
        and tuple(row.decision for row in rows) == expected
        and packetizable == 4
        and repairs == 3
        and rejects == 1
        and current_packetizable == 0
        and current_submission == 0
        and all(row.ok for row in rows)
    )
    return ConstructivePayloadContract(
        evidence_markers=markers,
        rows=rows,
        evidence_markers_ok=sum(row.ok for row in markers),
        packetizable_source_shapes=packetizable,
        repair_rows=repairs,
        reject_rows=rejects,
        current_packetizable_payloads=current_packetizable,
        current_submission_ready=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    print("p25 v2 constructive value payload contract")
    for marker_row in contract.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in contract.rows:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source={int(row.has_arithmetic_source)} row={int(row.selects_legal_row)} "
            f"scalar={int(row.fixes_fp_scalar)} eval={int(row.has_deterministic_evaluation)} "
            f"packet={int(row.enters_packet_intake)} "
            f"source_stage={int(row.source_stage_candidate_if_theorem_present)}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  packetizable_source_shapes={contract.packetizable_source_shapes}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  reject_rows={contract.reject_rows}")
    print(f"  current_packetizable_payloads={contract.current_packetizable_payloads}")
    print(f"  current_submission_ready={contract.current_submission_ready}")
    print("interpretation")
    print("  source_hit_must_be_constructive_enough_for_packet_intake=1")
    print("  exact_row_value_is_not_direct_vpp_payload=1")
    print(f"p25_v2_constructive_value_payload_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

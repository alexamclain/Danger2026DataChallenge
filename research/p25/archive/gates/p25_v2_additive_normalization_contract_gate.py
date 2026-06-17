#!/usr/bin/env python3
"""Additive-normalization contract for p25 theorem snippets.

The live first-pass positive row says "finite divisor/additive theorem."  This
gate makes that phrase precise enough for source intake: divisor/Hilbert-90
data must be paired with a finite additive, value, branch, basepoint, or
telescoping normalization that fixes the otherwise invisible F_p^* scalar.
Formal divisor-class or boundary statements alone remain repair rows.
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
class AdditiveDecision:
    name: str
    theorem_shape: str
    has_legal_row: bool
    has_h90_boundary: bool
    fixes_fp_scalar: bool
    has_arithmetic_source: bool
    decision: str
    source_candidate_if_theorem_present: bool
    normalize_then_intake: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class AdditiveNormalizationContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    decisions: tuple[AdditiveDecision, ...]
    evidence_markers_ok: int
    source_candidate_shapes: int
    normalize_rows: int
    repair_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "period156_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
    )


def decisions() -> tuple[AdditiveDecision, ...]:
    return (
        AdditiveDecision(
            name="normalized_divisor_additive_theorem",
            theorem_shape=(
                "finite divisor/additive theorem for one normalized legal support-156 row, "
                "with Norm_156(Y_507) boundary and finite normalization fixing the value"
            ),
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=True,
            has_arithmetic_source=True,
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        AdditiveDecision(
            name="period156_value_with_telescoping",
            theorem_shape=(
                "period-156 value theorem whose branch/root/telescoping context fixes the same finite value"
            ),
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=True,
            has_arithmetic_source=True,
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        AdditiveDecision(
            name="divisor_h90_no_additive_normalization",
            theorem_shape="divisor identity plus H90 boundary, but no scalar-fixing additive/value datum",
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=False,
            has_arithmetic_source=True,
            decision="repair_additive_normalization_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="finite additive/value/basepoint/telescoping normalization fixing the F_p^* scalar",
            ok=True,
        ),
        AdditiveDecision(
            name="principal_divisor_or_divisor_class_only",
            theorem_shape="principal-divisor or divisor-class equality for the legal row, with no finite value normalization",
            has_legal_row=True,
            has_h90_boundary=False,
            fixes_fp_scalar=False,
            has_arithmetic_source=True,
            decision="repair_additive_normalization_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="H90 boundary plus scalar-fixing finite additive/value normalization",
            ok=True,
        ),
        AdditiveDecision(
            name="additive_relation_without_selected_row",
            theorem_shape="finite additive relation for a dense norm or family average, but no selected legal support-156 row",
            has_legal_row=False,
            has_h90_boundary=True,
            fixes_fp_scalar=True,
            has_arithmetic_source=True,
            decision="repair_selected_row_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="legal support-156 row selection before applying the additive normalization",
            ok=True,
        ),
        AdditiveDecision(
            name="additive_relation_up_to_constant",
            theorem_shape="additive/value statement that is still only determined up to an unspecified F_p^* scalar",
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=False,
            has_arithmetic_source=True,
            decision="repair_constant_normalization_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="specified scalar, finite normalization, or period-156 branch/root context",
            ok=True,
        ),
        AdditiveDecision(
            name="local_numeric_normalization_no_source",
            theorem_shape="locally computed finite normalization for the row, but no arithmetic source theorem",
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=True,
            has_arithmetic_source=False,
            decision="repair_arithmetic_source_theorem_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            ok=True,
        ),
        AdditiveDecision(
            name="normalized_after_basepoint_or_telescoping_fix",
            theorem_shape="same theorem data after a basepoint, finite additive identity, or telescoping product fixes the scalar",
            has_legal_row=True,
            has_h90_boundary=True,
            fixes_fp_scalar=True,
            has_arithmetic_source=True,
            decision="normalize_additive_value_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after additive/value normalization",
            ok=True,
        ),
    )


def build_contract() -> AdditiveNormalizationContract:
    markers = evidence_markers()
    rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in rows)
    normalize = sum(row.normalize_then_intake for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    current_closers = 0
    expected = (
        "source_stage_candidate_if_theorem_present",
        "source_stage_candidate_if_theorem_present",
        "repair_additive_normalization_missing",
        "repair_additive_normalization_missing",
        "repair_selected_row_missing",
        "repair_constant_normalization_missing",
        "repair_arithmetic_source_theorem_missing",
        "normalize_additive_value_then_apply_source_snippet_intake",
    )
    row_ok = (
        markers_ok == len(markers)
        and len(rows) == 8
        and tuple(row.decision for row in rows) == expected
        and source_candidates == 2
        and normalize == 1
        and repairs == 5
        and current_closers == 0
        and all(row.ok for row in rows)
    )
    return AdditiveNormalizationContract(
        evidence_markers=markers,
        decisions=rows,
        evidence_markers_ok=markers_ok,
        source_candidate_shapes=source_candidates,
        normalize_rows=normalize,
        repair_rows=repairs,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for marker_row in contract.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("decisions")
    for row in contract.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"legal_row={int(row.has_legal_row)} h90={int(row.has_h90_boundary)} "
            f"fixes_scalar={int(row.fixes_fp_scalar)} source={int(row.has_arithmetic_source)} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)} "
            f"normalize={int(row.normalize_then_intake)}"
        )
        print(f"    shape={row.theorem_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  source_candidate_shapes={contract.source_candidate_shapes}")
    print(f"  normalize_rows={contract.normalize_rows}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print("interpretation")
    print("  divisor_additive_means_divisor_h90_plus_scalar_fixing_finite_normalization=1")
    print("  divisor_class_or_boundary_without_additive_value_normalization_is_repair=1")
    print("  additive_relation_for_dense_norm_still_needs_selected_legal_row=1")
    print(f"p25_v2_additive_normalization_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

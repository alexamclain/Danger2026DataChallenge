#!/usr/bin/env python3
"""Validate the priority-1 divisor/additive theorem work order."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class WorkRow:
    name: str
    decision: str
    requirement: str
    falsifier: str


EVIDENCE_INPUTS = (
    (
        "route_priority_falsifier_matrix",
        "evidence/p25_v2_route_priority_falsifier_matrix_20260617.md",
        "p25_v2_route_priority_falsifier_matrix_rows=1/1",
    ),
    (
        "unified_value_divisor_interface",
        "evidence/p25_v2_unified_value_divisor_interface_20260616.md",
        "p25_v2_unified_value_divisor_interface_rows=1/1",
    ),
    (
        "additive_normalization_contract",
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "additive_normalizer_source_scan",
        "evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
        "p25_v2_additive_normalizer_source_scan_rows=1/1",
    ),
    (
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    (
        "koo_shin_distribution_noncloser",
        "evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
        "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
    ),
    (
        "theorem52_constant_span_obstruction",
        "evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
        "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
    ),
    (
        "h0_theorem_interface_contract",
        "evidence/p25_v2_h0_theorem_interface_contract_20260616.md",
        "p25_v2_h0_theorem_interface_contract_rows=1/1",
    ),
    (
        "conductor39_yang_h90_interface_contract",
        "evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
        "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1",
    ),
    (
        "source_snippet_intake",
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def work_rows() -> tuple[WorkRow, ...]:
    return (
        WorkRow(
            "one_normalized_row_divisor_additive",
            "priority1_source_stage_candidate_if_present",
            "one legal support-156 row, Norm_156(Y_507) boundary, finite scalar-fixing additive/divisor identity",
            "source legality, boundary-only, divisor class only, or unspecified F_p^* scalar",
        ),
        WorkRow(
            "h0_h0_translate_additive_identity",
            "normalize_h0_product_then_priority1_intake",
            "one exact legal H0/H0-translate product with H90 boundary and scalar-fixed additive data",
            "H0 source certificate, formal product, or period language without finite scalar-fixing identity",
        ),
        WorkRow(
            "conductor39_yang_additive_identity",
            "normalize_yang_h90_product_then_priority1_intake",
            "mixed U_chi/W source, Yang lift, H90 descent, and scalar-fixed finite additive theorem",
            "prime projection, one-axis legality, Q support data, or Yang lift without finite theorem",
        ),
        WorkRow(
            "row_labeled_or_reciprocal_additive_theorem",
            "normalize_row_label_or_reciprocal_then_priority1_intake",
            "row label or reciprocal-minus-boundary convention plus scalar-fixed theorem for at least one legal row",
            "unordered orbit, symmetric aggregate, reciprocal plus boundary, or missing row label",
        ),
        WorkRow(
            "koo_shin_2010_source_legality",
            "repair_finite_additive_theorem_missing",
            "Theorem 6.2 legality plus a new finite scalar-fixed theorem not currently in the extract",
            "Theorem 6.2, Lemma 6.1, or Theorem 5.2 repeated as source/context only",
        ),
        WorkRow(
            "theorem52_constant_product_repair",
            "reject_constant_span_repair",
            "nonzero constant-exponent product in legal quotient-C4 span",
            "legal quotient-C4 span meets constant line only at zero",
        ),
        WorkRow(
            "divisor_h90_without_additive_normalizer",
            "repair_scalar_normalization_missing",
            "basepoint, finite additive value, telescoping product, branch/root, or specified scalar",
            "principal divisor, H90 boundary, or value up to F_p^* scalar only",
        ),
        WorkRow(
            "finite_payload_without_arithmetic_source",
            "repair_arithmetic_source_theorem_missing",
            "challenge-legal arithmetic source theorem producing the finite identity",
            "local row value, packet, fixture, or numeric target without source theorem",
        ),
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[WorkRow, ...], bool]:
    markers = evidence_markers(root)
    rows = work_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and len(rows) == 8
        and sum(row.decision.endswith("source_stage_candidate_if_present") for row in rows) == 1
        and sum("priority1_intake" in row.decision for row in rows) == 3
        and sum(row.decision.startswith("repair") for row in rows) == 3
        and sum(row.decision.startswith("reject") for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    markers, rows, row_ok = build_check(research_root())
    print("p25 v2 priority-1 divisor/additive work order")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    requirement={row.requirement}")
        print(f"    first_falsifier={row.falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"work_rows={len(rows)}")
    print(f"source_stage_candidate_rows={sum(row.decision.endswith('source_stage_candidate_if_present') for row in rows)}")
    print(f"normalization_rows={sum('priority1_intake' in row.decision for row in rows)}")
    print(f"repair_rows={sum(row.decision.startswith('repair') for row in rows)}")
    print(f"reject_rows={sum(row.decision.startswith('reject') for row in rows)}")
    print("current_priority1_source_theorems=0")
    print("current_submission_ready=0")
    print(f"p25_v2_priority1_divisor_additive_work_order_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

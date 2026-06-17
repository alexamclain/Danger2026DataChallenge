#!/usr/bin/env python3
"""Validate the priority-1 divisor/additive prior-art candidate sweep."""

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
class SweepRow:
    name: str
    prior_shape: str
    decision: str
    missing_or_falsifier: str


EVIDENCE_INPUTS = (
    (
        "priority1_work_order",
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    (
        "source_snippet_intake",
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
    (
        "current_expert_response_rubric",
        "evidence/p25_v2_current_expert_response_rubric_20260616.md",
        "p25_v2_current_expert_response_rubric_rows=1/1",
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
        "row_orientation_candidate_sweep",
        "evidence/p25_v2_row_orientation_candidate_sweep_20260617.md",
        "p25_v2_row_orientation_candidate_sweep_rows=1/1",
    ),
    (
        "quartic_selector_candidate_sweep",
        "evidence/p25_v2_quartic_selector_candidate_sweep_20260617.md",
        "p25_v2_quartic_selector_candidate_sweep_rows=1/1",
    ),
    (
        "zero_lattice_candidate_sweep",
        "evidence/p25_v2_zero_lattice_candidate_sweep_20260617.md",
        "p25_v2_zero_lattice_candidate_sweep_rows=1/1",
    ),
    (
        "q_route_candidate_sweep",
        "evidence/p25_v2_q_route_candidate_sweep_20260617.md",
        "p25_v2_q_route_candidate_sweep_rows=1/1",
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


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            "source_snippet_exact_divisor_additive_fixture",
            "intake classifier contains a hypothetical exact_divisor_additive_m1 source-stage row",
            "positive_classifier_not_existing_theorem",
            "no actual arithmetic source theorem payload is attached",
        ),
        SweepRow(
            "current_expert_rubric_source_closing_rows",
            "rubric lists normalized divisor/additive theorem as accepted",
            "classifier_not_prior_art_closer",
            "current_source_stage_closers remains zero",
        ),
        SweepRow(
            "koo_shin_2010_theorem62_legality",
            "Theorem 6.2 certifies legal source products",
            "repair_finite_additive_theorem_missing",
            "source legality does not emit finite scalar-fixed additive identity",
        ),
        SweepRow(
            "koo_shin_theorem52_constant_product",
            "Theorem 5.2 constant-product/root-descent repair",
            "reject_constant_span_repair",
            "legal quotient-C4 span has no nonzero constant vector",
        ),
        SweepRow(
            "local_additive_normalizer_scan",
            "local source extracts contain helper vocabulary",
            "no_local_additive_normalizer_found",
            "no basepoint, telescoping, period-156, H90, Y507, or scalar-fixing theorem in extract",
        ),
        SweepRow(
            "row_labeled_or_reciprocal_artifacts",
            "row/orientation artifacts normalize legal rows",
            "normalizer_only_priority1_theorem_missing",
            "missing scalar-fixed divisor/additive theorem after normalization",
        ),
        SweepRow(
            "quartic_selector_artifacts",
            "quartic C4 selector and reciprocal-orientation artifacts",
            "selector_only_priority1_theorem_missing",
            "missing scalar-fixed finite theorem for selected row",
        ),
        SweepRow(
            "zero_lattice_pair_square_artifacts",
            "boundary-zero, pair, square, and quotient artifacts",
            "repair_rows_not_priority1_closers",
            "need exact scalar-fixed one-row theorem, not relation or root debt",
        ),
        SweepRow(
            "q_route_artifacts",
            "Q, Q3, Q6, diagonal, split, and Q-square artifacts",
            "support_or_payload_not_priority1_closer",
            "support/normalization or extraction map missing; no one-row arithmetic theorem",
        ),
        SweepRow(
            "finite_payload_or_packet_without_source",
            "local row values, fixtures, packets, or numeric targets",
            "repair_arithmetic_source_theorem_missing",
            "finite target data is not a challenge-legal arithmetic theorem",
        ),
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[SweepRow, ...], bool]:
    markers = evidence_markers(root)
    rows = sweep_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and len(rows) == 10
        and sum(row.decision.endswith("missing") for row in rows) >= 4
        and sum(row.decision.startswith("reject") for row in rows) == 1
        and sum("not_existing_theorem" in row.decision for row in rows) == 1
        and sum("not_prior_art_closer" in row.decision for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    markers, rows, row_ok = build_check(research_root())
    print("p25 v2 priority-1 candidate sweep")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"sweep_rows={len(rows)}")
    print("newly_promoted_priority1_candidates=0")
    print("surviving_priority1_intake_families=4")
    print("current_priority1_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_priority1_candidate_sweep_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

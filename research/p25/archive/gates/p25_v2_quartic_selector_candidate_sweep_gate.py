#!/usr/bin/env python3
"""Sweep prior quartic/projector artifacts under the p25 v2 intake."""

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
class SweepRow:
    name: str
    prior_shape: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class QuarticSelectorCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_quartic_intake_families: int
    current_source_stage_closers: int
    current_submission_ready: int
    q_split_normalization_confirmed: bool
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "quartic_reciprocal_orientation",
            "research/p25/evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
            "p25_v2_quartic_reciprocal_orientation_rows=1/1",
        ),
        marker(
            "c4_character_spectrum",
            "research/p25/evidence/p25_v2_c4_character_spectrum_20260616.md",
            "p25_v2_c4_character_spectrum_rows=1/1",
        ),
        marker(
            "row_sign_c4_tensor_spectrum",
            "research/p25/evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md",
            "p25_v2_row_sign_c4_tensor_spectrum_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "q_split_quartic_selector",
            "research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md",
            "p25_v2_q_split_quartic_selector_rows=1/1",
        ),
        marker(
            "power_projector_extraction_boundary",
            "research/p25/evidence/p25_v2_power_projector_extraction_boundary_20260616.md",
            "p25_v2_power_projector_extraction_boundary_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="exact_c4_phase_selector",
            prior_shape="exact row-antisymmetric C4_1 phase table for the four legal rows",
            decision="live_selector_contract_not_prior_source_theorem",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem for the selected row",
            ok=True,
        ),
        SweepRow(
            name="coarse_quartic_or_quadratic_data",
            prior_shape="phase sign, magnitude, or quadratic character aggregate",
            decision="repair_quartic_edge_selection_missing",
            first_missing_or_falsifier="coarse data leaves a two-edge or all-four ambiguity",
            ok=True,
        ),
        SweepRow(
            name="row_sign_or_c4_projection_only",
            prior_shape="row sign without C4 phase, C4 edge without row sign, or projection-only theorem",
            decision="repair_or_reject_mixed_tensor_missing",
            first_missing_or_falsifier="legal conductor-39 row is row-antisymmetric tensor times one C4 edge",
            ok=True,
        ),
        SweepRow(
            name="reciprocal_phase_presentations",
            prior_shape="exact phase on a reciprocal row or phase collision with the opposite oriented edge",
            decision="normalize_only_with_orientation_and_minus_boundary",
            first_missing_or_falsifier="reciprocal rows carry -Norm_156(Y_507), not the positive boundary",
            ok=True,
        ),
        SweepRow(
            name="two_edge_or_doubled_edge_projectors",
            prior_shape="row/column/diagonal pair data or pair plus difference reaching 2*edge",
            decision="repair_oriented_square_root_missing",
            first_missing_or_falsifier="p25 has a real sign ambiguity when recovering one edge from a doubled edge",
            ok=True,
        ),
        SweepRow(
            name="four_edge_projector_components",
            prior_shape="constant, row, column, checkerboard components reconstructing 4*edge",
            decision="repair_mu4_root_or_scalar_missing",
            first_missing_or_falsifier="p25 has a four-element fourth-power kernel for projector division by 4",
            ok=True,
        ),
        SweepRow(
            name="q_split_quartic_support",
            prior_shape="Q diagonal pure quadratic plus pure quartic split",
            decision="support_normalization_not_prior_closer",
            first_missing_or_falsifier="diagonal plus split reaches 2*edge and still needs oriented root/sign or direct theorem",
            ok=True,
        ),
        SweepRow(
            name="selected_root_projector_value",
            prior_shape="future exact R4/projector value with selected fourth root",
            decision="normalize_then_apply_source_snippet_intake",
            first_missing_or_falsifier="no current source theorem supplies the selected root and finite row theorem",
            ok=True,
        ),
        SweepRow(
            name="source_family_prior_scan",
            prior_shape="inspected Koo-Shin/Sprang/Kubert-Lang/Schertz source families",
            decision="no_prior_exact_quartic_finite_theorem_found",
            first_missing_or_falsifier="source-family gap matrix still has scalar_fixed_finite_theorems=0 and first_pass_closers=0",
            ok=True,
        ),
    )


def build_sweep() -> QuarticSelectorCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    selector = read("research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md")
    reciprocal = read("research/p25/evidence/p25_v2_quartic_reciprocal_orientation_20260616.md")
    c4 = read("research/p25/evidence/p25_v2_c4_character_spectrum_20260616.md")
    tensor = read("research/p25/evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md")
    partial = read("research/p25/evidence/p25_v2_partial_projector_selector_20260616.md")
    projector = read("research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md")
    q_split = read("research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md")
    power_projector = read("research/p25/evidence/p25_v2_power_projector_extraction_boundary_20260616.md")
    positive = read("research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md")
    source_family = read("research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md")

    selector_ok = (
        "exact_quartic_selector_without_value_theorem" in selector
        and "current_source_theorems = 0" in selector
    )
    reciprocal_ok = (
        "reciprocal_phase_plus_boundary" in reciprocal
        and "reciprocal product carries -Norm_156 boundary" in reciprocal
        and "current_source_closers = 0" in reciprocal
    )
    c4_ok = (
        "order4_selector_without_value_theorem" in c4
        and "current_source_theorems = 0" in c4
    )
    tensor_ok = (
        "tensor_selector_without_value_theorem" in tensor
        and "current_source_theorems = 0" in tensor
    )
    partial_ok = (
        "pair_plus_difference_without_square_root" in partial
        and "current_source_theorems = 0" in partial
    )
    projector_ok = (
        "all_projector_values_without_root" in projector
        and "current_source_theorems = 0" in projector
    )
    q_split_normalization_confirmed = (
        "Q diagonal + correct quartic split + oriented root/sign" in q_split
        and "current_source_theorems = 0" in q_split
    )
    power_projector_ok = (
        "exact_R4_projector_value_with_selected_root" in power_projector
        and "current_source_theorem = no" in power_projector
    )
    positive_ok = (
        "exact_quartic_selector_without_finite_theorem" in positive
        and "repair_value_divisor_theorem_missing" in positive
        and "current_source_theorems = 0" in positive
    )
    source_scan_ok = (
        "scalar_fixed_finite_theorems = 0" in source_family
        and "first_pass_closers = 0" in source_family
    )
    newly_promoted_prior_candidates = 0
    surviving_quartic_intake_families = 3
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 9
        and all(row.ok for row in rows)
        and selector_ok
        and reciprocal_ok
        and c4_ok
        and tensor_ok
        and partial_ok
        and projector_ok
        and q_split_normalization_confirmed
        and power_projector_ok
        and positive_ok
        and source_scan_ok
        and newly_promoted_prior_candidates == 0
        and surviving_quartic_intake_families == 3
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return QuarticSelectorCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_quartic_intake_families=surviving_quartic_intake_families,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        q_split_normalization_confirmed=q_split_normalization_confirmed,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 quartic selector candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_quartic_intake_families={sweep.surviving_quartic_intake_families}")
    print(f"  q_split_normalization_confirmed={int(sweep.q_split_normalization_confirmed)}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_quartic_selector_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

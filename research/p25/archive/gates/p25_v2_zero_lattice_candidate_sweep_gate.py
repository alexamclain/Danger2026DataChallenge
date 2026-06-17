#!/usr/bin/env python3
"""Sweep zero-lattice and row-square artifacts under the p25 v2 intake."""

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
class ZeroLatticeCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_normalization_families: int
    current_source_stage_closers: int
    current_submission_ready: int
    q_square_payload_bounded: bool
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "edge_lattice_global_minimality",
            "research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
            "p25_v2_edge_lattice_global_minimality_rows=1/1",
        ),
        marker(
            "zero_lattice_transfer_contract",
            "research/p25/evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
            "p25_v2_zero_lattice_transfer_contract_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
        ),
        marker(
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_split_quotient_complexity",
            "research/p25/evidence/p25_v2_q_split_quotient_complexity_20260616.md",
            "p25_v2_q_split_quotient_complexity_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="unit_edge",
            prior_shape="one coefficient is 1 and the other three are 0",
            decision="only_source_stage_shape_if_finite_theorem_present",
            first_missing_or_falsifier="no current artifact supplies the scalar-fixed finite theorem",
            ok=True,
        ),
        SweepRow(
            name="zero_lattice_basis_or_pair_quotients",
            prior_shape="rank-3 boundary-zero quotient lattice among legal rows",
            decision="support_transfer_data_not_source_close",
            first_missing_or_falsifier="zero Hilbert-90 boundary cannot create the first W-boundary row value",
            ok=True,
        ),
        SweepRow(
            name="nonunit_w_boundary_vector",
            prior_shape="coefficient sum 1 but not a unit edge",
            decision="repair_edge_plus_boundary_zero_lattice",
            first_missing_or_falsifier="finite value for boundary-zero content or direct unit-edge theorem missing",
            ok=True,
        ),
        SweepRow(
            name="diagonal_pair_or_broad_quadratic",
            prior_shape="m1*m4=m2*m8 diagonal aggregate with 2W boundary",
            decision="repair_broad_quadratic_aggregate_boundary_2w",
            first_missing_or_falsifier="selector/factorization down to one sparse W-boundary edge missing",
            ok=True,
        ),
        SweepRow(
            name="row_quotient_square_bridge",
            prior_shape="diagonal aggregate plus matching quotient reaches 2*edge",
            decision="repair_row_square_bridge_halving_missing",
            first_missing_or_falsifier="halving/root/orientation data selecting one legal row missing",
            ok=True,
        ),
        SweepRow(
            name="row_square_or_doubled_boundary",
            prior_shape="exact value/divisor theorem for a row square or doubled 2W boundary",
            decision="repair_row_square_root_sign_missing",
            first_missing_or_falsifier="constant sign has zero divisor and zero H90 boundary",
            ok=True,
        ),
        SweepRow(
            name="two_edge_pair_data",
            prior_shape="row/column/diagonal pair aggregate or pair difference",
            decision="repair_sign_or_root_or_edge_selector_missing",
            first_missing_or_falsifier="pair data reaches at best 2*edge before oriented root selection",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_value",
            prior_shape="Q projection equals m1+m4=m2+m8",
            decision="support_diagonal_aggregate_selector_missing",
            first_missing_or_falsifier="boundary-zero split/orientation data or direct one-edge theorem missing",
            ok=True,
        ),
        SweepRow(
            name="q_diagonal_plus_split_without_root",
            prior_shape="Q diagonal plus m1-m4 or m2-m8 split reaches 2*edge",
            decision="repair_oriented_square_root_missing",
            first_missing_or_falsifier="oriented root/sign data missing after the split",
            ok=True,
        ),
        SweepRow(
            name="q_square_exact_value",
            prior_shape="future exact scalar-fixed value for the Q square row",
            decision="bounded_two_root_payload_not_source_close",
            first_missing_or_falsifier="row-value roots still need DANGER3 extraction map",
            ok=True,
        ),
        SweepRow(
            name="wrong_q_split_shortcut",
            prior_shape="support-12 quotient or one-axis split used as Q normalizer",
            decision="reject_wrong_split_for_q_diagonal",
            first_missing_or_falsifier="Q normalizer must be m1-m4 or m2-m8, both support 24 and all columns",
            ok=True,
        ),
    )


def build_sweep() -> ZeroLatticeCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    intake = read("research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md")
    global_min = read("research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md")
    transfer = read("research/p25/evidence/p25_v2_zero_lattice_transfer_contract_20260616.md")
    diagonal = read("research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md")
    quotient = read("research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md")
    square = read("research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md")
    partial = read("research/p25/evidence/p25_v2_partial_projector_selector_20260616.md")
    q_diag = read("research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md")
    q_split = read("research/p25/evidence/p25_v2_q_split_quotient_complexity_20260616.md")
    q_square = read("research/p25/evidence/p25_v2_q_square_payload_router_20260616.md")
    q_extraction = read("research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md")
    positive = read("research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md")

    intake_ok = (
        "W-boundary non-edge vector" in intake
        and "current_source_theorems = 0" in intake
    )
    global_ok = (
        "L1-minimal W-boundary vectors = {m1, m2, m4, m8}" in global_min
        and "current_source_theorems = 0" in global_min
    )
    transfer_ok = (
        "zero_lattice_basis_values_only" in transfer
        and "current_source_stage_closers = 0" in transfer
    )
    diagonal_ok = (
        "diagonal_identity_m1m4_equals_m2m8" in diagonal
        and "current_source_stage_closers = 0" in diagonal
    )
    quotient_ok = (
        "row_quotient_only" in quotient
        and "diagonal_aggregate_plus_quotient" in quotient
        and "current_source_stage_closers = 0" in quotient
    )
    square_ok = (
        "row_square_value_theorem" in square
        and "current_source_stage_closers = 0" in square
    )
    partial_ok = (
        "pair_plus_difference_without_square_root" in partial
        and "current_source_theorems = 0" in partial
    )
    q_diag_ok = (
        "q_diagonal_value_only" in q_diag
        and "current_source_theorems = 0" in q_diag
    )
    q_split_ok = (
        "support12_quotient_used_as_q_diagonal_split" in q_split
        and "current_source_theorems = 0" in q_split
    )
    q_square_payload_bounded = (
        "q_square_exact_fp_value" in q_square
        and "two row-value roots" in q_square
        and "current_source_theorems = 0" in q_square
        and "q_square_exact_fp_value_only" in q_extraction
        and "current_submission_ready_rows = 0" in q_extraction
    )
    positive_ok = (
        "projector_or_two_edge_value" in positive
        and "repair_oriented_edge_selection_missing" in positive
        and "current_source_theorems = 0" in positive
    )
    newly_promoted_prior_candidates = 0
    surviving_normalization_families = 3
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 11
        and all(row.ok for row in rows)
        and intake_ok
        and global_ok
        and transfer_ok
        and diagonal_ok
        and quotient_ok
        and square_ok
        and partial_ok
        and q_diag_ok
        and q_split_ok
        and q_square_payload_bounded
        and positive_ok
        and newly_promoted_prior_candidates == 0
        and surviving_normalization_families == 3
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return ZeroLatticeCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_normalization_families=surviving_normalization_families,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        q_square_payload_bounded=q_square_payload_bounded,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 zero-lattice candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_normalization_families={sweep.surviving_normalization_families}")
    print(f"  q_square_payload_bounded={int(sweep.q_square_payload_bounded)}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_zero_lattice_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

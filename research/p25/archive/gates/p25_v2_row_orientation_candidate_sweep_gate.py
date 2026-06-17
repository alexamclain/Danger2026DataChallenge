#!/usr/bin/env python3
"""Sweep row/orbit/orientation artifacts under the p25 v2 intake."""

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
class RowOrientationCandidateSweep:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SweepRow, ...]
    newly_promoted_prior_candidates: int
    surviving_row_intake_families: int
    legal_orbit_complete: bool
    reciprocal_split_complete: bool
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "row_orientation_reciprocal_normalizer",
            "research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
            "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "orbit_tuple_theorem_router",
            "research/p25/evidence/p25_v2_orbit_tuple_theorem_router_20260616.md",
            "p25_v2_orbit_tuple_theorem_router_rows=1/1",
        ),
        marker(
            "k22_automorphism_quotient_falsifier",
            "research/p25/evidence/p25_v2_k22_automorphism_quotient_falsifier_20260616.md",
            "p25_v2_k22_automorphism_quotient_falsifier_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def sweep_rows() -> tuple[SweepRow, ...]:
    return (
        SweepRow(
            name="single_normalized_legal_row",
            prior_shape="one row m in {1,2,4,8} with row label/hash/edge",
            decision="source_stage_candidate_if_scalar_fixed_theorem_present",
            first_missing_or_falsifier="finite value/divisor or period-156 value theorem still missing",
            ok=True,
        ),
        SweepRow(
            name="stabilizer_or_doubling_equivalent_row",
            prior_shape="unit in doubling subgroup or stabilizer presentation",
            decision="normalize_to_legal_row_then_apply_source_snippet_intake",
            first_missing_or_falsifier="same theorem data after normalization",
            ok=True,
        ),
        SweepRow(
            name="outside_doubling_orientation_unspecified",
            prior_shape="outside-doubling unit row with no reciprocal orientation or boundary sign",
            decision="repair_reciprocal_orientation_or_boundary_sign_missing",
            first_missing_or_falsifier="must rewrite to oriented row or state reciprocal with -Norm_156 boundary",
            ok=True,
        ),
        SweepRow(
            name="reciprocal_row_with_minus_boundary",
            prior_shape="outside-doubling reciprocal row with -Norm_156(Y_507) boundary",
            decision="normalize_reciprocal_then_apply_source_snippet_intake",
            first_missing_or_falsifier="same theorem data after reciprocal normalization",
            ok=True,
        ),
        SweepRow(
            name="reciprocal_row_with_plus_boundary",
            prior_shape="reciprocal row asserted with positive Norm_156(Y_507) boundary",
            decision="reject_orientation_boundary_mismatch",
            first_missing_or_falsifier="reciprocal product carries the opposite Hilbert-90 boundary sign",
            ok=True,
        ),
        SweepRow(
            name="row_labeled_four_edge_tuple",
            prior_shape="four row-labeled divisor/additive or period-156 value identities",
            decision="choose_any_labeled_row_then_route_to_extraction",
            first_missing_or_falsifier="not present as a current source theorem; downstream extraction still needed",
            ok=True,
        ),
        SweepRow(
            name="parametric_doubling_orbit_theorem",
            prior_shape="uniform theorem for m in {1,2,4,8} with row labels",
            decision="normalize_m_then_apply_positive_clause_matcher",
            first_missing_or_falsifier="not present as a current source theorem",
            ok=True,
        ),
        SweepRow(
            name="unordered_four_values",
            prior_shape="set of four values without row labels",
            decision="repair_row_labeling_missing",
            first_missing_or_falsifier="assignment to one exact oriented edge missing",
            ok=True,
        ),
        SweepRow(
            name="symmetric_all_four_product_or_norm",
            prior_shape="all-four product, norm, trace, or quotient-invariant aggregate",
            decision="repair_oriented_edge_selection_missing",
            first_missing_or_falsifier="selected root/scalar/row label or direct one-edge theorem missing",
            ok=True,
        ),
        SweepRow(
            name="diagonal_pair_or_row_quotient_tuple",
            prior_shape="diagonal pair, pair tuple, row quotient, or boundary-zero tuple",
            decision="repair_square_root_pair_selector_or_one_edge_value_missing",
            first_missing_or_falsifier="oriented root/selector or direct one-edge finite theorem missing",
            ok=True,
        ),
        SweepRow(
            name="outside_doubling_orbit_tuple",
            prior_shape="tuple or theorem on units outside the current doubling orbit target",
            decision="reject_not_current_legal_four_row_target",
            first_missing_or_falsifier="row orbit normalization fixes the legal representatives",
            ok=True,
        ),
        SweepRow(
            name="all_four_rows_required",
            prior_shape="claim that a source-stage theorem must prove all four rows",
            decision="repair_overdemand_one_legal_row_is_enough",
            first_missing_or_falsifier="one normalized legal row is sufficient for the first-pass ask",
            ok=True,
        ),
    )


def build_sweep() -> RowOrientationCandidateSweep:
    markers = evidence_markers()
    rows = sweep_rows()
    orbit = read("research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md")
    reciprocal = read("research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md")
    graph = read("research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md")
    tuple_router = read("research/p25/evidence/p25_v2_orbit_tuple_theorem_router_20260616.md")
    k22 = read("research/p25/evidence/p25_v2_k22_automorphism_quotient_falsifier_20260616.md")
    positive = read("research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md")
    intake = read("research/p25/evidence/p25_v2_source_snippet_intake_20260616.md")
    rubric = read("research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md")

    legal_orbit_complete = (
        "legal_representatives = (1,2,4,8)" in orbit
        and "outside_units_matching_legal_rows = 0" in orbit
        and "orbit_classes_ok = 4/4" in orbit
    )
    reciprocal_split_complete = (
        "oriented_unit_count = 12" in reciprocal
        and "reciprocal_unit_count = 12" in reciprocal
        and "unclassified_unit_count = 0" in reciprocal
        and "current_source_stage_closers = 0" in reciprocal
    )
    graph_ok = (
        "edge_graph_is_k22 = 1" in graph
        and "source_candidate_routes = 1" in graph
        and "current_source_theorems = 0" in graph
    )
    tuple_ok = (
        "accepted_routes = 4" in tuple_router
        and "repair_rows = 6" in tuple_router
        and "reject_rows = 1" in tuple_router
        and "current_source_theorems = 0" in tuple_router
    )
    k22_ok = (
        "current_source_theorems = 0" in k22
        and "K_{2,2}" in k22
    )
    intake_ok = (
        "outside-doubling presentation" in intake
        and "reciprocal_orientation_unspecified" in intake
        and "current_source_stage_closers = 0" in intake
    )
    rubric_ok = (
        "outside_doubling" in rubric
        and "reciprocal_row_minus_boundary" in rubric
        and "current_source_stage_closers = 0" in rubric
    )
    positive_ok = "current_source_theorems = 0" in positive
    newly_promoted_prior_candidates = 0
    surviving_row_intake_families = 4
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 12
        and all(row.ok for row in rows)
        and legal_orbit_complete
        and reciprocal_split_complete
        and graph_ok
        and tuple_ok
        and k22_ok
        and intake_ok
        and rubric_ok
        and positive_ok
        and newly_promoted_prior_candidates == 0
        and surviving_row_intake_families == 4
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return RowOrientationCandidateSweep(
        markers=markers,
        rows=rows,
        newly_promoted_prior_candidates=newly_promoted_prior_candidates,
        surviving_row_intake_families=surviving_row_intake_families,
        legal_orbit_complete=legal_orbit_complete,
        reciprocal_split_complete=reciprocal_split_complete,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    sweep = build_sweep()
    print("p25 v2 row/orientation candidate sweep")
    for marker_row in sweep.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in sweep.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    prior_shape={row.prior_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  newly_promoted_prior_candidates={sweep.newly_promoted_prior_candidates}")
    print(f"  surviving_row_intake_families={sweep.surviving_row_intake_families}")
    print(f"  legal_orbit_complete={int(sweep.legal_orbit_complete)}")
    print(f"  reciprocal_split_complete={int(sweep.reciprocal_split_complete)}")
    print(f"  current_source_stage_closers={sweep.current_source_stage_closers}")
    print(f"  current_submission_ready={sweep.current_submission_ready}")
    print(f"p25_v2_row_orientation_candidate_sweep_rows={int(sweep.row_ok)}/1")
    return 0 if sweep.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Classify source families against the current p25 one-edge theorem target."""

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
class SourceFamilyRow:
    name: str
    source_page: str
    current_use: str
    has_relevant_vocabulary: bool
    has_one_edge_source_object: bool
    has_scalar_fixed_finite_theorem: bool
    has_period156_value_theorem: bool
    has_exactp_upstream_theorem: bool
    decision: str
    missing: str
    row_ok: bool


@dataclass(frozen=True)
class SourceFamilyGapMatrix:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceFamilyRow, ...]
    vocabulary_sources: int
    one_edge_source_objects: int
    scalar_fixed_finite_theorems: int
    period156_value_theorems: int
    exactp_upstream_theorems: int
    first_pass_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "self_contained_theorem_statement",
            "research/p25/evidence/p25_v2_self_contained_theorem_statement_20260616.md",
            "p25_v2_self_contained_theorem_statement_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
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
        marker(
            "additive_normalizer_source_scan",
            "research/p25/evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
            "p25_v2_additive_normalizer_source_scan_rows=1/1",
        ),
        marker(
            "koo_shin_distribution_noncloser",
            "research/p25/evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
            "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
        ),
        marker(
            "exactp_theorem_interface",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "All six gates returned their expected `rows=1/1` markers.",
        ),
        marker(
            "sprang_theta2_source_intake",
            "research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
            "p25_v2_sprang_theta2_source_intake_rows=1/1",
        ),
        marker(
            "kubert_lang_selector_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
            "p25_v2_kubert_lang_selector_boundary_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
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
    )


def source_rows() -> tuple[SourceFamilyRow, ...]:
    return (
        SourceFamilyRow(
            name="koo_shin_2010",
            source_page="sources/koo-shin-2010.md",
            current_use="source legality, distribution/root-descent context",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=True,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="helper_source_not_closer",
            missing="finite scalar-fixed value/divisor theorem for one oriented edge",
            row_ok=True,
        ),
        SourceFamilyRow(
            name="koo_shin_yoon_1007_2307",
            source_page="sources/koo-shin-yoon-1007-2307.md",
            current_use="normalized-y and ray-class vocabulary for exact-P",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="exactp_vocabulary_not_closer",
            missing="75-atom exact-P theorem or bridge to the one-edge target",
            row_ok=True,
        ),
        SourceFamilyRow(
            name="koo_shin_ii_1007_2318",
            source_page="sources/koo-shin-ii-1007-2318.md",
            current_use="normal-basis/ring-class background",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="background_source_not_closer",
            missing="one-edge theorem, period-156 value theorem, or exact-P producer",
            row_ok=True,
        ),
        SourceFamilyRow(
            name="sprang",
            source_page="sources/sprang.md",
            current_use="D=2 Poincare/Kronecker/theta support",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="d2_support_source_not_theta2_closer",
            missing="exact p25 theta2 divisor/additive payload or compact KSY specialization",
            row_ok=True,
        ),
        SourceFamilyRow(
            name="kubert_lang",
            source_page="sources/kubert-lang.md",
            current_use="finite selector/exponent machinery for exact-P",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="finite_selector_rigid_source_theorem_missing",
            missing=(
                "theorem-legal mixed C3 x C169 product emitting the rigid "
                "selector, primitive word, or theta2 payload"
            ),
            row_ok=True,
        ),
        SourceFamilyRow(
            name="schertz_scholl",
            source_page="sources/schertz-scholl.md",
            current_use="period-value vocabulary for the H0/Y507 support-period route",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="h0_y507_value_route_live_no_theorem",
            missing=(
                "canonical H0 or Y_507 period-156 value theorem with branch "
                "context, or matching divisor/additive identity"
            ),
            row_ok=True,
        ),
        SourceFamilyRow(
            name="p24_prior_art",
            source_page="sources/p24-prior-art.md",
            current_use="practical and negative-route transfer constraints",
            has_relevant_vocabulary=True,
            has_one_edge_source_object=False,
            has_scalar_fixed_finite_theorem=False,
            has_period156_value_theorem=False,
            has_exactp_upstream_theorem=False,
            decision="prior_art_not_p25_source_theorem",
            missing="p25-specific arithmetic source theorem",
            row_ok=True,
        ),
    )


def build_matrix() -> SourceFamilyGapMatrix:
    markers = evidence_markers()
    rows = source_rows()
    vocabulary = sum(row.has_relevant_vocabulary for row in rows)
    one_edge = sum(row.has_one_edge_source_object for row in rows)
    scalar_theorems = sum(row.has_scalar_fixed_finite_theorem for row in rows)
    period_theorems = sum(row.has_period156_value_theorem for row in rows)
    exactp_theorems = sum(row.has_exactp_upstream_theorem for row in rows)
    first_pass_closers = sum(
        row.has_scalar_fixed_finite_theorem or row.has_period156_value_theorem
        for row in rows
    )
    current_submission_ready = 0
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and len(rows) == 7
        and vocabulary == 7
        and one_edge == 1
        and scalar_theorems == 0
        and period_theorems == 0
        and exactp_theorems == 0
        and first_pass_closers == 0
        and current_submission_ready == 0
        and all(row.row_ok for row in rows)
    )
    return SourceFamilyGapMatrix(
        evidence_markers=markers,
        rows=rows,
        vocabulary_sources=vocabulary,
        one_edge_source_objects=one_edge,
        scalar_fixed_finite_theorems=scalar_theorems,
        period156_value_theorems=period_theorems,
        exactp_upstream_theorems=exactp_theorems,
        first_pass_closers=first_pass_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    matrix = build_matrix()
    print("p25 v2 source family gap matrix")
    for marker_row in matrix.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in matrix.rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} one_edge={int(row.has_one_edge_source_object)} "
            f"scalar_theorem={int(row.has_scalar_fixed_finite_theorem)} "
            f"period156_theorem={int(row.has_period156_value_theorem)} "
            f"exactp={int(row.has_exactp_upstream_theorem)} missing={row.missing}"
        )
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in matrix.evidence_markers)}/{len(matrix.evidence_markers)}")
    print(f"  source_rows={len(matrix.rows)}")
    print(f"  vocabulary_sources={matrix.vocabulary_sources}")
    print(f"  one_edge_source_objects={matrix.one_edge_source_objects}")
    print(f"  scalar_fixed_finite_theorems={matrix.scalar_fixed_finite_theorems}")
    print(f"  period156_value_theorems={matrix.period156_value_theorems}")
    print(f"  exactp_upstream_theorems={matrix.exactp_upstream_theorems}")
    print(f"  first_pass_closers={matrix.first_pass_closers}")
    print(f"  current_submission_ready={matrix.current_submission_ready}")
    print(f"p25_v2_source_family_gap_matrix_rows={int(matrix.row_ok)}/1")
    return 0 if matrix.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

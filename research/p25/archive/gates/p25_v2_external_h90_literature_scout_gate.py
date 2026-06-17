#!/usr/bin/env python3
"""Validate the narrow external H90 literature scout for p25."""

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
class LiteratureRow:
    name: str
    source_url: str
    has_h90_language: bool
    has_siegel_or_modular_unit_language: bool
    has_exact_level507_row: bool
    has_norm156_y507_boundary: bool
    has_scalar_fixed_finite_theorem: bool
    decision: str
    first_missing_or_falsifier: str
    row_ok: bool


@dataclass(frozen=True)
class LiteratureScout:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[LiteratureRow, ...]
    external_sources_screened: int
    superficially_relevant_sources: int
    exact_level507_rows: int
    norm156_y507_boundaries: int
    scalar_fixed_finite_theorems: int
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
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def literature_rows() -> tuple[LiteratureRow, ...]:
    return (
        LiteratureRow(
            name="shin_2605_25291_h90_quotient_maps",
            source_url="https://arxiv.org/abs/2605.25291",
            has_h90_language=True,
            has_siegel_or_modular_unit_language=False,
            has_exact_level507_row=False,
            has_norm156_y507_boundary=False,
            has_scalar_fixed_finite_theorem=False,
            decision="reject_different_h90_rational_map_setting",
            first_missing_or_falsifier=(
                "trace-zero rational quotient maps, not p25 Siegel/Yang "
                "support-156 rows"
            ),
            row_ok=True,
        ),
        LiteratureRow(
            name="folsom_modular_units_selberg",
            source_url="https://afolsom.people.amherst.edu/Folsom-ModUnitsSel-MRL.pdf",
            has_h90_language=False,
            has_siegel_or_modular_unit_language=True,
            has_exact_level507_row=False,
            has_norm156_y507_boundary=False,
            has_scalar_fixed_finite_theorem=False,
            decision="background_kubert_lang_modular_unit_vocabulary",
            first_missing_or_falsifier="no exact oriented p25 support-156 finite theorem",
            row_ok=True,
        ),
        LiteratureRow(
            name="kubert_lang_units_without_cm",
            source_url="https://www.numdam.org/item/CM_1980__41_1_127_0.pdf",
            has_h90_language=False,
            has_siegel_or_modular_unit_language=True,
            has_exact_level507_row=False,
            has_norm156_y507_boundary=False,
            has_scalar_fixed_finite_theorem=False,
            decision="background_distribution_relations_not_row_value",
            first_missing_or_falsifier="no scalar-fixed finite value/divisor theorem",
            row_ok=True,
        ),
        LiteratureRow(
            name="anticyclotomic_theta_functions",
            source_url="https://annals.math.princeton.edu/wp-content/uploads/annals-v163-n3-p02.pdf",
            has_h90_language=True,
            has_siegel_or_modular_unit_language=True,
            has_exact_level507_row=False,
            has_norm156_y507_boundary=False,
            has_scalar_fixed_finite_theorem=False,
            decision="background_cm_theta_siegel_context",
            first_missing_or_falsifier=(
                "CM anticyclotomic theta setting, not DANGER3 p25 finite row"
            ),
            row_ok=True,
        ),
        LiteratureRow(
            name="class_invariants_cyclotomic_unit_groups",
            source_url="https://jtnb.centre-mersenne.org/item/10.5802/jtnb.628.pdf",
            has_h90_language=False,
            has_siegel_or_modular_unit_language=True,
            has_exact_level507_row=False,
            has_norm156_y507_boundary=False,
            has_scalar_fixed_finite_theorem=False,
            decision="background_modular_unit_class_invariant_vocabulary",
            first_missing_or_falsifier="no p25 one-edge theorem or period-156 branch data",
            row_ok=True,
        ),
    )


def build_scout() -> LiteratureScout:
    markers = evidence_markers()
    rows = literature_rows()
    exact_rows = sum(row.has_exact_level507_row for row in rows)
    norm_boundaries = sum(row.has_norm156_y507_boundary for row in rows)
    scalar_fixed = sum(row.has_scalar_fixed_finite_theorem for row in rows)
    closers = sum(
        row.has_exact_level507_row
        and row.has_norm156_y507_boundary
        and row.has_scalar_fixed_finite_theorem
        for row in rows
    )
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 5
        and sum(row.has_h90_language or row.has_siegel_or_modular_unit_language for row in rows) == 5
        and exact_rows == 0
        and norm_boundaries == 0
        and scalar_fixed == 0
        and closers == 0
        and current_submission_ready == 0
        and all(row.row_ok for row in rows)
    )
    return LiteratureScout(
        evidence_markers=markers,
        rows=rows,
        external_sources_screened=len(rows),
        superficially_relevant_sources=sum(
            row.has_h90_language or row.has_siegel_or_modular_unit_language for row in rows
        ),
        exact_level507_rows=exact_rows,
        norm156_y507_boundaries=norm_boundaries,
        scalar_fixed_finite_theorems=scalar_fixed,
        first_pass_closers=closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    scout = build_scout()
    print("p25 v2 external H90 literature scout")
    for marker_row in scout.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("literature_rows")
    for row in scout.rows:
        print(
            f"  {row.name}: h90={int(row.has_h90_language)} "
            f"siegel={int(row.has_siegel_or_modular_unit_language)} "
            f"level507={int(row.has_exact_level507_row)} "
            f"norm156={int(row.has_norm156_y507_boundary)} "
            f"scalar_fixed={int(row.has_scalar_fixed_finite_theorem)} "
            f"decision={row.decision}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in scout.evidence_markers)}/{len(scout.evidence_markers)}")
    print(f"  external_sources_screened={scout.external_sources_screened}")
    print(f"  superficially_relevant_sources={scout.superficially_relevant_sources}")
    print(f"  exact_level507_rows={scout.exact_level507_rows}")
    print(f"  norm156_y507_boundaries={scout.norm156_y507_boundaries}")
    print(f"  scalar_fixed_finite_theorems={scout.scalar_fixed_finite_theorems}")
    print(f"  first_pass_closers={scout.first_pass_closers}")
    print(f"  current_submission_ready={scout.current_submission_ready}")
    print(f"p25_v2_external_h90_literature_scout_rows={1 if scout.row_ok else 0}/1")
    return 0 if scout.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

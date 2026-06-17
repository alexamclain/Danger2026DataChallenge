#!/usr/bin/env python3
"""Validate the row/quartic/power normalizer lookup-row status artifact."""

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
class StatusRow:
    name: str
    accepted_hook: str
    current_status: str
    first_falsifier: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "priority1_source_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "route_priority_falsifier_matrix",
        "evidence/p25_v2_route_priority_falsifier_matrix_20260617.md",
        "p25_v2_route_priority_falsifier_matrix_rows=1/1",
    ),
    (
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "positive_theorem_clause_matcher",
        "evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
        "p25_v2_positive_theorem_clause_matcher_rows=1/1",
    ),
    (
        "row_orientation_candidate_sweep",
        "evidence/p25_v2_row_orientation_candidate_sweep_20260617.md",
        "p25_v2_row_orientation_candidate_sweep_rows=1/1",
    ),
    (
        "orbit_tuple_theorem_router",
        "evidence/p25_v2_orbit_tuple_theorem_router_20260616.md",
        "p25_v2_orbit_tuple_theorem_router_rows=1/1",
    ),
    (
        "quartic_selector_candidate_sweep",
        "evidence/p25_v2_quartic_selector_candidate_sweep_20260617.md",
        "p25_v2_quartic_selector_candidate_sweep_rows=1/1",
    ),
    (
        "quartic_reciprocal_orientation",
        "evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
        "p25_v2_quartic_reciprocal_orientation_rows=1/1",
    ),
    (
        "power_normalized_theorem_intake",
        "evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
        "p25_v2_power_normalized_theorem_intake_rows=1/1",
    ),
    (
        "power_output_kind_router",
        "evidence/p25_v2_power_output_kind_router_20260616.md",
        "p25_v2_power_output_kind_router_rows=1/1",
    ),
    (
        "power_candidate_sweep",
        "evidence/p25_v2_power_candidate_sweep_20260617.md",
        "p25_v2_power_candidate_sweep_rows=1/1",
    ),
    (
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        text = read(root / rel)
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def status_rows() -> tuple[StatusRow, ...]:
    return (
        StatusRow(
            "single_or_row_labeled_theorem",
            "one normalized legal row, a doubling-equivalent row, or a row-labeled orbit theorem containing one legal row, plus scalar-fixed finite theorem data",
            "live_not_in_hand",
            "unordered orbit values, symmetric all-four product/norm, diagonal pair, row quotient, outside-orbit tuple, or all-four over-demand",
            "normalize_to_one_row_then_apply_source_snippet_intake",
        ),
        StatusRow(
            "reciprocal_orientation_normalizer",
            "reciprocal row with explicit -Norm_156(Y_507) boundary plus the same scalar-fixed theorem data",
            "normalizer_live_not_in_hand",
            "outside-doubling row with unspecified orientation, reciprocal row with positive boundary, or phase collision without boundary sign",
            "normalize_reciprocal_then_apply_source_snippet_intake",
        ),
        StatusRow(
            "quartic_character_normalizer",
            "exact row-antisymmetric C4_1 phase, mixed tensor row sign, orientation/boundary convention, arithmetic source theorem, and scalar-fixed finite theorem",
            "selector_live_finite_theorem_missing",
            "quartic sign, magnitude, quadratic aggregate, row sign only, C4 projection only, reciprocal phase without boundary sign, or Q split without root",
            "continue_only_with_exact_quartic_finite_theorem",
        ),
        StatusRow(
            "power_value_normalizer",
            "exact finite F_p theorem for R_m^e with e in {3,5,13,39,75,169,507} on one legal row, with inverse recovery and Norm_156(Y_507) boundary or accepted period-156 bridge",
            "power_value_live_not_in_hand",
            "power value without row selector, boundary bridge, source theorem, or scalar; ambiguous kernels; powered boundary-only data; Lane B D^3=Y quotient relation",
            "normalize_unique_power_value_then_apply_source_snippet_intake",
        ),
        StatusRow(
            "projector_or_square_root_normalizer",
            "selected square/fourth root or projector value that explicitly recovers one oriented row and then supplies the finite theorem data",
            "repair_until_selected_root_and_theorem",
            "two-edge, doubled-edge, four-edge projector components, row-square, Q split, or fourth-power data without selected root/scalar",
            "do_not_promote_without_selected_root_and_source_theorem",
        ),
        StatusRow(
            "source_family_prior_scan",
            "none in the inspected Koo-Shin/Sprang/Kubert-Lang/Schertz family summaries",
            "prior_art_negative",
            "source-family vocabulary, character language, projector language, or power templates without the exact finite theorem",
            "ask_narrow_normalizer_question_only",
        ),
    )


def evidence_consistency(root: Path) -> bool:
    row = read(root / "evidence/p25_v2_row_orientation_candidate_sweep_20260617.md")
    quartic = read(root / "evidence/p25_v2_quartic_selector_candidate_sweep_20260617.md")
    power = read(root / "evidence/p25_v2_power_candidate_sweep_20260617.md")
    matcher = read(root / "evidence/p25_v2_positive_theorem_clause_matcher_20260616.md")
    route = read(root / "evidence/p25_v2_route_priority_falsifier_matrix_20260617.md")
    return (
        "surviving_row_intake_families = 4" in row
        and "current_source_stage_closers = 0" in row
        and "surviving_quartic_intake_families = 3" in quartic
        and "current_source_stage_closers = 0" in quartic
        and "surviving_future_power_intakes = 1" in power
        and "current_source_stage_closers = 0" in power
        and "power_normalized_row_value_theorem" in matcher
        and "quartic_character_finite_theorem" in matcher
        and "first_pass_normalizers = 3" in route
        and "current_source_stage_closers = 0" in route
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[StatusRow, ...], bool]:
    markers = evidence_markers(root)
    rows = status_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and evidence_consistency(root)
        and len(rows) == 6
        and sum(row.current_status == "live_not_in_hand" for row in rows) == 1
        and sum("normalizer" in row.current_status for row in rows) == 1
        and sum("quartic" in row.name for row in rows) == 1
        and sum("power" in row.name for row in rows) == 1
        and sum("projector" in row.name for row in rows) == 1
        and sum(row.current_status == "prior_art_negative" for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 normalizer lookup-row status")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"evidence_consistency={int(evidence_consistency(root))}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    current_status={row.current_status}")
        print(f"    accepted_hook={row.accepted_hook}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"status_rows={len(rows)}")
    print("surviving_row_intake_families=4")
    print("surviving_quartic_intake_families=3")
    print("surviving_future_power_intakes=1")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_normalizer_lookup_row_status_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

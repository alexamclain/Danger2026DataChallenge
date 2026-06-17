#!/usr/bin/env python3
"""Validate the p25 route-priority and falsifier matrix.

This gate is intentionally lightweight: it does not recompute the row payloads.
It checks that the prioritization layer is backed by the promoted intake,
normalization, value, Q-support, exact-P, source-family, and end-to-end router
artifacts.
"""

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
class RouteRow:
    name: str
    priority: int
    class_name: str
    closer: str
    first_falsifier: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "minimal_expert_ask",
        "evidence/p25_v2_minimal_expert_ask_20260616.md",
        "p25_v2_minimal_expert_ask_rows=1/1",
    ),
    (
        "first_pass_expert_intake_packet",
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
    (
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "extended_unique_power_intake",
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    (
        "unified_value_divisor_interface",
        "evidence/p25_v2_unified_value_divisor_interface_20260616.md",
        "p25_v2_unified_value_divisor_interface_rows=1/1",
    ),
    (
        "period156_value_source_hook",
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    (
        "q_route_candidate_sweep",
        "evidence/p25_v2_q_route_candidate_sweep_20260617.md",
        "p25_v2_q_route_candidate_sweep_rows=1/1",
    ),
    (
        "exactp_candidate_sweep",
        "evidence/p25_v2_exactp_candidate_sweep_20260617.md",
        "p25_v2_exactp_candidate_sweep_rows=1/1",
    ),
    (
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    (
        "end_to_end_answer_router",
        "evidence/p25_v2_end_to_end_answer_router_20260616.md",
        "p25_v2_end_to_end_answer_router_rows=1/1",
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


def route_rows() -> tuple[RouteRow, ...]:
    return (
        RouteRow(
            "direct_scalar_fixed_divisor_additive",
            1,
            "first_pass_source_closer",
            "finite divisor/additive theorem for one normalized legal row",
            "source legality, boundary-only, selector-only, or unspecified scalar",
            "continue_as_preferred_ask",
        ),
        RouteRow(
            "support_period156_value",
            2,
            "first_pass_source_closer",
            "support-period-156 value theorem with branch/root/telescoping data",
            "ambient-period-780 value, mu11 quotient, or degree-6 value without Fp descent",
            "continue_as_value_side_ask",
        ),
        RouteRow(
            "power_normalized_row_value",
            3,
            "first_pass_normalizer",
            "exact source theorem for R_m^e, e in {3,5,13,39,75,169,507}, plus inverse recovery",
            "power value without row selector, boundary bridge, or arithmetic source theorem",
            "normalize_then_route_to_one_edge",
        ),
        RouteRow(
            "quartic_character_finite_theorem",
            4,
            "first_pass_normalizer",
            "exact C4_1 phase, mixed row sign, orientation, and scalar-fixed theorem",
            "selector-only, coarse phase, wrong reciprocal boundary, or missing finite theorem",
            "normalize_then_route_to_one_edge",
        ),
        RouteRow(
            "row_labeled_or_reciprocal_presentation",
            5,
            "first_pass_normalizer",
            "row-labeled orbit theorem or reciprocal-minus-boundary theorem containing one legal row",
            "unordered orbit, symmetric aggregate, reciprocal plus boundary, or outside-orbit row",
            "normalize_then_route_to_one_edge",
        ),
        RouteRow(
            "q_support_route",
            6,
            "support_not_front_door",
            "Q/Q3 theorem plus selector normalization, or Q diagonal plus split plus oriented root",
            "Q source-only, Q6 boundary-only, wrong support-12 split, split without oriented root",
            "continue_only_as_support_or_normalization",
        ),
        RouteRow(
            "exactp_upstream",
            7,
            "heavy_upstream",
            "compact C,D,K,orientation theorem, equal-weight 75 atoms, theta2 payload, or reverse theorem",
            "normalized-y vocabulary, finite packet without source, branchless orientation, or unified-only theorem",
            "continue_only_on_exact_theorem_hook",
        ),
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[RouteRow, ...], bool]:
    markers = evidence_markers(root)
    rows = route_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and len(rows) == 7
        and [row.priority for row in rows] == list(range(1, 8))
        and sum(row.class_name == "first_pass_source_closer" for row in rows) == 2
        and sum(row.class_name == "first_pass_normalizer" for row in rows) == 3
        and sum(row.class_name == "support_not_front_door" for row in rows) == 1
        and sum(row.class_name == "heavy_upstream" for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    markers, rows, row_ok = build_check(research_root())
    print("p25 v2 route-priority falsifier matrix")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print("routes")
    for row in rows:
        print(f"  {row.priority}. {row.name}: class={row.class_name}")
        print(f"     closer={row.closer}")
        print(f"     first_falsifier={row.first_falsifier}")
        print(f"     decision={row.decision}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"route_rows={len(rows)}")
    print(f"first_pass_source_closers={sum(row.class_name == 'first_pass_source_closer' for row in rows)}")
    print(f"first_pass_normalizers={sum(row.class_name == 'first_pass_normalizer' for row in rows)}")
    print(f"support_routes={sum(row.class_name == 'support_not_front_door' for row in rows)}")
    print(f"heavy_upstream_routes={sum(row.class_name == 'heavy_upstream' for row in rows)}")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_route_priority_falsifier_matrix_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

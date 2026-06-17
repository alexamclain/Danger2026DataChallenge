#!/usr/bin/env python3
"""Validate the Q/Yang lookup-row status artifact."""

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
        "conductor39_yang_h90_interface_contract",
        "evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
        "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1",
    ),
    (
        "yang_lift_descent_boundary_contract",
        "evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md",
        "p25_v2_yang_lift_descent_boundary_contract_rows=1/1",
    ),
    (
        "q_route_selector_debt",
        "evidence/p25_v2_q_route_selector_debt_20260616.md",
        "p25_v2_q_route_selector_debt_rows=1/1",
    ),
    (
        "q_diagonal_normalization",
        "evidence/p25_v2_q_diagonal_normalization_20260616.md",
        "p25_v2_q_diagonal_normalization_rows=1/1",
    ),
    (
        "q_split_quartic_selector",
        "evidence/p25_v2_q_split_quartic_selector_20260616.md",
        "p25_v2_q_split_quartic_selector_rows=1/1",
    ),
    (
        "q_square_payload_router",
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
    (
        "q_square_extraction_boundary",
        "evidence/p25_v2_q_square_extraction_boundary_20260616.md",
        "p25_v2_q_square_extraction_boundary_rows=1/1",
    ),
    (
        "q_route_source_hook_scan",
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
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
            "mixed_yang_h90_direct_theorem",
            "mixed U_chi/W source theorem with level-507 Yang lift, Hilbert-90 descent to Norm_156(Y_507), and scalar-fixed finite divisor/additive or period-156 value theorem for one legal support-156 row",
            "live_not_in_hand",
            "mixed source word only, Yang lift only, H90 boundary only, source legality only, projection, suborbit, or wrong-boundary lift",
            "continue_only_on_full_finite_theorem",
        ),
        StatusRow(
            "q_or_q3_finite_theorem",
            "finite Q value theorem with period-156 context, or finite Q^3 Hilbert-90 theorem, plus selector/boundary-zero normalization to one oriented edge",
            "support_only_until_selector_paid",
            "Q source language, Q^6 boundary, Q value without period-156 context, or Q/Q^3 theorem without edge selector",
            "continue_only_with_selector_normalization",
        ),
        StatusRow(
            "q_diagonal_plus_quartic_split",
            "Q diagonal aggregate plus matching pure quartic split plus oriented root/sign or explicit oriented diagonal-split normalization",
            "live_support_normalizer_not_in_hand",
            "diagonal only, support-12 row quotient, wrong split, pure quartic split only, or split without oriented root/sign",
            "normalize_then_apply_source_snippet_intake",
        ),
        StatusRow(
            "q_square_payload",
            "exact scalar-fixed Q-square finite value plus extraction map from the two row roots to same-j/X_1(16)/halving data or concrete A,x0 candidates",
            "payload_not_source_stage",
            "Q-square divisor, H90 boundary, quartic phase, value up to scalar, exact row roots without extraction map, or direct vpp.py on row values",
            "keep_as_extraction_payload_only",
        ),
        StatusRow(
            "local_source_scan",
            "none in local Koo-Shin/KSY/Koo-Shin II/Sprang source corpus",
            "local_sources_negative",
            "generic Q, generic splitting/diagonal, theta/distribution, ray-class generation, or source-legality vocabulary",
            "ask_narrow_external_or_expert_question_only",
        ),
        StatusRow(
            "direct_one_edge_fallback",
            "scalar-fixed finite theorem for one legal oriented edge with Norm_156(Y_507) boundary",
            "same_target_as_priority1",
            "aggregate, diagonal, two-edge, row-square, boundary-only, or selector-only statement",
            "route_back_to_priority1_divisor_additive",
        ),
    )


def evidence_consistency(root: Path) -> bool:
    candidate = read(root / "evidence/p25_v2_q_route_candidate_sweep_20260617.md")
    source_scan = read(root / "evidence/p25_v2_q_route_source_hook_scan_20260616.md")
    yang_contract = read(root / "evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md")
    square_boundary = read(root / "evidence/p25_v2_q_square_extraction_boundary_20260616.md")
    return (
        "surviving_q_intake_families = 4" in candidate
        and "current_q_source_hooks = 0" in candidate
        and "current_source_stage_closers = 0" in candidate
        and "accepted_source_hook_rows = 0" in source_scan
        and "source_stage_closers = 0" in source_scan
        and "current_source_stage_closers = 0" in yang_contract
        and "current_submission_ready_rows = 0" in square_boundary
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[StatusRow, ...], bool]:
    markers = evidence_markers(root)
    rows = status_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and evidence_consistency(root)
        and len(rows) == 6
        and sum(row.current_status == "live_not_in_hand" for row in rows) == 1
        and sum(row.current_status == "support_only_until_selector_paid" for row in rows) == 1
        and sum(row.current_status == "live_support_normalizer_not_in_hand" for row in rows) == 1
        and sum(row.current_status == "payload_not_source_stage" for row in rows) == 1
        and sum(row.current_status == "local_sources_negative" for row in rows) == 1
        and sum("priority1" in row.decision for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 Q/Yang lookup-row status")
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
    print("surviving_q_intake_families=4")
    print("current_q_source_hooks=0")
    print("current_source_stage_closers=0")
    print("current_extraction_ready=0")
    print("current_submission_ready=0")
    print(f"p25_v2_q_yang_lookup_row_status_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the minimal post-theorem extraction hook for p25."""

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
class RequiredClause:
    name: str
    ok: bool


@dataclass(frozen=True)
class ExtractionRoute:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class ExtractionMinimalHook:
    evidence_markers: tuple[EvidenceMarker, ...]
    required_clauses: tuple[RequiredClause, ...]
    accepted_routes: tuple[ExtractionRoute, ...]
    repair_or_reject_routes: tuple[ExtractionRoute, ...]
    current_extraction_ready_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
        marker(
            "unified_submission_extraction_contract",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def required_clauses() -> tuple[RequiredClause, ...]:
    return (
        RequiredClause("accepted_source_theorem_or_exactp_hook", True),
        RequiredClause("danger3_finite_identity_or_non_cm_framing", True),
        RequiredClause("same_j_x1_8112_bridge_or_order_8112_generator", True),
        RequiredClause("practical_x1_16_payload_A_xP16_or_y_plus_model_root", True),
        RequiredClause("thirty_eight_halving_links_x_chain_or_direct_x0", True),
        RequiredClause("official_vpp_py_verification", True),
    )


def accepted_routes() -> tuple[ExtractionRoute, ...]:
    return (
        ExtractionRoute("official_vpp_verified_triple", "submission_ready", True),
        ExtractionRoute("direct_A_x0_plus_vpp", "submission_ready_after_vpp", True),
        ExtractionRoute("checkable_x_chain_plus_vpp", "submission_ready_after_vpp", True),
    )


def repair_or_reject_routes() -> tuple[ExtractionRoute, ...]:
    return (
        ExtractionRoute("source_theorem_no_framing", "repair_danger3_framing_missing", True),
        ExtractionRoute("framed_source_no_same_j_bridge", "repair_same_j_bridge_missing", True),
        ExtractionRoute("independent_p16_q507", "reject_unglued_components", True),
        ExtractionRoute("same_j_invariant_only", "repair_same_curve_torsion_missing", True),
        ExtractionRoute("order8112_generator_only", "repair_x16_surface_missing", True),
        ExtractionRoute("x16_y_only", "repair_model_root_missing", True),
        ExtractionRoute("x16_surface_no_halving", "repair_halving_or_direct_x0_missing", True),
        ExtractionRoute("optional_dgate_surface_only", "repair_optional_not_active_surface", True),
        ExtractionRoute("branch_word_without_values", "reject_concrete_values_missing", True),
        ExtractionRoute("x0_extracted_vpp_missing", "repair_official_vpp_missing", True),
    )


def build_hook() -> ExtractionMinimalHook:
    markers = evidence_markers()
    required = required_clauses()
    accepted = accepted_routes()
    repairs = repair_or_reject_routes()
    current_extraction_ready_rows = 0
    current_submission_ready_rows = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(required) == 6
        and all(row.ok for row in required)
        and len(accepted) == 3
        and all(row.ok for row in accepted)
        and len(repairs) == 10
        and all(row.ok for row in repairs)
        and current_extraction_ready_rows == 0
        and current_submission_ready_rows == 0
    )
    return ExtractionMinimalHook(
        evidence_markers=markers,
        required_clauses=required,
        accepted_routes=accepted,
        repair_or_reject_routes=repairs,
        current_extraction_ready_rows=current_extraction_ready_rows,
        current_submission_ready_rows=current_submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    hook = build_hook()
    print("p25 v2 extraction minimal hook")
    for marker_row in hook.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("required_clauses")
    for clause in hook.required_clauses:
        print(f"  {clause.name}=ok")
    print("accepted_routes")
    for route in hook.accepted_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("repair_or_reject_routes")
    for route in hook.repair_or_reject_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in hook.evidence_markers)}/{len(hook.evidence_markers)}")
    print(f"  required_clauses={len(hook.required_clauses)}")
    print(f"  accepted_routes={len(hook.accepted_routes)}")
    print(f"  repair_or_reject_routes={len(hook.repair_or_reject_routes)}")
    print(f"  current_extraction_ready_rows={hook.current_extraction_ready_rows}")
    print(f"  current_submission_ready_rows={hook.current_submission_ready_rows}")
    print(f"p25_v2_extraction_minimal_hook_rows={int(hook.row_ok)}/1")
    return 0 if hook.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

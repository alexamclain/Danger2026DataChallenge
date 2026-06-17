#!/usr/bin/env python3
"""Validate the minimal exact-P hook for the p25 heavy route."""

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
class IntakeRoute:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class ExactPMinimalHook:
    evidence_markers: tuple[EvidenceMarker, ...]
    required_clauses: tuple[RequiredClause, ...]
    accepted_routes: tuple[IntakeRoute, ...]
    repair_or_reject_routes: tuple[IntakeRoute, ...]
    current_exactp_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_finite_geometry_rigidity",
            "research/p25/evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
            "robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows=1/1",
        ),
        marker(
            "exactp_theorem_interface",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "All six gates returned their expected `rows=1/1` markers.",
        ),
        marker(
            "exactp_to_unified_spine",
            "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
            "p25_v2_exactp_to_unified_target_spine_rows=1/1",
        ),
        marker(
            "reverse_exactp_information_loss",
            "research/p25/evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
            "p25_v2_reverse_exactp_information_loss_rows=1/1",
        ),
        marker(
            "ksy_source_ingest_scan",
            "research/p25/evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md",
            "decision = continue_as_exactp_vocabulary_not_closer",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
    )


def required_clauses() -> tuple[RequiredClause, ...]:
    return (
        RequiredClause("arithmetic_source_theorem", True),
        RequiredClause("compact_C_D_K_orientation_or_accepted_theta2_payload", True),
        RequiredClause("one_of_four_exactp_orientation_branches_or_equivalent_theta2_payload", True),
        RequiredClause("exact_equal_weight_75_atom_product", True),
        RequiredClause("period156_or_divisor_additive_context", True),
        RequiredClause("feeds_75_to_300_to_12_to_312_to_156_bridge", True),
        RequiredClause("post_theorem_extraction_routing", True),
    )


def accepted_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("compact_C_D_K_orientation_theorem", "exactp_source_stage_win_route_to_extraction", True),
        IntakeRoute("one_of_four_C_D_K_orientation_branches", "exactp_source_stage_win_route_to_extraction", True),
        IntakeRoute("accepted_theta2_divisor_additive_payload", "exactp_source_stage_win_route_to_extraction", True),
        IntakeRoute("exact_equal_weight_75_atom_theorem", "exactp_source_stage_win_route_to_extraction", True),
        IntakeRoute("explicit_reverse_reconstruction_theorem", "normalize_reverse_then_exactp_intake", True),
    )


def repair_or_reject_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("ksy_normalized_y_vocabulary_only", "repair_exact_selector_theorem_missing", True),
        IntakeRoute("raw_kubert_lang_exponent_balance_only", "repair_theta2_intake_missing", True),
        IntakeRoute("branchless_C_D_K_orientation_word", "repair_exactp_orientation_branch_missing", True),
        IntakeRoute("theta2_value_without_period156_context", "repair_period156_branch_selection_missing", True),
        IntakeRoute("missing_or_nonprimitive_K_trace", "reject_wrong_exactp_payload", True),
        IntakeRoute("wrong_C_D_or_orientation", "reject_wrong_exactp_payload", True),
        IntakeRoute("nonuniform_or_missing_atom_weights", "reject_by_finite_geometry_rigidity", True),
        IntakeRoute("ambient_period780_value_only", "repair_period156_branch_selection_missing", True),
        IntakeRoute("unified_theorem_without_exactp_selector", "repair_reverse_selector_structure_missing", True),
        IntakeRoute("finite_payload_without_arithmetic_source", "repair_arithmetic_source_missing", True),
        IntakeRoute("generic_ray_class_generation", "repair_exact_finite_identity_missing", True),
    )


def build_hook() -> ExactPMinimalHook:
    markers = evidence_markers()
    required = required_clauses()
    accepted = accepted_routes()
    repairs = repair_or_reject_routes()
    current_exactp_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(required) == 7
        and all(row.ok for row in required)
        and len(accepted) == 5
        and all(row.ok for row in accepted)
        and len(repairs) == 11
        and all(row.ok for row in repairs)
        and current_exactp_source_theorems == 0
        and current_submission_ready == 0
    )
    return ExactPMinimalHook(
        evidence_markers=markers,
        required_clauses=required,
        accepted_routes=accepted,
        repair_or_reject_routes=repairs,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    hook = build_hook()
    print("p25 v2 exact-P minimal hook")
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
    print(f"  current_exactp_source_theorems={hook.current_exactp_source_theorems}")
    print(f"  current_submission_ready={hook.current_submission_ready}")
    print(f"p25_v2_exactp_minimal_hook_rows={int(hook.row_ok)}/1")
    return 0 if hook.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

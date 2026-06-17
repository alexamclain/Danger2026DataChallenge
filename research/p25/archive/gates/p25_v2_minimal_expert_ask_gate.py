#!/usr/bin/env python3
"""Validate the minimal expert ask for the p25 one-edge theorem target."""

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
class RoutingRow:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class MinimalExpertAsk:
    evidence_markers: tuple[EvidenceMarker, ...]
    required_clauses: tuple[RequiredClause, ...]
    accepted_routes: tuple[RoutingRow, ...]
    repair_or_reject_routes: tuple[RoutingRow, ...]
    current_source_theorems: int
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
            "unified_theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
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
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "source_stage_normalization_spine",
            "research/p25/evidence/p25_v2_source_stage_normalization_spine_20260617.md",
            "p25_v2_source_stage_normalization_spine_rows=1/1",
        ),
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "extended_unique_power_intake",
            "research/p25/evidence/p25_v2_extended_unique_power_intake_20260617.md",
            "p25_v2_extended_unique_power_intake_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
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
        marker(
            "conductor39_norm_one_quotient_route",
            "research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
            "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
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
    )


def required_clauses() -> tuple[RequiredClause, ...]:
    return (
        RequiredClause("one_exact_oriented_edge_R_m", True),
        RequiredClause("exact_row_antisymmetric_C4_1_phase_or_direct_edge_payload", True),
        RequiredClause("oriented_row_data_or_boundary_sign_for_quartic_phase", True),
        RequiredClause("arithmetic_source_theorem", True),
        RequiredClause("hilbert90_boundary_Norm_156_Y_507", True),
        RequiredClause("scalar_fixed_finite_divisor_additive_or_period156_value", True),
        RequiredClause("compact_Q_route_has_period156_or_finite_Q3_theorem", True),
        RequiredClause("Q_route_has_diagonal_split_or_direct_edge_after_value_data", True),
        RequiredClause("Q_square_exact_value_requires_extraction_map_after_two_roots", True),
        RequiredClause("power_normalized_route_has_bijective_exponent_and_inverse_recovery", True),
        RequiredClause("post_theorem_extraction_routing", True),
    )


def accepted_routes() -> tuple[RoutingRow, ...]:
    return (
        RoutingRow(
            "scalar_fixed_divisor_additive_theorem",
            "source_stage_win_route_to_extraction_contract",
            True,
        ),
        RoutingRow(
            "period156_value_theorem_with_branch_context",
            "source_stage_win_route_to_extraction_contract",
            True,
        ),
        RoutingRow(
            "exactp_upstream_theorem_via_minimal_hook",
            "source_stage_win_route_to_extraction_contract",
            True,
        ),
        RoutingRow(
            "norm_one_Q_value_theorem_with_period156_context",
            "route_through_period156_value_source_hook",
            True,
        ),
        RoutingRow(
            "explicit_Q3_hilbert90_preimage_with_finite_theorem",
            "normalize_h90_preimage_then_apply_source_snippet_intake",
            True,
        ),
        RoutingRow(
            "Q_plus_explicit_oriented_diagonal_split",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            True,
        ),
        RoutingRow(
            "power_normalized_row_value_theorem",
            "normalize_unique_power_then_apply_source_snippet_intake",
            True,
        ),
    )


def repair_or_reject_routes() -> tuple[RoutingRow, ...]:
    return (
        RoutingRow("source_legality_only", "repair_finite_theorem_missing", True),
        RoutingRow("boundary_only", "repair_identity_for_one_edge_missing", True),
        RoutingRow("unspecified_fp_scalar", "repair_scalar_normalization_missing", True),
        RoutingRow("period780_or_mu11_only", "repair_period156_value_selection_missing", True),
        RoutingRow("degree6_value_without_fp_descent", "repair_fp_descent_missing", True),
        RoutingRow("nonunit_w_boundary_edge_combination", "repair_boundary_zero_content_missing", True),
        RoutingRow("aggregate_or_row_square_only", "repair_oriented_edge_selection_missing", True),
        RoutingRow("projector_values_without_fourth_root", "repair_mu4_root_selection_missing", True),
        RoutingRow("two_edge_pair_without_oriented_square_root", "repair_sign_or_root_missing", True),
        RoutingRow("exact_quartic_selector_without_finite_theorem", "repair_value_divisor_theorem_missing", True),
        RoutingRow("coarse_quartic_phase_or_magnitude_only", "repair_quartic_edge_selection_missing", True),
        RoutingRow("reciprocal_quartic_phase_without_boundary_sign", "repair_reciprocal_orientation_or_boundary_sign_missing", True),
        RoutingRow("reciprocal_quartic_phase_with_positive_boundary", "reject_orientation_boundary_mismatch", True),
        RoutingRow("exactp_vocabulary_without_75_atom_theorem", "repair_exactp_theorem_missing", True),
        RoutingRow("exactp_branchless_orientation_word", "repair_exactp_orientation_branch_missing", True),
        RoutingRow("exactp_theta2_without_period156_context", "repair_period156_branch_selection_missing", True),
        RoutingRow("wrong_exactp_packet", "reject_wrong_exactp_payload", True),
        RoutingRow("finite_payload_without_source", "repair_arithmetic_source_missing", True),
        RoutingRow("generic_cm_or_class_field_generation", "repair_danger3_finite_framing_missing", True),
        RoutingRow("coset_selector_or_Q_source_only", "repair_finite_value_divisor_theorem_missing", True),
        RoutingRow("Q_diagonal_value_only", "support_diagonal_aggregate_selector_missing", True),
        RoutingRow("Q_plus_row_quotient_without_root", "repair_oriented_square_root_missing", True),
        RoutingRow(
            "Q_square_exact_value_without_extraction_map",
            "repair_extraction_map_missing_after_two_root_row_payload",
            True,
        ),
        RoutingRow("Q_square_value_up_to_scalar", "repair_scalar_and_root_orientation_missing", True),
        RoutingRow(
            "Q_square_sign_from_divisor_h90_or_phase",
            "reject_sign_invisible_to_current_invariants",
            True,
        ),
        RoutingRow("Q_wrong_zero_boundary_split", "reject_zero_boundary_wrong_edge", True),
        RoutingRow("Q6_boundary_only", "repair_additive_or_value_normalization_missing", True),
        RoutingRow(
            "primitive_U_chi_power_only",
            "repair_yang_lift_descent_and_finite_theorem_missing",
            True,
        ),
        RoutingRow("pure_character_degree6_norm", "reject_pure_character_degree6_norm_cancels", True),
        RoutingRow("ambiguous_power_value_without_selector", "repair_power_root_selection_missing", True),
    )


def build_ask() -> MinimalExpertAsk:
    markers = evidence_markers()
    required = required_clauses()
    accepted = accepted_routes()
    near_misses = repair_or_reject_routes()
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(required) == 11
        and all(row.ok for row in required)
        and len(accepted) == 7
        and all(row.ok for row in accepted)
        and len(near_misses) == 30
        and all(row.ok for row in near_misses)
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return MinimalExpertAsk(
        evidence_markers=markers,
        required_clauses=required,
        accepted_routes=accepted,
        repair_or_reject_routes=near_misses,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    ask = build_ask()
    print("p25 v2 minimal expert ask")
    for marker_row in ask.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("required_clauses")
    for clause in ask.required_clauses:
        print(f"  {clause.name}=ok")
    print("accepted_routes")
    for route in ask.accepted_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("repair_or_reject_routes")
    for route in ask.repair_or_reject_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in ask.evidence_markers)}/{len(ask.evidence_markers)}")
    print(f"  required_clauses={len(ask.required_clauses)}")
    print(f"  accepted_routes={len(ask.accepted_routes)}")
    print(f"  repair_or_reject_routes={len(ask.repair_or_reject_routes)}")
    print(f"  current_source_theorems={ask.current_source_theorems}")
    print(f"  current_submission_ready={ask.current_submission_ready}")
    print(f"p25_v2_minimal_expert_ask_rows={int(ask.row_ok)}/1")
    return 0 if ask.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

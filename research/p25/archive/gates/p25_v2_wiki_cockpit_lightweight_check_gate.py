#!/usr/bin/env python3
"""Lightweight cockpit validation for the p25 v2 wiki.

This gate validates the v2 operating surface without replaying old heavy
search/reconstruction gates.  It should be the default wiki sanity check during
practical-search-first work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


CANONICAL_TOP_LEVEL = {
    "AGENTS.md",
    "archive",
    "concepts",
    "evidence",
    "frontier.md",
    "index.md",
    "lanes",
    "log.md",
    "operations",
    "sources",
}

CANONICAL_PAGES = (
    "lanes/practical-search.md",
    "lanes/h0.md",
    "lanes/conductor39.md",
    "lanes/exact-p.md",
    "lanes/twisted-h90.md",
    "lanes/curved-corner.md",
    "sources/p24-prior-art.md",
    "sources/koo-shin-2010.md",
    "sources/koo-shin-yoon-1007-2307.md",
    "sources/koo-shin-ii-1007-2318.md",
    "sources/sprang.md",
    "sources/kubert-lang.md",
    "sources/schertz-scholl.md",
    "concepts/transfer-matrix.md",
    "operations/run-status.md",
)

REQUIRED_SECTIONS = (
    "## Purpose",
    "## Current Claim",
    "## Decisive Evidence",
    "## Open Blockers",
    "## Next Reads",
    "## Linked Artifacts",
)

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_current_expert_response_rubric_20260616.md",
        "p25_v2_current_expert_response_rubric_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_snippet_expert_intake_sync_20260617.md",
        "p25_v2_snippet_expert_intake_sync_rows=1/1",
    ),
    (
        "evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
        "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_extraction_payload_contract_20260616.md",
        "p25_v2_extraction_payload_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_orbit_normalization_20260616.md",
        "p25_v2_row_orbit_normalization_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
        "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_orientation_candidate_sweep_20260617.md",
        "p25_v2_row_orientation_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_repair_debt_closure_matrix_20260617.md",
        "p25_v2_repair_debt_closure_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "evidence/p25_v2_route_priority_falsifier_matrix_20260617.md",
        "p25_v2_route_priority_falsifier_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_candidate_sweep_20260617.md",
        "p25_v2_priority1_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_packet_fixture_contract_20260617.md",
        "p25_v2_priority1_packet_fixture_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_clause_necessity_matrix_20260617.md",
        "p25_v2_priority1_clause_necessity_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_row_binding_overlay_20260617.md",
        "p25_v2_conductor39_row_binding_overlay_rows=1/1",
    ),
    (
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_kato_siegel_divisor_scout_20260617.md",
        "p25_v2_kato_siegel_divisor_scout_rows=1/1",
    ),
    (
        "evidence/p25_v2_fpstar_branch_factorization_20260617.md",
        "p25_v2_fpstar_branch_factorization_rows=1/1",
    ),
    (
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_koo_shin_priority1_toprow_falsifier_20260617.md",
        "p25_v2_koo_shin_priority1_toprow_falsifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_lookup_row_status_20260617.md",
        "p25_v2_period156_lookup_row_status_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_row_bridge_packet_20260617.md",
        "p25_v2_period156_row_bridge_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_feasibility_supersession_20260617.md",
        "p25_v2_period156_feasibility_supersession_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_value_branch_contract_20260616.md",
        "p25_v2_period156_value_branch_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_value_divisor_interface_20260616.md",
        "p25_v2_unified_value_divisor_interface_rows=1/1",
    ),
    (
        "evidence/p25_v2_value_divisor_source_family_router_20260616.md",
        "p25_v2_value_divisor_source_family_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_theorem_review_packet_20260616.md",
        "p25_v2_unified_theorem_review_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_group_ring_payload_20260616.md",
        "p25_v2_unified_group_ring_payload_rows=1/1",
    ),
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_graph_normal_form_20260616.md",
        "p25_v2_source_graph_normal_form_rows=1/1",
    ),
    (
        "evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
        "p25_v2_edge_lattice_intake_classifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_source_theorem_gap_20260616.md",
        "p25_v2_unified_source_theorem_gap_rows=1/1",
    ),
    (
        "evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
        "p25_v2_h0_conductor39_unified_target_rows=1/1",
    ),
    (
        "evidence/p25_v2_h0_theorem_interface_contract_20260616.md",
        "p25_v2_h0_theorem_interface_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
        "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md",
        "p25_v2_conductor39_doubling_orbit_minimality_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
        "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
    ),
    (
        "evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
        "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
    ),
    (
        "evidence/p25_v2_mod13_coset_rectangle_20260616.md",
        "p25_v2_mod13_coset_rectangle_rows=1/1",
    ),
    (
        "evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
        "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
    ),
    (
        "evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md",
        "p25_v2_minimal_h90_preimage_classifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_h90_support_lower_bound_20260616.md",
        "p25_v2_h90_support_lower_bound_rows=1/1",
    ),
    (
        "evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
        "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
    ),
    (
        "evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
        "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
    ),
    (
        "evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
        "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
        "p25_v2_row_quotient_invariant_bridge_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_square_root_ambiguity_20260616.md",
        "p25_v2_row_square_root_ambiguity_rows=1/1",
    ),
    (
        "evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
        "p25_v2_constant_normalization_ambiguity_rows=1/1",
    ),
    (
        "evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
        "p25_v2_norm_only_descent_ambiguity_rows=1/1",
    ),
    (
        "evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
        "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
    ),
    (
        "evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md",
        "p25_v2_yang_lift_descent_boundary_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_coefficient6_root_normalization_20260616.md",
        "p25_v2_coefficient6_root_normalization_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
        "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
        "p25_v2_power_normalized_theorem_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_output_kind_router_20260616.md",
        "p25_v2_power_output_kind_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_primitive_character_power_recheck_20260617.md",
        "p25_v2_primitive_character_power_recheck_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_candidate_sweep_20260617.md",
        "p25_v2_power_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_constructive_value_payload_contract_20260616.md",
        "p25_v2_constructive_value_payload_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_constructive_payload_source_scan_20260616.md",
        "p25_v2_constructive_payload_source_scan_rows=1/1",
    ),
    (
        "evidence/p25_v2_value_payload_reality_ledger_20260616.md",
        "p25_v2_value_payload_reality_ledger_rows=1/1",
    ),
    (
        "evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
        "p25_v2_additive_normalizer_source_scan_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_local_source_hook_coverage_audit_20260617.md",
        "p25_v2_local_source_hook_coverage_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_external_h90_literature_scout_20260616.md",
        "p25_v2_external_h90_literature_scout_rows=1/1",
    ),
    (
        "evidence/p25_v2_minimal_expert_ask_20260616.md",
        "p25_v2_minimal_expert_ask_rows=1/1",
    ),
    (
        "evidence/p25_v2_frontdoor_count_sync_20260616.md",
        "p25_v2_frontdoor_count_sync_rows=1/1",
    ),
    (
        "evidence/p25_v2_support_lane_router_20260616.md",
        "p25_v2_support_lane_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_edge_projector_denominator_20260616.md",
        "p25_v2_edge_projector_denominator_rows=1/1",
    ),
    (
        "evidence/p25_v2_partial_projector_selector_20260616.md",
        "p25_v2_partial_projector_selector_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_minimal_hook_20260616.md",
        "p25_v2_exactp_minimal_hook_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_candidate_sweep_20260617.md",
        "p25_v2_exactp_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_theta2_producer_obstruction_20260617.md",
        "p25_v2_exactp_theta2_producer_obstruction_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md",
        "p25_v2_exactp_75_anchor_bridge_filter_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_spine_payload_separation_20260617.md",
        "p25_v2_exactp_spine_payload_separation_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_primitive_word_source_split_20260617.md",
        "p25_v2_kl_primitive_word_source_split_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_source_split_local_scan_20260617.md",
        "p25_v2_kl_source_split_local_scan_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_cyclotomic_norm_route_audit_20260617.md",
        "p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_extraction_minimal_hook_20260616.md",
        "p25_v2_extraction_minimal_hook_rows=1/1",
    ),
    (
        "evidence/p25_v2_post_theorem_extraction_router_20260616.md",
        "p25_v2_post_theorem_extraction_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
        "p25_v2_unified_submission_extraction_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_candidate_packet_intake_reorg_20260616.md",
        "p25_v2_candidate_packet_intake_reorg_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_projector_extraction_boundary_20260616.md",
        "p25_v2_power_projector_extraction_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    (
        "evidence/p25_v2_period156_value_candidate_sweep_20260617.md",
        "p25_v2_period156_value_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_arithmetic_baseline_audit_20260616.md",
        "p25_v2_arithmetic_baseline_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_theta2_period156_support_contract_20260616.md",
        "p25_v2_theta2_period156_support_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
        "p25_v2_exactp_finite_geometry_rigidity_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
        "p25_v2_exactp_orientation_branch_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
        "p25_v2_exactp_to_unified_target_spine_rows=1/1",
    ),
    (
        "evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
        "p25_v2_reverse_exactp_information_loss_rows=1/1",
    ),
    (
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md",
        "p25_v2_sprang_distribution_instantiation_falsifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
        "p25_v2_kubert_lang_selector_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
        "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
        "p25_v2_h0_y507_period156_compatibility_rows=1/1",
    ),
    (
        "evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
        "p25_v2_positive_theorem_clause_matcher_rows=1/1",
    ),
    (
        "evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
        "p25_v2_edge_lattice_global_minimality_rows=1/1",
    ),
    (
        "evidence/p25_v2_distribution_relation_closure_screen_20260617.md",
        "p25_v2_distribution_relation_closure_screen_rows=1/1",
    ),
    (
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_zero_lattice_candidate_sweep_20260617.md",
        "p25_v2_zero_lattice_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    (
        "evidence/p25_v2_common_scalar_anchor_filter_20260617.md",
        "p25_v2_common_scalar_anchor_filter_rows=1/1",
    ),
    (
        "evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md",
        "p25_v2_basis_sensitive_anchor_sieve_rows=1/1",
    ),
    (
        "evidence/p25_v2_affine_row_product_classifier_20260617.md",
        "p25_v2_affine_row_product_classifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_affine_row_normal_form_20260617.md",
        "p25_v2_affine_row_normal_form_rows=1/1",
    ),
    (
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_matched_quotient_source_feasibility_20260617.md",
        "p25_v2_matched_quotient_source_feasibility_rows=1/1",
    ),
    (
        "evidence/p25_v2_matched_quotient_burden_audit_20260617.md",
        "p25_v2_matched_quotient_burden_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_matched_zero_lattice_target_audit_20260617.md",
        "p25_v2_matched_zero_lattice_target_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
        "p25_v2_source_theorem_acceptance_automaton_rows=1/1",
    ),
    (
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_kernel_consistency_audit_20260617.md",
        "p25_v2_kernel_consistency_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_extended_power_source_coverage_addendum_20260617.md",
        "p25_v2_extended_power_source_coverage_addendum_rows=1/1",
    ),
    (
        "evidence/p25_v2_general_unit_power_intake_20260617.md",
        "p25_v2_general_unit_power_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_external_source_delta_20260617.md",
        "p25_v2_external_source_delta_20260617_rows=1/1",
    ),
    (
        "evidence/p25_v2_orphan_evidence_supersession_audit_20260617.md",
        "p25_v2_orphan_evidence_supersession_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_expert_handoff_supersession_20260617.md",
        "p25_v2_expert_handoff_supersession_rows=1/1",
    ),
    (
        "evidence/p25_v2_orbit_tuple_theorem_router_20260616.md",
        "p25_v2_orbit_tuple_theorem_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_k22_automorphism_quotient_falsifier_20260616.md",
        "p25_v2_k22_automorphism_quotient_falsifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_c4_character_spectrum_20260616.md",
        "p25_v2_c4_character_spectrum_rows=1/1",
    ),
    (
        "evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md",
        "p25_v2_row_sign_c4_tensor_spectrum_rows=1/1",
    ),
    (
        "evidence/p25_v2_frobenius_tensor_eigenboundary_20260616.md",
        "p25_v2_frobenius_tensor_eigenboundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_quartic_selector_payload_20260616.md",
        "p25_v2_quartic_selector_payload_rows=1/1",
    ),
    (
        "evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
        "p25_v2_quartic_reciprocal_orientation_rows=1/1",
    ),
    (
        "evidence/p25_v2_quartic_selector_candidate_sweep_20260617.md",
        "p25_v2_quartic_selector_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_route_selector_debt_20260616.md",
        "p25_v2_q_route_selector_debt_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_diagonal_normalization_20260616.md",
        "p25_v2_q_diagonal_normalization_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_split_quotient_complexity_20260616.md",
        "p25_v2_q_split_quotient_complexity_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_split_quartic_selector_20260616.md",
        "p25_v2_q_split_quartic_selector_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_square_extraction_boundary_20260616.md",
        "p25_v2_q_square_extraction_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_route_candidate_sweep_20260617.md",
        "p25_v2_q_route_candidate_sweep_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_yang_lookup_row_status_20260617.md",
        "p25_v2_q_yang_lookup_row_status_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_yang_row_bridge_packet_20260617.md",
        "p25_v2_q_yang_row_bridge_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_q_route_consistency_audit_20260617.md",
        "p25_v2_q_route_consistency_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_normalizer_lookup_row_status_20260617.md",
        "p25_v2_normalizer_lookup_row_status_rows=1/1",
    ),
    (
        "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
        "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_koo_shin_access_blocker_closure_20260616.md",
        "p25_v2_koo_shin_access_blocker_closure_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_closure_template_replay_boundary_20260616.md",
        "p25_v2_exactp_closure_template_replay_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_mccarthy_endpoint_stability_router_20260617.md",
        "p25_v2_mccarthy_endpoint_stability_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_support_microscope_router_20260617.md",
        "p25_v2_support_microscope_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_support_lane_status_demotion_20260616.md",
        "p25_v2_support_lane_status_demotion_rows=1/1",
    ),
    (
        "evidence/p25_v2_end_to_end_answer_router_20260616.md",
        "p25_v2_end_to_end_answer_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md",
        "p25_v2_first_class_run_v2_plan_guard_rows=1/1",
    ),
    (
        "evidence/p25_v2_cockpit_gate_manifest_20260616.md",
        "p25_v2_cockpit_gate_manifest_rows=1/1",
    ),
)

HEAVY_RECOMPUTATION_GATES = (
    "archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py",
    "archive/gates/p25_v2_h0_conductor39_unified_target_gate.py",
)


@dataclass(frozen=True)
class WikiCockpitCheck:
    top_level_ok: bool
    canonical_pages_present: int
    canonical_pages_total: int
    frontmatter_ok: int
    section_contract_ok: int
    index_links_ok: int
    evidence_markers_ok: int
    evidence_markers_total: int
    frontier_mentions_live_run: bool
    frontier_mentions_first_pass: bool
    frontier_mentions_zero_submission: bool
    heavy_gates_documented: bool
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def has_frontmatter_contract(text: str, expected_type: str) -> bool:
    lines = text.splitlines()
    required = {
        f"type: {expected_type}",
        "canonical: true",
        "owner: llm",
    }
    return (
        len(lines) >= 7
        and lines[0] == "---"
        and lines[6] == "---"
        and required <= set(lines[:7])
        and any(re.fullmatch(r"updated: \d{4}-\d{2}-\d{2}", line) for line in lines[:7])
    )


def page_type(path: str) -> str:
    if path.startswith("lanes/"):
        return "lane"
    if path.startswith("sources/"):
        return "source"
    if path.startswith("concepts/"):
        return "concept"
    return "operations"


def build_check(root: Path) -> WikiCockpitCheck:
    observed_top = {p.name for p in root.iterdir()}
    top_level_ok = observed_top == CANONICAL_TOP_LEVEL

    index_text = (root / "index.md").read_text()
    canonical_present = 0
    frontmatter_ok = 0
    section_ok = 0
    index_links_ok = 0
    for rel in CANONICAL_PAGES:
        path = root / rel
        if path.exists():
            canonical_present += 1
            text = path.read_text()
            frontmatter_ok += int(has_frontmatter_contract(text, page_type(rel)))
            section_ok += int(all(section in text for section in REQUIRED_SECTIONS))
        index_links_ok += int(f"({rel})" in index_text)

    evidence_ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        evidence_ok += int(path.exists() and marker in path.read_text())

    frontier_text = (root / "frontier.md").read_text()
    agents_text = (root / "AGENTS.md").read_text()
    heavy_documented = all(name in agents_text for name in HEAVY_RECOMPUTATION_GATES)

    row_ok = (
        top_level_ok
        and canonical_present == len(CANONICAL_PAGES)
        and frontmatter_ok == len(CANONICAL_PAGES)
        and section_ok == len(CANONICAL_PAGES)
        and index_links_ok == len(CANONICAL_PAGES)
        and evidence_ok == len(EVIDENCE_MARKERS)
        and "10-worker `x16halvenonsplit`" in frontier_text
        and "H0" in frontier_text
        and "Conductor 39" in frontier_text
        and "No `vpp.py`-verified p25 triple exists yet." in frontier_text
        and heavy_documented
    )

    return WikiCockpitCheck(
        top_level_ok=top_level_ok,
        canonical_pages_present=canonical_present,
        canonical_pages_total=len(CANONICAL_PAGES),
        frontmatter_ok=frontmatter_ok,
        section_contract_ok=section_ok,
        index_links_ok=index_links_ok,
        evidence_markers_ok=evidence_ok,
        evidence_markers_total=len(EVIDENCE_MARKERS),
        frontier_mentions_live_run="10-worker `x16halvenonsplit`" in frontier_text,
        frontier_mentions_first_pass=("H0" in frontier_text and "Conductor 39" in frontier_text),
        frontier_mentions_zero_submission="No `vpp.py`-verified p25 triple exists yet." in frontier_text,
        heavy_gates_documented=heavy_documented,
        row_ok=row_ok,
    )


def main() -> int:
    root = research_root()
    check = build_check(root)
    print("p25 v2 wiki cockpit lightweight check")
    print(f"top_level_ok={int(check.top_level_ok)}")
    print(f"canonical_pages={check.canonical_pages_present}/{check.canonical_pages_total}")
    print(f"frontmatter_ok={check.frontmatter_ok}/{check.canonical_pages_total}")
    print(f"section_contract_ok={check.section_contract_ok}/{check.canonical_pages_total}")
    print(f"index_links_ok={check.index_links_ok}/{check.canonical_pages_total}")
    print(f"evidence_markers_ok={check.evidence_markers_ok}/{check.evidence_markers_total}")
    print(f"frontier_mentions_live_run={int(check.frontier_mentions_live_run)}")
    print(f"frontier_mentions_first_pass={int(check.frontier_mentions_first_pass)}")
    print(f"frontier_mentions_zero_submission={int(check.frontier_mentions_zero_submission)}")
    print(f"heavy_gates_documented={int(check.heavy_gates_documented)}")
    print(f"p25_v2_wiki_cockpit_lightweight_check_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

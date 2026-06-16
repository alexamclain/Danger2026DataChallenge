#!/usr/bin/env python3
"""Degree and verifier accounting for current p24 certificate routes."""

from __future__ import annotations

from math import comb, isqrt, lgamma, log

import sympy as sp


def main() -> None:
    p = 10**24 + 7
    sqrt_p = isqrt(p)
    m = 66254
    n = 3107441
    first_trace_h = 278733727154
    first_trace_quotient_degree = 19
    first_trace_recovery_degree = first_trace_h // first_trace_quotient_degree
    first_trace_payload_slots = first_trace_quotient_degree + first_trace_recovery_degree
    components = [2, 157, 211]
    phase_top_slots = components[0]
    phase_first_refinement_slots = components[0] * components[1]
    phase_second_refinement_slots = m
    phase_selected_recovery_slots = n
    phase_total_slots = (
        phase_top_slots
        + phase_first_refinement_slots
        + phase_second_refinement_slots
        + phase_selected_recovery_slots
    )
    selected_chain_slots = 2 + 157 + 211 + n
    right = 211
    left = 157
    left_dim = left - 1
    right_order = sp.n_order(p % right, right)
    packet_degree = sp.n_order(p % n, n)
    trace_tail = 16
    trace_right_orbit = right_order
    l1_axis_dim = 1 + (2 - 1) + (157 - 1) + (211 - 1)
    l1_partial_degrees = [n * c for c in components]
    l1_total_visible = n + sum(l1_partial_degrees)
    trace_plucker_terms = comb(trace_right_orbit, trace_tail)
    ord_m = sp.n_order(p % m, m)
    tensor_factor_count = sp.igcd(packet_degree, ord_m)
    tensor_factor_degree = packet_degree // tensor_factor_count
    e_frobenius_order = sp.n_order(pow(p, ord_m, n), n)
    e_frobenius_orbit_count = (n - 1) // e_frobenius_order
    trace_frame_subdegree = 179
    trace_frame_blocks = 3
    trace_frame_target_dim = trace_frame_subdegree * trace_frame_blocks
    trace_frame_leading_full_blocks = l1_axis_dim // trace_frame_subdegree
    trace_frame_leading_tail = l1_axis_dim % trace_frame_subdegree
    trace_frame_A_dim = 1 + (2 - 1) + (157 - 1)
    trace_frame_B_dim = 211 - 1
    trace_frame_prefix_target = 2 * trace_frame_subdegree
    trace_frame_intersection_dim = trace_frame_A_dim + trace_frame_B_dim - trace_frame_prefix_target
    schubert_matrix_entries_per_packet = (
        trace_frame_A_dim * trace_frame_A_dim
        + trace_frame_B_dim * trace_frame_B_dim
        + (trace_frame_B_dim - trace_frame_intersection_dim) ** 2
        + trace_frame_intersection_dim * trace_frame_intersection_dim
    )
    leading_matrix_entries_per_packet = l1_axis_dim * l1_axis_dim
    leading_symbol_entries_per_packet = m
    leading_all_packets_e_entries = (
        ((n - 1) // packet_degree) * leading_matrix_entries_per_packet
    )
    leading_symbol_all_packets_e_entries = (
        ((n - 1) // packet_degree) * leading_symbol_entries_per_packet
    )
    leading_all_packets_fp_slots = leading_all_packets_e_entries * ord_m
    leading_symbol_all_packets_fp_slots = (
        leading_symbol_all_packets_e_entries * ord_m
    )
    leading_all_factors_fp_slots = leading_all_packets_fp_slots * tensor_factor_count
    leading_symbol_all_factors_fp_slots = (
        leading_symbol_all_packets_fp_slots * tensor_factor_count
    )
    leading_literal_orbit_symbol_e_entries = m * e_frobenius_order
    leading_literal_orbit_symbol_fp_slots = (
        leading_literal_orbit_symbol_e_entries * ord_m
    )
    leading_literal_all_orbit_symbol_fp_slots = (
        leading_literal_orbit_symbol_fp_slots * e_frobenius_orbit_count
    )
    leading_literal_beta_inverse_e_entries = n * e_frobenius_order
    leading_literal_beta_inverse_fp_slots = (
        leading_literal_beta_inverse_e_entries * ord_m
    )
    leading_literal_beta_inverse_all_factor_fp_slots = (
        leading_literal_beta_inverse_fp_slots * tensor_factor_count
    )
    leading_norm_values_with_inverses_fp_slots = (
        2 * e_frobenius_orbit_count * ord_m
    )
    leading_relative_degree8_values_with_inverses_fp_slots = (
        2 * tensor_factor_count * ord_m
    )
    leading_symmetric_degree8_values_with_inverses_fp_slots = 2 * ord_m
    schubert_all_packets_e_entries = ((n - 1) // packet_degree) * schubert_matrix_entries_per_packet
    schubert_all_packets_fp_slots = schubert_all_packets_e_entries * ord_m
    schubert_all_factors_fp_slots = schubert_all_packets_fp_slots * tensor_factor_count
    trace_frame_plucker_log10 = (
        lgamma(trace_frame_target_dim + 1)
        - lgamma(l1_axis_dim + 1)
        - lgamma(trace_frame_target_dim - l1_axis_dim + 1)
    ) / log(10)
    centered_profile_rows = 156
    centered_profile_cols = 210
    centered_profile_matrix_entries = centered_profile_rows * centered_profile_cols
    centered_profile_leading_minor_entries = centered_profile_rows * centered_profile_rows
    centered_profile_explicit_rank_witness_entries = (
        centered_profile_matrix_entries + centered_profile_leading_minor_entries
    )
    centered_profile_scalar_payload = 2
    centered_profile_pointwise_right_payload = 2 * 211
    centered_profile_orbit_norm_payload = 2 * 7

    print("p24 certificate route accounting")
    print(f"p={p}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"h={m*n}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"formal_m_plus_n={m+n}")
    print(f"formal_m_plus_n_over_sqrt={((m+n)/sqrt_p):.12e}")
    print()
    print("trace_gcd_right_resultant")
    print(f"  right={right}")
    print(f"  ord_right_p={right_order}")
    print(f"  tail_window={trace_tail}")
    print(f"  finite_value_count={right}")
    print(f"  orbit_product_count=7")
    print(f"  generic_plucker_terms=binom({trace_right_orbit},{trace_tail})={trace_plucker_terms}")
    print(f"  generic_exterior_support=211")
    print(f"  verifier_values_over_sqrt={(right/sqrt_p):.12e}")
    print()
    print("l1_partial_moment_resultant")
    print(f"  packet_degree=ord_n_p={packet_degree}")
    print(f"  axis_dim={l1_axis_dim}")
    print(f"  components={components}")
    print(f"  partial_degrees={l1_partial_degrees}")
    print(f"  visible_degree_n_plus_partials={l1_total_visible}")
    print(f"  visible_degree_over_sqrt={(l1_total_visible/sqrt_p):.12e}")
    print(f"  packet_degree_over_axis_dim={packet_degree/l1_axis_dim:.3f}")
    print()
    print("l1_trace_frame_selected_plucker")
    print(f"  E_degree=ord_m_p={ord_m}")
    print(f"  tensor_factor_count_over_E={tensor_factor_count}")
    print(f"  tensor_factor_degree_over_E={tensor_factor_degree}")
    print(f"  E_frobenius_orbit_size_on_H={e_frobenius_order}")
    print(f"  E_frobenius_nonzero_orbit_count_on_H={e_frobenius_orbit_count}")
    print(f"  beta_orbit_count_equals_H_packets_times_tensor_factors={int(e_frobenius_orbit_count == ((n - 1) // packet_degree) * tensor_factor_count)}")
    print(f"  trace_frame_target_dim=3*179={trace_frame_target_dim}")
    print(f"  axis_dim={l1_axis_dim}")
    print(f"  leading_prefix_coordinate={trace_frame_leading_full_blocks}*179+{trace_frame_leading_tail}")
    print(f"  log10_plucker_coordinates=log10(binomial({trace_frame_target_dim},{l1_axis_dim}))={trace_frame_plucker_log10:.6f}")
    print(f"  h_packet_count={(n-1)//packet_degree}")
    print("  finite_certificate_shape=leading_prefix_Plucker_coordinate_per_H_packet")
    print("  proof_target=selected_origin_Norm_E_over_Fp(delta_lead) != 0")
    print("  stronger_target=beta_product_or_eight_packet_product")
    print("  single_leading_matrix_surface")
    print(f"    matrix_entries_over_E_per_H_packet={leading_matrix_entries_per_packet}")
    print(f"    one_factor_all_H_packets_E_entries={leading_all_packets_e_entries}")
    print(f"    one_factor_all_H_packets_Fp_slots={leading_all_packets_fp_slots}")
    print(f"    one_factor_all_H_packets_Fp_slots_over_sqrt={(leading_all_packets_fp_slots/sqrt_p):.12e}")
    print(f"    all_70_factors_Fp_slots_over_sqrt={(leading_all_factors_fp_slots/sqrt_p):.12e}")
    print("  selected_toeplitz_symbol_surface")
    print(f"    symbol_entries_over_E_per_H_packet={leading_symbol_entries_per_packet}")
    print(f"    one_factor_all_H_packets_E_entries={leading_symbol_all_packets_e_entries}")
    print(f"    one_factor_all_H_packets_Fp_slots={leading_symbol_all_packets_fp_slots}")
    print(f"    one_factor_all_H_packets_Fp_slots_over_sqrt={(leading_symbol_all_packets_fp_slots/sqrt_p):.12e}")
    print(f"    all_70_factors_Fp_slots_over_sqrt={(leading_symbol_all_factors_fp_slots/sqrt_p):.12e}")
    print("  literal_beta_orbit_symbol_boundary")
    print(f"    symbol_entries_over_E_per_nonzero_beta_orbit={leading_literal_orbit_symbol_e_entries}")
    print(f"    Fp_slots_per_nonzero_beta_orbit_over_sqrt={(leading_literal_orbit_symbol_fp_slots/sqrt_p):.12e}")
    print(f"    all_nonzero_beta_orbits_Fp_slots_over_sqrt={(leading_literal_all_orbit_symbol_fp_slots/sqrt_p):.12e}")
    print("  literal_full_beta_inverse_boundary")
    print(f"    inverse_entries_over_E_one_beta_algebra={leading_literal_beta_inverse_e_entries}")
    print(f"    inverse_Fp_slots_one_beta_algebra_over_sqrt={(leading_literal_beta_inverse_fp_slots/sqrt_p):.12e}")
    print(f"    inverse_Fp_slots_times_70_over_sqrt={(leading_literal_beta_inverse_all_factor_fp_slots/sqrt_p):.12e}")
    print("  norm_compressed_beta_surface")
    print(f"    all_nonzero_norm_values_plus_inverses_Fp_slots_over_sqrt={(leading_norm_values_with_inverses_fp_slots/sqrt_p):.12e}")
    print(f"    degree8_relative_values_plus_inverses_without_symmetry_Fp_slots_over_sqrt={(leading_relative_degree8_values_with_inverses_fp_slots/sqrt_p):.12e}")
    print(f"    degree8_relative_values_plus_inverses_with_symmetry_Fp_slots_over_sqrt={(leading_symmetric_degree8_values_with_inverses_fp_slots/sqrt_p):.12e}")
    print("  factorized_schubert_surface")
    print(f"    A_dim=constant+2+157={trace_frame_A_dim}")
    print(f"    B_dim=211={trace_frame_B_dim}")
    print(f"    prefix_target=2*179={trace_frame_prefix_target}")
    print(f"    forced_intersection_dim={trace_frame_intersection_dim}")
    print(f"    matrix_entries_over_E_per_H_packet={schubert_matrix_entries_per_packet}")
    print(f"    one_factor_all_H_packets_Fp_slots={schubert_all_packets_fp_slots}")
    print(f"    one_factor_all_H_packets_Fp_slots_over_sqrt={(schubert_all_packets_fp_slots/sqrt_p):.12e}")
    print(f"    all_70_factors_Fp_slots_over_sqrt={(schubert_all_factors_fp_slots/sqrt_p):.12e}")
    print()
    print("first_trace_order19_quotient")
    print("  trace=1020608380936")
    print(f"  h={first_trace_h}")
    print(f"  quotient_degree={first_trace_quotient_degree}")
    print(f"  recovery_degree={first_trace_recovery_degree}")
    print(f"  payload_slots={first_trace_payload_slots}")
    print(f"  payload_slots_over_sqrt={(first_trace_payload_slots/sqrt_p):.12e}")
    print("  finite_certificate_shape=degree19_quotient_plus_selected_recovery")
    print("  proof_target=embedded_order19_quotient_phase_and_selected_recovery")
    print()
    print("centered_difference_minor")
    print(f"  base_matrix_rows={left_dim}")
    print(f"  base_matrix_cols={right-1}")
    print(f"  leading_minor_size={left_dim}")
    print(f"  origin_product_right_values={right}")
    print(f"  determinant_entries={left_dim*left_dim}")
    print(f"  entries_over_sqrt={(left_dim*left_dim/sqrt_p):.12e}")
    print("  centered_profile_payloads")
    print(f"    matrix_entries={centered_profile_matrix_entries}")
    print(f"    leading_minor_entries={centered_profile_leading_minor_entries}")
    print(f"    explicit_matrix_plus_rank_witness_entries={centered_profile_explicit_rank_witness_entries}")
    print(f"    explicit_matrix_plus_rank_witness_over_sqrt={(centered_profile_explicit_rank_witness_entries/sqrt_p):.12e}")
    print(f"    determinant_scalar_plus_inverse={centered_profile_scalar_payload}")
    print(f"    pointwise_right_product_values_plus_inverses={centered_profile_pointwise_right_payload}")
    print(f"    orbit_norm_values_plus_inverses={centered_profile_orbit_norm_payload}")
    print()
    print("phase_lifted_decomposed_tower")
    print(f"  top_slots={phase_top_slots}")
    print(f"  first_refinement_slots=2*157={phase_first_refinement_slots}")
    print(f"  second_refinement_slots=314*211={phase_second_refinement_slots}")
    print(f"  selected_recovery_slots={phase_selected_recovery_slots}")
    print(f"  total_slots={phase_total_slots}")
    print(f"  total_slots_over_sqrt={(phase_total_slots/sqrt_p):.12e}")
    print(f"  selected_chain_slots={selected_chain_slots}")
    print(f"  selected_chain_slots_over_sqrt={(selected_chain_slots/sqrt_p):.12e}")
    print(f"  overhead_over_formal_m_plus_n={phase_total_slots - (m+n)}")
    print("  finite_certificate_shape=top_root_plus_two_relative_phase_relations_plus_selected_recovery")
    print("  selected_chain_shape=top_root_plus_two_specialized_child_polynomials_plus_selected_recovery")
    print("  proof_target=embedded_relative_phase_and_selected_recovery_producer")
    print()
    print("interpretation")
    print("  trace_gcd_has_smallest_finite_verifier_but_hardest_embedded_producer=1")
    print("  l1_has_best_visible_tower_construction_but_selected_origin_punit_gap=1")
    print("  trace_frame_plucker_is_smallest_current_l1_axis_verifier_surface=1")
    print("  first_trace_order19_is_cleanest_single_layer_theorem_lab=1")
    print("  centered_minor_is_clean_base_field_sufficient_certificate_but_no_producer=1")
    print("  phase_lifted_tower_is_cleanest_j_producer_artifact_if_the_embedded_phase_theorem_is_found=1")
    print("conclusion=reported_p24_certificate_route_accounting")


if __name__ == "__main__":
    main()

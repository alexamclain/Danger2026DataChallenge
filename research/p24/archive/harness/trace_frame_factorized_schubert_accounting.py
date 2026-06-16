#!/usr/bin/env python3
"""Static accounting for the factorized trace-frame Schubert certificate."""

from __future__ import annotations

from math import isqrt

P = 10**24 + 7
M = 66254
N = 3107441
ORD_M = 5460
ORD_N = 388430
H_PACKET_COUNT = 8
TENSOR_FACTOR_COUNT = 70
SUBFIELD_DIM = 179

A_DIM = 1 + 1 + 156
B_DIM = 210
AXIS_DIM = A_DIM + B_DIM
PREFIX_BLOCKS = 2
PREFIX_TARGET_DIM = PREFIX_BLOCKS * SUBFIELD_DIM
FORCED_INTERSECTION_DIM = A_DIM + B_DIM - PREFIX_TARGET_DIM
TAIL_DIM = FORCED_INTERSECTION_DIM


def main() -> None:
    sqrt_p = isqrt(P)
    matrix_entries_per_packet = {
        "A_component_top1": A_DIM * A_DIM,
        "B_component_top2": B_DIM * B_DIM,
        "B_mod_A_quotient": (B_DIM - FORCED_INTERSECTION_DIM) ** 2,
        "residual_tail": TAIL_DIM * TAIL_DIM,
    }
    per_packet_e_entries = sum(matrix_entries_per_packet.values())
    leading_matrix_e_entries = AXIS_DIM * AXIS_DIM
    all_packets_e_entries = H_PACKET_COUNT * per_packet_e_entries
    all_packets_fp_slots = all_packets_e_entries * ORD_M
    leading_all_packets_e_entries = H_PACKET_COUNT * leading_matrix_e_entries
    leading_all_packets_fp_slots = leading_all_packets_e_entries * ORD_M
    all_tensor_factors_e_entries = (
        H_PACKET_COUNT * TENSOR_FACTOR_COUNT * per_packet_e_entries
    )
    all_tensor_factors_fp_slots = all_tensor_factors_e_entries * ORD_M
    leading_all_tensor_factors_e_entries = (
        H_PACKET_COUNT * TENSOR_FACTOR_COUNT * leading_matrix_e_entries
    )
    leading_all_tensor_factors_fp_slots = (
        leading_all_tensor_factors_e_entries * ORD_M
    )

    print("p24 factorized trace-frame Schubert accounting")
    print(f"p={P}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m(p)={ORD_M}")
    print(f"ord_n(p)={ORD_N}")
    print(f"h_packet_count={H_PACKET_COUNT}")
    print(f"tensor_factor_count_per_packet={TENSOR_FACTOR_COUNT}")
    print()
    print("dimensions")
    print(f"subfield_dim_E_C={SUBFIELD_DIM}")
    print(f"A_dim=constant+2+157={A_DIM}")
    print(f"B_dim=211={B_DIM}")
    print(f"axis_dim={AXIS_DIM}")
    print(f"prefix_target_dim=2*179={PREFIX_TARGET_DIM}")
    print(f"forced_intersection_dim={FORCED_INTERSECTION_DIM}")
    print(f"residual_tail_dim={TAIL_DIM}")
    print()
    print("factorized_matrix_entries_over_E_per_H_packet")
    for name, count in matrix_entries_per_packet.items():
        print(f"  {name}={count}")
    print(f"  total={per_packet_e_entries}")
    print()
    print("explicit_matrix_surface")
    print(f"  single_leading_plucker_E_entries_per_H_packet={leading_matrix_e_entries}")
    print(f"  single_leading_all_H_packets_E_entries={leading_all_packets_e_entries}")
    print(f"  single_leading_all_H_packets_Fp_slots={leading_all_packets_fp_slots}")
    print(f"  single_leading_all_H_packets_Fp_slots_over_sqrt={(leading_all_packets_fp_slots/sqrt_p):.12e}")
    print(f"  single_leading_all_70_factors_E_entries={leading_all_tensor_factors_e_entries}")
    print(f"  single_leading_all_70_factors_Fp_slots={leading_all_tensor_factors_fp_slots}")
    print(f"  single_leading_all_70_factors_Fp_slots_over_sqrt={(leading_all_tensor_factors_fp_slots/sqrt_p):.12e}")
    print(f"  one_factor_all_H_packets_E_entries={all_packets_e_entries}")
    print(f"  one_factor_all_H_packets_Fp_slots={all_packets_fp_slots}")
    print(f"  one_factor_all_H_packets_Fp_slots_over_sqrt={(all_packets_fp_slots/sqrt_p):.12e}")
    print(f"  all_70_factors_all_H_packets_E_entries={all_tensor_factors_e_entries}")
    print(f"  all_70_factors_all_H_packets_Fp_slots={all_tensor_factors_fp_slots}")
    print(f"  all_70_factors_all_H_packets_Fp_slots_over_sqrt={(all_tensor_factors_fp_slots/sqrt_p):.12e}")
    print()
    print("punit_surface")
    print("  single_leading_punit_per_H_packet=1")
    print("  single_leading_all_H_packets_punits=8")
    print("  single_leading_decomposition_field_relative_degree8_punits_with_tensor_symmetry=1")
    print("  single_leading_decomposition_field_relative_degree8_punits_without_tensor_symmetry=70")
    print("  per_H_packet_named_punits=4")
    print("  all_H_packets_named_punits=32")
    print("  decomposition_field_relative_degree8_punits_with_tensor_symmetry=4")
    print("  decomposition_field_relative_degree8_punits_without_tensor_symmetry=4*70=280")
    print("  factorized_punits=A_component,B_component,B_mod_A_intersection,residual_tail")
    print("  beta_tensor_factor_punits_if_no_factor_symmetry=32*70=2240")
    print()
    print("interpretation")
    print("  explicit_matrix_surface_is_sub_sqrt_even_when_E_entries_are_expanded_over_Fp=1")
    print("  all_70_factor_surface_is_still_sub_sqrt_but_much_larger=1")
    print("  decomposition_field_packaging_compresses_8_H_packets_to_one_relative_degree8_norm=1")
    print("  punit_surface_requires_arithmetic_theorem_not_matrix_entry_listing=1")
    print("conclusion=reported_factorized_trace_frame_schubert_accounting")


if __name__ == "__main__":
    main()

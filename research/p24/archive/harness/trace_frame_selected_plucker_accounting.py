#!/usr/bin/env python3
"""Static accounting for the selected trace-frame Plucker certificate."""

from __future__ import annotations

import math

P = 10**24 + 7
M = 66254
N = 3107441
ORD_M = 5460
ORD_N = 388430
AXIS_DIM = 368
SUBFIELD_DIM = 179
RELATIVE_DEGREE = 31
TOP_BLOCKS = 3


def log10_binom(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    ) / math.log(10)


def main() -> None:
    tensor_factor_count = math.gcd(ORD_M, ORD_N)
    tensor_factor_degree = ORD_N // tensor_factor_count
    h_packet_count = (N - 1) // ORD_N
    top_target_dim = TOP_BLOCKS * SUBFIELD_DIM
    leading_full_blocks = AXIS_DIM // SUBFIELD_DIM
    leading_tail = AXIS_DIM % SUBFIELD_DIM
    plucker_log10 = log10_binom(top_target_dim, AXIS_DIM)
    random_margin = top_target_dim - AXIS_DIM + 1
    log10_q = ORD_M * math.log10(P)

    print("p24 selected trace-frame Plucker accounting")
    print(f"p={P}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m(p)={ORD_M}")
    print(f"ord_n(p)={ORD_N}")
    print(f"h_packet_count={(N - 1) // ORD_N}")
    print(f"tensor_factor_count_over_E={tensor_factor_count}")
    print(f"tensor_factor_degree_over_E={tensor_factor_degree}")
    print()
    print("selected_trace_frame")
    print(f"axis_dimension={AXIS_DIM}")
    print(f"subfield_dimension_over_E={SUBFIELD_DIM}")
    print(f"relative_degree_B_over_C={RELATIVE_DEGREE}")
    print(f"top_blocks={TOP_BLOCKS}")
    print(f"top_target_dimension={top_target_dim}")
    print(f"leading_prefix_coordinate={leading_full_blocks}*{SUBFIELD_DIM}+{leading_tail}")
    print(f"plucker_coordinate_count=binom({top_target_dim},{AXIS_DIM})")
    print(f"log10_plucker_coordinate_count={plucker_log10:.6f}")
    print()
    print("random_model")
    print(f"log10_Q={log10_q:.6f}")
    print(f"codim_margin={random_margin}")
    print(f"log10_fixed_coordinate_failure_scale~={-random_margin * log10_q:.6e}")
    print()
    print("certificate_surface")
    print("  coordinate_free_object=Omega_top3 in Exterior_E^368(C^3)")
    print("  finite_certificate=leading_prefix_Plucker_coordinate_delta_lead != 0 in E")
    print("  proof_surface=selected_origin_Norm_E_over_Fp(delta_lead) != 0")
    print("  stronger_origin_stable_surface=beta_product_or_eight_packet_product")
    print("  all_packets_need_nonzero=8")
    print("  tensor_factor_rank_symmetry_avoids_listing_all_70_factors=1")
    print("  all_3block_erasure_theorem_is_stronger_than_needed=1")
    print("conclusion=reported_trace_frame_selected_plucker_accounting")


if __name__ == "__main__":
    main()

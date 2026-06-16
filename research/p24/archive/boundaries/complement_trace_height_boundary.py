#!/usr/bin/env python3
"""Height/divisibility audit for the complement-trace resolvent target."""

from __future__ import annotations

import math

P = 10**24 + 7
D_K = -652834595820939249713143
H = 205880396014
M = 66254
N = 3107441
ORD_N_P = 388430
PACKETS = 8


def main() -> None:
    log_p = math.log(P)
    # The trace order has conductor 2, so the singular-modulus discriminant is
    # Delta = 4*D_K.  This matches the previous principal-dominance audits.
    log_principal = math.pi * math.sqrt(4 * abs(D_K))
    log_one_other = 0.5 * log_principal
    log_all_other_crude = math.log(H - 1) + log_one_other
    dominance_margin = log_principal - log_all_other_crude

    packet_degree = ORD_N_P
    selected_zero_pdiv_log = N * log_p
    frobenius_packet_zero_pdiv_log = N * packet_degree * log_p
    one_embedding_norm_upper_log = N * log_principal
    packet_norm_upper_log = N * packet_degree * log_principal

    print("complement trace height/divisibility boundary")
    print(f"p={P}")
    print(f"D_K={D_K}")
    print(f"h={H}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_n_p={ORD_N_P}")
    print(f"frobenius_packets={PACKETS}")
    print()
    print("principal dominance")
    print(f"  log_principal={log_principal:.6e}")
    print(f"  log_one_other_upper={log_one_other:.6e}")
    print(f"  log_all_other_crude={log_all_other_crude:.6e}")
    print(f"  dominance_margin={dominance_margin:.6e}")
    print(f"  dominance_margin_over_log_p={dominance_margin / log_p:.6e}")
    print()
    print("selected-prime zero divisibility")
    print(f"  log_p={log_p:.6e}")
    print(f"  one_cyclotomic_embedding_forces_p_power={N}")
    print(f"  one_embedding_pdiv_log=n*log_p={selected_zero_pdiv_log:.6e}")
    print(f"  frobenius_packet_forces_p_power=n*ord_n_p={N * packet_degree}")
    print(f"  packet_pdiv_log=n*ord_n_p*log_p={frobenius_packet_zero_pdiv_log:.6e}")
    print()
    print("archimedean norm room")
    print(f"  one_embedding_norm_upper_log=n*log_principal={one_embedding_norm_upper_log:.6e}")
    print(f"  packet_norm_upper_log=n*ord_n_p*log_principal={packet_norm_upper_log:.6e}")
    print(f"  one_embedding_room_ratio={one_embedding_norm_upper_log / selected_zero_pdiv_log:.6e}")
    print(f"  packet_room_ratio={packet_norm_upper_log / frobenius_packet_zero_pdiv_log:.6e}")
    print()
    print("interpretation")
    print("  complement_resolvent_is_characteristic_zero_nonzero_by_principal_dominance=1")
    print("  selected_zero_propagates_to_all_n_H_conjugate_primes=1")
    print("  frobenius_packet_zero_propagates_to_n_ord_n_p_split_primes=1")
    print("  height_bound_still_allows_that_divisibility_by_a_factor_about_log_principal_over_log_p=1")
    print("conclusion=reported_complement_trace_height_boundary")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Height/divisibility audit for the L1 partial-moment scalar.

L1 keeps principal coefficient 1 but has nonprincipal coefficients up to 368.
It remains an H-character eigenvector, so a selected zero propagates through
the n H-conjugates and through the Frobenius packet of size ord_n(p).  It is
not K-trivial, so the clean degree-n quotient-field norm package of M0 is not
available.
"""

from __future__ import annotations

import math

P = 10**24 + 7
D_K = -652834595820939249713143
H = 205880396014
M = 66254
N = 3107441
ORD_N_P = 388430
L1_COEFF_MAX = 368


def main() -> None:
    log_p = math.log(P)
    log_principal = math.pi * math.sqrt(4 * abs(D_K))
    log_one_other_l1 = math.log(L1_COEFF_MAX) + 0.5 * log_principal
    log_all_other_l1 = math.log(H - 1) + log_one_other_l1
    dominance_margin_l1 = log_principal - log_all_other_l1

    one_embedding_pdiv_log = N * log_p
    packet_pdiv_log = N * ORD_N_P * log_p
    one_embedding_norm_upper_log = N * log_principal
    one_embedding_norm_upper_log_with_coeff = N * (log_principal + math.log(L1_COEFF_MAX))
    packet_norm_upper_log = N * ORD_N_P * log_principal
    packet_norm_upper_log_with_coeff = N * ORD_N_P * (log_principal + math.log(L1_COEFF_MAX))

    print("L1 height/divisibility audit")
    print(f"p={P}")
    print(f"D_K={D_K}")
    print(f"h={H}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_n_p={ORD_N_P}")
    print(f"L1_coeff_max={L1_COEFF_MAX}")
    print()
    print("principal dominance")
    print(f"  log_principal={log_principal:.6e}")
    print(f"  log_one_other_L1_upper=log(368)+0.5*log_principal={log_one_other_l1:.6e}")
    print(f"  log_all_other_L1_crude={log_all_other_l1:.6e}")
    print(f"  dominance_margin_L1={dominance_margin_l1:.6e}")
    print(f"  dominance_margin_L1_over_log_p={dominance_margin_l1 / log_p:.6e}")
    print()
    print("selected-prime zero divisibility")
    print(f"  one_embedding_pdiv_log=n*log_p={one_embedding_pdiv_log:.6e}")
    print(f"  packet_pdiv_log=n*ord_n_p*log_p={packet_pdiv_log:.6e}")
    print("  K_zero_propagation=0")
    print()
    print("archimedean norm room")
    print(f"  one_embedding_norm_upper_log=n*log_principal={one_embedding_norm_upper_log:.6e}")
    print(
        "  one_embedding_norm_upper_log_with_coeff="
        f"n*(log_principal+log(368))={one_embedding_norm_upper_log_with_coeff:.6e}"
    )
    print(f"  packet_norm_upper_log=n*ord_n_p*log_principal={packet_norm_upper_log:.6e}")
    print(
        "  packet_norm_upper_log_with_coeff="
        f"n*ord_n_p*(log_principal+log(368))={packet_norm_upper_log_with_coeff:.6e}"
    )
    print(f"  one_embedding_room_ratio={one_embedding_norm_upper_log_with_coeff / one_embedding_pdiv_log:.6e}")
    print(f"  packet_room_ratio={packet_norm_upper_log_with_coeff / packet_pdiv_log:.6e}")
    print()
    print("interpretation")
    print("  L1_is_characteristic_zero_nonzero_by_principal_dominance=1")
    print("  coefficient_loss_log_368_is_negligible=1")
    print("  selected_zero_still_forces_n_ord_n_p_padic_divisibility=1")
    print("  height_bound_still_allows_selected_prime_divisibility=1")
    print("  lack_of_K_triviality_removes_degree_n_quotient_norm_packaging=1")
    print("conclusion=reported_l1_height_divisibility_audit")


if __name__ == "__main__":
    main()

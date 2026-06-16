#!/usr/bin/env python3
"""Principal-square dominance for the ordinary autocorrelation energy."""

from __future__ import annotations

import math

P = 10**24 + 7
D_K = -652834595820939249713143
H = 205880396014
M = 66254
N = 3107441
ORD_N_P = 388430


def main() -> None:
    # Singular-modulus discriminant for the conductor-2 trace order.
    delta_abs = 4 * abs(D_K)
    log_j0 = math.pi * math.sqrt(delta_abs)
    log_half = 0.5 * log_j0

    # Ordinary energy:
    #   E_a = sum_d zeta^(a*d) C_d, C_d = sum_i j_i j_{i+m*d}.
    # The unique principal-square term is j_0^2 in C_0.
    log_principal_square = 2 * log_j0

    # Terms with exactly one principal factor occur only for d != 0, at
    # i=0 and i=-m*d.  Every other factor has reduced denominator at least 2.
    one_principal_terms = 2 * (N - 1)
    log_one_principal_bound = math.log(one_principal_terms) + log_j0 + log_half

    # All remaining terms have no principal factor, hence product log at most
    # log_j0.  The crude count h*n safely covers them.
    nonprincipal_terms = H * N
    log_nonprincipal_bound = math.log(nonprincipal_terms) + 2 * log_half

    log_other_bound = max(log_one_principal_bound, log_nonprincipal_bound)
    dominance_margin = log_principal_square - log_other_bound
    log_p = math.log(P)
    packet_norm_upper_log = ORD_N_P * log_principal_square
    packet_pdiv_log = ORD_N_P * log_p

    print("ordinary energy principal-square dominance audit")
    print(f"p={P}")
    print(f"D_K={D_K}")
    print(f"h={H}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_n_p={ORD_N_P}")
    print()
    print("archimedean dominance")
    print(f"  log_j_principal={log_j0:.6e}")
    print(f"  log_principal_square={log_principal_square:.6e}")
    print(f"  one_principal_terms={one_principal_terms}")
    print(f"  log_one_principal_bound={log_one_principal_bound:.6e}")
    print(f"  nonprincipal_terms_bound={nonprincipal_terms}")
    print(f"  log_nonprincipal_bound={log_nonprincipal_bound:.6e}")
    print(f"  log_other_bound={log_other_bound:.6e}")
    print(f"  dominance_margin={dominance_margin:.6e}")
    print(f"  dominance_margin_over_log_p={dominance_margin / log_p:.6e}")
    print()
    print("p-adic boundary")
    print(f"  packet_norm_upper_log=ord_n_p*log_principal_square={packet_norm_upper_log:.6e}")
    print(f"  packet_pdiv_log=ord_n_p*log_p={packet_pdiv_log:.6e}")
    print(f"  room_ratio={packet_norm_upper_log / packet_pdiv_log:.6e}")
    print()
    print("interpretation")
    print("  ordinary_energy_is_characteristic_zero_nonzero_by_principal_square_dominance=1")
    print("  ordinary_energy_is_shift_invariant_but_can_still_be_p_divisible=1")
    print("  height_bounds_do_not_prove_selected_packet_p_unitness=1")
    print("conclusion=reported_ordinary_energy_principal_dominance_audit")


if __name__ == "__main__":
    main()

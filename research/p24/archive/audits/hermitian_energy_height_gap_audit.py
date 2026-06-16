#!/usr/bin/env python3
"""Height audit for the Hermitian energy p-unit hope.

The carry-adjusted Hermitian energy is positive in characteristic zero:

    H_a = sum_u |P_u(a)|^2.

This is better than the ordinary energy, but the p24 certificate needs
`H_a` to be a unit at one selected split prime above p.  This script checks
whether positivity plus a crude archimedean height bound could force that.

It cannot: even a one-prime decomposition-field norm has a logarithmic height
many orders of magnitude larger than log(p).
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
TRACE = -1178414874616
H_CLASS = 205880396014
M_QUOTIENT = 66254
N_RELATIVE = 3107441
ORD_N_P = 388430


def main() -> None:
    delta = TRACE * TRACE - 4 * P24
    if delta >= 0:
        raise AssertionError("ordinary CM target should have negative discriminant")
    if H_CLASS != M_QUOTIENT * N_RELATIVE:
        raise AssertionError("bad h=m*n")
    if pow(P24, ORD_N_P // 2, N_RELATIVE) != N_RELATIVE - 1:
        raise AssertionError("expected real-cyclotomic packet")

    log_p = math.log(P24)
    sqrt_delta = math.sqrt(abs(delta))
    log_j_principal = math.pi * sqrt_delta

    # Naive upper bound: each P_u is a sum of n singular moduli, each bounded
    # by the principal height scale.  Then H_a is a sum of m squared magnitudes.
    log_pu_bound = math.log(N_RELATIVE) + log_j_principal
    log_hermitian_bound = math.log(M_QUOTIENT) + 2 * log_pu_bound

    real_packet_degree = ORD_N_P // 2
    decomposition_degree = (N_RELATIVE - 1) // ORD_N_P
    real_cyclotomic_degree = (N_RELATIVE - 1) // 2
    log_one_decomposition_prime_norm_bound = real_packet_degree * log_hermitian_bound
    log_rational_norm_bound = decomposition_degree * log_one_decomposition_prime_norm_bound

    # Constant-factor height reductions would have to hit this scale before a
    # naive "norm < p" argument can prove p-unit status.
    required_one_prime_factor = log_p / log_one_decomposition_prime_norm_bound
    required_global_factor = log_p / log_rational_norm_bound

    print("p24 Hermitian energy height-gap audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"delta=t^2-4p={delta}")
    print(f"h={H_CLASS}")
    print(f"m={M_QUOTIENT}")
    print(f"n={N_RELATIVE}")
    print(f"ord_n_p={ORD_N_P}")
    print(f"real_packet_degree={real_packet_degree}")
    print(f"decomposition_field_degree={decomposition_degree}")
    print()
    print(f"log_p={log_p:.6f}")
    print(f"log_principal_j_bound=pi*sqrt(|delta|)={log_j_principal:.6e}")
    print(f"log_single_Pu_bound=log(n)+log_j={log_pu_bound:.6e}")
    print(f"log_Hermitian_energy_bound=log(m)+2log(Pu)={log_hermitian_bound:.6e}")
    print()
    print("norm_height_bounds")
    print(
        f"  log_one_decomposition_prime_norm_bound="
        f"{log_one_decomposition_prime_norm_bound:.6e}"
    )
    print(
        f"  one_prime_bound_over_log_p="
        f"{log_one_decomposition_prime_norm_bound / log_p:.6e}"
    )
    print(f"  log_rational_norm_bound={log_rational_norm_bound:.6e}")
    print(f"  rational_norm_bound_over_log_p={log_rational_norm_bound / log_p:.6e}")
    print()
    print("required_height_reduction_for_naive_norm_lt_p")
    print(f"  one_decomposition_prime_factor={required_one_prime_factor:.6e}")
    print(f"  rational_norm_factor={required_global_factor:.6e}")
    print()
    print("interpretation")
    print("  hermitian_energy_is_complex_positive_if_content_vector_nonzero=1")
    print("  positivity_only_proves_characteristic_zero_nonvanishing=1")
    print("  punit_proof_by_crude_archimedean_norm_height=0")
    print("  required_constant_factor_height_reduction_is_astronomically_small=1")
    print(
        "conclusion=Hermitian_energy_punit_route_needs_structural_padic_"
        "argument_not_positivity_or_height"
    )


if __name__ == "__main__":
    main()

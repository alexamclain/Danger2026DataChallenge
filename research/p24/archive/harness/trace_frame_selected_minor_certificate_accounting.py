#!/usr/bin/env python3
"""Accounting for the selected trace-frame translate-minor certificate.

This is a static size audit.  It separates the useful selected-origin
Toeplitz-symbol compression from the oversized literal beta-orbit-algebra
variant.
"""

from __future__ import annotations

from math import isqrt

P = 10**24 + 7
SQRT_P = isqrt(P)
M = 66254
N = 3107441
ORD_M = 5460
ORD_N = 388430
H_PACKETS = 8
TENSOR_FACTORS = 70
ORBIT_DEGREE_OVER_E = 5549
NONZERO_BETA_ORBITS = 560
AXIS_DIM = 368


def ratio(slots: int) -> float:
    return slots / SQRT_P


def main() -> None:
    matrix_entries_e = AXIS_DIM * AXIS_DIM
    symbol_entries_e = M
    symbol_saved_e = matrix_entries_e - symbol_entries_e

    matrix_one_factor_fp = matrix_entries_e * H_PACKETS * ORD_M
    matrix_all_factors_fp = matrix_one_factor_fp * TENSOR_FACTORS
    symbol_one_factor_fp = symbol_entries_e * H_PACKETS * ORD_M
    symbol_all_factors_fp = symbol_one_factor_fp * TENSOR_FACTORS

    literal_orbit_symbol_e = symbol_entries_e * ORBIT_DEGREE_OVER_E
    literal_orbit_symbol_fp = literal_orbit_symbol_e * ORD_M
    literal_all_nonzero_orbits_fp = (
        literal_orbit_symbol_fp * NONZERO_BETA_ORBITS
    )
    literal_beta_inverse_e = N * ORBIT_DEGREE_OVER_E
    literal_beta_inverse_fp = literal_beta_inverse_e * ORD_M
    literal_beta_inverse_all_factors_fp = literal_beta_inverse_fp * TENSOR_FACTORS
    norm_values_with_inverses_e = 2 * NONZERO_BETA_ORBITS
    norm_values_with_inverses_fp = norm_values_with_inverses_e * ORD_M
    relative_degree8_values_with_inverses_e = 2 * TENSOR_FACTORS
    relative_degree8_values_with_inverses_fp = (
        relative_degree8_values_with_inverses_e * ORD_M
    )
    symmetric_degree8_values_with_inverses_e = 2
    symmetric_degree8_values_with_inverses_fp = (
        symmetric_degree8_values_with_inverses_e * ORD_M
    )

    print("p24 selected trace-frame translate-minor accounting")
    print(f"p={P}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m(p)={ORD_M}")
    print(f"ord_n(p)={ORD_N}")
    print(f"h_packet_count={H_PACKETS}")
    print(f"tensor_factor_count_over_E={TENSOR_FACTORS}")
    print(f"nonzero_beta_orbits={NONZERO_BETA_ORBITS}")
    print(f"orbit_degree_over_E={ORBIT_DEGREE_OVER_E}")
    print()
    print("selected_origin_matrix_surface")
    print(f"  axis_dim={AXIS_DIM}")
    print(f"  matrix_entries_over_E_per_packet_factor={matrix_entries_e}")
    print(f"  one_factor_all_H_packets_Fp_slots={matrix_one_factor_fp}")
    print(
        "  one_factor_all_H_packets_Fp_slots_over_sqrt="
        f"{ratio(matrix_one_factor_fp):.12e}"
    )
    print(f"  all_70_factors_Fp_slots={matrix_all_factors_fp}")
    print(
        "  all_70_factors_Fp_slots_over_sqrt="
        f"{ratio(matrix_all_factors_fp):.12e}"
    )
    print()
    print("selected_origin_toeplitz_symbol_surface")
    print(f"  symbol_entries_over_E_per_packet_factor={symbol_entries_e}")
    print(f"  symbol_entries_saved_over_E_per_packet_factor={symbol_saved_e}")
    print(
        "  matrix_entries_over_symbol_entries="
        f"{matrix_entries_e / symbol_entries_e:.12f}"
    )
    print(f"  one_factor_all_H_packets_Fp_slots={symbol_one_factor_fp}")
    print(
        "  one_factor_all_H_packets_Fp_slots_over_sqrt="
        f"{ratio(symbol_one_factor_fp):.12e}"
    )
    print(f"  all_70_factors_Fp_slots={symbol_all_factors_fp}")
    print(
        "  all_70_factors_Fp_slots_over_sqrt="
        f"{ratio(symbol_all_factors_fp):.12e}"
    )
    print()
    print("literal_beta_orbit_symbol_boundary")
    print(
        "  symbol_entries_over_E_per_nonzero_orbit="
        f"{literal_orbit_symbol_e}"
    )
    print(f"  Fp_slots_per_nonzero_orbit={literal_orbit_symbol_fp}")
    print(
        "  Fp_slots_per_nonzero_orbit_over_sqrt="
        f"{ratio(literal_orbit_symbol_fp):.12e}"
    )
    print(
        "  all_nonzero_orbits_literal_Fp_slots="
        f"{literal_all_nonzero_orbits_fp}"
    )
    print(
        "  all_nonzero_orbits_literal_Fp_slots_over_sqrt="
        f"{ratio(literal_all_nonzero_orbits_fp):.12e}"
    )
    print()
    print("literal_full_beta_inverse_boundary")
    print(f"  inverse_coefficients_over_E_one_beta_algebra={literal_beta_inverse_e}")
    print(f"  inverse_coefficients_Fp_slots_one_beta_algebra={literal_beta_inverse_fp}")
    print(
        "  inverse_coefficients_Fp_slots_one_beta_algebra_over_sqrt="
        f"{ratio(literal_beta_inverse_fp):.12e}"
    )
    print(
        "  inverse_coefficients_Fp_slots_times_70="
        f"{literal_beta_inverse_all_factors_fp}"
    )
    print(
        "  inverse_coefficients_Fp_slots_times_70_over_sqrt="
        f"{ratio(literal_beta_inverse_all_factors_fp):.12e}"
    )
    print()
    print("norm_compressed_beta_surface")
    print(
        "  nonzero_orbit_norm_values_plus_inverses_over_E="
        f"{norm_values_with_inverses_e}"
    )
    print(
        "  nonzero_orbit_norm_values_plus_inverses_Fp_slots="
        f"{norm_values_with_inverses_fp}"
    )
    print(
        "  nonzero_orbit_norm_values_plus_inverses_Fp_slots_over_sqrt="
        f"{ratio(norm_values_with_inverses_fp):.12e}"
    )
    print(
        "  degree8_relative_values_plus_inverses_over_E_without_symmetry="
        f"{relative_degree8_values_with_inverses_e}"
    )
    print(
        "  degree8_relative_values_plus_inverses_Fp_slots_without_symmetry="
        f"{relative_degree8_values_with_inverses_fp}"
    )
    print(
        "  degree8_relative_values_plus_inverses_Fp_slots_over_sqrt_without_symmetry="
        f"{ratio(relative_degree8_values_with_inverses_fp):.12e}"
    )
    print(
        "  degree8_relative_values_plus_inverses_over_E_with_symmetry="
        f"{symmetric_degree8_values_with_inverses_e}"
    )
    print(
        "  degree8_relative_values_plus_inverses_Fp_slots_with_symmetry="
        f"{symmetric_degree8_values_with_inverses_fp}"
    )
    print(
        "  degree8_relative_values_plus_inverses_Fp_slots_over_sqrt_with_symmetry="
        f"{ratio(symmetric_degree8_values_with_inverses_fp):.12e}"
    )
    print()
    print("interpretation")
    print("  selected_origin_symbol_surface_is_subsqrt=1")
    print("  selected_origin_symbol_surface_halves_raw_matrix_surface=1")
    print("  literal_beta_orbit_symbol_listing_is_not_subsqrt=1")
    print("  literal_full_beta_inverse_is_not_subsqrt=1")
    print("  norm_compressed_beta_values_are_tiny_if_matched_by_theorem=1")
    print("  beta_orbit_coverage_needs_norm_theorem_not_literal_symbols=1")
    print("conclusion=reported_trace_frame_selected_minor_certificate_accounting")


if __name__ == "__main__":
    main()

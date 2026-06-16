#!/usr/bin/env python3
"""Readiness check for the current p24 compressed search surface.

This is deliberately not a certificate producer.  It answers the operational
question: do we have a finite p24 search/check surface small enough to test
now, and what exact input is still missing?

The current answer is mixed:

* once a selected CM/Lang subgroup kernel polynomial is supplied, the
  remaining check is tiny and deterministic;
* a new low-moment selector hypothesis gives a concrete testing lane:
  4 first-layer moments and 26 second-layer moments should be enough by
  random entropy, if those moments can be constructed intrinsically and an
  anti-collision theorem holds;
* without that factor, there is no honest coefficient/root search to run
  inside the final compressed surface.  The only available large computation
  that directly searches triples is the old randomized Pomerance search, which
  is not the asymptotic result.
"""

from __future__ import annotations

from math import isqrt

from trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate import (
    exhaustive_right_mixed_pairs,
)
from trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate import (
    descends_to_base,
    descends_to_selected_correction,
    product_profile,
)
from trace_gcd_fixed_frequency_p24_h_coset_sum_verifier import (
    EQUATION_COUNT,
    H_STEP,
    LEFT_ROWS,
    NONZERO_RIGHT_COLUMNS,
    RIGHT,
    h_cosets,
    log_table,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    expected_admissible_rank,
    expected_broad_rank,
)
from trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate import (
    formal_cyclotomic_divisor,
    fourier_profile_ok,
)
from trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate import (
    diamond_norm_divisor,
)
from trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate import (
    kernel_polynomial_degree,
)


P24 = 10**24 + 7
SQRT_FLOOR = 10**12
TRACE_THIRD = -1178414874616
STRICT_ODD_PART = 454747350887
SELECTED_CHAIN_SLOTS = 3_107_811
CONDITIONAL_PUNIT_FIELD_ELEMENTS = 4
COMPRESSED_INDEPENDENT_EQUATIONS = 48
LOW_MOMENT_FIRST_LAYER = 4
LOW_MOMENT_SECOND_LAYER = 26
LOW_MOMENT_TOTAL = LOW_MOMENT_FIRST_LAYER + LOW_MOMENT_SECOND_LAYER
LOW_MOMENT_NEW_PRODUCER_VALUES = (LOW_MOMENT_FIRST_LAYER - 1) + (
    LOW_MOMENT_SECOND_LAYER - 1
)
LOW_MOMENT_PARENT_FIELD_COEFFICIENTS = 2 * LOW_MOMENT_FIRST_LAYER + 314 * (
    LOW_MOMENT_SECOND_LAYER
)


def verifier_k(p_value: int) -> int:
    q_value = isqrt(p_value)
    return (q_value + 1 + isqrt(4 * q_value)).bit_length()


def danger_trace_representatives(p_value: int, k_value: int) -> list[int]:
    modulus = 1 << k_value
    bound = isqrt(4 * p_value)
    residue = (p_value + 1) % modulus
    first = -bound + ((residue + bound) % modulus)
    out: list[int] = []
    trace = first
    while trace <= bound:
        out.append(trace)
        trace += modulus
    return out


def print_boolean(name: str, value: bool) -> None:
    print(f"{name}={int(value)}")


def main() -> None:
    print("p24 compressed search readiness")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_FLOOR}")
    print(f"p_mod_8={P24 % 8}")

    k_value = verifier_k(P24)
    traces = danger_trace_representatives(P24, k_value)
    order_third = P24 + 1 - TRACE_THIRD
    odd_part = order_third >> ((order_third & -order_third).bit_length() - 1)
    two_adic_depth = (order_third & -order_third).bit_length() - 1
    print(f"danger_k={k_value}")
    print(f"strict_trace_representatives={traces}")
    print(f"selected_trace={TRACE_THIRD}")
    print(f"selected_order_two_adic_depth={two_adic_depth}")
    print(f"selected_order_odd_part={odd_part}")
    print_boolean("selected_trace_matches_known_third_trace", TRACE_THIRD in traces)
    print_boolean("selected_odd_part_matches_post_j_tail", odd_part == STRICT_ODD_PART)
    print_boolean("x16_p23_sampler_available_for_p24", P24 % 8 == 5)

    p24_pairs = exhaustive_right_mixed_pairs(P24_C_DEGREE)
    expected_pairs = (RIGHT_DEGREE - 1) * (P24_C_DEGREE - 1) * (P24_C_DEGREE - 2)
    print(f"p24_c_degree={P24_C_DEGREE}")
    print(f"p24_symbolic_right_mixed_pairs={len(p24_pairs)}")
    print_boolean("p24_symbolic_pair_count_ok", len(p24_pairs) == expected_pairs)
    print(f"p24_admissible_jacobi_rank={expected_admissible_rank(P24_C_DEGREE)}")
    print(f"p24_broad_jacobi_rank={expected_broad_rank(P24_C_DEGREE)}")
    print(f"p24_broad_minus_admissible_rank={expected_broad_rank(P24_C_DEGREE) - expected_admissible_rank(P24_C_DEGREE)}")

    modulus = 32579
    diamond = diamond_norm_divisor(P24_C_DEGREE, modulus)
    expected = formal_cyclotomic_divisor(P24_C_DEGREE, modulus)
    print(f"p24_diamond_norm_modulus={modulus}")
    print(f"p24_diamond_orbit_size={P24_C_DEGREE - 1}")
    print(f"p24_oriented_one_point_diamond_choices={P24_C_DEGREE - 1}")
    print(f"p24_x_coordinate_generator_pairs={kernel_polynomial_degree(P24_C_DEGREE)}")
    print("p24_kernel_polynomial_generator_orbits=1")
    c_disc = (TRACE_THIRD * TRACE_THIRD - 4 * P24) % P24_C_DEGREE
    c_disc_legendre = pow(c_disc, (P24_C_DEGREE - 1) // 2, P24_C_DEGREE)
    c_disc_legendre = -1 if c_disc_legendre == P24_C_DEGREE - 1 else c_disc_legendre
    print(f"p24_c_divides_selected_group_order={int(order_third % P24_C_DEGREE == 0)}")
    print(f"p24_c_frobenius_discriminant_legendre={c_disc_legendre}")
    print(f"p24_c_final_curve_rational_isogeny_available={int(c_disc_legendre in (0, 1))}")
    print_boolean("p24_diamond_norm_matches_cyclotomic_residual", diamond == expected)
    print_boolean(
        "p24_diamond_norm_fourier_profile_ok",
        fourier_profile_ok(diamond, P24_C_DEGREE, modulus),
    )
    print(f"p24_residual_fourier_channels={RIGHT_DEGREE * (P24_C_DEGREE - 1)}")

    selected_e_values = [
        e_value
        for e_value in range(P24_C_DEGREE)
        if descends_to_selected_correction(P24_C_DEGREE, e_value)
    ]
    base_descent_e_values = [
        e_value
        for e_value in range(P24_C_DEGREE)
        if descends_to_base(P24_C_DEGREE, e_value)
    ]
    print(f"p24_kummer_selected_e_values={selected_e_values}")
    print(f"p24_kummer_base_descent_e_values_count={len(base_descent_e_values)}")
    print(f"p24_kummer_e1_zero_profile={product_profile(P24_C_DEGREE, 1)[0]}")
    print(f"p24_kummer_e1_nonzero_profile={product_profile(P24_C_DEGREE, 1)[1]}")
    print_boolean("p24_kummer_selected_exponent_unique_e_one", selected_e_values == [1])

    logs = log_table()
    cosets = h_cosets(logs)
    print(f"right={RIGHT}")
    print(f"right_h_cosets={len(cosets)}")
    print(f"right_h_coset_size={len(cosets[0])}")
    print(f"left_rows={LEFT_ROWS}")
    print(f"nonzero_right_columns={NONZERO_RIGHT_COLUMNS}")
    print(f"p24_h_coset_equations={EQUATION_COUNT}")
    print(f"p24_compressed_independent_equations={COMPRESSED_INDEPENDENT_EQUATIONS}")
    print_boolean(
        "p24_h_coset_equation_count_ok",
        EQUATION_COUNT == LEFT_ROWS * H_STEP == 1092,
    )

    print(f"conditional_punit_payload_field_elements={CONDITIONAL_PUNIT_FIELD_ELEMENTS}")
    print(f"conditional_punit_payload_over_sqrt={CONDITIONAL_PUNIT_FIELD_ELEMENTS / SQRT_FLOOR:.12e}")
    print(f"selected_chain_slots={SELECTED_CHAIN_SLOTS}")
    print(f"selected_chain_slots_over_sqrt={SELECTED_CHAIN_SLOTS / SQRT_FLOOR:.12e}")
    print(f"generic_sqrt_scale_trials={SQRT_FLOOR}")
    print(f"p24_low_moment_first_layer_constraints={LOW_MOMENT_FIRST_LAYER}")
    print(f"p24_low_moment_second_layer_constraints={LOW_MOMENT_SECOND_LAYER}")
    print(f"p24_low_moment_pairing_constraints={LOW_MOMENT_TOTAL}")
    print(f"p24_low_moment_new_producer_values={LOW_MOMENT_NEW_PRODUCER_VALUES}")
    print(f"p24_low_moment_parent_field_coefficients={LOW_MOMENT_PARENT_FIELD_COEFFICIENTS}")
    print(
        "p24_low_moment_parent_field_coefficients_over_sqrt="
        f"{LOW_MOMENT_PARENT_FIELD_COEFFICIENTS / SQRT_FLOOR:.12e}"
    )

    print("interpretation")
    print("  compressed_surface_ready_if_selected_cm_lang_factor_is_supplied=1")
    print("  deterministic_remaining_anchor_choices_are_two_signs_and_e_equals_one=1")
    print("  deterministic_diamond_norm_orbit_has_178_terms_not_sqrt_p_terms=1")
    print("  p24_178_diamond_one_point_choices_collapse_to_one_kernel_polynomial=1")
    print("  p24_conditional_search_after_kernel_generator_collapse_is_two_signs=1")
    print("  p24_kernel_polynomial_target_is_auxiliary_not_final_curve_179_isogeny=1")
    print("  low_moment_selector_hypothesis_is_now_testable_on_controls=1")
    print("  low_moment_constraints_are_not_a_producer_without_intrinsic_moments=1")
    print("  useful_parallel_compute_lane_is_low_moment_anti_collision_not_root_search=1")
    print("  current_missing_input_is_the_selected_p_integral_cm_lang_subgroup_kernel_polynomial=1")
    print("  without_that_factor_there_is_no_honest_compressed_root_search_to_run=1")
    print("  generic_pomerance_search_is_available_only_as_a_lottery_not_the_proof=1")
    print("conclusion=compressed_search_surface_ready_but_producer_missing")

    if TRACE_THIRD not in traces:
        raise SystemExit(1)
    if odd_part != STRICT_ODD_PART:
        raise SystemExit(1)
    if P24 % 8 == 5:
        raise SystemExit(1)
    if len(p24_pairs) != expected_pairs:
        raise SystemExit(1)
    if diamond != expected:
        raise SystemExit(1)
    if selected_e_values != [1]:
        raise SystemExit(1)
    if EQUATION_COUNT != 1092:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

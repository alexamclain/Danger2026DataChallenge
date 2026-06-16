#!/usr/bin/env python3
"""Exhaustive scalar search for the degenerate Jacobi anchor.

The anchor-correction gate set

    U(0,0)=J(1,1)=q-2

to `1` and proved that this repairs the product-formula identities for the
right-mixed admissible Jacobi packets in small exact models.  This script asks
a more search-like question:

    If we replace only U(0,0) by an arbitrary scalar x in the value field,
    which x work for every right-mixed admissible packet?

The answer in the tested rows is exactly x = +/-1.  The +1 branch is the
reduced Jacobi packet used by the cyclotomic-divisor residual; the -1 branch is
the sign-twisted scalar ambiguity that still satisfies pair-products and row
ratios but does not select the normalized Jdagger(1,1)=1 anchor.

No p24 class-set enumeration is used.  This is a finite-field microscope for
the remaining CM/Lang anchor ambiguity.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate import (
    exhaustive_right_mixed_pairs,
    packet_values_cached,
    pair_products_constant,
    row_ratios_constant,
)
from trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe import make_context
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
)


def replace_anchor(values: list[int], candidate: int) -> list[int]:
    out = values[:]
    out[0] = candidate
    return out


def candidate_works_for_all_pairs(
    candidate: int,
    packets: list[list[int]],
    c_degree: int,
    modulus: int,
) -> bool:
    for values in packets:
        corrected = replace_anchor(values, candidate)
        if not pair_products_constant(corrected, c_degree, modulus):
            return False
        if not row_ratios_constant(corrected, c_degree, modulus):
            return False
    return True


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi-sum anchor scalar search")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    scalar_search_rows = 0
    plus_minus_rows = 0
    plus_one_rows = 0
    q_minus_2_rejected_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        pairs = exhaustive_right_mixed_pairs(c_degree)
        packets = [
            packet_values_cached(ctx, c_degree, u_value, v_value)
            for u_value, v_value in pairs
        ]
        q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
        valid: list[int] = []
        for candidate in range(ctx.value_field_l):
            if candidate_works_for_all_pairs(
                candidate, packets, c_degree, ctx.value_field_l
            ):
                valid.append(candidate)

        expected = [1, ctx.value_field_l - 1]
        scalar_search_ok = int(len(valid) == 2)
        plus_minus_ok = int(valid == expected)
        plus_one_ok = int(
            candidate_works_for_all_pairs(1, packets, c_degree, ctx.value_field_l)
        )
        q_minus_2_rejected_ok = int(q_minus_2 not in valid)

        rows_checked += 1
        scalar_search_rows += scalar_search_ok
        plus_minus_rows += plus_minus_ok
        plus_one_rows += plus_one_ok
        q_minus_2_rejected_rows += q_minus_2_rejected_ok

        print(
            "row "
            f"c_degree={c_degree} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"right_mixed_pairs={len(pairs)} "
            f"q_minus_2={q_minus_2} "
            f"valid_anchor_scalars={valid} "
            f"valid_anchor_count={len(valid)} "
            f"expected_plus_minus_one={expected} "
            f"scalar_search_ok={scalar_search_ok} "
            f"plus_minus_ok={plus_minus_ok} "
            f"plus_one_ok={plus_one_ok} "
            f"raw_q_minus_2_rejected_ok={q_minus_2_rejected_ok}"
        )

    print(f"anchor_scalar_rows_checked={rows_checked}")
    print(f"exhaustive_anchor_scalar_search_rows={scalar_search_rows}/{rows_checked}")
    print(f"valid_anchor_scalars_are_plus_minus_one_rows={plus_minus_rows}/{rows_checked}")
    print(f"reduced_packet_plus_one_anchor_rows={plus_one_rows}/{rows_checked}")
    print(f"raw_q_minus_2_anchor_rejected_rows={q_minus_2_rejected_rows}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("interpretation")
    print("  finite_jacobi_anchor_scalar_search_space_collapses_to_two_signs=1")
    print("  plus_one_is_the_reduced_jdagger_anchor_used_by_cyclotomic_residual=1")
    print("  minus_one_is_a_remaining_scalar_sign_ambiguity_not_a_new_divisor_shape=1")
    print("  raw_q_minus_2_anchor_is_not_a_valid_product_formula_scalar=1")
    print("  p24_anchor_search_should_focus_on_cm_lang_realization_plus_sign_normalization=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search")

    if scalar_search_rows != rows_checked:
        raise SystemExit(1)
    if plus_minus_rows != rows_checked:
        raise SystemExit(1)
    if plus_one_rows != rows_checked:
        raise SystemExit(1)
    if q_minus_2_rejected_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

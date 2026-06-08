#!/usr/bin/env python3
"""Single-anchor correction for literal Jacobi-sum product identities.

The row-ratio miner found the exact right-zero defect

    delta_c = (q - 2)^(-(c - 1)).

This gate checks the stronger finite-field statement suggested by that
formula.  For a right-mixed admissible Jacobi packet

    U_t = J(chi^(u*t), chi^(v*t))

on C_7 x C_c, replace only the single value U(0,0)=J(1,1)=q-2 by

    U'(0,0) = U(0,0) / (q - 2).

All other packet values are unchanged.  Then:

* C-zero pair-products become constant, because (q-2)^2 is scaled to 1;
* the selected row-product ratio at right zero is multiplied by
  (q-2)^(c-1), cancelling delta_c;
* off-C-zero pair-products and nonzero right-row ratios are untouched.

So the literal finite-field Jacobi packet satisfies the full multiplicative
producer target after one non-cyclotomic anchor normalization.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe import (
    make_context,
    row_ratios,
    two_level_products,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    crt,
)


def anchor_corrected(values: list[int], q_minus_2: int, modulus: int) -> list[int]:
    out = values[:]
    out[0] = out[0] * pow(q_minus_2, -1, modulus) % modulus
    return out


def exhaustive_right_mixed_pairs(c_degree: int) -> list[tuple[int, int]]:
    order = RIGHT_DEGREE * c_degree
    pairs: list[tuple[int, int]] = []
    for c_axis_index in range(1, c_degree):
        u_value = RIGHT_DEGREE * c_axis_index
        for v_value in range(1, order):
            if (u_value + v_value) % order == 0:
                continue
            if v_value % c_degree == 0:
                continue
            if (u_value + v_value) % c_degree == 0:
                continue
            if v_value % RIGHT_DEGREE == 0:
                continue
            pairs.append((u_value, v_value))
    return pairs


def packet_values_cached(ctx, c_degree: int, u_value: int, v_value: int) -> list[int]:
    cache = getattr(ctx, "_anchor_gate_cache", None)
    if cache is None:
        cache = {}
        object.__setattr__(ctx, "_anchor_gate_cache", cache)
    values: list[int] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            point = crt(right, c_index, c_degree)
            key = ((u_value * point) % ctx.order, (v_value * point) % ctx.order)
            if key not in cache:
                cache[key] = ctx.jacobi_sum(key[0], key[1])
            values.append(cache[key])
    return values


def pair_products_constant(values: list[int], c_degree: int, modulus: int) -> bool:
    zero_products, off_products = two_level_products(values, c_degree, modulus)
    return len(zero_products) == 1 and len(off_products) == 1


def row_ratios_constant(values: list[int], c_degree: int, modulus: int) -> bool:
    ratios = row_ratios(values, c_degree, modulus)
    return None not in ratios and len(set(value for value in ratios if value is not None)) == 1


def nonzero_right_row_ratios_constant(
    values: list[int], c_degree: int, modulus: int
) -> bool:
    ratios = row_ratios(values, c_degree, modulus)
    nonzero_ratios = [value for value in ratios[1:] if value is not None]
    return len(nonzero_ratios) == RIGHT_DEGREE - 1 and len(set(nonzero_ratios)) == 1


def zero_fiber_has_expected_degeneracy(
    values: list[int], c_degree: int, q_minus_2: int, modulus: int
) -> bool:
    if values[0] != q_minus_2 % modulus:
        return False
    return all(values[right * c_degree] == modulus - 1 for right in range(1, RIGHT_DEGREE))


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi-sum anchor-correction gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    raw_full_pair_failure_rows = 0
    raw_row_ratio_failure_rows = 0
    expected_degeneracy_rows = 0
    corrected_pair_rows = 0
    corrected_ratio_rows = 0
    corrected_product_formula_rows = 0
    single_anchor_rows = 0
    anchor_scale_formula_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l
        pairs = exhaustive_right_mixed_pairs(c_degree)

        raw_full_pair_hits = 0
        raw_row_ratio_hits = 0
        expected_degeneracy_hits = 0
        corrected_pair_hits = 0
        corrected_ratio_hits = 0
        corrected_product_formula_hits = 0
        single_anchor_hits = 0
        anchor_scale_formula_hits = 0
        anchor_values: set[int] = set()

        for u_value, v_value in pairs:
            values = packet_values_cached(ctx, c_degree, u_value, v_value)
            corrected = anchor_corrected(values, q_minus_2, ctx.value_field_l)
            raw_ratios = row_ratios(values, c_degree, ctx.value_field_l)
            corrected_ratios = row_ratios(corrected, c_degree, ctx.value_field_l)

            raw_full_pair_hits += int(
                pair_products_constant(values, c_degree, ctx.value_field_l)
            )
            raw_row_ratio_hits += int(
                row_ratios_constant(values, c_degree, ctx.value_field_l)
            )
            expected_degeneracy_hits += int(
                zero_fiber_has_expected_degeneracy(
                    values, c_degree, q_minus_2, ctx.value_field_l
                )
            )
            corrected_pair_hit = pair_products_constant(
                corrected, c_degree, ctx.value_field_l
            )
            corrected_ratio_hit = row_ratios_constant(
                corrected, c_degree, ctx.value_field_l
            )
            corrected_pair_hits += int(corrected_pair_hit)
            corrected_ratio_hits += int(corrected_ratio_hit)
            corrected_product_formula_hits += int(
                corrected_pair_hit and corrected_ratio_hit
            )
            single_anchor_hits += int(
                corrected[0] == 1
                and corrected[1:] == values[1:]
                and nonzero_right_row_ratios_constant(
                    values, c_degree, ctx.value_field_l
                )
            )
            if (
                raw_ratios[0] is not None
                and raw_ratios[1] is not None
                and corrected_ratios[0] is not None
                and raw_ratios[0] != 0
                and raw_ratios[1] != 0
            ):
                raw_defect = (
                    raw_ratios[0]
                    * pow(raw_ratios[1], -1, ctx.value_field_l)
                    % ctx.value_field_l
                )
                correction_scale = (
                    corrected_ratios[0]
                    * pow(raw_ratios[0], -1, ctx.value_field_l)
                    % ctx.value_field_l
                )
                expected_scale = pow(q_minus_2, c_degree - 1, ctx.value_field_l)
                anchor_scale_formula_hits += int(
                    correction_scale == expected_scale
                    and raw_defect * expected_scale % ctx.value_field_l == 1
                )
            anchor_values.add(values[0])

        row_raw_full_pair_failure = int(raw_full_pair_hits == 0)
        row_raw_row_ratio_failure = int(raw_row_ratio_hits == 0)
        row_expected_degeneracy = int(expected_degeneracy_hits == len(pairs))
        row_corrected_pair = int(corrected_pair_hits == len(pairs))
        row_corrected_ratio = int(corrected_ratio_hits == len(pairs))
        row_corrected_product_formula = int(corrected_product_formula_hits == len(pairs))
        row_single_anchor = int(single_anchor_hits == len(pairs) and anchor_values == {q_minus_2})
        row_anchor_scale_formula = int(anchor_scale_formula_hits == len(pairs))

        raw_full_pair_failure_rows += row_raw_full_pair_failure
        raw_row_ratio_failure_rows += row_raw_row_ratio_failure
        expected_degeneracy_rows += row_expected_degeneracy
        corrected_pair_rows += row_corrected_pair
        corrected_ratio_rows += row_corrected_ratio
        corrected_product_formula_rows += row_corrected_product_formula
        single_anchor_rows += row_single_anchor
        anchor_scale_formula_rows += row_anchor_scale_formula
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"exhaustive_right_mixed_pairs={len(pairs)} "
            f"q_minus_2={q_minus_2} "
            f"raw_full_pair_hits={raw_full_pair_hits}/{len(pairs)} "
            f"raw_row_ratio_hits={raw_row_ratio_hits}/{len(pairs)} "
            f"expected_zero_fiber_degeneracy_hits={expected_degeneracy_hits}/{len(pairs)} "
            f"corrected_pair_product_hits={corrected_pair_hits}/{len(pairs)} "
            f"corrected_row_ratio_hits={corrected_ratio_hits}/{len(pairs)} "
            f"corrected_product_formula_hits={corrected_product_formula_hits}/{len(pairs)} "
            f"single_anchor_hits={single_anchor_hits}/{len(pairs)} "
            f"anchor_scale_formula_hits={anchor_scale_formula_hits}/{len(pairs)} "
            f"anchor_values={sorted(anchor_values)} "
            f"row_raw_full_pair_failure={row_raw_full_pair_failure} "
            f"row_raw_row_ratio_failure={row_raw_row_ratio_failure} "
            f"row_expected_degeneracy={row_expected_degeneracy} "
            f"row_corrected_pair={row_corrected_pair} "
            f"row_corrected_ratio={row_corrected_ratio} "
            f"row_corrected_product_formula={row_corrected_product_formula} "
            f"row_single_anchor={row_single_anchor} "
            f"row_anchor_scale_formula={row_anchor_scale_formula}"
        )

    print(f"raw_full_pair_failure_rows={raw_full_pair_failure_rows}/{rows_checked}")
    print(f"raw_row_ratio_failure_rows={raw_row_ratio_failure_rows}/{rows_checked}")
    print(f"expected_zero_fiber_degeneracy_rows={expected_degeneracy_rows}/{rows_checked}")
    print(f"single_anchor_correction_rows={single_anchor_rows}/{rows_checked}")
    print(f"corrected_pair_product_rows={corrected_pair_rows}/{rows_checked}")
    print(f"corrected_row_ratio_rows={corrected_ratio_rows}/{rows_checked}")
    print(f"corrected_product_formula_rows={corrected_product_formula_rows}/{rows_checked}")
    print(f"anchor_scale_formula_rows={anchor_scale_formula_rows}/{rows_checked}")
    print("interpretation")
    print("  raw_right_mixed_jacobi_packet_fails_only_by_degenerate_anchor=1")
    print("  correcting_single_J_1_1_anchor_by_q_minus_2_inverse_fixes_pair_products=1")
    print("  correcting_single_J_1_1_anchor_by_q_minus_2_inverse_fixes_row_ratio=1")
    print("  anchor_correction_scale_is_inverse_of_mined_delta=1")
    print("  punctured_hasse_davenport_plus_single_anchor_gives_product_formula=1")
    print("  p24_selected_packet_needs_analogue_of_single_anchor_unit=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate")

    if raw_full_pair_failure_rows != rows_checked:
        raise SystemExit(1)
    if raw_row_ratio_failure_rows != rows_checked:
        raise SystemExit(1)
    if expected_degeneracy_rows != rows_checked:
        raise SystemExit(1)
    if single_anchor_rows != rows_checked:
        raise SystemExit(1)
    if corrected_pair_rows != rows_checked:
        raise SystemExit(1)
    if corrected_ratio_rows != rows_checked:
        raise SystemExit(1)
    if corrected_product_formula_rows != rows_checked:
        raise SystemExit(1)
    if anchor_scale_formula_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

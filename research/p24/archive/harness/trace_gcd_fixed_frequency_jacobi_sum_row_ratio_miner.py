#!/usr/bin/env python3
"""Mine the row-ratio defect of literal Jacobi-sum packets.

The previous Jacobi-sum probe showed that raw finite-field Jacobi sums supply
the off-C-zero pair-product complement but not the selected row-product ratio.
This miner asks two questions:

* is the row-ratio defect only a small root-of-unity anomaly?
* does the defect affect all right rows, or only the right-zero anchor?

The observed answer is better than the first probe suggested: in right-mixed
samples, all six nonzero right rows already have a common row ratio.  The
remaining defect is the right-zero anchor, and that defect is not a small
root-of-unity multiplier.

The scalar is exactly the degenerate-Jacobi correction

    delta_c = (q - 2)^(-(c - 1)),

where q is the finite field used for the Jacobi sums.  This comes from
J(1,1)=q-2 in the right-zero row, versus J(1,lambda)=-1 in nonzero right rows.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe import (
    make_context,
    packet_values,
    row_ratios,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
)


MAX_RIGHT_MIXED_PAIRS = 32


def admissible_right_mixed_pairs(c_degree: int) -> list[tuple[int, int]]:
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
            if len(pairs) >= MAX_RIGHT_MIXED_PAIRS:
                return pairs
    return pairs


def normalized_variations(ratios: list[int | None], modulus: int) -> list[int]:
    if any(value is None for value in ratios):
        return []
    base = ratios[0]
    if base is None or base == 0:
        return []
    inv_base = pow(base, -1, modulus)
    return [(value or 0) * inv_base % modulus for value in ratios]


def all_in_roots(values: list[int], order: int, modulus: int) -> bool:
    return all(pow(value, order, modulus) == 1 for value in values)


def log_in_subgroup(value: int, subgroup_root: int, order: int, modulus: int) -> int | None:
    current = 1
    for exponent in range(order):
        if current == value:
            return exponent
        current = current * subgroup_root % modulus
    return None


def linear_root_profile(
    variations: list[int], subgroup_root: int, order: int, modulus: int
) -> bool:
    logs = [log_in_subgroup(value, subgroup_root, order, modulus) for value in variations]
    if any(log_value is None for log_value in logs):
        return False
    numeric_logs = [log_value or 0 for log_value in logs]
    slope = (numeric_logs[1] - numeric_logs[0]) % order
    return all(
        numeric_logs[right] == (numeric_logs[0] + slope * right) % order
        for right in range(len(numeric_logs))
    )


def has_power_root(value: int, exponent: int, modulus: int) -> bool:
    return pow(value, (modulus - 1) // gcd(exponent, modulus - 1), modulus) == 1


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi-sum row-ratio miner")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    no_constant_rows = 0
    nonzero_right_constant_rows = 0
    non_cyclotomic_rows = 0
    non_mu7_rows = 0
    non_muc_rows = 0
    non_linear_mu7_rows = 0
    universal_anchor_defect_rows = 0
    anchor_formula_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        right_root = pow(ctx.zeta, c_degree, ctx.value_field_l)
        c_root = pow(ctx.zeta, RIGHT_DEGREE, ctx.value_field_l)
        pairs = admissible_right_mixed_pairs(c_degree)
        constant_hits = 0
        nonzero_right_constant_hits = 0
        cyclotomic_hits = 0
        mu7_hits = 0
        muc_hits = 0
        linear_mu7_hits = 0
        example_non_cyclotomic: tuple[int, int] | None = None
        anchor_defects: set[int] = set()

        for u_value, v_value in pairs:
            values = packet_values(ctx, c_degree, u_value, v_value)
            ratios = row_ratios(values, c_degree, ctx.value_field_l)
            variations = normalized_variations(ratios, ctx.value_field_l)
            if (
                len(ratios) == RIGHT_DEGREE
                and ratios[0] is not None
                and ratios[1] is not None
                and ratios[1] != 0
            ):
                anchor_defects.add(ratios[0] * pow(ratios[1], -1, ctx.value_field_l) % ctx.value_field_l)
            is_constant = bool(variations) and all(value == 1 for value in variations)
            nonzero_values = [value for value in ratios[1:] if value is not None]
            nonzero_right_constant = (
                len(nonzero_values) == RIGHT_DEGREE - 1
                and len(set(nonzero_values)) == 1
            )
            in_mu_order = bool(variations) and all_in_roots(
                variations, order, ctx.value_field_l
            )
            in_mu7 = bool(variations) and all_in_roots(
                variations, RIGHT_DEGREE, ctx.value_field_l
            )
            in_muc = bool(variations) and all_in_roots(
                variations, c_degree, ctx.value_field_l
            )
            linear_mu7 = in_mu7 and linear_root_profile(
                variations, right_root, RIGHT_DEGREE, ctx.value_field_l
            )
            constant_hits += int(is_constant)
            nonzero_right_constant_hits += int(nonzero_right_constant)
            cyclotomic_hits += int(in_mu_order)
            mu7_hits += int(in_mu7)
            muc_hits += int(in_muc)
            linear_mu7_hits += int(linear_mu7)
            if not in_mu_order and example_non_cyclotomic is None:
                example_non_cyclotomic = (u_value, v_value)

        no_constant = int(constant_hits == 0)
        nonzero_right_constant_all = int(nonzero_right_constant_hits == len(pairs))
        non_cyclotomic = int(cyclotomic_hits == 0)
        non_mu7 = int(mu7_hits == 0)
        non_muc = int(muc_hits == 0)
        non_linear_mu7 = int(linear_mu7_hits == 0)
        universal_anchor_defect = int(len(anchor_defects) == 1)
        anchor_defect_has_c_root = int(
            len(anchor_defects) == 1
            and has_power_root(next(iter(anchor_defects)), c_degree, ctx.value_field_l)
        )
        predicted_anchor_defect = pow(
            ctx.base_field_q - 2, -(c_degree - 1), ctx.value_field_l
        )
        anchor_defect_formula_match = int(
            len(anchor_defects) == 1
            and next(iter(anchor_defects)) == predicted_anchor_defect
        )
        no_constant_rows += no_constant
        nonzero_right_constant_rows += nonzero_right_constant_all
        non_cyclotomic_rows += non_cyclotomic
        non_mu7_rows += non_mu7
        non_muc_rows += non_muc
        non_linear_mu7_rows += non_linear_mu7
        universal_anchor_defect_rows += universal_anchor_defect
        anchor_formula_rows += anchor_defect_formula_match
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"right_mixed_pairs={len(pairs)} "
            f"constant_row_ratio_hits={constant_hits}/{len(pairs)} "
            f"nonzero_right_constant_row_ratio_hits={nonzero_right_constant_hits}/{len(pairs)} "
            f"variation_in_mu_7c_hits={cyclotomic_hits}/{len(pairs)} "
            f"variation_in_mu_7_hits={mu7_hits}/{len(pairs)} "
            f"variation_in_mu_c_hits={muc_hits}/{len(pairs)} "
            f"linear_mu7_profile_hits={linear_mu7_hits}/{len(pairs)} "
            f"distinct_anchor_defects={len(anchor_defects)} "
            f"anchor_defects={sorted(anchor_defects)} "
            f"predicted_anchor_defect_q_minus_2={predicted_anchor_defect} "
            f"anchor_defect_formula_match={anchor_defect_formula_match} "
            f"example_non_cyclotomic_pair={example_non_cyclotomic} "
            f"no_constant={no_constant} "
            f"nonzero_right_constant_all={nonzero_right_constant_all} "
            f"non_cyclotomic={non_cyclotomic} "
            f"non_mu7={non_mu7} non_muc={non_muc} "
            f"non_linear_mu7={non_linear_mu7} "
            f"universal_anchor_defect={universal_anchor_defect}"
            f" anchor_defect_has_c_root={anchor_defect_has_c_root}"
        )

    print(f"right_mixed_no_constant_row_ratio_rows={no_constant_rows}/{rows_checked}")
    print(
        "right_mixed_nonzero_right_constant_row_ratio_rows="
        f"{nonzero_right_constant_rows}/{rows_checked}"
    )
    print(f"right_mixed_non_cyclotomic_defect_rows={non_cyclotomic_rows}/{rows_checked}")
    print(f"right_mixed_non_mu7_defect_rows={non_mu7_rows}/{rows_checked}")
    print(f"right_mixed_non_muc_defect_rows={non_muc_rows}/{rows_checked}")
    print(f"right_mixed_non_linear_mu7_defect_rows={non_linear_mu7_rows}/{rows_checked}")
    print(f"right_mixed_universal_anchor_defect_rows={universal_anchor_defect_rows}/{rows_checked}")
    print(f"right_mixed_anchor_defect_formula_rows={anchor_formula_rows}/{rows_checked}")
    print("interpretation")
    print("  row_ratio_defect_is_not_small_root_of_unity_multiplier=1")
    print("  right_mixed_jacobi_sums_have_constant_nonzero_right_row_ratio=1")
    print("  remaining_row_ratio_defect_is_the_right_zero_anchor=1")
    print("  anchor_defect_is_universal_across_sampled_admissible_pairs=1")
    print("  anchor_defect_equals_q_minus_2_to_minus_c_minus_1=1")
    print("  simple_hasse_davenport_root_of_unity_normalization_is_insufficient=1")
    print("  selected_anchor_ratio_needs_genuine_unit_or_distribution_correction=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_sum_row_ratio_miner")

    if no_constant_rows != rows_checked:
        raise SystemExit(1)
    if nonzero_right_constant_rows != rows_checked:
        raise SystemExit(1)
    if non_cyclotomic_rows != rows_checked:
        raise SystemExit(1)
    if universal_anchor_defect_rows != rows_checked:
        raise SystemExit(1)
    if anchor_formula_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

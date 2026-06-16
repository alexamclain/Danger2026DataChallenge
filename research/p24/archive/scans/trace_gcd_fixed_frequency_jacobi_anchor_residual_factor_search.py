#!/usr/bin/env python3
"""Search for base-field factors splitting the anchor correction.

The reduced-anchor decomposition writes the selected-defect correction as

    h = h_triv + h_nontriv.

Multiplicatively this would mean factoring the row-zero correction into:

    row-sum slice:      constant C on all C positions;
    cyclotomic residual: B^{-(c-1)} at k=0 and B at k != 0.

Their product is:

    k=0:     C * B^{-(c-1)}
    k != 0: C * B.

To realize the selected-defect anchor correction in the base value field, we
need this product to be `1` at k=0 and `s` at k != 0, where

    s = (q-2)/x

and `x` is the replacement scalar for the raw degenerate anchor.  The scalar
search already showed `x = +/-1`.  Eliminating C gives:

    B^c = s.

So the split exists in the value field iff the selected correction scalar is a
c-th power.  This gate exhaustively checks the two valid scalar branches in
the same finite Jacobi models.

The expected result is negative: neither branch has a base-field split.  Thus
the `R_c` residual is the right divisor shape, but a CM/Lang proof should not
expect to realize the row-sum slice and the C-nontrivial residual separately
as value-field factors without adjoining a c-th root or using norm/divisor
language.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe import make_context
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
)


def has_power_root(value: int, exponent: int, modulus: int) -> bool:
    if value % modulus == 0:
        return True
    # In a cyclic group of order modulus-1, x |-> x^exponent has image cut out
    # by value^((modulus-1)/gcd(exponent, modulus-1)) = 1.
    return pow(value, (modulus - 1) // gcd(exponent, modulus - 1), modulus) == 1


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def roots_for_power(value: int, exponent: int, modulus: int) -> list[int]:
    return [
        candidate
        for candidate in range(1, modulus)
        if pow(candidate, exponent, modulus) == value % modulus
    ]


def main() -> None:
    print("Trace-GCD fixed-frequency Jacobi anchor residual factor search")
    print(f"right_degree={RIGHT_DEGREE}")

    rows_checked = 0
    no_plus_split_rows = 0
    no_minus_split_rows = 0
    no_valid_sign_split_rows = 0
    root_criterion_rows = 0

    for c_degree in SMALL_C_DEGREES[:3]:
        order = RIGHT_DEGREE * c_degree
        ctx = make_context(order)
        q_minus_2 = (ctx.base_field_q - 2) % ctx.value_field_l

        # x=+1 gives selected-defect correction s=q-2.
        plus_s = q_minus_2
        # x=-1 gives selected-defect correction s=-(q-2), since U(0,0) is
        # replaced by -1.
        minus_s = (-q_minus_2) % ctx.value_field_l

        plus_roots = roots_for_power(plus_s, c_degree, ctx.value_field_l)
        minus_roots = roots_for_power(minus_s, c_degree, ctx.value_field_l)
        plus_criterion = has_power_root(plus_s, c_degree, ctx.value_field_l)
        minus_criterion = has_power_root(minus_s, c_degree, ctx.value_field_l)

        no_plus_split_ok = int(not plus_roots)
        no_minus_split_ok = int(not minus_roots)
        no_valid_sign_split_ok = int(not plus_roots and not minus_roots)
        criterion_ok = int(
            plus_criterion == bool(plus_roots)
            and minus_criterion == bool(minus_roots)
        )

        rows_checked += 1
        no_plus_split_rows += no_plus_split_ok
        no_minus_split_rows += no_minus_split_ok
        no_valid_sign_split_rows += no_valid_sign_split_ok
        root_criterion_rows += criterion_ok

        print(
            "row "
            f"c_degree={c_degree} order={order} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"q_minus_2={q_minus_2} "
            f"plus_selected_correction={plus_s} "
            f"minus_selected_correction={minus_s} "
            f"plus_c_root_count={len(plus_roots)} "
            f"minus_c_root_count={len(minus_roots)} "
            f"plus_root_criterion={int(plus_criterion)} "
            f"minus_root_criterion={int(minus_criterion)} "
            f"no_plus_split_ok={no_plus_split_ok} "
            f"no_minus_split_ok={no_minus_split_ok} "
            f"no_valid_sign_split_ok={no_valid_sign_split_ok} "
            f"root_criterion_ok={criterion_ok}"
        )

    print(f"anchor_residual_factor_rows_checked={rows_checked}")
    print(f"plus_one_branch_has_no_base_field_residual_split_rows={no_plus_split_rows}/{rows_checked}")
    print(f"minus_one_branch_has_no_base_field_residual_split_rows={no_minus_split_rows}/{rows_checked}")
    print(f"no_valid_sign_has_base_field_residual_split_rows={no_valid_sign_split_rows}/{rows_checked}")
    print(f"c_power_root_criterion_rows={root_criterion_rows}/{rows_checked}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("interpretation")
    print("  row_sum_slice_times_R_c_residual_requires_c_th_root_of_anchor_scalar=1")
    print("  finite_jacobi_value_field_has_no_such_root_for_either_valid_sign=1")
    print("  residual_unit_should_be_handled_divisorially_or_after_norm_extension=1")
    print("  base_field_separate_slice_factorization_is_a_dead_end=1")
    print("  p24_cm_lang_proof_must_use_integral_norm_or_divisor_language_for_R_179=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_jacobi_anchor_residual_factor_search")

    if no_plus_split_rows != rows_checked:
        raise SystemExit(1)
    if no_minus_split_rows != rows_checked:
        raise SystemExit(1)
    if no_valid_sign_split_rows != rows_checked:
        raise SystemExit(1)
    if root_criterion_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

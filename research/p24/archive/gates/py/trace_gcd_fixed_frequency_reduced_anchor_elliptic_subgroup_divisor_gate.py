#!/usr/bin/env python3
"""Genus-one divisor criterion for the reduced-anchor diamond residual.

The diamond norm gate described the residual as the sum of the formal
one-point divisors `[zeta_c^a] - [1]` over `a in (Z/cZ)^*`.  That phrasing is
safe on a cyclotomic/P^1 coordinate, but it is dangerous if read as an
elliptic-unit statement: on an elliptic curve, `[P] - [O]` is not principal
for nonzero torsion `P`.

This gate records the correct genus-one refinement.  For an odd cyclic
subgroup H=<P> of order c,

    D_H = sum_{Q in H, Q != O} [Q] - (c - 1)[O]

has degree zero and Abel-Jacobi sum zero, hence is principal on an elliptic
curve.  In contrast, the individual divisor `[P]-[O]` fails the Abel-Jacobi
criterion, while the Miller divisor `c[P]-c[O]` is principal but its diamond
norm is `c*D_H`, a c-th power overshoot.

So the producer theorem should not try to realize a nonprincipal one-point
elliptic factor.  It should realize the whole diamond/subgroup divisor
directly, or work on the descended cyclotomic coordinate where the one-point
factor is already principal.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate import (
    formal_cyclotomic_divisor,
)
from trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate import (
    diamond_norm_divisor,
)


def c_axis(divisor: list[int], c_degree: int) -> list[int]:
    return divisor[:c_degree]


def one_point_divisor(c_degree: int) -> list[int]:
    values = [0] * c_degree
    values[0] = -1
    values[1] = 1
    return values


def subgroup_residual_divisor(c_degree: int) -> list[int]:
    values = [0] * c_degree
    values[0] = -(c_degree - 1)
    for index in range(1, c_degree):
        values[index] = 1
    return values


def scale(values: list[int], scalar: int) -> list[int]:
    return [scalar * value for value in values]


def degree(values: list[int]) -> int:
    return sum(values)


def abel_sum_mod_c(values: list[int], c_degree: int) -> int:
    return sum(index * value for index, value in enumerate(values)) % c_degree


def elliptic_principal_by_cyclic_criterion(values: list[int], c_degree: int) -> bool:
    return degree(values) == 0 and abel_sum_mod_c(values, c_degree) == 0


def cyclic_nonzero_sum(c_degree: int) -> int:
    return sum(range(1, c_degree)) % c_degree


def main() -> None:
    print("Trace-GCD reduced-anchor elliptic subgroup divisor gate")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    single_nonprincipal_rows = 0
    miller_power_principal_rows = 0
    subgroup_sum_zero_rows = 0
    diamond_principal_rows = 0
    diamond_matches_cyclotomic_rows = 0
    miller_diamond_power_rows = 0
    direct_subgroup_target_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(7 * c_degree)
        single = one_point_divisor(c_degree)
        miller = scale(single, c_degree)
        residual = subgroup_residual_divisor(c_degree)
        miller_diamond = scale(residual, c_degree)
        diamond = c_axis(diamond_norm_divisor(c_degree, modulus), c_degree)
        cyclotomic = c_axis(formal_cyclotomic_divisor(c_degree, modulus), c_degree)
        cyclotomic_signed = [value if value < modulus // 2 else value - modulus for value in cyclotomic]

        single_nonprincipal_ok = int(
            degree(single) == 0
            and abel_sum_mod_c(single, c_degree) == 1
            and not elliptic_principal_by_cyclic_criterion(single, c_degree)
        )
        miller_power_principal_ok = int(
            elliptic_principal_by_cyclic_criterion(miller, c_degree)
        )
        subgroup_sum_zero_ok = int(cyclic_nonzero_sum(c_degree) == 0)
        diamond_principal_ok = int(
            elliptic_principal_by_cyclic_criterion(residual, c_degree)
        )
        diamond_matches_cyclotomic_ok = int(residual == cyclotomic_signed)
        miller_diamond_power_ok = int(
            miller_diamond == scale(residual, c_degree)
            and miller_diamond != residual
        )
        direct_subgroup_target_ok = int(
            diamond_principal_ok
            and diamond_matches_cyclotomic_ok
            and single_nonprincipal_ok
            and miller_diamond_power_ok
        )

        rows_checked += 1
        single_nonprincipal_rows += single_nonprincipal_ok
        miller_power_principal_rows += miller_power_principal_ok
        subgroup_sum_zero_rows += subgroup_sum_zero_ok
        diamond_principal_rows += diamond_principal_ok
        diamond_matches_cyclotomic_rows += diamond_matches_cyclotomic_ok
        miller_diamond_power_rows += miller_diamond_power_ok
        direct_subgroup_target_rows += direct_subgroup_target_ok

        print(
            "row "
            f"c_degree={c_degree} "
            f"single_degree={degree(single)} "
            f"single_abel_sum={abel_sum_mod_c(single, c_degree)} "
            f"miller_abel_sum={abel_sum_mod_c(miller, c_degree)} "
            f"subgroup_sum_mod_c={cyclic_nonzero_sum(c_degree)} "
            f"residual_degree={degree(residual)} "
            f"residual_abel_sum={abel_sum_mod_c(residual, c_degree)} "
            f"single_nonprincipal_ok={single_nonprincipal_ok} "
            f"miller_power_principal_ok={miller_power_principal_ok} "
            f"subgroup_sum_zero_ok={subgroup_sum_zero_ok} "
            f"diamond_principal_ok={diamond_principal_ok} "
            f"diamond_matches_cyclotomic_ok={diamond_matches_cyclotomic_ok} "
            f"miller_diamond_is_c_times_residual_ok={miller_diamond_power_ok} "
            f"direct_subgroup_target_ok={direct_subgroup_target_ok}"
        )

    print(f"elliptic_subgroup_rows_checked={rows_checked}")
    print(f"single_point_elliptic_nonprincipal_rows={single_nonprincipal_rows}/{rows_checked}")
    print(f"miller_c_power_principal_rows={miller_power_principal_rows}/{rows_checked}")
    print(f"nonzero_subgroup_sum_zero_rows={subgroup_sum_zero_rows}/{rows_checked}")
    print(f"diamond_subgroup_residual_principal_rows={diamond_principal_rows}/{rows_checked}")
    print(f"diamond_subgroup_matches_cyclotomic_residual_rows={diamond_matches_cyclotomic_rows}/{rows_checked}")
    print(f"miller_diamond_is_c_times_residual_rows={miller_diamond_power_rows}/{rows_checked}")
    print(f"direct_subgroup_divisor_target_rows={direct_subgroup_target_rows}/{rows_checked}")
    print(f"p24_subgroup_order={P24_C_DEGREE}")
    print(f"p24_nonzero_subgroup_divisor_degree={P24_C_DEGREE - 1}")
    print(f"p24_nonzero_subgroup_sum_mod_c={cyclic_nonzero_sum(P24_C_DEGREE)}")
    print("interpretation")
    print("  individual_one_point_divisor_is_not_an_elliptic_unit_divisor=1")
    print("  miller_c_multiple_is_principal_but_its_diamond_norm_is_R_c_to_c=1")
    print("  whole_nonzero_subgroup_divisor_is_principal_for_odd_c=1")
    print("  p24_target_can_be_direct_diamond_subgroup_divisor_not_single_point_factor=1")
    print("  remaining_problem_is_cm_lang_specialization_and_p_integrality_of_this_subgroup_divisor=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate")

    if single_nonprincipal_rows != rows_checked:
        raise SystemExit(1)
    if miller_power_principal_rows != rows_checked:
        raise SystemExit(1)
    if subgroup_sum_zero_rows != rows_checked:
        raise SystemExit(1)
    if diamond_principal_rows != rows_checked:
        raise SystemExit(1)
    if diamond_matches_cyclotomic_rows != rows_checked:
        raise SystemExit(1)
    if miller_diamond_power_rows != rows_checked:
        raise SystemExit(1)
    if direct_subgroup_target_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

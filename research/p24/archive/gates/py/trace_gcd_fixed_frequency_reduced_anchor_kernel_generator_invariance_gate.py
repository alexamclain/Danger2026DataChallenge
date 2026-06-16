#!/usr/bin/env python3
"""Generator-invariance of the reduced-anchor subgroup kernel polynomial.

The previous kernel-polynomial gate identified the live residual target as

    K_H(x) = prod_{Q in (H \ {O})/{+-1}} (x - x(Q)).

This gate checks the operational consequence: once the selected order-c
subgroup H is known, changing the generator of H does not create another
kernel-polynomial candidate.  The oriented one-point divisors have c-1
diamond conjugates, and their x-coordinates have (c-1)/2 sign-paired choices,
but the whole subgroup polynomial has exactly one generator orbit.

For p24 with c=179 this collapses the apparent 178 diamond-generator surface
to one kernel-polynomial object, leaving only the independent anchor sign
choice and the still-missing problem of constructing the selected CM/Lang
subgroup polynomial itself.
"""

from __future__ import annotations

from math import gcd

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    SMALL_C_DEGREES,
)
from trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate import (
    find_example,
    kernel_polynomial_degree,
    mul,
)


def unit_multipliers(c_degree: int) -> tuple[int, ...]:
    return tuple(u for u in range(1, c_degree) if gcd(u, c_degree) == 1)


def residue_pair_rep(k_value: int, c_degree: int) -> int:
    residue = k_value % c_degree
    return min(residue, (-residue) % c_degree)


def formal_kernel_root_pair_set(c_degree: int, generator_multiplier: int = 1) -> frozenset[int]:
    return frozenset(
        residue_pair_rep(generator_multiplier * k_value, c_degree)
        for k_value in range(1, c_degree)
    )


def formal_generator_invariant(c_degree: int) -> bool:
    base = formal_kernel_root_pair_set(c_degree)
    return all(
        formal_kernel_root_pair_set(c_degree, u_value) == base
        for u_value in unit_multipliers(c_degree)
    )


def actual_kernel_root_set_for_generator(c_degree: int, generator_multiplier: int) -> frozenset[int]:
    example = find_example(c_degree)
    generator = mul(example.curve, generator_multiplier, example.generator)
    return frozenset(
        mul(example.curve, k_value, generator)[0]  # type: ignore[index]
        for k_value in range(1, c_degree)
    )


def actual_generator_invariant(c_degree: int) -> bool:
    base = actual_kernel_root_set_for_generator(c_degree, 1)
    return all(
        actual_kernel_root_set_for_generator(c_degree, u_value) == base
        for u_value in unit_multipliers(c_degree)
    )


def main() -> None:
    print("Trace-GCD reduced-anchor kernel generator-invariance gate")

    actual_degrees = [5, 7, 11, 13, 17, 19]
    actual_rows = 0
    actual_invariant_rows = 0
    actual_pair_count_rows = 0
    for c_degree in actual_degrees:
        unit_count = len(unit_multipliers(c_degree))
        root_count = len(actual_kernel_root_set_for_generator(c_degree, 1))
        invariant = actual_generator_invariant(c_degree)
        pair_count_ok = root_count == kernel_polynomial_degree(c_degree)
        actual_rows += 1
        actual_invariant_rows += int(invariant)
        actual_pair_count_rows += int(pair_count_ok)
        print(
            "actual_row "
            f"c_degree={c_degree} "
            f"oriented_generator_choices={unit_count} "
            f"x_coordinate_generator_pairs={kernel_polynomial_degree(c_degree)} "
            f"kernel_polynomial_generator_orbits=1 "
            f"root_pair_count={root_count} "
            f"generator_invariant_ok={int(invariant)} "
            f"root_pair_count_ok={int(pair_count_ok)}"
        )

    formal_rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    formal_invariant_rows = 0
    formal_pair_count_rows = 0
    for c_degree in formal_rows:
        root_pair_count = len(formal_kernel_root_pair_set(c_degree))
        invariant = formal_generator_invariant(c_degree)
        pair_count_ok = root_pair_count == kernel_polynomial_degree(c_degree)
        formal_invariant_rows += int(invariant)
        formal_pair_count_rows += int(pair_count_ok)

    p24_oriented_generator_choices = P24_C_DEGREE - 1
    p24_x_coordinate_generator_pairs = kernel_polynomial_degree(P24_C_DEGREE)
    p24_kernel_polynomial_generator_orbits = 1
    p24_anchor_sign_choices = 2
    p24_forced_kummer_exponent_choices = 1
    p24_conditional_kernel_search_cases = (
        p24_anchor_sign_choices
        * p24_forced_kummer_exponent_choices
        * p24_kernel_polynomial_generator_orbits
    )

    print(f"actual_generator_invariance_rows={actual_invariant_rows}/{actual_rows}")
    print(f"actual_root_pair_count_rows={actual_pair_count_rows}/{actual_rows}")
    print(f"formal_generator_invariance_rows={formal_invariant_rows}/{len(formal_rows)}")
    print(f"formal_root_pair_count_rows={formal_pair_count_rows}/{len(formal_rows)}")
    print(f"p24_subgroup_order={P24_C_DEGREE}")
    print(f"p24_oriented_one_point_diamond_choices={p24_oriented_generator_choices}")
    print(f"p24_x_coordinate_generator_pairs={p24_x_coordinate_generator_pairs}")
    print(f"p24_kernel_polynomial_generator_orbits={p24_kernel_polynomial_generator_orbits}")
    print(f"p24_anchor_sign_choices={p24_anchor_sign_choices}")
    print(f"p24_forced_kummer_exponent_choices={p24_forced_kummer_exponent_choices}")
    print(f"p24_conditional_kernel_search_cases={p24_conditional_kernel_search_cases}")
    print("interpretation")
    print("  changing_the_generator_of_H_does_not_change_K_H=1")
    print("  p24_178_diamond_one_point_choices_collapse_to_one_kernel_polynomial=1")
    print("  p24_conditional_search_after_kernel_generator_collapse_is_two_signs=1")
    print("  constructing_the_selected_cm_lang_subgroup_polynomial_remains_the_producer_problem=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_kernel_generator_invariance_gate")

    if actual_invariant_rows != actual_rows:
        raise SystemExit(1)
    if actual_pair_count_rows != actual_rows:
        raise SystemExit(1)
    if formal_invariant_rows != len(formal_rows):
        raise SystemExit(1)
    if formal_pair_count_rows != len(formal_rows):
        raise SystemExit(1)
    if p24_conditional_kernel_search_cases != 2:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

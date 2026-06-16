#!/usr/bin/env python3
"""Truncated-polynomial form of the low-moment selector.

Equal first k power sums are equivalent, via Newton identities, to equal first
k elementary symmetric coefficients of the child polynomial.  Since e_1 is
the child sum, and that is the parent period, the p24 low-moment producer can
be phrased as constructing a truncated selected child polynomial:

    first layer:  e_2, e_3, e_4
    second layer: e_2, ..., e_26.
"""

from __future__ import annotations

from itertools import combinations
import random

from trace_gcd_low_moment_sparse_relation_gate import cm_period_values


SEED = 20260607


def power_sums(values: list[int], max_degree: int, q: int) -> tuple[int, ...]:
    return tuple(
        sum(pow(value, degree, q) for value in values) % q
        for degree in range(1, max_degree + 1)
    )


def elementary_prefix_from_power_sums(sums: tuple[int, ...], q: int) -> tuple[int, ...]:
    elementary = [1]
    for k in range(1, len(sums) + 1):
        total = 0
        for i in range(1, k + 1):
            sign = 1 if i % 2 == 1 else -1
            total = (total + sign * elementary[k - i] * sums[i - 1]) % q
        elementary.append(total * pow(k, -1, q) % q)
    return tuple(elementary[1:])


def elementary_prefix(values: list[int], max_degree: int, q: int) -> tuple[int, ...]:
    coeffs = [1] + [0] * max_degree
    for value in values:
        for degree in range(min(max_degree, len(values)), 0, -1):
            coeffs[degree] = (coeffs[degree] + value * coeffs[degree - 1]) % q
    return tuple(coeffs[1:])


def matching_count(
    values: list[int],
    child_size: int,
    target_indices: tuple[int, ...],
    max_degree: int,
    q: int,
    mode: str,
) -> int:
    target_values = [values[index] for index in target_indices]
    if mode == "power":
        target = power_sums(target_values, max_degree, q)
        sig = lambda subset: power_sums(subset, max_degree, q)
    elif mode == "elementary":
        target = elementary_prefix(target_values, max_degree, q)
        sig = lambda subset: elementary_prefix(subset, max_degree, q)
    else:
        raise ValueError(mode)

    count = 0
    for indices in combinations(range(len(values)), child_size):
        subset = [values[index] for index in indices]
        if sig(subset) == target:
            count += 1
    return count


def audit_case(
    label: str,
    values: list[int],
    child_size: int,
    target_indices: tuple[int, ...],
    max_degree: int,
    q: int,
) -> tuple[int, int, int]:
    target_values = [values[index] for index in target_indices]
    sums = power_sums(target_values, max_degree, q)
    elem_from_sums = elementary_prefix_from_power_sums(sums, q)
    elem_direct = elementary_prefix(target_values, max_degree, q)
    power_count = matching_count(values, child_size, target_indices, max_degree, q, "power")
    elementary_count = matching_count(
        values, child_size, target_indices, max_degree, q, "elementary"
    )
    print(
        f"{label} q={q} universe={len(values)} child_size={child_size} "
        f"k={max_degree} newton_match={int(elem_from_sums == elem_direct)} "
        f"power_matches={power_count} elementary_matches={elementary_count} "
        f"e1={elem_direct[0]}"
    )
    return int(elem_from_sums == elem_direct), power_count, elementary_count


def main() -> None:
    print("trace-GCD low-moment truncated-polynomial gate")
    print()

    rng = random.Random(SEED)
    random_q = 101
    random_values = [rng.randrange(random_q) for _ in range(20)]
    random_row = audit_case(
        "random_control=F_101_20_choose_10",
        random_values,
        10,
        tuple(range(10)),
        3,
        random_q,
    )
    print()

    cm_specs = [
        ("D=-200_parent2_child3", -200, 2, 6, 3, 0, 2),
        ("D=-239_parent3_child5", -239, 3, 15, 5, 0, 2),
        ("D=-5000_parent3_child5", -5000, 3, 15, 5, 0, 2),
    ]
    cm_rows: list[tuple[int, int, int]] = []
    print("actual_cm_controls")
    for label, D, parent_count, child_count, child_size, parent, max_degree in cm_specs:
        q, ell, h, values = cm_period_values(D, child_count)
        target = tuple(range(parent, child_count, parent_count))
        cm_rows.append(
            audit_case(
                f"{label} D={D} ell={ell} h={h}",
                values,
                child_size,
                target,
                max_degree,
                q,
            )
        )
    print()

    print("p24_truncated_child_polynomial_target")
    print("  p24_first_layer_nominal_power_sums=4")
    print("  p24_first_layer_coefficients_including_e1=4")
    print("  p24_first_layer_new_coefficients=e2_to_e4_count=3")
    print("  p24_second_layer_nominal_power_sums=26")
    print("  p24_second_layer_coefficients_including_e1=26")
    print("  p24_second_layer_new_coefficients=e2_to_e26_count=25")
    print("  p24_selected_path_new_coefficients=28")
    print()
    print("interpretation")
    print("  low_power_sums_equivalent_to_truncated_child_polynomial_by_newton=1")
    print("  first_coefficient_e1_is_the_parent_period=1")
    print("  p24_low_moment_producer_can_target_28_new_child_polynomial_coefficients=1")
    print("  selector_still_uses_30_constraints_including_parent_e1=1")
    print("conclusion=reported_trace_gcd_low_moment_truncated_polynomial_gate")

    all_rows = [random_row] + cm_rows
    if not all(row[0] for row in all_rows):
        raise SystemExit(1)
    if not all(row[1] == row[2] for row in all_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Entropy/accounting gate for automatic first low moments.

The first child power sum P_1 is automatic from the selected parent period, so
it is not a new producer value.  But it still remains a selector constraint:
candidate child subsets must have the correct sum.  This gate compares full
moments P_1..P_k with higher-only moments P_2..P_k.
"""

from __future__ import annotations

from itertools import combinations
import math
import random

from trace_gcd_low_moment_sparse_relation_gate import cm_period_values


P24_DIGITS = 24
SEED = 20260607


def log10_choose(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    ) / math.log(10)


def signature(values: list[int], degrees: tuple[int, ...], q: int) -> tuple[int, ...]:
    return tuple(
        sum(pow(value, degree, q) for value in values) % q
        for degree in degrees
    )


def matching_count(
    values: list[int],
    child_size: int,
    target_indices: tuple[int, ...],
    degrees: tuple[int, ...],
    q: int,
) -> int:
    target_values = [values[index] for index in target_indices]
    target = signature(target_values, degrees, q)
    count = 0
    for indices in combinations(range(len(values)), child_size):
        candidate = [values[index] for index in indices]
        if signature(candidate, degrees, q) == target:
            count += 1
    return count


def report_case(
    label: str,
    values: list[int],
    child_size: int,
    target_indices: tuple[int, ...],
    q: int,
    max_degree: int,
) -> tuple[int, int, int]:
    p1_degrees = (1,)
    higher_degrees = tuple(range(2, max_degree + 1))
    full_degrees = tuple(range(1, max_degree + 1))
    p1_count = matching_count(values, child_size, target_indices, p1_degrees, q)
    higher_count = matching_count(values, child_size, target_indices, higher_degrees, q)
    full_count = matching_count(values, child_size, target_indices, full_degrees, q)
    print(
        f"{label} q={q} universe={len(values)} child_size={child_size} "
        f"max_degree={max_degree} p1_only={p1_count} "
        f"higher_only={higher_count} full_with_p1={full_count}"
    )
    return p1_count, higher_count, full_count


def main() -> None:
    print("trace-GCD low-moment automatic-P1 entropy gate")
    print()

    random_q = 101
    rng = random.Random(SEED)
    random_values = [rng.randrange(random_q) for _ in range(20)]
    random_target = tuple(range(10))
    random_counts = report_case(
        "random_control=F_101_20_choose_10",
        random_values,
        10,
        random_target,
        random_q,
        3,
    )
    print()

    cm_specs = [
        ("D=-200_parent2_child3", -200, 2, 6, 3, 0, 2),
        ("D=-239_parent3_child5", -239, 3, 15, 5, 0, 2),
        ("D=-5000_parent3_child5", -5000, 3, 15, 5, 0, 2),
    ]
    cm_counts: list[tuple[int, int, int]] = []
    print("actual_cm_controls")
    for label, D, parent_count, child_count, child_size, parent, max_degree in cm_specs:
        q, ell, h, values = cm_period_values(D, child_count)
        target = tuple(range(parent, child_count, parent_count))
        counts = report_case(
            f"{label} D={D} ell={ell} h={h}",
            values,
            child_size,
            target,
            q,
            max_degree,
        )
        cm_counts.append(counts)
    print()

    first_log = log10_choose(314, 157)
    second_log = log10_choose(66254, 211)
    first_higher_only = first_log - 3 * P24_DIGITS
    first_full = first_log - 4 * P24_DIGITS
    second_higher_only = second_log - 25 * P24_DIGITS
    second_full = second_log - 26 * P24_DIGITS

    print("p24_entropy")
    print(f"first_layer_higher_only_target_collision_log10={first_higher_only:.6f}")
    print(f"first_layer_with_parent_p1_target_collision_log10={first_full:.6f}")
    print(
        "first_layer_parent_p1_changes_expected_target_collisions_by_log10="
        f"{first_full - first_higher_only:.6f}"
    )
    print(f"second_layer_higher_only_target_collision_log10={second_higher_only:.6f}")
    print(f"second_layer_with_parent_p1_target_collision_log10={second_full:.6f}")
    print(
        "second_layer_parent_p1_changes_expected_target_collisions_by_log10="
        f"{second_full - second_higher_only:.6f}"
    )
    print()

    print("interpretation")
    print("  automatic_P1_is_not_a_new_producer_value=1")
    print("  automatic_P1_remains_a_selector_constraint=1")
    print("  p24_higher_only_entropy_is_not_enough_for_random_unique_selection=1")
    print("  p24_full_selector_still_uses_30_constraints_but_only_28_new_values=1")
    print("conclusion=reported_trace_gcd_low_moment_automatic_p1_entropy_gate")

    if random_counts[2] > random_counts[1]:
        raise SystemExit(1)
    if not all(full <= higher for _p1, higher, full in cm_counts):
        raise SystemExit(1)
    if not (first_higher_only > 0 and first_full < 0):
        raise SystemExit(1)
    if not (second_higher_only > 0 and second_full < 0):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

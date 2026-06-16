#!/usr/bin/env python3
"""Low-moment window for pairing selected auxiliary child fibers.

The section-pairing guardrail showed that one trace/sum constraint does not
select the p24 child fiber.  This gate asks a sharper question:

    could a small number of power sums pair the selected child?

For a child set S, write

    P_d(S) = sum_{x in S} x^d,       d = 1, 2, ...

The deterministic Newton route needs all child-degree many power sums to
recover the child polynomial.  But over the p24-sized field, a few independent
power sums can behave like strong hashes of an unordered subset.  This is not
a proof; it is a candidate theorem window to test and aim at.

The gate checks:

* the D=-5000 embedded tower toy, where the first power sum already selects
  the true child above each top parent;
* a random F_101 control with 20 choose 10 subsets, where one sum leaves many
  candidates, two sums leave fewer, and three sums isolate the target;
* p24 entropy estimates for the first and second odd layers.
"""

from __future__ import annotations

import math
import random
from itertools import combinations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from tower_phase_refinement_toy import TOP_QUOTIENT, build_tower


P24 = 10**24 + 7
P24_DECIMAL_DIGITS = 24
FIRST_LAYER_TOTAL = 2 * 157
FIRST_LAYER_CHILD = 157
SECOND_LAYER_TOTAL = 2 * 157 * 211
SECOND_LAYER_CHILD = 211
SEED = 20260607


def signature(values: list[int], degree: int, q_value: int) -> tuple[int, ...]:
    return tuple(
        sum(pow(value, exponent, q_value) for value in values) % q_value
        for exponent in range(1, degree + 1)
    )


def count_matching_subsets(
    values: list[int],
    child_size: int,
    target_values: list[int],
    degree: int,
    q_value: int,
) -> int:
    target = signature(target_values, degree, q_value)
    count = 0
    for indices in combinations(range(len(values)), child_size):
        candidate = [values[index] for index in indices]
        if signature(candidate, degree, q_value) == target:
            count += 1
    return count


def actual_tower_counts(max_degree: int) -> dict[int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    tower = build_tower(cycle)

    child_size = len(tower.fine_periods) // TOP_QUOTIENT
    out: dict[int, list[int]] = {degree: [] for degree in range(1, max_degree + 1)}
    for parent in range(TOP_QUOTIENT):
        target_values = [
            tower.fine_periods[index]
            for index in range(parent, len(tower.fine_periods), TOP_QUOTIENT)
        ]
        for degree in range(1, max_degree + 1):
            out[degree].append(
                count_matching_subsets(
                    tower.fine_periods,
                    child_size,
                    target_values,
                    degree,
                    Q,
                )
            )
    return out


def random_control_counts(max_degree: int) -> dict[int, int]:
    rng = random.Random(SEED)
    q_value = 101
    values = [rng.randrange(q_value) for _ in range(20)]
    target_values = values[:10]
    return {
        degree: count_matching_subsets(values, 10, target_values, degree, q_value)
        for degree in range(1, max_degree + 1)
    }


def log10_choose(n_value: int, k_value: int) -> float:
    return (
        math.lgamma(n_value + 1)
        - math.lgamma(k_value + 1)
        - math.lgamma(n_value - k_value + 1)
    ) / math.log(10)


def moments_for_random_unique(log10_subsets: float) -> int:
    # Number of independent F_p moment constraints needed to push the random
    # expected collision count below 1.
    return math.floor(log10_subsets / P24_DECIMAL_DIGITS) + 1


def main() -> None:
    actual = actual_tower_counts(3)
    random_counts = random_control_counts(5)

    first_log = log10_choose(FIRST_LAYER_TOTAL, FIRST_LAYER_CHILD)
    second_log = log10_choose(SECOND_LAYER_TOTAL, SECOND_LAYER_CHILD)
    first_moments = moments_for_random_unique(first_log)
    second_moments = moments_for_random_unique(second_log)
    total_moments = first_moments + second_moments

    print("Trace-GCD reduced-anchor low-moment pairing window")
    print("actual_tower=D=-5000,q=1259,h=30")
    for degree, counts in actual.items():
        print(f"actual_toy_degree_{degree}_matching_counts={counts}")
    print()
    print("random_control=F_101_20_choose_10")
    for degree, count in random_counts.items():
        print(f"random_degree_{degree}_matching_count={count}")
    print()
    print("p24_entropy_window")
    print(f"p={P24}")
    print(f"first_layer_total_roots={FIRST_LAYER_TOTAL}")
    print(f"first_layer_child_size={FIRST_LAYER_CHILD}")
    print(f"first_layer_log10_unordered_child_subsets={first_log:.6f}")
    print(f"first_layer_moments_for_random_unique={first_moments}")
    print(f"first_layer_log10_expected_collisions_after_{first_moments}_moments={first_log - first_moments * P24_DECIMAL_DIGITS:.6f}")
    print(f"second_layer_total_roots={SECOND_LAYER_TOTAL}")
    print(f"second_layer_child_size={SECOND_LAYER_CHILD}")
    print(f"second_layer_log10_unordered_child_subsets={second_log:.6f}")
    print(f"second_layer_moments_for_random_unique={second_moments}")
    print(f"second_layer_log10_expected_collisions_after_{second_moments}_moments={second_log - second_moments * P24_DECIMAL_DIGITS:.6f}")
    print(f"p24_low_moment_pairing_constraints={total_moments}")
    print()
    print("interpretation")
    print("  bounded_power_sums_can_act_like_subset_hashes_in_random_controls=1")
    print("  first_layer_four_moment_window_is_plausible_by_entropy=1")
    print("  second_layer_twenty_six_moment_window_is_plausible_by_entropy=1")
    print("  low_moment_window_is_not_a_proof_without_cm_anti_collision=1")
    print("  constructing_these_selected_moments_remains_a_producer_theorem=1")
    print("conclusion=reported_trace_gcd_reduced_anchor_low_moment_pairing_window")

    if actual[1] != [1, 1]:
        raise SystemExit(1)
    if not (random_counts[1] > random_counts[2] > random_counts[3] == 1):
        raise SystemExit(1)
    if first_moments != 4:
        raise SystemExit(1)
    if second_moments != 26:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

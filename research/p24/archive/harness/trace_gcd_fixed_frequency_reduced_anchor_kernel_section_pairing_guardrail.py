#!/usr/bin/env python3
"""Guardrail: kernel generator collapse is not section selection.

The kernel-generator gate showed that, once a selected order-c subgroup/fiber
is fixed, all generator choices give the same subgroup kernel polynomial.
This does not choose the selected embedded fiber itself.

In tower language, an unordered child polynomial is invariant under
permuting/generating its children, but the proof still has to pair that child
polynomial with the correct parent/section.  This gate records:

* the small D=-5000 embedded tower has unique child subsets by top trace,
  so the finite toy remains internally consistent;
* a random control of modest size already has many subsets with the same
  trace/sum;
* at p24 scales, a trace/sum constraint alone has far too little entropy to
  select a degree-157 child among 314 quotient roots, let alone the degree-211
  refinement.

Thus the two-case kernel surface is conditional on a selected auxiliary
CM/Lang object.  It is not a stand-alone enumeration over generator choices.
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
    monic_poly_from_roots,
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


def log10_choose(n_value: int, k_value: int) -> float:
    return (
        math.lgamma(n_value + 1)
        - math.lgamma(k_value + 1)
        - math.lgamma(n_value - k_value + 1)
    ) / math.log(10)


def actual_tower_subset_counts() -> tuple[int, int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    tower = build_tower(cycle)

    counts: list[int] = []
    child_size = len(tower.fine_periods) // TOP_QUOTIENT
    for z_value in tower.top_periods:
        count = 0
        for indices in combinations(range(len(tower.fine_periods)), child_size):
            if sum(tower.fine_periods[index] for index in indices) % Q == z_value:
                count += 1
        counts.append(count)
    return sum(count == 1 for count in counts), len(counts), counts


def random_subset_sum_collision_count(n_value: int, k_value: int, q_value: int) -> int:
    rng = random.Random(SEED)
    values = [rng.randrange(q_value) for _ in range(n_value)]
    target_indices = tuple(range(k_value))
    target_sum = sum(values[index] for index in target_indices) % q_value
    return sum(
        1
        for indices in combinations(range(n_value), k_value)
        if sum(values[index] for index in indices) % q_value == target_sum
    )


def main() -> None:
    toy_unique_rows, toy_total_rows, toy_counts = actual_tower_subset_counts()
    random_count = random_subset_sum_collision_count(20, 10, 101)

    first_log = log10_choose(FIRST_LAYER_TOTAL, FIRST_LAYER_CHILD)
    first_after_trace = first_log - P24_DECIMAL_DIGITS
    second_local_log = log10_choose(SECOND_LAYER_TOTAL, SECOND_LAYER_CHILD)
    second_after_trace = second_local_log - P24_DECIMAL_DIGITS

    print("Trace-GCD reduced-anchor kernel section-pairing guardrail")
    print("actual_tower=D=-5000,q=1259,h=30")
    print(f"actual_toy_parent_sum_unique_rows={toy_unique_rows}/{toy_total_rows}")
    print(f"actual_toy_parent_subset_counts={toy_counts}")
    print()
    print("random_control")
    print("  n=20")
    print("  child_size=10")
    print("  q=101")
    print(f"  same_sum_subset_count={random_count}")
    print(f"  same_sum_ambiguous={int(random_count > 1)}")
    print()
    print("p24_entropy_accounting")
    print(f"  p={P24}")
    print(f"  first_layer_total_roots={FIRST_LAYER_TOTAL}")
    print(f"  first_layer_child_size={FIRST_LAYER_CHILD}")
    print(f"  first_layer_log10_unordered_child_subsets={first_log:.6f}")
    print(f"  first_layer_log10_expected_same_trace_subsets={first_after_trace:.6f}")
    print(f"  second_layer_total_roots={SECOND_LAYER_TOTAL}")
    print(f"  second_layer_child_size={SECOND_LAYER_CHILD}")
    print(f"  second_layer_log10_local_child_subsets={second_local_log:.6f}")
    print(f"  second_layer_log10_expected_same_trace_subsets={second_after_trace:.6f}")
    print()
    print("interpretation")
    print("  kernel_generator_invariance_collapses_generators_inside_a_fixed_fiber=1")
    print("  kernel_generator_invariance_does_not_pair_the_fiber_with_the_selected_section=1")
    print("  trace_sum_alone_is_not_an_asymptotic_section_selector=1")
    print("  p24_first_layer_trace_sum_entropy_guardrail=1")
    print("  selected_auxiliary_kernel_still_needs_section_pairing_or_relative_traces=1")
    print("conclusion=reported_trace_gcd_reduced_anchor_kernel_section_pairing_guardrail")

    if toy_unique_rows != toy_total_rows:
        raise SystemExit(1)
    if random_count <= 1:
        raise SystemExit(1)
    if first_after_trace <= 10:
        raise SystemExit(1)
    if second_after_trace <= 10:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

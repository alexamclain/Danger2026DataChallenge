#!/usr/bin/env python3
"""Audit whether low-level class invariants give the smooth p24 quotient for free.

The smooth third target has a tempting class group split

    h = 66254 * 3107441.

If one could find a modular/class invariant whose stabilizer inside the ring
class group had size 3107441, its class polynomial would have degree 66254,
and a recovery polynomial of degree 3107441 would still be far below sqrt(p).

This script records the obstruction.  Standard X0(ell) invariants attached to
a split ell-ideal give edge data in the CM isogeny graph.  The class group
acts on the starting vertex of the edge, so the edge values still have a full
class orbit (up to small Atkin-Lehner symmetries); the ideal order is a walk
period, not a stabilizer.  Large quotient invariants arise only after taking
orbit sums/products over an embedded subgroup.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import (
    D as TOY_D,
    ELL as TOY_ELL,
    H as TOY_H,
    Q as TOY_Q,
    decompose,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
CLASS_FACTORS = [2, 157, 211, 3107441]

# Split prime actions already observed or cheap to compute.
SPLIT_PRIME_ACTIONS = [
    (23, 205880396014),
    (2, 102940198007),
    (2897, 1311340102),
    (14057, 975736474),
    (677, 655670051),
    (7349, 487868237),
    (3107441, 205880396014),
]


@dataclass(frozen=True)
class ToyEdgeStats:
    cycle_length: int
    distinct_edge_sums: int
    distinct_edge_products: int
    distinct_unordered_edges: int
    quotient_coset_sums: int
    quotient_size: int
    subgroup_size: int


def gamma0_index_prime(ell: int) -> int:
    return ell + 1


def toy_edge_stats() -> ToyEdgeStats:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(TOY_D)
    roots = pari_linear_roots(hilbert, TOY_Q)
    graph = isogeny_neighbors(roots, TOY_ELL, TOY_Q)
    cycle = walk_cycle(graph)

    edge_sums: set[int] = set()
    edge_products: set[int] = set()
    unordered_edges: set[tuple[int, int]] = set()
    for i, a in enumerate(cycle):
        b = cycle[(i + 1) % len(cycle)]
        edge_sums.add((a + b) % TOY_Q)
        edge_products.add(a * b % TOY_Q)
        unordered_edges.add(tuple(sorted((a, b))))

    dec = decompose(cycle, TOY_Q)
    return ToyEdgeStats(
        cycle_length=len(cycle),
        distinct_edge_sums=len(edge_sums),
        distinct_edge_products=len(edge_products),
        distinct_unordered_edges=len(unordered_edges),
        quotient_coset_sums=len(set(dec.coset_sums)),
        quotient_size=len(dec.coset_sums),
        subgroup_size=len(dec.selected_roots),
    )


def print_p24_table() -> None:
    print("p24 class-invariant stabilizer audit")
    print(f"p={P24}")
    print(f"sqrt_floor_p={SQRT_P}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_factors={CLASS_FACTORS}")
    print()

    print("split_prime_edge_invariants")
    print("  ell kronecker ideal_order ideal_index x0_map_degree edge_orbit_proxy edge_orbit_over_sqrt")
    for ell, order in SPLIT_PRIME_ACTIONS:
        index = CLASS_NUMBER // order
        kronecker = int(sp.kronecker_symbol(D_K, ell))
        print(
            f"  {ell:8d} {kronecker:9d} {order:12d} {index:11d} "
            f"{gamma0_index_prime(ell):14d} {CLASS_NUMBER:16d} "
            f"{CLASS_NUMBER / SQRT_P:20.6e}"
        )

    print()
    print("desired_large_stabilizer_quotients")
    print("  stabilizer_size quotient_degree recovery_degree largest_degree_over_sqrt")
    for stabilizer in (3107441, 66254, 157, 211):
        quotient = CLASS_NUMBER // stabilizer
        recovery = stabilizer
        print(
            f"  {stabilizer:15d} {quotient:15d} {recovery:15d} "
            f"{max(quotient, recovery) / SQRT_P:24.6e}"
        )
    print()
    print("interpretation")
    print("  x0_ell_map_degree_can_be_small=1")
    print("  ideal_order_is_walk_period_not_stabilizer=1")
    print("  prime_level_atkin_lehner_symmetry_size_at_most_2=1")
    print("  large_stabilizer_requires_orbit_sum_or_special_class_invariant=1")
    print()


def print_toy_table() -> None:
    stats = toy_edge_stats()
    print("toy_edge_invariant_calibration")
    print(f"  D={TOY_D}")
    print(f"  q={TOY_Q}")
    print(f"  ell_generator={TOY_ELL}")
    print(f"  class_number={TOY_H}")
    print(f"  cycle_length={stats.cycle_length}")
    print(f"  distinct_X0_edge_sums={stats.distinct_edge_sums}")
    print(f"  distinct_X0_edge_products={stats.distinct_edge_products}")
    print(f"  distinct_unordered_edges={stats.distinct_unordered_edges}")
    print(f"  explicit_subgroup_size={stats.subgroup_size}")
    print(f"  explicit_quotient_coset_sums={stats.quotient_coset_sums}")
    print(f"  explicit_quotient_degree={stats.quotient_size}")
    print("  lesson=X0_edge_values_do_not_automatically_form_the_subgroup_quotient")
    print()


def main() -> None:
    print_p24_table()
    print_toy_table()
    print("obstruction_summary")
    print("  fixed_low_level_modular_functions_have_only_their_modular_symmetries=1")
    print("  smooth_class_subgroups_are_not_modular_automorphisms=1")
    print("  embedded_orbit_sums_would_give_the_desired_stabilizer_but_require_the_orbit=1")
    print(
        "conclusion=no_free_large_stabilizer_class_invariant_identified_for_the_"
        "strict_p24_smooth_class_lead"
    )


if __name__ == "__main__":
    main()

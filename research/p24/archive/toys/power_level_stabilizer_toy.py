#!/usr/bin/env python3
"""Toy audit for high-power generator-level invariants.

The first p24 trace has a striking refinement: the split prime above 2 is a
full class-group generator, while the desired order-19 quotient is the coset
quotient by <g^19>.  A tempting modular interpretation is therefore:

    maybe level 2^19 data has stabilizer <g^19> and gives the quotient.

This toy tests the same shape on the complete D=-5000 CM torsor, where the
norm-3 ideal generates a 30-cycle.  For several moves m, it compares:

* oriented generator paths i -> i+1 -> ... -> i+m, an analogue of level 3^m;
* endpoint/path symmetric values;
* whole-cycle period sums over the subgroup <g^m>.

The path values stay at full orbit size in the toy.  The quotient appears only
after aggregating the whole <g^m> orbit.
"""

from __future__ import annotations

import math

from cypari2 import Pari

from embedded_decomposition_calibration import D, ELL, H, Q, isogeny_neighbors, monic_poly_from_roots, pari_linear_roots, walk_cycle


MOVES = (2, 3, 5, 6, 10, 15)


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * value % q
    return out


def components_for_move(move: int) -> list[list[int]]:
    order = H // math.gcd(H, move)
    seen: set[int] = set()
    components: list[list[int]] = []
    for start in range(H):
        if start in seen:
            continue
        comp = [(start + k * move) % H for k in range(order)]
        seen.update(comp)
        components.append(comp)
    return components


def audit_move(cycle: list[int], move: int) -> None:
    paths = [[cycle[(i + step) % H] for step in range(move + 1)] for i in range(H)]
    endpoint_pairs = [tuple(sorted((path[0], path[-1]))) for path in paths]
    endpoint_sums = [(path[0] + path[-1]) % Q for path in paths]
    endpoint_products = [path[0] * path[-1] % Q for path in paths]
    path_sums = [sum(path) % Q for path in paths]
    path_products = [product(path, Q) for path in paths]

    comps = components_for_move(move)
    period_sums = [sum(cycle[i] for i in comp) % Q for comp in comps]
    period_products = [product([cycle[i] for i in comp], Q) for comp in comps]

    order = H // math.gcd(H, move)
    quotient = math.gcd(H, move)
    print("move_audit")
    print(f"  move={move}")
    print(f"  subgroup_order={order}")
    print(f"  quotient_size={quotient}")
    print(f"  path_level_proxy={ELL}^{move}")
    print(f"  oriented_path_count={len(paths)}")
    print(f"  distinct_endpoint_pairs={len(set(endpoint_pairs))}")
    print(f"  distinct_endpoint_sums={len(set(endpoint_sums))}")
    print(f"  distinct_endpoint_products={len(set(endpoint_products))}")
    print(f"  distinct_path_sums={len(set(path_sums))}")
    print(f"  distinct_path_products={len(set(path_products))}")
    print(f"  component_count={len(comps)}")
    print(f"  component_sizes={sorted({len(comp) for comp in comps})}")
    print(f"  distinct_period_sums={len(set(period_sums))}")
    print(f"  distinct_period_products={len(set(period_products))}")
    print(f"  period_sum_polynomial_degree={len(monic_poly_from_roots(period_sums, Q)) - 1}")
    print()


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    print("power-level stabilizer toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"cycle_length={len(cycle)}")
    print()
    for move in MOVES:
        audit_move(cycle, move)
    print("interpretation")
    print("  high_power_generator_paths_retain_full_orbit_in_toy=1")
    print("  endpoint_or_path_level_data_is_not_the_coset_period=1")
    print("  quotient_degree_appears_only_after_whole_subgroup_aggregation=1")
    print(
        "conclusion=power_level_modular_data_does_not_by_itself_give_a_"
        "large_class_stabilizer"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Toy audit for binary-oriented composite paths.

The p24 composite target needs the oriented ideal 2 * 463 * 223^(-1).  A
possible escape hatch is that binary split-prime orientation might provide a
small algebraic cover without requiring full X1 generator data.

This toy uses D=-5000, where the class group has order 30 and the norm-3 ideal
generates the CM cycle.  The oriented product

    3 * 17^(-1)

has class log 1 - 7 = -6 = 24 mod 30, hence index 6 and order 5.  We compare:

* local oriented path invariants from j_i -> j_{i+1} -> j_{i+24};
* whole-cycle period invariants over the order-5 oriented composite cycles.

If binary orientation alone supplied the quotient selector, simple local path
values would collapse to 6 values.  They do not: they retain the full orbit.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import D, ELL, H, Q, isogeny_neighbors, monic_poly_from_roots, pari_linear_roots, walk_cycle

LOG_3 = 1
LOG_17 = 7
MOVE = (LOG_3 - LOG_17) % H
ORDER = H // __import__("math").gcd(H, MOVE)
INDEX = H // ORDER


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * value % q
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    path_sums = []
    path_products = []
    path_edge_pair_sums = []
    for i in range(H):
        a = cycle[i]
        b = cycle[(i + LOG_3) % H]
        c = cycle[(i + MOVE) % H]
        path_sums.append((a + b + c) % Q)
        path_products.append(a * b % Q * c % Q)
        path_edge_pair_sums.append(((a + b) % Q, (b + c) % Q))

    components = []
    seen = set()
    for i in range(H):
        if i in seen:
            continue
        comp = [(i + k * MOVE) % H for k in range(ORDER)]
        seen.update(comp)
        components.append(comp)

    period_sums = [sum(cycle[i] for i in comp) % Q for comp in components]
    period_products = [product([cycle[i] for i in comp], Q) for comp in components]

    print("oriented composite path toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"oriented_product=3*17^(-1)")
    print(f"move_log={MOVE}")
    print(f"cycle_order={ORDER}")
    print(f"cycle_index={INDEX}")
    print()
    print("local_oriented_path_invariants")
    print(f"  path_count={H}")
    print(f"  distinct_path_sums={len(set(path_sums))}")
    print(f"  distinct_path_products={len(set(path_products))}")
    print(f"  distinct_path_edge_pair_sums={len(set(path_edge_pair_sums))}")
    print()
    print("whole_oriented_cycle_invariants")
    print(f"  component_count={len(components)}")
    print(f"  component_sizes={sorted({len(comp) for comp in components})}")
    print(f"  distinct_period_sums={len(set(period_sums))}")
    print(f"  distinct_period_products={len(set(period_products))}")
    print(f"  period_sum_polynomial_degree={len(monic_poly_from_roots(period_sums, Q)) - 1}")
    print()
    print("interpretation")
    print("  binary_oriented_local_path_values_have_full_orbit=1")
    print("  quotient_only_appears_after_whole_cycle_aggregation=1")
    print("  oriented_composite_period_problem_remains_a_class_period_problem=1")
    print("conclusion=binary_orientation_does_not_by_itself_supply_a_seedless_local_selector")


if __name__ == "__main__":
    main()

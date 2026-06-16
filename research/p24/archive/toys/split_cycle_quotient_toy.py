#!/usr/bin/env python3
"""Toy calibration for split-prime cycle quotients.

For D=-5000 over F_1259, the class group is cyclic of order 30.  The split
prime ell=11 has class order 3, so the horizontal 11-isogeny graph on CM
j-roots breaks into ten 3-cycles.

This is the concrete version of the p24 677-cycle idea: an X0(ell) edge value
is not a quotient invariant, but the symmetric functions of a whole split-prime
cycle are.  The catch is that forming those cycle invariants still requires
embedded vertices, or an equivalent theorem that supplies them.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
)

ELL = 11
CLASS_NUMBER = 30
CLASS_ORDER_OF_ELL = 3


def components(graph: dict[int, list[int]]) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for root in sorted(graph):
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        comp: list[int] = []
        while stack:
            current = stack.pop()
            comp.append(current)
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        out.append(sorted(comp))
    return sorted(out)


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    comps = components(graph)

    unordered_edges: set[tuple[int, int]] = set()
    edge_sums: set[int] = set()
    edge_products: set[int] = set()
    for a, neighbors in graph.items():
        for b in neighbors:
            edge = tuple(sorted((a, b)))
            unordered_edges.add(edge)
            edge_sums.add((a + b) % Q)
            edge_products.add(a * b % Q)

    cycle_sums = [sum(comp) % Q for comp in comps]
    cycle_poly = monic_poly_from_roots(cycle_sums, Q)

    print("split-prime cycle quotient toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell={ELL}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_order_of_ell={CLASS_ORDER_OF_ELL}")
    print(f"split_roots={len(roots)}")
    print(f"isogeny_graph_degree_set={sorted({len(v) for v in graph.values()})}")
    print(f"component_count={len(comps)}")
    print(f"component_sizes={sorted({len(c) for c in comps})}")
    print()
    print("edge_values")
    print(f"  unordered_edges={len(unordered_edges)}")
    print(f"  distinct_edge_sums={len(edge_sums)}")
    print(f"  distinct_edge_products={len(edge_products)}")
    print()
    print("cycle_quotient")
    print(f"  cycle_sum_values={len(cycle_sums)}")
    print(f"  distinct_cycle_sums={len(set(cycle_sums))}")
    print(f"  cycle_sum_polynomial_degree={len(cycle_poly) - 1}")
    print(f"  cycle_sum_polynomial_coeffs_ascending_mod_q={cycle_poly}")
    print()
    print("interpretation")
    print("  x0_edge_values_still_have_full_orbit=1")
    print("  whole_cycle_symmetric_values_have_quotient_degree=1")
    print("  constructing_cycle_values_used_embedded_cm_vertices=1")
    print(
        "conclusion=split_prime_cycles_are_the_right_quotient_object_but_"
        "do_not_remove_the_seed_or_embedded_orbit_problem"
    )


if __name__ == "__main__":
    main()

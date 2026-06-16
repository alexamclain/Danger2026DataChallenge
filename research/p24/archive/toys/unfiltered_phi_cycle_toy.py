#!/usr/bin/env python3
"""Universal Phi_l cycles do not select the fixed CM order.

This is the seedless counterpart to ``seedless_cycle_elimination_toy.py``.
For the small target

    D = -87, q = 103, ell = 7,

the fixed CM torsor has six roots and the horizontal Phi_7 graph has two
3-cycles with sums [4, 29].  If we remove the CM-order filter H_D(j)=0 and
look only at universal simple 3-cycles of Phi_7 over F_q, the target sums are
only a subset of a larger universal cycle locus.

Thus the closed-cycle equations know about ell-isogeny cycles, but not about
which fixed CM order/horizontal class is intended.
"""

from __future__ import annotations

from cypari2 import Pari
import sympy as sp

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots
from seedless_cycle_elimination_toy import parse_pari_poly

D = -87
Q = 103
ELL = 7
CYCLE_LENGTH = 3


def phi_adjacency(q: int, ell: int) -> dict[int, set[int]]:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    x, y = sp.symbols("x y")
    phi = sp.Poly(
        parse_pari_poly(str(pari.polmodular(ell)), x, y, modulus=q),
        x,
        y,
        modulus=q,
    )
    graph = {a: set() for a in range(q)}
    for a in range(q):
        for b in range(q):
            if int(phi.eval({x: a, y: b})) % q == 0:
                graph[a].add(b)
    return graph


def simple_3cycles(graph: dict[int, set[int]]) -> list[tuple[int, int, int]]:
    cycles: set[tuple[int, int, int]] = set()
    for a in graph:
        for b in graph[a]:
            if b == a:
                continue
            for c in graph[b]:
                if c == a or c == b:
                    continue
                if a in graph[c]:
                    cycles.add(tuple(sorted((a, b, c))))
    return sorted(cycles)


def cm_cycle_sums() -> list[int]:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    seen: set[int] = set()
    sums: list[int] = []
    for root in roots:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        component: list[int] = []
        while stack:
            current = stack.pop()
            component.append(current)
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        sums.append(sum(component) % Q)
    return sorted(sums)


def main() -> None:
    graph = phi_adjacency(Q, ELL)
    cycles = simple_3cycles(graph)
    universal_sums = sorted({sum(cycle) % Q for cycle in cycles})
    cm_sums = cm_cycle_sums()

    print("unfiltered Phi_l cycle toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell={ELL}")
    print(f"cycle_length={CYCLE_LENGTH}")
    print(f"universal_vertices={Q}")
    print(f"universal_simple_3cycles={len(cycles)}")
    print(f"universal_distinct_cycle_sums={len(universal_sums)}")
    print(f"universal_cycle_sums={universal_sums}")
    print(f"CM_cycle_sums={cm_sums}")
    print(f"CM_sums_subset_universal={set(cm_sums) <= set(universal_sums)}")
    print()
    print("interpretation")
    print("  Phi_l_closed_cycles_include_the_target_CM_cycles=1")
    print("  Phi_l_closed_cycles_also_include_extra_non_target_cycles=1")
    print("  fixed_CM_order_filter_or_equivalent_embedded_relation_required=1")
    print(
        "conclusion=unfiltered_modular_cycle_equations_do_not_select_the_"
        "fixed_CM_component_quotient"
    )


if __name__ == "__main__":
    main()

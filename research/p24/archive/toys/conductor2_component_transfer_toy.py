#!/usr/bin/env python3
"""Compare maximal and conductor-2 split-cycle quotients.

For the p=103, t=8 toy with D=-87, the strict trace discriminant is 4D.
The maximal roots H_D and conductor-2 roots H_4D have the same class number.
Because 2 splits, the descending 2-isogeny from the maximal 2-volcano surface
to the conductor-2 floor is an equivariant bijection of class torsors.

This script asks whether that bijection gives a cheap relation between
ell-cycle *sums* for ell=7.  If the conductor-2 component sums were a simple
function of maximal component sums, this might create a new route.  If not,
the conductor-2 branch is only a verifier-correct relabeling of the same
embedded class-action problem.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, monic_poly_from_roots
from fixed_trace_cm_root_toy import FROBENIUS_D, MAXIMAL_D, P, pari_linear_roots

ELL = 7
VERTICAL_ELL = 2


def components(graph: dict[int, list[int]]) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for root in sorted(graph):
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
        out.append(sorted(component))
    return sorted(out)


def phi_neighbors_between(source: list[int], target: list[int], ell: int, q: int) -> dict[int, list[int]]:
    pari = Pari()
    phi = pari.polmodular(ell)
    out: dict[int, list[int]] = {}
    for a in source:
        row: list[int] = []
        phi_a = pari(f"subst({phi}, x, Mod({a},{q}))")
        for b in target:
            if int(pari(f"subst({phi_a}, y, Mod({b},{q}))")) == 0:
                row.append(b)
        out[a] = sorted(row)
    return out


def component_index(root: int, comps: list[list[int]]) -> int:
    for idx, comp in enumerate(comps):
        if root in comp:
            return idx
    raise KeyError(root)


def symmetric_pair(values: list[int], q: int) -> tuple[int, int]:
    if len(values) != 2:
        raise ValueError(values)
    return (sum(values) % q, values[0] * values[1] % q)


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    max_roots = pari_linear_roots(pari.polclass(MAXIMAL_D), P)
    c2_roots = pari_linear_roots(pari.polclass(FROBENIUS_D), P)

    max_graph = isogeny_neighbors(max_roots, ELL, P)
    c2_graph = isogeny_neighbors(c2_roots, ELL, P)
    max_comps = components(max_graph)
    c2_comps = components(c2_graph)
    down = phi_neighbors_between(max_roots, c2_roots, VERTICAL_ELL, P)

    image_pairs: list[tuple[int, int]] = []
    image_component_sets: list[tuple[int, ...]] = []
    for comp in max_comps:
        images: list[int] = []
        c2_indices: set[int] = set()
        for root in comp:
            if len(down[root]) != 1:
                raise RuntimeError(f"expected unique down edge from {root}, got {down[root]}")
            image = down[root][0]
            images.append(image)
            c2_indices.add(component_index(image, c2_comps))
        image_pairs.append((sum(comp) % P, sum(images) % P))
        image_component_sets.append(tuple(sorted(c2_indices)))

    max_sums = [sum(comp) % P for comp in max_comps]
    c2_sums = [sum(comp) % P for comp in c2_comps]
    pair_poly = monic_poly_from_roots([a * P + b for a, b in image_pairs], P * P)

    print("conductor2 component transfer toy")
    print(f"p={P}")
    print(f"maximal_D={MAXIMAL_D}")
    print(f"conductor2_D={FROBENIUS_D}")
    print(f"ell={ELL}")
    print(f"max_roots={max_roots}")
    print(f"conductor2_roots={c2_roots}")
    print(f"max_component_sizes={sorted({len(c) for c in max_comps})}")
    print(f"conductor2_component_sizes={sorted({len(c) for c in c2_comps})}")
    print(f"vertical_down_degrees={sorted({len(v) for v in down.values()})}")
    print(f"max_cycle_sums={sorted(max_sums)}")
    print(f"conductor2_cycle_sums={sorted(c2_sums)}")
    print(f"down_image_component_indices={image_component_sets}")
    print(f"paired_max_to_conductor2_sums={image_pairs}")
    print(f"sum_sets_equal={int(sorted(max_sums) == sorted(c2_sums))}")
    if len(max_sums) == 2 and len(c2_sums) == 2:
        print(f"max_sums_symmetric={symmetric_pair(sorted(max_sums), P)}")
        print(f"conductor2_sums_symmetric={symmetric_pair(sorted(c2_sums), P)}")
    print(f"paired_sum_encoding_poly_degree={len(pair_poly) - 1}")
    print()
    print("interpretation")
    print("  descending_2_isogeny_is_equivariant_on_components=1")
    print("  conductor2_component_quotient_has_same_degree_as_maximal=1")
    print("  constructing_the_down_images_still_used_embedded_maximal_roots=1")
    print("conclusion=conductor2_branch_transfers_the_component_problem_not_solves_it")


if __name__ == "__main__":
    main()

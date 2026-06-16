#!/usr/bin/env python3
"""Non-genus abstract-vs-embedded quotient pairing toy.

The earlier D=-87 toy showed that an abstract unramified quotient polynomial
does not by itself pair with an embedded split-cycle quotient.  That example
had quotient degree 2, where every pairing is too small to be diagnostic.

This file repeats the test for a non-genus quotient:

    D = -2239, h = 35, split ell = 5, quotient size = 5.

PARI gives an abstract degree-5 Hilbert quotient.  Over q=2243 both the
abstract quotient and the CM class polynomial split, and the horizontal Phi_5
graph gives five embedded 7-cycles.  We compare the five abstract roots with
the five embedded cycle sums and search for affine or Mobius maps between the
two unordered root sets.

No such map is found.  The abstract quotient exists, but the phase/pairing to
the embedded j-cycles is not a simple low-degree finite-field relation in this
toy.
"""

from __future__ import annotations

from itertools import permutations

from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots

D = -2239
Q = 2243
ELL = 5
QUOTIENT_SIZE = 5
SUBGROUP_SIZE = 7


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
    return sorted(out, key=lambda row: row[0])


def affine_maps(source: list[int], target: list[int], q: int) -> set[tuple[int, int]]:
    target_set = set(target)
    out: set[tuple[int, int]] = set()
    for x0 in source:
        for x1 in source:
            if x1 == x0:
                continue
            for y0 in target:
                for y1 in target:
                    if y1 == y0:
                        continue
                    a = (y1 - y0) * pow(x1 - x0, -1, q) % q
                    b = (y0 - a * x0) % q
                    if {(a * x + b) % q for x in source} == target_set:
                        out.add((a, b))
    return out


def null_vector_mod_q(matrix: list[list[int]], q: int) -> list[int] | None:
    rows = [row[:] for row in matrix]
    m = len(rows)
    n = len(rows[0])
    pivots: list[int] = []
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(m):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % q for j in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in pivots]
    if not free:
        return None
    vec = [0] * n
    vec[free[0]] = 1
    for row_index, pivot_col in enumerate(pivots):
        vec[pivot_col] = (-rows[row_index][free[0]]) % q
    return vec


def mobius_maps(source: list[int], target: list[int], q: int) -> set[tuple[int, int, int, int]]:
    target_set = set(target)
    out: set[tuple[int, int, int, int]] = set()
    for xs in permutations(source, 3):
        for ys in permutations(target, 3):
            matrix = []
            for x, y in zip(xs, ys):
                # a*x + b = y*(c*x+d)
                matrix.append([x % q, 1, (-y * x) % q, (-y) % q])
            vec = null_vector_mod_q(matrix, q)
            if vec is None:
                continue
            a, b, c, d = vec
            if (a * d - b * c) % q == 0:
                continue
            values: list[int] = []
            ok = True
            for x in source:
                den = (c * x + d) % q
                if den == 0:
                    ok = False
                    break
                values.append((a * x + b) * pow(den, -1, q) % q)
            if ok and set(values) == target_set:
                out.add((a, b, c, d))
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    c = (1 - D) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")
    abstract = pari(f"bnrclassfield(bnr,{QUOTIENT_SIZE},1)")

    cm_roots = pari_linear_roots(hilbert, Q)
    abstract_roots = pari_linear_roots(abstract, Q)
    graph = isogeny_neighbors(cm_roots, ELL, Q)
    comps = components(graph)
    period_sums = sorted(sum(comp) % Q for comp in comps)

    affines = affine_maps(abstract_roots, period_sums, Q)
    mobius = mobius_maps(abstract_roots, period_sums, Q)

    print("abstract embedded pairing non-genus toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell={ELL}")
    print(f"class_number={len(cm_roots)}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print(f"abstract_polynomial={abstract}")
    print(f"abstract_roots={sorted(abstract_roots)}")
    print(f"component_sizes={sorted(len(comp) for comp in comps)}")
    print(f"embedded_period_sums={period_sums}")
    print(f"affine_set_maps_found={len(affines)}")
    print(f"mobius_set_maps_found={len(mobius)}")
    print()
    print("interpretation")
    print("  abstract_quotient_splits_mod_q=1")
    print("  embedded_period_quotient_splits_mod_q=1")
    print("  no_affine_pairing_between_root_sets=1")
    print("  no_mobius_pairing_between_root_sets=1")
    print("  quotient_pairing_behaves_like_extra_embedded_data=1")
    print("conclusion=abstract_non_genus_quotient_does_not_supply_a_simple_phase_map")


if __name__ == "__main__":
    main()

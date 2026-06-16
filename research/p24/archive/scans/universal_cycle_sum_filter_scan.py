#!/usr/bin/env python3
"""Compare universal Phi_ell cycle sums with fixed-CM component sums.

This generalizes the D=-87 unfiltered-cycle toy.  For small examples where a
split prime ell has small component size r on the embedded CM roots, enumerate
all simple r-cycles of Phi_ell over F_q and compare their cycle sums with the
fixed-CM component sums.

The goal is to test whether seedless closed-cycle equations are close to the
CM quotient, or whether they overselect a much larger universal cycle locus.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots
from seedless_cycle_elimination_toy import parse_pari_poly
from cycle_period_complexity_scan import find_splitting_prime


@dataclass(frozen=True)
class Row:
    D: int
    q: int
    h: int
    ell: int
    component_size: int
    cm_component_count: int
    cm_sum_count: int
    universal_cycle_count: int
    universal_sum_count: int
    cm_subset_universal: bool
    extra_sum_count: int


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
            if a == b:
                continue
            if int(phi.eval({x: a, y: b})) % q == 0:
                graph[a].add(b)
    return graph


def simple_cycles_of_length(graph: dict[int, set[int]], length: int) -> set[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()

    def canonical(path: list[int]) -> tuple[int, ...]:
        rots = [tuple(path[i:] + path[:i]) for i in range(len(path))]
        rev = list(reversed(path))
        rots.extend(tuple(rev[i:] + rev[:i]) for i in range(len(rev)))
        return min(rots)

    for start in graph:
        stack: list[tuple[int, list[int]]] = [(start, [start])]
        while stack:
            current, path = stack.pop()
            if len(path) == length:
                if start in graph[current]:
                    cycles.add(canonical(path))
                continue
            for nxt in graph[current]:
                if nxt in path:
                    continue
                stack.append((nxt, path + [nxt]))
    return cycles


def find_component_case(
    pari: Pari,
    D: int,
    hilbert,
    h: int,
    q_start: int,
    q_stop: int,
    max_ell: int,
    max_component_size: int,
) -> Row | None:
    split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
    if split is None:
        return None
    q, roots = split
    if q > q_stop:
        return None
    for ell in sp.primerange(2, max_ell + 1):
        if D % ell == 0 or sp.kronecker_symbol(D, int(ell)) != 1:
            continue
        graph = isogeny_neighbors(roots, int(ell), q)
        comps = components(graph)
        sizes = sorted({len(comp) for comp in comps})
        if len(sizes) != 1:
            continue
        size = sizes[0]
        if not (2 <= size <= max_component_size and size < h):
            continue
        universal_graph = phi_adjacency(q, int(ell))
        cycles = simple_cycles_of_length(universal_graph, size)
        universal_sums = {sum(cycle) % q for cycle in cycles}
        cm_sums = {sum(comp) % q for comp in comps}
        return Row(
            D=D,
            q=q,
            h=h,
            ell=int(ell),
            component_size=size,
            cm_component_count=len(comps),
            cm_sum_count=len(cm_sums),
            universal_cycle_count=len(cycles),
            universal_sum_count=len(universal_sums),
            cm_subset_universal=cm_sums <= universal_sums,
            extra_sum_count=len(universal_sums - cm_sums),
        )
    return None


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    q_start: int,
    q_stop: int,
    max_ell: int,
    max_component_size: int,
) -> list[Row]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-87, -5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[Row] = []
    seen: set[int] = set()
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        row = find_component_case(
            pari,
            D,
            hilbert,
            h,
            q_start,
            q_stop,
            max_ell,
            max_component_size,
        )
        if row is None:
            continue
        rows.append(row)
        if len(rows) >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=12)
    ap.add_argument("--min-h", type=int, default=4)
    ap.add_argument("--max-h", type=int, default=40)
    ap.add_argument("--max-abs-D", type=int, default=5000)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=350)
    ap.add_argument("--max-ell", type=int, default=13)
    ap.add_argument("--max-component-size", type=int, default=4)
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        q_start=args.q_start,
        q_stop=args.q_stop,
        max_ell=args.max_ell,
        max_component_size=args.max_component_size,
    )

    print("universal cycle-sum filter scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_ell={args.max_ell}")
    print(f"max_component_size={args.max_component_size}")
    print()
    print("columns: D q h ell r cm_components cm_sums universal_cycles universal_sums extra_sums subset")
    for row in rows:
        print(
            f"D={row.D:6d} q={row.q:4d} h={row.h:3d} ell={row.ell:2d} "
            f"r={row.component_size:2d} cm_components={row.cm_component_count:3d} "
            f"cm_sums={row.cm_sum_count:3d} universal_cycles={row.universal_cycle_count:5d} "
            f"universal_sums={row.universal_sum_count:4d} extra_sums={row.extra_sum_count:4d} "
            f"subset={int(row.cm_subset_universal)}"
        )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  all_cm_sums_subset_universal={int(all(row.cm_subset_universal for row in rows))}")
    print(f"  rows_with_extra_universal_sums={sum(1 for row in rows if row.extra_sum_count)}")
    print()
    print("interpretation")
    print("  universal_closed_cycles_contain_target_CM_component_sums=1")
    print("  extra_universal_sums_mean_Phi_cycle_equations_do_not_select_CM_order=1")
    print("  seedless_component_quotient_needs_a_CM_filter_or_equivalent_trace_formula=1")
    print("conclusion=reported_universal_cycle_sum_filter_scan")


if __name__ == "__main__":
    main()

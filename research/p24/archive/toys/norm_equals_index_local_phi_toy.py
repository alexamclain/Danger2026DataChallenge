#!/usr/bin/env python3
"""Toy scan for split primes with norm equal to quotient index.

The first p24 trace has the striking formal target

    ell = 19,  index(<ell>) = 19.

This script searches small CM examples with the same shape and asks whether
local Phi_ell data at the surface vertices determines the horizontal cycle
periods.  At a CM root j_i, Phi_ell(j_i,Y) has two horizontal roots when ell
splits; the remaining symmetric data is local volcano/descending data.  If the
ell=index coincidence created a seedless selector, it might show up as a low
degree relation between the cycle period and such local Phi data.

The result is only a toy audit, but it directly tests the new p24 coincidence
rather than generic class-character periods.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, monic_poly_from_roots, pari_linear_roots


@dataclass(frozen=True)
class Candidate:
    D: int
    h: int
    ell: int
    order: int
    index: int


def principal_form(pari: Pari, D: int):
    if D % 4 == 1:
        return pari.qfbred(pari(f"Qfb(1,1,{(1 - D) // 4})"))
    return pari.qfbred(pari(f"Qfb(1,0,{(-D) // 4})"))


def form_order(pari: Pari, D: int, h: int, ell: int) -> int:
    factors = {int(q): int(e) for q, e in sp.factorint(h).items()}
    principal = str(principal_form(pari, D))
    nucomp_l = int((abs(D) // 4) ** 0.25) + 1
    form = pari.qfbprimeform(D, int(ell))
    order = h
    for q, e in factors.items():
        for _ in range(e):
            candidate = order // q
            if str(pari.qfbred(pari.qfbnupow(form, candidate, nucomp_l))) == principal:
                order = candidate
            else:
                break
    return order


def find_candidates(max_abs_d: int, max_h: int, min_ell: int, max_ell: int, max_cases: int) -> list[Candidate]:
    pari = Pari()
    out: list[Candidate] = []
    for D in range(-3, -max_abs_d - 1, -1):
        if D % 4 not in (0, 1):
            continue
        try:
            h = int(pari.poldegree(pari.polclass(D)))
        except Exception:
            continue
        if h < 4 or h > max_h:
            continue
        for ell in sp.primerange(max(2, min_ell), max_ell + 1):
            if abs(D) % ell == 0 or sp.kronecker_symbol(D, int(ell)) != 1:
                continue
            order = form_order(pari, D, h, int(ell))
            index = h // order
            if index == ell:
                out.append(Candidate(D, h, int(ell), order, index))
                if len(out) >= max_cases:
                    return out
    return out


def find_splitting_prime(pari: Pari, D: int, h: int, min_q: int = 101, max_q: int = 20_000) -> tuple[int, list[int]] | None:
    hilbert = pari.polclass(D)
    for q in sp.primerange(max(min_q, h + 2), max_q):
        if abs(D) % q == 0:
            continue
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            return int(q), roots
    return None


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


def phi_y_coeffs_at_x(pari: Pari, ell: int, q: int, x_value: int) -> list[int]:
    phi = pari.polmodular(int(ell))
    y_poly = pari(f"Pol(subst({phi}, x, Mod({x_value},{q})), y)")
    degree = int(pari.poldegree(y_poly))
    leading = int(pari.polcoef(y_poly, degree)) % q
    inv_leading = pow(leading, -1, q)
    return [int(pari.polcoef(y_poly, i)) * inv_leading % q for i in range(degree + 1)]


def audit_candidate(candidate: Candidate) -> dict[str, object] | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    split = find_splitting_prime(pari, candidate.D, candidate.h)
    if split is None:
        return None
    q, roots = split
    graph = isogeny_neighbors(roots, candidate.ell, q)
    comps = components(graph)
    if sorted({len(c) for c in comps}) != [candidate.order] or len(comps) != candidate.index:
        return None

    root_to_period: dict[int, int] = {}
    cycle_sums = []
    local_rows = []
    root_set = set(roots)
    for comp in comps:
        period = sum(comp) % q
        cycle_sums.append(period)
        for root in comp:
            root_to_period[root] = period

    for root in roots:
        coeffs = phi_y_coeffs_at_x(pari, candidate.ell, q, root)
        total_neighbor_sum = (-coeffs[-2]) % q
        horizontal = graph[root]
        horizontal_sum = sum(horizontal) % q
        descending_sum = (total_neighbor_sum - horizontal_sum) % q
        horizontal_product = 1
        for value in horizontal:
            horizontal_product = horizontal_product * value % q
        local_rows.append((root, root_to_period[root], total_neighbor_sum, horizontal_sum, descending_sum, horizontal_product))

    # Search for a linear relation period = a0 + a1*j + a2*local1+...
    # over all roots.  Full rank means no such tiny local linear formula.
    columns = []
    for row in local_rows:
        root, period, total_sum, horizontal_sum, descending_sum, horizontal_product = row
        columns.append([1, root, total_sum, horizontal_sum, descending_sum, horizontal_product, period])
    matrix = sp.Matrix(columns)
    rank_features = sp.polys.matrices.DomainMatrix.from_Matrix(matrix[:, :-1], sp.GF(q)).rank()
    rank_augmented = sp.polys.matrices.DomainMatrix.from_Matrix(matrix, sp.GF(q)).rank()

    return {
        "D": candidate.D,
        "h": candidate.h,
        "ell": candidate.ell,
        "order": candidate.order,
        "index": candidate.index,
        "q": q,
        "cycle_sums": sorted(cycle_sums),
        "cycle_poly_degree": len(monic_poly_from_roots(cycle_sums, q)) - 1,
        "distinct_descending_sums": len({row[4] for row in local_rows}),
        "distinct_horizontal_sums": len({row[3] for row in local_rows}),
        "feature_rank": int(rank_features),
        "augmented_rank": int(rank_augmented),
        "linear_local_formula_exists": int(rank_features == rank_augmented),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-d", type=int, default=6000)
    ap.add_argument("--max-h", type=int, default=80)
    ap.add_argument("--min-ell", type=int, default=2)
    ap.add_argument("--max-ell", type=int, default=31)
    ap.add_argument("--max-cases", type=int, default=5)
    args = ap.parse_args()

    candidates = find_candidates(args.max_abs_d, args.max_h, args.min_ell, args.max_ell, args.max_cases)
    print("norm equals index local Phi toy")
    print(f"max_abs_d={args.max_abs_d}")
    print(f"max_h={args.max_h}")
    print(f"min_ell={args.min_ell}")
    print(f"max_ell={args.max_ell}")
    print(f"candidate_count={len(candidates)}")
    for candidate in candidates:
        print(
            f"candidate D={candidate.D} h={candidate.h} ell={candidate.ell} "
            f"order={candidate.order} index={candidate.index}"
        )
    print()

    audited = 0
    for candidate in candidates:
        result = audit_candidate(candidate)
        if result is None:
            continue
        audited += 1
        print("audit")
        for key, value in result.items():
            print(f"  {key}={value}")
        print()

    print("interpretation")
    print("  ell_equals_index_examples_exist_at_toy_scale=1" if candidates else "  ell_equals_index_examples_exist_at_toy_scale=0")
    print("  local_phi_features_tested=1")
    print("  linear_local_formula_exists_should_be_read_as_toy_only=1")
    print("conclusion=reported_norm_equals_index_local_phi_toy")


if __name__ == "__main__":
    main()

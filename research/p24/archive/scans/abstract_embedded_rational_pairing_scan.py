#!/usr/bin/env python3
"""Search for low-degree rational pairings from abstract quotient roots to periods.

An abstract class-field quotient polynomial and an embedded component-period
polynomial both split over the chosen finite field.  A useful p24 shortcut
would need more: a low-complexity relation pairing the abstract roots with the
embedded periods.

By default this runs the known non-genus `D=-2239` case and checks degree `1`,
which is the Mobius test from `abstract_embedded_pairing_non_genus_toy.py`.
The broader case discovery scan is opt-in because `bnrclassfield` searches can
otherwise become CPU waits rather than mathematical tests.
"""

from __future__ import annotations

import argparse
from itertools import permutations

import sympy as sp
from cypari2 import Pari

from abstract_embedded_pairing_non_genus_toy import components, null_vector_mod_q
from cycle_period_complexity_scan import find_splitting_prime
from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots


def eval_poly(coeffs: list[int], x: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % q
        power = power * x % q
    return total


def normalize(vec: list[int], q: int) -> tuple[int, ...]:
    for value in vec:
        if value % q:
            inv = pow(value % q, -1, q)
            return tuple((v * inv) % q for v in vec)
    raise ValueError("zero vector")


def rational_maps(
    source: list[int],
    target: list[int],
    q: int,
    degree: int,
    max_found: int = 3,
) -> set[tuple[int, ...]]:
    """Find rational maps P/Q of bounded degree carrying source set to target set."""
    if len(source) < 2 * degree + 1:
        return set()
    target_set = set(target)
    fixed_source = source[: 2 * degree + 1]
    found: set[tuple[int, ...]] = set()
    for image_tuple in permutations(target, len(fixed_source)):
        matrix: list[list[int]] = []
        for x, y in zip(fixed_source, image_tuple):
            row: list[int] = []
            power = 1
            for _ in range(degree + 1):
                row.append(power)
                power = power * x % q
            power = 1
            for _ in range(degree + 1):
                row.append((-y * power) % q)
                power = power * x % q
            matrix.append(row)
        vec = null_vector_mod_q(matrix, q)
        if vec is None:
            continue
        key = normalize(vec, q)
        if key in found:
            continue
        p_coeffs = list(key[: degree + 1])
        q_coeffs = list(key[degree + 1 :])
        values: list[int] = []
        ok = True
        for x in source:
            den = eval_poly(q_coeffs, x, q)
            if den == 0:
                ok = False
                break
            values.append(eval_poly(p_coeffs, x, q) * pow(den, -1, q) % q)
        if ok and set(values) == target_set:
            found.add(key)
            if len(found) >= max_found:
                return found
    return found


def quotient_cases(pari: Pari, max_abs_d: int, max_h: int, max_q: int):
    seen: set[int] = set()
    for D in range(-200, -max_abs_d - 1, -1):
        if D in seen or D % 4 not in (0, 1):
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if h < 12 or h > max_h:
            continue
        split = find_splitting_prime(pari, hilbert, h, stop=max_q)
        if split is None:
            continue
        q, roots = split
        for ell in sp.primerange(3, 31):
            if abs(D) % ell == 0 or sp.kronecker_symbol(D, ell) != 1:
                continue
            graph = isogeny_neighbors(roots, int(ell), q)
            if sorted({len(v) for v in graph.values()}) != [2]:
                continue
            comps = components(graph)
            m = len(comps)
            if m < 7 or m >= h:
                continue
            period_sums = sorted(sum(comp) % q for comp in comps)
            c = (1 - D) // 4
            pari(f"bnf=bnfinit(y^2-y+{c})")
            pari("bnr=bnrinit(bnf,1)")
            try:
                abstract = pari(f"bnrclassfield(bnr,{m},1)")
                abstract_roots = pari_linear_roots(abstract, q)
            except Exception:
                continue
            if len(abstract_roots) != m:
                continue
            yield D, q, int(ell), h, m, sorted(abstract_roots), period_sums


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scan",
        action="store_true",
        help="search for additional small cases; default runs the known D=-2239 case",
    )
    parser.add_argument("--max-abs-d", type=int, default=5000)
    parser.add_argument("--max-h", type=int, default=80)
    parser.add_argument("--max-q", type=int, default=10000)
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--degree", type=int, default=1)
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows = 0
    found_rows = 0
    print("abstract embedded rational pairing scan")
    print("D q ell h quotient degree maps_found abstract_roots embedded_periods")
    if args.scan:
        case_iter = quotient_cases(pari, args.max_abs_d, args.max_h, args.max_q)
    else:
        from abstract_embedded_pairing_non_genus_toy import D, ELL, Q, QUOTIENT_SIZE

        c = (1 - D) // 4
        pari(f"bnf=bnfinit(y^2-y+{c})")
        pari("bnr=bnrinit(bnf,1)")
        abstract = pari(f"bnrclassfield(bnr,{QUOTIENT_SIZE},1)")
        abstract_roots = sorted(pari_linear_roots(abstract, Q))
        cm_roots = pari_linear_roots(pari.polclass(D), Q)
        graph = isogeny_neighbors(cm_roots, ELL, Q)
        comps = components(graph)
        period_sums = sorted(sum(comp) % Q for comp in comps)
        case_iter = iter([(D, Q, ELL, len(cm_roots), QUOTIENT_SIZE, abstract_roots, period_sums)])

    for D, q, ell, h, m, abstract_roots, period_sums in case_iter:
        maps = rational_maps(abstract_roots, period_sums, q, args.degree)
        rows += 1
        found_rows += 1 if maps else 0
        print(
            f"{D} {q} {ell} {h} {m} {args.degree} {len(maps)} "
            f"{abstract_roots} {period_sums}"
        )
        if rows >= args.max_rows:
            break
    print()
    print(f"rows={rows}")
    print(f"rows_with_low_degree_map={found_rows}")
    print(f"all_no_low_degree_map={int(rows > 0 and found_rows == 0)}")
    print("conclusion=reported_abstract_embedded_rational_pairing_scan")


if __name__ == "__main__":
    main()

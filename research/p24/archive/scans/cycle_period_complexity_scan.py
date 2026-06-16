#!/usr/bin/env python3
"""Scan small CM period sequences for low-complexity structure.

This is a data-lift experiment aimed at the current theorem target, not at
raw DANGER triples.  For small discriminants where a split prime gives a full
CM class cycle over a splitting finite field, choose quotient sizes m and form

    y_r = sum_{k=0}^{n-1} j_{r+m*k},  h = m*n.

If these period sequences had unexpectedly low linear complexity or sparse
Fourier support, that would suggest a possible finite-field identity stronger
than the generic high-order class-character trace formulation.  The expected
negative result is random-like complexity: most quotient characters are
present.
"""

from __future__ import annotations

import math

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle


def divisors_between(n: int, lo: int, hi: int) -> list[int]:
    return [d for d in sorted(sp.divisors(n)) if lo <= d <= hi and d < n]


def bm_linear_complexity(sequence: list[int], q: int) -> int:
    """Berlekamp-Massey linear complexity over F_q."""
    c = [1]
    b = [1]
    linear_complexity = 0
    m = 1
    last_discrepancy = 1
    for idx, value in enumerate(sequence):
        discrepancy = value
        for j in range(1, linear_complexity + 1):
            discrepancy = (discrepancy + c[j] * sequence[idx - j]) % q
        if discrepancy == 0:
            m += 1
            continue
        old_c = c[:]
        scale = discrepancy * pow(last_discrepancy, -1, q) % q
        if len(c) < len(b) + m:
            c.extend([0] * (len(b) + m - len(c)))
        for j, coeff in enumerate(b):
            c[j + m] = (c[j + m] - scale * coeff) % q
        if 2 * linear_complexity <= idx:
            linear_complexity = idx + 1 - linear_complexity
            b = old_c
            last_discrepancy = discrepancy
            m = 1
        else:
            m += 1
    return linear_complexity


def primitive_root_of_order(q: int, order: int) -> int | None:
    if (q - 1) % order != 0:
        return None
    generator = sp.primitive_root(q)
    root = pow(generator, (q - 1) // order, q)
    if pow(root, order, q) != 1:
        return None
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            return None
    return int(root)


def dft_support(values: list[int], q: int) -> int | None:
    m = len(values)
    zeta = primitive_root_of_order(q, m)
    if zeta is None:
        return None
    support = 0
    for s in range(m):
        total = 0
        for r, value in enumerate(values):
            total = (total + pow(zeta, s * r, q) * value) % q
        if total:
            support += 1
    return support


def find_splitting_prime(pari: Pari, hilbert, h: int, start: int = 101, stop: int = 10_000) -> tuple[int, list[int]] | None:
    for q in sp.primerange(max(start, h + 2), stop):
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            return int(q), roots
    return None


def find_full_cycle_prime(roots: list[int], D: int, q: int, ell_bound: int = 43) -> tuple[int, list[int]] | None:
    for ell in sp.primerange(2, ell_bound + 1):
        if D % ell == 0 or sp.kronecker_symbol(D, ell) != 1:
            continue
        graph = isogeny_neighbors(roots, int(ell), q)
        if sorted({len(v) for v in graph.values()}) != [2]:
            continue
        try:
            cycle = walk_cycle(graph)
        except ValueError:
            continue
        if len(cycle) == len(roots):
            return int(ell), cycle
    return None


def period_sequence(cycle: list[int], quotient_size: int, q: int) -> list[int]:
    h = len(cycle)
    subgroup_size = h // quotient_size
    return [
        sum(cycle[(r + k * quotient_size) % h] for k in range(subgroup_size)) % q
        for r in range(quotient_size)
    ]


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    # Include D=-5000 because it is the calibrated p24 analogue, then scan a
    # small deterministic window for a few more examples.
    discriminants = [-5000] + [
        D for D in range(-200, -6001, -1)
        if D % 4 in (0, 1)
    ]

    seen: set[int] = set()
    cases = 0
    max_cases = 6
    print("cycle period complexity scan")
    print("columns: D q generator_ell h quotient_m bm_complexity bm_over_m dft_support")
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (12 <= h <= 80):
            continue
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        quotient_sizes = divisors_between(h, 6, min(40, h // 2))
        if not quotient_sizes:
            continue
        printed_for_case = False
        for m in quotient_sizes[:4]:
            values = period_sequence(cycle, m, q)
            complexity = bm_linear_complexity(values * 2, q)
            support = dft_support(values, q)
            support_text = "NA" if support is None else str(support)
            print(
                f"D={D:6d} q={q:5d} ell={ell:2d} h={h:3d} "
                f"m={m:3d} bm={complexity:3d} bm_over_m={complexity / m:5.2f} "
                f"dft_support={support_text}"
            )
            printed_for_case = True
        if printed_for_case:
            cases += 1
            if cases >= max_cases:
                break
    print()
    print("interpretation")
    print("  low_bm_complexity_or_sparse_dft_would_suggest_extra_period_structure=1")
    print("  random_like_bm_near_m_and_full_dft_support_supports_high_order_trace_barrier=1")
    print("  scan_is_small_and_toy_scale_only=1")
    print("conclusion=reported_small_cm_period_complexity_scan")


if __name__ == "__main__":
    main()

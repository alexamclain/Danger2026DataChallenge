#!/usr/bin/env python3
"""Toy complexity scan for full-generator CM crater sequences.

The first p24 theorem toy has an unusually clean property: the split prime
above 2 generates the whole CM class group.  If a Serre-Tate/Landen/crater
coordinate made this generator action into an elementary torus rotation with
a cheap j-evaluation map, small complete CM examples should show some trace:
low linear complexity, sparse Fourier support, or a simple low-degree
recurrence in the j_i sequence along a full split-prime cycle.

This scan deliberately stays toy-scale.  It builds complete CM root sets over
small splitting primes, finds a small split prime giving a full cycle, then
measures Berlekamp-Massey complexity for simple transforms of the generator
sequence.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle
from cycle_period_complexity_scan import bm_linear_complexity, dft_support


@dataclass(frozen=True)
class Case:
    D: int
    q: int
    ell: int
    h: int
    cycle: list[int]


def find_splitting_prime(pari: Pari, hilbert, h: int, start: int = 101, stop: int = 20000) -> tuple[int, list[int]] | None:
    for q in sp.primerange(max(start, h + 2), stop):
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            return int(q), roots
    return None


def find_full_cycle(roots: list[int], D: int, q: int, ell_bound: int) -> tuple[int, list[int]] | None:
    for ell in sp.primerange(2, ell_bound + 1):
        ell = int(ell)
        if abs(D) % ell == 0 or sp.kronecker_symbol(D, ell) != 1:
            continue
        graph = isogeny_neighbors(roots, ell, q)
        if sorted({len(v) for v in graph.values()}) != [2]:
            continue
        try:
            cycle = walk_cycle(graph)
        except ValueError:
            continue
        if len(cycle) == len(roots):
            return ell, cycle
    return None


def inv_or_zero(x: int, q: int) -> int:
    return pow(x, -1, q) if x % q else 0


def transforms(cycle: list[int], q: int) -> dict[str, list[int]]:
    h = len(cycle)
    diffs = [(cycle[(i + 1) % h] - cycle[i]) % q for i in range(h)]
    ratios = [cycle[(i + 1) % h] * inv_or_zero(cycle[i], q) % q for i in range(h)]
    edge_sums = [(cycle[i] + cycle[(i + 1) % h]) % q for i in range(h)]
    edge_products = [cycle[i] * cycle[(i + 1) % h] % q for i in range(h)]
    return {
        "j": cycle,
        "delta_j": diffs,
        "ratio_j": ratios,
        "edge_sum": edge_sums,
        "edge_product": edge_products,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-d", type=int, default=12000)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=90)
    ap.add_argument("--ell-bound", type=int, default=43)
    ap.add_argument("--max-cases", type=int, default=8)
    args = ap.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    cases: list[Case] = []

    preferred = [-5000]
    scan = [D for D in range(-200, -args.max_abs_d - 1, -1) if D % 4 in (0, 1)]
    for D in preferred + scan:
        if any(case.D == D for case in cases):
            continue
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if h < args.min_h or h > args.max_h:
            continue
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle(roots, D, q, args.ell_bound)
        if full is None:
            continue
        ell, cycle = full
        cases.append(Case(D, q, ell, h, cycle))
        if len(cases) >= args.max_cases:
            break

    print("generator crater sequence complexity")
    print(f"max_abs_d={args.max_abs_d}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"ell_bound={args.ell_bound}")
    print(f"case_count={len(cases)}")
    print("columns: D q ell h transform distinct bm bm_over_h dft_support")
    for case in cases:
        for name, seq in transforms(case.cycle, case.q).items():
            bm = bm_linear_complexity(seq * 2, case.q)
            support = dft_support(seq, case.q)
            print(
                f"D={case.D:6d} q={case.q:5d} ell={case.ell:2d} h={case.h:3d} "
                f"{name:12s} distinct={len(set(seq)):3d} bm={bm:3d} "
                f"bm_over_h={bm / case.h:5.2f} "
                f"dft_support={'NA' if support is None else support}"
            )
        print()

    print("interpretation")
    print("  low_complexity_generator_sequence_would_support_hidden_torus_coordinate=1")
    print("  full_complexity_simple_transforms_support_crater_coordinate_barrier=1")
    print("  toy_scan_does_not_rule_out_deep_Serre_Tate_identities=1")
    print("conclusion=reported_generator_crater_sequence_complexity")


if __name__ == "__main__":
    main()

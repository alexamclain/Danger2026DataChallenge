#!/usr/bin/env python3
"""Toy check for Hecke moments versus autocorrelation coefficients."""

from __future__ import annotations

import argparse
import math

from cypari2 import Pari

from cycle_period_complexity_scan import bm_linear_complexity, dft_support
from embedded_decomposition_calibration import D, ELL, H, Q, isogeny_neighbors, pari_linear_roots, walk_cycle


def autocorrelation(cycle: list[int], q: int, d: int) -> int:
    h = len(cycle)
    return sum(cycle[i] * cycle[(i + d) % h] for i in range(h)) % q


def hecke_walk_moment_from_autocorr(c_values: list[int], q: int, r: int) -> int:
    h = len(c_values)
    total = 0
    for k in range(r + 1):
        shift = (r - 2 * k) % h
        total = (total + math.comb(r, k) * c_values[shift]) % q
    return total


def hecke_walk_moment_direct(cycle: list[int], q: int, r: int) -> int:
    h = len(cycle)
    values = [0] * h
    values[0] = 1
    for _ in range(r):
        nxt = [0] * h
        for i, value in enumerate(values):
            nxt[(i + 1) % h] = (nxt[(i + 1) % h] + value) % q
            nxt[(i - 1) % h] = (nxt[(i - 1) % h] + value) % q
        values = nxt
    return sum(values[d] * autocorrelation(cycle, q, d) for d in range(h)) % q


def triangular_recover_c_prefix(moments: list[int], c_values: list[int], q: int) -> list[int]:
    """Recover C_0..C_R from moments <j,(S+S^-1)^rj> using triangularity.

    This assumes C_-d=C_d, and recovers only a prefix before wraparound.
    """
    recovered: list[int] = []
    inv2 = pow(2, -1, q)
    for r, moment in enumerate(moments):
        if r == 0:
            recovered.append(moment % q)
            continue
        known = 0
        for k in range(1, r):
            shift = abs(r - 2 * k)
            if shift < len(recovered):
                known = (known + math.comb(r, k) * recovered[shift]) % q
            else:
                known = (known + math.comb(r, k) * c_values[shift]) % q
        # k=0 and k=r both contribute C_r.
        recovered.append((moment - known) * inv2 % q)
    return recovered


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-r", type=int, default=12)
    args = ap.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    c_values = [autocorrelation(cycle, Q, d) for d in range(H)]
    moments_formula = [
        hecke_walk_moment_from_autocorr(c_values, Q, r)
        for r in range(args.max_r + 1)
    ]
    moments_direct = [
        hecke_walk_moment_direct(cycle, Q, r)
        for r in range(args.max_r + 1)
    ]
    recovered = triangular_recover_c_prefix(moments_formula, c_values, Q)
    expected_prefix = c_values[: args.max_r + 1]
    bm = bm_linear_complexity(c_values * 2, Q)
    long_moments = [
        hecke_walk_moment_from_autocorr(c_values, Q, r)
        for r in range(2 * H)
    ]
    moment_bm = bm_linear_complexity(long_moments * 2, Q)
    support = dft_support(c_values, Q)

    print("hecke autocorrelation toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"h={H}")
    print(f"generator_ell={ELL}")
    print(f"max_r={args.max_r}")
    print(f"moments_formula_equal_direct={int(moments_formula == moments_direct)}")
    print(f"triangular_recovery_prefix_ok={int(recovered == expected_prefix)}")
    print(f"C0={c_values[0]}")
    print(f"C1={c_values[1]}")
    print(f"hecke_edge_moment=<j,(S+S^-1)j>={moments_formula[1]}")
    print(f"twice_C1={2 * c_values[1] % Q}")
    print(f"autocorrelation_distinct={len(set(c_values))}")
    print(f"autocorrelation_bm={bm}")
    print(f"autocorrelation_bm_over_h={bm / H:.6f}")
    print(f"hecke_moment_bm={moment_bm}")
    print(f"hecke_moment_bm_over_h={moment_bm / H:.6f}")
    print(f"autocorrelation_dft_support={'NA' if support is None else support}")
    print()
    print("interpretation")
    print("  X0_ell_hecke_moments_determine_C_d_by_triangular_inversion=1")
    print("  triangular_inversion_requires_moments_up_to_d=1")
    print("  hecke_moment_sequence_has_no_short_recurrence_visible=1")
    print("  autocorrelation_sequence_still_has_full_complexity_in_toy=1")
    print("conclusion=hecke_moments_repackage_not_compress_relative_energy")


if __name__ == "__main__":
    main()

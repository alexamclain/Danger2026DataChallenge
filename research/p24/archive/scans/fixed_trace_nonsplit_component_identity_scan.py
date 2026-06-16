#!/usr/bin/env python3
"""Verify fixed-trace+nonsplit equals the conductor-2 CM component set.

Finite-field identity under test:

    {j(A): tr(E_A)=+-t and A^2-4 nonsquare} = roots(H_{4D})

when p == 7 mod 8, t == 0 mod 8, and t^2-4p=4D with D fundamental
and D == 1 mod 8.  The component-sum statement for a split odd ell then
follows by restricting Phi_ell to either side.

This identity is useful bookkeeping, not the p24 asymptotic shortcut: computing
the left side naively by scanning A is sqrt-scale in the target family.
"""

from __future__ import annotations

import argparse
from math import isqrt

from cypari2 import Pari

from conductor2_component_transfer_toy import components
from conductor2_nonsplit_gate_scan import is_prime, is_squarefree
from embedded_decomposition_calibration import isogeny_neighbors
from fixed_trace_cm_root_toy import pari_linear_roots
from fixed_trace_montgomery_verifier_toy import legendre, montgomery_j_from_A, montgomery_trace


def fixed_trace_nonsplit_j_values(p: int, t: int) -> set[int]:
    out: set[int] = set()
    for A in range(p):
        if legendre(A * A - 4, p) != -1:
            continue
        j = montgomery_j_from_A(A, p)
        if j is None:
            continue
        trace = montgomery_trace(A, p)
        if trace is not None and abs(trace) == t:
            out.add(j)
    return out


def cycle_sums(roots: list[int], ell: int, p: int) -> list[int] | None:
    graph = isogeny_neighbors(roots, ell, p)
    if sorted({len(v) for v in graph.values()}) != [2]:
        return None
    return sorted(sum(comp) % p for comp in components(graph))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-p", type=int, default=800)
    parser.add_argument("--max-h", type=int, default=40)
    parser.add_argument("--max-ell", type=int, default=17)
    parser.add_argument("--max-component-size", type=int, default=6)
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows = 0
    failures = 0
    component_failures = 0
    print("fixed trace nonsplit component identity scan")
    print("p t D h ell components root_set_equal component_sums_equal")
    for p in range(7, args.max_p + 1):
        if p % 8 != 7 or not is_prime(p):
            continue
        for t in range(8, 2 * isqrt(p) + 1, 8):
            D4 = t * t - 4 * p
            if D4 >= 0 or D4 % 4 != 0:
                continue
            D = D4 // 4
            if D % 8 != 1 or not is_squarefree(abs(D)):
                continue
            h = int(pari.poldegree(pari.polclass(D)))
            h2 = int(pari.poldegree(pari.polclass(4 * D)))
            if h > args.max_h or h2 > args.max_h:
                continue
            c2_roots = sorted(pari_linear_roots(pari.polclass(4 * D), p))
            ns_roots = sorted(fixed_trace_nonsplit_j_values(p, t))
            root_set_equal = ns_roots == c2_roots
            failures += 0 if root_set_equal else 1
            for ell in range(3, args.max_ell + 1, 2):
                if not is_prime(ell) or ell == p:
                    continue
                c2_sums = cycle_sums(c2_roots, ell, p)
                ns_sums = cycle_sums(ns_roots, ell, p)
                if c2_sums is None or ns_sums is None:
                    continue
                component_size = len(c2_roots) // len(c2_sums)
                if component_size > args.max_component_size:
                    continue
                component_equal = c2_sums == ns_sums
                component_failures += 0 if component_equal else 1
                rows += 1
                print(
                    f"{p} {t} {D} {h} {ell} {len(c2_sums)} "
                    f"{int(root_set_equal)} {int(component_equal)}"
                )
                if rows >= args.max_rows:
                    print()
                    print(f"rows={rows}")
                    print(f"root_set_failures={failures}")
                    print(f"component_failures={component_failures}")
                    print(f"all_passed={int(failures == 0 and component_failures == 0)}")
                    print("conclusion=reported_fixed_trace_nonsplit_component_identity_scan")
                    return

    print()
    print(f"rows={rows}")
    print(f"root_set_failures={failures}")
    print(f"component_failures={component_failures}")
    print(f"all_passed={int(failures == 0 and component_failures == 0)}")
    print("conclusion=reported_fixed_trace_nonsplit_component_identity_scan")


if __name__ == "__main__":
    main()

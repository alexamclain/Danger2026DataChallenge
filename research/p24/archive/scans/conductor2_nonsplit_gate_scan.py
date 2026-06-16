#!/usr/bin/env python3
"""Scan the conductor-2 versus nonsplit-Montgomery gate.

For p24 the strict traces have

    t^2 - 4p = 4*D_K,    D_K == 1 mod 8,

so the Frobenius order has conductor 2 in the maximal order.  The small
`fixed_trace_montgomery_verifier_toy.py` suggests that maximal-order roots
map to split Montgomery parameters, while conductor-2 roots map to nonsplit
Montgomery parameters.  This script tests that statement across small
ordinary rows where the Hilbert class polynomials are tiny.
"""

from __future__ import annotations

import argparse
from math import isqrt

from cypari2 import Pari

from fixed_trace_cm_root_toy import pari_linear_roots
from fixed_trace_montgomery_verifier_toy import (
    legendre,
    montgomery_j_from_A,
    montgomery_trace,
)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def is_squarefree(n: int) -> bool:
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1 if d == 2 else 2
    return True


def torsion_shape(A: int, p: int) -> str:
    return "split" if legendre(A * A - 4, p) == 1 else "nonsplit"


def row_counts(p: int, t: int, maximal_roots: set[int], conductor2_roots: set[int]) -> dict[str, int]:
    counts = {
        "maximal_split": 0,
        "maximal_nonsplit": 0,
        "conductor2_split": 0,
        "conductor2_nonsplit": 0,
        "other_split": 0,
        "other_nonsplit": 0,
    }
    for A in range(p):
        j = montgomery_j_from_A(A, p)
        if j is None:
            continue
        trace = montgomery_trace(A, p)
        if trace is None or abs(trace) != t:
            continue
        bucket = (
            "maximal"
            if j in maximal_roots
            else "conductor2"
            if j in conductor2_roots
            else "other"
        )
        counts[f"{bucket}_{torsion_shape(A, p)}"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-p", type=int, default=800)
    parser.add_argument("--max-h", type=int, default=40)
    parser.add_argument("--max-rows", type=int, default=30)
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)

    tested = 0
    failures = 0
    print("conductor2 nonsplit gate scan")
    print(f"max_p={args.max_p}")
    print(f"max_h={args.max_h}")
    print("p t D h counts gate_ok")
    for p in range(7, args.max_p + 1):
        if p % 8 != 7 or not is_prime(p):
            continue
        for t in range(8, 2 * isqrt(p) + 1, 8):
            delta = t * t - 4 * p
            if delta >= 0 or delta % 4 != 0:
                continue
            D = delta // 4
            if D % 8 != 1 or not is_squarefree(abs(D)):
                continue
            maximal_hilbert = pari.polclass(D)
            conductor2_hilbert = pari.polclass(4 * D)
            h = int(pari.poldegree(maximal_hilbert))
            h2 = int(pari.poldegree(conductor2_hilbert))
            if h > args.max_h or h2 > args.max_h:
                continue
            maximal_roots = set(pari_linear_roots(maximal_hilbert, p))
            conductor2_roots = set(pari_linear_roots(conductor2_hilbert, p))
            counts = row_counts(p, t, maximal_roots, conductor2_roots)
            gate_ok = (
                counts["maximal_nonsplit"] == 0
                and counts["conductor2_split"] == 0
                and counts["other_split"] == 0
                and counts["other_nonsplit"] == 0
                and counts["maximal_split"] > 0
                and counts["conductor2_nonsplit"] > 0
            )
            tested += 1
            failures += 0 if gate_ok else 1
            print(f"{p} {t} {D} {h} {counts} {int(gate_ok)}")
            if tested >= args.max_rows:
                print()
                print(f"tested_rows={tested}")
                print(f"failures={failures}")
                print(f"all_gate_ok={int(failures == 0)}")
                print("conclusion=reported_conductor2_nonsplit_gate_scan")
                return

    print()
    print(f"tested_rows={tested}")
    print(f"failures={failures}")
    print(f"all_gate_ok={int(failures == 0)}")
    print("conclusion=reported_conductor2_nonsplit_gate_scan")


if __name__ == "__main__":
    main()

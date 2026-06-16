#!/usr/bin/env python3
"""Search for small-CM traces compatible with the p24 DANGER depth.

For a CM shortcut we need a trace t in the Hasse interval with

    p + 1 - t == 0 mod 2^40

or, for x-only/twist use, the signed trace set.  The actual compatible traces
are very few.  This script audits them and also scans small fundamental
negative discriminants D to see whether any equation

    t^2 - 4p = D*f^2

can hold with the DANGER trace congruence.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp
from sympy.ntheory.modular import crt

P24 = 10**24 + 7
K = 40


def v2(n: int) -> int:
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def is_fundamental_negative_discriminant(D: int) -> bool:
    def is_squarefree(n: int) -> bool:
        return all(exp == 1 for exp in sp.factorint(abs(n)).values())

    if D >= 0:
        return False
    if D % 4 == 1:
        return is_squarefree(D)
    if D % 4 == 0:
        d = D // 4
        return d % 4 in (2, 3) and is_squarefree(d)
    return False


def compatible_traces(p: int, k: int) -> list[int]:
    bound = math.isqrt(4 * p)
    mod = 1 << k
    traces = []
    for t in range(-bound + ((p + 1 + bound) % mod), bound + 1, mod):
        traces.append(t)
    return traces


def squarefree_part(n: int) -> int:
    factors = sp.factorint(abs(n))
    out = 1
    for prime, exp in factors.items():
        if exp % 2:
            out *= prime
    return out


def fundamental_D_from_delta(delta: int) -> int:
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def scan_small_D(max_abs_D: int) -> list[tuple[int, int, int]]:
    hits = []
    mod = 1 << K
    bound = math.isqrt(4 * P24)
    for abs_D in range(3, max_abs_D + 1):
        for D in (-abs_D,):
            if not is_fundamental_negative_discriminant(D):
                continue
            # t^2 = 4p mod |D|.  Roots modulo |D| are enough for this small
            # audit; for each root, check the Hasse-sized candidates.
            roots = sp.sqrt_mod((4 * P24) % abs_D, abs_D, all_roots=True)
            for root in roots:
                for sign_root in {int(root), (-int(root)) % abs_D}:
                    combined = crt([abs_D, mod], [sign_root, (P24 + 1) % mod], check=True)
                    if combined is None:
                        continue
                    residue, modulus = (int(combined[0]), int(combined[1]))
                    first = -bound + ((residue + bound) % modulus)
                    t = first
                    while t <= bound:
                        if (P24 + 1 - t) % mod == 0:
                            q = (t * t - 4 * P24) // D
                            if q >= 0 and math.isqrt(q) ** 2 == q:
                                hits.append((D, t, math.isqrt(q)))
                        t += modulus
    return sorted(set(hits))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=5000)
    args = ap.parse_args()

    traces = compatible_traces(P24, K)
    signed = sorted(set(traces) | {-t for t in traces})
    print("p24 small-CM trace search")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"compatible_traces={traces}")
    print(f"signed_xonly_traces={signed}")
    print()
    print("actual_compatible_trace_discriminants")
    for t in traces:
        delta = t * t - 4 * P24
        print(
            f"t={t:15d} v2_order={v2(P24 + 1 - t):2d} "
            f"fundamental_D={fundamental_D_from_delta(delta)} "
            f"squarefree_abs={squarefree_part(delta)}"
        )

    hits = scan_small_D(args.max_abs_D)
    print()
    print(f"small_fundamental_D_hits={len(hits)}")
    for D, t, f in hits[:20]:
        print(f"D={D} t={t} conductor_factor={f}")
    print("conclusion=no_small_CM_D_hits_in_scanned_range" if not hits else "conclusion=review_hits")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Explicit class-number-one CM audit for p24 strict DANGER traces.

The only CM families that can plausibly beat sqrt(p) outright are the tiny
class-number-one orders, especially the exceptional automorphism cases
j = 0 (D=-3) and j = 1728 (D=-4).  The general small-D scan already covers
these, but this script records the exact Heegner list and the available traces
for p = 10^24 + 7 in one small, reproducible place.
"""

from __future__ import annotations

import math

import sympy as sp
from sympy.ntheory.modular import crt

P24 = 10**24 + 7
K = 40
M = 1 << K
HEEGNER_D = (-3, -4, -7, -8, -11, -19, -43, -67, -163)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def cornacchia(d: int, m: int, roots: list[int]) -> list[tuple[int, int]]:
    """Solve x^2 + d*y^2 = m from square roots of -d modulo m."""
    out: list[tuple[int, int]] = []
    for root in roots:
        a, b = m, min(root % m, (-root) % m)
        while b * b > m:
            a, b = b, a % b
        x = b
        rem = m - x * x
        if rem >= 0 and rem % d == 0:
            y2 = rem // d
            y = math.isqrt(y2)
            if y * y == y2:
                out.append((x, y))
                if x:
                    out.append((-x, y))
    return sorted(set(out))


def roots_mod_4p_for_odd_d(d: int) -> list[int]:
    roots_p = sp.sqrt_mod((-d) % P24, P24, all_roots=True)
    roots_4 = [1, 3]  # all odd Heegner |D| are 3 mod 4, so -|D| == 1 mod 4.
    out: set[int] = set()
    for root_p in roots_p:
        for root_4 in roots_4:
            combined = crt([4, P24], [root_4, int(root_p)], check=True)
            if combined is not None:
                out.add(int(combined[0]) % (4 * P24))
    return sorted(out)


def traces_for_fundamental_D(D: int) -> list[tuple[int, int]]:
    """Return (trace, conductor_factor) for 4p = t^2 + |D| f^2."""
    d = abs(D)
    if D == -4:
        # t^2 + 4f^2 = 4p => (t/2)^2 + f^2 = p.
        roots = sp.sqrt_mod(-1 % P24, P24, all_roots=True)
        return [(2 * x, y) for x, y in cornacchia(1, P24, [int(root) for root in roots])]
    if D == -8:
        # t^2 + 8f^2 = 4p => (t/2)^2 + 2f^2 = p.
        roots = sp.sqrt_mod(-2 % P24, P24, all_roots=True)
        return [(2 * x, y) for x, y in cornacchia(2, P24, [int(root) for root in roots])]
    # For odd D == 1 mod 4, solutions to t^2 + |D|f^2 = 4p can have t,f
    # both odd, or both even.  The even/even case reduces to
    # (t/2)^2 + |D|*(f/2)^2 = p and includes the p=n^2+7, D=-7 trace.
    out = cornacchia(d, 4 * P24, roots_mod_4p_for_odd_d(d))
    roots_p = sp.sqrt_mod((-d) % P24, P24, all_roots=True)
    out.extend((2 * x, 2 * y) for x, y in cornacchia(d, P24, [int(root) for root in roots_p]))
    return sorted(set(out))


def target_trace_set() -> set[int]:
    bound = math.isqrt(4 * P24)
    r = (P24 + 1) % M
    out: set[int] = set()
    for residue in {r, (-r) % M}:
        t = -bound + ((residue + bound) % M)
        while t <= bound:
            out.add(t)
            t += M
    return out


def main() -> None:
    targets = target_trace_set()
    print("p24 class-number-one CM audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"target_traces={sorted(targets)}")
    print("D traces")
    any_hit = False
    for D in HEEGNER_D:
        traces = traces_for_fundamental_D(D)
        print(f"D={D}")
        if not traces:
            print("  no_trace_over_Fp")
            continue
        for trace, conductor in traces:
            order = P24 + 1 - trace
            twist = P24 + 1 + trace
            hit = trace in targets or -trace in targets
            any_hit = any_hit or hit
            print(
                f"  trace={trace} conductor_factor={conductor} "
                f"trace_mod_2^40={trace % M} "
                f"v2_order={v2(order)} v2_twist={v2(twist)} "
                f"strict_target_hit={hit}"
            )
    print("conclusion=class_number_one_CM_has_no_strict_DANGER_trace" if not any_hit else "conclusion=review_hit")


if __name__ == "__main__":
    main()

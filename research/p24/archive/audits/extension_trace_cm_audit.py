#!/usr/bin/env python3
"""Audit small extension-field/descent shortcuts for p24 target traces.

If E/F_p has Frobenius trace t, then over F_{p^m} its trace T_m satisfies

    T_0 = 2, T_1 = t, T_m = t*T_{m-1} - p*T_{m-2}.

One might hope that a target p24 curve becomes a cheap small-CM curve over a
small extension field and can then be descended.  But the CM field is
unchanged.  Indeed

    T_m^2 - 4*p^m = (t^2 - 4*p) * U_{m-1}(t,p)^2,

where U is the corresponding Lucas/Chebyshev factor.  Thus the squarefree
part, and hence the fundamental CM field discriminant, is the same at every
extension degree.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(n).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def extension_trace(t: int, m: int) -> int:
    if m == 0:
        return 2
    if m == 1:
        return t
    a, b = 2, t
    for _ in range(2, m + 1):
        a, b = b, t * b - P24 * a
    return b


def lucas_factor(t: int, m_minus_1: int) -> int:
    # U_0=1, U_1=t, U_n=t*U_{n-1}-p*U_{n-2}.
    if m_minus_1 == 0:
        return 1
    if m_minus_1 == 1:
        return t
    a, b = 1, t
    for _ in range(2, m_minus_1 + 1):
        a, b = b, t * b - P24 * a
    return b


def short(n: int) -> str:
    s = str(abs(n))
    sign = "-" if n < 0 else ""
    if len(s) <= 32:
        return sign + s
    return f"{sign}{s[:14]}...{s[-14:]} (digits={len(s)})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-m", type=int, default=8)
    args = ap.parse_args()

    print("p24 extension-field CM descent audit")
    print(f"p={P24}")
    print(f"max_m={args.max_m}")
    print()

    for t in TARGET_TRACES:
        base_abs_delta = 4 * P24 - t * t
        sf = squarefree_part(base_abs_delta)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        print(f"base_trace={t}")
        print(f"  base_abs_delta={base_abs_delta}")
        print(f"  base_squarefree_part={sf}")
        print(f"  base_fundamental_D_K={D_K}")
        for m in range(2, args.max_m + 1):
            Tm = extension_trace(t, m)
            U = lucas_factor(t, m - 1)
            # Avoid constructing p^m-sized discriminants for no reason; verify
            # the exact factor formula for the small m values anyway.
            lhs = Tm * Tm - 4 * pow(P24, m)
            rhs = (t * t - 4 * P24) * U * U
            if lhs != rhs:
                raise AssertionError(f"extension discriminant identity failed for t={t} m={m}")
            print(
                f"  m={m} T_m={short(Tm)} "
                f"lucas_digits={len(str(abs(U)))} "
                f"same_fundamental_D=True"
            )
        print()

    print("conclusion=extension_traces_only_multiply_the_large_target_discriminant_by_a_square")


if __name__ == "__main__":
    main()

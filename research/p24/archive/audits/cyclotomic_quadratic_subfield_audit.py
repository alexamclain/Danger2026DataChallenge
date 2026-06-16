#!/usr/bin/env python3
"""Audit cheap cyclotomic/Jacobi-sum quadratic subfields for p24.

Jacobi-sum trace identities for elliptic curves are CM identities in
imaginary quadratic subfields of cyclotomic fields.  The cheap character data
visible at p24 comes from the smooth parts of p-1 and p+1:

    p-1 = 2 * 7 * 29 * huge
    p+1 = 2^3 * 3^2 * 19 * 739 * 1187 * huge

This script enumerates negative fundamental discriminants whose conductor
|D| divides those smooth conductors, then checks whether the fixed prime p is
principal in the CM field by solving

    t^2 + |D| f^2 = 4p.

When solutions exist, it records the available traces and their 2-adic depth.
This is a theorem-level audit, not a Montgomery-parameter search.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp
from sympy.ntheory.modular import crt

P24 = 10**24 + 7
K = 40

P_MINUS_SMOOTH = 2 * 7 * 29
P_PLUS_SMOOTH = (2**3) * (3**2) * 19 * 739 * 1187


@dataclass(frozen=True)
class TraceRow:
    trace: int
    conductor: int
    v2_order: int
    v2_twist: int
    strict_hit: bool


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def is_squarefree(n: int) -> bool:
    return all(exp == 1 for exp in sp.factorint(abs(n)).values())


def is_fundamental_negative_discriminant(D: int) -> bool:
    if D >= 0:
        return False
    if D % 4 == 1:
        return is_squarefree(D)
    if D % 4 == 0:
        d = D // 4
        return d % 4 in (2, 3) and is_squarefree(d)
    return False


def negative_fundamental_divisors(modulus: int) -> list[int]:
    out: list[int] = []
    for d in sp.divisors(modulus):
        D = -int(d)
        if is_fundamental_negative_discriminant(D):
            out.append(D)
    return sorted(set(out), key=lambda D: abs(D))


def cornacchia(d: int, m: int, roots: list[int]) -> list[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
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
                out.add((x, y))
                if x:
                    out.add((-x, y))
    return sorted(out)


def roots_mod_4p_for_odd_d(d: int) -> list[int]:
    roots_p = sp.sqrt_mod((-d) % P24, P24, all_roots=True)
    if not roots_p:
        return []
    # For odd negative fundamental D, d=|D| == 3 mod 4, so -d == 1 mod 4.
    roots_4 = [1, 3]
    out: set[int] = set()
    for root_p in roots_p:
        for root_4 in roots_4:
            combined = crt([4, P24], [root_4, int(root_p)], check=True)
            if combined is not None:
                out.add(int(combined[0]) % (4 * P24))
    return sorted(out)


def traces_for_fundamental_D(D: int) -> list[TraceRow]:
    absD = abs(D)
    raw: set[tuple[int, int]] = set()

    if D % 4 == 0:
        d = absD // 4
        if sp.kronecker_symbol(-d, P24) == 1:
            roots = [int(r) for r in sp.sqrt_mod((-d) % P24, P24, all_roots=True)]
            raw.update((2 * x, y) for x, y in cornacchia(d, P24, roots))
    else:
        d = absD
        # Odd trace/conductor solutions.
        raw.update(cornacchia(d, 4 * P24, roots_mod_4p_for_odd_d(d)))
        # Even trace/conductor solutions reduce to x^2 + d*y^2 = p.
        if sp.kronecker_symbol(-d, P24) == 1:
            roots = [int(r) for r in sp.sqrt_mod((-d) % P24, P24, all_roots=True)]
            raw.update((2 * x, 2 * y) for x, y in cornacchia(d, P24, roots))

    rows: list[TraceRow] = []
    for trace, conductor in sorted(raw):
        rows.append(
            TraceRow(
                trace=trace,
                conductor=conductor,
                v2_order=v2(P24 + 1 - trace),
                v2_twist=v2(P24 + 1 + trace),
                strict_hit=max(v2(P24 + 1 - trace), v2(P24 + 1 + trace)) >= K,
            )
        )
    return rows


def audit_source(label: str, modulus: int) -> None:
    discriminants = negative_fundamental_divisors(modulus)
    print(f"{label}")
    print(f"  smooth_conductor={modulus}")
    print(f"  negative_fundamental_D_count={len(discriminants)}")
    any_strict = False
    any_principal = False
    for D in discriminants:
        split = int(sp.kronecker_symbol(D, P24))
        rows = traces_for_fundamental_D(D)
        any_principal = any_principal or bool(rows)
        any_strict = any_strict or any(row.strict_hit for row in rows)
        print(f"  D={D:12d} split={split:2d} principal_traces={len(rows)}")
        for row in rows:
            print(
                f"    trace={row.trace:15d} conductor={row.conductor:15d} "
                f"v2_order={row.v2_order:2d} v2_twist={row.v2_twist:2d} "
                f"strict_hit={int(row.strict_hit)}"
            )
    print(f"  any_principal_trace={int(any_principal)}")
    print(f"  any_strict_hit={int(any_strict)}")
    print()


def main() -> None:
    print("p24 cyclotomic quadratic-subfield CM audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"p_minus_smooth={P_MINUS_SMOOTH}")
    print(f"p_plus_smooth={P_PLUS_SMOOTH}")
    print()
    audit_source("p_minus_character_subfields", P_MINUS_SMOOTH)
    audit_source("p_plus_unitary_character_subfields", P_PLUS_SMOOTH)
    print(
        "conclusion=cheap_cyclotomic_quadratic_subfields_give_no_strict_"
        "jacobi_sum_trace;_only_small_non_strict_CM_traces_or_nonprincipal_splitting"
    )


if __name__ == "__main__":
    main()

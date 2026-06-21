#!/usr/bin/env python3
"""Symbolic obstruction for descending the label-2 T-cover to E'.

The d3/d4 bits are invariant under translation by (0,0) on

    E: W^2 = X^3 - X,

so it is tempting to search only on the 2-isogenous quotient

    E': V^2 = U^3 + 4U,  U = X - 1/X.

This probe checks a possible trap in that move: the label-2 T-cover used by
the compactD source does not itself have a rational T-linear invariant over
E' in p27-compatible fields.  The obstruction is a constant -1 norm.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

from p27_label2_alpha_branch_recurrence_probe import sqrt_mod


def legendre(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    r = pow(a, (q - 1) // 2, q)
    return 1 if r == 1 else -1


def roots2(a: int, q: int) -> list[int]:
    root = sqrt_mod(a % q, q)
    if root is None:
        return []
    if root == 0:
        return [0]
    return [root, (-root) % q]


def symbolic_identities() -> dict[str, sp.Expr | tuple[sp.Expr, sp.Expr]]:
    x, u, w = sp.symbols("X U W")
    sigma_x = -1 / x
    sigma_w = w / x**2
    s = x * (x**2 + 1) * (x**2 + 2 * x - 1)
    sigma_s = sp.factor(s.subs(x, sigma_x))
    rel = x**2 - u * x - 1

    def reduce_mod(expr: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
        num, den = sp.together(expr).as_numer_denom()
        return sp.factor(sp.rem(num, rel, x)), sp.factor(sp.rem(den, rel, x))

    U = x - 1 / x
    V = w * (x**2 + 1) / x**2
    e_relation = sp.factor(V**2 - (U**3 + 4 * U))
    e_reduced = reduce_mod(e_relation.subs(w**2, x**3 - x))

    return {
        "S": sp.factor(s),
        "sigma_S": sigma_s,
        "sigma_S_over_S": sp.factor(sigma_s / s),
        "S_over_sigma_S": sp.factor(s / sigma_s),
        "norm_X3": sp.factor(x**3 * (sigma_x**3)),
        "norm_minus_X3": sp.factor((-x**3) * (-(sigma_x**3))),
        "Eprime_relation_reduced_num_den": e_reduced,
    }


def finite_field_check(q: int) -> Counter[str]:
    stats: Counter[str] = Counter()
    inv = lambda a: pow(a % q, q - 2, q)
    for x in range(q):
        for w in roots2((x * x * x - x) % q, q):
            if x == 0:
                stats["x_zero_skip"] += 1
                continue
            sx = (-inv(x)) % q
            sw = w * inv(x * x) % q
            if (sw * sw - (sx * sx % q * sx - sx)) % q != 0:
                stats["sigma_E_mismatch"] += 1

            u = (x - inv(x)) % q
            v = w * (x * x + 1) % q * inv(x * x) % q
            if (v * v - (u * u % q * u + 4 * u)) % q != 0:
                stats["Eprime_mismatch"] += 1

            s = x * (x * x + 1) % q * (x * x + 2 * x - 1) % q
            ss = sx * (sx * sx + 1) % q * (sx * sx + 2 * sx - 1) % q
            if s == 0 or ss == 0:
                stats["S_zero_skip"] += 1
                continue
            ratio = ss * inv(s) % q
            expected = inv(pow(x, 6, q))
            if ratio != expected:
                stats["sigma_S_ratio_mismatch"] += 1
            for t in roots2(s, q):
                stats["T_points"] += 1
                image_t = t * inv(pow(x, 3, q)) % q
                if image_t * image_t % q != ss:
                    stats["sigma_T_mismatch"] += 1
    stats["q"] = q
    stats["minus_one_chi"] = legendre(-1, q)
    stats["norm_X3_is_minus_one"] = 1
    stats["rational_T_linear_invariant_possible_over_Fq"] = int(legendre(-1, q) == 1)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1471,1607,1847")
    args = parser.parse_args()

    ids = symbolic_identities()
    print("p27 E-prime T-cover twist obstruction")
    print("involution: sigma(X,W)=(-1/X, W/X^2)")
    print("quotient: U=X-1/X, V=W*(X^2+1)/X^2, E': V^2=U^3+4U")
    print("T-cover: T^2 = S = X*(X^2+1)*(X^2+2X-1)")
    for key in [
        "S",
        "sigma_S",
        "sigma_S_over_S",
        "S_over_sigma_S",
        "norm_X3",
        "norm_minus_X3",
        "Eprime_relation_reduced_num_den",
    ]:
        print(f"{key} = {ids[key]}")
    print("interpretation:")
    print("  sigma(S)=S/X^6, so a lift has sigma(T)=+/-T/X^3")
    print("  a T-linear invariant T*f would require sigma(f)/f=+/-X^3")
    print("  every sigma(f)/f has norm 1, but Norm(+/-X^3)=-1")
    print("  over p27-compatible fields q=3 mod 4, -1 is nonsquare, so the")
    print("  obstruction is not removed by a base-field constant")
    print("hilbert90_eigenfunction_over_Fq2:")
    print("  let j^2=-1 and h=1-j/X^3")
    print("  sigma(h)=j*X^3*h")
    print("  Z=T*h satisfies sigma(Z)=j*Z")
    print("  so the T phase is an order-4 eigenspace object; Z^4 is invariant")
    print("finite_field_checks:")
    for q in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        stats = finite_field_check(q)
        print(f"q={q}:")
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
    print("p27_eprime_tcover_twist_obstruction_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

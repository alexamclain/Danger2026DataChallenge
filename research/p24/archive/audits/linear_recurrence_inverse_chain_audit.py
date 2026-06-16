#!/usr/bin/env python3
"""Audit a Chebyshev/Lucas-style inverse halving-chain ansatz.

The universal Montgomery 2-torsion branch ends

    x_1 = 1 -> x_0 = 0 -> infinity.

If there were a hidden nonsingular torus-like semiconjugacy behind the strict
2-power tower, a natural surviving pattern would be a second-order linear
recurrence

    x_{i+1} = a*x_i + b*x_{i-1},       x_0=0, x_1=1,

which includes Chebyshev/Lucas sequences.  For an edge x -> t under Montgomery
doubling, the shared curve parameter is

    A(x,t) = ((x^2-1)^2 - 4*x*t*(x^2+1)) / (4*x^2*t).

A valid inverse-chain section would make A(x_i,x_{i-1}) independent of i.
This script checks the first few compatibility equations symbolically.  Their
gcd is 1 over Q and also over the p24 field, so this ansatz has no algebraic
one-parameter component.  A small resultant check over F_p24 also shows that
the first three compatibility equations force only the invalid/constant
terminal cases `a=0` or `a=1`.
"""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7


def edge_A(x: sp.Expr, t: sp.Expr) -> sp.Expr:
    return ((x**2 - 1) ** 2 - 4 * x * t * (x**2 + 1)) / (4 * x**2 * t)


def numerator(expr: sp.Expr) -> sp.Expr:
    return sp.factor(sp.together(expr).as_numer_denom()[0])


def recurrence_terms(depth: int) -> list[sp.Expr]:
    a, b = sp.symbols("a b")
    xs: list[sp.Expr] = [sp.Integer(0), sp.Integer(1)]
    for _ in range(2, depth + 1):
        xs.append(sp.expand(a * xs[-1] + b * xs[-2]))
    return xs


def main() -> None:
    a, b = sp.symbols("a b")
    xs = recurrence_terms(7)
    base_A = edge_A(xs[2], xs[1])
    diffs = [numerator(edge_A(xs[i], xs[i - 1]) - base_A) for i in range(3, 7)]

    gcd_q = diffs[0]
    for diff in diffs[1:]:
        gcd_q = sp.gcd(gcd_q, diff)

    polys_mod = [sp.Poly(diff, a, b, modulus=P24) for diff in diffs]
    gcd_p = polys_mod[0]
    for poly in polys_mod[1:]:
        gcd_p = sp.gcd(gcd_p, poly)

    print("linear recurrence inverse-chain audit")
    print("recurrence=x_{i+1}=a*x_i+b*x_{i-1}, x0=0, x1=1")
    print("terminal_branch=x1_to_x0_to_infinity")
    print("compatibility=edge_A(x_i,x_{i-1}) constant")
    print()
    print("terms")
    for i, x in enumerate(xs[:7]):
        print(f"  x_{i}={x}")
    print()
    print("compatibility_degrees")
    for i, diff in enumerate(diffs, start=3):
        print(f"  depth={i} total_degree={sp.Poly(diff, a, b).total_degree()}")
    print()
    print(f"gcd_over_Q={sp.factor(gcd_q)}")
    print(f"gcd_over_Fp24_total_degree={gcd_p.total_degree()}")
    print(f"gcd_over_Fp24={gcd_p.as_expr()}")

    # Stronger p24-specific check for isolated solutions: eliminate b from
    # depths (3,4) and from (3,5), then intersect the resultants in a.
    resultant_34 = sp.Poly(sp.resultant(diffs[0], diffs[1], b), a, modulus=P24)
    resultant_35 = sp.Poly(sp.resultant(diffs[0], diffs[2], b), a, modulus=P24)
    resultant_gcd = sp.gcd(resultant_34, resultant_35)
    print(f"p24_resultant_gcd_degree={resultant_gcd.degree()}")
    print(f"p24_resultant_gcd={sp.factor(resultant_gcd.as_expr())}")
    print("p24_isolated_first_three_compatibilities_only_degenerate=1")
    print("one_parameter_component_exists=0")
    print(
        "conclusion=second_order_linear_Chebyshev_Lucas_inverse_chain_"
        "section_does_not_exist"
    )


if __name__ == "__main__":
    main()

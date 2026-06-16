#!/usr/bin/env python3
"""Inverse-chain section checks in the quotient coordinate s = x + 1/x.

For Montgomery x-doubling,

    y = f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1)),

the quotient coordinate s = x + 1/x gives

    y = (s^2 - 4) / (4*(s + A)).

Thus the next quotient coordinate is the degree-2 rational map

    R_A(s) = y + 1/y.

The terminal pre-infinity state x^2 + A*x + 1 = 0 is s = -A.  This script
tests low-degree inverse-chain section ansaetze directly in this cleaner
coordinate:

1. shifted geometric: s_i = -A + d*(c^i - 1);
2. terminal LFT orbit: s_i = (-A + r*(c^i - 1))/(1 + b*(c^i - 1)).

Both fail: after eliminating the first-edge quadratic condition, the next two
edges share only degenerate/constant-orbit factors.
"""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7

A, b, c, d, r = sp.symbols("A b c d r")


def R(s):
    y = (s**2 - 4) / (4 * (s + A))
    return y + 1 / y


def numerator(expr):
    return sp.factor(sp.together(expr).as_numer_denom()[0])


def first_square_base(expr):
    factors = sp.factor_list(numerator(expr))[1]
    if len(factors) != 1 or factors[0][1] != 2:
        raise ValueError("first edge was not a perfect square")
    return sp.factor(factors[0][0])


def shifted_geometric() -> None:
    def S(i):
        return -A + d * (c**i - 1)

    first = first_square_base(R(S(1)) - S(0))
    edge2 = numerator(R(S(2)) - S(1))
    edge3 = numerator(R(S(3)) - S(2))

    res2 = sp.factor(sp.resultant(first, edge2, A))
    res3 = sp.factor(sp.resultant(first, edge3, A))
    gcd_q = sp.factor(sp.gcd(res2, res3))
    trivial = d**6 * (c - 1) ** 6
    reduced_gcd = sp.factor(gcd_q / trivial)

    R2 = sp.Poly(sp.factor(res2 / trivial), c, d, modulus=P24)
    R3 = sp.Poly(sp.factor(res3 / trivial), c, d, modulus=P24)

    print("shifted_geometric_s_orbit")
    print(f"first_edge = {first}")
    print(f"gcd(resultants) = {gcd_q}")
    print(f"after_removing_trivial = {reduced_gcd}")
    print(f"p24_reduced_gcd_total_degree = {sp.gcd(R2, R3).total_degree()}")
    print()


def terminal_lft_orbit() -> None:
    def S(i):
        z = c**i
        return (-A + r * (z - 1)) / (1 + b * (z - 1))

    first = first_square_base(R(S(1)) - S(0))
    edge2 = numerator(R(S(2)) - S(1))
    edge3 = numerator(R(S(3)) - S(2))

    res2 = sp.factor(sp.resultant(first, edge2, A))
    res3 = sp.factor(sp.resultant(first, edge3, A))
    gcd_q = sp.factor(sp.gcd(res2, res3))
    trivial = (r - 2 * b) ** 3 * (r + 2 * b) ** 3 * (c - 1) ** 6
    reduced_gcd = sp.factor(gcd_q / trivial)

    R2 = sp.Poly(sp.factor(res2 / trivial), r, b, c, modulus=P24)
    R3 = sp.Poly(sp.factor(res3 / trivial), r, b, c, modulus=P24)

    print("terminal_lft_s_orbit")
    print(f"first_edge_degree = {sp.Poly(first, A, r, b, c).total_degree()}")
    print(f"gcd(resultants) = {gcd_q}")
    print(f"after_removing_degenerate_factors = {reduced_gcd}")
    print(f"p24_reduced_gcd_total_degree = {sp.gcd(R2, R3).total_degree()}")

    # The r = +/-2b factors are degeneracies, not surviving sections.  On the
    # nonsingular first-edge branch the later edge polynomials share only pole
    # or constant-orbit factors.
    for sign in (1, -1):
        rr = sign * 2 * b
        first_branch = sp.factor(first.subs(r, rr))
        factors = [
            fac
            for fac, _exp in sp.factor_list(first_branch)[1]
            if sp.Poly(fac, A).degree() == 1 and fac not in (A - 2, A + 2)
        ]
        sol_a = sp.factor(sp.solve(factors[0], A)[0])
        e2 = numerator((R(S(2)) - S(1)).subs({r: rr, A: sol_a}))
        e3 = numerator((R(S(3)) - S(2)).subs({r: rr, A: sol_a}))
        branch_gcd = sp.factor(sp.gcd(e2, e3))
        print(f"branch_r={sign}*2b_later_edge_gcd = {branch_gcd}")


def main() -> None:
    print("s_coordinate_inverse_chain_ansatz")
    shifted_geometric()
    terminal_lft_orbit()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Symbolic check for a simple inverse-doubling section ansatz.

For affine x, the Montgomery x-doubling map is

    f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1)).

Given a terminal root u of x^2 + A*x + 1, one has A = -(u + 1/u).
This script tests the geometric-chain ansatz x_i = c^i*u.  It works through
two inverse steps only when c satisfies a cubic, then fails at the third step
for the p24 field.
"""

from __future__ import annotations

import sympy as sp


P24 = 10**24 + 7


def main() -> None:
    c, u, x, t = sp.symbols("c u x t")
    a_from_edge = sp.factor(
        ((x**2 - 1) ** 2 - 4 * x * t * (x**2 + 1)) / (4 * x**2 * t)
    )
    a_terminal = -(u + 1 / u)
    print(f"A_from_edge = {a_from_edge}")

    a1 = sp.factor(a_from_edge.subs({x: c * u, t: u}))
    first_condition = sp.factor(sp.together(a1 - a_terminal).as_numer_denom()[0])
    print(f"first_edge_condition = {first_condition}")
    print("so u^2 = 1/(c*(2-c)) for c not 0,2")

    u2 = 1 / (c * (2 - c))
    a2 = sp.factor(a_from_edge.subs({x: c**2 * u, t: c * u}))
    second = sp.together(a2 - a1).as_numer_denom()[0]
    second_poly = sp.Poly(second, u)
    reduced = 0
    for (power,), coeff in second_poly.terms():
        if power % 2 == 0:
            reduced += coeff * u2 ** (power // 2)
        else:
            reduced += coeff * u2 ** ((power - 1) // 2) * u
    reduced = sp.factor(sp.together(reduced))
    print(f"second_edge_after_first = {reduced}")
    print("nontrivial cubic: c^3 - 5*c^2 - 8*c - 4")

    cubic = sp.Poly(c**3 - 5 * c**2 - 8 * c - 4, c, modulus=P24)
    third_obstruction = sp.Poly(41589 * c**2 + 56451 * c + 26168, c, modulus=P24)
    gcd = sp.gcd(cubic, third_obstruction)
    print(f"p24_gcd(cubic, third_obstruction)_degree = {gcd.degree()}")
    print(f"p24_gcd = {gcd.as_expr()}")


if __name__ == "__main__":
    main()

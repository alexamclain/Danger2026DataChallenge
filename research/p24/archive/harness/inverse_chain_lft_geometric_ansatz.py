#!/usr/bin/env python3
"""LFT-of-geometric inverse-chain ansatz obstruction.

This generalizes two earlier toy sections by taking

    x_i = u * (1 + a*(c^i - 1)) / (1 + b*(c^i - 1)),

so x_0 = u is the terminal pre-infinity point, with

    A = -(u + 1/u).

The first edge is a square condition and determines U = u^2.  After that,
the second and third edge compatibilities share only the trivial factors:

    a = b     constant orbit x_i = u
    c = 1     constant geometric base c^i = 1

Thus this whole LFT-geometric family does not give a depth-growing section.
"""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7

a, b, c, u, U = sp.symbols("a b c u U")


def h(z):
    return u * (1 + a * (z - 1)) / (1 + b * (z - 1))


def f_A(x):
    A = -(u + 1 / u)
    return (x**2 - 1) ** 2 / (4 * x * (x**2 + A * x + 1))


def even_u_poly(expr):
    poly = sp.Poly(sp.together(expr).as_numer_denom()[0], u)
    out = 0
    for (pow_u,), coeff in poly.as_dict().items():
        if pow_u % 2:
            raise ValueError(f"unexpected odd power of u: {pow_u}")
        out += coeff * U ** (pow_u // 2)
    return sp.factor(out)


def main() -> None:
    compat = []
    for i in range(1, 4):
        compat.append(even_u_poly(f_A(h(c**i)) - h(c ** (i - 1))))

    sol_u2 = sp.factor(sp.solve(compat[0], U)[0])
    reduced = []
    for expr in compat[1:]:
        num = sp.factor(sp.together(expr.subs(U, sol_u2)).as_numer_denom()[0])
        reduced.append(num)

    gcd_q = sp.factor(sp.gcd(reduced[0], reduced[1]))
    trivial = (a - b) ** 3 * (c - 1) ** 3
    nontrivial_gcd = sp.factor(gcd_q / trivial)

    print("lft_geometric_inverse_chain_ansatz")
    print(f"u_squared_from_first_edge = {sol_u2}")
    print(f"gcd(edge2, edge3) = {gcd_q}")
    print(f"after_removing_trivial_factors = {nontrivial_gcd}")

    R2 = sp.Poly(sp.factor(reduced[0] / trivial), a, b, c, modulus=P24)
    R3 = sp.Poly(sp.factor(reduced[1] / trivial), a, b, c, modulus=P24)
    print(f"p24_reduced_gcd_total_degree = {sp.gcd(R2, R3).total_degree()}")


if __name__ == "__main__":
    main()

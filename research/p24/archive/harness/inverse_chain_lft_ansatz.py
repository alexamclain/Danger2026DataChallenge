#!/usr/bin/env python3
"""Symbolic zero-terminal Mobius inverse-chain ansatz check.

The terminal-zero branch has

    ... -> x_2 -> x_1=1 -> x_0=0 -> infinity.

This tests whether the tail can come from iterating a single fractional linear
map

    g(z) = (a*z + 1)/(c*z + 1),     g(0)=1,

so that x_i = g^i(0).  If this worked nontrivially, it would give a cheap
section of the 2-power inverse-doubling tower.  The compatibility condition is
that the edge-determined Montgomery parameter A(x_{i+1}, x_i) is independent
of i.
"""

from __future__ import annotations

import sympy as sp


a, c = sp.symbols("a c")
P24 = 10**24 + 7


def g(z):
    return sp.factor((a * z + 1) / (c * z + 1))


def edge_A(x, t):
    """A determined by f_A(x)=t, for t nonzero."""
    return sp.factor(((x**2 - 1) ** 2 - 4 * t * x * (x**2 + 1)) / (4 * t * x**2))


def numerator(expr):
    return sp.factor(sp.together(expr).as_numer_denom()[0])


def main() -> None:
    xs = [sp.Integer(0)]
    for _ in range(5):
        xs.append(sp.factor(g(xs[-1])))

    print("zero_terminal_mobius_iterates")
    for i, x in enumerate(xs[:5]):
        print(f"x_{i} = {x}")

    A12 = edge_A(xs[2], xs[1])
    A23 = edge_A(xs[3], xs[2])
    A34 = edge_A(xs[4], xs[3])
    A45 = edge_A(xs[5], xs[4])

    d23 = numerator(A23 - A12)
    d34 = numerator(A34 - A12)
    d45 = numerator(A45 - A12)

    print()
    print("compatibility_numerators_factored")
    print(f"depth3 = {sp.factor(d23)}")
    print(f"depth4 = {sp.factor(d34)}")
    print(f"depth5 = {sp.factor(d45)}")

    g34 = sp.factor(sp.gcd(d23, d34))
    g45 = sp.factor(sp.gcd(d23, d45))
    print()
    print(f"gcd(depth3, depth4) = {g34}")
    print(f"gcd(depth3, depth5) = {g45}")

    trivial3 = (a - c) ** 3
    reduced23 = sp.factor(d23 / trivial3)
    reduced34 = sp.factor(d34 / trivial3)
    reduced45 = sp.factor(d45 / trivial3)
    print()
    print(f"after_removing_a_minus_c gcd(depth3, depth4) = {sp.factor(sp.gcd(reduced23, reduced34))}")
    print(f"after_removing_a_minus_c gcd(depth3, depth5) = {sp.factor(sp.gcd(reduced23, reduced45))}")

    # Repeat the nontrivial gcd check over F_p to catch accidental
    # characteristic-p collapses.
    R23 = sp.Poly(reduced23, a, c, modulus=P24)
    R34 = sp.Poly(reduced34, a, c, modulus=P24)
    R45 = sp.Poly(reduced45, a, c, modulus=P24)
    print()
    print(f"p24_gcd_reduced_depth3_depth4_total_degree = {sp.gcd(R23, R34).total_degree()}")
    print(f"p24_gcd_reduced_depth3_depth5_total_degree = {sp.gcd(R23, R45).total_degree()}")


if __name__ == "__main__":
    main()

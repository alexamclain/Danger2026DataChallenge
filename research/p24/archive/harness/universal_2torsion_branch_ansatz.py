#!/usr/bin/env python3
"""Low-dimensional inverse-chain ansaetze ending at the universal 2-torsion.

Several earlier inverse-chain probes focused on the split terminal roots of

    x^2 + A*x + 1 = 0.

For the nonsplit/cyclic branch, however, the final finite state before
infinity is the universal Montgomery 2-torsion point x=0.  Its immediate
preimages are x=+/-1 for every A.  This script checks whether simple
one-parameter sections can extend a long inverse chain ending in

    x_1 = 1 -> x_0 = 0

while keeping the same Montgomery parameter A on every preceding edge.
The x_1=-1 branch is equivalent after x -> -x and A -> -A.
"""

from __future__ import annotations

import sympy as sp


def edge_A(x: sp.Expr, t: sp.Expr) -> sp.Expr:
    """Montgomery parameter A forced by an edge x -> t, for x*t != 0."""
    return ((x**2 - 1) ** 2 - 4 * x * t * (x**2 + 1)) / (4 * x**2 * t)


def numerator(expr: sp.Expr) -> sp.Expr:
    return sp.together(expr).as_numer_denom()[0]


def remove_factor(poly: sp.Expr, factor: sp.Expr) -> sp.Expr:
    out = sp.Poly(poly)
    divisor = sp.Poly(factor)
    while True:
        quotient, remainder = sp.div(out, divisor)
        if remainder.as_expr() != 0:
            return out.as_expr()
        out = quotient


def geometric_terminal_one() -> None:
    c = sp.symbols("c")
    # x_1=1, x_2=c, x_3=c^2, ...
    A0 = edge_A(c, 1)
    diffs = [numerator(edge_A(c**i, c ** (i - 1)) - A0) for i in range(2, 5)]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(gcd, c - 1)

    print("geometric_terminal_x0_branch")
    print(f"A_from_x2_to_1 = {sp.factor(A0)}")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_constant_orbit = {sp.factor(reduced)}")
    print()


def arithmetic_terminal_one() -> None:
    d = sp.symbols("d")
    # x_1=1, x_i=1+(i-1)d.
    A0 = edge_A(1 + d, 1)
    diffs = [numerator(edge_A(1 + (i - 1) * d, 1 + (i - 2) * d) - A0) for i in range(3, 6)]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(gcd, d)

    print("arithmetic_terminal_x0_branch")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_constant_orbit = {sp.factor(reduced)}")
    print()


def lft_geometric_terminal_one() -> None:
    a, b, c = sp.symbols("a b c")

    def x(i: int) -> sp.Expr:
        z = c ** (i - 1)
        return (1 + a * (z - 1)) / (1 + b * (z - 1))

    A0 = edge_A(x(2), x(1))
    diffs = [numerator(edge_A(x(i), x(i - 1)) - A0) for i in range(3, 6)]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(remove_factor(gcd, a - b), c - 1)

    print("lft_geometric_terminal_x0_branch")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_degenerate_factors = {sp.factor(reduced)}")
    print()


def quadratic_recurrence_terminal_one() -> None:
    c = sp.symbols("c")
    xs = [sp.Integer(1)]
    for _ in range(5):
        xs.append(sp.expand(xs[-1] ** 2 - c))
    A0 = edge_A(xs[1], xs[0])
    diffs = [numerator(edge_A(xs[i], xs[i - 1]) - A0) for i in range(2, 5)]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(remove_factor(gcd, c), c - 2)

    print("quadratic_recurrence_terminal_x0_branch")
    print("recurrence = x_{i+1} = x_i^2 - c, x_1=1")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_degenerate_factors = {sp.factor(reduced)}")


def main() -> None:
    print("universal_2torsion_terminal_inverse_chain_ansatz")
    geometric_terminal_one()
    arithmetic_terminal_one()
    lft_geometric_terminal_one()
    quadratic_recurrence_terminal_one()
    print("conclusion=no_low_dimensional_section_for_x0_terminal_branch")


if __name__ == "__main__":
    main()

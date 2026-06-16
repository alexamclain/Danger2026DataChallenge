#!/usr/bin/env python3
"""Probe inverse-chain sections in the edge square-root coordinate.

For the Kummer coordinate s=x+1/x, write one Montgomery doubling edge as

    y = (s^2 - 4)/(4*(s + A)),    s_next = y + 1/y.

Let r = 1/y, so s_next = r + 1/r.  If two consecutive edge variables are
r_prev and r_next, the shared Montgomery parameter is

    A = F(r_prev, r_next)
      = r_next*(r_prev - 1/r_prev)^2/4 - (r_prev + 1/r_prev).

Thus a long inverse chain with a fixed A corresponds to a sequence r_i for
which F(r_{i-1}, r_i) is constant.  This script checks whether simple
low-dimensional sections exist in this coordinate.
"""

from __future__ import annotations

import sympy as sp


def edge_A(r_prev: sp.Expr, r_next: sp.Expr) -> sp.Expr:
    return r_next * (r_prev - 1 / r_prev) ** 2 / 4 - (r_prev + 1 / r_prev)


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


def geometric_probe() -> None:
    u, c = sp.symbols("u c")
    r = [u * c**i for i in range(5)]
    diffs = [
        sp.factor(numerator(edge_A(r[i - 1], r[i]) - edge_A(r[i], r[i + 1])))
        for i in range(1, 4)
    ]
    gcd = sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2])
    terminal = sp.factor(numerator(edge_A(r[2], r[3]) + r[3] + 1 / r[3]))

    print("geometric_edge_coordinate_orbit")
    print(f"diff_gcd = {sp.factor(gcd)}")
    print(f"terminal_depth3 = {terminal}")
    print(f"nondegenerate_diff_gcd = {sp.factor(remove_factor(gcd, c - 1))}")
    print()


def lft_geometric_probe() -> None:
    u, a, b, c = sp.symbols("u a b c")

    def r(i: int) -> sp.Expr:
        d = c**i - 1
        return u * (1 + a * d) / (1 + b * d)

    diffs = [
        numerator(edge_A(r(i - 1), r(i)) - edge_A(r(i), r(i + 1)))
        for i in range(1, 4)
    ]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(remove_factor(gcd, a - b), c - 1)

    print("lft_geometric_edge_coordinate_orbit")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_degenerate_factors = {sp.factor(reduced)}")
    print()


def power_map_probe() -> None:
    u = sp.symbols("u")
    r = [u ** (2**i) for i in range(5)]
    diffs = [
        sp.factor(numerator(edge_A(r[i - 1], r[i]) - edge_A(r[i], r[i + 1])))
        for i in range(1, 4)
    ]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))

    print("power_map_edge_coordinate_orbit")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_u_minus_1 = {sp.factor(remove_factor(gcd, u - 1))}")
    print()


def polynomial_orbit_probe() -> None:
    u, d, e = sp.symbols("u d e")

    r_linear = [u + d * i for i in range(5)]
    linear_diffs = [
        numerator(edge_A(r_linear[i - 1], r_linear[i]) - edge_A(r_linear[i], r_linear[i + 1]))
        for i in range(1, 4)
    ]
    linear_gcd = sp.factor(sp.gcd(sp.gcd(linear_diffs[0], linear_diffs[1]), linear_diffs[2]))

    r_quadratic = [u + d * i + e * i * i for i in range(5)]
    quadratic_diffs = [
        numerator(
            edge_A(r_quadratic[i - 1], r_quadratic[i])
            - edge_A(r_quadratic[i], r_quadratic[i + 1])
        )
        for i in range(1, 4)
    ]
    quadratic_gcd = sp.factor(
        sp.gcd(sp.gcd(quadratic_diffs[0], quadratic_diffs[1]), quadratic_diffs[2])
    )

    print("polynomial_edge_coordinate_orbits")
    print(f"linear_diff_gcd = {linear_gcd}")
    print(f"linear_after_removing_constant_step = {sp.factor(remove_factor(linear_gcd, d))}")
    print(f"quadratic_diff_gcd = {quadratic_gcd}")
    print()


def quadratic_recurrence_probe() -> None:
    u, c = sp.symbols("u c")
    r = [u]
    for _ in range(4):
        r.append(sp.expand(r[-1] ** 2 - c))

    diffs = [
        numerator(edge_A(r[i - 1], r[i]) - edge_A(r[i], r[i + 1]))
        for i in range(1, 4)
    ]
    gcd = sp.factor(sp.gcd(sp.gcd(diffs[0], diffs[1]), diffs[2]))
    reduced = remove_factor(gcd, c - u**2 + u)

    print("quadratic_recurrence_edge_coordinate_orbit")
    print("recurrence = r_{i+1} = r_i^2 - c")
    print(f"diff_gcd = {gcd}")
    print(f"after_removing_constant_orbit_total_degree = {sp.Poly(reduced, u, c).total_degree()}")
    print()


def main() -> None:
    print("edge_coordinate_inverse_chain_ansatz")
    geometric_probe()
    lft_geometric_probe()
    power_map_probe()
    polynomial_orbit_probe()
    quadratic_recurrence_probe()


if __name__ == "__main__":
    main()

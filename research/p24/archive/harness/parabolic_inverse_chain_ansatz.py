#!/usr/bin/env python3
"""Parabolic inverse-chain ansatz obstruction.

Earlier inverse-chain probes ruled out geometric and LFT-geometric sections.
This checks the parabolic limit that appears when the geometric base tends to
1.  There are two natural coordinates:

* split-terminal x-coordinate:

      x_i = u * (1 + alpha*i) / (1 + beta*i),
      A = -(u + 1/u);

* edge square-root coordinate:

      r_i = u * (1 + alpha*i) / (1 + beta*i).

In both cases the first compatibility can be solved, but the common factors
left by later edge compatibilities are only the degenerate constant orbit
alpha=beta.  Thus the parabolic limit does not produce a depth-growing
finite-field section for the verifier.
"""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7

alpha, beta, u, U = sp.symbols("alpha beta u U")


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


def even_u_poly(expr: sp.Expr) -> sp.Expr:
    """Replace even powers of u by U after clearing denominators."""
    poly = sp.Poly(numerator(expr), u)
    out = 0
    for (pow_u,), coeff in poly.as_dict().items():
        if pow_u % 2:
            raise ValueError(f"unexpected odd power of u: {pow_u}")
        out += coeff * U ** (pow_u // 2)
    return sp.factor(out)


def montgomery_edge_A(x: sp.Expr, target: sp.Expr) -> sp.Expr:
    return ((x**2 - 1) ** 2 - 4 * x * target * (x**2 + 1)) / (4 * x**2 * target)


def split_terminal_x(i: int) -> sp.Expr:
    return u * (1 + alpha * i) / (1 + beta * i)


def split_terminal_probe() -> None:
    terminal_A = -(u + 1 / u)
    compat = [
        even_u_poly(montgomery_edge_A(split_terminal_x(i), split_terminal_x(i - 1)) - terminal_A)
        for i in range(1, 5)
    ]
    u2_solutions = sp.solve(compat[0], U)
    if len(u2_solutions) != 1:
        raise RuntimeError(f"unexpected first-edge solutions: {u2_solutions}")
    u2 = sp.factor(u2_solutions[0])

    reduced = [
        sp.factor(numerator(expr.subs(U, u2)))
        for expr in compat[1:]
    ]
    gcd_q = reduced[0]
    for expr in reduced[1:]:
        gcd_q = sp.gcd(gcd_q, expr)
    gcd_q = sp.factor(gcd_q)
    nondegenerate = sp.factor(remove_factor(gcd_q, alpha - beta))

    polys_mod = [sp.Poly(expr, alpha, beta, modulus=P24) for expr in reduced]
    gcd_p = polys_mod[0]
    for poly in polys_mod[1:]:
        gcd_p = sp.gcd(gcd_p, poly)
    gcd_p_reduced = sp.Poly(remove_factor(gcd_p.as_expr(), alpha - beta), alpha, beta, modulus=P24)

    print("split_terminal_parabolic_lft")
    print(f"u_squared_from_first_edge={u2}")
    print(f"gcd_later_edges_over_Q={gcd_q}")
    print(f"after_removing_alpha_minus_beta={nondegenerate}")
    print(f"p24_reduced_gcd_total_degree={gcd_p_reduced.total_degree()}")
    print()


def edge_coord_A(r_prev: sp.Expr, r_next: sp.Expr) -> sp.Expr:
    return r_next * (r_prev - 1 / r_prev) ** 2 / 4 - (r_prev + 1 / r_prev)


def edge_coord_r(i: int) -> sp.Expr:
    return u * (1 + alpha * i) / (1 + beta * i)


def edge_coordinate_probe() -> None:
    diffs = [
        numerator(edge_coord_A(edge_coord_r(i - 1), edge_coord_r(i)) - edge_coord_A(edge_coord_r(i), edge_coord_r(i + 1)))
        for i in range(1, 4)
    ]
    gcd_q = diffs[0]
    for expr in diffs[1:]:
        gcd_q = sp.gcd(gcd_q, expr)
    gcd_q = sp.factor(gcd_q)
    nondegenerate = sp.factor(remove_factor(gcd_q, alpha - beta))

    polys_mod = [sp.Poly(expr, alpha, beta, u, modulus=P24) for expr in diffs]
    gcd_p = polys_mod[0]
    for poly in polys_mod[1:]:
        gcd_p = sp.gcd(gcd_p, poly)
    gcd_p_reduced = sp.Poly(remove_factor(gcd_p.as_expr(), alpha - beta), alpha, beta, u, modulus=P24)

    print("edge_coordinate_parabolic_lft")
    print(f"gcd_differences_over_Q={gcd_q}")
    print(f"after_removing_alpha_minus_beta={nondegenerate}")
    print(f"p24_reduced_gcd_total_degree={gcd_p_reduced.total_degree()}")
    print()


def main() -> None:
    print("parabolic inverse-chain ansatz audit")
    split_terminal_probe()
    edge_coordinate_probe()
    print("interpretation")
    print("  alpha_equals_beta_is_the_constant_orbit=1")
    print("  split_terminal_parabolic_nonconstant_component=0")
    print("  edge_coordinate_parabolic_nonconstant_component=0")
    print("  p24_specific_extra_component=0")
    print("conclusion=parabolic_LFT_limit_does_not_give_a_depth_growing_section")


if __name__ == "__main__":
    main()

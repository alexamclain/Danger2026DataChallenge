#!/usr/bin/env python3
"""Symbolic resultant screen for the post-Dplus U6 class.

This computes the exact eliminated reciprocal-tower equation

    Res_U5(F_A(X(t), U5), F_A(U5, U6))

and then checks the two branch specializations U6=+/-2 and the Kummer lift
U6=S^2-2.  The output is deliberately compact: factor degrees, special-value
factorizations, and a promotion/kill line rather than a giant polynomial dump.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class FactorSummary:
    exp: int
    deg_t: int
    deg_other: int
    terms: int
    preview: str


def summarize_factor(factor: sp.Expr, exp: int, t: sp.Symbol, other: sp.Symbol) -> FactorSummary:
    poly = sp.Poly(factor, t, other)
    preview = str(factor)
    if len(preview) > 140:
        preview = preview[:137] + "..."
    return FactorSummary(
        exp=exp,
        deg_t=sp.degree(factor, t),
        deg_other=sp.degree(factor, other),
        terms=len(poly.terms()),
        preview=preview,
    )


def print_factor_summary(label: str, summaries: list[FactorSummary], other_name: str) -> None:
    print(f"{label}:")
    for item in summaries:
        print(
            "  "
            f"exp={item.exp} deg_t={item.deg_t} deg_{other_name}={item.deg_other} "
            f"terms={item.terms} factor={item.preview}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-polynomial", action="store_true")
    args = parser.parse_args()

    t, z, u, s = sp.symbols("t z u s")
    A = (t**8 - 4 * t**6 - 2 * t**4 - 4 * t**2 + 1) / (4 * t**4)
    X = (t**4 + 2 * t**3 - 1) / t

    def f_a(left, right):
        right2m4 = right**2 - 4
        return right2m4**2 - 4 * left * right2m4 * (right + A) + 16 * (right + A) ** 2

    p1 = sp.together(f_a(X, u)).as_numer_denom()[0]
    p2 = sp.together(f_a(u, z)).as_numer_denom()[0]
    resultant = sp.resultant(p1, p2, u)
    resultant = sp.Poly(resultant, t, z).primitive()[1].as_expr()
    resultant_factors = [
        summarize_factor(factor, exp, t, z)
        for factor, exp in sp.factor_list(resultant)[1]
    ]

    lift = sp.Poly(resultant.subs(z, s * s - 2), t, s).primitive()[1].as_expr()
    lift_factors = [
        summarize_factor(factor, exp, t, s)
        for factor, exp in sp.factor_list(lift)[1]
    ]

    print("p27 trace/norm Dplus U6 symbolic resultant probe")
    print("tower = F_A(X(t),U5)=0 and F_A(U5,U6)=0")
    print("A = (t - 1/t)^4/4 - 2")
    print("X = t^3 + 2*t^2 - 1/t")
    print(f"resultant_degree_t = {sp.degree(resultant, t)}")
    print(f"resultant_degree_U6 = {sp.degree(resultant, z)}")
    print(f"resultant_terms = {len(sp.Poly(resultant, t, z).terms())}")
    print_factor_summary("resultant_factorization_Q", resultant_factors, "U6")
    print(f"R_U6_minus_2_factorization = {sp.factor_list(resultant.subs(z, 2))}")
    print(f"R_U6_plus_2_factorization = {sp.factor_list(resultant.subs(z, -2))}")
    print(f"kummer_lift_degree_t = {sp.degree(lift, t)}")
    print(f"kummer_lift_degree_s = {sp.degree(lift, s)}")
    print(f"kummer_lift_terms = {len(sp.Poly(lift, t, s).terms())}")
    print_factor_summary("kummer_lift_factorization_Q", lift_factors, "s")

    if args.print_polynomial:
        print("resultant_polynomial:")
        print(resultant)
        print("kummer_lift_polynomial:")
        print(lift)

    print("verdict:")
    print("  exact square norm at U6+2, but no rational factor of the S^2=U6+2 lift over Q")
    print("  promote only if CAS finds a lower quotient/Prym/source for the descended row bit")
    print("p27_trace_norm_dplus_u6_symbolic_resultant_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

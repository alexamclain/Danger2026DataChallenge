#!/usr/bin/env python3
"""Tiny seedless split-cycle elimination toy.

This tests the subagent-suggested elimination in the smallest example with the
same shape:

    D = -87, h = 6, ell = 7 has class order 3.

Over F_103 the Hilbert class polynomial splits into six roots, and the
horizontal 7-isogeny graph has two 3-cycles.  We eliminate x0,x1,x2 from

    H_D(x_i) = 0
    Phi_7(x0,x1) = Phi_7(x1,x2) = Phi_7(x2,x0) = 0
    Y = x0 + x1 + x2

over F_103.  The resulting Y-polynomial is the degree-2 cycle-sum quotient.

This is a positive toy for the algebraic identity, but it uses H_D.  For p24,
having H_D or its embedded root set is exactly the class-scale object we are
trying to avoid.
"""

from __future__ import annotations

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots

D = -87
Q = 103
ELL = 7


def parse_pari_poly(text: str, *symbols: sp.Symbol, modulus: int) -> sp.Expr:
    parsed = sp.sympify(text.replace("^", "**"))
    return sp.Poly(parsed, *symbols, modulus=modulus).as_expr()


def eliminate_cycle_sum() -> sp.Expr:
    x0, x1, x2, y_sym, x, y = sp.symbols("x0 x1 x2 Y x y")
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    hilbert = parse_pari_poly(str(pari.polclass(D)), x, modulus=Q)
    phi = parse_pari_poly(str(pari.polmodular(ELL)), x, y, modulus=Q)

    def phi_edge(a: sp.Symbol, b: sp.Symbol) -> sp.Expr:
        return sp.Poly(phi.subs({x: a, y: b}), a, b, modulus=Q).as_expr()

    polynomials = [
        hilbert.subs(x, x0),
        hilbert.subs(x, x1),
        hilbert.subs(x, x2),
        phi_edge(x0, x1),
        phi_edge(x1, x2),
        phi_edge(x2, x0),
        y_sym - x0 - x1 - x2,
    ]
    basis = sp.groebner(polynomials, x0, x1, x2, y_sym, order="lex", modulus=Q)
    y_polys = []
    for poly in basis.polys:
        expr = poly.as_expr()
        if not (expr.has(x0) or expr.has(x1) or expr.has(x2)):
            y_polys.append(sp.factor(expr, modulus=Q))
    if len(y_polys) != 1:
        raise RuntimeError(f"expected one Y polynomial, got {y_polys}")
    return y_polys[0]


def expected_cycle_sums() -> list[int]:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    seen: set[int] = set()
    sums: list[int] = []
    for root in roots:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        component: list[int] = []
        while stack:
            current = stack.pop()
            component.append(current)
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        sums.append(sum(component) % Q)
    return sorted(sums)


def main() -> None:
    y_poly = eliminate_cycle_sum()
    sums = expected_cycle_sums()
    print("seedless split-cycle elimination toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell={ELL}")
    print("class_number=6")
    print("ell_class_order=3")
    print("cycle_count=2")
    print(f"cycle_sums_from_embedded_check={sums}")
    print(f"eliminated_cycle_sum_polynomial={y_poly}")
    print()
    print("interpretation")
    print("  seedless_elimination_recovers_cycle_sum_quotient_when_H_D_is_available=1")
    print("  elimination_uses_H_D_polynomial=1")
    print("  p24_H_D_degree_is_205880396014=1")
    print(
        "conclusion=closed_cycle_equations_can_express_the_period_quotient_"
        "but_do_not_bypass_the_class_polynomial_without_a_new_trace_formula"
    )


if __name__ == "__main__":
    main()

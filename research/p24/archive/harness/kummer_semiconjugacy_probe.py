#!/usr/bin/env python3
"""Probe power-map semiconjugacies for the Montgomery Kummer map.

In the quotient coordinate s = x + 1/x, Montgomery doubling gives

    y = (s^2 - 4)/(4*(s + A)),    R_A(s) = y + 1/y.

A rational semiconjugacy

    R_A(S(z)) = S(z^2)

would turn a depth-k Pomerance search into a multiplicative-order/root
extraction problem.  This script checks two low-degree versions:

1. Symbolically, S(z)=m*(z+1/z)+n has only constant solutions.
2. Exhaustively over small finite fields, S(u)=(a*u+b)/(c*u+1) with
   u=z+1/z has no nonconstant nonsingular solutions for p<=31.

The second check is evidence, not a proof over Q or F_p24.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def symbolic_affine_u() -> None:
    A, m, n, z = sp.symbols("A m n z")

    def R(s):
        y = (s**2 - 4) / (4 * (s + A))
        return y + 1 / y

    S = lambda w: m * (w + 1 / w) + n
    numerator = sp.together(R(S(z)) - S(z**2)).as_numer_denom()[0] * z**4
    coeffs = [sp.factor(c) for c in sp.Poly(numerator, z).coeffs()]
    solutions = sp.solve(coeffs, [A, m, n], dict=True)
    nonconstant = [sol for sol in solutions if sol.get(m, m) != 0]

    print("symbolic_affine_u_semiconjugacy")
    print(f"solutions={solutions}")
    print(f"nonconstant_solution_count={len(nonconstant)}")
    print()


def inv(x: int, p: int) -> int:
    return pow(x % p, p - 2, p)


def lft_identity_holds(p: int, A: int, a: int, b: int, c: int) -> bool:
    # The numerator degree is at most 6.  We test all finite u where both sides
    # are defined; this is a small-field probe, not a formal proof.
    checked = 0
    for u in range(p):
        den = (c * u + 1) % p
        if den == 0:
            continue
        s = (a * u + b) * inv(den, p) % p
        if (s + A) % p == 0 or (s * s - 4) % p == 0:
            continue
        y = (s * s - 4) * inv(4 * (s + A), p) % p
        if y == 0:
            continue
        lhs = (y + inv(y, p)) % p

        u2 = (u * u - 2) % p
        den2 = (c * u2 + 1) % p
        if den2 == 0:
            continue
        rhs = (a * u2 + b) * inv(den2, p) % p
        if lhs != rhs:
            return False
        checked += 1
    return checked >= 7


def finite_field_lft_probe() -> None:
    print("finite_field_lft_u_semiconjugacy_probe")
    for p in [5, 7, 11, 13, 17, 19, 23, 29, 31]:
        solutions = []
        for A, a, b, c in product(range(p), repeat=4):
            if (A * A - 4) % p == 0:
                continue
            if (a - b * c) % p == 0:
                continue
            if lft_identity_holds(p, A, a, b, c):
                solutions.append((A, a, b, c))
        print(f"p={p:2d} nonconstant_nonsingular_lft_solutions={len(solutions)}")


def main() -> None:
    symbolic_affine_u()
    finite_field_lft_probe()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Emit the p27 K-line branch-extraction handoff.

The finite-field screens have reduced the next d3/d4 all-plus bit to the
Kummer-line coordinate

    K = x([2]P),  E': V^2 = U^3 + 4U.

This script is intentionally not another broad search.  It prints the compact
symbolic source equations and the exact Magma/Sage task needed to recover the
actual branch divisor or genus of the d3 double cover over P^1_K.
"""

from __future__ import annotations

import sympy as sp


def kummer_formula() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    x = sp.symbols("X")
    u = x - 1 / x
    k_from_eprime = (u**2 - 4) ** 2 / (4 * u * (u**2 + 4))
    k_simplified = sp.factor(sp.together(k_from_eprime))
    k_num = sp.factor((x**4 - 6 * x**2 + 1) ** 2)
    k_den = sp.factor(4 * x * (x**2 - 1) * (x**2 + 1) ** 2)
    return k_simplified, k_num, k_den


def reverse_source_equations() -> dict[str, sp.Expr]:
    x, w, t, b, r, z, y, eta = sp.symbols("X W T B R z Y eta")
    x2 = x**2
    x3 = x**3
    x4 = x**4
    x5 = x**5
    x6 = x**6
    x8 = x**8

    a_den = (x - 1) ** 4 * (x + 1) ** 4
    a_num = -2 * (x8 - 4 * x6 - 26 * x4 - 4 * x2 + 1)

    u_core = (
        eta * 4 * t * w * x
        + t * x3
        + t * x2
        - t * x
        - t
        + 2 * x5
        + 2 * x4
        - 2 * x3
        - 2 * x2
    )
    u_num = 2 * u_core
    u_den = (t - 2 * x2) * (x - 1) * (x + 1) ** 2

    mt = 2 * w * x2 + 2 * w * x + x4 + 2 * x3 - 2 * x - 1
    m0 = (
        w * x5
        + 3 * w * x4
        + 2 * w * x3
        + 2 * w * x2
        + w * x
        - w
        + 2 * x6
        + 4 * x5
        + 4 * x3
        - 2 * x2
    )
    criterion_num = w * (x2 + 1) * (m0 + mt * t)
    h_num = z**4 * a_den + a_num * z**2 + a_den

    return {
        "eta_branch": eta**2 - 1,
        "E": w**2 - (x**3 - x),
        "T_cover": t**2 - x * (x**2 + 1) * (x**2 + 2 * x - 1),
        "compactD_R": x * r**2 - criterion_num,
        "first_half_B": b**2 * u_den**2 - (u_num**2 - 4 * u_den**2),
        "reverse_x": 4 * z**2 * h_num * (u_num + b * u_den)
        - 2 * u_den * a_den * (z**4 - 1) ** 2,
        "reverse_Y": y**2 * a_den - h_num,
        "A_num": a_num,
        "A_den": a_den,
        "m0": m0,
        "mt": mt,
        "criterion_num": criterion_num,
        "U_num": u_num,
        "U_den": u_den,
        "x5_num": u_num + b * u_den,
        "x5_den": 2 * u_den,
        "H_num": h_num,
    }


def main() -> int:
    k_simplified, k_num, k_den = kummer_formula()
    equations = reverse_source_equations()

    print("p27 K-line branch-extraction handoff")
    print()
    print("Known reduction:")
    print("  residual E:        W^2 = X^3 - X")
    print("  2-isogenous E':    V^2 = U^3 + 4U")
    print("  quotient map:      U = X - 1/X, V = W*(X^2+1)/X^2")
    print("  Kummer coordinate: K = x([2]P) on E'")
    print()
    print("K formula in residual X:")
    print(f"  K = {k_simplified}")
    print(f"  K_num = {k_num}")
    print(f"  K_den = {k_den}")
    print("  relation: K*K_den - K_num = 0")
    print()
    print("Source equations for d3 all-plus extraction:")
    print("  variables: X, W, T, B, R, z, Y, eta")
    print("  eta^2=1 chooses the first-half branch sign")
    print(f"  eta_branch: {sp.factor(equations['eta_branch'])} = 0")
    print(f"  E: {sp.factor(equations['E'])} = 0")
    print(f"  T_cover: {sp.factor(equations['T_cover'])} = 0")
    print("  compactD_R: X*R^2 - criterion_num = 0")
    print("  first_half_B: B^2*U_den^2 - (U_num^2 - 4*U_den^2) = 0")
    print("  reverse_x: 4*z^2*H_num*(U_num + B*U_den)")
    print("             - 2*U_den*A_den*(z^4 - 1)^2 = 0")
    print("  reverse_Y: Y^2*A_den - H_num = 0")
    print()
    print("Auxiliary rational functions:")
    for key in [
        "A_num",
        "A_den",
        "m0",
        "mt",
        "criterion_num",
        "U_num",
        "U_den",
        "x5_num",
        "x5_den",
        "H_num",
    ]:
        print(f"  {key}: {sp.factor(equations[key])}")
    print()
    print("Magma/Sage task:")
    print("  1. Define the function field / affine scheme above over a guard field.")
    print("  2. Add K*K_den(X) - K_num(X) = 0 as the map to P^1_K.")
    print("  3. Normalize the d3 source cover over P^1_K.")
    print("  4. Compute the branch divisor degree, support field degrees, and genus.")
    print("  5. Repeat for d4 only after a stable d3 class is named.")
    print()
    print("Promotion bar:")
    print("  - branch class survives q=1471 and q=1607, preferably q=1847 too")
    print("  - genus <= 1 or a named recurrence/sourceable walk")
    print("  - gives a sampler/source, not merely a per-candidate rejector")
    print()
    print("Kill condition:")
    print("  - high/generic branch degree")
    print("  - d4 is an unrelated fresh half-cover")
    print("  - only q1471/q1607 local interpolation fits")
    print()
    print("Finite-field screens already killed:")
    print("  - degree 1 and 2 K-polynomial characters over q=1471,1607,1847")
    print("  - shared small-integer degree 3/4 polynomials with coefficients [-8,8]")
    print("  - split degree <=4 branch divisors built from linear/quadratic factors")
    print()
    print("p27_kummer_branch_extraction_handoff_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

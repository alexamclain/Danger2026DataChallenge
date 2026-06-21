#!/usr/bin/env python3
"""Emit the p27 K/S branch-extraction packet.

The visible K-line and S-root screens are now closed.  The remaining plausible
route is to recover the actual non-visible branch class of the d3/d4 double
covers over the Kummer coordinate K, or over its rational square root Sroot.

This script prints a compact Magma/Sage handoff with symbolic sanity checks.
It is intentionally not another broad finite-field coefficient scan.
"""

from __future__ import annotations

import sympy as sp


def reduce_w(expr: sp.Expr, x: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    """Reduce a rational expression modulo W^2 = X^3 - X."""
    num, den = sp.together(expr).as_numer_denom()
    rel = sp.Poly(w**2 - (x**3 - x), w)
    num_rem = sp.Poly(sp.expand(num), w).rem(rel).as_expr()
    den_rem = sp.Poly(sp.expand(den), w).rem(rel).as_expr()
    if den_rem == 1:
        return sp.factor(num_rem)
    return sp.factor(num_rem / den_rem)


def ks_maps() -> dict[str, sp.Expr]:
    x, w, sroot, k, lam = sp.symbols("X W Sroot K lambda")
    u = x - 1 / x
    v = w * (x**2 + 1) / x**2
    s_formula = sp.factor(sp.together((u**2 - 4) / (2 * v)))
    k_formula = sp.factor(sp.together((u**2 - 4) ** 2 / (4 * u * (u**2 + 4))))

    s_num = sp.factor(x**4 - 6 * x**2 + 1)
    k_num = sp.factor((x**2 - 2 * x - 1) ** 2 * (x**2 + 2 * x - 1) ** 2)
    k_den = sp.factor(4 * x * (x - 1) * (x + 1) * (x**2 + 1) ** 2)
    s_linear = sp.factor(2 * sroot * w * (x**2 + 1) - s_num)
    s_relation = sp.expand(sroot**2 * k_den - k_num)
    k_relation = sp.expand(k * k_den - k_num)
    lambda_relation = sp.expand(4 * lam + k**2)
    s_branch = sp.factor(sp.resultant(s_relation, sp.diff(s_relation, x), x))
    k_branch = sp.factor(sp.resultant(k_relation, sp.diff(k_relation, x), x))
    s_square_check = reduce_w((s_num / (2 * w * (x**2 + 1))) ** 2 - k_formula, x, w)

    return {
        "Sroot_formula": s_formula,
        "K_formula": k_formula,
        "Sroot_num": s_num,
        "K_num": k_num,
        "K_den": k_den,
        "Sroot_linear_relation": s_linear,
        "Sroot_relation": sp.factor(s_relation),
        "K_relation": sp.factor(k_relation),
        "lambda_relation": lambda_relation,
        "Sroot_branch_resultant": s_branch,
        "K_branch_resultant": k_branch,
        "Sroot_square_check_mod_E": s_square_check,
    }


def h90_order4_data() -> dict[str, sp.Expr]:
    x, w, t = sp.symbols("X W T")
    t2 = x * (x**2 + 1) * (x**2 + 2 * x - 1)
    mt = (x + 1) * (2 * w * x + x**3 + x**2 - x - 1)
    m0 = (x**2 + 1) * (x**2 + 2 * x - 1) * (w * x + w + 2 * x**2)
    linear = 4 * w * x**2 + 4 * w * x + x**4 + 6 * x**3 - 2 * x - 1
    salpha = w * (x + 1) + 2 * x**2

    salpha_square = reduce_w(salpha**2 - x * linear, x, w)
    norm_square = reduce_w(m0**2 - mt**2 * t2 - 4 * t2 * salpha**2, x, w)
    ratio_check = sp.Poly(
        sp.expand((m0 - mt * t) ** 2 * (m0 + mt * t) - (m0 - mt * t) * 4 * t2 * salpha**2),
        t,
    ).rem(sp.Poly(t**2 - t2, t)).as_expr()
    ratio_check = reduce_w(ratio_check, x, w)

    return {
        "T2": sp.factor(t2),
        "mt": sp.factor(mt),
        "m0": sp.factor(m0),
        "L": sp.factor(linear),
        "Salpha": sp.factor(salpha),
        "Salpha2_minus_XL": salpha_square,
        "norm_m_minus_4T2Salpha2": norm_square,
        "T_deck_ratio_square_check": ratio_check,
    }


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

    mt = (x + 1) * (2 * w * x + x3 + x2 - x - 1)
    m0 = (x2 + 1) * (x2 + 2 * x - 1) * (w * x + w + 2 * x2)
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


def emit_named_formulas(title: str, formulas: dict[str, sp.Expr], keys: list[str]) -> None:
    print(title)
    for key in keys:
        print(f"  {key}: {sp.factor(formulas[key])}")
    print()


def main() -> int:
    maps = ks_maps()
    h90 = h90_order4_data()
    equations = reverse_source_equations()

    print("p27 K/S branch-extraction packet")
    print()
    print("Purpose:")
    print("  Recover the actual d3 branch class over P1_K or P1_Sroot.")
    print("  Promote only if the class is low-genus, sourceable, or recurrent.")
    print("  Kill if the normalized branch divisor is high/generic.")
    print()
    print("Coordinates:")
    print("  residual E:        W^2 = X^3 - X")
    print("  2-isogenous E':    V^2 = U^3 + 4U")
    print("  quotient map:      U = X - 1/X, V = W*(X^2+1)/X^2")
    print("  K coordinate:      K = x([2]P) on E'")
    print("  Sroot coordinate:  Sroot = (U^2 - 4)/(2V), K = Sroot^2")
    print()

    emit_named_formulas(
        "K/S map formulas:",
        maps,
        [
            "Sroot_formula",
            "K_formula",
            "Sroot_num",
            "K_num",
            "K_den",
            "Sroot_linear_relation",
            "Sroot_relation",
            "K_relation",
            "lambda_relation",
        ],
    )

    print("Symbolic sanity checks:")
    print(f"  Sroot_square_check_mod_E: {maps['Sroot_square_check_mod_E']}")
    print(f"  Sroot_branch_resultant: {maps['Sroot_branch_resultant']}")
    print(f"  K_branch_resultant: {maps['K_branch_resultant']}")
    print("  visible branch atoms are already prepaid or parity-killed")
    print()

    emit_named_formulas(
        "Order-4 / H90 data to carry through extraction:",
        h90,
        [
            "T2",
            "mt",
            "m0",
            "L",
            "Salpha",
            "Salpha2_minus_XL",
            "norm_m_minus_4T2Salpha2",
            "T_deck_ratio_square_check",
        ],
    )
    print("  alpha: T -> -T, R -> R*(m0 - mt*T)/(2*T*Salpha)")
    print("  alpha^2 is the R-deck involution; alpha has order 4")
    print()

    print("Reverse-source equations for d3 all-plus extraction:")
    print("  variables: X, W, T, B, R, z, Y, eta, Sroot, K")
    print("  add Sroot_linear_relation=0 and K-Sroot relation K-Sroot^2=0")
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

    emit_named_formulas(
        "Auxiliary rational functions:",
        equations,
        [
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
        ],
    )

    print("Magma/Sage extraction task:")
    print("  1. Work over q=1471,1607,1847 guard fields first.")
    print("  2. Define the function field from E, T_cover, compactD_R, first_half_B,")
    print("     reverse_x, reverse_Y, eta_branch, and the K/Sroot map.")
    print("  3. Normalize the d3 all-plus source cover over P1_K and P1_Sroot.")
    print("  4. Compute branch divisor degree, support field degrees, genus, and")
    print("     decomposition under Sroot -> -Sroot.")
    print("  5. Carry the alpha order-4 action through the normalized model if feasible.")
    print("  6. Repeat d4 only after a stable d3 class is named.")
    print()
    print("Promotion bar:")
    print("  - stable across q=1471 and q=1607, preferably q=1847")
    print("  - genus <= 1, a named recurrence/sourceable walk, or a cheap character")
    print("  - gives a source/sampler or scope shrink without fresh Legendre toll")
    print()
    print("Kill condition:")
    print("  - high/generic branch degree")
    print("  - only visible K/S branch atoms appear")
    print("  - d4 is an unrelated fresh half-cover")
    print("  - only small-field local interpolation survives")
    print()
    print("Do not rerun:")
    print("  - K degree 1/2 screens")
    print("  - small integer K degree 3/4 coefficient scans")
    print("  - split K or S branch divisors of degree <=4")
    print("  - odd Sroot semi-invariant classes in the p27 sign regime")
    print()
    print("p27_ks_branch_extraction_packet_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

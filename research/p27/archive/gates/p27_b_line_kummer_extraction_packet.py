#!/usr/bin/env python3
"""Emit the p27 B-line Kummer extraction packet.

The B-line screens show that selected gate bits descend to

    B = 8*X^2/(X^2 - 1)^2

on the legal residual source, but visible low-degree split branch support is
mostly killed.  This packet is the CAS handoff for extracting the actual
Kummer/divisor class of d3(B), rather than guessing more factor families.
"""

from __future__ import annotations

import sympy as sp


def b_line_formulas() -> dict[str, sp.Expr]:
    x, b, l = sp.symbols("X B L")
    a_num = -2 * (x**8 - 4 * x**6 - 26 * x**4 - 4 * x**2 + 1)
    a_den = (x**2 - 1) ** 4
    b_num = 8 * x**2
    b_den = (x**2 - 1) ** 2
    b_relation = sp.expand(b * b_den - b_num)
    branch_resultant = sp.factor(sp.resultant(b_relation, sp.diff(b_relation, x), x))
    k_num = (x**4 - 6 * x**2 + 1) ** 2
    k_den = 4 * x * (x**2 - 1) * (x**2 + 1) ** 2
    l_branch_plus = (b - 2) ** 4 / (8 * b * (b + 2) ** 2)
    l_branch_minus = -((b + 2) ** 4) / (8 * b * (b - 2) ** 2)
    l_relation = sp.expand(
        (8 * b * (b + 2) ** 2 * l - (b - 2) ** 4)
        * (8 * b * (b - 2) ** 2 * l + (b + 2) ** 4)
    )
    return {
        "A_num": sp.factor(a_num),
        "A_den": sp.factor(a_den),
        "B_num": sp.factor(b_num),
        "B_den": sp.factor(b_den),
        "B_relation": sp.factor(b_relation),
        "A_plus_2_minus_B2": sp.factor(sp.together(a_num / a_den + 2 - (b_num / b_den) ** 2)),
        "B_branch_resultant": branch_resultant,
        "K_num": sp.factor(k_num),
        "K_den": sp.factor(k_den),
        "L_branch_Bplus": sp.factor(l_branch_plus),
        "L_branch_Bminus": sp.factor(l_branch_minus),
        "L_relation_over_B": sp.factor(l_relation),
    }


def source_equations() -> dict[str, sp.Expr]:
    x, w, t, beta, r, z, y, eta, bline = sp.symbols("X W T beta R z Y eta Bline")
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
        "Bline_relation": bline * (x**2 - 1) ** 2 - 8 * x**2,
        "first_half_beta": beta**2 * u_den**2 - (u_num**2 - 4 * u_den**2),
        "reverse_x": 4 * z**2 * h_num * (u_num + beta * u_den)
        - 2 * u_den * a_den * (z**4 - 1) ** 2,
        "reverse_Y": y**2 * a_den - h_num,
        "A_num": a_num,
        "A_den": a_den,
        "m0": m0,
        "mt": mt,
        "criterion_num": criterion_num,
        "U_num": u_num,
        "U_den": u_den,
        "x5_num": u_num + beta * u_den,
        "x5_den": 2 * u_den,
        "H_num": h_num,
    }


def emit_formulas(title: str, formulas: dict[str, sp.Expr], keys: list[str]) -> None:
    print(title)
    for key in keys:
        print(f"  {key}: {sp.factor(formulas[key])}")
    print()


def main() -> int:
    b_formulas = b_line_formulas()
    equations = source_equations()

    print("p27 B-line Kummer extraction packet")
    print()
    print("Purpose:")
    print("  Extract the actual d3(B) Kummer/divisor class on P1_B.")
    print("  Use this to decide whether the B-line gives a source, recurrence,")
    print("  or multi-gate coupling that can beat sqrt(p).")
    print()

    emit_formulas(
        "B-line quotient formulas:",
        b_formulas,
        [
            "A_num",
            "A_den",
            "B_num",
            "B_den",
            "B_relation",
            "A_plus_2_minus_B2",
            "B_branch_resultant",
            "K_num",
            "K_den",
            "L_branch_Bplus",
            "L_branch_Bminus",
            "L_relation_over_B",
        ],
    )

    print("Known finite-field facts to preserve:")
    print("  - legal B values stay in the core B bucket in q1607/q1847/q2087")
    print("  - d3 descends to B with no mixed groups in p27 train/heldout")
    print("  - d4 after d3=+1 also descends to B in tested samples")
    print("  - no rational-linear support of weight <=4 for d3(B)")
    print("  - no one irreducible quadratic times <=2 linears for d3(B)")
    print("  - no product of two irreducible quadratics for d3(B)")
    print("  - no product of two irreducible quadratics for the legal B-domain")
    print()

    print("Source equations for the d3 all-plus cover over P1_B:")
    print("  variables: X, W, T, beta, R, z, Y, eta, Bline")
    print("  beta is the first-half branch root; Bline is the quotient coordinate.")
    print(f"  eta_branch: {sp.factor(equations['eta_branch'])} = 0")
    print(f"  E: {sp.factor(equations['E'])} = 0")
    print(f"  T_cover: {sp.factor(equations['T_cover'])} = 0")
    print("  compactD_R: X*R^2 - criterion_num = 0")
    print("  Bline_relation: Bline*(X^2 - 1)^2 - 8*X^2 = 0")
    print("  first_half_beta: beta^2*U_den^2 - (U_num^2 - 4*U_den^2) = 0")
    print("  reverse_x: 4*z^2*H_num*(U_num + beta*U_den)")
    print("             - 2*U_den*A_den*(z^4 - 1)^2 = 0")
    print("  reverse_Y: Y^2*A_den - H_num = 0")
    print()

    emit_formulas(
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
    print("  1. Work first over q=1607,1847,2087.")
    print("  2. Build the legal d2 source using E, T_cover, compactD_R,")
    print("     eta_branch, first_half_beta, and Bline_relation.")
    print("  3. Add reverse_x and reverse_Y to form the d3 all-plus cover.")
    print("  4. Normalize over P1_Bline.")
    print("  5. Compute branch divisor degree, support field degrees, genus,")
    print("     and any involutions/quotients visible over Bline.")
    print("  6. If d3 is low-genus/sourceable, repeat for d4/d5 and compare")
    print("     Kummer classes f3(B), f4(B), f5(B).")
    print()
    print("Promotion bar:")
    print("  - stable branch class across q1607/q1847/q2087")
    print("  - genus <= 1, sourceable walk, or explicit recurrence/coupling")
    print("  - target/source_draw improves without paying fresh half-losses")
    print()
    print("Kill condition:")
    print("  - high/generic branch degree")
    print("  - only previously killed split low-degree supports appear")
    print("  - f4/f5 are unrelated fresh Kummer classes")
    print()
    print("p27_b_line_kummer_extraction_packet_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

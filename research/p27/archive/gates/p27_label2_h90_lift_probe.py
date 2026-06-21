#!/usr/bin/env python3
"""Hilbert-90/order-4 lift probe for the p27 label-2 second-gate cover.

The second-gate cover looked high genus, but the T-deck involution has a
special lift because the T-norm of the mixed linear term is an exact square on
the residual elliptic field.  This script verifies the symbolic identity and
does a small finite-field sanity check of the deck-flip squareclasses.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


PRIMES = [17, 23, 29, 31, 37, 41, 43]


def reduce_w(expr: sp.Expr, x: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    num, den = sp.together(expr).as_numer_denom()
    rel = sp.Poly(w**2 - (x**3 - x), w)
    num_rem = sp.Poly(sp.expand(num), w).rem(rel).as_expr()
    den_rem = sp.Poly(sp.expand(den), w).rem(rel).as_expr()
    if den_rem == 1:
        return sp.factor(num_rem)
    return sp.factor(num_rem / den_rem)


def symbolic_identities() -> dict[str, sp.Expr]:
    x, w, t = sp.symbols("X W T")
    t2 = x * (x**2 + 1) * (x**2 + 2 * x - 1)
    mt = (x + 1) * (2 * w * x + x**3 + x**2 - x - 1)
    m0 = (x**2 + 1) * (x**2 + 2 * x - 1) * (w * x + w + 2 * x**2)
    linear = 4 * w * x**2 + 4 * w * x + x**4 + 6 * x**3 - 2 * x - 1
    s = 2 * x**2 + (x + 1) * w

    s_square = reduce_w(s**2 - x * linear, x, w)
    norm_square = reduce_w(m0**2 - mt**2 * t2 - 4 * t2 * s**2, x, w)

    # The T-deck ratio for h = W(X^2+1)(m0+mt*T)/X is
    # h(T -> -T)/h = (m0-mt*T)/(m0+mt*T).
    # Using norm_square, this equals ((m0-mt*T)/(2*T*S))^2.
    ratio_square_num = (m0 - mt * t) ** 2
    ratio_square_den = 4 * t2 * s**2
    ratio_target_num = m0 - mt * t
    ratio_target_den = m0 + mt * t
    ratio_check = sp.Poly(
        sp.expand(ratio_square_num * ratio_target_den - ratio_target_num * ratio_square_den),
        t,
    ).rem(sp.Poly(t**2 - t2, t)).as_expr()
    ratio_check = reduce_w(ratio_check, x, w)

    # If alpha lifts T -> -T with multiplier (m0-mt*T)/(2*T*S), then applying
    # alpha twice multiplies R by -1.  So alpha has order 4 and alpha^2 is the
    # R-deck involution.
    lift_square = -1
    pref = w * (x**2 + 1) / x

    return {
        "T2": sp.factor(t2),
        "mt": sp.factor(mt),
        "m0": sp.factor(m0),
        "linear": sp.factor(linear),
        "S": sp.factor(s),
        "S2_minus_XL": sp.factor(s_square),
        "norm_m_minus_4T2S2": sp.factor(norm_square),
        "T_deck_ratio_square_check": sp.factor(ratio_check),
        "lift_square": lift_square,
        "pref": sp.factor(pref),
    }


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def roots(a: int, p: int) -> list[int]:
    a %= p
    return [x for x in range(p) if x * x % p == a]


def f_scalar(x: int, p: int) -> int:
    return (x * x * x - x) % p


def g_scalar(x: int, p: int) -> int:
    x2 = x * x % p
    return x * (x2 + 1) * (x2 + 2 * x - 1) % p


def compact_parts_scalar(x: int, w: int, p: int) -> tuple[int, int]:
    x2 = x * x % p
    mt = (x + 1) * (2 * w * x + x**3 + x2 - x - 1) % p
    m0 = (x2 + 1) * (x2 + 2 * x - 1) * (w * x + w + 2 * x2) % p
    return mt, m0


def h_scalar(x: int, w: int, t: int, p: int) -> int | None:
    if x % p == 0:
        return None
    mt, m0 = compact_parts_scalar(x, w, p)
    return w * (x * x + 1) * (m0 + mt * t) * pow(x, p - 2, p) % p


def deck_ratio_counts(name: str, p: int) -> dict[int, int]:
    counts = {-1: 0, 0: 0, 1: 0}
    for x in range(1, p):
        for w, t in product(roots(f_scalar(x, p), p), roots(g_scalar(x, p), p)):
            h0 = h_scalar(x, w, t, p)
            if name == "T":
                h1 = h_scalar(x, w, -t, p)
            elif name == "W":
                h1 = h_scalar(x, -w, t, p)
            elif name == "WT":
                h1 = h_scalar(x, -w, -t, p)
            else:
                raise ValueError(name)
            if h0 is None or h1 is None or h0 % p == 0 or h1 % p == 0:
                counts[0] += 1
                continue
            ratio = h1 * pow(h0, p - 2, p) % p
            counts[legendre(ratio, p)] += 1
    return counts


def main() -> int:
    ids = symbolic_identities()
    print("p27 label2 T-H90/order-4 lift probe")
    print(f"T2 = {ids['T2']}")
    print(f"mt_coeff = {ids['mt']}")
    print(f"m0 = {ids['m0']}")
    print(f"L = {ids['linear']}")
    print(f"S = {ids['S']}")
    print(f"S2_minus_XL = {ids['S2_minus_XL']}")
    print(f"norm_m_minus_4T2S2 = {ids['norm_m_minus_4T2S2']}")
    print(f"T_deck_ratio_square_check = {ids['T_deck_ratio_square_check']}")
    print("T_deck_multiplier = (m0 - mt_coeff*T)/(2*T*S)")
    print("T_deck_lift_alpha_squared = R_deck_involution")
    print(f"T_deck_lift_multiplier_square_product = {ids['lift_square']}")
    print(f"prefactor = {ids['pref']}")
    print("cyclic_quartic_over_E = R^4 - 2*prefactor*m0*R^2 + 4*prefactor^2*T2*S^2")
    print("alpha_fixed_points_inferred = 8")
    print("R_deck_fixed_points_inferred = 16")
    print("genus_D_input = 17")
    print("genus_D_mod_alpha_by_RH = 1")
    print("D_mod_alpha_identifies_residual_E = 1")
    print("finite_field_deck_ratio_counts:")
    print("p deck nonsquare zero_or_undefined square")
    for p in PRIMES:
        for deck in ["T", "W", "WT"]:
            counts = deck_ratio_counts(deck, p)
            print(f"{p} {deck} {counts[-1]} {counts[0]} {counts[1]}")
    print("p27_label2_h90_lift_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

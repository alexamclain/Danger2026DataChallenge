#!/usr/bin/env python3
"""Test whether the K/S first-half B-cover respects the alpha deck.

The saturated q7 Magma smoke found a genus-37 first-half layer.  The next
quotient-shaped hope is that this B-cover still carries the label-2 order-4
alpha symmetry.  This probe packages the exact first-half branch factorization
and tests the two obvious alpha-lift ratios on p27-signature guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp


def legendre(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    v = pow(a, (q - 1) // 2, q)
    return 1 if v == 1 else -1


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def roots_mod(a: int, q: int, sqrt_table: dict[int, list[int]]) -> list[int]:
    return sqrt_table.get(a % q, [])


def make_sqrt_table(q: int) -> dict[int, list[int]]:
    table: dict[int, list[int]] = {}
    for x in range(q):
        table.setdefault((x * x) % q, []).append(x)
    return table


def symbolic_factorization_ok() -> tuple[sp.Expr, sp.Expr]:
    X, W, T, eta = sp.symbols("X W T eta")
    x2 = X**2
    x3 = X**3
    x4 = X**4
    x5 = X**5
    u_core = (
        eta * 4 * T * W * X
        + T * x3
        + T * x2
        - T * X
        - T
        + 2 * x5
        + 2 * x4
        - 2 * x3
        - 2 * x2
    )
    u_num = 2 * u_core
    u_den = (T - 2 * x2) * (X - 1) * (X + 1) ** 2
    lhs = sp.factor(u_num**2 - 4 * u_den**2)
    branch = sp.factor(
        32
        * T
        * X
        * (eta * T * W + X * (X - 1) * (X + 1) ** 2)
        * (2 * eta * W * X + X**3 + X**2 - X - 1)
    )
    return sp.factor(lhs - branch), branch


def same_eta_ratio_identity() -> sp.Expr:
    X, W, T = sp.symbols("X W T")
    pterm = X * (X - 1) * (X + 1) ** 2
    a_plus = T * W + pterm
    a_minus = -T * W + pterm
    t2 = X * (X**2 + 1) * (X**2 + 2 * X - 1)
    e_w = W**2 - (X**3 - X)
    raw = sp.expand(a_plus * a_minus + 4 * X**2 * W**2)
    rem_t = sp.Poly(raw, T).rem(sp.Poly(T**2 - t2, T)).as_expr()
    rem_w = sp.Poly(sp.expand(rem_t), W).rem(sp.Poly(e_w, W)).as_expr()
    return sp.factor(rem_w)


def compactd_h(x: int, w: int, t: int, q: int) -> int:
    x2 = x * x % q
    mt = (x + 1) % q
    mt = mt * ((2 * w * x + x**3 + x2 - x - 1) % q) % q
    m0 = (x2 + 1) % q
    m0 = m0 * ((x2 + 2 * x - 1) % q) % q
    m0 = m0 * ((w * x + w + 2 * x2) % q) % q
    return w * (x2 + 1) % q * ((m0 + mt * t) % q) % q * inv(x, q) % q


def field_stats(q: int) -> Counter:
    sqrt_table = make_sqrt_table(q)
    stats: Counter = Counter()
    for x in range(q):
        if x in (0, 1, q - 1):
            stats["bad_x"] += 1
            continue
        x2 = x * x % q
        w2 = (x**3 - x) % q
        t2 = x * ((x2 + 1) % q) % q * ((x2 + 2 * x - 1) % q) % q
        for w in roots_mod(w2, q, sqrt_table):
            for t in roots_mod(t2, q, sqrt_table):
                stats["intermediate_points"] += 1
                h = compactd_h(x, w, t, q)
                h_chi = legendre(h, q)
                if h_chi == 0:
                    stats["compactd_ramified_or_zero"] += 1
                    continue
                if h_chi != 1:
                    stats["compactd_reject"] += 1
                    continue
                stats["compactd_points"] += 1

                poly = (x**3 + x2 - x - 1) % q
                pterm = x * (x - 1) % q * pow(x + 1, 2, q) % q
                a_plus = (t * w + pterm) % q
                a_minus = (-t * w + pterm) % q
                m_plus = (2 * w * x + poly) % q
                m_flip = (2 * w * x - poly) % q

                if a_plus == 0 or a_minus == 0:
                    stats["same_eta_zero_or_pole"] += 1
                else:
                    stats[f"same_eta_ratio_chi_{legendre(a_minus * inv(a_plus, q), q)}"] += 1

                if m_plus == 0 or m_flip == 0:
                    stats["eta_flip_zero_or_pole"] += 1
                else:
                    stats[f"eta_flip_ratio_chi_{legendre(m_flip * inv(m_plus, q), q)}"] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fields",
        default="1607,1847,2087",
        help="comma-separated p27-signature prime fields",
    )
    args = parser.parse_args()

    diff, branch = symbolic_factorization_ok()
    ratio_identity_diff = same_eta_ratio_identity()
    print("p27_ks_first_half_branch_alpha_probe")
    print(f"symbolic_factorization_diff={diff}")
    print(f"branch_factor={branch}")
    print(f"same_eta_ratio_identity_diff={ratio_identity_diff}")
    print("branch_class_eta_plus=T*X*(T*W + X*(X-1)*(X+1)^2)*(2*W*X + X^3 + X^2 - X - 1)")
    print("same_eta_alpha_ratio=(-T*W + X*(X-1)*(X+1)^2)/(T*W + X*(X-1)*(X+1)^2)")
    print("same_eta_alpha_ratio=-((-T*W + X*(X-1)*(X+1)^2)/(2*X*W))^2 on E,T")
    print("eta_flip_alpha_ratio=(2*W*X - (X^3+X^2-X-1))/(2*W*X + (X^3+X^2-X-1))")
    print()

    for field in args.fields.split(","):
        q = int(field.strip())
        stats = field_stats(q)
        print(f"FIELD q={q}")
        for key in sorted(stats):
            print(f"  {key}={stats[key]}")
        same_pos = stats.get("same_eta_ratio_chi_1", 0)
        same_neg = stats.get("same_eta_ratio_chi_-1", 0)
        flip_pos = stats.get("eta_flip_ratio_chi_1", 0)
        flip_neg = stats.get("eta_flip_ratio_chi_-1", 0)
        print(f"  same_eta_mixed={int(same_pos > 0 and same_neg > 0)}")
        print(f"  eta_flip_mixed={int(flip_pos > 0 and flip_neg > 0)}")
    print("p27_ks_first_half_branch_alpha_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

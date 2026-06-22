#!/usr/bin/env python3
"""Check the K/S first-half B-cover under the (0,0) quotient deck.

The alpha lift is obstructed over F_p by a sqrt(-1) twist.  The other live
quotient is translation by the rational 2-torsion point (0,0) on
E: W^2=X^3-X, whose quotient is E': V^2=U^3+4U.  This probe asks whether the
first-half B-branch class is compatible with that quotient.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp


def legendre(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def make_sqrt_table(q: int) -> dict[int, list[int]]:
    table: dict[int, list[int]] = {}
    for x in range(q):
        table.setdefault((x * x) % q, []).append(x)
    return table


def t2_transform_diff() -> sp.Expr:
    X = sp.symbols("X")
    t2 = X * (X**2 + 1) * (X**2 + 2 * X - 1)
    image = t2.subs(X, -1 / X)
    return sp.factor(sp.together(X**6 * image - t2))


def branch_factorization_diff() -> sp.Expr:
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
    branch = (
        32
        * T
        * X
        * (eta * T * W + X * (X - 1) * (X + 1) ** 2)
        * (2 * eta * W * X + X**3 + X**2 - X - 1)
    )
    return sp.factor(u_num**2 - 4 * u_den**2 - branch)


def compactd_h(x: int, w: int, t: int, q: int) -> int:
    x2 = x * x % q
    mt = (x + 1) % q
    mt = mt * ((2 * w * x + x**3 + x2 - x - 1) % q) % q
    m0 = (x2 + 1) % q
    m0 = m0 * ((x2 + 2 * x - 1) % q) % q
    m0 = m0 * ((w * x + w + 2 * x2) % q) % q
    return w * (x2 + 1) % q * ((m0 + mt * t) % q) % q * inv(x, q) % q


def bbranch_eta_plus(x: int, w: int, t: int, q: int) -> int:
    x2 = x * x % q
    return (
        t
        * x
        * ((t * w + x * (x - 1) * pow(x + 1, 2, q)) % q)
        * ((2 * w * x + x**3 + x2 - x - 1) % q)
    ) % q


def field_stats(q: int) -> Counter:
    table = make_sqrt_table(q)
    stats: Counter = Counter()
    for x in range(q):
        if x in (0, 1, q - 1):
            stats["bad_x"] += 1
            continue
        x2 = x * x % q
        w2 = (x**3 - x) % q
        t2 = x * (x2 + 1) % q * ((x2 + 2 * x - 1) % q) % q
        for w in table.get(w2, []):
            for t in table.get(t2, []):
                stats["intermediate_points"] += 1
                h = compactd_h(x, w, t, q)
                if legendre(h, q) != 1:
                    stats["compactd_reject"] += 1
                    continue
                stats["compactd_points"] += 1
                base = bbranch_eta_plus(x, w, t, q)
                if base == 0:
                    stats["bbranch_zero_base"] += 1
                    continue
                x_image = (-inv(x, q)) % q
                w_image = w * inv(x2, q) % q
                for sign in (1, -1):
                    t_image = sign * t * inv(pow(x, 3, q), q) % q
                    image_t2 = x_image * (x_image * x_image + 1) % q
                    image_t2 = image_t2 * ((x_image * x_image + 2 * x_image - 1) % q) % q
                    if (t_image * t_image - image_t2) % q:
                        stats[f"t_lift_{sign}_bad_t_cover"] += 1
                        continue
                    image_h = compactd_h(x_image, w_image, t_image, q)
                    stats[f"t_lift_{sign}_compactd_chi_{legendre(image_h, q)}"] += 1
                    image_branch = bbranch_eta_plus(x_image, w_image, t_image, q)
                    if image_branch == 0:
                        stats[f"t_lift_{sign}_bbranch_zero_image"] += 1
                        continue
                    ratio = image_branch * inv(base, q) % q
                    stats[f"t_lift_{sign}_bbranch_ratio_chi_{legendre(ratio, q)}"] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27_ks_first_half_t0_descent_probe")
    print("deck = translation by (0,0): X -> -1/X, W -> W/X^2")
    print("quotient = Eprime: U=X-1/X, V=W*(X^2+1)/X^2")
    print("T_lifts = T -> +/- T/X^3")
    print(f"T2_transform_diff={t2_transform_diff()}")
    print(f"branch_factorization_diff={branch_factorization_diff()}")
    print()
    for field in args.fields.split(","):
        q = int(field.strip())
        stats = field_stats(q)
        print(f"FIELD q={q}")
        for key in sorted(stats):
            print(f"  {key}={stats[key]}")
    print("p27_ks_first_half_t0_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

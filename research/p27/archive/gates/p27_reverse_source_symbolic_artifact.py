#!/usr/bin/env python3
"""Emit and verify the p27 reverse-source equations.

This is the Sage/Magma handoff precursor for the reverse-doubling source.  It
derives a single oriented affine model over the label-2 compactD cover and
checks the equations on actual p27 compactD sample points.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

from p27_label2_alpha_branch_recurrence_probe import (
    P,
    compact_class,
    halve_all,
    inv,
    legendre,
    sample_rows,
    sqrt_mod,
)
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row


def x16_a_num_mod(y: int, p: int = P) -> int:
    num = 1
    for coeff in [-8, 24, -32, 8, 32, -48, 32, -8]:
        num = (num * y + coeff) % p
    return num


def formula_values(x: int, w: int, t: int, p: int = P, branch_sign: int = 1) -> dict[str, int]:
    if branch_sign not in (1, -1):
        raise ValueError("branch_sign must be +1 or -1")
    x2 = x * x % p
    x3 = x2 * x % p
    x4 = x2 * x2 % p
    x5 = x4 * x % p
    x6 = x5 * x % p
    den_a = pow(x - 1, 4, p) * pow(x + 1, 4, p) % p
    a_num = -2 * (x**8 - 4 * x**6 - 26 * x**4 - 4 * x2 + 1)
    a = a_num % p * inv(den_a, p) % p

    u_core = (
        branch_sign * 4 * t * w * x
        + t * x3
        + t * x2
        - t * x
        - t
        + 2 * x5
        + 2 * x4
        - 2 * x3
        - 2 * x2
    )
    u_num = 2 * u_core % p
    u_den = (t - 2 * x2) % p
    u_den = u_den * (x - 1) % p
    u_den = u_den * pow(x + 1, 2, p) % p
    u = u_num * inv(u_den, p) % p

    mt = (2 * w * x2 + 2 * w * x + x4 + 2 * x3 - 2 * x - 1) % p
    m0 = (
        w * x6
        + 3 * w * x5
        + 2 * w * x4
        + 2 * w * x3
        + w * x2
        - w * x
        + 2 * x6 * x
        + 4 * x6
        + 4 * x4
        - 2 * x3
    )
    # The C code expression is in powers X^5..X.  Recompute directly to avoid
    # relying on the shifted names above.
    m0 = (
        w * pow(x, 5, p)
        + 3 * w * pow(x, 4, p)
        + 2 * w * pow(x, 3, p)
        + 2 * w * x2
        + w * x
        - w
        + 2 * pow(x, 6, p)
        + 4 * pow(x, 5, p)
        + 4 * pow(x, 3, p)
        - 2 * x2
    ) % p
    criterion = w * (x2 + 1) % p
    criterion = criterion * inv(x, p) % p
    criterion = criterion * ((m0 + mt * t) % p) % p
    return {
        "A": a,
        "A_num": a_num % p,
        "A_den": den_a,
        "u": u,
        "u_num": u_num,
        "u_den": u_den,
        "criterion": criterion,
        "branch_sign": branch_sign,
    }


def symbolic_equations() -> dict[str, sp.Expr]:
    X, W, T, B, R, z, Y, eta = sp.symbols("X W T B R z Y eta")
    x2 = X**2
    x3 = X**3
    x4 = X**4
    x5 = X**5
    x6 = X**6
    x8 = X**8

    A_den = (X - 1) ** 4 * (X + 1) ** 4
    A_num = -2 * (x8 - 4 * X**6 - 26 * x4 - 4 * x2 + 1)
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
    U_num = 2 * u_core
    U_den = (T - 2 * x2) * (X - 1) * (X + 1) ** 2

    mt = 2 * W * x2 + 2 * W * X + x4 + 2 * x3 - 2 * X - 1
    m0 = (
        W * x5
        + 3 * W * x4
        + 2 * W * x3
        + 2 * W * x2
        + W * X
        - W
        + 2 * x6
        + 4 * x5
        + 4 * x3
        - 2 * x2
    )
    criterion_num = W * (x2 + 1) * (m0 + mt * T)
    H_num = z**4 * A_den + A_num * z**2 + A_den

    return {
        "eta_branch": eta**2 - 1,
        "E_W": W**2 - (X**3 - X),
        "T_cover": T**2 - X * (X**2 + 1) * (X**2 + 2 * X - 1),
        "compactD_R": X * R**2 - criterion_num,
        "first_half_B": B**2 * U_den**2 - (U_num**2 - 4 * U_den**2),
        "reverse_x": 4 * z**2 * H_num * (U_num + B * U_den)
        - 2 * U_den * A_den * (z**4 - 1) ** 2,
        "reverse_Y": Y**2 * A_den - H_num,
        "A_num": A_num,
        "A_den": A_den,
        "U_num": U_num,
        "U_den": U_den,
        "x5_num": U_num + B * U_den,
        "x5_den": 2 * U_den,
        "H_num": H_num,
    }


def verify_p27_points(target: int, seed: int, max_draws: int) -> Counter:
    rows, _ = sample_rows(target, seed, max_draws)
    stats: Counter = Counter()
    seen: set[tuple[int, int, int, int, int]] = set()
    for row in rows:
        for cand in all_oriented_candidates_from_row(row, P):
            x = int(cand["X"])
            w = int(cand["W"])
            t = int(cand["T"])
            if int(cand["root_index"]) == 1:
                t = (-t) % P
            a = int(cand["A"])
            x5 = int(cand["x5"])
            key = (x, w, t, a, x5)
            if key in seen:
                continue
            seen.add(key)
            vals0 = formula_values(x, w, t, P, 1)
            if vals0["A"] != a:
                stats["A_mismatch"] += 1
                continue
            matched = None
            for branch_sign in (1, -1):
                vals = formula_values(x, w, t, P, branch_sign)
                u = vals["u"]
                b = (2 * x5 - u) % P
                if b * b % P == (u * u - 4) % P:
                    matched = vals
                    stats[f"B_branch_{'plus' if branch_sign == 1 else 'minus'}"] += 1
                    break
            if matched is None:
                stats["B_mismatch"] += 1
                continue
            vals = matched
            crit = vals["criterion"]
            r = sqrt_mod(crit, P)
            if r is None or compact_class(x, w, t, P) != -1:
                stats["R_missing"] += 1
                continue
            d2, x6s = halve_all(a, x5, P)
            if d2 != 1:
                stats["d2_missing"] += 1
                continue
            for x6 in x6s:
                d3 = (x6 * x6 + a * x6 + 1) % P
                if legendre(x6) != 1:
                    continue
                z0 = sqrt_mod(x6, P)
                y0 = sqrt_mod(d3, P)
                if z0 is None or y0 is None:
                    stats["source_root_missing"] += 1
                    continue
                den = 4 * x6 % P * d3 % P
                reverse_x = (x6 * x6 - 1) % P
                reverse_x = reverse_x * reverse_x % P * inv(den, P) % P
                if reverse_x != x5:
                    stats["reverse_x_mismatch"] += 1
                    continue
                stats["verified_source_points"] += 1
            stats["verified_oriented_candidates"] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=200000)
    args = parser.parse_args()

    eqs = symbolic_equations()
    print("p27 reverse-source symbolic artifact")
    print("variables = X, W, T, B, R, z, Y, eta")
    print("branch convention: eta^2=1; eta chooses the selected first-half square-root sign")
    for key in [
        "eta_branch",
        "E_W",
        "T_cover",
        "compactD_R",
        "first_half_B",
        "reverse_x",
        "reverse_Y",
        "A_num",
        "A_den",
        "U_num",
        "U_den",
        "x5_num",
        "x5_den",
        "H_num",
    ]:
        print(f"{key} = {sp.factor(eqs[key])}")

    stats = verify_p27_points(args.target, args.seed, args.max_draws)
    print("p27_verification:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("p27_reverse_source_symbolic_artifact_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

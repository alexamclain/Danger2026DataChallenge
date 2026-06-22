#!/usr/bin/env python3
"""Emit the symbolic p27 B-line reduced-cover packet.

The reduced d3 fiber uses the halving coordinate

    U_next = x6 + 1/x6

before materializing x6.  If x5 is the current selected x-coordinate, then

    (U_next - 2*x5)^2 = 4*(x5^2 + A*x5 + 1).

This packet writes that equation in the B-line source variables so CAS can try
normalizing the reduced 4-u cover instead of the heavier reverse z/Y cover.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates


def source_equations() -> dict[str, sp.Expr]:
    X, W, T, beta, R, eta, Bline, Unext = sp.symbols("X W T beta R eta Bline Unext")
    x2 = X**2
    x3 = X**3
    x4 = X**4
    x5 = X**5
    x6 = X**6
    x8 = X**8

    A_den = (X - 1) ** 4 * (X + 1) ** 4
    A_num = -2 * (x8 - 4 * x6 - 26 * x4 - 4 * x2 + 1)

    U_core = (
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
    U_num = 2 * U_core
    U_den = (T - 2 * x2) * (X - 1) * (X + 1) ** 2
    x5_num = U_num + beta * U_den

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

    # x5 = x5_num/(2*U_den).  The reduced equation is the denominator-cleared
    # form of (Unext - 2*x5)^2 = 4*(x5^2 + A*x5 + 1).
    reduced_unext_compact = (
        "A_den*(Unext*U_den - x5_num)^2 "
        "- (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2)"
    )

    return {
        "eta_branch": eta**2 - 1,
        "E_W": W**2 - (X**3 - X),
        "T_cover": T**2 - X * (X**2 + 1) * (X**2 + 2 * X - 1),
        "compactD_R": X * R**2 - criterion_num,
        "Bline_relation": Bline * (X**2 - 1) ** 2 - 8 * X**2,
        "first_half_beta": beta**2 * U_den**2 - (U_num**2 - 4 * U_den**2),
        "reduced_Unext_compact": reduced_unext_compact,
        "A_num": A_num,
        "A_den": A_den,
        "U_num": U_num,
        "U_den": U_den,
        "x5_num": x5_num,
        "x5_den": 2 * U_den,
        "criterion_num": criterion_num,
        "selector": Unext + 2,
        "materialize_x6": sp.Symbol("x6") ** 2 - Unext * sp.Symbol("x6") + 1,
    }


def validate_field(q: int) -> Counter:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in dedupe_candidates(candidates):
        A = int(cand["A"]) % q
        x5 = int(cand["x5"]) % q
        X = int(cand["X"]) % q
        B = source_b_plus(X, q)
        if B is None:
            stats["B_degenerate"] += 1
            continue
        if (A + 2 - B * B) % q:
            stats["A_B_identity_mismatch"] += 1
        d2, branches = halve_all(A, x5, q)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        stats["d2_plus_candidates"] += 1
        for x6 in branches:
            if x6 == 0:
                stats["x6_zero"] += 1
                continue
            Unext = (x6 + pow(x6, q - 2, q)) % q
            lhs = (Unext - 2 * x5) % q
            lhs = lhs * lhs % q
            rhs = 4 * ((x5 * x5 + A * x5 + 1) % q) % q
            if lhs != rhs:
                stats["reduced_equation_mismatch"] += 1
            if legendre(Unext + 2, q) != legendre(x6, q):
                stats["selector_mismatch"] += 1
            stats["validated_branches"] += 1
    for key in [
        "A_B_identity_mismatch",
        "B_degenerate",
        "d2_minus",
        "reduced_equation_mismatch",
        "selector_mismatch",
        "x6_zero",
    ]:
        stats.setdefault(key, 0)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    equations = source_equations()
    print("p27 B-line reduced-cover symbolic packet")
    print("purpose = normalize the reduced 4-u d3 cover over legal B")
    print("variables = X, W, T, beta, R, eta, Bline, Unext")
    print("materialized x6, reverse z, and Y are not needed for this reduced cover")
    print()
    print("Equations:")
    for key in [
        "eta_branch",
        "E_W",
        "T_cover",
        "compactD_R",
        "Bline_relation",
        "first_half_beta",
    ]:
        print(f"{key} = {sp.factor(equations[key])}")
    print(f"reduced_Unext = {equations['reduced_Unext_compact']}")
    print()
    print("Auxiliary:")
    for key in [
        "A_num",
        "A_den",
        "U_num",
        "U_den",
        "x5_num",
        "x5_den",
        "criterion_num",
        "selector",
        "materialize_x6",
    ]:
        print(f"{key} = {sp.factor(equations[key])}")
    print()
    print("CAS task:")
    print("  1. Work over q1607/q1847/q2087 or another q=7 mod 16 guard field.")
    print("  2. Saturate by the usual denominator and branch factors.")
    print("  3. Normalize the map to P1_Bline with the reduced_Unext equation.")
    print("  4. Compute genus/components/quotients and test selector chi(Unext+2).")
    print("  5. Compare f4 only after this reduced f3 cover is understood.")
    print()
    print("Validation:")
    for q in parse_ints(args.small_primes):
        stats = validate_field(q)
        print(f"q={q}:")
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
    print("p27_b_line_reduced_cover_symbolic_packet_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

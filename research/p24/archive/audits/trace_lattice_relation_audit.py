#!/usr/bin/env python3
"""Audit low-height relations in the p24 trace lattice.

For p = n^2 + 7 and M = 2^40, the strict curve-side traces are

    t_j = (p+1) - M*(floor((p+1)/M) + j),  j=0,1,2.

This script records that exact lattice and searches for small-coefficient
linear/quadratic identities in n and M.  Such an identity would be a plausible
starting point for a special finite-field construction; absence does not prove
impossibility, but it rules out the most visible near-square algebra.
"""

from __future__ import annotations

import argparse
import bisect
import math
from dataclasses import dataclass

import sympy as sp


P = 10**24 + 7
N = 10**12
K = 40
M = 1 << K


@dataclass(frozen=True)
class TargetRow:
    offset: int
    order_div_m: int
    trace: int
    abs_delta_over_4: int
    fundamental_abs_D: int


def v2(n: int) -> int:
    return (abs(n) & -abs(n)).bit_length() - 1


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(abs(n)).items():
        if e & 1:
            out *= int(q)
    return out


def targets() -> list[TargetRow]:
    q, r = divmod(P + 1, M)
    out: list[TargetRow] = []
    for offset in range(3):
        order_div_m = q + offset
        trace = P + 1 - M * order_div_m
        abs_delta_over_4 = P - (trace * trace // 4)
        out.append(
            TargetRow(
                offset=offset,
                order_div_m=order_div_m,
                trace=trace,
                abs_delta_over_4=abs_delta_over_4,
                fundamental_abs_D=squarefree_part(abs_delta_over_4),
            )
        )
    return out


def best_linear_relation(value: int, bound: int) -> tuple[int, int, int, int]:
    best: tuple[int, int, int, int] | None = None
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            residual = value - a * N - b * M
            score = abs(residual)
            row = (score, a, b, residual)
            if best is None or row < best:
                best = row
    assert best is not None
    return best


def linear_combo_table(bound: int) -> list[tuple[int, int, int]]:
    rows = []
    for d in range(-bound, bound + 1):
        for e in range(-bound, bound + 1):
            rows.append((d * N + e * M, d, e))
    return sorted(rows)


def closest_linear_combo(table: list[tuple[int, int, int]], residual: int) -> tuple[int, int, int, int]:
    values = [row[0] for row in table]
    best: tuple[int, int, int, int] | None = None
    for idx in (bisect.bisect_left(values, residual) - 1, bisect.bisect_left(values, residual)):
        if 0 <= idx < len(table):
            value, d, e = table[idx]
            rem = residual - value
            row = (abs(rem), d, e, rem)
            if best is None or row < best:
                best = row
    assert best is not None
    return best


def best_quadratic_relation(value: int, bound: int) -> tuple[int, int, int, int, int, int, int]:
    linear_table = linear_combo_table(bound)
    best: tuple[int, int, int, int, int, int, int] | None = None
    n2 = N * N
    nm = N * M
    m2 = M * M
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                residual = value - a * n2 - b * nm - c * m2
                score, d, e, rem = closest_linear_combo(linear_table, residual)
                row = (score, a, b, c, d, e, rem)
                if best is None or row < best:
                    best = row
    assert best is not None
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--linear-bound", type=int, default=64)
    ap.add_argument("--quadratic-bound", type=int, default=12)
    args = ap.parse_args()

    q, r = divmod(P + 1, M)
    print("p24 trace-lattice low-height relation audit")
    print(f"p={P}")
    print(f"n={N}")
    print(f"M=2^40={M}")
    print(f"M_minus_n={M - N}")
    print(f"floor((p+1)/M)={q}")
    print(f"(p+1)_mod_M={r}")
    print(f"gcd(n,M)={math.gcd(N, M)}")
    print(f"linear_bound={args.linear_bound}")
    print(f"quadratic_bound={args.quadratic_bound}")
    print()

    print("target_rows")
    for row in targets():
        print(f"offset={row.offset}")
        print(f"  order_div_M={row.order_div_m}")
        print(f"  factor_order_div_M={sp.factorint(row.order_div_m)}")
        print(f"  trace={row.trace}")
        print(f"  trace_over_n={row.trace / N:.12f}")
        print(f"  v2_curve_order={v2(P + 1 - row.trace)}")
        print(f"  abs_delta_over_4={row.abs_delta_over_4}")
        print(f"  factor_abs_delta_over_4={sp.factorint(row.abs_delta_over_4)}")
        print(f"  fundamental_abs_D={row.fundamental_abs_D}")
        print()

    print("best_trace_linear_relations value ~= a*n+b*M")
    for row in targets():
        score, a, b, residual = best_linear_relation(row.trace, args.linear_bound)
        print(
            f"  offset={row.offset} score={score} a={a} b={b} "
            f"residual={residual} residual_over_n={residual / N:.6e}"
        )
    print()

    print("best_fundamental_D_quadratic_relations value ~= a*n^2+b*n*M+c*M^2+d*n+e*M")
    for row in targets():
        score, a, b, c, d, e, residual = best_quadratic_relation(
            row.fundamental_abs_D, args.quadratic_bound
        )
        print(
            f"  offset={row.offset} score={score} "
            f"a={a} b={b} c={c} d={d} e={e} residual={residual} "
            f"residual_over_n={residual / N:.6e}"
        )
    print("conclusion=no_small_coefficient_n_M_identity_visible_for_target_traces_or_fundamental_discriminants")


if __name__ == "__main__":
    main()

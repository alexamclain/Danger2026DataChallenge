#!/usr/bin/env python3
"""Probe low-height near-square formulas on the X1(16) parameter.

Previous p24 probes ruled out small linear-fractional formulas for the final
Montgomery parameter A, A^2, and j in the family p = n^2 + 7.  A hidden section
of the 2-power tower could still look simple on the upstream X1(16) y-line and
messy after conversion to Montgomery form.

For small primes p = n^2 + 7, this script enumerates the X1(16) y-line exactly,
marks y-values whose induced Montgomery parameter has enough x-only 2-power for
the local DANGER depth, and tests low-height LFTs in n against:

    y, y^2, or u = (y^2 - 2)/(y - 1).

This is a formula probe, not a random search.
"""

from __future__ import annotations

import argparse
import math

import numpy as np

from near_square_formula_probe import (
    Formula,
    all_montgomery_traces_fft,
    formulas,
    is_prime_trial,
    legendre_table,
    v2,
    verifier_k,
)


def prime_rows(
    min_p: int,
    max_p: int,
    max_rows: int,
    n_modulus: int,
    n_residue: int,
) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    start_n = max(2, math.isqrt(max(0, min_p - 7)))
    if start_n * start_n + 7 < min_p:
        start_n += 1
    first = start_n + ((n_residue - start_n) % n_modulus)
    for n in range(first, math.isqrt(max_p - 7) + 1, n_modulus):
        p = n * n + 7
        if p < min_p:
            continue
        if is_prime_trial(p):
            rows.append((n, p))
            if len(rows) >= max_rows:
                break
    return rows


def inverse_table(p: int) -> np.ndarray:
    inv = np.zeros(p, dtype=np.int64)
    inv[1] = 1
    for a in range(2, p):
        inv[a] = (p - (p // a) * int(inv[p % a]) % p) % p
    return inv


def sqrt_table(p: int) -> np.ndarray:
    roots = np.full(p, -1, dtype=np.int64)
    for x in range(p):
        roots[x * x % p] = x
    return roots


def exact_xonly_good(A: int, trace: int, p: int, k: int, chi: np.ndarray) -> bool:
    split = int(chi[(A * A - 4) % p]) == 1
    curve_v = v2(p + 1 - trace)
    twist_v = v2(p + 1 + trace)
    if split:
        curve_exp = max(0, curve_v - 1)
        twist_exp = max(0, twist_v - 1)
    else:
        curve_exp = curve_v
        twist_exp = twist_v
    return max(curve_exp, twist_exp) >= k


def x16_A_from_y(y: int, p: int, inv: np.ndarray) -> int | None:
    ym1 = (y - 1) % p
    den = 4 * pow(ym1, 4, p) % p
    if den == 0:
        return None

    y2 = y * y % p
    y3 = y2 * y % p
    y4 = y2 * y2 % p
    y5 = y4 * y % p
    y6 = y3 * y3 % p
    y7 = y6 * y % p
    y8 = y4 * y4 % p
    num = (
        y8
        - 8 * y7
        + 24 * y6
        - 32 * y5
        + 8 * y4
        + 32 * y3
        - 48 * y2
        + 32 * y
        - 8
    ) % p
    return num * int(inv[den]) % p


def x16_y_has_model_root(y: int, p: int, chi: np.ndarray) -> bool:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return False
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    return int(chi[disc]) >= 0


def good_parameter_sets(p: int, mode: str) -> tuple[np.ndarray, dict[str, int]]:
    chi = legendre_table(p)
    inv = inverse_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    k = verifier_k(p)
    roots = sqrt_table(p) if mode == "y2" else None

    good_y = np.zeros(p, dtype=np.bool_)
    good_param = np.zeros(p, dtype=np.bool_)
    x16_y_count = 0
    good_A_count = 0

    for y in range(1, p):
        if not x16_y_has_model_root(y, p, chi):
            continue
        A = x16_A_from_y(y, p, inv)
        if A is None or (A * A - 4) % p == 0:
            continue
        x16_y_count += 1
        trace = int(traces[A])
        if not exact_xonly_good(A, trace, p, k, chi):
            continue

        good_A_count += 1
        good_y[y] = True
        if mode == "y":
            good_param[y] = True
        elif mode == "y2":
            good_param[y * y % p] = True
        elif mode == "u":
            den = (y - 1) % p
            if den:
                u = (y * y - 2) % p * int(inv[den]) % p
                good_param[u] = True
        else:
            raise ValueError(mode)

    stats = {
        "k": k,
        "fft_error_scaled": int(round(fft_error * 1_000_000)),
        "x16_y_count": x16_y_count,
        "good_y_count": int(np.count_nonzero(good_y)),
        "good_A_count_with_multiplicity": good_A_count,
        "good_param_count": int(np.count_nonzero(good_param)),
    }

    if mode == "y2":
        # Sanity check the square table is populated for every marked y^2.
        assert roots is not None
        for value in np.flatnonzero(good_param):
            if int(roots[int(value)]) < 0:
                raise AssertionError(value)

    return good_param, stats


def eval_formula_for_mode(f: Formula, n: int, p: int, mode: str) -> int | None:
    value = f.eval(n, p)
    if value is None:
        return None
    if mode == "y" and value == 0:
        return None
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=500_000)
    ap.add_argument("--max-rows", type=int, default=30)
    ap.add_argument("--coeff-bound", type=int, default=6)
    ap.add_argument("--mode", choices=["y", "y2", "u"], default="y")
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = formulas(args.coeff_bound)
    hits = {f: 0 for f in fs}
    valid = {f: 0 for f in fs}
    survivors = set(fs)

    print("x16 near-square section formula probe")
    print("family=p=n^2+7")
    print(f"mode={args.mode}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"formula_count={len(fs)}")

    for index, (n, p) in enumerate(rows, start=1):
        good, stats = good_parameter_sets(p, args.mode)
        next_survivors: set[Formula] = set()
        for f in fs:
            value = eval_formula_for_mode(f, n, p, args.mode)
            if value is None:
                continue
            valid[f] += 1
            if bool(good[value]):
                hits[f] += 1
                if f in survivors:
                    next_survivors.add(f)
        survivors = next_survivors

        print(
            f"row={index:02d} n={n} p={p} k={stats['k']} "
            f"x16_y={stats['x16_y_count']} "
            f"good_y={stats['good_y_count']} "
            f"good_param={stats['good_param_count']} "
            f"fft_error_scaled={stats['fft_error_scaled']} "
            f"survivors_all_rows_so_far={len(survivors)}"
        )

    ranked = sorted(
        fs,
        key=lambda f: (hits[f], valid[f], -sum(map(abs, (f.a, f.b, f.c, f.d)))),
        reverse=True,
    )
    print("top_formulas_by_hit_count")
    for f in ranked[: args.top]:
        print(f"  hits={hits[f]:2d}/{valid[f]:2d} formula={f.label()}")
    print(f"perfect_survivors={len(survivors)}")
    for f in sorted(survivors, key=lambda row: row.label())[: args.top]:
        print(f"  survivor={f.label()}")
    print(
        "conclusion=no_low_height_x16_section_formula"
        if not survivors
        else "conclusion=surviving_x16_section_formula_lead"
    )


if __name__ == "__main__":
    main()

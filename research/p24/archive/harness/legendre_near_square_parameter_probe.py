#!/usr/bin/env python3
"""Probe near-square formulas in Legendre / split-Montgomery parameters.

Previous probes ruled out low-height formulas for the final Montgomery A,
Montgomery j, and upstream X1(16) parameters.  A split curve can still have a
simple 2-torsion root r or Legendre modulus lambda while

    A = -(r + 1/r)
    j = 256*(1 - lambda + lambda^2)^3/(lambda^2*(1-lambda)^2)

looks too nonlinear for an LFT-in-n probe.

For small primes p = n^2 + 7, this script computes all Montgomery traces using
the FFT convolution from near_square_formula_probe.py, keeps only split
Montgomery curves whose curve or twist has enough x-only 2-power for the local
DANGER depth, and tests low-height LFTs in n against:

    root    : r, 1/r where x^2 + A*x + 1 = (x-r)(x-1/r)
    lambda  : the S3 orbit of lambda = r^2
    landen  : (1-r)/(1+r) and the same expression with r inverted

This is exact over the small fields; it is not a p24 brute-force search.
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


def s3_lambda_orbit(lam: int, p: int, inv: np.ndarray) -> set[int]:
    if lam in (0, 1):
        return set()
    one_minus = (1 - lam) % p
    return {
        lam,
        int(inv[lam]),
        one_minus,
        int(inv[one_minus]),
        lam * int(inv[(lam - 1) % p]) % p,
        (lam - 1) % p * int(inv[lam]) % p,
    }


def landen_values(r: int, p: int, inv: np.ndarray) -> set[int]:
    out: set[int] = set()
    for value in {r, int(inv[r])}:
        den = (1 + value) % p
        if den:
            out.add((1 - value) % p * int(inv[den]) % p)
    return out


def split_strict_good_parameters(p: int, mode: str) -> tuple[np.ndarray, dict[str, int]]:
    chi = legendre_table(p)
    inv = inverse_table(p)
    sqrts = sqrt_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    k = verifier_k(p)
    inv2 = (p + 1) // 2
    marked = np.zeros(p, dtype=np.bool_)

    split_A = 0
    good_split_A = 0
    for A in range(p):
        disc = (A * A - 4) % p
        sd = int(sqrts[disc])
        if sd < 0:
            continue
        split_A += 1
        trace = int(traces[A])
        if max(v2(p + 1 - trace), v2(p + 1 + trace)) < k + 1:
            continue
        good_split_A += 1

        r1 = (-A + sd) * inv2 % p
        r2 = (-A - sd) * inv2 % p
        if r1 == 0 or r2 == 0:
            continue

        if mode == "root":
            marked[r1] = True
            marked[r2] = True
        elif mode == "lambda":
            lam = r1 * int(inv[r2]) % p
            for value in s3_lambda_orbit(lam, p, inv):
                marked[value] = True
        elif mode == "landen":
            for value in landen_values(r1, p, inv) | landen_values(r2, p, inv):
                marked[value] = True
        else:
            raise ValueError(mode)

    return marked, {
        "k": k,
        "fft_error_scaled": int(round(fft_error * 1_000_000)),
        "split_A": split_A,
        "good_split_A": good_split_A,
        "marked_count": int(np.count_nonzero(marked)),
    }


def eval_formula(f: Formula, n: int, p: int) -> int | None:
    value = f.eval(n, p)
    if value is None or value == 0:
        return None
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=250_000)
    ap.add_argument("--max-rows", type=int, default=20)
    ap.add_argument("--coeff-bound", type=int, default=8)
    ap.add_argument("--mode", choices=["root", "lambda", "landen"], default="root")
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = formulas(args.coeff_bound)
    hits = {f: 0 for f in fs}
    valid = {f: 0 for f in fs}
    survivors = set(fs)

    print("legendre near-square parameter formula probe")
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
        marked, stats = split_strict_good_parameters(p, args.mode)
        next_survivors: set[Formula] = set()
        for f in fs:
            value = eval_formula(f, n, p)
            if value is None:
                continue
            valid[f] += 1
            if bool(marked[value]):
                hits[f] += 1
                if f in survivors:
                    next_survivors.add(f)
        survivors = next_survivors

        print(
            f"row={index:02d} n={n} p={p} k={stats['k']} "
            f"split_A={stats['split_A']} "
            f"good_split_A={stats['good_split_A']} "
            f"marked={stats['marked_count']} "
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
        "conclusion=no_low_height_legendre_parameter_formula"
        if not survivors
        else "conclusion=surviving_legendre_parameter_formula_lead"
    )


if __name__ == "__main__":
    main()

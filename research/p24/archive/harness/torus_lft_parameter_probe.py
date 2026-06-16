#!/usr/bin/env python3
"""Probe near-singular torus-coordinate formulas for strict DANGER traces.

The singular Montgomery limits A = +/-2 are multiplicative/norm-one tori, but
they are rejected by the verifier and for p24 have only tiny 2-power depth.
The remaining hope is a structured perturbation of the torus:

    A =  s * (r + 1/r),      s in {+1, -1},

where the torus coordinate r itself is a simple function of n in the family
p = n^2 + 7.  This is a focused near-singular audit: it tests low-height LFTs

    r(n) = (a*n + b)/(c*n + d)

and maps them to Montgomery A before checking the exact strict x-only bucket
by trace convolution over small calibration primes.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

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


@dataclass(frozen=True)
class TorusFormula:
    sign: int
    r_formula: Formula

    def eval_A(self, n: int, p: int) -> int | None:
        r = self.r_formula.eval(n, p)
        if r is None or r == 0:
            return None
        inv_r = pow(r, p - 2, p)
        return self.sign * (r + inv_r) % p

    def label(self) -> str:
        prefix = "" if self.sign == 1 else "-"
        return f"A={prefix}(r+1/r), r={self.r_formula.label()}"


def prime_rows(min_p: int, max_p: int, max_rows: int, n_modulus: int, n_residue: int) -> list[tuple[int, int]]:
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


def exact_good_A(p: int) -> tuple[np.ndarray, dict[str, int]]:
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    k = verifier_k(p)
    good = np.zeros(p, dtype=np.bool_)
    split_good = 0
    nonsplit_good = 0
    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            continue
        split = int(chi[disc]) == 1
        t = int(traces[A])
        curve_v = v2(p + 1 - t)
        twist_v = v2(p + 1 + t)
        if split:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        ok = max(curve_exp, twist_exp) >= k
        good[A] = ok
        if ok and split:
            split_good += 1
        elif ok:
            nonsplit_good += 1
    return good, {
        "k": k,
        "good": int(np.count_nonzero(good)),
        "split_good": split_good,
        "nonsplit_good": nonsplit_good,
        "fft_error_scaled": int(round(float(fft_error) * 1_000_000)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=250_000)
    ap.add_argument("--max-rows", type=int, default=20)
    ap.add_argument("--coeff-bound", type=int, default=8)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    r_formulas = formulas(args.coeff_bound)
    fs = [TorusFormula(sign, f) for f in r_formulas for sign in (-1, 1)]
    hits = {f: 0 for f in fs}
    valid = {f: 0 for f in fs}
    singular = {f: 0 for f in fs}
    survivors = set(fs)

    print("near-singular torus-coordinate LFT probe")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"r_formula_count={len(r_formulas)}")
    print(f"torus_formula_count={len(fs)}")

    for index, (n, p) in enumerate(rows, start=1):
        good, stats = exact_good_A(p)
        next_survivors: set[TorusFormula] = set()
        for f in fs:
            A = f.eval_A(n, p)
            if A is None:
                continue
            if (A * A - 4) % p == 0:
                singular[f] += 1
                continue
            valid[f] += 1
            if bool(good[A]):
                hits[f] += 1
                if f in survivors:
                    next_survivors.add(f)
        survivors = next_survivors
        print(
            f"row={index:02d} n={n} p={p} k={stats['k']} "
            f"good={stats['good']} split_good={stats['split_good']} "
            f"nonsplit_good={stats['nonsplit_good']} "
            f"fft_error_scaled={stats['fft_error_scaled']} "
            f"survivors_all_rows_so_far={len(survivors)}"
        )

    ranked = sorted(
        fs,
        key=lambda f: (
            hits[f],
            valid[f],
            -singular[f],
            -sum(abs(x) for x in (f.r_formula.a, f.r_formula.b, f.r_formula.c, f.r_formula.d)),
        ),
        reverse=True,
    )
    print("top_torus_formulas_by_hit_count")
    for f in ranked[: args.top]:
        print(
            f"  hits={hits[f]:2d}/{valid[f]:2d} singular={singular[f]:2d} "
            f"formula={f.label()}"
        )
    print(f"perfect_survivors={len(survivors)}")
    for f in sorted(survivors, key=lambda row: row.label())[: args.top]:
        print(f"  survivor={f.label()}")
    print(
        "conclusion=no_low_height_torus_lft_parameter"
        if not survivors
        else "conclusion=surviving_torus_lft_parameter_lead"
    )


if __name__ == "__main__":
    main()

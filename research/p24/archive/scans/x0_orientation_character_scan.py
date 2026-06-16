#!/usr/bin/env python3
"""Scan cheap labels for the X0-to-X1 orientation gap.

AGM/Landen/2-isogeny dynamics naturally gives X0(2^d): a rational cyclic
2^d-isogeny chain.  The strict DANGER verifier needs X1-like orientation: an
x-only point of order 2^d on the curve or twist.

This exact small-field scan conditions on the X0 event and asks whether simple
Legendre labels chi(q(A,n)) can choose the missing X1 orientation.  A useful
canonical branch rule would show stable high lift inside the X0 bucket; a
constant/noisy lift means the orientation cover is still the hard part.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import product

import numpy as np

from near_square_formula_probe import all_montgomery_traces_fft, legendre_table, v2
from low_degree_character_trace_scan import prime_rows


@dataclass(frozen=True)
class Feature:
    a2: int
    b2: int
    a1: int
    b1: int
    a0: int
    b0: int

    def coeffs(self, n: int, p: int) -> tuple[int, int, int]:
        return (
            (self.a2 * n + self.b2) % p,
            (self.a1 * n + self.b1) % p,
            (self.a0 * n + self.b0) % p,
        )

    def label(self) -> str:
        def part(a: int, b: int) -> str:
            if a == 0:
                return str(b)
            if b == 0:
                return f"{a}*n"
            sign = "+" if b > 0 else ""
            return f"{a}*n{sign}{b}"

        return f"({part(self.a2,self.b2)})*A^2+({part(self.a1,self.b1)})*A+({part(self.a0,self.b0)})"


def features(bound: int, include_linear_n: bool) -> list[Feature]:
    vals = range(-bound, bound + 1)
    n_vals = vals if include_linear_n else [0]
    out: set[Feature] = set()
    for raw in product(n_vals, vals, n_vals, vals, n_vals, vals):
        if all(v == 0 for v in raw):
            continue
        g = 0
        for v in raw:
            g = math.gcd(g, abs(v))
        if g > 1:
            raw = tuple(v // g for v in raw)
        first = next(v for v in raw if v)
        if first < 0:
            raw = tuple(-v for v in raw)
        out.add(Feature(*raw))
    return sorted(
        out,
        key=lambda f: (
            sum(abs(v) for v in (f.a2, f.b2, f.a1, f.b1, f.a0, f.b0)),
            f.a2,
            f.b2,
            f.a1,
            f.b1,
            f.a0,
            f.b0,
        ),
    )


def x0_residues(p: int, d: int) -> set[int]:
    modulus = 1 << d
    out: set[int] = set()
    for lam in range(1, modulus, 2):
        mu = p * pow(lam, -1, modulus) % modulus
        out.add((lam + mu) % modulus)
    return out


def x1_x0_flags(p: int, n: int, depth: int, chi: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    residues = x0_residues(p, depth)
    modulus = 1 << depth
    x0 = np.zeros(p, dtype=np.bool_)
    x1 = np.zeros(p, dtype=np.bool_)
    nonsingular = np.ones(p, dtype=np.bool_)
    split_count = 0

    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            nonsingular[A] = False
            continue
        split = int(chi[disc]) == 1
        split_count += int(split)
        t = int(traces[A])
        x0[A] = (t % modulus in residues) or ((-t) % modulus in residues)
        curve_v = v2(p + 1 - t)
        twist_v = v2(p + 1 + t)
        if split:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        x1[A] = max(curve_exp, twist_exp) >= depth

    x0 &= nonsingular
    x1 &= nonsingular
    return x1, x0, {
        "fft_error_scaled": int(round(fft_error * 1_000_000)),
        "nonsingular": int(np.count_nonzero(nonsingular)),
        "split": split_count,
        "x0": int(np.count_nonzero(x0)),
        "x1": int(np.count_nonzero(x1)),
        "x1_inside_x0": int(np.count_nonzero(x1 & x0)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=160_000)
    ap.add_argument("--max-rows", type=int, default=10)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--depth", type=int, default=8)
    ap.add_argument("--coeff-bound", type=int, default=2)
    ap.add_argument("--constant-coeffs", action="store_true")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--min-coverage", type=float, default=0.02)
    ap.add_argument("--max-coverage", type=float, default=0.98)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = features(args.coeff_bound, include_linear_n=not args.constant_coeffs)
    cum_hits = np.zeros((len(fs), 2), dtype=np.int64)
    cum_total = np.zeros((len(fs), 2), dtype=np.int64)
    cum_x1 = 0
    cum_x0 = 0

    print("X0-to-X1 orientation character scan")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"depth={args.depth}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"constant_coeffs={args.constant_coeffs}")
    print(f"feature_count={len(fs)}")

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        x1, x0, stats = x1_x0_flags(p, n, args.depth, chi)
        base_hits = int(np.count_nonzero(x1 & x0))
        base_total = int(np.count_nonzero(x0))
        base_rate = base_hits / base_total if base_total else 0.0
        cum_x1 += base_hits
        cum_x0 += base_total
        A = np.arange(p, dtype=np.int64)
        A2 = A * A % p

        best: list[tuple[float, str]] = []
        for idx, feature in enumerate(fs):
            c2, c1, c0 = feature.coeffs(n, p)
            values = (c2 * A2 + c1 * A + c0) % p
            signs = chi[values]
            for sign_index, sign in enumerate((-1, 1)):
                selected = x0 & (signs == sign)
                total = int(np.count_nonzero(selected))
                if total == 0:
                    continue
                coverage = total / base_total
                if coverage < args.min_coverage or coverage > args.max_coverage:
                    continue
                hits = int(np.count_nonzero(selected & x1))
                cum_total[idx, sign_index] += total
                cum_hits[idx, sign_index] += hits
                precision = hits / total
                lift = precision / base_rate if base_rate else 0.0
                capture = hits / base_hits if base_hits else 0.0
                score = lift * math.sqrt(capture)
                if lift > 1.0:
                    best.append(
                        (
                            score,
                            f"sign={sign:+d} lift={lift:.3f} capture={capture:.3f} "
                            f"coverage={coverage:.3f} hits={hits}/{total} feature={feature.label()}",
                        )
                    )

        print(
            f"row={row_index:02d} n={n} p={p} "
            f"x0={stats['x0']} x1={stats['x1']} x1_inside_x0={stats['x1_inside_x0']} "
            f"base_rate={base_rate:.6f}"
        )
        for _, text in sorted(best, reverse=True)[: args.top]:
            print(f"  {text}")

    base = cum_x1 / cum_x0 if cum_x0 else 0.0
    print(f"aggregate x1_inside_x0={cum_x1}/{cum_x0} base_rate={base:.6f}")
    ranked: list[tuple[float, str]] = []
    for idx, feature in enumerate(fs):
        for sign_index, sign in enumerate((-1, 1)):
            total = int(cum_total[idx, sign_index])
            if total == 0:
                continue
            hits = int(cum_hits[idx, sign_index])
            precision = hits / total
            lift = precision / base if base else 0.0
            capture = hits / cum_x1 if cum_x1 else 0.0
            coverage = total / cum_x0 if cum_x0 else 0.0
            if coverage < args.min_coverage or coverage > args.max_coverage:
                continue
            score = lift * math.sqrt(capture)
            if lift > 1.0:
                ranked.append(
                    (
                        score,
                        f"sign={sign:+d} lift={lift:.3f} capture={capture:.3f} "
                        f"coverage={coverage:.3f} hits={hits}/{total} feature={feature.label()}",
                    )
                )
    print("aggregate_top_features")
    for _, text in sorted(ranked, reverse=True)[: args.top]:
        print(f"  {text}")
    best_lift = 0.0
    if base:
        for i in range(len(fs)):
            for s in range(2):
                total = int(cum_total[i, s])
                if not total:
                    continue
                coverage = total / cum_x0 if cum_x0 else 0.0
                if coverage < args.min_coverage or coverage > args.max_coverage:
                    continue
                best_lift = max(best_lift, int(cum_hits[i, s]) / total / base)
    print(f"best_aggregate_lift={best_lift:.6f}")
    print("conclusion=no_growing_low_degree_character_orientation_selector")


if __name__ == "__main__":
    main()

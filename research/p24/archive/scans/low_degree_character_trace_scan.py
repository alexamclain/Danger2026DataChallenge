#!/usr/bin/env python3
"""Scan low-degree Legendre labels against the strict p=n^2+7 trace bucket.

The missing strict-DANGER primitive could be a cheap curve-level trace-v2 label:
something much cheaper than point counting that predicts whether a Montgomery
parameter A lands in the high 2-adic x-only bucket.

This exact small-field audit tests a concrete version of that idea.  For small
primes p = n^2 + 7, it computes every Montgomery trace by convolution, marks
the exact strict x-only DANGER bucket, and scans Legendre labels

    chi(q(A,n))

where q is quadratic in A and each coefficient is linear in n with small
integer coefficients.

This can only discover constant-bit labels, not prove an asymptotic tower.  Its
purpose is to catch or rule out visible low-degree trace-v2 structure before
spending time on a more elaborate construction.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from itertools import product

import numpy as np

from near_square_formula_probe import (
    all_montgomery_traces_fft,
    is_prime_trial,
    legendre_table,
    v2,
    verifier_k,
)


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
        return (
            f"(({self.a2})n+{self.b2})*A^2+"
            f"(({self.a1})n+{self.b1})*A+"
            f"(({self.a0})n+{self.b0})"
        )


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


def features(bound: int, include_linear_n: bool) -> list[Feature]:
    vals = range(-bound, bound + 1)
    n_vals = vals if include_linear_n else [0]
    out: list[Feature] = []
    seen: set[Feature] = set()
    for a2, b2, a1, b1, a0, b0 in product(n_vals, vals, n_vals, vals, n_vals, vals):
        if a2 == b2 == a1 == b1 == a0 == b0 == 0:
            continue
        row = Feature(a2, b2, a1, b1, a0, b0)
        # Coarse integer normalization to cut exact duplicates.
        coeffs = (a2, b2, a1, b1, a0, b0)
        g = 0
        for value in coeffs:
            g = math.gcd(g, abs(value))
        if g > 1:
            row = Feature(*(value // g for value in coeffs))
        first = next(value for value in (row.a2, row.b2, row.a1, row.b1, row.a0, row.b0) if value)
        if first < 0:
            row = Feature(-row.a2, -row.b2, -row.a1, -row.b1, -row.a0, -row.b0)
        if row not in seen:
            seen.add(row)
            out.append(row)
    return sorted(
        out,
        key=lambda row: (
            sum(abs(x) for x in (row.a2, row.b2, row.a1, row.b1, row.a0, row.b0)),
            row.a2,
            row.b2,
            row.a1,
            row.b1,
            row.a0,
            row.b0,
        ),
    )


def exact_xonly_good_flags(p: int, chi: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    k = verifier_k(p)
    good = np.zeros(p, dtype=np.bool_)
    nonsingular = np.ones(p, dtype=np.bool_)
    split_count = 0
    nonsplit_count = 0

    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            nonsingular[A] = False
            continue
        split = int(chi[disc]) == 1
        split_count += int(split)
        nonsplit_count += int(not split)
        trace = int(traces[A])
        curve_v = v2(p + 1 - trace)
        twist_v = v2(p + 1 + trace)
        if split:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        good[A] = max(curve_exp, twist_exp) >= k

    return good & nonsingular, {
        "k": k,
        "fft_error_scaled": int(round(fft_error * 1_000_000)),
        "nonsingular": int(np.count_nonzero(nonsingular)),
        "split": split_count,
        "nonsplit": nonsplit_count,
        "good": int(np.count_nonzero(good & nonsingular)),
    }


def summarize_row(rows: list[tuple[float, str]], top: int) -> None:
    for score, text in sorted(rows, reverse=True)[:top]:
        print(f"    score={score:.6f} {text}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=150_000)
    ap.add_argument("--max-rows", type=int, default=12)
    ap.add_argument("--coeff-bound", type=int, default=2)
    ap.add_argument("--constant-coeffs", action="store_true")
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-coverage", type=float, default=0.02)
    ap.add_argument("--max-coverage", type=float, default=0.98)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = features(args.coeff_bound, include_linear_n=not args.constant_coeffs)
    cum_hits = np.zeros((len(fs), 2), dtype=np.int64)
    cum_total = np.zeros((len(fs), 2), dtype=np.int64)
    cum_good = 0
    cum_nonsingular = 0

    print("low-degree character trace-v2 scan")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"constant_coeffs={args.constant_coeffs}")
    print(f"feature_count={len(fs)}")

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        A = np.arange(p, dtype=np.int64)
        A2 = A * A % p
        nonsingular = np.ones(p, dtype=np.bool_)
        nonsingular[[2, p - 2]] = False
        base_total = int(stats["nonsingular"])
        base_hits = int(stats["good"])
        base_rate = base_hits / base_total if base_total else 0.0
        cum_good += base_hits
        cum_nonsingular += base_total

        best: list[tuple[float, str]] = []
        for idx, feature in enumerate(fs):
            c2, c1, c0 = feature.coeffs(n, p)
            if c2 == c1 == c0 == 0:
                continue
            values = (c2 * A2 + c1 * A + c0) % p
            signs = chi[values]
            for sign_index, sign in enumerate((-1, 1)):
                selected = nonsingular & (signs == sign)
                total = int(np.count_nonzero(selected))
                if total == 0:
                    continue
                coverage = total / base_total
                if coverage < args.min_coverage or coverage > args.max_coverage:
                    continue
                hits = int(np.count_nonzero(selected & good))
                cum_total[idx, sign_index] += total
                cum_hits[idx, sign_index] += hits
                precision = hits / total
                lift = precision / base_rate if base_rate else 0.0
                capture = hits / base_hits if base_hits else 0.0
                # Favor labels that improve precision while still capturing a
                # nontrivial share of the bucket.
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
            f"row={row_index:02d} n={n} p={p} k={stats['k']} "
            f"good={base_hits}/{base_total} base_rate={base_rate:.6f} "
            f"split={stats['split']} nonsplit={stats['nonsplit']} "
            f"fft_error_scaled={stats['fft_error_scaled']}"
        )
        summarize_row(best, args.top)

    aggregate_base = cum_good / cum_nonsingular if cum_nonsingular else 0.0
    aggregate_rows: list[tuple[float, str]] = []
    for idx, feature in enumerate(fs):
        for sign_index, sign in enumerate((-1, 1)):
            total = int(cum_total[idx, sign_index])
            if total == 0:
                continue
            hits = int(cum_hits[idx, sign_index])
            precision = hits / total
            lift = precision / aggregate_base if aggregate_base else 0.0
            capture = hits / cum_good if cum_good else 0.0
            coverage = total / cum_nonsingular if cum_nonsingular else 0.0
            score = lift * math.sqrt(capture)
            if lift > 1.0:
                aggregate_rows.append(
                    (
                        score,
                        f"sign={sign:+d} lift={lift:.3f} capture={capture:.3f} "
                        f"coverage={coverage:.3f} hits={hits}/{total} feature={feature.label()}",
                    )
                )

    print()
    print(
        f"aggregate good={cum_good}/{cum_nonsingular} "
        f"base_rate={aggregate_base:.6f}"
    )
    print("aggregate_top_features")
    summarize_row(aggregate_rows, args.top)
    best_lift = max((float(text.split("lift=")[1].split()[0]) for _score, text in aggregate_rows), default=0.0)
    print(f"best_aggregate_lift={best_lift:.6f}")
    print(
        "conclusion=only_constant_scale_low_degree_character_labels_seen"
        if best_lift < 2.0
        else "conclusion=visible_character_label_lead"
    )


if __name__ == "__main__":
    main()

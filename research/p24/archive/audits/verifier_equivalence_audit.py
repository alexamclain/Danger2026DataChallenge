#!/usr/bin/env python3
"""Exact small-field audit of the DANGER3 verifier equivalence.

The strict verifier accepts an affine x-coordinate when the Montgomery x-only
doubling map reaches infinity exactly at depth k.  The working assumption in
the p24 notes is that this is equivalent to an exact order-2^k point on the
curve or its quadratic twist.  In split Montgomery form the rational 2-primary
exponent is one less than v2(#E), while in the nonsplit/cyclic case it equals
v2(#E).

This script checks that equivalence directly for small p = n^2 + 7 fields:
for every nonsingular A, it enumerates every x accepted by the literal
doubling verifier and compares the count with the trace/group-structure
prediction.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows
from near_square_formula_probe import all_montgomery_traces_fft, legendre_table, v2, verifier_k


@dataclass(frozen=True)
class RowSummary:
    n: int
    p: int
    k: int
    total_A: int
    total_accepted_x: int
    total_predicted_x: int
    mismatches: int
    max_abs_diff: int
    good_A: int


def exponent_v2(order_v2: int, split: bool) -> int:
    if order_v2 == 0:
        return 0
    return order_v2 - 1 if split and order_v2 >= 2 else order_v2


def xcoords_exact_order(k: int, exponent: int, split: bool) -> int:
    if exponent < k or k < 2:
        return 0
    if split:
        return 1 << (k - 1)
    return 1 << (k - 2)


def verifier_accept_count(p: int, A: int, k: int) -> int:
    inv4 = pow(4, -1, p)
    C = ((A + 2) * inv4) % p
    X = np.arange(p, dtype=np.int64)
    Z = np.ones(p, dtype=np.int64)
    Zprev = Z
    for _ in range(k):
        Zprev = Z
        xpz = (X + Z) % p
        xmz = (X - Z) % p
        U = (xpz * xpz) % p
        V = (xmz * xmz) % p
        W = (U - V) % p
        X = (U * V) % p
        Z = (W * ((V + C * W) % p)) % p
    return int(np.count_nonzero((Z == 0) & (Zprev != 0)))


def predicted_accept_count(p: int, A: int, trace: int, chi: np.ndarray, k: int) -> int:
    split = int(chi[(A * A - 4) % p]) == 1
    curve_exp = exponent_v2(v2(p + 1 - trace), split)
    twist_exp = exponent_v2(v2(p + 1 + trace), split)
    return xcoords_exact_order(k, curve_exp, split) + xcoords_exact_order(k, twist_exp, split)


def audit_row(n: int, p: int, max_mismatches_to_print: int) -> RowSummary:
    k = verifier_k(p)
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    if fft_error > 0.25:
        raise RuntimeError(f"FFT trace error too large for p={p}: {fft_error}")

    total_A = 0
    total_accepted = 0
    total_predicted = 0
    mismatches = 0
    max_abs_diff = 0
    good_A = 0
    printed = 0

    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        total_A += 1
        actual = verifier_accept_count(p, A, k)
        predicted = predicted_accept_count(p, A, int(traces[A]), chi, k)
        total_accepted += actual
        total_predicted += predicted
        good_A += int(actual > 0)
        diff = actual - predicted
        if diff:
            mismatches += 1
            max_abs_diff = max(max_abs_diff, abs(diff))
            if printed < max_mismatches_to_print:
                split = int(chi[(A * A - 4) % p]) == 1
                print(
                    f"  mismatch A={A} trace={int(traces[A])} split={int(split)} "
                    f"actual={actual} predicted={predicted}"
                )
                printed += 1

    return RowSummary(
        n=n,
        p=p,
        k=k,
        total_A=total_A,
        total_accepted_x=total_accepted,
        total_predicted_x=total_predicted,
        mismatches=mismatches,
        max_abs_diff=max_abs_diff,
        good_A=good_A,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=500)
    ap.add_argument("--max-p", type=int, default=12_000)
    ap.add_argument("--max-rows", type=int, default=6)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-mismatches-to-print", type=int, default=8)
    ap.add_argument(
        "--max-literal-work",
        type=int,
        default=10_000_000,
        help="skip rows with roughly p*(p-2) literal x-map evaluations above this",
    )
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("strict verifier exact-order equivalence audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print("row n p k total_A accepted_x predicted_x good_A mismatches max_abs_diff")

    summaries: list[RowSummary] = []
    for index, (n, p) in enumerate(rows, start=1):
        literal_work = p * max(0, p - 2)
        if literal_work > args.max_literal_work:
            print(
                f"{index:02d} {n} {p} skip literal_work={literal_work} "
                f"max_literal_work={args.max_literal_work}"
            )
            continue
        summary = audit_row(n, p, args.max_mismatches_to_print)
        summaries.append(summary)
        print(
            f"{index:02d} {summary.n} {summary.p} {summary.k} {summary.total_A} "
            f"{summary.total_accepted_x} {summary.total_predicted_x} {summary.good_A} "
            f"{summary.mismatches} {summary.max_abs_diff}"
        )

    print("aggregate")
    print(f"  checked_rows={len(summaries)}")
    print(f"  total_accepted_x={sum(row.total_accepted_x for row in summaries)}")
    print(f"  total_predicted_x={sum(row.total_predicted_x for row in summaries)}")
    print(f"  total_mismatching_A={sum(row.mismatches for row in summaries)}")
    if not summaries:
        print("conclusion=no_rows_checked_under_literal_work_budget")
    elif all(row.mismatches == 0 for row in summaries):
        print("conclusion=literal_verifier_matches_exact_order_curve_or_twist_prediction")
    else:
        print("conclusion=review_verifier_equivalence_mismatches")


if __name__ == "__main__":
    main()

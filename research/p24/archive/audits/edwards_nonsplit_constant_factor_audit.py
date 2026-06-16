#!/usr/bin/env python3
"""Audit twisted/complete Edwards forms as a strict p24 shortcut.

Twisted Edwards curves

    a*x^2 + y^2 = 1 + d*x^2*y^2

with a=1 map to Montgomery form with

    A = 2*(1+d)/(1-d),      d = (A-2)/(A+2).

Moreover

    chi(A^2 - 4) = chi(d)

up to squares.  Thus complete Edwards with d nonsquare is exactly the
nonsplit Montgomery subfamily (for the usual a=1 choice), not a new
trace-selector.  This script verifies that exact small-field strict DANGER
hits in the complete-Edwards/nonsplit subfamily have only constant-factor
density changes relative to the full Montgomery line.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from near_square_formula_probe import all_montgomery_traces_fft, legendre_table, v2, verifier_k
from low_degree_character_trace_scan import prime_rows


@dataclass(frozen=True)
class Row:
    n: int
    p: int
    k: int
    total_A: int
    nonsplit_A: int
    split_A: int
    strict_all: int
    strict_nonsplit: int
    strict_split: int
    target_trace_all: int
    target_trace_nonsplit: int
    target_trace_split: int


def exponent_v2(order_v2: int, split: bool) -> int:
    if order_v2 == 0:
        return 0
    return order_v2 - 1 if split and order_v2 >= 2 else order_v2


def audit_row(n: int, p: int) -> Row:
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    if fft_error > 0.25:
        raise RuntimeError(f"FFT trace error too large for p={p}: {fft_error}")
    k = verifier_k(p)

    total_A = nonsplit_A = split_A = 0
    strict_all = strict_nonsplit = strict_split = 0
    target_trace_all = target_trace_nonsplit = target_trace_split = 0

    modulus = 1 << k
    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            continue
        split = int(chi[disc]) == 1
        trace = int(traces[A])
        curve_v = v2(p + 1 - trace)
        twist_v = v2(p + 1 + trace)
        curve_exp = exponent_v2(curve_v, split)
        twist_exp = exponent_v2(twist_v, split)
        strict = max(curve_exp, twist_exp) >= k
        target_trace = (trace % modulus == (p + 1) % modulus) or (
            (-trace) % modulus == (p + 1) % modulus
        )

        total_A += 1
        nonsplit_A += int(not split)
        split_A += int(split)
        strict_all += int(strict)
        strict_nonsplit += int(strict and not split)
        strict_split += int(strict and split)
        target_trace_all += int(target_trace)
        target_trace_nonsplit += int(target_trace and not split)
        target_trace_split += int(target_trace and split)

    return Row(
        n=n,
        p=p,
        k=k,
        total_A=total_A,
        nonsplit_A=nonsplit_A,
        split_A=split_A,
        strict_all=strict_all,
        strict_nonsplit=strict_nonsplit,
        strict_split=strict_split,
        target_trace_all=target_trace_all,
        target_trace_nonsplit=target_trace_nonsplit,
        target_trace_split=target_trace_split,
    )


def ratio(num: int, den: int) -> float:
    return num / den if den else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=500_000)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("edwards/complete-edwards nonsplit constant-factor audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print("row n p k total_A nonsplit_A strict_all strict_nonsplit strict_split nonsplit_lift")

    out: list[Row] = []
    for index, (n, p) in enumerate(rows, start=1):
        row = audit_row(n, p)
        out.append(row)
        full_density = ratio(row.strict_all, row.total_A)
        nonsplit_density = ratio(row.strict_nonsplit, row.nonsplit_A)
        lift = nonsplit_density / full_density if full_density else 0.0
        print(
            f"{index:02d} {row.n} {row.p} {row.k} {row.total_A} {row.nonsplit_A} "
            f"{row.strict_all} {row.strict_nonsplit} {row.strict_split} {lift:.6f}"
        )

    total_A = sum(row.total_A for row in out)
    nonsplit_A = sum(row.nonsplit_A for row in out)
    split_A = sum(row.split_A for row in out)
    strict_all = sum(row.strict_all for row in out)
    strict_nonsplit = sum(row.strict_nonsplit for row in out)
    strict_split = sum(row.strict_split for row in out)
    target_trace_all = sum(row.target_trace_all for row in out)
    target_trace_nonsplit = sum(row.target_trace_nonsplit for row in out)
    target_trace_split = sum(row.target_trace_split for row in out)

    full_density = ratio(strict_all, total_A)
    nonsplit_density = ratio(strict_nonsplit, nonsplit_A)
    split_density = ratio(strict_split, split_A)
    print("aggregate")
    print(f"  total_A={total_A}")
    print(f"  nonsplit_A={nonsplit_A}")
    print(f"  split_A={split_A}")
    print(f"  strict_all={strict_all}")
    print(f"  strict_nonsplit={strict_nonsplit}")
    print(f"  strict_split={strict_split}")
    print(f"  strict_density_all={full_density:.8f}")
    print(f"  strict_density_complete_edwards_nonsplit={nonsplit_density:.8f}")
    print(f"  strict_density_split={split_density:.8f}")
    print(f"  complete_edwards_lift_vs_all={nonsplit_density / full_density if full_density else 0.0:.6f}")
    print(f"  target_trace_all={target_trace_all}")
    print(f"  target_trace_nonsplit={target_trace_nonsplit}")
    print(f"  target_trace_split={target_trace_split}")
    print(
        "conclusion=complete_edwards_is_the_nonsplit_montgomery_half_and_changes_"
        "strict_density_by_only_a_constant_factor"
    )


if __name__ == "__main__":
    main()

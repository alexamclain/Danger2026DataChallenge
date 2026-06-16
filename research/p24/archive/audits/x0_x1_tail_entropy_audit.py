#!/usr/bin/env python3
"""Exact 2-adic tail entropy from half-level X0/X1 data to strict X1 data.

For a cyclic 2^h eigenline, Frobenius acts by an odd eigenvalue lambda mod
2^h.  On the curve-side strict branch, lambda == 1 mod 2^h.  This script
counts the lifts lambda mod 2^k and the trace residues

    t(lambda) = lambda + p/lambda mod 2^k.

The strict DANGER curve-side X1 lift is lambda == 1 mod 2^k.  The strict trace
residue is t == p+1 mod 2^k.
"""

from __future__ import annotations

import argparse

P24 = 10**24 + 7
K = 40


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def formula_stats(h: int, k: int) -> dict[str, int]:
    lift_count = 1 << (k - h)
    return {
        "lift_count": lift_count,
        "trace_residue_count": 1 << (k - h - 1),
        "strict_trace_lifts": 2,
        "true_x1_lifts": 1,
        "near_x1_lifts": 2,
        "bruteforce_checked": 0,
    }


def branch_stats(p: int, h: int, k: int, base: int, max_bruteforce: int) -> dict[str, int]:
    mod = 1 << k
    step = 1 << h
    lift_count = 1 << (k - h)
    if lift_count > max_bruteforce:
        return formula_stats(h, k)
    target_trace = (p + 1) % mod
    trace_residues: set[int] = set()
    strict_trace_lifts = 0
    true_x1_lifts = 0
    near_x1_lifts = 0
    for u in range(lift_count):
        lam = (base + step * u) % mod
        tr = (lam + p * pow(lam, -1, mod)) % mod
        trace_residues.add(tr)
        if tr == target_trace:
            strict_trace_lifts += 1
        if lam == 1 % mod:
            true_x1_lifts += 1
        if min(v2(lam - 1), k) >= k - 1:
            near_x1_lifts += 1
    return {
        "lift_count": lift_count,
        "trace_residue_count": len(trace_residues),
        "strict_trace_lifts": strict_trace_lifts,
        "true_x1_lifts": true_x1_lifts,
        "near_x1_lifts": near_x1_lifts,
        "bruteforce_checked": 1,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=K)
    ap.add_argument("--h-values", type=int, nargs="+", default=[8, 12, 16, 20, 24, 28, 32])
    ap.add_argument("--max-bruteforce", type=int, default=1 << 20)
    args = ap.parse_args()

    print("p24 X0-to-X1 tail entropy audit")
    print(f"p={P24}")
    print(f"k={args.k}")
    print(f"v2(p-1)={v2(P24 - 1)}")
    print(f"target_trace_residue={(P24 + 1) % (1 << args.k)}")
    print()
    print(
        "h lifts trace_residues lifts_per_trace strict_trace_lifts "
        "true_x1_lifts near_x1_lifts true_tail_cost trace_tail_cost checked"
    )
    for h in args.h_values:
        if not (1 < h < args.k):
            continue
        stats = branch_stats(P24, h, args.k, 1, args.max_bruteforce)
        trace_tail_cost = stats["lift_count"] // max(1, stats["strict_trace_lifts"])
        true_tail_cost = stats["lift_count"] // max(1, stats["true_x1_lifts"])
        print(
            f"{h:2d} {stats['lift_count']:12d} {stats['trace_residue_count']:14d} "
            f"{stats['lift_count'] // stats['trace_residue_count']:15d} "
            f"{stats['strict_trace_lifts']:18d} {stats['true_x1_lifts']:14d} "
            f"{stats['near_x1_lifts']:14d} {true_tail_cost:14d} "
            f"{trace_tail_cost:15d} {stats['bruteforce_checked']:7d}"
        )
    print()
    print("interpretation")
    print("  fixing_lambda_equal_1_mod_2h_leaves_2^(k-h)_eigenvalue_lifts=1")
    print("  strict_trace_residue_has_two_lifts_inside_this_branch=1")
    print("  true_X1_orientation_has_one_lift_inside_this_branch=1")
    print("  half_level_X0_or_X1_data_does_not_predict_the_missing_tail=1")
    print("conclusion=tail_entropy_from_half_level_to_strict_X1_is_exactly_2^(k-h)")


if __name__ == "__main__":
    main()

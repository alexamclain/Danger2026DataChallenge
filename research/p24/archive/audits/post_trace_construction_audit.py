#!/usr/bin/env python3
"""Audit what remains after a target-trace Montgomery curve is known.

The strict DANGER3 search can be split into two conceptual steps:

1. construct a nonsingular Montgomery parameter A whose curve or twist has a
   signed trace s with p + 1 - s divisible by the verifier power 2^k;
2. find an x-coordinate of exact x-only order 2^k on that known curve/twist.

This small-field audit measures those two costs separately in the family
p = n^2 + 7.  It computes every Montgomery trace by convolution, counts how
many A values lie in the signed target trace classes, and then uses the
2-primary group structure to count accepted x-coordinates.  It deliberately
does not enumerate all (A,x) pairs.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows
from near_square_formula_probe import (
    all_montgomery_traces_fft,
    legendre_table,
    montgomery_j_from_A,
    v2,
    verifier_k,
)


@dataclass(frozen=True)
class SideCounts:
    signed_trace: int
    curve_A: int
    twist_A: int
    strict_curve_A: int
    strict_twist_A: int
    curve_x: int
    twist_x: int


@dataclass(frozen=True)
class RowSummary:
    n: int
    p: int
    k: int
    signed_targets: tuple[int, ...]
    nonsingular_A: int
    target_trace_A: int
    raw_side_hits: int
    strict_good_A: int
    lost_to_split: int
    accepted_x_total: int
    distinct_target_j: int
    distinct_strict_j: int
    max_target_bucket: int
    side_counts: tuple[SideCounts, ...]


def signed_target_traces(p: int, k: int) -> tuple[int, ...]:
    """Hasse traces s with p + 1 - s == 0 mod 2^k."""
    modulus = 1 << k
    residue = (p + 1) % modulus
    bound = math.isqrt(4 * p)
    first = -bound + ((residue + bound) % modulus)
    return tuple(range(first, bound + 1, modulus))


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


def side_x_count(p: int, k: int, trace: int, split: bool, twist: bool) -> int:
    order = p + 1 + trace if twist else p + 1 - trace
    exp = exponent_v2(v2(order), split)
    return xcoords_exact_order(k, exp, split)


def audit_row(n: int, p: int) -> RowSummary:
    k = verifier_k(p)
    chi = legendre_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    if fft_error > 0.25:
        raise RuntimeError(f"FFT trace error too large for p={p}: {fft_error}")

    targets = signed_target_traces(p, k)
    target_set = set(targets)
    actual_trace_set = target_set | {-t for t in targets}

    trace_buckets: Counter[int] = Counter()
    target_j: set[int] = set()
    strict_j: set[int] = set()
    side_rows: dict[int, list[int]] = {s: [0, 0, 0, 0, 0, 0] for s in targets}

    nonsingular = 0
    target_trace_A = 0
    raw_side_hits = 0
    strict_good_A = 0
    lost_to_split = 0
    accepted_x_total = 0

    for A in range(p):
        disc = (A * A - 4) % p
        if disc == 0:
            continue
        nonsingular += 1
        trace = int(traces[A])
        trace_buckets[trace] += 1
        if trace not in actual_trace_set:
            continue

        target_trace_A += 1
        j = montgomery_j_from_A(A, p)
        if j is not None:
            target_j.add(j)

        split = int(chi[disc]) == 1
        curve_signed = trace
        twist_signed = -trace
        curve_raw = curve_signed in target_set
        twist_raw = twist_signed in target_set
        raw_side_hits += int(curve_raw) + int(twist_raw)

        curve_x = side_x_count(p, k, trace, split, twist=False) if curve_raw else 0
        twist_x = side_x_count(p, k, trace, split, twist=True) if twist_raw else 0
        total_x = curve_x + twist_x
        accepted_x_total += total_x
        if total_x:
            strict_good_A += 1
            if j is not None:
                strict_j.add(j)
        else:
            lost_to_split += 1

        if curve_raw:
            row = side_rows[curve_signed]
            row[0] += 1
            row[2] += int(curve_x > 0)
            row[4] += curve_x
        if twist_raw:
            row = side_rows[twist_signed]
            row[1] += 1
            row[3] += int(twist_x > 0)
            row[5] += twist_x

    side_counts = tuple(
        SideCounts(
            signed_trace=s,
            curve_A=row[0],
            twist_A=row[1],
            strict_curve_A=row[2],
            strict_twist_A=row[3],
            curve_x=row[4],
            twist_x=row[5],
        )
        for s, row in side_rows.items()
    )
    max_target_bucket = max((trace_buckets[t] for t in actual_trace_set), default=0)
    return RowSummary(
        n=n,
        p=p,
        k=k,
        signed_targets=targets,
        nonsingular_A=nonsingular,
        target_trace_A=target_trace_A,
        raw_side_hits=raw_side_hits,
        strict_good_A=strict_good_A,
        lost_to_split=lost_to_split,
        accepted_x_total=accepted_x_total,
        distinct_target_j=len(target_j),
        distinct_strict_j=len(strict_j),
        max_target_bucket=max_target_bucket,
        side_counts=side_counts,
    )


def format_ratio(num: float, den: float) -> str:
    return "nan" if den == 0 else f"{num / den:.6f}"


def print_row(summary: RowSummary, details: bool) -> None:
    root = math.sqrt(summary.p)
    avg_x = summary.accepted_x_total / summary.strict_good_A if summary.strict_good_A else 0.0
    print(
        f"{summary.n:5d} {summary.p:8d} {summary.k:2d} "
        f"{len(summary.signed_targets):3d} {summary.target_trace_A:8d} "
        f"{summary.strict_good_A:8d} {summary.lost_to_split:8d} "
        f"{format_ratio(summary.target_trace_A, root):>10s} "
        f"{format_ratio(summary.strict_good_A, root):>10s} "
        f"{summary.distinct_target_j:8d} {summary.distinct_strict_j:8d} "
        f"{summary.max_target_bucket:8d} {summary.accepted_x_total:12d} "
        f"{avg_x:10.2f}"
    )
    if not details:
        return
    for side in summary.side_counts:
        print(
            f"    s={side.signed_trace:+8d} "
            f"curve_A={side.curve_A:6d} twist_A={side.twist_A:6d} "
            f"strict_curve_A={side.strict_curve_A:6d} "
            f"strict_twist_A={side.strict_twist_A:6d} "
            f"curve_x={side.curve_x:9d} twist_x={side.twist_x:9d}"
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=10)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--details", action="store_true")
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("post-trace DANGER3 construction audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(
        "n p k signed target_A strict_A lost_split target/sqrt "
        "strict/sqrt target_j strict_j max_bucket accepted_x avg_x_per_strict_A"
    )

    summaries = [audit_row(n, p) for n, p in rows]
    for summary in summaries:
        print_row(summary, args.details)

    target_A = sum(row.target_trace_A for row in summaries)
    strict_A = sum(row.strict_good_A for row in summaries)
    accepted_x = sum(row.accepted_x_total for row in summaries)
    lost = sum(row.lost_to_split for row in summaries)
    root_sum = sum(math.sqrt(row.p) for row in summaries)
    print("aggregate")
    print(f"  checked_rows={len(summaries)}")
    print(f"  target_trace_A={target_A}")
    print(f"  strict_good_A={strict_A}")
    print(f"  lost_to_split={lost}")
    print(f"  accepted_x_total={accepted_x}")
    print(f"  target_A_over_sum_sqrt={format_ratio(target_A, root_sum)}")
    print(f"  strict_A_over_sum_sqrt={format_ratio(strict_A, root_sum)}")
    if strict_A:
        print(f"  avg_x_per_strict_A={accepted_x / strict_A:.6f}")
    print("  projected_group_point_expected_trials_per_known_good_side<=2")
    print(
        "conclusion=post_trace_x0_is_constant_expected_after_A_is_known; "
        "target_trace_A_construction_remains_sqrt_scale_in_this_calibration"
    )


if __name__ == "__main__":
    main()

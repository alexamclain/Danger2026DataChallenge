#!/usr/bin/env python3
"""Small-prime conditioned trace calibration for X1(16) families.

The p23 probability model uses

    hazard_all_x1 ~= 16 * trace_mass * L

where L absorbs family bias, p-specific effects, and downstream halving
survival.  This helper isolates the first component on small primes: among
sampled X1(16) Montgomery curves, how often does the trace itself fall in the
admissible high-2-adic trace set?

It is intentionally small-prime and brute-force.  It does not touch the active
p23 production run.
"""

from __future__ import annotations

import argparse
import math
import random
import time
from collections import Counter

from x16_hazard_calibration import compute_k, odd_parts, trace_mass
from x16_trace_residue_calibration import (
    P23,
    find_calibration_prime,
    trace_for_montgomery_A,
    x16_montgomery_A_values,
)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def target_traces(p: int) -> set[int]:
    k = compute_k(p)
    twok = 1 << k
    return {p + 1 - twok * m for m in odd_parts(p, k)}


def wilson_half_width(successes: int, total: int) -> float:
    if total == 0:
        return 0.0
    z = 1.96
    phat = successes / total
    denom = 1 + z * z / total
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total) / denom
    return half


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=int, nargs="+", default=[100_000, 300_000, 1_000_000])
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260602)
    ap.add_argument("--modulus", type=int, default=120, help="match p23 modulo this value")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    print("X1(16) conditioned trace calibration")
    print(f"starts={args.starts}")
    print(f"samples_per_prime={args.samples}")
    print(f"seed={args.seed}")
    print(f"modulus={args.modulus}")
    print(f"p23_mod_modulus={P23 % args.modulus}")
    print()

    for start in args.starts:
        p = find_calibration_prime(start, args.modulus, P23 % args.modulus)
        k = compute_k(p)
        targets = target_traces(p)
        tm = trace_mass(p, k)
        heuristic = 16.0 * tm

        t0 = time.perf_counter()
        As = x16_montgomery_A_values(p, rng, args.samples)
        rows: list[tuple[int, int, str]] = []
        for A in As:
            trace = trace_for_montgomery_A(p, A)
            cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
            rows.append((A, trace, cls))
        elapsed = time.perf_counter() - t0

        all_hits = sum(1 for _A, trace, _cls in rows if trace in targets)
        nonsplit_rows = [(A, trace, cls) for A, trace, cls in rows if cls == "nonsplit"]
        split_rows = [(A, trace, cls) for A, trace, cls in rows if cls == "split"]
        nonsplit_hits = sum(1 for _A, trace, _cls in nonsplit_rows if trace in targets)
        split_hits = sum(1 for _A, trace, _cls in split_rows if trace in targets)

        all_rate = all_hits / len(rows) if rows else 0.0
        nonsplit_rate = nonsplit_hits / len(nonsplit_rows) if nonsplit_rows else 0.0
        split_rate = split_hits / len(split_rows) if split_rows else 0.0
        all_L_trace = all_rate / heuristic if heuristic else 0.0
        nonsplit_L_trace = nonsplit_rate / heuristic if heuristic else 0.0
        split_L_trace = split_rate / heuristic if heuristic else 0.0

        trace_hist = Counter(trace for _A, trace, _cls in rows)
        cls_counts = Counter(cls for _A, _trace, cls in rows)
        print(f"p={p}")
        print(f"k={k}")
        print(f"sqrt_p={math.isqrt(p)}")
        print(f"target_trace_count={len(targets)}")
        print(f"target_traces={sorted(targets)}")
        print(f"trace_mass={tm:.9e}")
        print(f"heuristic_16x_trace_mass={heuristic:.9e}")
        print(f"elapsed_seconds={elapsed:.6f}")
        print(f"samples={len(rows)}")
        print("split_class_counts=" + ",".join(f"{key}:{cls_counts[key]}" for key in sorted(cls_counts)))
        print(
            "all_x16 "
            f"hits={all_hits}/{len(rows)} rate={all_rate:.6f} "
            f"wilson_half={wilson_half_width(all_hits, len(rows)):.6f} "
            f"L_trace={all_L_trace:.3f}"
        )
        print(
            "nonsplit_x16 "
            f"hits={nonsplit_hits}/{len(nonsplit_rows)} rate={nonsplit_rate:.6f} "
            f"wilson_half={wilson_half_width(nonsplit_hits, len(nonsplit_rows)):.6f} "
            f"L_trace={nonsplit_L_trace:.3f}"
        )
        print(
            "split_x16 "
            f"hits={split_hits}/{len(split_rows)} rate={split_rate:.6f} "
            f"wilson_half={wilson_half_width(split_hits, len(split_rows)):.6f} "
            f"L_trace={split_L_trace:.3f}"
        )
        print("observed_target_trace_hist=" + ",".join(
            f"{trace}:{trace_hist[trace]}" for trace in sorted(targets) if trace_hist[trace]
        ))
        print()


if __name__ == "__main__":
    main()

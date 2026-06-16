#!/usr/bin/env python3
"""Exact small-prime X1(16) trace enumeration.

This enumerates the accepted X1(16) sampler stream for a small prime, counting
root multiplicity as the C sampler does: a y whose quadratic fiber splits gives
two marked xP candidates with the same Montgomery A and trace.

It is meant to de-noise the sampled conditioned-trace calibration at primes
small enough for brute-force point counting.
"""

from __future__ import annotations

import argparse
import math
import time
from collections import Counter

from x16_hazard_calibration import compute_k, odd_parts, trace_mass
from x16_trace_residue_calibration import (
    P23,
    find_calibration_prime,
    inv,
    sqrt_mod,
    trace_for_montgomery_A,
)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def x16_A_from_y(y: int, p: int) -> int | None:
    ym1 = (y - 1) % p
    if ym1 == 0:
        return None
    P = (
        pow(y, 8, p)
        - 8 * pow(y, 7, p)
        + 24 * pow(y, 6, p)
        - 32 * pow(y, 5, p)
        + 8 * pow(y, 4, p)
        + 32 * pow(y, 3, p)
        - 48 * (y * y % p)
        + 32 * y
        - 8
    ) % p
    den = 4 * pow(ym1, 4, p) % p
    if den == 0:
        return None
    A = P * inv(den, p) % p
    if A <= 2 or A >= p - 2:
        return None
    return A


def fiber_root_count(y: int, p: int) -> int:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return 0
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    sd = sqrt_mod(disc, p)
    if sd is None:
        return 0
    if sd == 0:
        return 1
    inv_2qa = inv(2 * qa, p)
    roots = {((sd - qb) * inv_2qa) % p, ((-sd - qb) * inv_2qa) % p}
    return len(roots)


def target_traces(p: int) -> set[int]:
    k = compute_k(p)
    twok = 1 << k
    return {p + 1 - twok * m for m in odd_parts(p, k)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0)
    ap.add_argument("--start", type=int, default=10_000)
    ap.add_argument("--modulus", type=int, default=120)
    args = ap.parse_args()

    p = args.p or find_calibration_prime(args.start, args.modulus, P23 % args.modulus)
    k = compute_k(p)
    targets = target_traces(p)
    tm = trace_mass(p, k)
    heuristic = 16.0 * tm

    t0 = time.perf_counter()
    trace_cache: dict[int, int] = {}
    rows = 0
    y_accept = 0
    degenerate_roots = 0
    class_counts: Counter[str] = Counter()
    class_hits: Counter[str] = Counter()
    trace_hist: Counter[int] = Counter()
    target_trace_hist: Counter[int] = Counter()
    unique_As: set[int] = set()

    for y in range(1, p):
        A = x16_A_from_y(y, p)
        if A is None:
            continue
        mult = fiber_root_count(y, p)
        if mult == 0:
            continue
        y_accept += 1
        if mult == 1:
            degenerate_roots += 1
        unique_As.add(A)
        if A not in trace_cache:
            trace_cache[A] = trace_for_montgomery_A(p, A)
        trace = trace_cache[A]
        cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
        rows += mult
        class_counts[cls] += mult
        trace_hist[trace] += mult
        if trace in targets:
            class_hits[cls] += mult
            target_trace_hist[trace] += mult

    elapsed = time.perf_counter() - t0
    all_hits = sum(class_hits.values())
    print("X1(16) exact trace enumeration")
    print(f"p={p}")
    print(f"k={k}")
    print(f"sqrt_p={math.isqrt(p)}")
    print(f"mod120={p % 120}")
    print(f"target_trace_count={len(targets)}")
    print(f"target_traces={sorted(targets)}")
    print(f"trace_mass={tm:.9e}")
    print(f"heuristic_16x_trace_mass={heuristic:.9e}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"accepted_y={y_accept}")
    print(f"candidate_rows_with_root_multiplicity={rows}")
    print(f"unique_A={len(unique_As)}")
    print(f"trace_cache_size={len(trace_cache)}")
    print(f"degenerate_root_y={degenerate_roots}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print()
    for cls in ["all", "nonsplit", "split"]:
        total = rows if cls == "all" else class_counts[cls]
        hits = all_hits if cls == "all" else class_hits[cls]
        rate = hits / total if total else 0.0
        L = rate / heuristic if heuristic else 0.0
        print(f"{cls}_x16 hits={hits}/{total} rate={rate:.9f} L_trace={L:.3f}")
    print("target_trace_hist=" + ",".join(f"{tr}:{target_trace_hist[tr]}" for tr in sorted(target_trace_hist)))


if __name__ == "__main__":
    main()

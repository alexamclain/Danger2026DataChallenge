#!/usr/bin/env python3
"""Exact small-prime X1(16) v2(#E) distribution by split/nonsplit class."""

from __future__ import annotations

import argparse
import time
from collections import Counter

from x16_trace_residue_calibration import trace_for_montgomery_A
from x16_exact_trace_enumeration import fiber_root_count, legendre, x16_A_from_y


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    args = ap.parse_args()
    p = args.p

    start = time.perf_counter()
    trace_cache: dict[int, int] = {}
    rows = 0
    class_counts: Counter[str] = Counter()
    class_v2_hist: Counter[str] = Counter()
    class_v2_ge: Counter[str] = Counter()
    unique_As: set[int] = set()
    for y in range(1, p):
        A = x16_A_from_y(y, p)
        if A is None:
            continue
        mult = fiber_root_count(y, p)
        if mult == 0:
            continue
        unique_As.add(A)
        if A not in trace_cache:
            trace_cache[A] = trace_for_montgomery_A(p, A)
        trace = trace_cache[A]
        cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
        e2 = v2(p + 1 - trace)
        rows += mult
        class_counts[cls] += mult
        class_v2_hist[f"{cls}:v2={e2}"] += mult
        for threshold in range(1, 13):
            if e2 >= threshold:
                class_v2_ge[f"{cls}:ge{threshold}"] += mult
    elapsed = time.perf_counter() - start

    print("X1(16) exact v2(#E) distribution")
    print(f"p={p}")
    print(f"mod120={p % 120}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"rows={rows}")
    print(f"unique_A={len(unique_As)}")
    print(f"trace_cache_size={len(trace_cache)}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print("class_v2_hist=" + ",".join(f"{k}:{class_v2_hist[k]}" for k in sorted(class_v2_hist)))
    print("threshold_rates")
    for threshold in range(1, 13):
        pieces = []
        for cls in ["nonsplit", "split"]:
            total = class_counts[cls]
            hits = class_v2_ge[f"{cls}:ge{threshold}"]
            rate = hits / total if total else 0.0
            pieces.append(f"{cls}:ge{threshold}={hits}/{total}:{rate:.6f}")
        print(" ".join(pieces))


if __name__ == "__main__":
    main()

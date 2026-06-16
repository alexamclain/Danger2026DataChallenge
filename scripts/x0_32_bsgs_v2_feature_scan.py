#!/usr/bin/env python3
"""Sample X0(32) rows and scan cheap features against exact curve-v2.

The earlier X0(32) curve-v2 feature scan was limited to small primes because
it brute-counted points.  This helper reuses the Hasse-interval BSGS trace
routine to test the same question at larger calibration primes:

    Can cheap X0(32) parameter characters predict v2(#E(Fp))?

This is a calibration helper only.  It does not touch p23 production workers.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter

import sympy as sp

import x0_32_small_prime_probe as x0
from x0_32_v2_feature_scan import feature_labels
from x16_bsgs_trace_sample import trace_bsgs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--rows", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=20260631)
    ap.add_argument("--root-method", choices=("auto", "brute", "sympy"), default="auto")
    ap.add_argument("--class-filter", choices=("all", "split", "nonsplit"), default="nonsplit")
    ap.add_argument("--thresholds", default="6,7,8,9,10")
    ap.add_argument("--top", type=int, default=18)
    ap.add_argument("--quartic", action="store_true")
    ap.add_argument("--verify-random-points", type=int, default=1)
    args = ap.parse_args()

    p = args.p
    if p <= 3 or not sp.isprime(p):
        raise SystemExit("--p must be an odd prime")
    root_method = args.root_method
    if root_method == "auto":
        root_method = "brute" if p <= 200_000 else "sympy"
    thresholds = [int(x) for x in args.thresholds.split(",") if x]
    rng = random.Random(args.seed)

    trace_cache: dict[int, tuple[int, int]] = {}
    label_totals: Counter[str] = Counter()
    label_hits: dict[int, Counter[str]] = {thr: Counter() for thr in thresholds}
    v2_hist: Counter[int] = Counter()
    split_counts: Counter[str] = Counter()
    rows = 0
    v_samples = 0
    x0_points = 0
    j_values = 0
    A_values = 0
    bsgs_attempts = 0
    t0 = time.perf_counter()

    while rows < args.rows:
        v = rng.randrange(0, p)
        v_samples += 1
        rhs = (1 - pow(v, 4, p)) % p
        u_roots = x0.sqrt_mod_roots(rhs, p)
        x0_points += len(u_roots)
        for u in u_roots:
            if u in (0, 1, p - 1):
                continue
            j = x0.j_x0_32(u, p)
            if j is None:
                continue
            j_values += 1
            for A in x0.montgomery_As_from_j(j, p, root_method):
                A_values += 1
                cls = "split" if x0.legendre(A * A - 4, p) == 1 else "nonsplit"
                split_counts[cls] += 1
                if args.class_filter != "all" and cls != args.class_filter:
                    continue
                if A not in trace_cache:
                    trace, attempts = trace_bsgs(A, p, rng, args.verify_random_points)
                    trace_cache[A] = (trace, x0.v2(p + 1 - trace))
                    bsgs_attempts += attempts
                e2 = trace_cache[A][1]
                v2_hist[e2] += 1
                labels = feature_labels(p, v, u, A, pow(2, (p - 1) // 4, p) if args.quartic and p % 4 == 1 else None)
                for label in labels:
                    label_totals[label] += 1
                    for thr in thresholds:
                        if e2 >= thr:
                            label_hits[thr][label] += 1
                rows += 1
                if rows >= args.rows:
                    break
            if rows >= args.rows:
                break

    elapsed = time.perf_counter() - t0
    print("X0(32) sampled BSGS curve-v2 feature scan")
    print(f"p={p}")
    print(f"rows={rows}")
    print(f"seed={args.seed}")
    print(f"root_method={root_method}")
    print(f"class_filter={args.class_filter}")
    print(f"quartic_features={1 if args.quartic else 0}")
    print(f"verify_random_points={args.verify_random_points}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"rows_per_second={rows / elapsed if elapsed else 0.0:.3f}")
    print(f"v_samples={v_samples}")
    print(f"x0_points={x0_points}")
    print(f"j_values={j_values}")
    print(f"A_values={A_values}")
    print(f"unique_A={len(trace_cache)}")
    print(f"mean_bsgs_attempts={bsgs_attempts / len(trace_cache) if trace_cache else 0.0:.3f}")
    print("split_class_counts=" + ",".join(f"{k}:{split_counts[k]}" for k in sorted(split_counts)))
    print("curve_v2_hist=" + ",".join(f"{k}:{v2_hist[k]}" for k in sorted(v2_hist)))
    print()

    total = rows
    for thr in thresholds:
        base_hits = sum(count for e2, count in v2_hist.items() if e2 >= thr)
        base_rate = base_hits / total if total else 0.0
        print(f"threshold_v2>={thr} base_hits={base_hits}/{total} base_rate={base_rate:.6f}")
        ranked: list[tuple[float, str]] = []
        for label, selected in label_totals.items():
            hits = label_hits[thr][label]
            if not selected or not hits:
                continue
            precision = hits / selected
            coverage = selected / total
            capture = hits / base_hits if base_hits else 0.0
            lift = precision / base_rate if base_rate else 0.0
            score = lift * capture
            ranked.append(
                (
                    score,
                    (
                        f"feature={label} selected={selected} hits={hits} "
                        f"coverage={coverage:.4f} capture={capture:.4f} "
                        f"precision={precision:.4f} lift={lift:.3f}"
                    ),
                )
            )
        for _score, line in sorted(ranked, reverse=True)[: args.top]:
            print(line)
        print()


if __name__ == "__main__":
    main()

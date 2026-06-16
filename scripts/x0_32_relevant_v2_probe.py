#!/usr/bin/env python3
"""Correlate X0(32) state depth with the curve/twist group-order v2.

This is a small-prime research helper.  The earlier X0(32) trace scan compared
first-branch depth only to v2(#E).  For x-only states, the point can live on
E or on the quadratic twist, depending on the squareclass of
x^3 + A*x^2 + x.  This probe compares depth to the relevant side:

    v2(#E)       if x^3 + A*x^2 + x is a square;
    v2(#E_twist) if it is a nonsquare.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter

import sympy as sp

import x0_32_small_prime_probe as x0
import x16_trace_residue_calibration as trace_cal


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--samples", type=int, default=80)
    ap.add_argument("--seed", type=int, default=563)
    ap.add_argument("--target-depth", type=int, default=12)
    ap.add_argument("--root-method", choices=("auto", "brute", "sympy"), default="auto")
    args = ap.parse_args()

    if args.p <= 3 or not sp.isprime(args.p):
        raise SystemExit("--p must be an odd prime")

    root_method = args.root_method
    if root_method == "auto":
        root_method = "brute" if args.p <= 200_000 else "sympy"

    rng = random.Random(args.seed)
    p = args.p
    trace_cache: dict[int, tuple[int, int, int]] = {}
    counters: Counter[str] = Counter()
    side_counts: Counter[str] = Counter()
    depth_hist: Counter[int] = Counter()
    relevant_v2_hist: Counter[int] = Counter()
    relevant_v2_depth_hist: Counter[str] = Counter()
    side_relevant_v2_depth_hist: Counter[str] = Counter()
    class_counts: Counter[str] = Counter()
    class_relevant_v2_depth_hist: Counter[str] = Counter()
    class_slack_hist: Counter[str] = Counter()
    excess_hist: Counter[int] = Counter()
    slack_hist: Counter[int] = Counter()
    per_A_max_depth: dict[int, int] = {}
    per_A_relevant_v2_seen: Counter[str] = Counter()

    start = time.perf_counter()
    for _ in range(args.samples):
        counters["v_samples"] += 1
        v = rng.randrange(0, p)
        rhs = (1 - pow(v, 4, p)) % p
        u_roots = x0.sqrt_mod_roots(rhs, p)
        counters["x0_points"] += len(u_roots)
        for u in u_roots:
            if u in (0, 1, p - 1):
                continue
            j = x0.j_x0_32(u, p)
            if j is None:
                continue
            counters["j_values"] += 1
            As = x0.montgomery_As_from_j(j, p, root_method)
            counters["montgomery_A_values"] += len(As)
            for A in As:
                if A not in trace_cache:
                    trace = trace_cal.trace_for_montgomery_A(p, A)
                    curve_v2 = x0.v2(p + 1 - trace)
                    twist_v2 = x0.v2(p + 1 + trace)
                    trace_cache[A] = (trace, curve_v2, twist_v2)
                _trace, curve_v2, twist_v2 = trace_cache[A]
                split_class = "split" if x0.legendre(A * A - 4, p) == 1 else "nonsplit"
                states = x0.lift_from_two_torsion(p, A, levels=4)
                counters["lifted_states"] += len(states)
                for x in states:
                    step = x0.xonly_zero_step(p, A, x, max_steps=8)
                    if step != 5:
                        continue
                    counters["order32_states"] += 1
                    state_rhs = (x * x % p * x + A * x % p * x + x) % p
                    chi = x0.legendre(state_rhs, p)
                    if chi == 1:
                        side = "curve"
                        relevant_v2 = curve_v2
                    elif chi == -1:
                        side = "twist"
                        relevant_v2 = twist_v2
                    else:
                        side = "zero"
                        relevant_v2 = max(curve_v2, twist_v2)
                    depth = x0.first_branch_depth(p, A, x, 5, args.target_depth)
                    side_counts[side] += 1
                    class_counts[split_class] += 1
                    depth_hist[depth] += 1
                    relevant_v2_hist[relevant_v2] += 1
                    relevant_v2_depth_hist[f"rv2={relevant_v2}:depth={depth}"] += 1
                    side_relevant_v2_depth_hist[f"{side}:rv2={relevant_v2}:depth={depth}"] += 1
                    class_relevant_v2_depth_hist[
                        f"{split_class}:rv2={relevant_v2}:depth={depth}"
                    ] += 1
                    per_A_max_depth[A] = max(per_A_max_depth.get(A, 0), depth)
                    per_A_relevant_v2_seen[f"A={A}:rv2={relevant_v2}:side={side}"] += 1
                    if depth > relevant_v2:
                        counters["depth_exceeds_relevant_v2"] += 1
                        excess_hist[depth - relevant_v2] += 1
                        class_slack_hist[f"{split_class}:excess={depth - relevant_v2}"] += 1
                    else:
                        slack_hist[relevant_v2 - depth] += 1
                        class_slack_hist[f"{split_class}:slack={relevant_v2 - depth}"] += 1
                        if relevant_v2 > depth:
                            counters["relevant_v2_above_depth"] += 1
                        else:
                            counters["depth_equals_relevant_v2"] += 1

    elapsed = time.perf_counter() - start
    per_A_depth_hist = Counter(per_A_max_depth.values())

    print("X0(32) relevant curve/twist v2 probe")
    print(f"p={p}")
    print(f"samples={args.samples}")
    print(f"seed={args.seed}")
    print(f"root_method={root_method}")
    print(f"target_depth={args.target_depth}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"unique_A_traces={len(trace_cache)}")
    print()
    for key in [
        "v_samples",
        "x0_points",
        "j_values",
        "montgomery_A_values",
        "lifted_states",
        "order32_states",
        "depth_exceeds_relevant_v2",
        "depth_equals_relevant_v2",
        "relevant_v2_above_depth",
    ]:
        print(f"{key}={counters[key]}")
    print("side_counts=" + ",".join(f"{k}:{side_counts[k]}" for k in sorted(side_counts)))
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print("first_branch_depth_hist=" + ",".join(f"{k}:{depth_hist[k]}" for k in sorted(depth_hist)))
    print("relevant_v2_hist=" + ",".join(f"{k}:{relevant_v2_hist[k]}" for k in sorted(relevant_v2_hist)))
    print(
        "relevant_v2_depth_hist="
        + ",".join(f"{k}:{relevant_v2_depth_hist[k]}" for k in sorted(relevant_v2_depth_hist))
    )
    print(
        "side_relevant_v2_depth_hist="
        + ",".join(
            f"{k}:{side_relevant_v2_depth_hist[k]}" for k in sorted(side_relevant_v2_depth_hist)
        )
    )
    print(
        "class_relevant_v2_depth_hist="
        + ",".join(
            f"{k}:{class_relevant_v2_depth_hist[k]}"
            for k in sorted(class_relevant_v2_depth_hist)
        )
    )
    print("slack_hist=" + ",".join(f"{k}:{slack_hist[k]}" for k in sorted(slack_hist)))
    print("class_slack_hist=" + ",".join(f"{k}:{class_slack_hist[k]}" for k in sorted(class_slack_hist)))
    print("excess_hist=" + ",".join(f"{k}:{excess_hist[k]}" for k in sorted(excess_hist)))
    print("per_A_max_first_depth_hist=" + ",".join(f"{k}:{per_A_depth_hist[k]}" for k in sorted(per_A_depth_hist)))


if __name__ == "__main__":
    main()

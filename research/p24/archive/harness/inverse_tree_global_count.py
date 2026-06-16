#!/usr/bin/env python3
"""Exact small-field inverse-tree global count for DANGER-style x-only hits.

For each nonsingular Montgomery A over a small prime field, build the inverse
tree of the x-only doubling map back from Z=0 and count:

  * how many A have at least one exact-depth hit;
  * how many x0 values are exact-depth hits;
  * how this mass grows with depth.

This tests the tempting "walk backward from infinity" batching idea.  If it
beat trace entropy, the global inverse mass would reveal more than the same
2-adic trace condition seen by forward sampling.
"""

from __future__ import annotations

import argparse
from collections import Counter
from math import isqrt

from inverse_mass_correlation_probe import (
    final_targets,
    inverse_preimages,
    legendre,
    sqrt_mod_prime,
)


def verifier_k(p: int) -> int:
    q = isqrt(p)
    return (q + 1 + isqrt(4 * q)).bit_length()


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def trace_for_montgomery_A(p: int, A: int) -> int:
    count = 1  # infinity
    for x in range(p):
        rhs = (x * x % p * x + A * x % p * x + x) % p
        chi = legendre(rhs, p)
        count += 1 if chi == 0 else 2 if chi == 1 else 0
    return p + 1 - count


def exact_layers(p: int, A: int, max_depth: int) -> list[set[int]]:
    # layer[0] are states that hit infinity after one more doubling.
    layers: list[set[int]] = []
    seen: set[int] = set()
    current = final_targets(p, A)
    for depth in range(max_depth):
        exact = {x for x in current if x not in seen}
        layers.append(exact)
        seen.update(current)
        nxt: set[int] = set()
        for t in current:
            nxt.update(inverse_preimages(p, A, t))
        current = nxt
        if not current:
            for _ in range(depth + 1, max_depth):
                layers.append(set())
            break
    return layers


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=10007)
    ap.add_argument("--max-depth", type=int, default=0)
    args = ap.parse_args()

    p = args.p
    k = verifier_k(p)
    max_depth = args.max_depth or k
    total_A = 0
    by_depth_states = Counter()
    by_depth_A = Counter()
    trace_v2_counter = Counter()
    exact_depth_trace_v2_counter = Counter()
    eligible_by_depth = Counter()
    mass_hist_by_depth: dict[int, Counter[int]] = {d: Counter() for d in range(1, max_depth + 1)}

    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        total_A += 1
        trace = trace_for_montgomery_A(p, A)
        curve_v2 = v2(p + 1 - trace)
        twist_v2 = v2(p + 1 + trace)
        relevant_v2 = max(curve_v2, twist_v2)
        trace_v2_counter[relevant_v2] += 1
        for depth in range(1, max_depth + 1):
            if relevant_v2 >= depth:
                eligible_by_depth[depth] += 1

        layers = exact_layers(p, A, max_depth)
        for i, layer in enumerate(layers, start=1):
            mass = len(layer)
            mass_hist_by_depth[i][mass] += 1
            if mass:
                by_depth_A[i] += 1
                by_depth_states[i] += mass
                exact_depth_trace_v2_counter[(i, relevant_v2)] += 1

    print("inverse-tree global exact count")
    print(f"p={p}")
    print(f"k={k}")
    print(f"max_depth={max_depth}")
    print(f"nonsingular_A={total_A}")
    print("relevant_v2_hist=" + ",".join(f"{k}:{trace_v2_counter[k]}" for k in sorted(trace_v2_counter)))
    print("depth A_with_hits eligible_A_relevant_v2_ge_depth exact_x_states avg_states_per_A_with_hit mass_hist")
    for depth in range(1, max_depth + 1):
        a_hits = by_depth_A[depth]
        states = by_depth_states[depth]
        avg = states / a_hits if a_hits else 0.0
        hist = mass_hist_by_depth[depth]
        hist_s = ",".join(f"{m}:{hist[m]}" for m in sorted(hist) if hist[m])
        print(f"{depth:2d} {a_hits:8d} {eligible_by_depth[depth]:34d} {states:14d} {avg:24.6f} {hist_s}")
    print("depth_relevant_v2_hits=" + ",".join(
        f"d{d}_v{v}:{exact_depth_trace_v2_counter[(d, v)]}"
        for d, v in sorted(exact_depth_trace_v2_counter)
    ))
    print("conclusion=inverse_tree_mass_is_the_same_2adic_trace_condition_not_a_free_batch")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Complexity audit for beta-shifted leading axis minors.

For the coefficient-minor product

    Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a),

the sequence

    a_beta = det(P_0 X^(-beta) V_a)

would be easier to package if it had low recurrence/Fourier complexity.  This
script measures Berlekamp-Massey linear complexity of `a_beta` on small CM
packets and compares it to random full-rank subspaces in the same packet.
"""

from __future__ import annotations

import argparse
import random

from cycle_period_complexity_scan import bm_linear_complexity
from cyclic_superregular_random_baseline import (
    beta_leading_dets,
    first_case,
    monomial_transforms,
    random_full_rank_vectors,
)


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % q)) % q
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=70000)
    parser.add_argument("--max-prime-quotients", type=int, default=10)
    parser.add_argument("--max-composite-quotients", type=int, default=10)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=700000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-axis-dim", type=int, default=12)
    parser.add_argument("--max-factor-degree", type=int, default=20)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--only-D", type=int)
    args = parser.parse_args()

    case = first_case(args)
    if case is None:
        raise SystemExit("no eligible case found")

    q = case.q
    d = case.factor.degree()
    r = len(case.vectors)
    transforms = monomial_transforms(case.factor, case.n, q)
    cm_dets = beta_leading_dets(case.vectors, case.factor, case.n, q, transforms)
    cm_bm = bm_linear_complexity(cm_dets * 2, q)

    rng = random.Random(args.seed)
    random_bm: list[int] = []
    random_distinct: list[int] = []
    random_zero_counts: list[int] = []
    for _ in range(args.random_trials):
        vectors = random_full_rank_vectors(rng, r, d, q)
        dets = beta_leading_dets(vectors, case.factor, case.n, q, transforms)
        random_bm.append(bm_linear_complexity(dets * 2, q))
        random_distinct.append(len(set(dets)))
        random_zero_counts.append(sum(1 for value in dets if value == 0))

    print("axis sliding-window sequence complexity")
    print(f"D={case.D}")
    print(f"q={case.q}")
    print(f"ell={case.ell}")
    print(f"h={case.h}")
    print(f"m={case.m}")
    print(f"n={case.n}")
    print(f"factor_degree={d}")
    print(f"axis_dim={r}")
    print(f"random_trials={args.random_trials}")
    print()
    print("cm_axis")
    print(f"  distinct_values={len(set(cm_dets))}")
    print(f"  zero_count={sum(1 for value in cm_dets if value == 0)}")
    print(f"  bm_complexity={cm_bm}")
    print(f"  bm_over_n={cm_bm / case.n:.6f}")
    print(f"  product={product_mod(cm_dets, q)}")
    print()
    print("random_baseline")
    print(f"  bm_min={min(random_bm) if random_bm else 'NA'}")
    print(f"  bm_max={max(random_bm) if random_bm else 'NA'}")
    print(f"  bm_avg={sum(random_bm) / len(random_bm) if random_bm else 0:.6f}")
    print(f"  full_or_near_full_bm={sum(1 for value in random_bm if value >= case.n - 1)}")
    print(f"  distinct_min={min(random_distinct) if random_distinct else 'NA'}")
    print(f"  distinct_max={max(random_distinct) if random_distinct else 'NA'}")
    print(f"  subspaces_with_zero={sum(1 for value in random_zero_counts if value)}")
    print()
    print("interpretation")
    print("  low_bm_would_support_recurrence_or_resultant_compression=1")
    print("  full_bm_means_sliding_product_keeps_high_order_beta_phase=1")
    print("conclusion=reported_axis_sliding_window_sequence_complexity")


if __name__ == "__main__":
    main()

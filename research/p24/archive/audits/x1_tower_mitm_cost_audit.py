#!/usr/bin/env python3
"""Cost audit for meet-in-the-middle hopes in the X1(2^h) tower.

The cleanest possible strict-DANGER speedup would be:

1. sample curves with a rational x-only point of order 2^h for h around k/2;
2. pay only the residual 2^(k-h) tail to reach order 2^k.

If the level-2^h sampler is obtained by lifting through h nested quadratic
covers by rejection, its cost is 2^h, so the product is still 2^k.  This file
records that accounting and the much stronger requirement a genuine MITM
sampler would have to meet.

It is intentionally a cost-shape audit, not a p24 search.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
K = 40
BASE_LEVEL = 4  # X1(16) is the cheap rational starting point already used.


def log2(n: float) -> float:
    return math.log(n, 2)


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def main() -> None:
    p = P24
    sqrt_p = math.sqrt(p)
    k = verifier_k(p)
    if k != K:
        raise AssertionError(k)

    print("p24 X1 tower MITM cost audit")
    print(f"p={p}")
    print(f"k={k}")
    print(f"sqrt_p={sqrt_p:.6e}")
    print(f"log2_sqrt_p={log2(sqrt_p):.6f}")
    print(f"cheap_base_level=2^{BASE_LEVEL}=16")
    print()

    print("ordinary_tower_rejection_split")
    print("  h lift_cost_from_X1_16 residual_tail product product_over_2^k product_over_sqrt")
    for h in (8, 12, 16, 20, 24, 28, 32, 36, 40):
        lift = 1 << max(0, h - BASE_LEVEL)
        residual = 1 << max(0, k - h)
        product = lift * residual
        print(
            f"  {h:2d} {lift:18d} {residual:15d} {product:15d} "
            f"{product / (1 << (k - BASE_LEVEL)):16.6f} {product / sqrt_p:18.6e}"
        )
    print()

    print("hypothetical_sampler_exponent")
    print("  Assume a level 2^h sampler costs 2^(beta*(h-4)) from X1(16).")
    print("  Work exponent is beta*(h-4)+(k-h); beta<1 is required.")
    print("  beta h total_log2_work work_over_sqrt")
    for beta in (1.0, 0.75, 0.5, 0.25):
        for h in (20, 28, 36, 40):
            total = beta * max(0, h - BASE_LEVEL) + max(0, k - h)
            print(f"  {beta:4.2f} {h:2d} {total:16.6f} {2**total / sqrt_p:14.6e}")
        print()

    print("base_parameter_MITM_set_sizes")
    print("  Splitting h independent quadratic lift conditions over the base")
    print("  parameter line gives subsets of F_p of size about p/2^(h/2).")
    print("  For h<=k this is far larger than both 2^h and sqrt(p).")
    print("  h half_constraints log2_subset_size subset_over_sqrt")
    for h in (20, 28, 36, 40):
        half = h / 2
        log_subset = log2(p) - half
        print(f"  {h:2d} {half:16.1f} {log_subset:16.6f} {2**log_subset / sqrt_p:18.6e}")
    print()

    print("branch_space_MITM_warning")
    print("  Enumerating 2^(h/2) branch words is not by itself a finite meet:")
    print("  after h/2 inverse steps one still has a positive-dimensional")
    print("  family in the starting parameter.  Making it finite requires")
    print("  evaluating over field parameters or adding the missing equations,")
    print("  which returns to the density or high-genus modular-curve cost.")
    print()

    print("obstruction_summary")
    print("  rejection_lift_cost_times_residual_tail_is_independent_of_split=1")
    print("  base_parameter_subset_MITM_is_worse_than_sqrt_for_h_le_k=1")
    print("  useful_MITM_requires_nontrivial_beta_less_than_1_tower_sampler=1")
    print(
        "conclusion=no_X1_tower_MITM_speedup_without_a_new_subdensity_sampler_"
        "for_nested_quadratic_lifts"
    )


if __name__ == "__main__":
    main()

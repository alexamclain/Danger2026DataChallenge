#!/usr/bin/env python3
"""Entropy audit for bounded-degree explicit j-line families.

Suppose a proposed shortcut gives a rational parameter u and a bounded-degree
map j = phi(u) into the elliptic j-line.  This includes the Montgomery A-line,
Legendre lambda, Edwards/Tate/Kubert-style one-parameter forms at fixed level,
and any other fixed-degree algebraic reparametrization of elliptic curves.

For a fixed ordinary target trace, the target j-invariants form a ring-class
set of size about h(D).  Pulling this set back through a degree-d family gives
at most d*h(D) parameter values.  Thus bounded-degree families can improve only
constant factors; an exponent-changing sampler needs the degree/level to grow.

This script records the p24 constants for that argument using the same Euler
product class-size estimates as cm_class_size_audit.py.
"""

from __future__ import annotations

import math

import sympy as sp

from cm_class_size_audit import (
    P24,
    TRACES,
    euler_product_l1,
    fundamental_discriminant_for_negative_squarefree,
    squarefree_part_from_abs_delta,
)


PRIME_BOUND = 200_000


def target_class_estimates() -> list[tuple[int, int, int, float]]:
    rows = []
    for trace in TRACES:
        abs_delta = 4 * P24 - trace * trace
        sf = squarefree_part_from_abs_delta(abs_delta)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        conductor_sq = abs_delta // abs(D_K)
        conductor = math.isqrt(conductor_sq)
        L_est = euler_product_l1(D_K, PRIME_BOUND)
        h_est = math.sqrt(abs(D_K)) * L_est / math.pi
        ring_factor = conductor
        for ell in sp.factorint(conductor):
            ring_factor *= 1.0 - sp.kronecker_symbol(D_K, ell) / ell
        h_order_est = h_est * ring_factor
        rows.append((trace, D_K, conductor, h_order_est))
    return rows


def expected_trials(total_h: float, degree: float) -> float:
    return P24 / (degree * total_h)


def main() -> None:
    rows = target_class_estimates()
    total_h = sum(row[3] for row in rows)
    sqrt_p = math.sqrt(P24)

    print("p24 low-degree explicit-family entropy audit")
    print(f"p={P24}")
    print(f"sqrt_p={sqrt_p:.6e}")
    print(f"euler_product_prime_bound={PRIME_BOUND}")
    print()
    print("target trace class estimates")
    for trace, D_K, conductor, h in rows:
        print(
            f"  trace={trace:15d} D_K={D_K} conductor={conductor} "
            f"h_est={h:.6e} h/sqrt_p={h / sqrt_p:.6f}"
        )
    print(f"  total_signed_j_classes_est={total_h:.6e}")
    print(f"  total_h_over_sqrt_p={total_h / sqrt_p:.6f}")
    print(f"  random_j_expected_trials={expected_trials(total_h, 1.0):.6e}")
    print()

    print("bounded-degree family model")
    print("degree expected_trials expected_trials/sqrt_p")
    for degree in (1, 2, 3, 6, 16, 64, 256, 4096, 65536, 1_000_000):
        trials = expected_trials(total_h, float(degree))
        print(f"{degree:8d} {trials:18.6e} {trials / sqrt_p:22.6e}")
    print()

    print("degree required for target trial exponents")
    print("alpha target_trials=p^alpha required_degree")
    for alpha in (0.49, 0.45, 0.40, 0.35, 0.30, 0.25):
        target = P24 ** alpha
        degree = P24 / (total_h * target)
        print(f"{alpha:5.2f} {target:20.6e} {degree:18.6e}")
    print()
    print(
        "conclusion=bounded_degree_explicit_families_only_change_constants; "
        "exponent_saving_requires_growing_degree_or_new_class_selector"
    )


if __name__ == "__main__":
    main()

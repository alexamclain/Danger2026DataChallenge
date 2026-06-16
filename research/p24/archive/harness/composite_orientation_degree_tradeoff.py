#!/usr/bin/env python3
"""Degree accounting for orienting the composite split ideal.

The best certificate-oriented CM target uses

    a = p2 * p463 * p223^(-1)

with good class index 66254 and recovery degree 3107441.  The unoriented
X0(2*223*463) relation loses this and only gives an index-2 subgroup.

This script records what various orientation models would cost.  It is not a
construction; it is a sanity check for whether "just orient the small factors"
is plausibly still below sqrt(p).
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
FACTORS = (2, 223, 463)
GOOD_QUOTIENT = 66254
GOOD_RECOVERY = 3107441
UNORIENTED_QUOTIENT = 2
UNORIENTED_RECOVERY = 102940198007


def gamma0_index_squarefree(factors: tuple[int, ...]) -> int:
    out = 1
    for ell in factors:
        out *= ell + 1
    return out


def binary_orientation_cover(factors: tuple[int, ...]) -> int:
    # Two choices for each split rational prime.  For ell=2 this is also a
    # binary split-prime choice in the CM class group.
    return 1 << len(factors)


def x1_point_cover_for_odd_factors(factors: tuple[int, ...]) -> int:
    # A pessimistic full point-level orientation cover over X0: choosing a
    # generator of each cyclic kernel modulo sign.
    out = 1
    for ell in factors:
        if ell == 2:
            continue
        out *= (ell - 1) // 2
    return out


def gamma1_index_squarefree(factors: tuple[int, ...]) -> int:
    # [SL2Z:Gamma1(N)] for squarefree N = N^2 prod(1-1/ell^2).
    n = math.prod(factors)
    value = n * n
    for ell in factors:
        value = value * (ell * ell - 1) // (ell * ell)
    return value


def main() -> None:
    x0 = gamma0_index_squarefree(FACTORS)
    binary = binary_orientation_cover(FACTORS)
    x1_cover = x1_point_cover_for_odd_factors(FACTORS)
    gamma1 = gamma1_index_squarefree(FACTORS)

    rows = [
        (
            "oriented_sign_oracle",
            x0 * binary,
            GOOD_QUOTIENT,
            GOOD_RECOVERY,
            "binary sign labels only",
        ),
        (
            "oriented_full_point_cover",
            x0 * x1_cover,
            GOOD_QUOTIENT,
            GOOD_RECOVERY,
            "choose kernel generators modulo sign",
        ),
        (
            "gamma1_squarefree_level",
            gamma1,
            GOOD_QUOTIENT,
            GOOD_RECOVERY,
            "full Gamma1(N) index proxy",
        ),
        (
            "plain_unoriented_x0",
            x0,
            UNORIENTED_QUOTIENT,
            UNORIENTED_RECOVERY,
            "loses balanced class index",
        ),
    ]

    print("p24 composite orientation degree tradeoff")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"factors={FACTORS}")
    print(f"norm={math.prod(FACTORS)}")
    print(f"gamma0_index_squarefree={x0}")
    print(f"binary_orientation_cover={binary}")
    print(f"x1_point_cover_for_odd_factors={x1_cover}")
    print(f"gamma1_index_squarefree={gamma1}")
    print()
    print("model correspondence_degree quotient recovery seeded_proxy seeded_over_sqrt max_degree_over_sqrt note")
    for label, degree, quotient, recovery, note in rows:
        seeded = degree * recovery
        max_degree = max(degree, quotient, recovery)
        print(
            f"{label:28s} {degree:21d} {quotient:8d} {recovery:12d} "
            f"{seeded:18d} {seeded / SQRT_P:16.6e} "
            f"{max_degree / SQRT_P:20.6e} {note}"
        )
    print()
    print("interpretation")
    print("  binary_orientation_cover_would_keep_seeded_proxy_subsqrt=0")
    print("  full_point_or_gamma1_orientation_is_far_above_sqrt=1")
    print("  plain_unoriented_x0_loses_the_good_recovery_degree=1")
    print(
        "conclusion=composite_route_needs_a_cheap_split_prime_sign_selector; "
        "full_X1_orientation_is_too_expensive"
    )


if __name__ == "__main__":
    main()

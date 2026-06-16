#!/usr/bin/env python3
"""Estimate CM class sizes for the p24 target traces.

The target traces have discriminants with no useful square factor.  A possible
escape hatch would be an algorithm that finds one root of the relevant Hilbert
class polynomial without computing the whole polynomial.  This audit estimates
the size of the hidden root set: the class number is already on the order of
sqrt(p), so without a seed in the isogeny class, "find one root" has the same
entropy as random trace search.

The L-values below are rough Euler-product estimates for orientation, not
certified class numbers.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


def v2(n: int) -> int:
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def squarefree_part_from_abs_delta(abs_delta: int) -> int:
    factors = sp.factorint(abs_delta)
    sf = 1
    for prime, exp in factors.items():
        if exp % 2:
            sf *= prime
    return sf


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    # K = Q(sqrt(-sf)), with sf positive squarefree.
    d = -sf
    return d if d % 4 == 1 else 4 * d


def euler_product_l1(D: int, prime_bound: int) -> float:
    product = 1.0
    for ell in list(sp.primerange(2, prime_bound + 1)):
        chi = sp.kronecker_symbol(D, ell)
        if chi:
            product *= 1.0 / (1.0 - chi / ell)
    return product


def main() -> None:
    prime_bound = 200_000
    print("p24 CM class-size audit")
    print(f"p={P24}")
    print(f"sqrt_floor={math.isqrt(P24)}")
    print(f"euler_product_prime_bound={prime_bound}")
    for t in TRACES:
        abs_delta = 4 * P24 - t * t
        sf = squarefree_part_from_abs_delta(abs_delta)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        conductor_sq = abs_delta // abs(D_K)
        conductor = math.isqrt(conductor_sq)
        L_est = euler_product_l1(D_K, prime_bound)
        h_est = math.sqrt(abs(D_K)) * L_est / math.pi
        # Ring class number for conductor f, up to the usual unit index, which
        # is 1 here because D_K < -4.
        ring_factor = conductor
        for ell in sp.factorint(conductor):
            ring_factor *= 1.0 - sp.kronecker_symbol(D_K, ell) / ell
        h_order_est = h_est * ring_factor
        random_curve_rate = h_est / P24

        print()
        print(f"trace={t}")
        print(f"abs_delta={abs_delta}")
        print(f"squarefree_part={sf}")
        print(f"fundamental_D_K={D_K}")
        print(f"conductor_in_Zpi={conductor}")
        print(f"L1_euler_est={L_est:.6f}")
        print(f"h_max_order_est={h_est:.6e}")
        print(f"h_Zpi_order_est={h_order_est:.6e}")
        print(f"random_j_hit_rate_est={random_curve_rate:.6e}")
        print(f"random_j_expected_trials_est={1.0 / random_curve_rate:.6e}")


if __name__ == "__main__":
    main()

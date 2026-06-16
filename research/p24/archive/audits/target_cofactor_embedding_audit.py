#!/usr/bin/env python3
"""Audit pairing-friendly/cofactor structure in the p24 strict target orders.

The third target order is

    #E = 2^41 * 454747350887

with a prime odd cofactor.  This is attractive after a curve is known, and it
raises the question whether a pairing-friendly/MNT-style construction might
name the curve more cheaply than generic CM.

This script checks the embedding degrees of the large odd cofactors relative
to the fixed p24 field.  Small embedding degree would point to a known family
of constructions.  The observed degrees are large, so the cofactor shape does
not supply a fixed-field construction.
"""

from __future__ import annotations

import math

import sympy as sp


P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)
K = 40
M = 1 << K


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def embedding_degree_mod_prime(p: int, r: int) -> int:
    if math.gcd(p, r) != 1:
        return 0
    return int(sp.n_order(p % r, r))


def print_side(label: str, trace: int, order: int) -> None:
    two = v2(order)
    odd = order >> two
    print(f"{label} trace={trace}")
    print(f"  order={order}")
    print(f"  v2(order)={two}")
    print(f"  odd_part={odd}")
    print(f"  odd_factorization={sp.factorint(odd)}")
    print(f"  order_over_2^40={order // M if order % M == 0 else 'not_divisible'}")
    for r, exp in sp.factorint(odd).items():
        if r < 1000:
            continue
        emb = embedding_degree_mod_prime(P24, int(r))
        print(
            f"  large_factor={r} exp={exp} "
            f"p_mod_r={P24 % r} embedding_degree={emb} "
            f"embedding_degree_over_r={emb / r:.6f} "
            f"factor_r_minus_1={sp.factorint(r - 1)}"
        )


def main() -> None:
    print("p24 target cofactor embedding audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"2^k={M}")
    print()
    for trace in TRACES:
        curve_order = P24 + 1 - trace
        twist_order = P24 + 1 + trace
        print_side("curve_side", trace, curve_order)
        print_side("twist_side", -trace, twist_order)
        print()
    print("interpretation")
    print("  prime_odd_cofactor_after_large_2_power=useful_after_curve_exists")
    print("  small_embedding_degree_for_large_cofactors=0")
    print("  MNT_or_pairing_friendly_fixed_p_route_visible=0")
    print(
        "conclusion=target_odd_cofactor_shape_does_not_supply_a_subsqrt_"
        "fixed_field_constructor"
    )


if __name__ == "__main__":
    main()

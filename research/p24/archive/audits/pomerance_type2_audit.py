#!/usr/bin/env python3
"""Audit whether original Pomerance type-2 certificates help for p24.

Pomerance's paper allows a type-2 certificate with two independent points of
orders 2^k1 and 2^k2 on the same curve, with product exceeding the Hasse bound
needed for a prime divisor of n.  This is more general than the DANGER3
single-point verifier.

For a curve over F_p, the Weil pairing forces full rational 2^m torsion to
imply 2^m | p-1.  Thus min(k1, k2) <= v2(p-1).  For p = 10^24 + 7, and in
fact for the whole 10^n+7 family with n >= 1, v2(p-1)=1.  So type-2 can add at
most one independent factor of 2; it does not change the p^(1/2) trace search
exponent.
"""

from __future__ import annotations

from math import isqrt

P24 = 10**24 + 7


def v2(n: int) -> int:
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def main() -> None:
    p = P24
    q = isqrt(p)
    danger_bound = q + 1 + isqrt(4 * q)
    danger_k = danger_bound.bit_length()
    max_second_exponent = v2(p - 1)

    # If k2 is capped by the Weil pairing, the first point must supply the
    # remaining exponent in the product 2^(k1+k2) > danger_bound.
    min_large_exponent = max(0, danger_k - max_second_exponent)

    print("p24 original-Pomerance type-2 audit")
    print(f"p={p}")
    print(f"sqrt_floor={q}")
    print(f"danger_bound={danger_bound}")
    print(f"danger_single_point_k={danger_k}")
    print(f"v2(p-1)={max_second_exponent}")
    print(f"max_independent_second_2power=2^{max_second_exponent}")
    print(f"min_large_point_exponent_with_type2={min_large_exponent}")
    print(f"type2_product_exponent_needed={danger_k}")
    print(f"asymptotic_family_10^n_plus_7_v2_p_minus_1=1")
    print("conclusion=type2_can_only_change_constants_not_the_sqrt_trace_exponent")


if __name__ == "__main__":
    main()

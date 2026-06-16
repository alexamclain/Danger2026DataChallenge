#!/usr/bin/env python3
"""Audit split-prime-over-2 class relations for p24 target CM orders.

For each strict DANGER target trace, the fundamental CM discriminant satisfies
D_K == 1 mod 8, so 2 splits in O_K.  A tempting direct-eigenvalue shortcut
would be a short horizontal 2-isogeny cycle: a small power of one prime ideal
above 2 becoming principal in the class group.

If p2^m is principal, its generator has norm 2^m.  For an imaginary quadratic
order of discriminant D, every non-scalar principal element has norm at least
|D|/4, because

    4*N(alpha) = x^2 + |D|*y^2,  y != 0.

Thus no split-2 ideal relation can occur before 2^m >= |D|/4.  This script
computes that exact lower bound for the p24 target traces and compares the
corresponding relation norm with sqrt(p) and the verifier 2^k.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(n).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def main() -> None:
    sqrt_p = math.isqrt(P24)
    k = verifier_k(P24)
    danger_power = 1 << k
    print("p24 split-prime-over-2 relation audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"k={k}")
    print(f"2^k={danger_power}")
    print()
    for t in TRACES:
        delta_abs = 4 * P24 - t * t
        sf = squarefree_part(delta_abs)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        if D_K % 8 != 1:
            raise AssertionError("2 is not split for this target field")
        min_non_scalar_norm = (abs(D_K) + 3) // 4
        min_power = (min_non_scalar_norm - 1).bit_length()
        relation_norm_floor = 1 << min_power
        print(f"trace={t}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  factor_abs_D_K={sp.factorint(abs(D_K))}")
        print(f"  two_splits=True")
        print(f"  min_non_scalar_principal_norm=ceil(|D_K|/4)={min_non_scalar_norm}")
        print(f"  no_principal_power_of_split_2_before_m={min_power}")
        print(f"  first_possible_power_norm=2^{min_power}={relation_norm_floor}")
        print(f"  first_possible_norm_over_sqrt_p={relation_norm_floor / sqrt_p:.6e}")
        print(f"  first_possible_norm_over_2^k={relation_norm_floor / danger_power:.6e}")
        print()
    print(
        "conclusion=split_2_horizontal_cycle_relation_has_norm_far_above_sqrt_p"
    )


if __name__ == "__main__":
    main()

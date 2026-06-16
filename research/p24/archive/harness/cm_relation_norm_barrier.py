#!/usr/bin/env python3
"""Audit low-degree CM relation/cycle shortcuts for the p24 traces.

One possible escape from the huge class-polynomial degree would be to find a
short relation in the target CM class group and solve a small modular-equation
cycle instead of computing a full Hilbert class polynomial.

For an order of discriminant D < 0, a non-scalar principal relation of norm n
comes from an element (x + y*sqrt(D))/2 with

    4*n = x^2 + |D|*y^2,  y != 0.

Thus every non-scalar endomorphism/relation has n >= |D|/4.  Relations below
that bound are only scalar multiplications, which do not identify the target
CM class.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(n).items():
        if exp & 1:
            out *= prime
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def genus_factor_upper_bound(D: int) -> int:
    """Coarse genus-class count for odd negative fundamental D."""
    omega = len(sp.factorint(abs(D)))
    return 1 << max(0, omega - 1)


def main() -> None:
    sqrt_p = math.isqrt(P24)
    danger_m = 1 << ((sqrt_p + 1 + math.isqrt(4 * sqrt_p)).bit_length())

    print("p24 CM low-degree relation/cycle barrier")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"danger_m={danger_m}")
    print()

    for t in TRACES:
        abs_delta = 4 * P24 - t * t
        sf = squarefree_part(abs_delta)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        min_non_scalar_norm = (abs(D_K) + 3) // 4
        genus_bound = genus_factor_upper_bound(D_K)

        print(f"trace={t}")
        print(f"  abs_delta={abs_delta}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  factor_abs_D_K={sp.factorint(abs(D_K))}")
        print(f"  genus_factor_upper_bound={genus_bound}")
        print(f"  min_non_scalar_principal_norm=ceil(|D_K|/4)={min_non_scalar_norm}")
        print(f"  min_norm_over_sqrt_p={min_non_scalar_norm / sqrt_p:.6e}")
        print(f"  min_norm_over_danger_m={min_non_scalar_norm / danger_m:.6e}")
        print()

    print(
        "conclusion=any_CM_cycle_or_principal_relation_that_selects_the_target_class_"
        "has_degree_far_above_sqrt_p"
    )


if __name__ == "__main__":
    main()

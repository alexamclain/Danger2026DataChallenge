#!/usr/bin/env python3
"""Degree audit for splitting the inverse-doubling tower into two curves.

A tempting improvement over rejection is to split the condition

    [2^k] x = infinity

at a middle x-coordinate.  Let C_a(A, x) be the algebraic curve saying that x
reaches infinity after a doublings.  To extend x backward by b more rational
halvings is another algebraic condition D_b(A, x).  The split certificate
comes from an intersection

    C_a ∩ D_b

in the (A, x)-plane.

The problem is that both degrees grow like 2^a and 2^b.  Their intersection
degree is the product 2^(a+b), so a balanced split moves the work from a
depth-k equation to two depth-k/2 equations whose intersection still has the
full depth-k degree.  This is the algebraic version of the density product
barrier.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
K = 40


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 inverse-tower intersection degree audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"sqrt_floor_p={sqrt_p}")
    print()
    print("split_depths degree_C degree_D bezout_product product_over_sqrt")
    for a in (4, 8, 12, 16, 20, 24, 28, 32, 36):
        b = K - a
        degree_c = 1 << a
        degree_d = 1 << b
        product = degree_c * degree_d
        print(
            f"{a:2d}+{b:2d} {degree_c:14d} {degree_d:14d} "
            f"{product:16d} {product / sqrt_p:18.6f}"
        )
    print()
    print("balanced_split_detail")
    a = K // 2
    degree = 1 << a
    product = degree * degree
    print(f"  C_{a}_degree={degree}")
    print(f"  D_{a}_degree={degree}")
    print(f"  Bezout_product=2^{K}={product}")
    print(f"  2^k_over_sqrt_p={product / sqrt_p:.6f}")
    print()
    print("interpretation")
    print("  branch_word_MITM_has_no_finite_collision_key_before_elimination=1")
    print("  eliminating_the_middle_variable_forms_a_resultant_of_product_degree=1")
    print("  balanced_split_reduces_max_single_degree_but_not_total_intersection_entropy=1")
    print(
        "conclusion=inverse_tower_curve_intersection_does_not_beat_sqrt_"
        "without_extra_structure"
    )


if __name__ == "__main__":
    main()

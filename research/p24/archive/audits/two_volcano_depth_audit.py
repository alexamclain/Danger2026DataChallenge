#!/usr/bin/env python3
"""Audit whether p24 target classes hide a deep 2-isogeny volcano shortcut.

For trace t, the order Z[pi] has discriminant Delta = t^2 - 4p.  The conductor
inside the maximal CM order is the square root of Delta/D_K.  A long 2-volcano
shortcut would require a large 2-power conductor.  The p24 target traces have
only conductor 2, so the 2-volcano above the target trace has depth at most 1.

Thus the large v2(#E) condition is a Frobenius eigenvalue/orientation
condition, not a deep conductor/volcano condition that can be navigated from a
small seed.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


def v2(n: int) -> int:
    return (abs(n) & -abs(n)).bit_length() - 1


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(n).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def main() -> None:
    print("p24 2-isogeny volcano depth audit")
    print(f"p={P24}")
    print()
    for t in TARGET_TRACES:
        delta_abs = 4 * P24 - t * t
        sf = squarefree_part(delta_abs)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        conductor_sq = delta_abs // abs(D_K)
        conductor = math.isqrt(conductor_sq)
        if conductor * conductor != conductor_sq:
            raise AssertionError("bad conductor square")
        order = P24 + 1 - t
        print(f"trace={t}")
        print(f"  v2_group_order={v2(order)}")
        print(f"  abs_delta={delta_abs}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  conductor_Zpi_in_OK={conductor}")
        print(f"  v2_conductor={v2(conductor)}")
        print(f"  max_2_volcano_depth_from_Zpi={v2(conductor)}")
        print()
    print("conclusion=target_2power_depth_is_not_a_deep_2_volcano_conductor_depth")


if __name__ == "__main__":
    main()

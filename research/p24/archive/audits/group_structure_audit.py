#!/usr/bin/env python3
"""Audit p24 target 2-primary group structures.

The DANGER3 verifier needs an x-only point whose underlying curve/twist point
has exact order 2^k.  Divisibility of #E by 2^k is not quite enough in the
split Montgomery case, because full rational 2-torsion makes the 2-Sylow
noncyclic.

For E/F_p, E(F_p) ~= Z/d1 x Z/d2 with d1 | d2 and d1 | p-1.  Since
v2(p-1)=1 for p=10^24+7, the 2-primary part is either cyclic C_{2^v}
(nonsplit Montgomery, one rational 2-torsion point) or C_2 x C_{2^{v-1}}
(split Montgomery, full rational 2-torsion).  This script records which target
traces can actually support exact order 2^40 points on each side.
"""

from __future__ import annotations

from dataclasses import dataclass

P24 = 10**24 + 7
K = 40
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Side:
    label: str
    trace: int
    order: int
    v2_order: int


def v2(n: int) -> int:
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def exponent_v2(order_v2: int, split: bool) -> int:
    if order_v2 == 0:
        return 0
    return order_v2 - 1 if split and order_v2 >= 2 else order_v2


def x_coordinate_count_exact_order(k: int, exponent: int, split: bool) -> int:
    """Number of x-coordinates of exact order 2^k in the abstract 2-Sylow.

    This ignores the odd part, which is irrelevant after projection.
    """
    if exponent < k or k < 2:
        return 0
    if split:
        # C2 x C_{2^e}: exact 2^k elements = 2*phi(2^k) for k>=2.
        points = 1 << k
    else:
        # C_{2^e}: exact 2^k elements = phi(2^k).
        points = 1 << (k - 1)
    return points // 2


def sides() -> list[Side]:
    out: list[Side] = []
    for trace in sorted(set(TARGET_TRACES) | {-t for t in TARGET_TRACES}):
        curve_order = P24 + 1 - trace
        twist_order = P24 + 1 + trace
        out.append(Side("curve", trace, curve_order, v2(curve_order)))
        out.append(Side("twist", trace, twist_order, v2(twist_order)))
    return out


def main() -> None:
    print("p24 target 2-primary group-structure audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"v2(p-1)={v2(P24 - 1)}")
    print("side trace v2_order split exponent_v2 supports_exact_2^k xcoords_exact_2^k")
    for side in sides():
        if side.v2_order < K:
            continue
        for split in (False, True):
            exp = exponent_v2(side.v2_order, split)
            count = x_coordinate_count_exact_order(K, exp, split)
            print(
                f"{side.label:5s} {side.trace:15d} {side.v2_order:8d} "
                f"{int(split):5d} {exp:11d} {int(exp >= K):18d} {count}"
            )
    print("conclusion=prime_odd_part_helps_projection_only_after_target_isogeny_class_is_found")


if __name__ == "__main__":
    main()

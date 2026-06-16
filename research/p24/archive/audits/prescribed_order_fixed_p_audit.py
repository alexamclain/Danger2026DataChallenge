#!/usr/bin/env python3
"""Audit prescribed-order algorithms against the fixed p24 target.

Algorithms such as Bröker-Stevenhagen construct elliptic curves of prescribed
order by finding a suitable prime field and a small CM discriminant.  That can
sound like it should solve the strict DANGER3 target immediately: the target
orders are explicitly known and factored.

For this challenge, however, the field prime p is fixed.  Once p and the order
N are both fixed, the trace t = p + 1 - N and the CM discriminant
Delta = t^2 - 4p are fixed too.  This script records that the three strict
target orders have no large square factor in Delta; the fundamental
discriminants are all of size about p.  Thus exact prescribed-order CM
construction over the fixed p24 field is the same hard target-class problem
already tracked in the frontier.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
K = 40
M = 1 << K
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)
NEAR_SQUARE_TRACE = 2 * 10**12


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(abs(n)).items():
        if exp & 1:
            out *= int(prime)
    return out


def fundamental_discriminant_from_delta(delta: int) -> int:
    if delta >= 0:
        raise ValueError("ordinary target delta should be negative")
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def describe_trace(label: str, trace: int) -> None:
    order = P24 + 1 - trace
    delta = trace * trace - 4 * P24
    D = fundamental_discriminant_from_delta(delta)
    conductor_sq = delta // D
    conductor = math.isqrt(conductor_sq)
    if conductor * conductor != conductor_sq:
        raise AssertionError("non-square conductor quotient")
    print(label)
    print(f"  trace={trace}")
    print(f"  order={order}")
    print(f"  order_over_2^40={order // M if order % M == 0 else 'not_divisible'}")
    print(f"  v2(order)={v2(order)}")
    print(f"  factor(order)={sp.factorint(order)}")
    print(f"  abs_delta={abs(delta)}")
    print(f"  fundamental_D={D}")
    print(f"  conductor_in_Zpi={conductor}")
    print(f"  abs_D_over_p={abs(D) / P24:.6f}")
    print(f"  sqrt_abs_D_over_sqrt_p={math.sqrt(abs(D)) / math.sqrt(P24):.6f}")
    print(f"  delta_square_factor={conductor}")


def main() -> None:
    print("p24 fixed-prime prescribed-order audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"2^k={M}")
    print(f"sqrt_floor={math.isqrt(P24)}")
    print()
    for trace in TARGET_TRACES:
        describe_trace("strict_target", trace)
        print()
    describe_trace("near_square_fast_CM_non_strict", NEAR_SQUARE_TRACE)
    print()
    print(
        "conclusion=fixed_p_prescribed_order_reduces_to_large_discriminant_CM; "
        "variable_field_prescribed_order_algorithms_do_not_select_the_fixed_p24_trace"
    )


if __name__ == "__main__":
    main()

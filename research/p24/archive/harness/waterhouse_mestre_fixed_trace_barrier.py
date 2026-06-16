#!/usr/bin/env python3
"""Waterhouse/Mestre fixed-trace barrier for the strict p24 target.

Existence theorems can make the p24 problem sound easier than it is:
Waterhouse, Rueck, and Voloch describe which group structures occur, and
Mestre-style tricks are useful inside point-counting algorithms.  For the
strict DANGER3 target, however, p is fixed and the verifier forces one of a
few exact ordinary isogeny classes.  By Tate, that is the same as fixing the
trace.  The constructive route in the prescribed-subgroup literature then
returns to CM: compute H_D mod p, find a root, and choose the correct twist.

This audit records the arithmetic obstruction for p = 10^24 + 7.  The three
absolute strict traces have conductor 2 but fundamental discriminant comparable
to p, and the Hilbert class polynomial degrees are already a positive
constant times sqrt(p).  Thus Waterhouse/Rueck/Voloch supply existence, not a
sub-sqrt selector for A or j.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
K = 40
M = 1 << K

# Absolute values of the signed verifier traces.  The x-only verifier accepts
# either the curve side or the quadratic-twist side, so +/- trace have the same
# CM field; the high 2-adic order may live on either p+1-t or p+1+t.
ABS_STRICT_TRACES = (1020608380936, 78903246840, 1178414874616)


@dataclass(frozen=True)
class TraceRow:
    abs_trace: int
    high_side: str
    high_order: int
    high_v2: int
    fundamental_D: int
    conductor: int
    class_number: int
    class_group: tuple[int, ...]


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(abs(n)).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant(delta: int) -> int:
    if delta >= 0:
        raise ValueError("strict ordinary traces have negative delta")
    d = -squarefree_part(delta)
    return d if d % 4 == 1 else 4 * d


def row_for_abs_trace(pari: Pari, abs_trace: int) -> TraceRow:
    minus_order = P24 + 1 - abs_trace
    plus_order = P24 + 1 + abs_trace
    minus_v2 = v2(minus_order)
    plus_v2 = v2(plus_order)
    if minus_v2 >= plus_v2:
        high_side = "p+1-abs(t)"
        high_order = minus_order
        high_v2 = minus_v2
    else:
        high_side = "p+1+abs(t)"
        high_order = plus_order
        high_v2 = plus_v2

    delta = abs_trace * abs_trace - 4 * P24
    D = fundamental_discriminant(delta)
    conductor_sq = delta // D
    conductor = math.isqrt(conductor_sq)
    if conductor * conductor != conductor_sq:
        raise AssertionError("delta/D should be a square")

    class_data = pari.quadclassunit(D)
    h = int(class_data[0])
    group = tuple(int(x) for x in list(class_data[1]))
    return TraceRow(
        abs_trace=abs_trace,
        high_side=high_side,
        high_order=high_order,
        high_v2=high_v2,
        fundamental_D=D,
        conductor=conductor,
        class_number=h,
        class_group=group,
    )


def main() -> None:
    pari = Pari()
    sqrt_floor = math.isqrt(P24)
    print("p24 Waterhouse/Mestre fixed-trace barrier")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_floor}")
    print(f"strict_level=2^{K}={M}")
    print(f"hasse_trace_count_proxy={2 * sqrt_floor + 1}")
    print()

    print("literature_route_checkpoint")
    print("  Tate: fixed trace <=> fixed elliptic isogeny class over F_p")
    print("  Waterhouse/Rueck/Voloch: existence/group-structure criteria")
    print("  constructive step in prescribed-subgroup route: CM H_D root mod p")
    print("  Mestre/Cremona-Sutherland trick: point-counting aid, not fixed-trace selector")
    print()

    for row in (row_for_abs_trace(pari, t) for t in ABS_STRICT_TRACES):
        h_factor = sp.factorint(row.class_number)
        print(f"abs_trace={row.abs_trace}")
        print(f"  accepting_order_side={row.high_side}")
        print(f"  high_order={row.high_order}")
        print(f"  high_order_over_2^40={row.high_order // M}")
        print(f"  high_v2={row.high_v2}")
        print(f"  fundamental_D={row.fundamental_D}")
        print(f"  conductor={row.conductor}")
        print(f"  abs_D_over_p={abs(row.fundamental_D) / P24:.6f}")
        print(f"  class_number_degree_H_D={row.class_number}")
        print(f"  class_number_over_sqrt={row.class_number / sqrt_floor:.6f}")
        print(f"  class_group={list(row.class_group)}")
        print(f"  factor_class_number={dict(h_factor)}")
        print()

    print("barrier")
    print("  existence_without_root=insufficient_for_certificate")
    print("  generic_isogeny_class_representative_enumeration=unknown")
    print("  exact_fixed_trace_construction_cost_proxy=max(h(D), root_selection)")
    print(
        "conclusion=Waterhouse_Rueck_Voloch_and_Mestre_do_not_bypass_"
        "the_large_CM_root_selector_for_strict_p24"
    )


if __name__ == "__main__":
    main()

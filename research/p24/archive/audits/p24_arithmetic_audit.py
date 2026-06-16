#!/usr/bin/env python3
"""Arithmetic audit for the DANGER3 p24 target.

This script records the deterministic facts that govern any Pomerance triple
for p = 10^24 + 7.  It is intentionally lightweight: no random search and no
large class-polynomial computation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sympy import factorint, isprime


P = 10**24 + 7


@dataclass(frozen=True)
class TargetOrder:
    trace: int
    order: int
    v2: int
    odd_part: int
    discriminant_abs: int


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def verifier_depth(p: int) -> tuple[int, int, int, int]:
    q = math.isqrt(p)
    sq = math.isqrt(q)
    bound = q + 1 + 2 * sq
    k = 0
    power = 1
    while power <= bound:
        k += 1
        power <<= 1
    return q, sq, bound, k


def target_orders(p: int) -> list[TargetOrder]:
    q, _sq, _bound, k = verifier_depth(p)
    modulus = 1 << k
    lo = p + 1 - 2 * q
    hi = p + 1 + 2 * q
    first = lo + ((modulus - lo) % modulus)
    out: list[TargetOrder] = []
    for order in range(first, hi + 1, modulus):
        trace = p + 1 - order
        two = v2(order)
        out.append(
            TargetOrder(
                trace=trace,
                order=order,
                v2=two,
                odd_part=order >> two,
                discriminant_abs=4 * p - trace * trace,
            )
        )
    return out


def xonly_target_traces(p: int) -> list[int]:
    """Signed traces for which E or its quadratic twist has 2^k order."""
    out = {row.trace for row in target_orders(p)}
    out.update(-row.trace for row in target_orders(p))
    return sorted(out)


def squarefree_decomposition(n: int) -> tuple[int, int, dict[int, int]]:
    fac = factorint(n)
    square_root = 1
    squarefree = 1
    for prime, exponent in fac.items():
        square_root *= prime ** (exponent // 2)
        if exponent & 1:
            squarefree *= prime
    return square_root, squarefree, fac


def main() -> None:
    q, sq, bound, k = verifier_depth(P)
    print(f"p = {P}")
    print(f"is_prime = {isprime(P)}")
    print(f"p_mod_8 = {P % 8}")
    print(f"p_mod_12 = {P % 12}")
    print(f"sqrt_floor = {q}")
    print(f"sqrt_sqrt_floor = {sq}")
    print(f"verifier_bound = {bound}")
    print(f"k = {k}")
    print(f"2^k = {1 << k}")
    print(f"v2(p+1) = {v2(P + 1)}")
    print(f"factor(p+1) = {factorint(P + 1)}")
    print()

    print("target_orders:")
    for row in target_orders(P):
        square_root, squarefree, fac = squarefree_decomposition(row.discriminant_abs)
        print(f"  trace = {row.trace}")
        print(f"    order = {row.order}")
        print(f"    v2(order) = {row.v2}")
        print(f"    odd_part = {row.odd_part}")
        print(f"    factor(odd_part) = {factorint(row.odd_part)}")
        print(f"    abs_discriminant = {row.discriminant_abs}")
        print(f"    factor(abs_discriminant) = {fac}")
        print(f"    square_part_root = {square_root}")
        print(f"    squarefree_part = {squarefree}")

    print()
    print("xonly_target_traces_allowing_quadratic_twist:")
    modulus = 1 << k
    for trace in xonly_target_traces(P):
        order = P + 1 - trace
        twist_order = P + 1 + trace
        print(f"  trace = {trace}")
        print(f"    trace_mod_2^k = {trace % modulus}")
        print(f"    v2(order) = {v2(order)}")
        print(f"    v2(twist_order) = {v2(twist_order)}")


if __name__ == "__main__":
    main()

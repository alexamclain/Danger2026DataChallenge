#!/usr/bin/env python3
"""Audit mixed odd/2-power divisor routes for p24.

If a construction forces a divisor M of #E(F_p) that is larger than sqrt(p),
then it starts to narrow the Hasse trace lattice.  If M is larger than the
Hasse interval width, it isolates at most one order.  This script asks whether
the p24 target orders contain a "cheap" mixed divisor that beats the pure
2^40 condition.

The conclusion is negative for DANGER3: among divisors above sqrt(p), the
minimum largest-prime-factor choice is always 2^40.  Odd factors can produce
other divisors above sqrt(p), but they introduce large X1/X0 levels and do not
provide a new asymptotic primitive.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sympy import divisors, factorint

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class DivisorChoice:
    divisor: int
    factors: dict[int, int]
    largest_prime: int


def best_by_largest_prime(order: int, threshold: int) -> DivisorChoice | None:
    best: DivisorChoice | None = None
    for d in divisors(order):
        if d <= threshold:
            continue
        fac = factorint(d)
        choice = DivisorChoice(d, fac, max(fac))
        if (
            best is None
            or choice.largest_prime < best.largest_prime
            or (choice.largest_prime == best.largest_prime and choice.divisor < best.divisor)
        ):
            best = choice
    return best


def min_divisor_above(order: int, threshold: int) -> DivisorChoice | None:
    for d in sorted(divisors(order)):
        if d > threshold:
            fac = factorint(d)
            return DivisorChoice(d, fac, max(fac))
    return None


def fmt(choice: DivisorChoice | None) -> str:
    if choice is None:
        return "none"
    return f"{choice.divisor} factors={choice.factors} largest_prime={choice.largest_prime}"


def main() -> None:
    sqrt_p = math.isqrt(P24)
    hasse_width = math.isqrt(4 * P24) + 1
    print("p24 mixed torsion divisor audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"hasse_width_threshold={hasse_width}")
    print()

    for trace in TARGET_TRACES:
        order = P24 + 1 - trace
        print(f"trace={trace}")
        print(f"  order={order}")
        print(f"  factor(order)={factorint(order)}")
        print(f"  min_divisor_gt_sqrt={fmt(min_divisor_above(order, sqrt_p))}")
        print(f"  best_gt_sqrt_by_largest_prime={fmt(best_by_largest_prime(order, sqrt_p))}")
        print(f"  min_divisor_gt_hasse_width={fmt(min_divisor_above(order, hasse_width))}")
        print(f"  best_gt_hasse_width_by_largest_prime={fmt(best_by_largest_prime(order, hasse_width))}")
        print()


if __name__ == "__main__":
    main()

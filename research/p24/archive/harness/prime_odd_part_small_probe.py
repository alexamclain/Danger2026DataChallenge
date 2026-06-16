#!/usr/bin/env python3
"""Small-field probe for target orders with prime odd part.

One p24 target order is 2^41 times a prime.  After a curve in that isogeny
class is found, this is operationally pleasant: projection by the prime odd
part lands in the 2-Sylow.  The question is whether the prime odd part makes
the isogeny class itself easier to construct.

This script exactly enumerates Montgomery A values for small primes, finds
curve/twist sides satisfying the DANGER depth condition, and labels the target
orders whose odd part is prime.  It is a structural calibration, not a p24
search.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter

import sympy as sp


def v2(n: int) -> int:
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def trace_for_montgomery_A(p: int, A: int, legendre: list[int]) -> int:
    total = 0
    for x in range(p):
        rhs = (x * x % p * x + A * x % p * x + x) % p
        total += legendre[rhs]
    return -total


def run_prime(p: int, max_examples: int) -> None:
    if not sp.isprime(p) or p <= 5:
        raise ValueError(f"not an odd prime >5: {p}")
    k = verifier_k(p)
    legendre = [0] * p
    for a in range(1, p):
        legendre[a] = 1 if pow(a, (p - 1) // 2, p) == 1 else -1

    target_traces: set[int] = set()
    for t in range(-math.isqrt(4 * p), math.isqrt(4 * p) + 1):
        if (p + 1 - t) % (1 << k) == 0:
            target_traces.add(t)
        if (p + 1 + t) % (1 << k) == 0:
            target_traces.add(t)

    side_counter: Counter[str] = Counter()
    prime_odd_counter: Counter[str] = Counter()
    split_counter: Counter[str] = Counter()
    examples: list[tuple[int, int, str, int, int, bool, int]] = []
    seen_orders: dict[tuple[str, int], int] = {}

    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        trace = trace_for_montgomery_A(p, A, legendre)
        split = legendre[(A * A - 4) % p] == 1
        for side, order, side_trace in (
            ("curve", p + 1 - trace, trace),
            ("twist", p + 1 + trace, -trace),
        ):
            if v2(order) < k:
                continue
            odd = order >> v2(order)
            odd_prime = sp.isprime(odd)
            side_counter[side] += 1
            split_counter[f"{side}:{'split' if split else 'nonsplit'}"] += 1
            if odd_prime:
                prime_odd_counter[side] += 1
            seen_orders[(side, side_trace)] = order
            if len(examples) < max_examples:
                examples.append((A, side_trace, side, v2(order), odd, odd_prime, int(split)))

    print()
    print(f"p={p}")
    print(f"k={k}")
    print(f"target_signed_traces={sorted(target_traces)}")
    print(f"distinct_target_sides={len(seen_orders)}")
    for key, order in sorted(seen_orders.items()):
        side, trace = key
        odd = order >> v2(order)
        print(
            f"  side={side:5s} trace={trace:6d} order={order:8d} "
            f"v2={v2(order):2d} odd={odd:6d} odd_prime={int(sp.isprime(odd))}"
        )
    print("side_counter=" + ",".join(f"{k}:{side_counter[k]}" for k in sorted(side_counter)))
    print(
        "prime_odd_counter="
        + ",".join(f"{k}:{prime_odd_counter[k]}" for k in sorted(prime_odd_counter))
    )
    print("split_counter=" + ",".join(f"{k}:{split_counter[k]}" for k in sorted(split_counter)))
    print("examples A trace side v2 odd odd_prime split")
    for row in examples:
        print("  " + " ".join(str(x) for x in row))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", type=int, nargs="+", default=[107, 1009, 3037])
    ap.add_argument("--max-examples", type=int, default=10)
    args = ap.parse_args()
    print("small-prime prime-odd target order probe")
    for p in args.primes:
        run_prime(p, args.max_examples)


if __name__ == "__main__":
    main()

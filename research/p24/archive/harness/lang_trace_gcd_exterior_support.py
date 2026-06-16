#!/usr/bin/env python3
"""Exterior-character support bound for right-origin determinant sequences.

The right-origin action on one right Frobenius orbit has character support O.
A generic k x k exterior coordinate can have support in k-fold sums of O, or
in distinct k-subset sums for a pure wedge coordinate.  This script checks
whether the low support seen in small trace-gcd determinant sequences is
forced by representation theory.
"""

from __future__ import annotations

import argparse


def multiplicative_orbit(p: int, modulus: int) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()
    value = 1 % modulus
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = (value * p) % modulus
    return out


def repeated_sum_sizes(orbit: list[int], modulus: int, max_k: int) -> list[int]:
    support = {0}
    sizes: list[int] = []
    for _ in range(max_k):
        support = {(a + b) % modulus for a in support for b in orbit}
        sizes.append(len(support))
    return sizes


def distinct_subset_sum_sizes(orbit: list[int], modulus: int, max_k: int) -> list[int]:
    supports = [{0}] + [set() for _ in range(max_k)]
    for value in orbit:
        for k in range(max_k - 1, -1, -1):
            for old in list(supports[k]):
                supports[k + 1].add((old + value) % modulus)
    return [len(supports[k]) for k in range(1, max_k + 1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=10**24 + 7)
    parser.add_argument("--right", type=int, default=211)
    parser.add_argument("--tail", type=int, default=16)
    args = parser.parse_args()

    orbit = multiplicative_orbit(args.p, args.right)
    repeated = repeated_sum_sizes(orbit, args.right, args.tail)
    distinct = distinct_subset_sum_sizes(orbit, args.right, args.tail)

    print("Lang trace-gcd exterior support")
    print(f"p_mod_right={args.p % args.right}")
    print(f"right={args.right}")
    print(f"orbit_len={len(orbit)}")
    print(f"tail={args.tail}")
    print(f"orbit_prefix={orbit[:20]}")
    for k, (rep_size, distinct_size) in enumerate(zip(repeated, distinct), start=1):
        print(
            f"k={k} repeated_sum_size={rep_size} "
            f"distinct_subset_sum_size={distinct_size}"
        )
    print("interpretation")
    print("  full_support_by_small_k_means_low_complexity_is_not_generic=1")
    print("conclusion=reported_lang_trace_gcd_exterior_support")


if __name__ == "__main__":
    main()

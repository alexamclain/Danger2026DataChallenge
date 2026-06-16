#!/usr/bin/env python3
"""Search low-norm split-prime words lying in the p24 complement subgroup K.

For the balanced complement-trace route, K has order

    m = 66254 = 2*157*211

inside the cyclic class group of order h=m*n with n=3107441.  A specialized
recovery fiber would be much more constructive if K had small split-prime
generators for its factors.  This audit searches split primes and signed
split-prime-power products up to a norm bound for elements of K.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from composite_split_cycle_audit import CLASS_NUMBER, split_prime_logs

N = 3107441
M = 66254
TARGET_ORDERS = (2, 157, 211, 314, 422, 33127, 66254)


@dataclass(frozen=True)
class Hit:
    norm: int
    terms: tuple[int, ...]
    order_in_K: int
    index_in_K: int
    k_log: int
    full_log: int


def k_order_from_log(full_log: int) -> tuple[int, int, int] | None:
    if full_log % N:
        return None
    k_log = (full_log // N) % M
    if k_log == 0:
        return 1, M, k_log
    index = math.gcd(M, k_log)
    return M // index, index, k_log


def audit(norm_bound: int, prime_bound: int, max_hits_per_order: int) -> tuple[int, dict[int, list[Hit]]]:
    rows = split_prime_logs(prime_bound)
    eligible = [row for row in rows if row.ell <= norm_bound]
    hits: dict[int, list[Hit]] = {order: [] for order in TARGET_ORDERS}
    visited = 0

    def maybe_add(norm: int, log_sum: int, terms: list[int]) -> None:
        data = k_order_from_log(log_sum % CLASS_NUMBER)
        if data is None:
            return
        order, index, k_log = data
        if order not in hits or len(hits[order]) >= max_hits_per_order:
            return
        hits[order].append(
            Hit(
                norm=norm,
                terms=tuple(terms),
                order_in_K=order,
                index_in_K=index,
                k_log=k_log,
                full_log=log_sum % CLASS_NUMBER,
            )
        )

    def rec(start: int, norm: int, log_sum: int, terms: list[int]) -> None:
        nonlocal visited
        if terms:
            visited += 1
            maybe_add(norm, log_sum, terms)
        for pos in range(start, len(eligible)):
            row = eligible[pos]
            if norm * row.ell > norm_bound:
                continue
            power = row.ell
            exponent = 1
            while norm * power <= norm_bound:
                for sign in (1, -1):
                    rec(
                        pos + 1,
                        norm * power,
                        (log_sum + sign * exponent * row.log) % CLASS_NUMBER,
                        terms + [sign * (row.ell**exponent)],
                    )
                exponent += 1
                power *= row.ell

    rec(0, 1, 0, [])
    for order in hits:
        hits[order].sort(key=lambda hit: (hit.norm, len(hit.terms), hit.terms))
    return visited, hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--norm-bound", type=int, default=M)
    ap.add_argument("--prime-bound", type=int, default=M)
    ap.add_argument("--max-hits-per-order", type=int, default=8)
    args = ap.parse_args()

    visited, hits = audit(args.norm_bound, args.prime_bound, args.max_hits_per_order)
    print("complement subgroup generator audit")
    print(f"class_number={CLASS_NUMBER}")
    print(f"n={N}")
    print(f"m={M}")
    print(f"norm_bound={args.norm_bound}")
    print(f"prime_bound={args.prime_bound}")
    print(f"visited_products={visited}")
    print()
    for order in TARGET_ORDERS:
        rows = hits[order]
        print(f"target_order={order} hits_recorded={len(rows)}")
        for hit in rows:
            print(
                f"  norm={hit.norm} terms={hit.terms} "
                f"k_log={hit.k_log} index_in_K={hit.index_in_K} "
                f"full_log={hit.full_log}"
            )
    print()
    print("interpretation")
    print("  no_hits_means_balanced_K_has_no_low_norm_split_prime_power_generators_in_window=1")
    print("  specialized_recovery_fiber_still_needs_a_nonlocal_K_orbit_construction=1")
    print("conclusion=reported_complement_subgroup_generator_audit")


if __name__ == "__main__":
    main()

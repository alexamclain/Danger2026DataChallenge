#!/usr/bin/env python3
"""Legal label-2 pullback counts for the p27 conic chain.

This is the finite-field counterpart to the heavy Magma pullback fixture.
Starting from actual label-2 / compactD candidates, count lifts to:

    A = 2 - c^2
    x5 = r0^2
    h^2 = r0^2 + c*r0 + 1
    g^2 = r0^2 - c*r0 + 1
    r1^2 - (h+g)*r1 + 1 = 0

and iterate the conic-chain transition.  This verifies that the conic chain is
attached to the legal source, not just a free-standing tail model.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_conic_chain_source_probe import sqrt_table, transitions
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


def chain_lift_count(a: int, x5: int, p: int, depth: int, roots: list[list[int]]) -> int:
    c_roots = roots[(2 - a) % p]
    r_roots = roots[x5 % p]
    if not c_roots or not r_roots:
        return 0
    active: dict[tuple[int, int], int] = {(c, r): 1 for c in c_roots for r in r_roots}
    for _ in range(depth):
        nxt: defaultdict[tuple[int, int], int] = defaultdict(int)
        for (c, r), mult in active.items():
            for rn in transitions(c, r, p, roots):
                nxt[(c, rn)] += mult
        active = dict(nxt)
        if not active:
            return 0
    return sum(active.values())


def screen_field(p: int, depth: int) -> Counter:
    roots = sqrt_table(p)
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in candidates:
        a = int(cand["A"])
        x5 = int(cand["x5"])
        bits = candidate_bits(cand, p)
        stats["legal_candidates"] += 1
        stats[f"d3_{bits.d3}"] += 1
        if bits.d3 == 1:
            stats[f"d4_after_d3_{bits.d4}"] += 1
        for d in range(1, depth + 1):
            lifts = chain_lift_count(a, x5, p, d, roots)
            if lifts:
                stats[f"depth{d}_candidates_with_lift"] += 1
                stats[f"depth{d}_total_lifts"] += lifts
            if d == 1:
                if (lifts > 0) == (bits.d3 == 1):
                    stats["depth1_matches_d3plus_indicator"] += 1
                else:
                    stats["depth1_mismatch_d3plus_indicator"] += 1
            if d == 2 and bits.d3 == 1:
                if (lifts > 0) == (bits.d4 == 1):
                    stats["depth2_matches_d4plus_indicator_after_d3"] += 1
                else:
                    stats["depth2_mismatch_d4plus_indicator_after_d3"] += 1
    return stats


def print_counter(prefix: str, stats: Counter, depth: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    legal = stats["legal_candidates"]
    if legal:
        for d in range(1, depth + 1):
            print(
                f"  depth{d}_candidate_lift_rate = "
                f"{stats[f'depth{d}_candidates_with_lift'] / legal:.9f}"
            )


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=2)
    args = parser.parse_args()

    print("p27 legal conic pullback count probe")
    print("source = label-2 / compactD candidates")
    print(f"depth = {args.depth}")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", screen_field(p, args.depth), args.depth)
    print("p27_legal_conic_pullback_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

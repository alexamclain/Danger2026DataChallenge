#!/usr/bin/env python3
"""P27 conic-chain source probe.

The quadratic gate recurrence says that after writing A=2-c^2 and x=r^2,
one selected all-plus gate is controlled by:

    h^2 = r^2 + c*r + 1.

Legal halving also needs the conjugate factor:

    g^2 = r^2 - c*r + 1.

If both are present, the next square-root coordinate satisfies:

    r_next + 1/r_next = h + g.

This probe checks the resulting chain as a source object rather than a
one-bit filter.  It measures:

* lift count: number of (c,r0,h0,g0,r1,...) chain points
* projection count: number of starting (c,r0) pairs admitting a chain
* xDBL consistency: whether r_next really doubles back to r^2 for A=2-c^2
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for a in range(1, p):
        table[a] = 1 if pow(a, (p - 1) // 2, p) == 1 else -1
    return table


def sqrt_table(p: int) -> list[list[int]]:
    roots: list[list[int]] = [[] for _ in range(p)]
    for x in range(p):
        roots[x * x % p].append(x)
    return roots


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def xdouble(a: int, x: int, p: int) -> int | None:
    den = 4 * x % p
    den = den * ((x * x + a * x + 1) % p) % p
    if den == 0:
        return None
    num = (x * x - 1) % p
    return num * num % p * inv(den, p) % p


def transitions(c: int, r: int, p: int, roots: list[list[int]]) -> list[int]:
    qp = (r * r + c * r + 1) % p
    qm = (r * r - c * r + 1) % p
    out: list[int] = []
    for h in roots[qp]:
        for g in roots[qm]:
            s = (h + g) % p
            # r_next^2 - s*r_next + 1 = 0.
            disc = (s * s - 4) % p
            for delta in roots[disc]:
                inv2 = (p + 1) // 2
                out.append((s + delta) * inv2 % p)
                if delta:
                    out.append((s - delta) * inv2 % p)
    return out


def chain_counts(p: int, depth: int) -> Counter:
    roots = sqrt_table(p)
    stats: Counter = Counter()
    active: dict[tuple[int, int], int] = {(c, r): 1 for c in range(p) for r in range(p)}
    stats["initial_pairs"] = len(active)
    for step in range(1, depth + 1):
        next_active: defaultdict[tuple[int, int], int] = defaultdict(int)
        starts_with_lift: set[tuple[int, int]] = set()
        transition_total = 0
        xdouble_mismatch = 0
        degenerate_transition = 0
        for (c, r), multiplicity in active.items():
            rs = transitions(c, r, p, roots)
            if rs:
                starts_with_lift.add((c, r))
            a = (2 - c * c) % p
            x_prev = r * r % p
            for rn in rs:
                transition_total += multiplicity
                x_next = rn * rn % p
                xd = xdouble(a, x_next, p)
                if xd is None:
                    degenerate_transition += multiplicity
                elif xd != x_prev:
                    xdouble_mismatch += multiplicity
                next_active[(c, rn)] += multiplicity
        stats[f"step{step}_input_pairs"] = len(active)
        stats[f"step{step}_starts_with_lift"] = len(starts_with_lift)
        stats[f"step{step}_output_pairs"] = len(next_active)
        stats[f"step{step}_transition_lifts"] = transition_total
        stats[f"step{step}_xdouble_mismatch"] = xdouble_mismatch
        stats[f"step{step}_degenerate_transition"] = degenerate_transition
        active = dict(next_active)
    stats[f"depth{depth}_final_pairs"] = len(active)
    stats[f"depth{depth}_final_lift_multiplicity"] = sum(active.values())
    return stats


def print_counter(prefix: str, stats: Counter, p: int, depth: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    q2 = p * p
    for step in range(1, depth + 1):
        starts = stats[f"step{step}_starts_with_lift"]
        outputs = stats[f"step{step}_output_pairs"]
        lifts = stats[f"step{step}_transition_lifts"]
        print(f"  step{step}_starts_per_q2 = {starts / q2:.9f}")
        print(f"  step{step}_outputs_per_q2 = {outputs / q2:.9f}")
        print(f"  step{step}_lifts_per_q2 = {lifts / q2:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="103,263,607")
    parser.add_argument("--depth", type=int, default=4)
    args = parser.parse_args()

    print("p27 conic-chain source probe")
    print("A=2-c^2, x=r^2")
    print("h^2=r^2+c*r+1, g^2=r^2-c*r+1")
    print("r_next^2-(h+g)*r_next+1=0")
    print(f"depth = {args.depth}")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", chain_counts(p, args.depth), p, args.depth)
    print("p27_conic_chain_source_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

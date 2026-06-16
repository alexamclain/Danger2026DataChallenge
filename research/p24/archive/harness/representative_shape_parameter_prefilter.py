#!/usr/bin/env python3
"""Cheap orbit-arithmetic prefilter for p24-shaped representative analogues.

The p24 representative determinant has shape

    left_degree = 156,
    right_orbit_degree = 35,
    right_orbit_count = 6,
    left_degree = 4*right_orbit_degree + 16.

Before running expensive CM/class-polynomial extraction, this script searches
small finite-field parameters with the same delete-one geometry:

    right_orbit_count = 6,
    floor(left_degree / right_degree) = 4,
    left_degree mod right_degree > 0,
    gcd(left_degree, right_degree) = 1.

These are good toy/mining targets for residual norm identities because they
have the same "four full packets plus a tail" shape.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


P24_P = 10**24 + 7
P24_LEFT = 157
P24_RIGHT = 211


@dataclass(frozen=True)
class ShapeHit:
    q: int
    left: int
    left_degree: int
    right: int
    right_degree: int
    right_orbit_count: int
    full_blocks: int
    tail: int
    exact_p24_moduli: bool


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def primes_up_to(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_prime(n)]


def multiplicative_order(a: int, n: int) -> int:
    if math.gcd(a, n) != 1:
        raise ValueError("order requires coprime inputs")
    a %= n
    value = a
    order = 1
    while value != 1:
        value = (value * a) % n
        order += 1
    return order


def find_hits(args: argparse.Namespace) -> list[ShapeHit]:
    qs = primes_up_to(args.max_q)
    moduli = primes_up_to(args.max_modulus)
    hits: list[ShapeHit] = []
    for q in qs:
        if q < args.min_q:
            continue
        for right in moduli:
            if right <= 3 or right == q:
                continue
            if math.gcd(q, right) != 1:
                continue
            right_degree = multiplicative_order(q, right)
            right_orbits = (right - 1) // right_degree
            if right_orbits != args.right_orbit_count:
                continue
            for left in moduli:
                if left <= 3 or left in (q, right):
                    continue
                if math.gcd(q, left) != 1:
                    continue
                left_degree = multiplicative_order(q, left)
                if math.gcd(left_degree, right_degree) != 1:
                    continue
                full_blocks, tail = divmod(left_degree, right_degree)
                if full_blocks != args.full_blocks or tail == 0:
                    continue
                if args.tail and tail != args.tail:
                    continue
                if args.min_left_degree and left_degree < args.min_left_degree:
                    continue
                hits.append(
                    ShapeHit(
                        q=q,
                        left=left,
                        left_degree=left_degree,
                        right=right,
                        right_degree=right_degree,
                        right_orbit_count=right_orbits,
                        full_blocks=full_blocks,
                        tail=tail,
                        exact_p24_moduli=(left == P24_LEFT and right == P24_RIGHT),
                    )
                )
    return hits


def format_hit(hit: ShapeHit) -> str:
    return (
        f"q={hit.q} left={hit.left} L={hit.left_degree} "
        f"right={hit.right} R={hit.right_degree} "
        f"right_orbits={hit.right_orbit_count} "
        f"shape={hit.full_blocks}*R+{hit.tail} "
        f"exact_p24_moduli={int(hit.exact_p24_moduli)}"
    )


def p24_line() -> str:
    left_degree = multiplicative_order(P24_P, P24_LEFT)
    right_degree = multiplicative_order(P24_P, P24_RIGHT)
    full_blocks, tail = divmod(left_degree, right_degree)
    return (
        "p24_shape: "
        f"p_mod_left={P24_P % P24_LEFT} p_mod_right={P24_P % P24_RIGHT} "
        f"L={left_degree} R={right_degree} "
        f"right_orbits={(P24_RIGHT - 1) // right_degree} "
        f"shape={full_blocks}*R+{tail}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-q", type=int, default=2)
    parser.add_argument("--max-q", type=int, default=31)
    parser.add_argument("--max-modulus", type=int, default=400)
    parser.add_argument("--right-orbit-count", type=int, default=6)
    parser.add_argument("--full-blocks", type=int, default=4)
    parser.add_argument("--tail", type=int, default=0)
    parser.add_argument("--min-left-degree", type=int, default=0)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()

    hits = find_hits(args)
    hits.sort(
        key=lambda hit: (
            not hit.exact_p24_moduli,
            hit.q,
            hit.right_degree,
            hit.left_degree,
            hit.left,
            hit.right,
        )
    )
    print("Representative shape parameter prefilter")
    print(p24_line())
    print(
        "target_geometry="
        f"right_orbit_count={args.right_orbit_count} "
        f"full_blocks={args.full_blocks} "
        f"tail={'any_positive' if args.tail == 0 else args.tail}"
    )
    print(f"search=max_q={args.max_q} max_modulus={args.max_modulus}")
    print(f"hits={len(hits)}")
    for hit in hits[: args.limit]:
        print(format_hit(hit))
    print("conclusion=reported_representative_shape_parameter_prefilter")


if __name__ == "__main__":
    main()

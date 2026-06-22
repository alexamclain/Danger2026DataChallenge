#!/usr/bin/env python3
"""Belyi-orbit audit for the p27 B-line quotient.

The B-line quotient has branch values {0, -2, infinity}.  After normalizing
u=-B/2, this is {0, 1, infinity}, whose visible automorphism group is S3.  This
probe asks whether that small orbit group explains the legal B-domain or the
descended d3/d4 bits.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps, parse_ints


@dataclass(frozen=True)
class Transform:
    name: str
    fn: Callable[[int, int], int | None]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def belyi_transforms() -> list[Transform]:
    return [
        Transform("B", lambda b, p: b % p),
        Transform("-B-2", lambda b, p: (-b - 2) % p),
        Transform("4/B", lambda b, p: None if inv(b, p) is None else 4 * inv(b, p) % p),
        Transform("-4/(B+2)", lambda b, p: None if inv(b + 2, p) is None else -4 * inv(b + 2, p) % p),
        Transform("-2B/(B+2)", lambda b, p: None if inv(b + 2, p) is None else -2 * b * inv(b + 2, p) % p),
        Transform("-2(B+2)/B", lambda b, p: None if inv(b, p) is None else -2 * (b + 2) * inv(b, p) % p),
    ]


def target_label(value: int | None) -> str:
    if value == 1:
        return "plus"
    if value == -1:
        return "minus"
    if value == 0:
        return "mixed"
    return "missing"


def transform_stats(
    domain: set[int],
    targets: dict[int, int] | None,
    q: int,
    transforms: list[Transform],
    core: set[int],
    legal: set[int],
) -> Counter:
    stats: Counter = Counter()
    for transform in transforms:
        for value in domain:
            image = transform.fn(value, q)
            if image is None:
                stats[f"{transform.name}_undefined"] += 1
                continue
            image %= q
            if image in core:
                stats[f"{transform.name}_image_core"] += 1
            else:
                stats[f"{transform.name}_image_not_core"] += 1
            if image in legal:
                stats[f"{transform.name}_image_legal"] += 1
            else:
                stats[f"{transform.name}_image_not_legal"] += 1
            if image in domain:
                stats[f"{transform.name}_image_in_domain"] += 1
                if targets is not None:
                    if targets[image] == targets[value]:
                        stats[f"{transform.name}_same_target"] += 1
                    else:
                        stats[f"{transform.name}_opposite_target"] += 1
            else:
                stats[f"{transform.name}_image_out_domain"] += 1
    return stats


def group_orbits(domain: set[int], targets: dict[int, int] | None, q: int, transforms: list[Transform]) -> Counter:
    stats: Counter = Counter()
    unseen = set(domain)
    while unseen:
        start = unseen.pop()
        orbit = {start}
        frontier = [start]
        while frontier:
            value = frontier.pop()
            for transform in transforms:
                image = transform.fn(value, q)
                if image is None:
                    continue
                image %= q
                if image not in domain or image in orbit:
                    continue
                orbit.add(image)
                frontier.append(image)
                unseen.discard(image)
        stats["orbits"] += 1
        stats[f"orbit_size_{len(orbit)}"] += 1
        if targets is not None:
            values = {targets[value] for value in orbit}
            if len(values) == 1:
                stats[f"constant_{target_label(next(iter(values)))}_orbits"] += 1
            else:
                stats["mixed_target_orbits"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int) -> None:
    d3, d4, setup = legal_b_maps(q)
    core = core_b_values(q)
    legal = set(d3)
    transforms = belyi_transforms()

    print(f"q{q}:")
    stats = Counter(setup)
    stats["core_B"] = len(core)
    stats["legal_B"] = len(legal)
    stats["d3_labeled_B"] = len(d3)
    stats["d4_labeled_B"] = len(d4)
    print_counter("  setup_stats", stats)

    legal_bit = {b: (1 if b in legal else -1) for b in core}
    print_counter(
        "  core_legal_transform_stats",
        transform_stats(core, legal_bit, q, transforms, core, legal),
    )
    print_counter("  core_legal_orbit_stats", group_orbits(core, legal_bit, q, transforms))

    print_counter(
        "  legal_d3_transform_stats",
        transform_stats(legal, d3, q, transforms, core, legal),
    )
    print_counter("  legal_d3_orbit_stats", group_orbits(legal, d3, q, transforms))

    d4_domain = set(d4)
    print_counter(
        "  d4_domain_transform_stats",
        transform_stats(d4_domain, d4, q, transforms, core, legal),
    )
    print_counter("  d4_domain_orbit_stats", group_orbits(d4_domain, d4, q, transforms))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 B-line Belyi-orbit probe")
    print("branch set = {0, -2, infinity}")
    print("transforms = B, -B-2, 4/B, -4/(B+2), -2B/(B+2), -2(B+2)/B")
    for q in parse_ints(args.small_primes):
        run_field(q)
    print("p27_b_line_belyi_orbit_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

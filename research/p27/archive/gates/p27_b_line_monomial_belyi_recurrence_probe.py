#!/usr/bin/env python3
"""Monomial Belyi recurrence screen for the p27 B-line selected classes.

The B-line branch set is {0, -2, infinity}.  With u=-B/2 this is
{0, 1, infinity}.  The fixed monomial Belyi maps u -> u^m, conjugated by the
visible S3 branch symmetries, are the other nearest theorem-shaped B-line
self-correspondence after PGL2 and the hidden-X power maps.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_b_line_belyi_orbit_probe import Transform, belyi_transforms
from p27_b_line_branch_support_probe import core_b_values, legal_b_maps, parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre


@dataclass(frozen=True)
class MonomialHit:
    name: str
    polarity: int
    covered: int
    matches: int
    domain_size: int
    core_images: int
    legal_images: int
    undefined: int


def inv2(p: int) -> int:
    return (p + 1) // 2


def monomial_belyi_map(m: int, b: int, p: int) -> int:
    u = (-b * inv2(p)) % p
    return (-2 * pow(u, m, p)) % p


def compose_monomial(left: Transform, m: int, right: Transform, b: int, p: int) -> int | None:
    first = right.fn(b, p)
    if first is None:
        return None
    middle = monomial_belyi_map(m, first, p)
    return left.fn(middle, p)


def score_map(
    source: dict[int, int],
    target: dict[int, int],
    core: set[int],
    legal: set[int],
    q: int,
    name: str,
    fn: Callable[[int, int], int | None],
) -> list[MonomialHit]:
    base: Counter = Counter()
    polarity_matches = Counter()
    for B, target_sign in target.items():
        image = fn(B, q)
        if image is None:
            base["undefined"] += 1
            continue
        image %= q
        if image in core:
            base["core_images"] += 1
        if image in legal:
            base["legal_images"] += 1
        source_sign = source.get(image)
        if source_sign is None:
            continue
        base["covered"] += 1
        for polarity in (1, -1):
            if target_sign == polarity * source_sign:
                polarity_matches[polarity] += 1

    return [
        MonomialHit(
            name=name,
            polarity=polarity,
            covered=base["covered"],
            matches=polarity_matches[polarity],
            domain_size=len(target),
            core_images=base["core_images"],
            legal_images=base["legal_images"],
            undefined=base["undefined"],
        )
        for polarity in (1, -1)
    ]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(prefix: str, hits: list[MonomialHit], keep_best: int) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
        return
    for hit in sorted(
        hits,
        key=lambda item: (
            item.matches == item.covered == item.domain_size,
            item.covered,
            item.matches,
        ),
        reverse=True,
    )[:keep_best]:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"core_images={hit.core_images} legal_images={hit.legal_images} "
            f"undefined={hit.undefined}"
        )


def run_field(q: int, degrees: list[int], keep_best: int) -> None:
    d3, d4, setup = legal_b_maps(q)
    core = core_b_values(q)
    legal = set(d3)
    transforms = belyi_transforms()

    setup_stats = Counter({f"setup_{key}": value for key, value in setup.items()})
    setup_stats["q_mod_16"] = q % 16
    setup_stats["chi_minus_one"] = legendre(-1, q)
    setup_stats["chi_two"] = legendre(2, q)
    setup_stats["core_B"] = len(core)
    setup_stats["legal_B"] = len(legal)
    setup_stats["d3_B_rows"] = len(d3)
    setup_stats["d4_B_rows"] = len(d4)
    print_counter(f"q{q}_setup", setup_stats)

    stats: Counter = Counter()
    forward_hits: list[MonomialHit] = []
    reverse_hits: list[MonomialHit] = []
    for left in transforms:
        for degree in degrees:
            for right in transforms:
                name = f"{left.name} o u^{degree} o {right.name}"
                fn = lambda b, p, ll=left, dd=degree, rr=right: compose_monomial(ll, dd, rr, b, p)
                stats["maps_tested"] += 1
                forward = score_map(d3, d4, core, legal, q, name, fn)
                reverse = score_map(d4, d3, core, legal, q, name, fn)
                forward_hits.extend(forward)
                reverse_hits.extend(reverse)
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in forward):
                    stats["forward_exact"] += 1
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in reverse):
                    stats["reverse_exact"] += 1

    if forward_hits:
        best_forward = max(forward_hits, key=lambda hit: (hit.covered, hit.matches))
        stats["forward_best_covered"] = best_forward.covered
        stats["forward_best_matches"] = best_forward.matches
        stats["forward_best_coverage_x1000000"] = best_forward.covered * 1_000_000 // best_forward.domain_size
        stats["forward_best_match_x1000000"] = best_forward.matches * 1_000_000 // best_forward.domain_size
    if reverse_hits:
        best_reverse = max(reverse_hits, key=lambda hit: (hit.covered, hit.matches))
        stats["reverse_best_covered"] = best_reverse.covered
        stats["reverse_best_matches"] = best_reverse.matches
        stats["reverse_best_coverage_x1000000"] = best_reverse.covered * 1_000_000 // best_reverse.domain_size
        stats["reverse_best_match_x1000000"] = best_reverse.matches * 1_000_000 // best_reverse.domain_size

    print_counter(f"q{q}_monomial_belyi_recurrence_stats", stats)
    print_hits(f"q{q}_forward_d4_eq_d3_monomial_best", forward_hits, keep_best)
    print_hits(f"q{q}_reverse_d3_eq_d4_monomial_best", reverse_hits, keep_best)


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--degrees", default="2,3,4,5,6,7,8,9,10,11,12")
    parser.add_argument("--keep-best", type=int, default=10)
    args = parser.parse_args()

    degrees = parse_degrees(args.degrees)
    print("p27 B-line monomial Belyi recurrence probe")
    print("screen = d4(B) or d3(B) via S3-conjugated u -> u^m, u=-B/2")
    print(f"degrees = {','.join(str(degree) for degree in degrees)}")
    for q in parse_ints(args.small_primes):
        run_field(q, degrees, args.keep_best)
    print("p27_b_line_monomial_belyi_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Chebyshev/Dickson recurrence screen for p27 A-level selected classes.

The A-line branch set is {-2, 2, infinity}.  The canonical higher self-maps
preserving that postcritical set are the Dickson/Chebyshev maps

    D_0(A)=2, D_1(A)=A, D_{m+1}(A)=A*D_m(A)-D_{m-1}(A),

equivalently D_m(A)=2*T_m(A/2).  This probe tests whether successive selected
A-level gate classes are related by these fixed maps, conjugated by the visible
S3 branch symmetries.  It is intentionally not a coefficient fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import target_rows
from p27_a_line_named_transform_probe import Transform, branch_s3_transforms
from p27_label2_alpha_branch_recurrence_probe import legendre


LabelMap = dict[int, int]


@dataclass(frozen=True)
class ChebHit:
    name: str
    polarity: int
    covered: int
    matches: int
    domain_size: int
    undefined: int


def row_label(bit: int) -> int:
    # target_rows convention: 0 = +1, 1 = -1.
    return 1 if bit == 0 else -1


def cheb_dickson(m: int, a: int, p: int) -> int:
    if m == 0:
        return 2 % p
    prev = 2 % p
    cur = a % p
    if m == 1:
        return cur
    for _ in range(1, m):
        prev, cur = cur, (a * cur - prev) % p
    return cur


def compose_cheb(left: Transform, m: int, right: Transform, a: int, p: int) -> int | None:
    first = right.fn(a, p)
    if first is None:
        return None
    middle = cheb_dickson(m, first, p)
    return left.fn(middle, p)


def gate_maps(ax_points: set[tuple[int, int]], p: int, depth: int, min_rows: int) -> tuple[dict[int, LabelMap], Counter]:
    maps: dict[int, LabelMap] = {}
    stats: Counter = Counter()
    stats["base_A"] = len({A for A, _x in ax_points})
    stats["base_ax"] = len(ax_points)
    for gate in range(3, depth + 3):
        rows, row_stats = target_rows(ax_points, p, gate, depth)
        stats[f"d{gate}_rows"] = len(rows)
        stats[f"d{gate}_plus"] = row_stats["plus_A"]
        stats[f"d{gate}_minus"] = row_stats["minus_A"]
        stats[f"d{gate}_mixed"] = row_stats["mixed_A_groups"]
        if len(rows) >= min_rows or gate <= 4:
            maps[gate] = {A % p: row_label(bit) for A, bit in rows}
    return maps, stats


def score_map(
    source: LabelMap,
    target: LabelMap,
    p: int,
    name: str,
    fn: Callable[[int, int], int | None],
) -> list[ChebHit]:
    base: Counter = Counter()
    polarity_matches = Counter()
    for A, target_sign in target.items():
        image = fn(A, p)
        if image is None:
            base["undefined"] += 1
            continue
        image %= p
        source_sign = source.get(image)
        if source_sign is None:
            continue
        base["covered"] += 1
        for polarity in (1, -1):
            if target_sign == polarity * source_sign:
                polarity_matches[polarity] += 1

    return [
        ChebHit(
            name=name,
            polarity=polarity,
            covered=base["covered"],
            matches=polarity_matches[polarity],
            domain_size=len(target),
            undefined=base["undefined"],
        )
        for polarity in (1, -1)
    ]


def score_successive(
    maps: dict[int, LabelMap],
    p: int,
    degrees: list[int],
    keep_best: int,
) -> tuple[Counter, dict[str, list[ChebHit]]]:
    transforms = branch_s3_transforms()
    stats: Counter = Counter()
    best_by_transition: dict[str, list[ChebHit]] = {}

    for gate in sorted(maps):
        if gate - 1 not in maps:
            continue
        source = maps[gate - 1]
        target = maps[gate]
        transition = f"d{gate - 1}_to_d{gate}"
        hits: list[ChebHit] = []
        for left in transforms:
            for degree in degrees:
                for right in transforms:
                    name = f"{left.name} o D{degree} o {right.name}"
                    fn = lambda a, pp, ll=left, dd=degree, rr=right: compose_cheb(ll, dd, rr, a, pp)
                    stats[f"{transition}_maps_tested"] += 1
                    scored = score_map(source, target, p, name, fn)
                    hits.extend(scored)
                    if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in scored):
                        stats[f"{transition}_exact"] += 1

        if hits:
            best = max(hits, key=lambda hit: (hit.covered, hit.matches))
            stats[f"{transition}_best_covered"] = best.covered
            stats[f"{transition}_best_matches"] = best.matches
            stats[f"{transition}_best_coverage_x1000000"] = best.covered * 1_000_000 // best.domain_size
            stats[f"{transition}_best_match_x1000000"] = best.matches * 1_000_000 // best.domain_size
            best_by_transition[transition] = sorted(
                hits,
                key=lambda hit: (
                    hit.matches == hit.covered == hit.domain_size,
                    hit.covered,
                    hit.matches,
                ),
                reverse=True,
            )[:keep_best]

    return stats, best_by_transition


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(prefix: str, hits: list[ChebHit]) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
    for hit in hits:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"undefined={hit.undefined}"
        )


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def run_field(q: int, depth: int, min_rows: int, degrees: list[int], keep_best: int) -> None:
    ax_points, base_stats = collect_field_ax(q)
    maps, gate_stats = gate_maps(ax_points, q, depth, min_rows)

    setup = Counter({f"base_{key}": value for key, value in base_stats.items()})
    setup["q_mod_16"] = q % 16
    setup["chi_minus_one"] = legendre(-1, q)
    setup["chi_two"] = legendre(2, q)
    setup.update({f"gate_{key}": value for key, value in gate_stats.items()})
    print_counter(f"q{q}_setup", setup)
    print(f"q{q}_maps_kept: {','.join('d' + str(gate) for gate in sorted(maps))}")

    stats, best = score_successive(maps, q, degrees, keep_best)
    print_counter(f"q{q}_chebyshev_recurrence_stats", stats)
    for transition in sorted(best):
        print_hits(f"q{q}_{transition}_best", best[transition])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=8)
    parser.add_argument("--degrees", default="2,3,4,5,6,7,8,9,10,11,12")
    parser.add_argument("--keep-best", type=int, default=10)
    args = parser.parse_args()

    degrees = parse_degrees(args.degrees)
    print("p27 A-line Chebyshev recurrence probe")
    print("screen = d_j(A) via S3-conjugated Dickson maps D_m(A)=2*T_m(A/2)")
    print(f"degrees = {','.join(str(degree) for degree in degrees)}")
    print(f"depth = {args.depth}")
    print(f"min_rows = {args.min_rows}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.depth, args.min_rows, degrees, args.keep_best)
    print("p27_a_line_chebyshev_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Affine recurrence screen for the p27 A-line selected Kummer sequence.

The A-prefix descent probes show that selected gates d3..d14 descend to whole
A-fibers.  This probe asks for the cheapest possible recurrence:

    d_{j+1}(A) = polarity * d_j(m*A + b)

on the selected prefix domain before d_{j+1}.  It is a structural map screen,
not a coefficient fit for a single character.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import target_rows


@dataclass(frozen=True)
class RecurrenceHit:
    m: int
    b: int
    polarity: int
    covered: int
    matches: int


def row_map(rows: list[tuple[int, int]]) -> dict[int, int]:
    """Convert target rows to sign map.  Row bit: 0 => +1, 1 => -1."""

    return {A: (1 if bit == 0 else -1) for A, bit in rows}


def transition_name(prev_gate: int, next_gate: int) -> str:
    return f"d{prev_gate}_to_d{next_gate}"


def score_affine(
    q: int,
    prev: dict[int, int],
    nxt: dict[int, int],
    m: int,
    b: int,
    polarity: int,
) -> tuple[int, int]:
    covered = 0
    matches = 0
    for A, target in nxt.items():
        image = (m * A + b) % q
        source = prev.get(image)
        if source is None:
            continue
        covered += 1
        if target == polarity * source:
            matches += 1
    return covered, matches


def find_affine_recurrences(
    q: int,
    prev_rows: list[tuple[int, int]],
    next_rows: list[tuple[int, int]],
    keep_best: int,
) -> tuple[Counter, list[RecurrenceHit], list[RecurrenceHit]]:
    prev = row_map(prev_rows)
    nxt = row_map(next_rows)
    stats: Counter = Counter()
    stats["prev_rows"] = len(prev)
    stats["next_rows"] = len(nxt)
    if not prev or not nxt:
        return stats, [], []

    next_items = sorted(nxt.items())
    first_A, _first_target = next_items[0]
    exact: list[RecurrenceHit] = []
    best: list[RecurrenceHit] = []
    seen: set[tuple[int, int]] = set()

    # Any full-coverage affine map sends the first next-domain A to one of the
    # previous-domain A values.  This avoids a q^2 scan.
    for m in range(1, q):
        m_first = (m * first_A) % q
        for first_image in prev:
            b = (first_image - m_first) % q
            key = (m, b)
            if key in seen:
                continue
            seen.add(key)
            stats["affine_maps_tested"] += 1
            for polarity in (1, -1):
                covered, matches = score_affine(q, prev, nxt, m, b, polarity)
                hit = RecurrenceHit(m=m, b=b, polarity=polarity, covered=covered, matches=matches)
                if covered == len(nxt) and matches == len(nxt):
                    exact.append(hit)
                best.append(hit)

    best.sort(key=lambda hit: (hit.matches, hit.covered), reverse=True)
    stats["exact_affine_recurrences"] = len(exact)
    if best:
        stats["best_covered"] = best[0].covered
        stats["best_matches"] = best[0].matches
        stats["best_match_x1000000"] = (best[0].matches * 1_000_000) // len(nxt)
        stats["best_coverage_x1000000"] = (best[0].covered * 1_000_000) // len(nxt)
    return stats, exact[:keep_best], best[:keep_best]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(prefix: str, hits: list[RecurrenceHit]) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
    for hit in hits:
        print(
            "  "
            f"m={hit.m} b={hit.b} polarity={hit.polarity} "
            f"covered={hit.covered} matches={hit.matches}"
        )


def run_field(q: int, depth: int, min_rows: int, keep_best: int) -> None:
    ax_points, base_stats = collect_field_ax(q)
    print_counter(f"q{q}_base", base_stats)
    rows_by_gate: dict[int, list[tuple[int, int]]] = {}
    stats_by_gate: dict[int, Counter] = {}
    for gate in range(3, depth + 3):
        rows, stats = target_rows(ax_points, q, gate, depth)
        rows_by_gate[gate] = rows
        stats_by_gate[gate] = stats
        print_counter(f"q{q}_d{gate}_target", stats)

    for prev_gate in range(3, depth + 2):
        next_gate = prev_gate + 1
        label = transition_name(prev_gate, next_gate)
        prev_rows = rows_by_gate[prev_gate]
        next_rows = rows_by_gate[next_gate]
        if len(prev_rows) < min_rows or len(next_rows) < min_rows:
            print(f"q{q}_{label}_affine_result: skipped_rows_lt_{min_rows}")
            continue
        stats, exact, best = find_affine_recurrences(q, prev_rows, next_rows, keep_best)
        print_counter(f"q{q}_{label}_affine_stats", stats)
        print_hits(f"q{q}_{label}_exact_affine", exact)
        print_hits(f"q{q}_{label}_best_affine", best)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=20)
    parser.add_argument("--keep-best", type=int, default=5)
    args = parser.parse_args()

    print("p27 A-line affine recurrence probe")
    print("screen = d_{j+1}(A) = +/- d_j(m*A+b) on selected prefix domains")
    print(f"depth = {args.depth}")
    print(f"min_rows = {args.min_rows}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.depth, args.min_rows, args.keep_best)
    print("p27_a_line_affine_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

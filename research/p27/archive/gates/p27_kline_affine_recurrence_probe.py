#!/usr/bin/env python3
"""Affine K-line recurrence screen for p27 d3 -> d4.

The Lattes screen killed the natural maps K -> x([m]Q), but a sourceable
degree-one recurrence could still be an ordinary affine or reciprocal-affine
map on the reduced Kummer line:

    K -> a*K + b
    K -> a/K + b

This probe tests those two exact families over p27-signature guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_k_belyi_involution_probe import collect_rows


@dataclass(frozen=True)
class MapScore:
    family: str
    a: int
    b: int
    polarity: int
    good: int
    covered: int
    total: int


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def insert_best(best: list[MapScore], score: MapScore, limit: int) -> None:
    best.append(score)
    best.sort(
        key=lambda item: (
            item.covered == item.total,
            item.good == item.covered,
            item.covered,
            item.good,
            -item.a,
            -item.b,
        ),
        reverse=True,
    )
    del best[limit:]


def score_family(
    family: str,
    d3_map: dict[int, int],
    d4_map: dict[int, int],
    p: int,
    limit: int,
) -> tuple[Counter, list[MapScore], list[MapScore]]:
    d3_items = list(d3_map.items())
    d4_items = list(d4_map.items())
    if family == "affine":
        domain = [(k, target) for k, target in d4_items]
    elif family == "reciprocal":
        domain = []
        for k, target in d4_items:
            ik = inv(k, p)
            if ik is None:
                continue
            domain.append((ik, target))
    else:
        raise ValueError(f"unknown family {family}")

    stats: Counter = Counter()
    best: list[MapScore] = []
    exact: list[MapScore] = []
    stats["d3_rows"] = len(d3_map)
    stats["d4_rows"] = len(d4_map)
    stats["domain_rows"] = len(domain)

    # For fixed nonzero a, every covered pair determines b = k3 - a*k4.
    # Accumulate coverage/good counts by b in O(q * #d3 * #d4), avoiding q^2
    # maps times #d4 direct scoring.
    for a in range(1, p):
        by_b: dict[int, list[int]] = {}
        for source_k, d4_target in domain:
            ax = a * source_k % p
            for image_k, d3_target in d3_items:
                b = (image_k - ax) % p
                counts = by_b.setdefault(b, [0, 0, 0])
                counts[0] += 1
                if d4_target == d3_target:
                    counts[1] += 1
                else:
                    counts[2] += 1
        for b, (covered, same, opposite) in by_b.items():
            stats["maps_with_nonzero_coverage"] += 1
            if covered == len(d4_map):
                stats["full_coverage_maps"] += 1
            if same >= opposite:
                score = MapScore(family, a, b, 1, same, covered, len(d4_map))
            else:
                score = MapScore(family, a, b, -1, opposite, covered, len(d4_map))
            if score.good == score.covered and score.covered > 0:
                stats["exact_on_covered_maps"] += 1
            if score.covered == score.total and score.good == score.covered:
                stats["full_exact_maps"] += 1
                exact.append(score)
            insert_best(best, score, limit)

    exact.sort(key=lambda item: (item.family, item.a, item.b, item.polarity))
    stats["best_covered"] = best[0].covered if best else 0
    stats["best_good"] = best[0].good if best else 0
    stats["exact_reported"] = min(limit, len(exact))
    return stats, best, exact[:limit]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[MapScore]) -> None:
    print(f"{prefix}:")
    if not scores:
        print("  none")
        return
    for score in scores:
        rate = score.good / score.covered if score.covered else 0.0
        coverage = score.covered / score.total if score.total else 0.0
        expr = "a*K+b" if score.family == "affine" else "a/K+b"
        print(
            f"  family={score.family} map={score.a},{score.b} expr={expr} "
            f"polarity={score.polarity} good={score.good}/{score.covered} "
            f"rate={rate:.9f} coverage={coverage:.9f}"
        )


def run_field(q: int, limit: int) -> None:
    kd3, kd4, _sd3, _sd4, setup_stats = collect_rows(q)
    d3_map = {row.k: row.target for row in kd3}
    d4_map = {row.k: row.target for row in kd4}
    print(f"q={q}:")
    print(f"  q_mod_16 = {q % 16}")
    print_counter("  setup_stats", setup_stats)
    print(f"  d3_k_rows = {len(d3_map)}")
    print(f"  d4_k_rows = {len(d4_map)}")
    print(f"  d3_plus = {sum(1 for value in d3_map.values() if value == 1)}")
    print(f"  d3_minus = {sum(1 for value in d3_map.values() if value == -1)}")
    print(f"  d4_plus = {sum(1 for value in d4_map.values() if value == 1)}")
    print(f"  d4_minus = {sum(1 for value in d4_map.values() if value == -1)}")
    for family in ["affine", "reciprocal"]:
        stats, best, exact = score_family(family, d3_map, d4_map, q, limit)
        print_counter(f"  q{q}_{family}_stats", stats)
        print_scores(f"  q{q}_{family}_best", best)
        print_scores(f"  q{q}_{family}_full_exact", exact)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2039,2087")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    print("p27 K-line affine recurrence probe")
    print("test = d4(K) ?= +/- d3(a*K+b) or +/- d3(a/K+b)")
    print(f"small_primes = {args.small_primes}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.limit)
    print("p27_kline_affine_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

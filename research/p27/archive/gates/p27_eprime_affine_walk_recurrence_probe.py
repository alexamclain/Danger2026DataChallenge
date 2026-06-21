#!/usr/bin/env python3
"""Small-field affine-walk recurrence screen on the 2-isogenous quotient E'.

The d3 and d4 tower bits descend from the residual E to

    E': V^2 = U^3 + 4U.

The earlier affine-walk recurrence screen ran on the original E.  This probe
tests the sharper quotient directly:

    d4(P) ?= +/- d3([m]P + Q)

for small multipliers m and every Q in E'(F_q), over non-degenerate guard
fields.  A positive exact recurrence would be a real sqrt-beating candidate;
a negative screen is a structured falsifier, not another coefficient fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from p27_label2_alpha_branch_recurrence_probe import inv
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod
from p27_reverse_source_d4_recurrence_probe import QuotientRow, quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


Point = Optional[tuple[int, int]]


@dataclass(frozen=True)
class TransformScore:
    good: int
    covered: int
    total: int
    polarity: int
    multiplier: int
    translate: Point


def eprime_points(p: int) -> list[Point]:
    out: list[Point] = [None]
    for u in range(p):
        rhs = (u * u % p * u + 4 * u) % p
        for v in roots_mod(rhs, p):
            out.append((u, v))
    return out


def eprime_add(left: Point, right: Point, p: int) -> Point:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if left == right:
        if y1 % p == 0:
            return None
        slope = (3 * x1 * x1 + 4) * inv(2 * y1, p) % p
    else:
        slope = (y2 - y1) * inv(x2 - x1, p) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def eprime_neg(point: Point, p: int) -> Point:
    if point is None:
        return None
    x, y = point
    return x, (-y) % p


def eprime_mul(point: Point, n: int, p: int) -> Point:
    if point is None or n == 0:
        return None
    if n < 0:
        return eprime_neg(eprime_mul(point, -n, p), p)
    acc: Point = None
    base = point
    while n:
        if n & 1:
            acc = eprime_add(acc, base, p)
        base = eprime_add(base, base, p)
        n >>= 1
    return acc


def format_point(point: Point) -> str:
    if point is None:
        return "O"
    return f"({point[0]},{point[1]})"


def score_transform(
    d3_map: dict[tuple[int, int], int],
    d4_rows: list[QuotientRow],
    p: int,
    multiplier: int,
    translate: Point,
) -> TransformScore:
    covered = 0
    good_plus = 0
    good_minus = 0
    for row in d4_rows:
        image = eprime_add(eprime_mul((row.x, row.w), multiplier, p), translate, p)
        if image is None or image not in d3_map:
            continue
        covered += 1
        target = d3_map[image]
        if row.target == target:
            good_plus += 1
        if row.target == -target:
            good_minus += 1
    if good_plus >= good_minus:
        return TransformScore(good_plus, covered, len(d4_rows), 1, multiplier, translate)
    return TransformScore(good_minus, covered, len(d4_rows), -1, multiplier, translate)


def sort_key(score: TransformScore) -> tuple[int, int, int, int]:
    full_exact = int(score.covered == score.total and score.good == score.covered)
    high_coverage_exact = int(score.good == score.covered)
    return (full_exact, high_coverage_exact, score.good, score.covered, -abs(score.multiplier))


def coverage_sort_key(score: TransformScore) -> tuple[int, int, int, int]:
    return (score.covered, score.good, int(score.good == score.covered), -abs(score.multiplier))


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def screen_field(
    p: int,
    multipliers: list[int],
    min_coverage: float,
    limit: int,
) -> None:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    d3_rows, d4_rows, source_stats = quotient_bit_rows_from_candidates(candidates, p)
    qd3, d3_stats = quotient_rows(d3_rows, p)
    qd4, d4_stats = quotient_rows(d4_rows, p)
    d3_map = {(row.x, row.w): row.target for row in qd3}
    points = eprime_points(p)

    print(f"q={p}:")
    print(f"  Eprime_points = {len(points)}")
    print_counter("  enum_stats", Counter({f"enum_{key}": value for key, value in enum_stats.items()}))
    print_counter("  original_quotient_stats", source_stats)
    print_counter("  eprime_d3_stats", d3_stats)
    print_counter("  eprime_d4_stats", d4_stats)

    stats: Counter = Counter()
    best: list[TransformScore] = []
    min_covered = int(min_coverage * len(qd4) + 0.999999)
    for multiplier in multipliers:
        for translate in points:
            stats["transforms_tested"] += 1
            score = score_transform(d3_map, qd4, p, multiplier, translate)
            if score.covered >= min_covered:
                stats["transforms_meeting_min_coverage"] += 1
            if score.covered == score.total:
                stats["full_coverage_transforms"] += 1
                if score.good == score.covered:
                    stats["full_coverage_exact_transforms"] += 1
            if score.good == score.covered and score.covered >= min_covered:
                stats["high_coverage_exact_transforms"] += 1
            best.append(score)

    best.sort(key=sort_key, reverse=True)
    top = best[:limit]
    coverage_top = sorted(best, key=coverage_sort_key, reverse=True)[:limit]
    full_coverage = [score for score in best if score.covered == score.total]
    full_coverage.sort(key=lambda score: (score.good, -abs(score.multiplier)), reverse=True)
    stats["d3_rows"] = len(qd3)
    stats["d4_rows"] = len(qd4)
    stats["multipliers_tested"] = len(multipliers)
    stats["translations_tested"] = len(points)
    stats["min_covered"] = min_covered
    stats["best_good"] = top[0].good if top else 0
    stats["best_covered"] = top[0].covered if top else 0
    stats["best_total"] = top[0].total if top else 0
    stats["best_full_coverage_good"] = full_coverage[0].good if full_coverage else 0
    stats["best_min_coverage_good"] = coverage_top[0].good if coverage_top else 0
    stats["best_min_coverage_covered"] = coverage_top[0].covered if coverage_top else 0
    print_counter("  recurrence_stats", stats)

    print(f"q{p}_best_exact_overlap_eprime_affine_walks:")
    for score in top:
        rate = score.good / score.covered if score.covered else 0.0
        coverage = score.covered / score.total if score.total else 0.0
        print(
            f"  m={score.multiplier} Q={format_point(score.translate)} "
            f"polarity={score.polarity} good={score.good}/{score.covered} "
            f"rate={rate:.9f} coverage={coverage:.9f}"
        )
    print(f"q{p}_best_coverage_eprime_affine_walks:")
    for score in coverage_top:
        rate = score.good / score.covered if score.covered else 0.0
        coverage = score.covered / score.total if score.total else 0.0
        print(
            f"  m={score.multiplier} Q={format_point(score.translate)} "
            f"polarity={score.polarity} good={score.good}/{score.covered} "
            f"rate={rate:.9f} coverage={coverage:.9f}"
        )
    if full_coverage:
        print(f"q{p}_full_coverage_eprime_affine_walks:")
        for score in full_coverage[:limit]:
            rate = score.good / score.covered if score.covered else 0.0
            print(
                f"  m={score.multiplier} Q={format_point(score.translate)} "
                f"polarity={score.polarity} good={score.good}/{score.covered} "
                f"rate={rate:.9f}"
            )


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607")
    parser.add_argument("--multipliers", default="1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8")
    parser.add_argument("--min-coverage", type=float, default=0.75)
    parser.add_argument("--limit", type=int, default=16)
    args = parser.parse_args()

    print("p27 E-prime affine-walk recurrence probe")
    print("Eprime = V^2 = U^3 + 4U")
    print(f"small_primes = {args.small_primes}")
    print(f"multipliers = {args.multipliers}")
    print(f"min_coverage = {args.min_coverage}")
    for p in parse_ints(args.small_primes):
        screen_field(p, parse_ints(args.multipliers), args.min_coverage, args.limit)
    print("p27_eprime_affine_walk_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Small-field elliptic-walk recurrence screen for p27 d4 versus d3.

The d3 and d4 bits both descend to the residual elliptic quotient
E: W^2 = X^3-X.  A sqrt-beating recurrence would be much stronger than a
one-off source: if d4(P) were d3(phi(P)) for a fixed low-complexity elliptic
walk phi, the tower would have reusable structure.

Earlier probes only checked identity, negation, rational 2-torsion additions,
and doubling variants.  This probe broadens that test over small fields:

    phi(P) = [m]P + Q

for small multipliers m and every Q in E(F_q).  It is an exact finite-field
screen for translation / affine endomorphism recurrences on the sampled
quotient domain.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    e_add,
    e_neg,
    quotient_bit_rows_from_candidates,
)


Point = Optional[tuple[int, int]]


@dataclass(frozen=True)
class TransformScore:
    good: int
    covered: int
    total: int
    polarity: int
    multiplier: int
    translate: Point


def e_points(p: int) -> list[Point]:
    out: list[Point] = [None]
    for x in range(p):
        rhs = (x * x * x - x) % p
        for w in roots_mod(rhs, p):
            out.append((x, w))
    return out


def e_mul(point: Point, n: int, p: int) -> Point:
    if point is None or n == 0:
        return None
    if n < 0:
        return e_neg(e_mul(point, -n, p), p)
    acc: Point = None
    base = point
    while n:
        if n & 1:
            acc = e_add(acc, base, p)
        base = e_add(base, base, p)
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
        image = e_add(e_mul((row.x, row.w), multiplier, p), translate, p)
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
    return (full_exact, score.good, score.covered, -abs(score.multiplier))


def screen_field(
    p: int,
    multipliers: list[int],
    min_coverage: float,
    limit: int,
) -> None:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, p)
    d3_map = {(row.x, row.w): row.target for row in d3_rows}
    points = e_points(p)

    print(f"q={p}:")
    print(f"  E_points = {len(points)}")
    for key in sorted(enum_stats):
        print(f"  enum_{key} = {enum_stats[key]}")
    for key in sorted(qstats):
        print(f"  quotient_{key} = {qstats[key]}")

    stats: Counter = Counter()
    best: list[TransformScore] = []
    min_covered = int(min_coverage * len(d4_rows) + 0.999999)
    for multiplier in multipliers:
        for translate in points:
            stats["transforms_tested"] += 1
            score = score_transform(d3_map, d4_rows, p, multiplier, translate)
            if score.covered >= min_covered:
                stats["transforms_meeting_min_coverage"] += 1
            if score.covered == score.total:
                stats["full_coverage_transforms"] += 1
                if score.good == score.covered:
                    stats["full_coverage_exact_transforms"] += 1
            best.append(score)

    best.sort(key=sort_key, reverse=True)
    top = best[:limit]
    stats["d3_rows"] = len(d3_rows)
    stats["d4_rows"] = len(d4_rows)
    stats["multipliers_tested"] = len(multipliers)
    stats["translations_tested"] = len(points)
    stats["best_good"] = top[0].good if top else 0
    stats["best_covered"] = top[0].covered if top else 0
    stats["best_total"] = top[0].total if top else 0
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    print(f"q{p}_best_affine_walks:")
    for score in top:
        rate = score.good / score.covered if score.covered else 0.0
        coverage = score.covered / score.total if score.total else 0.0
        print(
            f"  m={score.multiplier} Q={format_point(score.translate)} "
            f"polarity={score.polarity} good={score.good}/{score.covered} "
            f"rate={rate:.9f} coverage={coverage:.9f}"
        )


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1087,1471,1607")
    parser.add_argument("--multipliers", default="1,-1,2,-2,3,-3,4,-4")
    parser.add_argument("--min-coverage", type=float, default=0.75)
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    primes = parse_ints(args.small_primes)
    multipliers = parse_ints(args.multipliers)
    print("p27 E-quotient affine-walk recurrence probe")
    print(f"small_primes = {args.small_primes}")
    print(f"multipliers = {args.multipliers}")
    print(f"min_coverage = {args.min_coverage}")
    for p in primes:
        screen_field(p, multipliers, args.min_coverage, args.limit)
    print("p27_equotient_translation_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

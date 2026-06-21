#!/usr/bin/env python3
"""K-line Lattes recurrence screen for p27 d3 -> d4.

The E' affine-walk screen killed high-coverage recurrences on the elliptic
quotient itself.  Since d3 and d4 descend farther to

    K = x([2]P) on E': V^2 = U^3 + 4U,

this probe tests the induced Kummer-line maps directly:

    K -> x([m]Q),  Q=(K,V) on E',
    K -> x([m]Q + (0,0)) = 4 / x([m]Q).

An exact high-coverage law d4(K)=+/-d3(phi(K)) would be a real recurrence
candidate for beating repeated sqrt half-loss.  Failure says the next gate is
not reusing the same K-line character under a small Lattes map.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from p27_eprime_affine_walk_recurrence_probe import Point, eprime_add, eprime_mul
from p27_k_belyi_involution_probe import collect_rows
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import roots_mod


T0_LABEL = "T0=(0,0)"


@dataclass(frozen=True)
class KMapScore:
    good: int
    covered: int
    total: int
    polarity: int
    multiplier: int
    torsion: str
    undefined: int
    image_missing: int


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def k_point(k: int, p: int) -> Point:
    rhs = k * ((k * k + 4) % p) % p
    roots = roots_mod(rhs, p)
    if not roots:
        return None
    return k % p, roots[0]


def k_lattes(k: int, p: int, multiplier: int, torsion: str) -> int | None:
    point = k_point(k, p)
    if point is None:
        return None
    image = eprime_mul(point, multiplier, p)
    if torsion == T0_LABEL:
        image = eprime_add(image, (0, 0), p)
    if image is None:
        return None
    return image[0] % p


def score_map(
    d3_map: dict[int, int],
    d4_map: dict[int, int],
    p: int,
    multiplier: int,
    torsion: str,
) -> KMapScore:
    good_plus = 0
    good_minus = 0
    covered = 0
    undefined = 0
    missing = 0
    for k, d4 in d4_map.items():
        image = k_lattes(k, p, multiplier, torsion)
        if image is None:
            undefined += 1
            continue
        if image not in d3_map:
            missing += 1
            continue
        covered += 1
        d3 = d3_map[image]
        if d4 == d3:
            good_plus += 1
        if d4 == -d3:
            good_minus += 1
    if good_plus >= good_minus:
        return KMapScore(good_plus, covered, len(d4_map), 1, multiplier, torsion, undefined, missing)
    return KMapScore(good_minus, covered, len(d4_map), -1, multiplier, torsion, undefined, missing)


def sort_key(score: KMapScore) -> tuple[int, int, int, int, int]:
    exact = int(score.covered == score.total and score.good == score.covered)
    high_exact = int(score.good == score.covered)
    return (exact, score.covered, high_exact, score.good, -abs(score.multiplier))


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def screen_field(q: int, multipliers: list[int], limit: int) -> None:
    kd3, kd4, _sd3, _sd4, setup_stats = collect_rows(q)
    d3_map = {row.k: row.target for row in kd3}
    d4_map = {row.k: row.target for row in kd4}
    stats: Counter = Counter()
    stats.update({f"setup_{key}": value for key, value in setup_stats.items()})
    stats["d3_k_rows"] = len(kd3)
    stats["d4_k_rows"] = len(kd4)
    stats["d3_k_plus"] = sum(1 for row in kd3 if row.target == 1)
    stats["d3_k_minus"] = sum(1 for row in kd3 if row.target == -1)
    stats["d4_k_plus"] = sum(1 for row in kd4 if row.target == 1)
    stats["d4_k_minus"] = sum(1 for row in kd4 if row.target == -1)
    stats["d3_k_non_eprime_x"] = sum(
        1 for row in kd3 if legendre(row.k * ((row.k * row.k + 4) % q), q) != 1
    )
    scores: list[KMapScore] = []
    for multiplier in multipliers:
        for torsion in ["O", T0_LABEL]:
            score = score_map(d3_map, d4_map, q, multiplier, torsion)
            scores.append(score)
            stats["maps_tested"] += 1
            if score.covered == score.total:
                stats["full_coverage_maps"] += 1
                if score.good == score.covered:
                    stats["full_coverage_exact_maps"] += 1
            if score.good == score.covered and score.covered > 0:
                stats["exact_on_covered_maps"] += 1
            stats[f"coverage_{score.covered}"] += 1

    scores.sort(key=sort_key, reverse=True)
    print(f"q={q}:")
    print(f"  q_mod_8 = {q % 8}")
    print(f"  chi_minus_one = {legendre(-1, q)}")
    print_counter("  k_lattes_stats", stats)
    print(f"q{q}_best_k_lattes_maps:")
    for score in scores[:limit]:
        rate = score.good / score.covered if score.covered else 0.0
        coverage = score.covered / score.total if score.total else 0.0
        print(
            f"  m={score.multiplier} torsion={score.torsion} polarity={score.polarity} "
            f"good={score.good}/{score.covered} rate={rate:.9f} "
            f"coverage={coverage:.9f} undefined={score.undefined} missing={score.image_missing}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--multipliers", default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16")
    parser.add_argument("--limit", type=int, default=16)
    args = parser.parse_args()

    print("p27 K-line Lattes recurrence probe")
    print("Eprime = V^2 = U^3 + 4U")
    print("test = d4(K) ?= +/- d3(x([m]Q)) or +/- d3(x([m]Q+T0))")
    print(f"small_primes = {args.small_primes}")
    print(f"multipliers = {args.multipliers}")
    for q in parse_ints(args.small_primes):
        screen_field(q, parse_ints(args.multipliers), args.limit)
    print("p27_k_lattes_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

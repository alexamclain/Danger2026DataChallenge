#!/usr/bin/env python3
"""P27 rational [8]-kernel invariance probe for quotient d3/d4.

Small non-degenerate fields showed an unexpected pattern: the descended d3 bit
is often constant on classes with the same [8]P, and d4 sometimes is too.  A
random p27 sample will almost never collide under [8], so this probe forces
collisions by adding the rational kernel of [8] on E(F_p).

For p27, #E(F_p)=p+1=8*odd.  Multiplying random E-points by the odd part
(p+1)/8 generates the rational 2-primary subgroup killed by [8].  We then test
whether P and P+K have the same quotient d3/d4 bits whenever both points lie
in the compactD label-2 domain.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from typing import Optional

from p27_label2_alpha_branch_recurrence_probe import P, compact_class, sample_rows, sqrt_mod
from p27_reverse_doubling_source_probe import label2_oriented_candidates_from_xwt, roots_mod
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    e_add,
    quotient_bit_rows_from_candidates,
)
from p27_equotient_translation_recurrence_probe import e_mul


Point = Optional[tuple[int, int]]


def e_random_points(seed: int) -> tuple[random.Random, int]:
    return random.Random(seed), (P + 1) // 8


def random_e_point(rng: random.Random) -> tuple[int, int]:
    while True:
        x = rng.randrange(0, P)
        w = sqrt_mod((x * x * x - x) % P, P)
        if w is None:
            continue
        if w and rng.randrange(2):
            w = (-w) % P
        return x, w


def kernel8(seed: int, max_draws: int) -> tuple[list[Point], Counter]:
    rng, odd_part = e_random_points(seed)
    points: set[Point] = {None}
    stats: Counter = Counter()
    while len(points) < 8 and stats["random_points"] < max_draws:
        stats["random_points"] += 1
        point = random_e_point(rng)
        ker = e_mul(point, odd_part, P)
        if e_mul(ker, 8, P) is not None:
            stats["not_killed_by_8"] += 1
            continue
        points.add(ker)
    stats["kernel_points"] = len(points)
    stats["odd_part"] = odd_part
    return sorted(points, key=lambda pt: (-1, -1) if pt is None else pt), stats


def candidates_for_e_point(point: tuple[int, int]) -> list[dict[str, int]]:
    x, w = point
    t2 = x * (x * x + 1) % P
    t2 = t2 * ((x * x + 2 * x - 1) % P) % P
    out: list[dict[str, int]] = []
    for t in roots_mod(t2, P):
        if compact_class(x, w, t, P) != -1:
            continue
        for cand in label2_oriented_candidates_from_xwt(x, w, t, P):
            cand = dict(cand)
            cand["X"] = x
            cand["W"] = w
            cand["T"] = t
            out.append(cand)
    return out


def bits_for_e_point(point: tuple[int, int]) -> tuple[QuotientRow | None, QuotientRow | None, Counter]:
    candidates = candidates_for_e_point(point)
    d3_rows, d4_rows, stats = quotient_bit_rows_from_candidates(candidates, P)
    if len(d3_rows) > 1:
        stats["multiple_d3_rows"] += len(d3_rows)
    if len(d4_rows) > 1:
        stats["multiple_d4_rows"] += len(d4_rows)
    return (d3_rows[0] if d3_rows else None), (d4_rows[0] if d4_rows else None), stats


def p27_seed_rows(target: int, seed: int, max_draws: int) -> list[tuple[QuotientRow, QuotientRow | None]]:
    rows, _ = sample_rows(target, seed, max_draws)
    out: list[tuple[QuotientRow, QuotientRow | None]] = []
    for row in rows:
        d3, d4, _ = bits_for_e_point((int(row["X"]), int(row["W"])))
        if d3 is not None:
            out.append((d3, d4))
    return out


def format_point(point: Point) -> str:
    if point is None:
        return "O"
    return f"({point[0]},{point[1]})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=200000)
    parser.add_argument("--kernel-seed", type=int, default=20260621)
    parser.add_argument("--kernel-max-draws", type=int, default=2000)
    args = parser.parse_args()

    print("p27 E-quotient [8]-kernel invariance probe")
    print(f"p = {P}")
    print(f"target = {args.target}")
    print(f"seed = {args.seed}")

    kernel, kstats = kernel8(args.kernel_seed, args.kernel_max_draws)
    print("kernel8_stats:")
    for key in sorted(kstats):
        print(f"  {key} = {kstats[key]}")
    print("kernel8_points:")
    for point in kernel:
        print(f"  {format_point(point)}")
    if len(kernel) != 8:
        print("p27_equotient_kernel8_invariance_probe_rows=0/1")
        return 1

    base_rows = p27_seed_rows(args.target, args.seed, args.max_draws)
    stats: Counter = Counter()
    mixed_d3_orbits = 0
    mixed_d4_orbits = 0
    for d3_base, d4_base in base_rows:
        d3_values: list[int] = []
        d4_values: list[int] = []
        orbit_domain = 0
        for idx, ker in enumerate(kernel):
            point = e_add((d3_base.x, d3_base.w), ker, P)
            if point is None:
                stats["orbit_hit_infinity"] += 1
                continue
            d3, d4, bit_stats = bits_for_e_point(point)
            for key, value in bit_stats.items():
                stats[f"bit_{key}"] += value
            if d3 is None:
                stats[f"kernel_{idx}_not_in_d3_domain"] += 1
                stats["translated_not_in_d3_domain"] += 1
                continue
            orbit_domain += 1
            stats[f"kernel_{idx}_in_d3_domain"] += 1
            stats["translated_in_d3_domain"] += 1
            d3_values.append(d3.target)
            if d4_base is not None and d4 is not None:
                stats[f"kernel_{idx}_in_d4_domain"] += 1
                stats["translated_in_d4_domain"] += 1
                d4_values.append(d4.target)
            elif d4_base is not None:
                stats[f"kernel_{idx}_not_in_d4_domain"] += 1
                stats["translated_not_in_d4_domain"] += 1
        stats[f"d3_orbit_domain_size_{orbit_domain}"] += 1
        if d3_values and len(set(d3_values)) > 1:
            mixed_d3_orbits += 1
        if d4_values and len(set(d4_values)) > 1:
            mixed_d4_orbits += 1

    stats["base_rows"] = len(base_rows)
    stats["base_d4_rows"] = sum(1 for _, d4 in base_rows if d4 is not None)
    stats["mixed_d3_orbits"] = mixed_d3_orbits
    stats["mixed_d4_orbits"] = mixed_d4_orbits
    print("kernel8_invariance_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("p27_equotient_kernel8_invariance_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

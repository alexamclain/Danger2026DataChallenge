#!/usr/bin/env python3
"""Small-field group-projection screen on the p27 2-isogenous quotient E'.

The previous group-projection screen on E found the rational (0,0) orbit and
led to the quotient

    E': V^2 = U^3 + 4U.

This probe asks the next source-shaped question: after passing to E', are the
d3/d4 bits constant on any further small group projection of E'(F_q)?  A
positive result would suggest a coset sampler or low-cost quotient source.  A
negative result kills the most direct group-quotient route after the isogeny.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Optional

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import QuotientRow, quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


Point = Optional[tuple[int, int]]


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def divisors(n: int) -> list[int]:
    out: list[int] = []
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def eprime_add(p1: Point, p2: Point, p: int) -> Point:
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if p1 == p2:
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
    out: Point = None
    base = point
    k = n
    while k:
        if k & 1:
            out = eprime_add(out, base, p)
        base = eprime_add(base, base, p)
        k >>= 1
    return out


def canonical_signed(point: Point, p: int) -> Point:
    if point is None:
        return None
    neg = eprime_neg(point, p)
    assert neg is not None
    return min(point, neg)


def projection_key(row: QuotientRow, p: int, modulus: int, signed: bool) -> Point:
    projected = eprime_mul((row.x, row.w), (p + 1) // modulus, p)
    if signed:
        return canonical_signed(projected, p)
    return projected


def multiplier_key(row: QuotientRow, p: int, multiplier: int, signed: bool) -> Point:
    projected = eprime_mul((row.x, row.w), multiplier, p)
    if signed:
        return canonical_signed(projected, p)
    return projected


def score_projection(rows: list[QuotientRow], p: int, modulus: int, signed: bool) -> Counter:
    by_class: defaultdict[Point, list[int]] = defaultdict(list)
    for row in rows:
        by_class[projection_key(row, p, modulus, signed)].append(row.target)
    stats = score_classes(by_class)
    stats["rows"] = len(rows)
    stats["modulus"] = modulus
    return stats


def score_multiplier(rows: list[QuotientRow], p: int, multiplier: int, signed: bool) -> Counter:
    by_class: defaultdict[Point, list[int]] = defaultdict(list)
    for row in rows:
        by_class[multiplier_key(row, p, multiplier, signed)].append(row.target)
    stats = score_classes(by_class)
    stats["rows"] = len(rows)
    stats["multiplier"] = multiplier
    return stats


def score_classes(by_class: dict[Point, list[int]]) -> Counter:
    stats: Counter = Counter()
    stats["classes"] = len(by_class)
    stats["singleton_classes"] = sum(1 for vals in by_class.values() if len(vals) == 1)
    stats["non_singleton_classes"] = stats["classes"] - stats["singleton_classes"]
    stats["max_class_size"] = max((len(vals) for vals in by_class.values()), default=0)

    good = 0
    mixed_classes = 0
    collision_pairs = 0
    disagree_pairs = 0
    for vals in by_class.values():
        plus = sum(1 for v in vals if v == 1)
        minus = sum(1 for v in vals if v == -1)
        good += max(plus, minus)
        if plus and minus:
            mixed_classes += 1
        n = len(vals)
        collision_pairs += n * (n - 1) // 2
        disagree_pairs += plus * minus
    stats["majority_good"] = good
    stats["mixed_classes"] = mixed_classes
    stats["collision_pairs"] = collision_pairs
    stats["disagree_pairs"] = disagree_pairs
    stats["exact_constant_on_classes"] = int(mixed_classes == 0)
    stats["collision_disagree_num"] = disagree_pairs
    stats["collision_disagree_den"] = collision_pairs
    return stats


def print_score(prefix: str, stats: Counter) -> None:
    rows = stats["rows"]
    maj = stats["majority_good"] / rows if rows else 0.0
    disagree = (
        stats["collision_disagree_num"] / stats["collision_disagree_den"]
        if stats["collision_disagree_den"]
        else 0.0
    )
    print(
        f"  {prefix} m={stats['modulus']} classes={stats['classes']} "
        f"non_singleton={stats['non_singleton_classes']} max_class={stats['max_class_size']} "
        f"mixed={stats['mixed_classes']} exact={stats['exact_constant_on_classes']} "
        f"majority={stats['majority_good']}/{rows} rate={maj:.9f} "
        f"collision_disagree={disagree:.9f}"
    )


def print_multiplier_score(prefix: str, stats: Counter) -> None:
    rows = stats["rows"]
    maj = stats["majority_good"] / rows if rows else 0.0
    disagree = (
        stats["collision_disagree_num"] / stats["collision_disagree_den"]
        if stats["collision_disagree_den"]
        else 0.0
    )
    print(
        f"  {prefix} mul={stats['multiplier']} classes={stats['classes']} "
        f"non_singleton={stats['non_singleton_classes']} max_class={stats['max_class_size']} "
        f"mixed={stats['mixed_classes']} exact={stats['exact_constant_on_classes']} "
        f"majority={stats['majority_good']}/{rows} rate={maj:.9f} "
        f"collision_disagree={disagree:.9f}"
    )


def run_family(label: str, rows: list[QuotientRow], p: int, moduli: list[int], top: int) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    print(f"  plus = {sum(1 for row in rows if row.target == 1)}")
    print(f"  minus = {sum(1 for row in rows if row.target == -1)}")
    scored: list[tuple[int, int, int, int, int, int, str, Counter]] = []
    exact: list[tuple[str, Counter]] = []
    for modulus in moduli:
        if modulus <= 0 or (p + 1) % modulus:
            continue
        for signed in (False, True):
            stats = score_projection(rows, p, modulus, signed)
            label2 = "signed" if signed else "unsigned"
            if stats["exact_constant_on_classes"] and stats["non_singleton_classes"]:
                exact.append((label2, stats))
            scored.append(
                (
                    stats["majority_good"],
                    stats["non_singleton_classes"],
                    stats["max_class_size"],
                    -stats["mixed_classes"],
                    -stats["classes"],
                    1 if signed else 0,
                    label2,
                    stats,
                )
            )
    scored.sort(key=lambda item: item[:7], reverse=True)
    print(f"{label}_exact_nontrivial_projection_classes:")
    if exact:
        for label2, stats in exact[:top]:
            print_score(label2, stats)
    else:
        print("  none")
    print(f"{label}_best_projection_scores:")
    for *_prefix, label2, stats in scored[:top]:
        print_score(label2, stats)


def run_multiplier_family(label: str, rows: list[QuotientRow], p: int, multipliers: list[int], top: int) -> None:
    print(f"{label}_fixed_multiplier_projection:")
    scored: list[tuple[int, int, int, int, int, int, str, Counter]] = []
    exact: list[tuple[str, Counter]] = []
    for multiplier in multipliers:
        if multiplier <= 0:
            continue
        for signed in (False, True):
            stats = score_multiplier(rows, p, multiplier, signed)
            label2 = "signed" if signed else "unsigned"
            if stats["exact_constant_on_classes"] and stats["non_singleton_classes"]:
                exact.append((label2, stats))
            scored.append(
                (
                    stats["majority_good"],
                    stats["non_singleton_classes"],
                    stats["max_class_size"],
                    -stats["mixed_classes"],
                    -stats["classes"],
                    1 if signed else 0,
                    label2,
                    stats,
                )
            )
    scored.sort(key=lambda item: item[:7], reverse=True)
    print(f"{label}_exact_fixed_multiplier_classes:")
    if exact:
        for label2, stats in exact[:top]:
            print_multiplier_score(label2, stats)
    else:
        print("  none")
    print(f"{label}_best_fixed_multiplier_scores:")
    for *_prefix, label2, stats in scored[:top]:
        print_multiplier_score(label2, stats)


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def default_moduli(p: int, max_modulus: int) -> list[int]:
    return [d for d in divisors(p + 1) if d <= max_modulus]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--max-modulus", type=int, default=512)
    parser.add_argument("--moduli", default="")
    parser.add_argument("--multipliers", default="2,4,8,16")
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 E-prime group-projection probe")
    print("curve = V^2 = U^3 + 4U")
    print(f"small_primes = {args.small_primes}")
    print(f"max_modulus = {args.max_modulus}")
    explicit_moduli = parse_ints(args.moduli) if args.moduli.strip() else None
    multipliers = parse_ints(args.multipliers)

    for p in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(p)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, p)
        qd3, d3_iso_stats = quotient_rows(d3_rows, p)
        qd4, d4_iso_stats = quotient_rows(d4_rows, p)
        moduli = explicit_moduli or default_moduli(p, args.max_modulus)
        print(f"q={p}:")
        print(f"  group_order_expected = {p + 1}")
        print(f"  moduli = {','.join(str(m) for m in moduli)}")
        for key in sorted(enum_stats):
            print(f"  enum_{key} = {enum_stats[key]}")
        for key in sorted(qstats):
            print(f"  quotient_{key} = {qstats[key]}")
        for key in sorted(d3_iso_stats):
            print(f"  d3_eprime_{key} = {d3_iso_stats[key]}")
        for key in sorted(d4_iso_stats):
            print(f"  d4_eprime_{key} = {d4_iso_stats[key]}")
        run_family(f"q{p}_eprime_d3", qd3, p, moduli, args.top)
        run_multiplier_family(f"q{p}_eprime_d3", qd3, p, multipliers, args.top)
        run_family(f"q{p}_eprime_d4", qd4, p, moduli, args.top)
        run_multiplier_family(f"q{p}_eprime_d4", qd4, p, multipliers, args.top)

    print("p27_eprime_group_projection_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

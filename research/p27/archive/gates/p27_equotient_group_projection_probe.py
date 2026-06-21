#!/usr/bin/env python3
"""Small-field group-quotient screen for p27 quotient d3/d4 bits.

The residual quotient is E: W^2=X^3-X.  Over q == 3 mod 4 this curve is
supersingular with #E(F_q)=q+1, so a tempting sqrt-beating source would be:

    the next bit is a function of a small group projection of P in E(F_q).

This probe tests that possibility exactly on non-degenerate small fields.  For
each divisor m of #E(F_q), it projects P to [(q+1)/m]P in E[m] and asks whether
d3 or d4 is constant on projection classes.  It also tests signed classes
modulo P ~ -P.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Optional

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    e_add,
    e_neg,
    quotient_bit_rows_from_candidates,
)
from p27_equotient_translation_recurrence_probe import e_mul


Point = Optional[tuple[int, int]]


def divisors(n: int) -> list[int]:
    out = []
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def canonical_signed(point: Point, p: int) -> Point:
    if point is None:
        return None
    neg = e_neg(point, p)
    assert neg is not None
    return min(point, neg)


def projection_key(row: QuotientRow, p: int, modulus: int, signed: bool) -> Point:
    projected = e_mul((row.x, row.w), (p + 1) // modulus, p)
    if signed:
        return canonical_signed(projected, p)
    return projected


def score_projection(rows: list[QuotientRow], p: int, modulus: int, signed: bool) -> Counter:
    by_class: defaultdict[Point, list[int]] = defaultdict(list)
    for row in rows:
        by_class[projection_key(row, p, modulus, signed)].append(row.target)

    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["modulus"] = modulus
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
    return stats


def print_score(prefix: str, stats: Counter) -> None:
    rows = stats["rows"]
    maj = stats["majority_good"] / rows if rows else 0.0
    disagree = stats["disagree_pairs"] / stats["collision_pairs"] if stats["collision_pairs"] else 0.0
    print(
        f"  {prefix} m={stats['modulus']} classes={stats['classes']} "
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
    scored: list[tuple[int, int, int, int, str, Counter]] = []
    exact: list[tuple[str, Counter]] = []
    for modulus in moduli:
        if modulus <= 0 or (p + 1) % modulus:
            continue
        for signed in [False, True]:
            stats = score_projection(rows, p, modulus, signed)
            label2 = "signed" if signed else "unsigned"
            if stats["exact_constant_on_classes"]:
                exact.append((label2, stats))
            scored.append(
                (
                    stats["majority_good"],
                    -stats["classes"],
                    -stats["mixed_classes"],
                    stats["non_singleton_classes"],
                    stats["modulus"],
                    1 if signed else 0,
                    label2,
                    stats,
                )
            )
    scored.sort(reverse=True)
    print(f"{label}_exact_projection_classes:")
    if exact:
        for label2, stats in exact[:top]:
            print_score(label2, stats)
    else:
        print("  none")
    print(f"{label}_best_projection_scores:")
    for _, _, _, _, _, _, label2, stats in scored[:top]:
        print_score(label2, stats)


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def default_moduli(p: int, max_modulus: int) -> list[int]:
    return [d for d in divisors(p + 1) if d <= max_modulus]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1087,1471,1607")
    parser.add_argument("--max-modulus", type=int, default=256)
    parser.add_argument("--moduli", default="")
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 E-quotient group-projection probe")
    print(f"small_primes = {args.small_primes}")
    print(f"max_modulus = {args.max_modulus}")
    explicit_moduli = parse_ints(args.moduli) if args.moduli.strip() else None

    for p in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(p)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, p)
        moduli = explicit_moduli or default_moduli(p, args.max_modulus)
        print(f"q={p}:")
        print(f"  group_order_expected = {p + 1}")
        print(f"  moduli = {','.join(str(m) for m in moduli)}")
        for key in sorted(enum_stats):
            print(f"  enum_{key} = {enum_stats[key]}")
        for key in sorted(qstats):
            print(f"  quotient_{key} = {qstats[key]}")
        run_family(f"q{p}_d3", d3_rows, p, moduli, args.top)
        run_family(f"q{p}_d4", d4_rows, p, moduli, args.top)

    print("p27_equotient_group_projection_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

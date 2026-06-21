#!/usr/bin/env python3
"""Exhaustive small-field line-product screen on the p27 E quotient.

The random low-pole pilot is only a bounded sample.  This probe makes one
nearby falsifier exact on small fields: if the descended d3/d4 character is a
product of two projective-line characters on E: W^2=X^3-X, then it should show
up as an XOR of two line signatures.

This does not test irreducible conics or arbitrary Riemann-Roch sections.  It
is specifically a sharp screen for reducible conic / two-line divisor sources.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    quotient_bit_rows_from_candidates,
)
from p27_reverse_source_quotient_probe import legendre_table, projective_lines


@dataclass(frozen=True)
class LineSig:
    mask: int
    line: tuple[int, int, int]


def target_mask(rows: list[QuotientRow]) -> int:
    out = 0
    for i, row in enumerate(rows):
        if row.target == -1:
            out |= 1 << i
    return out


def line_signature(
    rows: list[QuotientRow],
    p: int,
    line: tuple[int, int, int],
    table: list[int],
) -> int | None:
    a, b, c = line
    mask = 0
    for i, row in enumerate(rows):
        chi = table[(a + b * row.x + c * row.w) % p]
        if chi == 0:
            return None
        if chi == -1:
            mask |= 1 << i
    return mask


def bit_count(n: int) -> int:
    return bin(n).count("1")


def score_mask(mask: int, target: int, full: int) -> tuple[int, int]:
    mismatches = bit_count(mask ^ target)
    good_plus = bit_count(full) - mismatches
    good_minus = mismatches
    if good_plus >= good_minus:
        return good_plus, 1
    return good_minus, -1


def build_line_signatures(rows: list[QuotientRow], p: int) -> tuple[Counter, dict[int, tuple[int, int, int]], Counter, list[tuple[int, int, int, tuple[int, int, int]]]]:
    table = legendre_table(p)
    counts: Counter = Counter()
    first: dict[int, tuple[int, int, int]] = {}
    stats: Counter = Counter()
    best: list[tuple[int, int, int, tuple[int, int, int]]] = []
    target = target_mask(rows)
    full = (1 << len(rows)) - 1

    for line in projective_lines(p):
        stats["projective_lines_tested"] += 1
        mask = line_signature(rows, p, line, table)
        if mask is None:
            stats["zero_lines"] += 1
            continue
        stats["zero_free_lines"] += 1
        counts[mask] += 1
        first.setdefault(mask, line)
        good, polarity = score_mask(mask, target, full)
        best.append((good, -bit_count(mask ^ target), polarity, line))

    best.sort(reverse=True)
    stats["distinct_signatures"] = len(counts)
    if best:
        stats["best_one_line_good"] = best[0][0]
        stats["best_one_line_polarity"] = best[0][2]
    else:
        stats["best_one_line_good"] = 0
        stats["best_one_line_polarity"] = 0
    return counts, first, stats, best[:8]


def pair_count_for_xor(counts: Counter, desired: int) -> int:
    total = 0
    for mask, count in counts.items():
        other = mask ^ desired
        other_count = counts.get(other, 0)
        if not other_count:
            continue
        if mask < other:
            total += count * other_count
        elif mask == other:
            # Allow the same projective line twice.  This only matters for
            # desired=0 and is harmless for nonconstant target masks.
            total += count * (count + 1) // 2
    return total


def sample_pairs(
    first: dict[int, tuple[int, int, int]],
    desired: int,
    limit: int,
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    out = []
    for mask, line in first.items():
        other = mask ^ desired
        if other not in first:
            continue
        out.append((line, first[other]))
        if len(out) >= limit:
            break
    return out


def run_family(label: str, rows: list[QuotientRow], p: int, pair_limit: int) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    print(f"  plus = {sum(1 for row in rows if row.target == 1)}")
    print(f"  minus = {sum(1 for row in rows if row.target == -1)}")
    if not rows:
        print("  skipped_empty_rows = 1")
        return

    counts, first, stats, best = build_line_signatures(rows, p)
    target = target_mask(rows)
    full = (1 << len(rows)) - 1
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    plus_pairs = pair_count_for_xor(counts, target)
    minus_pairs = pair_count_for_xor(counts, target ^ full)
    print(f"  exact_two_line_pairs_polarity_plus = {plus_pairs}")
    print(f"  exact_two_line_pairs_polarity_minus = {minus_pairs}")
    print(f"  exact_two_line_pairs_total = {plus_pairs + minus_pairs}")

    print(f"{label}_best_one_lines:")
    for good, neg_mismatches, polarity, line in best:
        rate = good / len(rows)
        print(
            f"  good={good}/{len(rows)} rate={rate:.9f} "
            f"mismatches={-neg_mismatches} polarity={polarity} "
            f"line={line[0]}+{line[1]}*X+{line[2]}*W"
        )

    plus_samples = sample_pairs(first, target, pair_limit)
    minus_samples = sample_pairs(first, target ^ full, pair_limit)
    if plus_samples:
        print(f"{label}_exact_two_line_samples_polarity_plus:")
        for left, right in plus_samples:
            print(
                "  "
                f"({left[0]}+{left[1]}*X+{left[2]}*W) * "
                f"({right[0]}+{right[1]}*X+{right[2]}*W)"
            )
    if minus_samples:
        print(f"{label}_exact_two_line_samples_polarity_minus:")
        for left, right in minus_samples:
            print(
                "  "
                f"({left[0]}+{left[1]}*X+{left[2]}*W) * "
                f"({right[0]}+{right[1]}*X+{right[2]}*W)"
            )


def parse_primes(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def parse_families(raw: str) -> set[str]:
    families = {part.strip() for part in raw.split(",") if part.strip()}
    allowed = {"d3", "d4"}
    bad = families - allowed
    if bad:
        raise ValueError(f"unknown families: {sorted(bad)}")
    return families or allowed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1087,1471")
    parser.add_argument("--families", default="d3,d4")
    parser.add_argument("--pair-limit", type=int, default=4)
    args = parser.parse_args()

    families = parse_families(args.families)
    print("p27 E-quotient line-product probe")
    print(f"small_primes = {args.small_primes}")
    print(f"families = {','.join(sorted(families))}")

    for prime in parse_primes(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        for key in sorted(enum_stats):
            print(f"  enum_{key} = {enum_stats[key]}")
        for key in sorted(qstats):
            print(f"  quotient_{key} = {qstats[key]}")
        if "d3" in families:
            run_family(f"q{prime}_d3", d3_rows, prime, args.pair_limit)
        if "d4" in families:
            run_family(f"q{prime}_d4", d4_rows, prime, args.pair_limit)

    print("p27_equotient_line_product_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

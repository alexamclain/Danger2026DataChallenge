#!/usr/bin/env python3
"""Bitset exact L(4O) section solver on E'.

This is the exact version of the L(4O) screen intended for non-degenerate
p27-signature guard fields.  It tests whether d3/d4 is the squareclass of

    a + b U + c U^2 + d V

on E': V^2=U^3+4U, using projective coefficient charts.  The solver avoids a
naive q^3 * rows loop by treating the constant coefficient a as a bitset
intersection of shifted square/nonsquare sets.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


@dataclass(frozen=True)
class ExactSection:
    polarity: int
    coeffs: tuple[int, int, int, int]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for a in range(1, p):
        r = pow(a, (p - 1) // 2, p)
        table[a] = 1 if r == 1 else -1
    return table


def first_bit(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def bit_count(mask: int) -> int:
    return bin(mask).count("1")


def build_masks(p: int) -> dict[int, list[int]]:
    table = legendre_table(p)
    masks = {1: [], -1: []}
    for desired in (1, -1):
        for offset in range(p):
            mask = 0
            for a in range(p):
                if table[(a + offset) % p] == desired:
                    mask |= 1 << a
            masks[desired].append(mask)
    return masks


def exact_chart(
    rows,
    p: int,
    d: int,
    c_fixed: int | None,
    b_fixed: int | None,
    masks: dict[int, list[int]],
    limit: int,
) -> tuple[Counter, list[ExactSection]]:
    stats: Counter = Counter()
    samples: list[ExactSection] = []
    all_a = (1 << p) - 1
    u = [row.x % p for row in rows]
    u2 = [(row.x * row.x) % p for row in rows]
    v = [row.w % p for row in rows]
    targets = [row.target for row in rows]

    c_values = [c_fixed] if c_fixed is not None else range(p)
    b_values = [b_fixed] if b_fixed is not None else range(p)
    for c in c_values:
        for b in b_values:
            stats["bc_pairs"] += 1
            for polarity in (1, -1):
                intersection = all_a
                for i, target in enumerate(targets):
                    desired = polarity * target
                    offset = (b * u[i] + c * u2[i] + d * v[i]) % p
                    intersection &= masks[desired][offset]
                    if not intersection:
                        break
                if intersection:
                    count = bit_count(intersection)
                    stats[f"exact_polarity_{polarity}"] += count
                    if len(samples) < limit:
                        a = first_bit(intersection)
                        samples.append(ExactSection(polarity, (a, b, c, d)))
    return stats, samples


def screen_family(label: str, rows, p: int, min_rows: int, limit: int) -> Counter:
    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["plus"] = sum(1 for row in rows if row.target == 1)
    stats["minus"] = sum(1 for row in rows if row.target == -1)
    if len(rows) < min_rows:
        stats["skipped_too_few_rows"] = 1
        print_counter(f"{label}_stats", stats)
        return stats
    if stats["plus"] == 0 or stats["minus"] == 0:
        stats["skipped_one_sided"] = 1
        print_counter(f"{label}_stats", stats)
        return stats

    masks = build_masks(p)
    samples: list[ExactSection] = []
    # d=1 chart: a,b,c free
    chart_stats, chart_samples = exact_chart(rows, p, 1, None, None, masks, limit)
    stats.update({f"d1_{key}": value for key, value in chart_stats.items()})
    samples.extend(chart_samples)
    # d=0,c=1 chart
    chart_stats, chart_samples = exact_chart(rows, p, 0, 1, None, masks, max(0, limit - len(samples)))
    stats.update({f"c1_{key}": value for key, value in chart_stats.items()})
    samples.extend(chart_samples)
    # d=c=0,b=1 chart
    chart_stats, chart_samples = exact_chart(rows, p, 0, 0, 1, masks, max(0, limit - len(samples)))
    stats.update({f"b1_{key}": value for key, value in chart_stats.items()})
    samples.extend(chart_samples)
    # constant section cannot match a non-one-sided family, but count it as tested.
    stats["constant_tested"] = 1
    stats["exact_sections"] = sum(
        value for key, value in stats.items() if key.endswith("exact_polarity_1") or key.endswith("exact_polarity_-1")
    )
    print_counter(f"{label}_stats", stats)
    print(f"{label}_exact_samples:")
    for sample in samples[:limit]:
        a, b, c, d = sample.coeffs
        print(
            f"  polarity={sample.polarity} section={a}+{b}*U+{c}*U2+{d}*V"
        )
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="487,599")
    parser.add_argument("--min-rows", type=int, default=12)
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    print("p27 E-prime bitset exact L(4O) section probe")
    print("Eprime = V^2 = U^3 + 4U")
    print("basis = 1,U,U^2,V")
    print(f"small_primes = {args.small_primes}")

    for prime in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, source_stats = quotient_bit_rows_from_candidates(candidates, prime)
        qd3, d3_stats = quotient_rows(d3_rows, prime)
        qd4, d4_stats = quotient_rows(d4_rows, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{key}": value for key, value in enum_stats.items()}))
        print_counter("  original_quotient_stats", source_stats)
        print_counter("  eprime_d3_stats", d3_stats)
        print_counter("  eprime_d4_stats", d4_stats)
        screen_family(f"q{prime}_d3_l4_bitset", qd3, prime, args.min_rows, args.sample_limit)
        screen_family(f"q{prime}_d4_l4_bitset", qd4, prime, args.min_rows, args.sample_limit)

    print("p27_eprime_l4_section_bitset_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

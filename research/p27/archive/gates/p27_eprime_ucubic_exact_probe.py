#!/usr/bin/env python3
"""Exact U-cubic screen on the p27 E-prime quotient.

The L(4O) screen found local q487 artifacts among quadratic polynomials in U,
but no section survives q599/q727/q919.  This probe tests the next rational
U-line family exactly:

    a + b U + c U^2 + d U^3.

It is a targeted Kummer-line falsifier, not a broad low-pole search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


@dataclass(frozen=True)
class ExactPolynomial:
    polarity: int
    coeffs: tuple[int, int, int, int]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for a in range(1, p):
        table[a] = 1 if pow(a, (p - 1) // 2, p) == 1 else -1
    return table


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


def first_bit(mask: int) -> int:
    return (mask & -mask).bit_length() - 1


def bit_count(mask: int) -> int:
    return bin(mask).count("1")


def exact_chart(rows, p: int, d: int, c_fixed: int | None, b_fixed: int | None, masks, limit: int):
    stats: Counter = Counter()
    samples: list[ExactPolynomial] = []
    all_a = (1 << p) - 1
    u = [row.x % p for row in rows]
    u2 = [(row.x * row.x) % p for row in rows]
    u3 = [(row.x * row.x % p) * row.x % p for row in rows]
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
                    offset = (b * u[i] + c * u2[i] + d * u3[i]) % p
                    intersection &= masks[desired][offset]
                    if not intersection:
                        break
                if intersection:
                    stats[f"exact_polarity_{polarity}"] += bit_count(intersection)
                    if len(samples) < limit:
                        samples.append(ExactPolynomial(polarity, (first_bit(intersection), b, c, d)))
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
    samples: list[ExactPolynomial] = []
    # d=1 chart: a,b,c free
    chart, chart_samples = exact_chart(rows, p, 1, None, None, masks, limit)
    stats.update({f"d1_{key}": value for key, value in chart.items()})
    samples.extend(chart_samples)
    # d=0,c=1 chart: quadratics already tested, but retained for exact counts.
    chart, chart_samples = exact_chart(rows, p, 0, 1, None, masks, max(0, limit - len(samples)))
    stats.update({f"c1_{key}": value for key, value in chart.items()})
    samples.extend(chart_samples)
    # d=c=0,b=1 chart
    chart, chart_samples = exact_chart(rows, p, 0, 0, 1, masks, max(0, limit - len(samples)))
    stats.update({f"b1_{key}": value for key, value in chart.items()})
    samples.extend(chart_samples)
    stats["constant_tested"] = 1
    stats["exact_polynomials"] = sum(
        value for key, value in stats.items()
        if key.endswith("exact_polarity_1") or key.endswith("exact_polarity_-1")
    )
    print_counter(f"{label}_stats", stats)
    print(f"{label}_exact_samples:")
    for sample in samples[:limit]:
        a, b, c, d = sample.coeffs
        print(f"  polarity={sample.polarity} poly={a}+{b}*U+{c}*U2+{d}*U3")
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="487,599,727,919")
    parser.add_argument("--min-rows", type=int, default=12)
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    print("p27 E-prime exact U-cubic probe")
    print("Eprime = V^2 = U^3 + 4U")
    print("family = a+bU+cU2+dU3")
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
        screen_family(f"q{prime}_d3_ucubic", qd3, prime, args.min_rows, args.sample_limit)
        screen_family(f"q{prime}_d4_ucubic", qd4, prime, args.min_rows, args.sample_limit)

    print("p27_eprime_ucubic_exact_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

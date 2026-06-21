#!/usr/bin/env python3
"""Exact L(4O) section screen on the p27 E-prime quotient.

Prior probes killed lines, two-line products, sparse visible branch packets,
small affine walks, and random low-pole products on

    E': V^2 = U^3 + 4U.

This probe tests the next tiny exact family: single projective sections of
L(4O), with basis

    1, U, U^2, V.

Equivalently it asks whether the descended d3/d4 bit is the squareclass of

    a + b U + c U^2 + d V

over small p27-signature guard fields q = 7 mod 16.  This is still a narrow
finite-field falsifier, not a broad coefficient fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_reverse_source_quotient_probe import legendre_table
from p27_equotient_2isogeny_line_probe import quotient_rows


@dataclass(frozen=True)
class SectionScore:
    good: int
    zeros: int
    polarity: int
    coeffs: tuple[int, int, int, int]


def projective_sections_l4(p: int) -> Iterable[tuple[int, int, int, int]]:
    # d = 1 chart
    for a in range(p):
        for b in range(p):
            for c in range(p):
                yield a, b, c, 1
    # d = 0, c = 1 chart
    for a in range(p):
        for b in range(p):
            yield a, b, 1, 0
    # d = c = 0, b = 1 chart
    for a in range(p):
        yield a, 1, 0, 0
    # constant section
    yield 1, 0, 0, 0


def section_value(row, coeffs: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = coeffs
    u = row.x % p
    v = row.w % p
    return (a + b * u + c * u * u + d * v) % p


def score_section(rows, coeffs: tuple[int, int, int, int], table: list[int], p: int) -> SectionScore:
    good_plus = 0
    good_minus = 0
    zeros = 0
    for row in rows:
        chi = table[section_value(row, coeffs, p)]
        if chi == 0:
            zeros += 1
            continue
        if chi == row.target:
            good_plus += 1
        if chi == -row.target:
            good_minus += 1
    if good_plus >= good_minus:
        return SectionScore(good_plus, zeros, 1, coeffs)
    return SectionScore(good_minus, zeros, -1, coeffs)


def insert_best(best: list[SectionScore], score: SectionScore, limit: int) -> None:
    best.append(score)
    best.sort(
        key=lambda item: (
            item.good,
            -item.zeros,
            -sum(1 for c in item.coeffs if c),
            tuple(-c for c in item.coeffs),
        ),
        reverse=True,
    )
    del best[limit:]


def screen_family(label: str, rows, p: int, top: int) -> tuple[Counter, list[SectionScore], list[SectionScore]]:
    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["plus"] = sum(1 for row in rows if row.target == 1)
    stats["minus"] = sum(1 for row in rows if row.target == -1)
    stats["projective_sections"] = p**3 + p**2 + p + 1
    if not rows:
        stats["skipped_empty_rows"] = 1
        print_counter(f"{label}_stats", stats)
        print(f"{label}_best:")
        print(f"{label}_exact:")
        return stats, [], []
    table = legendre_table(p)
    best: list[SectionScore] = []
    exact: list[SectionScore] = []
    for coeffs in projective_sections_l4(p):
        score = score_section(rows, coeffs, table, p)
        insert_best(best, score, top)
        if score.zeros == 0 and score.good == len(rows):
            exact.append(score)
            if len(exact) > top:
                exact = exact[:top]
        stats["sections_tested"] += 1
    stats["exact_sections"] = len(exact)
    stats["best_good"] = best[0].good if best else 0
    stats["best_zeros"] = best[0].zeros if best else 0
    stats["best_polarity"] = best[0].polarity if best else 0
    print_counter(f"{label}_stats", stats)
    print_scores(f"{label}_best", best, len(rows))
    print_scores(f"{label}_exact", exact, len(rows))
    return stats, best, exact


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[SectionScore], total: int) -> None:
    print(f"{prefix}:")
    for score in scores:
        rate = score.good / total if total else 0.0
        a, b, c, d = score.coeffs
        print(
            f"  good={score.good}/{total} rate={rate:.9f} zeros={score.zeros} "
            f"polarity={score.polarity} section={a}+{b}*U+{c}*U2+{d}*V"
        )


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="103,167,263")
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    print("p27 E-prime exact L(4O) section probe")
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
        screen_family(f"q{prime}_d3_l4", qd3, prime, args.top)
        screen_family(f"q{prime}_d4_l4", qd4, prime, args.top)

    print("p27_eprime_l4_section_exact_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

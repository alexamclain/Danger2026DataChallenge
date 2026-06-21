#!/usr/bin/env python3
"""Kummer-line screen after signed doubling on the p27 E' quotient.

The E' group-projection probe found that both d3 and d4 are constant on signed
[2] projection classes over many guard fields.  On

    E': V^2 = U^3 + 4U

the signed [2] projection is represented by the Kummer coordinate

    K = x([2](U,V)) = (U^2 - 4)^2 / (4*U*(U^2 + 4)).

This probe verifies descent to K and asks the first sourceable question: are
d3 or d4 quadratic characters of a degree-1 or degree-2 polynomial in K?  A
degree <= 2 formula would give a rational source; degree 3/4 would suggest an
elliptic source as the next test.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import QuotientRow, quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


@dataclass(frozen=True)
class KRow:
    k: int
    target: int


@dataclass(frozen=True)
class PolyScore:
    good: int
    total: int
    zeros: int
    polarity: int
    coeffs: tuple[int, ...]


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def kummer_double_x(u: int, p: int) -> int | None:
    den = 4 * u % p * ((u * u + 4) % p) % p
    if den == 0:
        return None
    num = (u * u - 4) % p
    num = num * num % p
    return num * inv(den, p) % p


def to_krows(rows: list[QuotientRow], p: int) -> tuple[list[KRow], Counter]:
    by_k: dict[int, int] = {}
    stats: Counter = Counter()
    for row in rows:
        k = kummer_double_x(row.x, p)
        if k is None:
            stats["k_undefined_skip"] += 1
            continue
        prior = by_k.get(k)
        if prior is not None and prior != row.target:
            stats["mixed_k_class"] += 1
            continue
        by_k[k] = row.target
    out = [KRow(k=k, target=target) for k, target in sorted(by_k.items())]
    stats["input_rows"] = len(rows)
    stats["k_rows"] = len(out)
    stats["plus"] = sum(1 for row in out if row.target == 1)
    stats["minus"] = sum(1 for row in out if row.target == -1)
    return out, stats


def projective_polys(degree: int, p: int) -> Iterable[tuple[int, ...]]:
    if degree == 0:
        yield (1,)
        return
    # Normalize by the highest nonzero coefficient.
    for coeffs in _projective_polys_exact_len(degree + 1, p):
        yield coeffs


def _projective_polys_exact_len(length: int, p: int) -> Iterable[tuple[int, ...]]:
    if length == 1:
        yield (1,)
        return
    # Highest coefficient nonzero and normalized to 1.
    prefix_len = length - 1
    for n in range(p ** prefix_len):
        coeffs = []
        x = n
        for _ in range(prefix_len):
            coeffs.append(x % p)
            x //= p
        yield tuple(coeffs + [1])
    # Highest coefficient zero: recurse to lower degree.
    for lower in _projective_polys_exact_len(length - 1, p):
        yield lower + (0,)


def eval_poly(coeffs: tuple[int, ...], k: int, p: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * k + coeff) % p
    return acc


def score_poly(rows: list[KRow], coeffs: tuple[int, ...], p: int) -> PolyScore:
    good_plus = 0
    good_minus = 0
    zeros = 0
    total = 0
    for row in rows:
        chi = legendre(eval_poly(coeffs, row.k, p), p)
        if chi == 0:
            zeros += 1
            continue
        total += 1
        if chi == row.target:
            good_plus += 1
        if chi == -row.target:
            good_minus += 1
    if good_plus >= good_minus:
        return PolyScore(good_plus, total, zeros, 1, coeffs)
    return PolyScore(good_minus, total, zeros, -1, coeffs)


def screen_polys(rows: list[KRow], p: int, degree: int, top: int) -> tuple[Counter, list[PolyScore], list[PolyScore]]:
    best: list[PolyScore] = []
    exact: list[PolyScore] = []
    tested = 0
    for coeffs in projective_polys(degree, p):
        tested += 1
        score = score_poly(rows, coeffs, p)
        best.append(score)
        if score.total == len(rows) and score.zeros == 0 and score.good == len(rows):
            exact.append(score)
    best.sort(key=lambda s: (s.good / s.total if s.total else 0.0, s.good, -s.zeros), reverse=True)
    exact.sort(key=lambda s: (len(s.coeffs), s.coeffs))
    stats: Counter = Counter()
    stats["degree"] = degree
    stats["rows"] = len(rows)
    stats["polys_tested"] = tested
    stats["exact_polys"] = len(exact)
    stats["best_good"] = best[0].good if best else 0
    stats["best_total"] = best[0].total if best else 0
    stats["best_zeros"] = best[0].zeros if best else 0
    return stats, best[:top], exact[:top]


def coeffs_name(coeffs: tuple[int, ...]) -> str:
    terms = []
    for i, coeff in enumerate(coeffs):
        if coeff == 0:
            continue
        if i == 0:
            terms.append(str(coeff))
        elif i == 1:
            terms.append(f"{coeff}*K")
        else:
            terms.append(f"{coeff}*K^{i}")
    return " + ".join(terms) if terms else "0"


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[PolyScore]) -> None:
    print(f"{prefix}:")
    for score in scores:
        rate = score.good / score.total if score.total else 0.0
        print(
            f"  good={score.good}/{score.total} rate={rate:.9f} "
            f"zeros={score.zeros} polarity={score.polarity} poly={coeffs_name(score.coeffs)}"
        )


def run_family(label: str, rows: list[QuotientRow], p: int, max_degree: int, top: int) -> None:
    krows, kstats = to_krows(rows, p)
    print_counter(f"{label}_kummer_descent", kstats)
    for degree in range(1, max_degree + 1):
        stats, best, exact = screen_polys(krows, p, degree, top)
        print_counter(f"{label}_degree{degree}_screen", stats)
        print_scores(f"{label}_degree{degree}_best", best)
        print_scores(f"{label}_degree{degree}_exact", exact)


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--max-degree", type=int, default=2)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    print("p27 E-prime signed-doubling Kummer-line probe")
    print("K = x([2]P) = (U^2-4)^2/(4*U*(U^2+4))")
    print(f"small_primes = {args.small_primes}")
    print(f"max_degree = {args.max_degree}")

    for p in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(p)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, p)
        qd3, d3_iso_stats = quotient_rows(d3_rows, p)
        qd4, d4_iso_stats = quotient_rows(d4_rows, p)
        print(f"q={p}:")
        for key in sorted(enum_stats):
            print(f"  enum_{key} = {enum_stats[key]}")
        for key in sorted(qstats):
            print(f"  quotient_{key} = {qstats[key]}")
        for key in sorted(d3_iso_stats):
            print(f"  d3_eprime_{key} = {d3_iso_stats[key]}")
        for key in sorted(d4_iso_stats):
            print(f"  d4_eprime_{key} = {d4_iso_stats[key]}")
        run_family(f"q{p}_d3", qd3, p, args.max_degree, args.top)
        run_family(f"q{p}_d4", qd4, p, args.max_degree, args.top)

    print("p27_eprime_double_kummer_line_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

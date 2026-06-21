#!/usr/bin/env python3
"""Quotient/orbit screen for the p27 reverse-doubling source.

The reverse source is useful only if it leads to a direct source or recurrence,
not merely another generic half-density cover.  This probe tests the first
quotient-shaped possibility after the order-4 lift:

* does the d3/reverse-source bit descend to the residual elliptic quotient
  E: W^2 = X^3-X?
* if it descends, is it a visible low-degree line character on E?

The line screen is intentionally narrow.  It is a falsifier for a cheap
quotient character, not a broad search over arbitrary rational functions.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable

from p27_label2_alpha_branch_recurrence_probe import (
    P,
    halve_all,
    legendre,
    sample_rows,
)
from p27_reverse_doubling_source_probe import (
    all_oriented_candidates_from_row,
    enumerate_small_prime_candidates,
)


@dataclass(frozen=True)
class QuotientRow:
    x: int
    w: int
    target: int


def d3_squareclass_for_candidate(cand: dict[str, int], p: int) -> int | None:
    a = int(cand["A"])
    x5 = int(cand["x5"])
    d2_chi, x6s = halve_all(a, x5, p)
    if d2_chi != 1 or not x6s:
        return None
    classes = {legendre(x6, p) for x6 in x6s}
    classes.discard(0)
    if len(classes) != 1:
        return 0
    return next(iter(classes))


def quotient_rows_from_candidates(
    candidates: Iterable[dict[str, int]], p: int
) -> tuple[list[QuotientRow], Counter]:
    by_ew: defaultdict[tuple[int, int], list[int | None]] = defaultdict(list)
    stats: Counter = Counter()
    for cand in candidates:
        key = (int(cand["X"]), int(cand["W"]))
        by_ew[key].append(d3_squareclass_for_candidate(cand, p))
        stats["oriented_candidates"] += 1

    rows: list[QuotientRow] = []
    for (x, w), values in by_ew.items():
        stats["quotient_E_points"] += 1
        none_count = sum(v is None for v in values)
        zero_count = sum(v == 0 for v in values)
        nonzero = [int(v) for v in values if v in (-1, 1)]
        if none_count:
            stats["d3_missing_on_E_orbit"] += 1
        if zero_count:
            stats["d3_mixed_branch_squareclass"] += 1
        if not nonzero:
            stats["d3_no_nonzero_on_E_orbit"] += 1
            continue
        if len(set(nonzero)) != 1:
            stats["d3_not_descended_to_E"] += 1
            continue
        stats[f"orbit_size_{len(values)}"] += 1
        rows.append(QuotientRow(x=x, w=w, target=nonzero[0]))

    stats["quotient_rows"] = len(rows)
    stats["d3_plus_E_points"] = sum(1 for row in rows if row.target == 1)
    stats["d3_minus_E_points"] = sum(1 for row in rows if row.target == -1)
    for key in [
        "d3_missing_on_E_orbit",
        "d3_mixed_branch_squareclass",
        "d3_no_nonzero_on_E_orbit",
        "d3_not_descended_to_E",
    ]:
        stats.setdefault(key, 0)
    return rows, stats


def p27_quotient_rows(target: int, seed: int, max_draws: int) -> tuple[list[QuotientRow], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    quotient_rows, stats = quotient_rows_from_candidates(candidates, P)
    stats.update({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    return quotient_rows, stats


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for a in range(1, p):
        r = pow(a, (p - 1) // 2, p)
        table[a] = 1 if r == 1 else -1
    return table


def projective_lines(p: int) -> Iterable[tuple[int, int, int]]:
    for a in range(p):
        for b in range(p):
            yield a, b, 1
    for a in range(p):
        yield a, 1, 0
    yield 1, 0, 0


def score_lines_all_projective(rows: list[QuotientRow], p: int, limit: int = 8) -> tuple[Counter, list[tuple[int, int, int, int, int, int]]]:
    stats: Counter = Counter()
    if not rows:
        return stats, []
    table = legendre_table(p)
    best: list[tuple[int, int, int, int, int, int]] = []
    exact: list[tuple[int, int, int, int, int, int]] = []
    total = len(rows)
    for a, b, c in projective_lines(p):
        good = 0
        good_neg = 0
        zeros = 0
        for row in rows:
            value = (a + b * row.x + c * row.w) % p
            chi = table[value]
            if chi == 0:
                zeros += 1
                continue
            if chi == row.target:
                good += 1
            if chi == -row.target:
                good_neg += 1
        best_good = max(good, good_neg)
        polarity = 1 if good >= good_neg else -1
        record = (best_good, -zeros, polarity, a, b, c)
        best.append(record)
        if zeros == 0 and best_good == total:
            exact.append(record)
    best.sort(reverse=True)
    exact.sort(reverse=True)
    stats["line_rows"] = total
    stats["projective_lines_tested"] = p * p + p + 1
    stats["exact_lines"] = len(exact)
    stats["best_good"] = best[0][0] if best else 0
    stats["best_zeros"] = -best[0][1] if best else 0
    stats["best_polarity"] = best[0][2] if best else 0
    return stats, (exact[:limit] if exact else best[:limit])


def small_coeff_lines(bound: int) -> Iterable[tuple[int, int, int]]:
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                if a == b == c == 0:
                    continue
                yield a, b, c


def score_lines_small_coeff(rows: list[QuotientRow], p: int, bound: int, limit: int = 8) -> tuple[Counter, list[tuple[int, int, int, int, int, int]]]:
    stats: Counter = Counter()
    best: list[tuple[int, int, int, int, int, int]] = []
    total = len(rows)
    for a, b, c in small_coeff_lines(bound):
        good = 0
        good_neg = 0
        zeros = 0
        for row in rows:
            chi = legendre(a + b * row.x + c * row.w, p)
            if chi == 0:
                zeros += 1
                continue
            if chi == row.target:
                good += 1
            if chi == -row.target:
                good_neg += 1
        best_good = max(good, good_neg)
        polarity = 1 if good >= good_neg else -1
        best.append((best_good, -zeros, polarity, a, b, c))
    best.sort(reverse=True)
    stats["line_rows"] = total
    stats["small_coeff_bound"] = bound
    stats["small_coeff_lines_tested"] = (2 * bound + 1) ** 3 - 1
    stats["exact_lines"] = sum(1 for row in best if row[0] == total and row[1] == 0)
    stats["best_good"] = best[0][0] if best else 0
    stats["best_zeros"] = -best[0][1] if best else 0
    stats["best_polarity"] = best[0][2] if best else 0
    return stats, best[:limit]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_line_results(prefix: str, stats: Counter, rows: list[tuple[int, int, int, int, int, int]]) -> None:
    print_counter(prefix, stats)
    total = stats["line_rows"]
    print(f"{prefix}_top_lines:")
    for good, neg_zeros, polarity, a, b, c in rows:
        zeros = -neg_zeros
        rate = good / total if total else 0.0
        print(
            f"  good={good}/{total} rate={rate:.9f} zeros={zeros} "
            f"polarity={polarity} line={a}+{b}*X+{c}*W"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--small-primes", default="607,863,991")
    parser.add_argument(
        "--p27-line-bound",
        type=int,
        default=2,
        help="small integer bound for the expensive p27 line sanity screen",
    )
    args = parser.parse_args()

    print("p27 reverse-source quotient/orbit probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")

    rows, stats = p27_quotient_rows(args.target, args.seed, args.max_draws)
    print_counter("p27_quotient_descent", stats)
    line_stats, line_rows = score_lines_small_coeff(rows, P, args.p27_line_bound)
    print_line_results("p27_small_coeff_line_screen", line_stats, line_rows)

    print("small_prime_quotient_line_screens:")
    for prime in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        qrows, qstats = quotient_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enumeration", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_descent", qstats)
        qline_stats, qline_rows = score_lines_all_projective(qrows, prime)
        print_line_results("  projective_line_screen", qline_stats, qline_rows)

    print("p27_reverse_source_quotient_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

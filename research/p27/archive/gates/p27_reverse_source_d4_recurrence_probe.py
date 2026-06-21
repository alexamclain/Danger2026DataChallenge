#!/usr/bin/env python3
"""D4 quotient/recurrence screen for the p27 reverse-source lane.

The previous quotient probe showed that the d3/reverse-source bit descends to
the residual elliptic quotient E: W^2=X^3-X, but is not a degree-1 line
character.  This probe asks the next recurrence-shaped question:

* after conditioning on d3=+1, does d4 also descend to the same E quotient?
* on a small exhaustive field, is d4 just the d3 character after an obvious
  elliptic transformation such as negation, adding rational 2-torsion, or
  doubling plus 2-torsion?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows
from p27_reverse_doubling_source_probe import (
    all_oriented_candidates_from_row,
    enumerate_small_prime_candidates,
)
from p27_reverse_source_quotient_probe import (
    QuotientRow,
    score_lines_all_projective,
    score_lines_small_coeff,
)


Point = Optional[tuple[int, int]]


@dataclass(frozen=True)
class CandidateBits:
    d3: int | None
    d4: int | None


def normalize(values: Iterable[int | None]) -> int | None:
    vals = {int(v) for v in values if v in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return next(iter(vals))


def candidate_bits(cand: dict[str, int], p: int) -> CandidateBits:
    a = int(cand["A"])
    x5 = int(cand["x5"])
    d2_chi, x6s = halve_all(a, x5, p)
    if d2_chi != 1 or not x6s:
        return CandidateBits(None, None)

    d3_values: list[int] = []
    d4_values: list[int] = []
    for x6 in x6s:
        # On this nonsplit path chi(d_next)=chi(x_next), and the alpha probe
        # independently checks this against the Montgomery d-polynomial.
        d3_chi = legendre(x6, p)
        d3_values.append(d3_chi)
        if d3_chi != 1:
            continue
        d3_halve_chi, x7s = halve_all(a, x6, p)
        if d3_halve_chi != 1 or not x7s:
            d4_values.append(0)
            continue
        d4_values.extend(legendre(x7, p) for x7 in x7s)

    d3 = normalize(d3_values)
    d4 = normalize(d4_values) if d3 == 1 else None
    return CandidateBits(d3=d3, d4=d4)


def quotient_bit_rows_from_candidates(
    candidates: Iterable[dict[str, int]], p: int
) -> tuple[list[QuotientRow], list[QuotientRow], Counter]:
    by_ew: defaultdict[tuple[int, int], list[CandidateBits]] = defaultdict(list)
    stats: Counter = Counter()
    for cand in candidates:
        by_ew[(int(cand["X"]), int(cand["W"]))].append(candidate_bits(cand, p))
        stats["oriented_candidates"] += 1

    d3_rows: list[QuotientRow] = []
    d4_rows: list[QuotientRow] = []
    for (x, w), bits in by_ew.items():
        stats["quotient_E_points"] += 1
        stats[f"orbit_size_{len(bits)}"] += 1
        d3 = normalize(bit.d3 for bit in bits)
        if d3 is None:
            stats["d3_missing_on_E_orbit"] += 1
            continue
        if d3 == 0:
            stats["d3_not_descended_to_E"] += 1
            continue
        d3_rows.append(QuotientRow(x=x, w=w, target=d3))
        if d3 != 1:
            continue
        d4 = normalize(bit.d4 for bit in bits)
        if d4 is None:
            stats["d4_missing_on_E_orbit"] += 1
            continue
        if d4 == 0:
            stats["d4_not_descended_to_E"] += 1
            continue
        d4_rows.append(QuotientRow(x=x, w=w, target=d4))

    stats["d3_quotient_rows"] = len(d3_rows)
    stats["d3_plus_E_points"] = sum(1 for row in d3_rows if row.target == 1)
    stats["d3_minus_E_points"] = sum(1 for row in d3_rows if row.target == -1)
    stats["d4_quotient_rows_after_d3"] = len(d4_rows)
    stats["d4_plus_E_points_after_d3"] = sum(1 for row in d4_rows if row.target == 1)
    stats["d4_minus_E_points_after_d3"] = sum(1 for row in d4_rows if row.target == -1)
    for key in [
        "d3_missing_on_E_orbit",
        "d3_not_descended_to_E",
        "d4_missing_on_E_orbit",
        "d4_not_descended_to_E",
    ]:
        stats.setdefault(key, 0)
    return d3_rows, d4_rows, stats


def p27_rows(target: int, seed: int, max_draws: int) -> tuple[list[QuotientRow], list[QuotientRow], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    d3_rows, d4_rows, stats = quotient_bit_rows_from_candidates(candidates, P)
    stats.update({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    return d3_rows, d4_rows, stats


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def e_add(p1: Point, p2: Point, p: int) -> Point:
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
        slope = (3 * x1 * x1 - 1) * inv(2 * y1, p) % p
    else:
        slope = (y2 - y1) * inv(x2 - x1, p) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def e_neg(point: Point, p: int) -> Point:
    if point is None:
        return None
    x, y = point
    return x, (-y) % p


def recurrence_transforms(p: int) -> list[tuple[str, Callable[[Point], Point]]]:
    torsion = {
        "T0": (0, 0),
        "T1": (1 % p, 0),
        "Tm1": ((-1) % p, 0),
    }
    transforms: list[tuple[str, Callable[[Point], Point]]] = [
        ("id", lambda point: point),
        ("neg", lambda point: e_neg(point, p)),
    ]
    for name, tors in torsion.items():
        transforms.append((f"add_{name}", lambda point, tors=tors: e_add(point, tors, p)))
        transforms.append(
            (
                f"neg_add_{name}",
                lambda point, tors=tors: e_neg(e_add(point, tors, p), p),
            )
        )
    transforms.append(("double", lambda point: e_add(point, point, p)))
    transforms.append(("neg_double", lambda point: e_neg(e_add(point, point, p), p)))
    for name, tors in torsion.items():
        transforms.append(
            (
                f"double_add_{name}",
                lambda point, tors=tors: e_add(e_add(point, point, p), tors, p),
            )
        )
        transforms.append(
            (
                f"neg_double_add_{name}",
                lambda point, tors=tors: e_neg(e_add(e_add(point, point, p), tors, p), p),
            )
        )
    return transforms


def recurrence_screen(
    d3_rows: list[QuotientRow], d4_rows: list[QuotientRow], p: int
) -> list[tuple[int, int, int, str, int]]:
    d3_map = {(row.x, row.w): row.target for row in d3_rows}
    out: list[tuple[int, int, int, str, int]] = []
    total = len(d4_rows)
    for name, transform in recurrence_transforms(p):
        covered = 0
        good = 0
        good_neg = 0
        for row in d4_rows:
            image = transform((row.x, row.w))
            if image is None or image not in d3_map:
                continue
            covered += 1
            target = d3_map[image]
            if row.target == target:
                good += 1
            if row.target == -target:
                good_neg += 1
        out.append((max(good, good_neg), covered, total, name, 1 if good >= good_neg else -1))
    out.sort(reverse=True)
    return out


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


def print_recurrence(prefix: str, rows: list[tuple[int, int, int, str, int]], limit: int = 16) -> None:
    print(f"{prefix}:")
    for good, covered, total, name, polarity in rows[:limit]:
        rate = good / covered if covered else 0.0
        coverage = covered / total if total else 0.0
        print(
            f"  transform={name} polarity={polarity} "
            f"good={good}/{covered} rate={rate:.9f} coverage={coverage:.9f}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--small-primes", default="607")
    parser.add_argument("--p27-line-bound", type=int, default=2)
    args = parser.parse_args()

    print("p27 reverse-source d4 quotient/recurrence probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")

    d3_rows, d4_rows, stats = p27_rows(args.target, args.seed, args.max_draws)
    print_counter("p27_quotient_descent", stats)
    p27_line_stats, p27_line_rows = score_lines_small_coeff(d4_rows, P, args.p27_line_bound)
    print_line_results("p27_d4_small_coeff_line_screen", p27_line_stats, p27_line_rows)

    print("small_prime_d4_recurrence_screens:")
    for prime in [int(part) for part in args.small_primes.split(",") if part.strip()]:
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        qd3, qd4, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enumeration", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_descent", qstats)
        qline_stats, qline_rows = score_lines_all_projective(qd4, prime)
        print_line_results("  d4_projective_line_screen", qline_stats, qline_rows)
        print_recurrence("  simple_E_transform_recurrence_screen", recurrence_screen(qd3, qd4, prime))

    print("p27_reverse_source_d4_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

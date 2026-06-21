#!/usr/bin/env python3
"""Small-integer Kummer-line polynomial screen for p27 d3/d4.

The signed-doubling screen reduced the active quotient target to the Kummer
line

    K = x([2]P) on E': V^2 = U^3 + 4U.

The exhaustive per-field degree <= 2 screen was negative.  Exhaustive degree
3/4 over all field coefficients is too large and, for d4, too fit-prone in a
single small field.  This probe tests the theorem-shaped subcase first:

    one small integer cubic/quartic in K works across all guard fields,
    allowing an overall field-dependent polarity.

That is the finite-field shadow of a compact rational formula with small
integer coefficients.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from dataclasses import dataclass
from itertools import product

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows
from p27_eprime_double_kummer_line_probe import KRow, to_krows


@dataclass(frozen=True)
class FieldRows:
    q: int
    d3: list[KRow]
    d4: list[KRow]


@dataclass(frozen=True)
class FieldScore:
    q: int
    good: int
    total: int
    zeros: int
    polarity: int


@dataclass(frozen=True)
class CandidateScore:
    coeffs: tuple[int, ...]
    exact_fields: int
    min_good_rate_num: int
    min_good_rate_den: int
    total_good: int
    total_rows: int
    total_zeros: int
    field_scores: tuple[FieldScore, ...]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


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


def canonical_coeffs(coeffs: tuple[int, ...]) -> tuple[int, ...] | None:
    if not any(coeffs):
        return None
    g = 0
    for coeff in coeffs:
        g = math.gcd(g, abs(coeff))
    if g != 1:
        return None
    for coeff in reversed(coeffs):
        if coeff:
            return coeffs if coeff > 0 else tuple(-c for c in coeffs)
    return None


def small_integer_coeffs(degree: int, bound: int):
    lo = -bound
    hi = bound + 1
    for coeffs in product(range(lo, hi), repeat=degree + 1):
        if coeffs[-1] == 0:
            continue
        canon = canonical_coeffs(tuple(coeffs))
        if canon is None or canon != coeffs:
            continue
        yield coeffs


def eval_poly(coeffs: tuple[int, ...], k: int, q: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * k + coeff) % q
    return acc


def score_field(rows: list[KRow], q: int, coeffs: tuple[int, ...]) -> FieldScore:
    good_plus = 0
    good_minus = 0
    zeros = 0
    total = 0
    for row in rows:
        chi = legendre(eval_poly(coeffs, row.k, q), q)
        if chi == 0:
            zeros += 1
            continue
        total += 1
        if chi == row.target:
            good_plus += 1
        if chi == -row.target:
            good_minus += 1
    if good_plus >= good_minus:
        return FieldScore(q=q, good=good_plus, total=total, zeros=zeros, polarity=1)
    return FieldScore(q=q, good=good_minus, total=total, zeros=zeros, polarity=-1)


def score_candidate(fields: list[FieldRows], target: str, coeffs: tuple[int, ...]) -> CandidateScore:
    scores = []
    exact_fields = 0
    total_good = 0
    total_rows = 0
    total_zeros = 0
    min_num = 1
    min_den = 1
    for field in fields:
        rows = field.d3 if target == "d3" else field.d4
        score = score_field(rows, field.q, coeffs)
        scores.append(score)
        total_good += score.good
        total_rows += len(rows)
        total_zeros += score.zeros
        if score.total == len(rows) and score.zeros == 0 and score.good == len(rows):
            exact_fields += 1
        if score.total == 0 or score.good * min_den < min_num * score.total:
            min_num = score.good
            min_den = score.total
    return CandidateScore(
        coeffs=coeffs,
        exact_fields=exact_fields,
        min_good_rate_num=min_num,
        min_good_rate_den=min_den,
        total_good=total_good,
        total_rows=total_rows,
        total_zeros=total_zeros,
        field_scores=tuple(scores),
    )


def score_key(score: CandidateScore) -> tuple[int, float, int, int, int]:
    min_rate = score.min_good_rate_num / score.min_good_rate_den if score.min_good_rate_den else 0.0
    total_rate_num = score.total_good
    return (
        score.exact_fields,
        min_rate,
        total_rate_num,
        -score.total_zeros,
        -sum(abs(c) for c in score.coeffs),
    )


def insert_best(best: list[CandidateScore], score: CandidateScore, limit: int) -> None:
    best.append(score)
    best.sort(key=score_key, reverse=True)
    del best[limit:]


def collect_fields(primes: list[int]) -> tuple[list[FieldRows], Counter]:
    out: list[FieldRows] = []
    stats: Counter = Counter()
    for q in primes:
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, q)
        qd3, d3_iso_stats = quotient_rows(d3_rows, q)
        qd4, d4_iso_stats = quotient_rows(d4_rows, q)
        kd3, d3_k_stats = to_krows(qd3, q)
        kd4, d4_k_stats = to_krows(qd4, q)
        out.append(FieldRows(q=q, d3=kd3, d4=kd4))
        for key, value in enum_stats.items():
            stats[f"q{q}_enum_{key}"] = value
        for key, value in qstats.items():
            stats[f"q{q}_quotient_{key}"] = value
        for key, value in d3_iso_stats.items():
            stats[f"q{q}_d3_eprime_{key}"] = value
        for key, value in d4_iso_stats.items():
            stats[f"q{q}_d4_eprime_{key}"] = value
        for key, value in d3_k_stats.items():
            stats[f"q{q}_d3_k_{key}"] = value
        for key, value in d4_k_stats.items():
            stats[f"q{q}_d4_k_{key}"] = value
    return out, stats


def print_field_summary(fields: list[FieldRows]) -> None:
    print("field_rows:")
    for field in fields:
        print(
            f"  q={field.q} d3={len(field.d3)} "
            f"d3_plus={sum(1 for row in field.d3 if row.target == 1)} "
            f"d4={len(field.d4)} d4_plus={sum(1 for row in field.d4 if row.target == 1)}"
        )


def print_candidate(prefix: str, score: CandidateScore) -> None:
    min_rate = score.min_good_rate_num / score.min_good_rate_den if score.min_good_rate_den else 0.0
    total_rate = score.total_good / score.total_rows if score.total_rows else 0.0
    print(
        f"  exact_fields={score.exact_fields} min_rate={min_rate:.9f} "
        f"total={score.total_good}/{score.total_rows} total_rate={total_rate:.9f} "
        f"zeros={score.total_zeros} poly={coeffs_name(score.coeffs)}"
    )
    for fs in score.field_scores:
        rate = fs.good / fs.total if fs.total else 0.0
        print(
            f"    q={fs.q} good={fs.good}/{fs.total} rate={rate:.9f} "
            f"zeros={fs.zeros} polarity={fs.polarity}"
        )


def run_screen(fields: list[FieldRows], target: str, degree: int, bound: int, top: int) -> None:
    stats: Counter = Counter()
    best: list[CandidateScore] = []
    exact: list[CandidateScore] = []
    for coeffs in small_integer_coeffs(degree, bound):
        stats["polys_tested"] += 1
        score = score_candidate(fields, target, coeffs)
        if score.exact_fields == len(fields) and score.total_zeros == 0:
            exact.append(score)
        insert_best(best, score, top)
    exact.sort(key=score_key, reverse=True)
    print(f"{target}_degree{degree}_bound{bound}:")
    print(f"  polys_tested = {stats['polys_tested']}")
    print(f"  exact_all_fields = {len(exact)}")
    print(f"  best_count = {len(best)}")
    print(f"{target}_degree{degree}_bound{bound}_best:")
    for score in best[:top]:
        print_candidate("best", score)
    print(f"{target}_degree{degree}_bound{bound}_exact:")
    for score in exact[:top]:
        print_candidate("exact", score)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--degrees", default="3,4")
    parser.add_argument("--bound", type=int, default=8)
    parser.add_argument("--targets", default="d3,d4")
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    primes = parse_ints(args.small_primes)
    degrees = parse_ints(args.degrees)
    targets = [part.strip() for part in args.targets.split(",") if part.strip()]
    fields, stats = collect_fields(primes)

    print("p27 Kummer-line small-integer polynomial probe")
    print("K = x([2]P) on E': V^2=U^3+4U")
    print(f"small_primes = {args.small_primes}")
    print(f"degrees = {args.degrees}")
    print(f"bound = {args.bound}")
    print_field_summary(fields)
    print("setup_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    for target in targets:
        if target not in {"d3", "d4"}:
            raise ValueError(f"unknown target {target}")
        for degree in degrees:
            run_screen(fields, target, degree, args.bound, args.top)

    print("p27_kummer_small_integer_poly_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Line/two-line screens after quotienting E by the (0,0) torsion.

The p27 [8]-kernel probe showed that the quotient d3/d4 bits are invariant
under translation by (0,0) whenever the translated point remains in the
compactD domain.  The quotient by <(0,0)> has coordinates

    U = X - 1/X
    V = W*(X^2 + 1)/X^2
    V^2 = U^3 + 4U.

Lines on this 2-isogenous quotient are T0-invariant rational functions on the
original residual E, so they were not covered by the earlier visible line
screen in X,W.  This probe tests whether d3/d4 become simple line or two-line
characters after that quotient.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import P, inv
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import (
    QuotientRow,
    p27_rows,
    quotient_bit_rows_from_candidates,
)
from p27_reverse_source_quotient_probe import (
    score_lines_all_projective,
    score_lines_small_coeff,
)
from p27_equotient_line_product_probe import (
    build_line_signatures,
    pair_count_for_xor,
    sample_pairs,
    target_mask,
)


def quotient_point(row: QuotientRow, p: int) -> QuotientRow | None:
    x = row.x % p
    if x == 0:
        return None
    x2 = x * x % p
    u = (x - inv(x, p)) % p
    v = row.w * (x2 + 1) % p * inv(x2, p) % p
    if v * v % p != (u * u % p * u + 4 * u) % p:
        raise ValueError("2-isogeny quotient equation mismatch")
    return QuotientRow(x=u, w=v, target=row.target)


def quotient_rows(rows: list[QuotientRow], p: int) -> tuple[list[QuotientRow], Counter]:
    out: list[QuotientRow] = []
    stats: Counter = Counter()
    by_uv: dict[tuple[int, int], int] = {}
    for row in rows:
        qrow = quotient_point(row, p)
        if qrow is None:
            stats["x_zero_skip"] += 1
            continue
        key = (qrow.x, qrow.w)
        prior = by_uv.get(key)
        if prior is not None and prior != qrow.target:
            stats["mixed_after_quotient"] += 1
            continue
        by_uv[key] = qrow.target
    for (u, v), target in by_uv.items():
        out.append(QuotientRow(x=u, w=v, target=target))
    stats["input_rows"] = len(rows)
    stats["quotient_rows"] = len(out)
    stats["plus"] = sum(1 for row in out if row.target == 1)
    stats["minus"] = sum(1 for row in out if row.target == -1)
    return out, stats


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
            f"polarity={polarity} line={a}+{b}*U+{c}*V"
        )


def run_line_product(label: str, rows: list[QuotientRow], p: int, pair_limit: int) -> None:
    print(f"{label}_line_product:")
    print(f"  rows = {len(rows)}")
    if not rows:
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
    print(f"{label}_best_one_lines_from_product_pass:")
    for good, neg_mismatches, polarity, line in best:
        rate = good / len(rows)
        print(
            f"  good={good}/{len(rows)} rate={rate:.9f} "
            f"mismatches={-neg_mismatches} polarity={polarity} "
            f"line={line[0]}+{line[1]}*U+{line[2]}*V"
        )
    for name, desired in [("plus", target), ("minus", target ^ full)]:
        samples = sample_pairs(first, desired, pair_limit)
        if samples:
            print(f"{label}_exact_two_line_samples_polarity_{name}:")
            for left, right in samples:
                print(
                    "  "
                    f"({left[0]}+{left[1]}*U+{left[2]}*V) * "
                    f"({right[0]}+{right[1]}*U+{right[2]}*V)"
                )


def run_dataset(label: str, d3_rows: list[QuotientRow], d4_rows: list[QuotientRow], p: int, line_bound: int, exhaustive: bool, pair_limit: int) -> None:
    print(f"{label}:")
    qd3, d3_stats = quotient_rows(d3_rows, p)
    qd4, d4_stats = quotient_rows(d4_rows, p)
    print_counter(f"{label}_d3_2isogeny_stats", d3_stats)
    print_counter(f"{label}_d4_2isogeny_stats", d4_stats)
    if exhaustive:
        d3_line_stats, d3_line_rows = score_lines_all_projective(qd3, p)
        d4_line_stats, d4_line_rows = score_lines_all_projective(qd4, p)
    else:
        d3_line_stats, d3_line_rows = score_lines_small_coeff(qd3, p, line_bound)
        d4_line_stats, d4_line_rows = score_lines_small_coeff(qd4, p, line_bound)
    print_line_results(f"{label}_d3_line_screen", d3_line_stats, d3_line_rows)
    print_line_results(f"{label}_d4_line_screen", d4_line_stats, d4_line_rows)
    if exhaustive:
        run_line_product(f"{label}_d3", qd3, p, pair_limit)
        run_line_product(f"{label}_d4", qd4, p, pair_limit)


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1087,1471,1607")
    parser.add_argument("--p27-target", type=int, default=5000)
    parser.add_argument("--p27-heldout-target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--p27-line-bound", type=int, default=2)
    parser.add_argument("--pair-limit", type=int, default=4)
    args = parser.parse_args()

    print("p27 E-quotient 2-isogeny line probe")
    print("quotient_curve = V^2 = U^3 + 4U")
    print(f"small_primes = {args.small_primes}")

    d3_train, d4_train, train_stats = p27_rows(args.p27_target, args.seed, args.max_draws)
    print_counter("p27_train_original_quotient_stats", train_stats)
    run_dataset("p27_train", d3_train, d4_train, P, args.p27_line_bound, False, args.pair_limit)

    d3_hold, d4_hold, hold_stats = p27_rows(args.p27_heldout_target, args.heldout_seed, args.max_draws)
    print_counter("p27_heldout_original_quotient_stats", hold_stats)
    run_dataset("p27_heldout", d3_hold, d4_hold, P, args.p27_line_bound, False, args.pair_limit)

    print("small_prime_2isogeny_screens:")
    for prime in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{k}": v for k, v in enum_stats.items()}))
        print_counter("  quotient_stats", qstats)
        run_dataset(f"q{prime}", d3_rows, d4_rows, prime, args.p27_line_bound, True, args.pair_limit)

    print("p27_equotient_2isogeny_line_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

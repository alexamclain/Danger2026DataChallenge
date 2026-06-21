#!/usr/bin/env python3
"""Sparse branch-factor screen on the p27 2-isogenous quotient E'.

The p26 scratch work left a useful structural breadcrumb: after quotienting by
the rational (0,0) translation, the relevant first-w cover looked like a genus-4
double cover over

    E': V^2 = U^3 + 4U

with branch-degree 6.  This p27 probe asks the closest transfer question:
do the descended d3/d4 bits come from a sparse product of the same visible
E' branch factors and nearby tangent/vertical factors?

This is not a broad coefficient fit.  It is an exact GF(2) character-span
screen for named factors, with sparse products up to a small size.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_label2_alpha_branch_recurrence_probe import P, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import QuotientRow, p27_rows, quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows


@dataclass(frozen=True)
class FeatureSig:
    name: str
    sign_mask: int
    zero_mask: int


@dataclass(frozen=True)
class ComboScore:
    good: int
    nonzero: int
    zeros: int
    polarity: int
    names: tuple[str, ...]
    sign_mask: int
    zero_mask: int


def bit_count(value: int) -> int:
    return bin(value).count("1")


def target_mask(rows: list[QuotientRow]) -> int:
    mask = 0
    for i, row in enumerate(rows):
        if row.target == -1:
            mask |= 1 << i
    return mask


def addmod_expr(value: int, p: int) -> int:
    return value % p


def named_feature_functions() -> list[tuple[str, Callable[[int, int, int], int]]]:
    features: list[tuple[str, Callable[[int, int, int], int]]] = []

    def add(name: str, fn: Callable[[int, int, int], int]) -> None:
        features.append((name, fn))

    add("U", lambda u, v, p: u)
    add("V", lambda u, v, p: v)
    for c in [-4, -2, -1, 1, 2, 4]:
        add(f"U{c:+d}", lambda u, v, p, c=c: u + c)
    add("U2+4", lambda u, v, p: u * u + 4)
    add("U2-4", lambda u, v, p: u * u - 4)
    add("U2+1", lambda u, v, p: u * u + 1)
    add("U2-1", lambda u, v, p: u * u - 1)
    add("U2+2U+4", lambda u, v, p: u * u + 2 * u + 4)
    add("U2-2U+4", lambda u, v, p: u * u - 2 * u + 4)

    # Tangent/near-tangent branch lines suggested by the p26 quotient branch
    # packet.  The line V+2U vanishes at (2,-4), and V-2U at (2,4).
    for a in [-4, -2, -1, 0, 1, 2, 4]:
        for b in [-4, -2, -1, 0, 1, 2, 4]:
            if a == 0 and b == 0:
                continue
            label = f"V{a:+d}U{b:+d}" if b else f"V{a:+d}U"
            add(label, lambda u, v, p, a=a, b=b: v + a * u + b)

    # A few low-degree rational branch packets from the same visible geometry.
    add("branch_core_(U+2)(U2+4)", lambda u, v, p: (u + 2) * (u * u + 4))
    add("branch_core_(U-2)(U2+4)", lambda u, v, p: (u - 2) * (u * u + 4))
    add("tangent_pair_(V+2U)(V-2U)", lambda u, v, p: (v + 2 * u) * (v - 2 * u))
    add("p26_branch_packet_minus", lambda u, v, p: (u + 2) * (u * u + 4) * (v + 2 * u))
    add("p26_branch_packet_plus", lambda u, v, p: (u + 2) * (u * u + 4) * (v - 2 * u))
    return features


def feature_signature(
    rows: list[QuotientRow],
    p: int,
    name: str,
    fn: Callable[[int, int, int], int],
) -> FeatureSig:
    sign_mask = 0
    zero_mask = 0
    for i, row in enumerate(rows):
        chi = legendre(addmod_expr(fn(row.x, row.w, p), p), p)
        if chi == 0:
            zero_mask |= 1 << i
        elif chi == -1:
            sign_mask |= 1 << i
    return FeatureSig(name=name, sign_mask=sign_mask, zero_mask=zero_mask)


def build_features(rows: list[QuotientRow], p: int) -> list[FeatureSig]:
    seen: set[tuple[int, int]] = set()
    out: list[FeatureSig] = []
    for name, fn in named_feature_functions():
        sig = feature_signature(rows, p, name, fn)
        key = (sig.sign_mask, sig.zero_mask)
        if key in seen:
            continue
        seen.add(key)
        out.append(sig)
    return out


def score_combo(
    combo: tuple[FeatureSig, ...],
    rows: list[QuotientRow],
    target: int,
) -> ComboScore:
    sign_mask = 0
    zero_mask = 0
    for feature in combo:
        sign_mask ^= feature.sign_mask
        zero_mask |= feature.zero_mask
    full = (1 << len(rows)) - 1
    usable = full ^ zero_mask
    mismatches = bit_count((sign_mask ^ target) & usable)
    nonzero = bit_count(usable)
    good_plus = nonzero - mismatches
    good_minus = mismatches
    if good_plus >= good_minus:
        return ComboScore(
            good=good_plus,
            nonzero=nonzero,
            zeros=bit_count(zero_mask),
            polarity=1,
            names=tuple(feature.name for feature in combo),
            sign_mask=sign_mask,
            zero_mask=zero_mask,
        )
    return ComboScore(
        good=good_minus,
        nonzero=nonzero,
        zeros=bit_count(zero_mask),
        polarity=-1,
        names=tuple(feature.name for feature in combo),
        sign_mask=sign_mask,
        zero_mask=zero_mask,
    )


def sparse_screen(
    rows: list[QuotientRow],
    p: int,
    max_size: int,
    top: int,
) -> tuple[Counter, list[ComboScore], list[ComboScore]]:
    features = build_features(rows, p)
    target = target_mask(rows)
    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["features"] = len(features)
    stats["max_size"] = max_size
    stats["target_plus"] = sum(1 for row in rows if row.target == 1)
    stats["target_minus"] = sum(1 for row in rows if row.target == -1)

    best: list[ComboScore] = []
    exact: list[ComboScore] = []
    for size in range(1, max_size + 1):
        for combo in itertools.combinations(features, size):
            stats[f"combos_size_{size}"] += 1
            score = score_combo(combo, rows, target)
            best.append(score)
            if score.zeros == 0 and score.good == len(rows):
                exact.append(score)

    best.sort(
        key=lambda item: (
            item.good,
            item.nonzero,
            -item.zeros,
            -len(item.names),
            item.names,
        ),
        reverse=True,
    )
    exact.sort(key=lambda item: (len(item.names), item.names))
    stats["combos_tested"] = sum(stats[f"combos_size_{size}"] for size in range(1, max_size + 1))
    stats["exact_combos"] = len(exact)
    stats["best_good"] = best[0].good if best else 0
    stats["best_nonzero"] = best[0].nonzero if best else 0
    stats["best_zeros"] = best[0].zeros if best else 0
    return stats, best[:top], exact[:top]


def evaluate_combos(
    rows: list[QuotientRow],
    p: int,
    names_list: list[tuple[str, ...]],
) -> list[ComboScore]:
    by_name = {sig.name: sig for sig in build_features(rows, p)}
    target = target_mask(rows)
    out: list[ComboScore] = []
    for names in names_list:
        try:
            combo = tuple(by_name[name] for name in names)
        except KeyError:
            continue
        out.append(score_combo(combo, rows, target))
    out.sort(key=lambda item: (item.good, item.nonzero, -item.zeros), reverse=True)
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(prefix: str, scores: list[ComboScore], total: int) -> None:
    print(f"{prefix}:")
    for score in scores:
        rate = score.good / score.nonzero if score.nonzero else 0.0
        total_rate = score.good / total if total else 0.0
        expr = " * ".join(score.names)
        print(
            f"  good={score.good}/{score.nonzero} rate={rate:.9f} "
            f"total_rate={total_rate:.9f} zeros={score.zeros} "
            f"polarity={score.polarity} size={len(score.names)} expr={expr}"
        )


def to_eprime(d3_rows: list[QuotientRow], d4_rows: list[QuotientRow], p: int) -> tuple[list[QuotientRow], list[QuotientRow], Counter]:
    qd3, d3_stats = quotient_rows(d3_rows, p)
    qd4, d4_stats = quotient_rows(d4_rows, p)
    stats: Counter = Counter()
    stats.update({f"d3_{key}": value for key, value in d3_stats.items()})
    stats.update({f"d4_{key}": value for key, value in d4_stats.items()})
    return qd3, qd4, stats


def run_family(
    label: str,
    rows: list[QuotientRow],
    heldout_rows: list[QuotientRow] | None,
    p: int,
    max_size: int,
    top: int,
) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    stats, best, exact = sparse_screen(rows, p, max_size, top)
    print_counter(f"{label}_span_stats", stats)
    print_scores(f"{label}_best", best, len(rows))
    print_scores(f"{label}_exact", exact, len(rows))
    if heldout_rows is not None:
        selected = [score.names for score in (exact if exact else best)]
        heldout = evaluate_combos(heldout_rows, p, selected)
        print_scores(f"{label}_heldout_eval", heldout, len(heldout_rows))


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=2000)
    parser.add_argument("--heldout-target", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=500000)
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--max-size", type=int, default=4)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    print("p27 E-prime sparse branch-factor span probe")
    print("Eprime = V^2 = U^3 + 4U")
    print("family = p26 branch/H90 visible factors plus nearby tangent lines")
    print(f"max_size = {args.max_size}")

    d3_train, d4_train, train_stats = p27_rows(args.target, args.seed, args.max_draws)
    d3_hold, d4_hold, heldout_stats = p27_rows(args.heldout_target, args.heldout_seed, args.max_draws)
    qd3_train, qd4_train, qtrain_stats = to_eprime(d3_train, d4_train, P)
    qd3_hold, qd4_hold, qhold_stats = to_eprime(d3_hold, d4_hold, P)
    print_counter("p27_train_original_stats", train_stats)
    print_counter("p27_train_eprime_stats", qtrain_stats)
    print_counter("p27_heldout_original_stats", heldout_stats)
    print_counter("p27_heldout_eprime_stats", qhold_stats)
    run_family("p27_eprime_d3", qd3_train, qd3_hold, P, args.max_size, args.top)
    run_family("p27_eprime_d4", qd4_train, qd4_hold, P, args.max_size, args.top)

    print("small_prime_eprime_branch_factor_screens:")
    for prime in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(prime)
        d3_rows, d4_rows, source_stats = quotient_bit_rows_from_candidates(candidates, prime)
        qd3, qd4, qstats = to_eprime(d3_rows, d4_rows, prime)
        print(f"q={prime}:")
        print_counter("  enum_stats", Counter({f"enum_{key}": value for key, value in enum_stats.items()}))
        print_counter("  original_quotient_stats", source_stats)
        print_counter("  eprime_stats", qstats)
        run_family(f"q{prime}_eprime_d3", qd3, None, prime, args.max_size, args.top)
        run_family(f"q{prime}_eprime_d4", qd4, None, prime, args.max_size, args.top)

    print("p27_eprime_branch_factor_span_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify the p27 selected K/A polynomial as a d3 classifier."""

from __future__ import annotations

import argparse
from collections import Counter

from p27_kline_reverse_z_relation_probe import dedupe_candidates, ks_coordinates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates


def formula_k(k: int, A: int, p: int) -> int:
    k %= p
    A %= p
    k2 = k * k % p
    k4 = k2 * k2 % p
    a2 = A * A % p
    a3 = a2 * A % p
    a4 = a2 * a2 % p
    return (
        -a4
        + 8 * a3
        - 24 * a2
        + 32 * A
        - 16
        + (192 * a3 + 3712 * a2 + 15616 * A + 17920) * k2
        + (64 * a3 - 128 * a2 - 256 * A + 512) * k4
    ) % p


def formula_s(s: int, A: int, p: int) -> int:
    return formula_k(s * s % p, A, p)


def classify_candidates(candidates: list[dict[str, int]], p: int) -> Counter:
    stats: Counter = Counter()
    for cand in dedupe_candidates(candidates):
        stats["candidates"] += 1
        ks = ks_coordinates(cand, p)
        if ks is None:
            stats["ks_degenerate"] += 1
            continue
        k, s = ks
        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        d2, x6s = halve_all(A, x5, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        stats["d2_plus"] += 1
        classes = [legendre(x6, p) for x6 in x6s]
        vals = {value for value in classes if value in (-1, 1)}
        if vals == {1}:
            label = "d3_plus"
        elif vals == {-1}:
            label = "d3_minus"
        else:
            label = "d3_mixed_or_degenerate"
        stats[label] += 1
        k_zero = formula_k(k, A, p) == 0
        s_zero = formula_s(s, A, p) == 0
        stats[f"{label}_K_zero_{int(k_zero)}"] += 1
        stats[f"{label}_S_zero_{int(s_zero)}"] += 1
        if k_zero != s_zero:
            stats["K_S_formula_disagree"] += 1
        if (label == "d3_plus") != k_zero:
            stats["K_classifier_mismatch"] += 1
        if (label == "d3_plus") != s_zero:
            stats["S_classifier_mismatch"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=1000)
    parser.add_argument("--p27-heldout-target", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=500000)
    args = parser.parse_args()

    print("p27 K-line A-map formula verifier")
    print("formula: P(K,A)=0 with degree 4 in K and A")
    print("question: does P(K,A)=0 classify d3-plus among d2-plus candidates?")

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats)
        print_counter("p27_train_formula_stats", classify_candidates(candidates, P))

    if args.p27_heldout_target:
        candidates, sample_stats = p27_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats)
        print_counter("p27_heldout_formula_stats", classify_candidates(candidates, P))

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print(f"q={q}:")
        print_counter(f"q{q}_enum_stats", enum_stats)
        print_counter(f"q{q}_formula_stats", classify_candidates(candidates, q))

    print("p27_kline_a_map_formula_verify_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

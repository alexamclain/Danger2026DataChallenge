#!/usr/bin/env python3
"""B-source identity and descent probe for p27.

The B-parameter base curve was introduced by rationalizing A+2.  In the
residual label-2 source it has a direct meaning:

    A + 2 = (8 X^2 / (X^2 - 1)^2)^2.

This probe verifies that identity on actual legal rows, checks the corresponding
K/A branch equations, and asks how far the next gate descends: to B alone, to
(B,K), to (B,Sroot), or only to finer source data.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Iterable

from p27_kline_base_param_sampler_probe import ParamRow, atom_bit
from p27_kline_reverse_z_relation_probe import dedupe_candidates, ks_coordinates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import CandidateBits, candidate_bits, normalize


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def source_b_plus(X: int, p: int) -> int | None:
    den = (X * X - 1) % p
    if den == 0:
        return None
    return 8 * X * X % p * inv(den * den, p) % p


def branch_l(B: int, branch: int, p: int) -> int | None:
    B %= p
    if B in (0, 2, p - 2):
        return None
    if branch == 0:
        den = 8 * B * (B - 2) * (B - 2)
        return (-pow(B + 2, 4, p) * inv(den, p)) % p
    if branch == 1:
        den = 8 * B * (B + 2) * (B + 2)
        return (pow(B - 2, 4, p) * inv(den, p)) % p
    raise ValueError(branch)


def normalized_bits_for_group(candidates: Iterable[dict[str, int]], p: int) -> tuple[CandidateBits, Counter]:
    stats: Counter = Counter()
    d3_values: list[int | None] = []
    d4_values: list[int | None] = []
    for cand in candidates:
        bits = candidate_bits(cand, p)
        d3_values.append(bits.d3)
        if bits.d3 == 1:
            d4_values.append(bits.d4)
    d3 = normalize(d3_values)
    d4 = normalize(d4_values) if d3 == 1 else None
    if d3 == 0:
        stats["d3_mixed_candidate_group"] += 1
    if d4 == 0:
        stats["d4_mixed_candidate_group"] += 1
    return CandidateBits(d3=d3, d4=d4), stats


def pm_label(value: int | None) -> str:
    if value == 1:
        return "plus"
    if value == -1:
        return "minus"
    if value == 0:
        return "mixed"
    return "missing"


def summarize_descent(
    label: str,
    groups: defaultdict[object, list[CandidateBits]],
    stats: Counter,
) -> None:
    d3_summary: Counter = Counter()
    d4_summary: Counter = Counter()
    size_hist: Counter = Counter()
    for values in groups.values():
        size_hist[len(values)] += 1
        d3 = normalize(bits.d3 for bits in values)
        d3_summary[pm_label(d3)] += 1
        if d3 == 1:
            d4 = normalize(bits.d4 for bits in values)
            d4_summary[pm_label(d4)] += 1
    stats[f"{label}_groups"] = len(groups)
    for key, value in d3_summary.items():
        stats[f"{label}_d3_{key}_groups"] = value
    for key, value in d4_summary.items():
        stats[f"{label}_d4_{key}_groups"] = value
    for key, value in size_hist.items():
        stats[f"{label}_size_{key}"] = value


def row_core_ok(row: ParamRow, p: int) -> bool:
    return (
        atom_bit("K", row, p) == 0
        and atom_bit("B+2", row, p) == 0
        and atom_bit("B-2", row, p) == 1
        and atom_bit("L", row, p) == 0
    )


def analyze_candidates(label: str, candidates: list[dict[str, int]], p: int) -> Counter:
    stats: Counter = Counter()
    seen: dict[tuple[int, int, int, int, int], dict[str, int]] = {}
    for cand in dedupe_candidates(candidates):
        key = (
            int(cand["X"]) % p,
            int(cand["W"]) % p,
            int(cand["T"]) % p,
            int(cand["A"]) % p,
            int(cand["x5"]) % p,
        )
        seen[key] = cand

    groups: dict[str, defaultdict[object, list[CandidateBits]]] = {
        name: defaultdict(list)
        for name in [
            "X",
            "XW",
            "Bplus",
            "Bbranch",
            "BK",
            "BS",
            "BKS",
            "KA",
            "SA",
        ]
    }

    for cand in seen.values():
        stats["deduped_candidates"] += 1
        X = int(cand["X"]) % p
        W = int(cand["W"]) % p
        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        d2, _ = halve_all(A, x5, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        stats["d2_plus_candidates"] += 1
        ks = ks_coordinates(cand, p)
        if ks is None:
            stats["ks_degenerate"] += 1
            continue
        K, S = ks
        b_plus = source_b_plus(X, p)
        if b_plus is None:
            stats["b_degenerate"] += 1
            continue
        b_minus = (-b_plus) % p
        if (b_plus * b_plus - (A + 2)) % p:
            stats["A_plus_2_identity_mismatch"] += 1
        L = K * K % p
        if branch_l(b_plus, 1, p) != L:
            stats["Bplus_branch1_L_mismatch"] += 1
        if branch_l(b_minus, 0, p) != L:
            stats["Bminus_branch0_L_mismatch"] += 1

        plus_row = ParamRow(K=K, A=A, B=b_plus, L=L, branch=1)
        minus_row = ParamRow(K=K, A=A, B=b_minus, L=L, branch=0)
        if not row_core_ok(plus_row, p):
            stats["Bplus_core_miss"] += 1
        if not row_core_ok(minus_row, p):
            stats["Bminus_core_miss"] += 1

        bits = candidate_bits(cand, p)
        groups["X"][X].append(bits)
        groups["XW"][(X, W)].append(bits)
        groups["Bplus"][b_plus].append(bits)
        groups["Bbranch"][(b_plus, 1)].append(bits)
        groups["Bbranch"][(b_minus, 0)].append(bits)
        groups["BK"][(b_plus, K)].append(bits)
        groups["BK"][(b_minus, K)].append(bits)
        groups["BS"][(b_plus, S)].append(bits)
        groups["BS"][(b_minus, S)].append(bits)
        groups["BKS"][(b_plus, K, S)].append(bits)
        groups["BKS"][(b_minus, K, S)].append(bits)
        groups["KA"][(K, A)].append(bits)
        groups["SA"][(S, A)].append(bits)

    for group_label, group in groups.items():
        summarize_descent(group_label, group, stats)
    print_counter(f"{label}_b_source_descent_stats", stats)
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def symbolic_identities() -> None:
    print("symbolic_identities:")
    print("  A = -2*(X^8 - 4X^6 - 26X^4 - 4X^2 + 1)/(X^2 - 1)^4")
    print("  A + 2 = (8*X^2/(X^2 - 1)^2)^2")
    print("  Bplus = 8*X^2/(X^2 - 1)^2")
    print("  Bplus + 2 = 2*(X^2 + 1)^2/(X^2 - 1)^2")
    print("  Bplus - 2 = -2*(X^2 - 2X - 1)*(X^2 + 2X - 1)/(X^2 - 1)^2")
    print("  K = (X^4 - 6X^2 + 1)^2/(4*X*(X^2 - 1)*(X^2 + 1)^2)")
    print("  Bplus uses K/A branch1; -Bplus uses branch0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=6000)
    parser.add_argument("--p27-heldout-target", type=int, default=6000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1500000)
    args = parser.parse_args()

    print("p27 B-source identity/descent probe")
    symbolic_identities()

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats)
        analyze_candidates("p27_train", candidates, P)

    if args.p27_heldout_target:
        candidates, sample_stats = p27_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats)
        analyze_candidates("p27_heldout", candidates, P)

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print_counter(f"q{q}_enum_stats", enum_stats)
        analyze_candidates(f"q{q}", candidates, q)

    print("p27_b_source_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

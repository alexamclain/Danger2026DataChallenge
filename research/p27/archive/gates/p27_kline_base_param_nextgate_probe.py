#!/usr/bin/env python3
"""Next-gate screen inside the p27 B-parameter legal bucket.

The B-parameter base probe found an all-recall bucket that separates the sparse
legal d2 subset from the full K/A base curve by about 8x.  This probe tests the
harder moonshot question: after conditioning on actual legal d2 rows, do the
same B-parameter squareclasses predict d3 or d4?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
from typing import Iterable

from p27_kline_base_param_sampler_probe import ATOM_NAMES, ParamRow, atom_bit, inv
from p27_kline_reverse_z_relation_probe import dedupe_candidates, ks_coordinates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod
from p27_reverse_source_d4_recurrence_probe import CandidateBits, candidate_bits, normalize


CORE_BUCKET = {
    "K": 0,
    "B+2": 0,
    "B-2": 1,
    "L": 0,
}


def param_rows_for_ka(K: int, A: int, p: int) -> list[ParamRow]:
    """Return B-parameter rows above one realized (K,A)."""

    out: set[ParamRow] = set()
    K %= p
    A %= p
    target_L = K * K % p
    for B in roots_mod((A + 2) % p, p):
        if B % p in (0, 2, p - 2):
            continue
        den0 = 8 * B * (B - 2) * (B - 2)
        den1 = 8 * B * (B + 2) * (B + 2)
        L0 = (-pow(B + 2, 4, p) * inv(den0, p)) % p
        L1 = (pow(B - 2, 4, p) * inv(den1, p)) % p
        for branch, L in [(0, L0), (1, L1)]:
            if L == target_L:
                out.add(ParamRow(K, A, B % p, L, branch))
    return sorted(out)


def signature(row: ParamRow, p: int) -> tuple[int, ...] | None:
    bits: list[int] = []
    for name in ATOM_NAMES:
        bit = atom_bit(name, row, p)
        if bit is None:
            return None
        bits.append(bit)
    return tuple(bits)


def in_core_bucket(row: ParamRow, p: int) -> bool:
    for name, expected in CORE_BUCKET.items():
        bit = atom_bit(name, row, p)
        if bit != expected:
            return False
    return True


def normalized_bits_for_ka(candidates: Iterable[dict[str, int]], p: int) -> tuple[CandidateBits, Counter]:
    stats: Counter = Counter()
    d3_values: list[int | None] = []
    d4_values: list[int | None] = []
    for cand in candidates:
        bits = candidate_bits(cand, p)
        d3_values.append(bits.d3)
        if bits.d3 == 1:
            d4_values.append(bits.d4)
    d3 = normalize(d3_values)
    if d3 == 1:
        d4 = normalize(d4_values)
    else:
        d4 = None
    if d3 == 0:
        stats["d3_mixed_on_KA"] += 1
    if d4 == 0:
        stats["d4_mixed_on_KA"] += 1
    return CandidateBits(d3=d3, d4=d4), stats


def legal_param_rows(candidates: list[dict[str, int]], p: int) -> tuple[list[tuple[ParamRow, CandidateBits]], Counter]:
    stats: Counter = Counter()
    by_ka: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for cand in dedupe_candidates(candidates):
        stats["deduped_candidates"] += 1
        K_S = ks_coordinates(cand, p)
        if K_S is None:
            stats["ks_degenerate"] += 1
            continue
        K, _S = K_S
        A = int(cand["A"]) % p
        d2, _x6s = halve_all(A, int(cand["x5"]) % p, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        by_ka[(K, A)].append(cand)

    rows: list[tuple[ParamRow, CandidateBits]] = []
    for (K, A), group in by_ka.items():
        bits, bit_stats = normalized_bits_for_ka(group, p)
        stats.update(bit_stats)
        stats["legal_KA"] += 1
        stats[f"group_size_{len(group)}"] += 1
        if bits.d3 == 1:
            stats["d3_plus_KA"] += 1
        elif bits.d3 == -1:
            stats["d3_minus_KA"] += 1
        elif bits.d3 is None:
            stats["d3_missing_KA"] += 1
        else:
            stats["d3_mixed_KA"] += 1
        if bits.d4 == 1:
            stats["d4_plus_after_d3_KA"] += 1
        elif bits.d4 == -1:
            stats["d4_minus_after_d3_KA"] += 1
        elif bits.d3 == 1:
            stats["d4_missing_after_d3_KA"] += 1

        param_rows = param_rows_for_ka(K, A, p)
        stats[f"param_rows_per_KA_{len(param_rows)}"] += 1
        if not param_rows:
            stats["missing_param_rows"] += 1
            continue
        for row in param_rows:
            stats["param_rows"] += 1
            if in_core_bucket(row, p):
                stats["core_bucket_rows"] += 1
            else:
                stats["core_bucket_misses"] += 1
            rows.append((row, bits))
    return rows, stats


def scored_rows(rows: list[tuple[ParamRow, CandidateBits]], p: int, target_name: str) -> tuple[list[tuple[tuple[int, ...], int]], Counter]:
    scored: list[tuple[tuple[int, ...], int]] = []
    stats: Counter = Counter()
    for row, bits in rows:
        target = getattr(bits, target_name)
        if target not in (-1, 1):
            stats["target_missing"] += 1
            continue
        sig = signature(row, p)
        if sig is None:
            stats["zero_atom_skip"] += 1
            continue
        label = 0 if target == 1 else 1
        scored.append((sig, label))
    stats["scored_rows"] = len(scored)
    stats["plus_rows"] = sum(1 for _, label in scored if label == 0)
    stats["minus_rows"] = sum(1 for _, label in scored if label == 1)
    return scored, stats


def best_parity_combos(scored: list[tuple[tuple[int, ...], int]], max_weight: int, top: int) -> list[tuple[int, int, int, tuple[str, ...]]]:
    out: list[tuple[int, int, int, tuple[str, ...]]] = []
    indices = range(len(ATOM_NAMES))
    for weight in range(max_weight + 1):
        for combo in combinations(indices, weight):
            good_plus = 0
            good_minus = 0
            for sig, label in scored:
                bit = sum(sig[i] for i in combo) & 1
                good_plus += bit == label
                good_minus += (bit ^ 1) == label
            good = max(good_plus, good_minus)
            polarity = 1 if good_plus >= good_minus else -1
            out.append((good, polarity, weight, tuple(ATOM_NAMES[i] for i in combo)))
    out.sort(key=lambda item: (item[0], -item[2]), reverse=True)
    return out[:top]


def best_buckets(scored: list[tuple[tuple[int, ...], int]], max_weight: int, top: int, min_count: int) -> list[tuple[float, float, int, int, int, tuple[str, ...], tuple[int, ...]]]:
    total = len(scored)
    plus = sum(1 for _, label in scored if label == 0)
    baseline = plus / total if total else 0.0
    out: list[tuple[float, float, int, int, int, tuple[str, ...], tuple[int, ...]]] = []
    indices = range(len(ATOM_NAMES))
    for weight in range(1, max_weight + 1):
        for combo in combinations(indices, weight):
            buckets: defaultdict[tuple[int, ...], list[int]] = defaultdict(lambda: [0, 0])
            for sig, label in scored:
                key = tuple(sig[i] for i in combo)
                buckets[key][0] += 1
                if label == 0:
                    buckets[key][1] += 1
            for key, (count, hit) in buckets.items():
                if count < min_count:
                    continue
                best_hit = max(hit, count - hit)
                precision = best_hit / count
                majority = max(baseline, 1 - baseline)
                lift = precision / majority if majority else 0.0
                out.append((lift, precision, best_hit, count, len(combo), tuple(ATOM_NAMES[i] for i in combo), key))
    out.sort(key=lambda item: (item[0], item[2], -item[3]), reverse=True)
    return out[:top]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_score(label: str, scored: list[tuple[tuple[int, ...], int]], stats: Counter, max_weight: int, top: int, min_bucket: int) -> None:
    print_counter(f"{label}_stats", stats)
    total = stats["scored_rows"]
    plus = stats["plus_rows"]
    minus = stats["minus_rows"]
    plus_rate = plus / total if total else 0.0
    majority = max(plus, minus) / total if total else 0.0
    print(f"{label}_baseline:")
    print(f"  plus_rate = {plus_rate:.9f}")
    print(f"  majority_rate = {majority:.9f}")

    print(f"{label}_best_parity_combos:")
    for good, polarity, weight, combo in best_parity_combos(scored, max_weight, top):
        rate = good / total if total else 0.0
        lift = rate / majority if majority else 0.0
        print(
            f"  good={good}/{total} rate={rate:.9f} majority_lift={lift:.6f} "
            f"polarity={polarity} weight={weight} combo={' * '.join(combo) if combo else '1'}"
        )

    print(f"{label}_best_buckets_min_count_{min_bucket}:")
    for lift, precision, hit, count, weight, combo, key in best_buckets(scored, max_weight, top, min_bucket):
        bits = "".join(str(bit) for bit in key)
        print(
            f"  majority_lift={lift:.6f} precision={precision:.9f} "
            f"hits={hit}/{count} weight={weight} bits={bits} combo={' * '.join(combo)}"
        )


def run_candidates(label: str, candidates: list[dict[str, int]], p: int, max_weight: int, top: int, min_bucket: int) -> None:
    rows, stats = legal_param_rows(candidates, p)
    print_counter(f"{label}_legal_param_stats", stats)
    for target_name in ["d3", "d4"]:
        scored, score_stats = scored_rows(rows, p, target_name)
        print_score(f"{label}_{target_name}", scored, score_stats, max_weight, top, min_bucket)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=6000)
    parser.add_argument("--p27-heldout-target", type=int, default=6000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1500000)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-bucket", type=int, default=16)
    args = parser.parse_args()

    print("p27 B-parameter next-gate probe")
    print(f"atoms = {ATOM_NAMES}")
    print(f"core_bucket = {CORE_BUCKET}")

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats)
        run_candidates("p27_train", candidates, P, args.max_weight, args.top, args.min_bucket)

    if args.p27_heldout_target:
        candidates, sample_stats = p27_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats)
        run_candidates("p27_heldout", candidates, P, args.max_weight, args.top, args.min_bucket)

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print_counter(f"q{q}_enum_stats", enum_stats)
        run_candidates(f"q{q}", candidates, q, args.max_weight, args.top, args.min_bucket)

    print("p27_kline_base_param_nextgate_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

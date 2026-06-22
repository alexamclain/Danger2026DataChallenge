#!/usr/bin/env python3
"""B-parameter sampler screen for the p27 K/A base curve.

The K/A base curve rationalizes after adjoining B with A = B^2 - 2.  This
probe asks whether the sparse legal source subset becomes a simple branch or
squareclass bucket in the B-parameter coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
from typing import NamedTuple

from p27_kline_base_curve_sampler_probe import realized_ka
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import roots_mod


class ParamRow(NamedTuple):
    K: int
    A: int
    B: int
    L: int
    branch: int


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def enumerate_param_rows(p: int) -> list[ParamRow]:
    """Enumerate the B-rationalized K/A base curve rows.

    With A = B^2 - 2 and L = K^2, the two branches are:

      L = -(B + 2)^4 / (8 B (B - 2)^2)
      L =  (B - 2)^4 / (8 B (B + 2)^2)
    """

    rows: set[ParamRow] = set()
    for B in range(p):
        if B % p in (0, 2, p - 2):
            continue
        A = (B * B - 2) % p
        den0 = 8 * B * (B - 2) * (B - 2)
        den1 = 8 * B * (B + 2) * (B + 2)
        L0 = (-pow(B + 2, 4, p) * inv(den0, p)) % p
        L1 = (pow(B - 2, 4, p) * inv(den1, p)) % p
        for branch, L in [(0, L0), (1, L1)]:
            for K in roots_mod(L, p):
                rows.add(ParamRow(K % p, A, B, L, branch))
    return sorted(rows)


ATOM_NAMES = [
    "branch",
    "K",
    "K+1",
    "K-1",
    "K^2+4",
    "L",
    "L+1",
    "B",
    "B+1",
    "B-1",
    "B+2",
    "B-2",
    "B^2+1",
    "B^2-4",
    "A+2",
    "A-2",
    "A+6",
    "A+14",
    "3A+10",
    "A^2+60A+132",
]


def atom_bit(name: str, row: ParamRow, p: int) -> int | None:
    K, A, B, L, branch = row
    if name == "branch":
        return branch
    if name == "K":
        value = K
    elif name == "K+1":
        value = K + 1
    elif name == "K-1":
        value = K - 1
    elif name == "K^2+4":
        value = K * K + 4
    elif name == "L":
        value = L
    elif name == "L+1":
        value = L + 1
    elif name == "B":
        value = B
    elif name == "B+1":
        value = B + 1
    elif name == "B-1":
        value = B - 1
    elif name == "B+2":
        value = B + 2
    elif name == "B-2":
        value = B - 2
    elif name == "B^2+1":
        value = B * B + 1
    elif name == "B^2-4":
        value = B * B - 4
    elif name == "A+2":
        value = A + 2
    elif name == "A-2":
        value = A - 2
    elif name == "A+6":
        value = A + 6
    elif name == "A+14":
        value = A + 14
    elif name == "3A+10":
        value = 3 * A + 10
    elif name == "A^2+60A+132":
        value = A * A + 60 * A + 132
    else:
        raise ValueError(name)
    chi = legendre(value, p)
    if chi == 0:
        return None
    return 0 if chi == 1 else 1


def signature(row: ParamRow, p: int) -> tuple[int, ...] | None:
    bits: list[int] = []
    for name in ATOM_NAMES:
        bit = atom_bit(name, row, p)
        if bit is None:
            return None
        bits.append(bit)
    return tuple(bits)


def scored_rows(rows: list[ParamRow], target: set[tuple[int, int]], p: int) -> tuple[list[tuple[tuple[int, ...], int]], Counter]:
    out: list[tuple[tuple[int, ...], int]] = []
    stats: Counter = Counter()
    for row in rows:
        sig = signature(row, p)
        if sig is None:
            stats["zero_atom_skip"] += 1
            continue
        out.append((sig, 1 if (row.K, row.A) in target else 0))
    stats["scored_rows"] = len(out)
    stats["target_rows"] = sum(label for _, label in out)
    return out, stats


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
    positives = sum(label for _, label in scored)
    baseline = positives / total if total else 0.0
    out: list[tuple[float, float, int, int, int, tuple[str, ...], tuple[int, ...]]] = []
    indices = range(len(ATOM_NAMES))
    for weight in range(1, max_weight + 1):
        for combo in combinations(indices, weight):
            buckets: defaultdict[tuple[int, ...], list[int]] = defaultdict(lambda: [0, 0])
            for sig, label in scored:
                key = tuple(sig[i] for i in combo)
                buckets[key][0] += 1
                buckets[key][1] += label
            for key, (count, hit) in buckets.items():
                if count < min_count or hit == 0:
                    continue
                precision = hit / count
                lift = precision / baseline if baseline else 0.0
                out.append((lift, precision, hit, count, weight, tuple(ATOM_NAMES[i] for i in combo), key))
    out.sort(key=lambda item: (item[0], item[2], -item[3]), reverse=True)
    return out[:top]


def bucket_stats_for_combo(scored: list[tuple[tuple[int, ...], int]], combo: tuple[int, ...], min_count: int) -> list[tuple[float, float, float, int, int, tuple[int, ...]]]:
    total = len(scored)
    positives = sum(label for _, label in scored)
    baseline = positives / total if total else 0.0
    buckets: defaultdict[tuple[int, ...], list[int]] = defaultdict(lambda: [0, 0])
    for sig, label in scored:
        key = tuple(sig[i] for i in combo)
        buckets[key][0] += 1
        buckets[key][1] += label
    out: list[tuple[float, float, float, int, int, tuple[int, ...]]] = []
    for key, (count, hit) in buckets.items():
        if count < min_count or hit == 0:
            continue
        precision = hit / count
        recall = hit / positives if positives else 0.0
        lift = precision / baseline if baseline else 0.0
        out.append((lift, precision, recall, hit, count, key))
    out.sort(key=lambda item: (item[0], item[3], -item[4]), reverse=True)
    return out


def print_core_grid(prefix: str, scored: list[tuple[tuple[int, ...], int]], top: int, min_bucket: int) -> None:
    name_to_index = {name: index for index, name in enumerate(ATOM_NAMES)}
    core = ("K", "B+2", "B-2")
    extras = [name for name in ATOM_NAMES if name not in core and name != "branch"]
    rows: list[tuple[float, float, float, int, int, str, tuple[int, ...]]] = []
    for extra in extras:
        combo = tuple(name_to_index[name] for name in (*core, extra))
        best = bucket_stats_for_combo(scored, combo, min_bucket)
        if best:
            lift, precision, recall, hit, count, key = best[0]
            rows.append((lift, precision, recall, hit, count, extra, key))
    rows.sort(key=lambda item: (item[0], item[3], -item[4]), reverse=True)

    print(f"{prefix}_core_K_Bpm_best_buckets:")
    for lift, precision, recall, hit, count, extra, key in rows[:top]:
        bits = "".join(str(bit) for bit in key)
        print(
            f"  extra={extra} lift={lift:.6f} precision={precision:.9f} "
            f"recall={recall:.9f} hits={hit}/{count} bits={bits}"
        )

    print(f"{prefix}_core_K_Bpm_all_recall_buckets:")
    all_recall = [row for row in rows if row[2] >= 0.999999]
    all_recall.sort(key=lambda item: (item[0], -item[4]), reverse=True)
    for lift, precision, recall, hit, count, extra, key in all_recall[:top]:
        bits = "".join(str(bit) for bit in key)
        print(
            f"  extra={extra} lift={lift:.6f} precision={precision:.9f} "
            f"recall={recall:.9f} hits={hit}/{count} bits={bits}"
        )


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def branch_stats(rows: list[ParamRow], target: set[tuple[int, int]]) -> Counter:
    stats: Counter = Counter()
    by_ka: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for row in rows:
        stats["param_rows"] += 1
        stats[f"branch_{row.branch}_rows"] += 1
        if (row.K, row.A) in target:
            stats["target_rows"] += 1
            stats[f"branch_{row.branch}_target_rows"] += 1
        by_ka[(row.K, row.A)].add((row.B, row.branch))
    stats["unique_KA"] = len(by_ka)
    for fibers in by_ka.values():
        stats[f"param_rows_per_KA_{len(fibers)}"] += 1
    return stats


def print_scores(prefix: str, scored: list[tuple[tuple[int, ...], int]], max_weight: int, top: int, min_bucket: int) -> None:
    total = len(scored)
    positives = sum(label for _, label in scored)
    baseline = positives / total if total else 0.0
    print(f"{prefix}_baseline:")
    print(f"  total = {total}")
    print(f"  positives = {positives}")
    print(f"  positive_rate = {baseline:.9f}")

    print(f"{prefix}_best_parity_combos:")
    for good, polarity, weight, combo in best_parity_combos(scored, max_weight, top):
        rate = good / total if total else 0.0
        print(
            f"  good={good}/{total} rate={rate:.9f} polarity={polarity} "
            f"weight={weight} combo={' * '.join(combo) if combo else '1'}"
        )

    print(f"{prefix}_best_buckets_min_count_{min_bucket}:")
    for lift, precision, hit, count, weight, combo, key in best_buckets(scored, max_weight, top, min_bucket):
        recall = hit / positives if positives else 0.0
        bits = "".join(str(bit) for bit in key)
        print(
            f"  lift={lift:.6f} precision={precision:.9f} recall={recall:.9f} "
            f"hits={hit}/{count} weight={weight} bits={bits} "
            f"combo={' * '.join(combo)}"
        )

    print_core_grid(prefix, scored, top, min_bucket)


def run_field(p: int, max_weight: int, top: int, min_bucket: int) -> None:
    rows = enumerate_param_rows(p)
    unique_ka = {(row.K, row.A) for row in rows}
    realized_d2, realized_d3, source_stats = realized_ka(p)
    stats = Counter(source_stats)
    stats.update(branch_stats(rows, realized_d2))
    stats["unique_KA_in_d2"] = len(unique_ka & realized_d2)
    stats["unique_KA_missing_d2"] = len(realized_d2 - unique_ka)
    stats["unique_KA_in_d3plus"] = len(unique_ka & realized_d3)
    stats["unique_KA_missing_d3plus"] = len(realized_d3 - unique_ka)
    print_counter(f"q{p}_param_sampler_stats", stats)

    for label, target in [("d2", realized_d2), ("d3plus", realized_d3)]:
        scored, score_stats = scored_rows(rows, target, p)
        print_counter(f"q{p}_{label}_score_stats", score_stats)
        print_scores(f"q{p}_{label}", scored, max_weight, top, min_bucket)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--max-weight", type=int, default=5)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-bucket", type=int, default=12)
    args = parser.parse_args()

    print("p27 B-parameter base-curve sampler viability probe")
    print("A = B^2 - 2")
    print("branch0 L = -(B + 2)^4 / (8 B (B - 2)^2)")
    print("branch1 L =  (B - 2)^4 / (8 B (B + 2)^2)")
    print(f"atoms = {ATOM_NAMES}")
    for p in parse_ints(args.small_primes):
        run_field(p, args.max_weight, args.top, args.min_bucket)
    print("p27_kline_base_param_sampler_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

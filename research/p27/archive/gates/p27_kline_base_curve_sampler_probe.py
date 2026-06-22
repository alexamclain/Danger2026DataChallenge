#!/usr/bin/env python3
"""Sampler viability probe for the explicit p27 K/A base curve.

The K/A identity is necessary for all d2-plus legal candidates, but a useful
sampler would need the legal source to be a simple stratum of that base curve.
This probe enumerates the base curve over guard fields and compares it with
the actually realized label-2/compactD candidates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

from p27_kline_reverse_z_relation_probe import dedupe_candidates, ks_coordinates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def base_l_values(A: int, p: int) -> list[int]:
    """Solve the normalized K/A equation for L=K^2."""
    A %= p
    c2 = 64 * (A - 2) * (A - 2) % p * (A + 2) % p
    c1 = 64 * (A + 2) % p * (A + 14) % p * (3 * A + 10) % p
    c0 = -pow(A - 2, 4, p)
    if c2 == 0:
        if c1 == 0:
            return []
        return [(-c0 * inv(c1, p)) % p]
    disc = (c1 * c1 - 4 * c2 * c0) % p
    out: set[int] = set()
    for sd in roots_mod(disc, p):
        out.add(((-c1 + sd) * inv(2 * c2, p)) % p)
        out.add(((-c1 - sd) * inv(2 * c2, p)) % p)
    return sorted(out)


def enumerate_base_ka(p: int) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for A in range(p):
        for L in base_l_values(A, p):
            for K in roots_mod(L, p):
                out.add((K, A))
    return out


def realized_ka(p: int) -> tuple[set[tuple[int, int]], set[tuple[int, int]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    all_rows: set[tuple[int, int]] = set()
    d3_plus_rows: set[tuple[int, int]] = set()
    for cand in dedupe_candidates(candidates):
        ks = ks_coordinates(cand, p)
        if ks is None:
            stats["ks_degenerate"] += 1
            continue
        K, _S = ks
        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        d2, x6s = halve_all(A, x5, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        all_rows.add((K, A))
        classes = {legendre(x6, p) for x6 in x6s}
        if classes == {1}:
            d3_plus_rows.add((K, A))
    stats["realized_d2_KA"] = len(all_rows)
    stats["realized_d3plus_KA"] = len(d3_plus_rows)
    return all_rows, d3_plus_rows, stats


ATOM_NAMES = [
    "K",
    "K+1",
    "K-1",
    "K^2+4",
    "A+2",
    "A-2",
    "A+6",
    "A+14",
    "3A+10",
    "A^2+60A+132",
]


def atom_value(name: str, K: int, A: int, p: int) -> int:
    if name == "K":
        return K
    if name == "K+1":
        return K + 1
    if name == "K-1":
        return K - 1
    if name == "K^2+4":
        return K * K + 4
    if name == "A+2":
        return A + 2
    if name == "A-2":
        return A - 2
    if name == "A+6":
        return A + 6
    if name == "A+14":
        return A + 14
    if name == "3A+10":
        return 3 * A + 10
    if name == "A^2+60A+132":
        return A * A + 60 * A + 132
    raise ValueError(name)


def signature(point: tuple[int, int], p: int) -> tuple[int, ...] | None:
    K, A = point
    bits: list[int] = []
    for name in ATOM_NAMES:
        chi = legendre(atom_value(name, K, A, p), p)
        if chi == 0:
            return None
        bits.append(0 if chi == 1 else 1)
    return tuple(bits)


def best_atom_combos(base: set[tuple[int, int]], target: set[tuple[int, int]], p: int, max_weight: int, top: int) -> tuple[Counter, list[tuple[int, int, int, tuple[str, ...]]]]:
    rows: list[tuple[tuple[int, ...], int]] = []
    stats: Counter = Counter()
    for point in base:
        sig = signature(point, p)
        if sig is None:
            stats["zero_atom_skip"] += 1
            continue
        rows.append((sig, 1 if point in target else 0))
    stats["scored_rows"] = len(rows)
    stats["target_rows"] = sum(label for _, label in rows)
    scored: list[tuple[int, int, int, tuple[str, ...]]] = []
    indices = range(len(ATOM_NAMES))
    for weight in range(max_weight + 1):
        for combo in combinations(indices, weight):
            good_plus = 0
            good_minus = 0
            for sig, label in rows:
                bit = sum(sig[i] for i in combo) & 1
                good_plus += bit == label
                good_minus += (bit ^ 1) == label
            good = max(good_plus, good_minus)
            polarity = 1 if good_plus >= good_minus else -1
            scored.append((good, polarity, weight, tuple(ATOM_NAMES[i] for i in combo)))
    scored.sort(key=lambda item: (item[0], -item[2]), reverse=True)
    return stats, scored[:top]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(p: int, max_weight: int, top: int) -> None:
    base = enumerate_base_ka(p)
    realized_d2, realized_d3, stats = realized_ka(p)
    stats["base_KA"] = len(base)
    stats["realized_d2_in_base"] = len(realized_d2 & base)
    stats["realized_d2_missing_from_base"] = len(realized_d2 - base)
    stats["realized_d3plus_in_base"] = len(realized_d3 & base)
    stats["realized_d3plus_missing_from_base"] = len(realized_d3 - base)
    stats["base_realized_d2_fraction_ppm"] = int(1_000_000 * len(realized_d2 & base) / len(base)) if base else 0
    stats["base_realized_d3plus_fraction_ppm"] = int(1_000_000 * len(realized_d3 & base) / len(base)) if base else 0
    print_counter(f"q{p}_base_sampler_stats", stats)

    for label, target in [("d2", realized_d2 & base), ("d3plus", realized_d3 & base)]:
        score_stats, best = best_atom_combos(base, target, p, max_weight, top)
        print_counter(f"q{p}_{label}_atom_score_stats", score_stats)
        total = score_stats["scored_rows"]
        print(f"q{p}_{label}_best_atom_combos:")
        for good, polarity, weight, combo in best:
            rate = good / total if total else 0.0
            print(f"  good={good}/{total} rate={rate:.9f} polarity={polarity} weight={weight} combo={' * '.join(combo) if combo else '1'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    print("p27 K/A base-curve sampler viability probe")
    print("base curve: 64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0, L=K^2")
    print(f"atoms = {ATOM_NAMES}")
    for p in parse_ints(args.small_primes):
        run_field(p, args.max_weight, args.top)
    print("p27_kline_base_curve_sampler_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Legal conic-chain tower depth screen for p27.

Depth 1 of the legal conic pullback is d3-plus.
Depth 2 is d4-plus after d3.
This probe extends that check to deeper depths and records how the legal tower
thins as more selected gates are imposed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_conic_chain_source_probe import sqrt_table, transitions
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates


def normalize_pm1(values: list[int]) -> int | None:
    vals = {value for value in values if value in (-1, 1)}
    if not vals:
        return None
    if len(vals) != 1:
        return 0
    return vals.pop()


def selected_gate_bits(a: int, x0: int, p: int, depth: int) -> list[int | None]:
    bits: list[int | None] = []
    active = [x0]
    for _ in range(depth):
        branch_values: list[int] = []
        next_active: list[int] = []
        for x in active:
            _, branches = halve_all(a, x, p)
            branch_values.extend(legendre(branch, p) for branch in branches)
            next_active.extend(branch for branch in branches if legendre(branch, p) == 1)
        bit = normalize_pm1(branch_values)
        bits.append(bit)
        if bit != 1 or not next_active:
            active = []
        else:
            active = sorted(set(next_active))
    return bits


def chain_lift_count(a: int, x5: int, p: int, depth: int, roots: list[list[int]]) -> int:
    c_roots = roots[(2 - a) % p]
    r_roots = roots[x5 % p]
    if not c_roots or not r_roots:
        return 0
    active: dict[tuple[int, int], int] = {(c, r): 1 for c in c_roots for r in r_roots}
    for _ in range(depth):
        nxt: defaultdict[tuple[int, int], int] = defaultdict(int)
        for (c, r), mult in active.items():
            for rn in transitions(c, r, p, roots):
                nxt[(c, rn)] += mult
        active = dict(nxt)
        if not active:
            return 0
    return sum(active.values())


def expected_lift(bits: list[int | None], depth: int) -> bool:
    return all(bit == 1 for bit in bits[:depth])


def screen_field(p: int, depth: int) -> Counter:
    roots = sqrt_table(p)
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in candidates:
        a = int(cand["A"])
        x5 = int(cand["x5"])
        bits = selected_gate_bits(a, x5, p, depth)
        stats["legal_candidates"] += 1
        for i, bit in enumerate(bits, start=1):
            stats[f"d{i+2}_{bit}"] += 1
            if expected_lift(bits, i):
                stats[f"prefix_depth{i}_plus"] += 1
        for d in range(1, depth + 1):
            lifts = chain_lift_count(a, x5, p, d, roots)
            if lifts:
                stats[f"depth{d}_candidates_with_lift"] += 1
                stats[f"depth{d}_total_lifts"] += lifts
            if (lifts > 0) == expected_lift(bits, d):
                stats[f"depth{d}_matches_prefix_indicator"] += 1
            else:
                stats[f"depth{d}_mismatch_prefix_indicator"] += 1
    return stats


def screen_p27_sample(label: str, target: int, seed: int, max_draws: int, depth: int) -> tuple[str, Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))

    by_ax: dict[tuple[int, int], dict[str, int]] = {}
    for cand in candidates:
        by_ax.setdefault((int(cand["A"]), int(cand["x5"])), cand)

    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    stats["unique_ax"] = len(by_ax)
    for a, x5 in by_ax:
        bits = selected_gate_bits(a, x5, P, depth)
        stats["sample_unique_ax"] += 1
        for i, bit in enumerate(bits, start=1):
            stats[f"d{i+2}_{bit}"] += 1
            if expected_lift(bits, i):
                stats[f"prefix_depth{i}_plus"] += 1
    return label, stats


def print_counter(prefix: str, stats: Counter, depth: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    legal = stats["legal_candidates"]
    if legal:
        for d in range(1, depth + 1):
            with_lift = stats[f"depth{d}_candidates_with_lift"]
            total_lifts = stats[f"depth{d}_total_lifts"]
            print(f"  depth{d}_candidate_lift_rate = {with_lift / legal:.9f}")
            print(
                f"  depth{d}_avg_lifts_per_lifted_candidate = "
                f"{(total_lifts / with_lift) if with_lift else 0.0:.9f}"
            )


def print_p27_counter(prefix: str, stats: Counter, depth: int) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    total = stats["sample_unique_ax"]
    if total:
        for d in range(1, depth + 1):
            print(f"  prefix_depth{d}_rate = {stats[f'prefix_depth{d}_plus'] / total:.9f}")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--p27-target", type=int, default=1000)
    parser.add_argument("--p27-heldout-target", type=int, default=1000)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--p27-max-draws", type=int, default=1000000)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    print("p27 legal conic tower depth probe")
    print("depth d corresponds to selected gate d_{d+2}")
    print(f"depth = {args.depth}")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", screen_field(p, args.depth), args.depth)
    if not args.skip_p27:
        for label, stats in [
            screen_p27_sample("p27_train", args.p27_target, args.p27_seed, args.p27_max_draws, args.depth),
            screen_p27_sample(
                "p27_heldout",
                args.p27_heldout_target,
                args.p27_heldout_seed,
                args.p27_max_draws,
                args.depth,
            ),
        ]:
            print_p27_counter(label, stats, args.depth)
    print("p27_legal_conic_tower_depth_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

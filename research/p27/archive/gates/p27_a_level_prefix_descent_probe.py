#!/usr/bin/env python3
"""A-level descent screen for deeper p27 selected-prefix gates.

The conic d6 probe showed that after the selected d4/d5 prefix, the d6 bit
descends to A.  This cheaper probe asks how far that pattern persists without
materializing conic sign covers: for each gate d_j, group surviving (A,x)
fibers by A and report whether both signs occur in the same A group.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict

from p27_a_projection_prefix_profile_probe import auto_primes
from p27_legal_conic_tower_depth_probe import selected_gate_bits
from p27_label2_alpha_branch_recurrence_probe import P, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def unique_ax_from_candidates(candidates: list[dict[str, int]]) -> set[tuple[int, int]]:
    return {(int(cand["A"]), int(cand["x5"])) for cand in candidates}


def collect_field_ax(p: int) -> tuple[set[tuple[int, int]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    ax_points = unique_ax_from_candidates(candidates)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats["unique_ax"] = len(ax_points)
    stats["unique_A"] = len({A for A, _x in ax_points})
    return ax_points, stats


def collect_p27_ax(target: int, seed: int, max_draws: int) -> tuple[set[tuple[int, int]], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    ax_points = unique_ax_from_candidates(candidates)
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sample_rows"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    stats["unique_ax"] = len(ax_points)
    stats["unique_A"] = len({A for A, _x in ax_points})
    return ax_points, stats


def prefix_alive(bits: list[int | None], depth: int) -> bool:
    return all(bit == 1 for bit in bits[:depth])


def descent_profile(ax_points: set[tuple[int, int]], p: int, depth: int) -> list[tuple[int, Counter]]:
    bits_by_ax = {
        (A, x): selected_gate_bits(A, x, p, depth)
        for A, x in sorted(ax_points)
    }
    out: list[tuple[int, Counter]] = []
    base_A = len({A for A, _x in ax_points})
    base_ax = len(ax_points)

    for gate_index in range(depth):
        groups: defaultdict[int, Counter] = defaultdict(Counter)
        stats: Counter = Counter()
        for (A, x), bits in bits_by_ax.items():
            if not prefix_alive(bits, gate_index):
                continue
            bit = bits[gate_index]
            if bit not in (-1, 0, 1):
                stats["none_rows"] += 1
                continue
            groups[A][int(bit)] += 1
            groups[A]["rows"] += 1
        stats["gate_d"] = gate_index + 3
        stats["prefix_depth_before_gate"] = gate_index
        stats["rows"] = sum(counter["rows"] for counter in groups.values())
        stats["groups"] = len(groups)
        stats["base_A"] = base_A
        stats["base_ax"] = base_ax
        stats["plus_rows"] = sum(counter[1] for counter in groups.values())
        stats["minus_rows"] = sum(counter[-1] for counter in groups.values())
        stats["zero_rows"] = sum(counter[0] for counter in groups.values())
        for counter in groups.values():
            size = counter["rows"]
            stats[f"group_size_{size}"] += 1
            signs = {sign for sign in (-1, 0, 1) if counter[sign]}
            if len(signs) > 1:
                stats["mixed_groups"] += 1
                stats["mixed_rows"] += size
            elif 1 in signs:
                stats["plus_groups"] += 1
            elif -1 in signs:
                stats["minus_groups"] += 1
            elif 0 in signs:
                stats["zero_groups"] += 1
        if stats["groups"]:
            stats["max_group_size"] = max(counter["rows"] for counter in groups.values())
            stats["group_rate_x1000000"] = (stats["groups"] * 1_000_000) // base_A if base_A else 0
            stats["row_rate_x1000000"] = (stats["rows"] * 1_000_000) // base_ax if base_ax else 0
            stats["plus_group_rate_x1000000"] = (stats["plus_groups"] * 1_000_000) // stats["groups"]
            stats["mixed_group_rate_x1000000"] = (stats["mixed_groups"] * 1_000_000) // stats["groups"]
            stats["mixed_row_rate_x1000000"] = (stats["mixed_rows"] * 1_000_000) // stats["rows"]
            stats["random_scaled_groups_x1000000"] = (
                stats["groups"] * (2**gate_index) * 1_000_000 // base_A
                if base_A
                else 0
            )
        out.append((gate_index + 3, stats))
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_profile(label: str, ax_points: set[tuple[int, int]], p: int, base_stats: Counter, depth: int) -> None:
    print_counter(f"{label}_base", base_stats)
    for gate, stats in descent_profile(ax_points, p, depth):
        print_counter(f"{label}_d{gate}", stats)
        groups = stats["groups"]
        if groups:
            print(f"  group_rate = {groups / stats['base_A']:.9f}")
            print(f"  plus_group_rate = {stats['plus_groups'] / groups:.9f}")
            print(f"  mixed_group_rate = {stats['mixed_groups'] / groups:.9f}")
            print(f"  random_scaled_groups = {stats['random_scaled_groups_x1000000'] / 1_000_000:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--auto-start", type=int, default=0)
    parser.add_argument("--auto-count", type=int, default=0)
    parser.add_argument("--depth", type=int, default=12)
    parser.add_argument("--p27-target", type=int, default=6000)
    parser.add_argument("--p27-heldout-target", type=int, default=6000)
    parser.add_argument("--p27-max-draws", type=int, default=5000000)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    primes = parse_ints(args.small_primes)
    if args.auto_count:
        primes.extend(auto_primes(args.auto_start, args.auto_count))

    print("p27 A-level prefix descent probe")
    print("question = do selected gates d_j descend to whole A-fibers?")
    print(f"depth = {args.depth}")
    for q in dict.fromkeys(primes):
        ax_points, stats = collect_field_ax(q)
        stats["sqrt_p_floor"] = math.isqrt(q)
        print_profile(f"q{q}", ax_points, q, stats, args.depth)

    if not args.skip_p27:
        ax_points, stats = collect_p27_ax(args.p27_target, args.p27_seed, args.p27_max_draws)
        stats["sqrt_p_floor"] = math.isqrt(P)
        print_profile("p27_train", ax_points, P, stats, args.depth)

        heldout_ax, heldout_stats = collect_p27_ax(
            args.p27_heldout_target,
            args.p27_heldout_seed,
            args.p27_max_draws,
        )
        heldout_stats["sqrt_p_floor"] = math.isqrt(P)
        print_profile("p27_heldout", heldout_ax, P, heldout_stats, args.depth)

    print("p27_a_level_prefix_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

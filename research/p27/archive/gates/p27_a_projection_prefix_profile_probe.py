#!/usr/bin/env python3
"""A-projection profile for selected p27 legal/conic tower prefixes."""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict

from p27_legal_conic_tower_depth_probe import selected_gate_bits
from p27_label2_alpha_branch_recurrence_probe import P, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row, enumerate_small_prime_candidates


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def auto_primes(start: int, count: int) -> list[int]:
    out: list[int] = []
    n = start
    while len(out) < count:
        if n % 8 == 7 and is_prime(n):
            out.append(n)
        n += 1
    return out


def unique_ax_from_candidates(candidates: list[dict[str, int]]) -> set[tuple[int, int]]:
    return {(int(cand["A"]), int(cand["x5"])) for cand in candidates}


def prefix_profile(ax_points: set[tuple[int, int]], p: int, depth: int) -> Counter:
    stats: Counter = Counter()
    prefix_ax: list[set[tuple[int, int]]] = [set() for _ in range(depth + 1)]
    prefix_A: list[set[int]] = [set() for _ in range(depth + 1)]
    A_to_x: list[defaultdict[int, set[int]]] = [defaultdict(set) for _ in range(depth + 1)]

    for A, x in ax_points:
        bits = selected_gate_bits(A, x, p, depth)
        prefix_ax[0].add((A, x))
        prefix_A[0].add(A)
        A_to_x[0][A].add(x)
        alive = True
        for d in range(1, depth + 1):
            alive = alive and bits[d - 1] == 1
            if alive:
                prefix_ax[d].add((A, x))
                prefix_A[d].add(A)
                A_to_x[d][A].add(x)
            stats[f"d{d + 2}_{bits[d - 1]}"] += 1

    base_ax = len(prefix_ax[0])
    base_A = len(prefix_A[0])
    for d in range(depth + 1):
        ax_count = len(prefix_ax[d])
        A_count = len(prefix_A[d])
        x_fibers = [len(xs) for xs in A_to_x[d].values()]
        stats[f"depth{d}_ax"] = ax_count
        stats[f"depth{d}_A"] = A_count
        stats[f"depth{d}_ax_rate"] = ax_count / base_ax if base_ax else 0.0
        stats[f"depth{d}_A_rate"] = A_count / base_A if base_A else 0.0
        stats[f"depth{d}_A_over_p"] = A_count / p
        stats[f"depth{d}_A_over_sqrtp"] = A_count / math.sqrt(p)
        stats[f"depth{d}_avg_x_per_A"] = ax_count / A_count if A_count else 0.0
        stats[f"depth{d}_max_x_per_A"] = max(x_fibers) if x_fibers else 0
        stats[f"depth{d}_random_scaled_A"] = (A_count / base_A * (2**d)) if base_A else 0.0
        stats[f"depth{d}_random_scaled_ax"] = (ax_count / base_ax * (2**d)) if base_ax else 0.0
    return stats


def screen_field(p: int, depth: int) -> Counter:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    ax_points = unique_ax_from_candidates(candidates)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    stats["unique_ax"] = len(ax_points)
    stats["unique_A"] = len({A for A, _ in ax_points})
    stats.update(prefix_profile(ax_points, p, depth))
    return stats


def screen_p27_sample(label: str, target: int, seed: int, max_draws: int, depth: int) -> tuple[str, Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    ax_points = unique_ax_from_candidates(candidates)
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sampled_pairs"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    stats["unique_ax"] = len(ax_points)
    stats["unique_A"] = len({A for A, _ in ax_points})
    stats.update(prefix_profile(ax_points, P, depth))
    return label, stats


def print_counter(prefix: str, stats: Counter, p: int | None, depth: int) -> None:
    print(f"{prefix}:")
    print(f"  unique_ax = {stats['unique_ax']}")
    print(f"  unique_A = {stats['unique_A']}")
    for d in range(depth + 1):
        print(
            f"  depth{d}: "
            f"ax={stats[f'depth{d}_ax']} "
            f"A={stats[f'depth{d}_A']} "
            f"ax_rate={stats[f'depth{d}_ax_rate']:.9f} "
            f"A_rate={stats[f'depth{d}_A_rate']:.9f} "
            f"A_over_p={stats[f'depth{d}_A_over_p']:.6e} "
            f"A_over_sqrtp={stats[f'depth{d}_A_over_sqrtp']:.6e} "
            f"avg_x_per_A={stats[f'depth{d}_avg_x_per_A']:.6f} "
            f"scaled_A={stats[f'depth{d}_random_scaled_A']:.6f} "
            f"scaled_ax={stats[f'depth{d}_random_scaled_ax']:.6f}"
        )
    if p is not None:
        print(f"  sqrt_p = {math.sqrt(p):.6f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--auto-start", type=int, default=2200)
    parser.add_argument("--auto-count", type=int, default=8)
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--p27-target", type=int, default=3000)
    parser.add_argument("--p27-heldout-target", type=int, default=3000)
    parser.add_argument("--p27-max-draws", type=int, default=2000000)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    primes = parse_ints(args.small_primes) + auto_primes(args.auto_start, args.auto_count)
    seen: set[int] = set()
    print("p27 A-projection selected-prefix profile")
    print("depth d = legal source plus selected gates d3..d_{d+2}")
    for p in primes:
        if p in seen:
            continue
        seen.add(p)
        print_counter(f"q{p}", screen_field(p, args.depth), p, args.depth)
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
            print_counter(label, stats, P, args.depth)
    print("p27_a_projection_prefix_profile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

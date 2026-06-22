#!/usr/bin/env python3
"""Low-degree relation screen for the selected K/Sroot -> A graph.

The p27 K/S fiber profile found that every selected K and Sroot fiber carries
one selected A in the promotion fields.  This probe asks whether that graph is
low-degree enough to become a theorem/source target.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_conic_pair_invariant_relation_probe import System, relation_stats_for_system
from p27_kline_reverse_z_relation_probe import (
    dedupe_candidates,
    inv,
    ks_coordinates,
    p27_candidates,
    parse_ints,
)
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod


SYSTEMS = [
    System("K_A", ("K", "A"), 16),
    System("S_A", ("S", "A"), 16),
    System("K_x5", ("K", "x5"), 16),
    System("S_x5", ("S", "x5"), 16),
    System("K_A_x5", ("K", "A", "x5"), 8),
    System("S_A_x5", ("S", "A", "x5"), 8),
]


def selected_rows_from_candidates(candidates: list[dict[str, int]], p: int) -> tuple[list[dict[str, int | None]], Counter]:
    rows: list[dict[str, int | None]] = []
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
        stats["d2_plus_candidates"] += 1
        for x6 in x6s:
            stats["x6_branches"] += 1
            if legendre(x6, p) != 1:
                stats["x6_nonsquare"] += 1
                continue
            zroots = roots_mod(x6, p)
            if not zroots:
                stats["zroot_missing"] += 1
                continue
            ix6 = inv(x6, p)
            r = (x6 + ix6) % p if ix6 is not None else None
            for z in zroots:
                iz = inv(z, p)
                rows.append(
                    {
                        "K": k,
                        "S": s,
                        "A": A,
                        "x5": x5,
                        "x6": x6 % p,
                        "z": z % p,
                        "r": r,
                        "zsum": (z + iz) % p if iz is not None else None,
                        "zdiff": (z - iz) % p if iz is not None else None,
                    }
                )
                stats["z_rows"] += 1
    stats["unique_K"] = len({int(row["K"]) for row in rows})
    stats["unique_S"] = len({int(row["S"]) for row in rows})
    stats["unique_A"] = len({int(row["A"]) for row in rows})
    stats["unique_K_A"] = len({(int(row["K"]), int(row["A"])) for row in rows})
    stats["unique_S_A"] = len({(int(row["S"]), int(row["A"])) for row in rows})
    stats["unique_K_x5"] = len({(int(row["K"]), int(row["x5"])) for row in rows})
    stats["unique_S_x5"] = len({(int(row["S"]), int(row["x5"])) for row in rows})
    stats["unique_K_A_x5"] = len({(int(row["K"]), int(row["A"]), int(row["x5"])) for row in rows})
    stats["unique_S_A_x5"] = len({(int(row["S"]), int(row["A"]), int(row["x5"])) for row in rows})
    return rows, stats


def transformed_points(rows: list[dict[str, int | None]], system: System) -> tuple[list[tuple[int, ...]], Counter]:
    points: list[tuple[int, ...]] = []
    stats: Counter = Counter()
    for row in rows:
        coords: list[int] = []
        for name in system.coordinates:
            value = row.get(name)
            if value is None:
                stats["degenerate"] += 1
                break
            coords.append(int(value))
        else:
            points.append(tuple(coords))
    stats["rows"] = len(points)
    stats["unique"] = len(set(points))
    return points, stats


def safe_relation_stats(points: list[tuple[int, ...]], p: int, degrees: list[int]) -> Counter:
    if not points:
        stats: Counter = Counter()
        for degree in degrees:
            prefix = f"deg{degree}"
            stats[f"{prefix}_monomials"] = 0
            stats[f"{prefix}_rank"] = 0
            stats[f"{prefix}_nullity"] = 0
            stats[f"{prefix}_forced_nullity"] = 0
            stats[f"{prefix}_extra_nullity"] = 0
        return stats
    return relation_stats_for_system(points, p, degrees)


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def screen_rows(label: str, rows: list[dict[str, int | None]], p: int, pair_degrees: list[int], triple_degrees: list[int]) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    for system in SYSTEMS:
        points, transform_stats = transformed_points(rows, system)
        degrees = triple_degrees if len(system.coordinates) == 3 else pair_degrees
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, degrees))
        print(f"{label}_{system.name}:")
        print(f"  transform_rows = {stats['transform_rows']}")
        print(f"  transform_unique = {stats['transform_unique']}")
        print(f"  transform_degenerate = {stats['transform_degenerate']}")
        for degree in degrees:
            prefix = f"deg{degree}"
            print(
                "  "
                f"{prefix}: monomials={stats[f'{prefix}_monomials']} "
                f"rank={stats[f'{prefix}_rank']} "
                f"nullity={stats[f'{prefix}_nullity']} "
                f"forced={stats[f'{prefix}_forced_nullity']} "
                f"extra={stats[f'{prefix}_extra_nullity']}"
            )
            if stats[f"{prefix}_extra_nullity"]:
                print(
                    "  "
                    f"{prefix}_relation_terms={stats[f'{prefix}_relation_terms']} "
                    f"self_mismatches={stats[f'{prefix}_relation_self_mismatches']}"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="2,4,6,8,10,12,14,16")
    parser.add_argument("--triple-degrees", default="2,4,6,8")
    parser.add_argument("--p27-target", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees)
    triple_degrees = parse_ints(args.triple_degrees)
    print("p27 K-line selected A-map relation probe")
    print("source rows: d2 square and d3 all-plus with x6=z^2")
    print("question: is selected A a low-degree relation over K or Sroot?")
    print(f"pair_degrees = {pair_degrees}")
    print(f"triple_degrees = {triple_degrees}")

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_sample_stats", sample_stats)
        rows, stats = selected_rows_from_candidates(candidates, P)
        print_counter("p27_selected_stats", stats)
        screen_rows("p27", rows, P, pair_degrees, triple_degrees)

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        rows, stats = selected_rows_from_candidates(candidates, q)
        print(f"q={q}:")
        print_counter(f"q{q}_enum_stats", enum_stats)
        print_counter(f"q{q}_selected_stats", stats)
        screen_rows(f"q{q}", rows, q, pair_degrees, triple_degrees)

    print("p27_kline_a_map_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

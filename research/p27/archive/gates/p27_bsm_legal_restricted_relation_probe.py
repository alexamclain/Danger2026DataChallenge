#!/usr/bin/env python3
"""Relation screen on the legal-B-restricted BSM surface.

The BSM surface is q^2-sized.  Restricting B to the legal B-domain gives a
constant-factor smaller surface, but still leaves a q-sized fiber over each B.
This probe asks whether the canonical d3-plus points inside that restricted
surface satisfy an additional low-degree relation beyond the BSM surface
equation itself.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_bsm_surface_incidence_probe import legal_b_data, parse_ints
from p27_conic_pair_invariant_relation_probe import System, relation_stats_for_system
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, sqrt_table


PAIR_SYSTEMS = [
    System("B_s", ("B", "s"), 12),
    System("B_m", ("B", "m"), 12),
    System("s_m", ("s", "m"), 12),
]

TRIPLE_SYSTEMS = [
    System("B_s_m", ("B", "s", "m"), 10),
]


def b_set(raw: set[tuple[int, int] | tuple[int, int, int]]) -> set[int]:
    return {int(item[0]) for item in raw}


def bax_set(raw: set[tuple[int, int] | tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    return {item for item in raw if len(item) == 3}  # type: ignore[return-value]


def bsm_rows(p: int) -> tuple[list[dict[str, int]], list[dict[str, int]], Counter]:
    roots = sqrt_table(p)
    invs = inv_table(p)
    data, data_stats = legal_b_data(p)
    legal_b = b_set(data["legal_b"])
    d3plus_bax = bax_set(data["d3plus_bax"])
    stats: Counter = Counter({f"data_{key}": value for key, value in data_stats.items()})
    inv16 = invs[16 % p]

    legal_rows: list[dict[str, int]] = []
    target_rows: list[dict[str, int]] = []
    per_b_surface: Counter = Counter()
    per_b_target: Counter = Counter()

    for B in sorted(legal_b):
        B2 = B * B % p
        for s in range(p):
            s2 = s * s % p
            den = (B2 + s2 - 4) % p
            rhs = 4 * s2 % p * ((s2 - 4) % p) % p
            if den == 0:
                if rhs == 0:
                    stats["degenerate_all_m_pairs"] += 1
                else:
                    stats["inconsistent_den0_pairs"] += 1
                continue
            m2 = rhs * invs[den] % p
            m_roots = roots[m2]
            if not m_roots:
                stats["surface_no_m_root_pairs"] += 1
                continue
            for m in m_roots:
                if m == 0:
                    stats["skip_m0"] += 1
                    continue
                row = {"B": B, "s": s, "m": m}
                legal_rows.append(row)
                per_b_surface[B] += 1
                A = (B2 - 2) % p
                x = m * m % p * inv16 % p
                if (B, A, x) in d3plus_bax:
                    target_rows.append(row)
                    per_b_target[B] += 1

    stats["legal_surface_rows"] = len(legal_rows)
    stats["target_rows"] = len(target_rows)
    stats["legal_B"] = len(legal_b)
    stats["target_B"] = len(per_b_target)
    for value, count in Counter(per_b_surface.values()).items():
        stats[f"surface_rows_per_B_{value}"] = count
    for value, count in Counter(per_b_target.values()).items():
        stats[f"target_rows_per_B_{value}"] = count
    return legal_rows, target_rows, stats


def transformed_points(rows: list[dict[str, int]], system: System) -> list[tuple[int, ...]]:
    return [tuple(row[name] for name in system.coordinates) for row in rows]


def empty_stats(degrees: list[int]) -> Counter:
    stats: Counter = Counter()
    for degree in degrees:
        prefix = f"deg{degree}"
        stats[f"{prefix}_monomials"] = 0
        stats[f"{prefix}_rank"] = 0
        stats[f"{prefix}_nullity"] = 0
        stats[f"{prefix}_forced_nullity"] = 0
        stats[f"{prefix}_extra_nullity"] = 0
    return stats


def safe_relation_stats(points: list[tuple[int, ...]], p: int, degrees: list[int]) -> Counter:
    if not points:
        return empty_stats(degrees)
    return relation_stats_for_system(points, p, degrees)


def compare_system(
    label: str,
    p: int,
    legal_rows: list[dict[str, int]],
    target_rows: list[dict[str, int]],
    system: System,
    degrees: list[int],
) -> None:
    legal_points = transformed_points(legal_rows, system)
    target_points = transformed_points(target_rows, system)
    legal_stats = safe_relation_stats(legal_points, p, degrees)
    target_stats = safe_relation_stats(target_points, p, degrees)
    print(f"{label}_{system.name}:")
    print(f"  legal_rows = {len(legal_points)}")
    print(f"  legal_unique = {len(set(legal_points))}")
    print(f"  target_rows = {len(target_points)}")
    print(f"  target_unique = {len(set(target_points))}")
    for degree in degrees:
        prefix = f"deg{degree}"
        le = legal_stats[f"{prefix}_extra_nullity"]
        te = target_stats[f"{prefix}_extra_nullity"]
        print(
            "  "
            f"{prefix}: legal_rank={legal_stats[f'{prefix}_rank']} "
            f"legal_extra={le} "
            f"target_rank={target_stats[f'{prefix}_rank']} "
            f"target_extra={te} "
            f"target_minus_legal_extra={te - le}"
        )


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="2,4,6,8,10,12")
    parser.add_argument("--triple-degrees", default="2,4,6,8,10")
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees)
    triple_degrees = parse_ints(args.triple_degrees)
    print("p27 BSM legal-restricted relation probe")
    print("legal surface = BSM surface with B in legal B-domain")
    print("target = canonical d3-plus B/A/x rows inside that surface")
    print(f"pair_degrees = {pair_degrees}")
    print(f"triple_degrees = {triple_degrees}")
    for p in parse_ints(args.small_primes):
        legal_rows, target_rows, stats = bsm_rows(p)
        print_counter(f"q{p}_base", stats)
        for system in PAIR_SYSTEMS:
            compare_system(f"q{p}", p, legal_rows, target_rows, system, pair_degrees)
        for system in TRIPLE_SYSTEMS:
            compare_system(f"q{p}", p, legal_rows, target_rows, system, triple_degrees)
    print("p27_bsm_legal_restricted_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

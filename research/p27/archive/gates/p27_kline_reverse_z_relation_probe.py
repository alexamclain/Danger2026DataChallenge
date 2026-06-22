#!/usr/bin/env python3
"""Low-degree relation screen for the actual d3 reverse-source root.

Previous K-line tests used only the d3 sign bit.  This probe keeps the actual
source variable z from the all-plus reverse-doubling condition x6=z^2 and asks
whether the d3 source cover is a low-degree plane curve over the reduced
coordinates K or Sroot.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_conic_pair_invariant_relation_probe import System, relation_stats_for_system
from p27_eprime_double_kummer_line_probe import kummer_double_x
from p27_equotient_2isogeny_line_probe import quotient_point
from p27_label2_alpha_branch_recurrence_probe import (
    P,
    halve_all,
    legendre,
    sample_rows,
)
from p27_reverse_doubling_source_probe import (
    all_oriented_candidates_from_row,
    enumerate_small_prime_candidates,
    roots_mod,
)
from p27_reverse_source_d4_recurrence_probe import QuotientRow
from p27_sroot_branch_divisor_probe import s_coordinate


SYSTEMS = [
    System("K_z", ("K", "z"), 14),
    System("S_z", ("S", "z"), 14),
    System("K_x6", ("K", "x6"), 14),
    System("S_x6", ("S", "x6"), 14),
    System("K_r", ("K", "r"), 14),
    System("S_r", ("S", "r"), 14),
    System("K_zsum", ("K", "zsum"), 14),
    System("S_zsum", ("S", "zsum"), 14),
    System("K_zdiff", ("K", "zdiff"), 14),
    System("S_zdiff", ("S", "zdiff"), 14),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def dedupe_candidates(candidates: list[dict[str, int]]) -> list[dict[str, int]]:
    seen: set[tuple[int, int, int, int, int]] = set()
    out: list[dict[str, int]] = []
    for cand in candidates:
        key = (
            int(cand["X"]),
            int(cand["W"]),
            int(cand["T"]),
            int(cand["A"]),
            int(cand["x5"]),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(cand)
    return out


def ks_coordinates(cand: dict[str, int], p: int) -> tuple[int, int] | None:
    qrow = QuotientRow(x=int(cand["X"]) % p, w=int(cand["W"]) % p, target=1)
    eprime = quotient_point(qrow, p)
    if eprime is None:
        return None
    k = kummer_double_x(eprime.x, p)
    s = s_coordinate(eprime, p)
    if k is None or s is None:
        return None
    if s * s % p != k % p:
        raise ValueError("Sroot square did not match K")
    return k, s


def z_rows_from_candidates(candidates: list[dict[str, int]], p: int) -> tuple[list[dict[str, int | None]], Counter]:
    rows: list[dict[str, int | None]] = []
    stats: Counter = Counter()
    for cand in dedupe_candidates(candidates):
        stats["candidates"] += 1
        ks = ks_coordinates(cand, p)
        if ks is None:
            stats["ks_degenerate"] += 1
            continue
        k, s = ks
        d2, x6s = halve_all(int(cand["A"]) % p, int(cand["x5"]) % p, p)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
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
                        "x6": x6 % p,
                        "z": z % p,
                        "r": r,
                        "zsum": (z + iz) % p if iz is not None else None,
                        "zdiff": (z - iz) % p if iz is not None else None,
                    }
                )
                stats["z_rows"] += 1
    stats["unique_K_z"] = len({(int(row["K"]), int(row["z"])) for row in rows})
    stats["unique_S_z"] = len({(int(row["S"]), int(row["z"])) for row in rows})
    stats["unique_K"] = len({int(row["K"]) for row in rows})
    stats["unique_S"] = len({int(row["S"]) for row in rows})
    return rows, stats


def p27_candidates(target: int, seed: int, max_draws: int) -> tuple[list[dict[str, int]], Counter]:
    sampled, sample_stats = sample_rows(target, seed, max_draws)
    candidates: list[dict[str, int]] = []
    for row in sampled:
        candidates.extend(all_oriented_candidates_from_row(row, P))
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sample_rows"] = len(sampled)
    stats["oriented_candidates_raw"] = len(candidates)
    return candidates, stats


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


def screen_rows(label: str, rows: list[dict[str, int | None]], p: int, degrees: list[int]) -> None:
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    for system in SYSTEMS:
        points, transform_stats = transformed_points(rows, system)
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


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--degrees", default="2,4,6,8,10,12")
    parser.add_argument("--p27-target", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    args = parser.parse_args()

    degrees = parse_ints(args.degrees)
    print("p27 K-line reverse-z relation probe")
    print("source rows: d2 square and d3 all-plus with x6=z^2")
    print("coordinates: K=x([2]P), Sroot^2=K")
    print(f"degrees = {degrees}")

    if args.p27_target:
        candidates, sample_stats = p27_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_sample_stats", sample_stats)
        rows, stats = z_rows_from_candidates(candidates, P)
        print_counter("p27_zrow_stats", stats)
        screen_rows("p27", rows, P, degrees)

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        rows, stats = z_rows_from_candidates(candidates, q)
        print(f"q={q}:")
        print_counter(f"q{q}_enum_stats", enum_stats)
        print_counter(f"q{q}_zrow_stats", stats)
        screen_rows(f"q{q}", rows, q, degrees)

    print("p27_kline_reverse_z_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

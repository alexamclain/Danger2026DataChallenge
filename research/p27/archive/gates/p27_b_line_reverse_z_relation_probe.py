#!/usr/bin/env python3
"""Low-degree relation screen for the d3 reverse-source root over the B-line.

The B-line descent shows that the selected gate bits descend to

    B = 8*X^2/(X^2 - 1)^2

on the legal residual source.  Sign-only support scans have killed several
visible low-degree Kummer classes.  This probe keeps the actual d3 all-plus
source root z, where x6 = z^2, and asks whether the source cover itself has a
low-degree plane model over B or nearby branch-normalized B coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_source_descent_probe import source_b_plus
from p27_conic_pair_invariant_relation_probe import System, relation_stats_for_system
from p27_kline_reverse_z_relation_probe import dedupe_candidates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates, roots_mod


SYSTEMS = [
    System("B_z", ("B", "z"), 20),
    System("B_x6", ("B", "x6"), 20),
    System("B_r", ("B", "r"), 20),
    System("B_zsum", ("B", "zsum"), 20),
    System("B_zdiff", ("B", "zdiff"), 20),
    System("lambda_z", ("lambda", "z"), 20),
    System("lambda_zsum", ("lambda", "zsum"), 20),
    System("lambda_zdiff", ("lambda", "zdiff"), 20),
    System("mu_z", ("mu", "z"), 20),
    System("mu_zsum", ("mu", "zsum"), 20),
    System("B_z_over_B", ("B", "z_over_B"), 20),
    System("B_z_over_Bp2", ("B", "z_over_Bp2"), 20),
    System("B_z_over_Bm2", ("B", "z_over_Bm2"), 20),
]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def maybe_div(num: int, den: int, p: int) -> int | None:
    iden = inv(den, p)
    if iden is None:
        return None
    return num % p * iden % p


def z_rows_from_candidates(
    candidates: list[dict[str, int]], p: int
) -> tuple[list[dict[str, int | None]], Counter]:
    rows: list[dict[str, int | None]] = []
    stats: Counter = Counter()

    for cand in dedupe_candidates(candidates):
        stats["candidates"] += 1
        X = int(cand["X"]) % p
        B = source_b_plus(X, p)
        if B is None:
            stats["B_degenerate"] += 1
            continue

        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        d2, x6s = halve_all(A, x5, p)
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
                z %= p
                iz = inv(z, p)
                rows.append(
                    {
                        "B": B,
                        "lambda": maybe_div(B, B + 2, p),
                        "mu": maybe_div(B - 2, B + 2, p),
                        "x6": x6 % p,
                        "z": z,
                        "r": r,
                        "zsum": (z + iz) % p if iz is not None else None,
                        "zdiff": (z - iz) % p if iz is not None else None,
                        "z_over_B": maybe_div(z, B, p),
                        "z_over_Bp2": maybe_div(z, B + 2, p),
                        "z_over_Bm2": maybe_div(z, B - 2, p),
                    }
                )
                stats["z_rows"] += 1

    stats["unique_B"] = len({int(row["B"]) for row in rows})
    stats["unique_B_z"] = len({(int(row["B"]), int(row["z"])) for row in rows})
    stats["unique_lambda_z"] = len(
        {
            (int(row["lambda"]), int(row["z"]))
            for row in rows
            if row["lambda"] is not None
        }
    )
    return rows, stats


def p27_rows(target: int, seed: int, max_draws: int) -> tuple[list[dict[str, int]], Counter]:
    candidates, sample_stats = p27_candidates(target, seed, max_draws)
    return candidates, Counter({f"sample_{key}": value for key, value in sample_stats.items()})


def transformed_points(
    rows: list[dict[str, int | None]], system: System
) -> tuple[list[tuple[int, ...]], Counter]:
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


def run_candidates(label: str, candidates: list[dict[str, int]], p: int, degrees: list[int]) -> None:
    rows, stats = z_rows_from_candidates(candidates, p)
    print_counter(f"{label}_zrow_stats", stats)
    screen_rows(label, rows, p, degrees)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--degrees", default="2,4,6,8,10,12")
    parser.add_argument("--p27-target", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    args = parser.parse_args()

    degrees = parse_ints(args.degrees)
    print("p27 B-line reverse-z relation probe")
    print("source rows: d2 square and d3 all-plus with x6=z^2")
    print("B = 8*X^2/(X^2-1)^2")
    print(f"degrees = {degrees}")

    if args.p27_target:
        candidates, sample_stats = p27_rows(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_sample_stats", sample_stats)
        run_candidates("p27", candidates, P, degrees)

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print(f"q={q}:")
        print_counter(f"q{q}_enum_stats", enum_stats)
        run_candidates(f"q{q}", candidates, q, degrees)

    print("p27_b_line_reverse_z_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

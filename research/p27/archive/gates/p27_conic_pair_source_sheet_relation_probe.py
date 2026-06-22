#!/usr/bin/env python3
"""Source-sheet relation screen for the p27 conic-pair legal pullback.

The B/K-enhanced screen found the staged surface

    m^2*(B^2+s^2-4) = 4*s^2*(s^2-4),

where B is the descended source coordinate and s,m are conic-pair invariants.
That surface is still two-dimensional.  A sqrt-beating direct pullback would
need another stable relation, quotient, or low-genus source once the actual
residual source sheets X,W,T are retained.

This probe joins legal d3-plus source rows (X,W,T,A,x5) to their conic-pair
preimages and screens small coordinate systems such as (X,s,m) and
(X,W,s,m).  The output is a relation-nullity screen, not a production sampler.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_source_descent_probe import source_b_plus
from p27_conic_pair_invariant_relation_probe import System, invariant_values, relation_stats_for_system
from p27_conic_pair_sampler_legal_incidence_probe import inv_table
from p27_kline_reverse_z_relation_probe import ks_coordinates, parse_ints
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits


PAIR_SYSTEMS = [
    System("X_s", ("X", "s"), 16),
    System("X_m", ("X", "m"), 16),
    System("X_R", ("X", "R"), 16),
    System("X_L", ("X", "L"), 16),
    System("W_s", ("W", "s"), 16),
    System("T_s", ("T", "s"), 16),
    System("B_s", ("B", "s"), 16),
    System("K_s", ("K", "s"), 16),
]

TRIPLE_SYSTEMS = [
    System("X_s_m", ("X", "s", "m"), 12),
    System("X_s_w", ("X", "s", "w"), 12),
    System("X_R_L", ("X", "R", "L"), 12),
    System("W_s_m", ("W", "s", "m"), 12),
    System("T_s_m", ("T", "s", "m"), 12),
    System("B_s_m", ("B", "s", "m"), 12),
    System("K_s_m", ("K", "s", "m"), 12),
]

QUAD_SYSTEMS = [
    System("X_W_s_m", ("X", "W", "s", "m"), 8),
    System("X_T_s_m", ("X", "T", "s", "m"), 8),
    System("X_B_s_m", ("X", "B", "s", "m"), 8),
    System("X_s_m_w", ("X", "s", "m", "w"), 8),
    System("X_R_L_B", ("X", "R", "L", "B"), 8),
]


def d3plus_source_rows(p: int) -> tuple[dict[tuple[int, int], list[dict[str, int]]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    rows_by_ax: defaultdict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    seen: set[tuple[int, int, int, int, int]] = set()

    for cand in candidates:
        key = (
            int(cand["X"]) % p,
            int(cand["W"]) % p,
            int(cand["T"]) % p,
            int(cand["A"]) % p,
            int(cand["x5"]) % p,
        )
        if key in seen:
            stats["duplicate_source_rows"] += 1
            continue
        seen.add(key)
        bits = candidate_bits(cand, p)
        if bits.d3 != 1:
            continue
        X = int(cand["X"]) % p
        B = source_b_plus(X, p)
        if B is None:
            stats["B_degenerate"] += 1
            continue
        ks = ks_coordinates(cand, p)
        if ks is None:
            stats["KS_degenerate"] += 1
            continue
        K, S = ks
        row = {
            "X": X,
            "W": int(cand["W"]) % p,
            "T": int(cand["T"]) % p,
            "A": int(cand["A"]) % p,
            "x5": int(cand["x5"]) % p,
            "B": B,
            "K": K,
            "Sroot": S,
        }
        rows_by_ax[(row["A"], row["x5"])].append(row)
        stats["d3plus_source_rows"] += 1

    stats["d3plus_Ax"] = len(rows_by_ax)
    return dict(rows_by_ax), stats


def joined_rows(p: int) -> tuple[list[dict[str, int]], Counter]:
    source_by_ax, source_stats = d3plus_source_rows(p)
    invs = inv_table(p)
    inv2 = invs[2]
    inv4 = invs[4]
    rows: list[dict[str, int]] = []
    stats: Counter = Counter(source_stats)

    for R in range(1, p):
        invR = invs[R]
        a_line = (R - invR) % p
        s = (R + invR) % p
        a2 = a_line * a_line % p
        for L in range(1, p):
            stats["draws"] += 1
            a2_over_l = a2 * invs[L] % p
            d = (L - a2_over_l) * inv2 % p
            r = -(L + a2_over_l) * inv4 % p
            if r == 0:
                stats["degenerate_r"] += 1
                continue
            c = s * d % p * invs[(2 * r) % p] % p
            A = (2 - c * c) % p
            x = r * r % p
            source_rows = source_by_ax.get((A, x))
            if not source_rows:
                continue
            values = invariant_values((R, L), p, invs)
            if values is None:
                stats["invariant_degenerate"] += 1
                continue
            for source in source_rows:
                row = dict(source)
                row.update(values)
                row["R"] = R
                row["L"] = L
                rows.append(row)
                stats["joined_rows"] += 1

    stats["unique_joined_RL_source"] = len(
        {
            (row["X"], row["W"], row["T"], row["A"], row["x5"], row["R"], row["L"])
            for row in rows
        }
    )
    stats["unique_joined_Ax"] = len({(row["A"], row["x5"]) for row in rows})
    return rows, stats


def transformed_points(rows: list[dict[str, int]], system: System) -> tuple[list[tuple[int, ...]], Counter]:
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


def print_system(label: str, system: System, stats: Counter, degrees: list[int]) -> None:
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


def screen_field(
    p: int,
    pair_degrees: list[int],
    triple_degrees: list[int],
    quad_degrees: list[int],
) -> None:
    rows, base_stats = joined_rows(p)
    print_counter(f"q{p}_base", base_stats)

    for system in PAIR_SYSTEMS:
        points, transform_stats = transformed_points(rows, system)
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, pair_degrees))
        print_system(f"q{p}", system, stats, pair_degrees)

    for system in TRIPLE_SYSTEMS:
        points, transform_stats = transformed_points(rows, system)
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, triple_degrees))
        print_system(f"q{p}", system, stats, triple_degrees)

    for system in QUAD_SYSTEMS:
        points, transform_stats = transformed_points(rows, system)
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, quad_degrees))
        print_system(f"q{p}", system, stats, quad_degrees)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="4,8,12,16")
    parser.add_argument("--triple-degrees", default="4,8,12")
    parser.add_argument("--quad-degrees", default="4,6,8")
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees)
    triple_degrees = parse_ints(args.triple_degrees)
    quad_degrees = parse_ints(args.quad_degrees)
    print("p27 conic-pair source-sheet relation probe")
    print("rows = legal d3-plus source sheets joined to conic-pair preimages")
    print("question = do X/W/T source sheets expose a second low-degree pullback relation?")
    print(f"pair_degrees = {pair_degrees}")
    print(f"triple_degrees = {triple_degrees}")
    print(f"quad_degrees = {quad_degrees}")
    for p in parse_ints(args.small_primes):
        screen_field(p, pair_degrees, triple_degrees, quad_degrees)
    print("p27_conic_pair_source_sheet_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

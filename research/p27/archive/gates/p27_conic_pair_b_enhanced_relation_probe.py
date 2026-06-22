#!/usr/bin/env python3
"""B/K-enhanced relation screen for legal conic-pair preimages.

Raw conic-pair preimages in (R,L) and obvious invariant coordinates have no
small plane relation.  This probe adds the legal-source coordinates that are
known to descend on the X1(16) side:

    B = 8*X^2/(X^2 - 1)^2
    K = x([2]P) on E': V^2 = U^3 + 4U

and asks whether the legal d3-plus preimages become low-degree after retaining
B/K alongside conic-pair sampler variables.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_source_descent_probe import source_b_plus
from p27_conic_pair_invariant_relation_probe import System, invariant_values, relation_stats_for_system
from p27_conic_pair_sampler_legal_incidence_probe import inv_table
from p27_kline_reverse_z_relation_probe import ks_coordinates
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits, normalize


PAIR_SYSTEMS = [
    System("B_R", ("B", "R"), 20),
    System("B_L", ("B", "L"), 20),
    System("B_s", ("B", "s"), 20),
    System("B_m", ("B", "m"), 20),
    System("B_n", ("B", "n"), 20),
    System("B_w", ("B", "w"), 20),
    System("B_c", ("B", "c"), 20),
    System("B_r", ("B", "r"), 20),
    System("K_R", ("K", "R"), 20),
    System("K_L", ("K", "L"), 20),
    System("K_s", ("K", "s"), 20),
    System("K_m", ("K", "m"), 20),
    System("S_R", ("S", "R"), 20),
    System("S_L", ("S", "L"), 20),
]

TRIPLE_SYSTEMS = [
    System("B_R_L", ("B", "R", "L"), 8),
    System("B_s_m", ("B", "s", "m"), 8),
    System("B_c_r", ("B", "c", "r"), 8),
    System("B_s_w", ("B", "s", "w"), 8),
    System("K_R_L", ("K", "R", "L"), 8),
    System("K_s_m", ("K", "s", "m"), 8),
    System("S_R_L", ("S", "R", "L"), 8),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def strict_single(values: list[int | None]) -> int | None:
    vals = {value for value in values if value is not None}
    if len(vals) != 1:
        return None
    return vals.pop()


def target_info(p: int) -> tuple[dict[tuple[int, int], dict[str, int | None]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    by_ax_bits: defaultdict[tuple[int, int], list[int | None]] = defaultdict(list)
    by_ax_b: defaultdict[tuple[int, int], list[int | None]] = defaultdict(list)
    by_ax_k: defaultdict[tuple[int, int], list[int | None]] = defaultdict(list)
    by_ax_s: defaultdict[tuple[int, int], list[int | None]] = defaultdict(list)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in candidates:
        key = (int(cand["A"]) % p, int(cand["x5"]) % p)
        bits = candidate_bits(cand, p)
        by_ax_bits[key].append(bits.d3)
        by_ax_b[key].append(source_b_plus(int(cand["X"]) % p, p))
        ks = ks_coordinates(cand, p)
        if ks is None:
            by_ax_k[key].append(None)
            by_ax_s[key].append(None)
        else:
            k, s = ks
            by_ax_k[key].append(k)
            by_ax_s[key].append(s)

    info: dict[tuple[int, int], dict[str, int | None]] = {}
    for key in sorted(by_ax_bits):
        d3 = normalize(by_ax_bits[key])
        if d3 != 1:
            continue
        B = strict_single(by_ax_b[key])
        K = strict_single(by_ax_k[key])
        S = strict_single(by_ax_s[key])
        if B is None:
            stats["d3plus_missing_B"] += 1
            continue
        if K is None:
            stats["d3plus_missing_or_mixed_K"] += 1
        if S is None:
            stats["d3plus_missing_or_mixed_S"] += 1
        info[key] = {"B": B, "K": K, "S": S}

    stats["d3plus_targets"] = len(info)
    stats["all_ax"] = len(by_ax_bits)
    return info, stats


def rows_for_targets(p: int) -> tuple[list[dict[str, int | None]], Counter]:
    info, base_stats = target_info(p)
    invs = inv_table(p)
    inv2 = invs[2]
    inv4 = invs[4]
    rows: list[dict[str, int | None]] = []
    stats: Counter = Counter(base_stats)

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
            key = (A, x)
            if key not in info:
                continue
            values = invariant_values((R, L), p, invs)
            if values is None:
                stats["invariant_degenerate"] += 1
                continue
            row: dict[str, int | None] = {name: value for name, value in values.items()}
            row["R"] = R
            row["L"] = L
            row.update(info[key])
            rows.append(row)
            stats["target_preimage_rows"] += 1

    stats["unique_preimage_rows"] = len({(int(row["R"]), int(row["L"])) for row in rows})
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


def screen_field(p: int, pair_degrees: list[int], triple_degrees: list[int]) -> None:
    rows, base_stats = rows_for_targets(p)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="2,4,6,8,10,12")
    parser.add_argument("--triple-degrees", default="2,4,6")
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees)
    triple_degrees = parse_ints(args.triple_degrees)
    print("p27 conic-pair B/K-enhanced relation probe")
    print("rows = conic-pair sampler preimages of legal d3-plus targets")
    print("added source coordinates = B, K, and S when single-valued")
    print(f"pair_degrees = {pair_degrees}")
    print(f"triple_degrees = {triple_degrees}")
    for p in parse_ints(args.small_primes):
        screen_field(p, pair_degrees, triple_degrees)
    print("p27_conic_pair_b_enhanced_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

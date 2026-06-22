#!/usr/bin/env python3
"""Two-step Kummer relation screen for the p27 conic-pair tower.

The first-Z layer did not expose a simple quotient.  This probe asks whether
two consecutive selector layers do:

    Z0^2 = -(L0+a0)(L0-a0)c*r1
    S1   = -(L1+a1)(L1-a1)c*r2

and, when S1 is square,

    Z1^2 = S1.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_conic_pair_d4_recurrence_probe import conic_lifts, inv
from p27_conic_pair_d5_tower_probe import transition_lifts_table
from p27_conic_pair_invariant_relation_probe import (
    System,
    relation_stats_for_system,
)
from p27_conic_pair_sampler_legal_incidence_probe import legal_sets, sqrt_table


SELECTOR_SYSTEMS = [
    System("A_S1", ("A", "S1"), 12),
    System("Z0_S1", ("Z0", "S1"), 12),
    System("Z0_lpa_S1", ("Z0_lpa", "S1"), 12),
    System("Z0_lma_S1", ("Z0_lma", "S1"), 12),
    System("Z0_cR_S1", ("Z0_cR", "S1"), 12),
    System("R0_S1", ("R0", "S1"), 12),
    System("R1_S1", ("R1", "S1"), 12),
    System("a0_S1", ("a0", "S1"), 12),
    System("a1_S1", ("a1", "S1"), 12),
    System("L0_S1", ("L0", "S1"), 12),
    System("L1_S1", ("L1", "S1"), 12),
    System("w0_S1", ("w0", "S1"), 12),
    System("w1_S1", ("w1", "S1"), 12),
]

ROOT_SYSTEMS = [
    System("A_Z1", ("A", "Z1"), 12),
    System("Z0_Z1", ("Z0", "Z1"), 12),
    System("Z0_lpa_Z1_lpa", ("Z0_lpa", "Z1_lpa"), 12),
    System("Z0_lma_Z1_lma", ("Z0_lma", "Z1_lma"), 12),
    System("Z0_cR_Z1_cR", ("Z0_cR", "Z1_cR"), 12),
    System("A_Zratio", ("A", "Zratio"), 12),
    System("A_Zprod", ("A", "Zprod"), 12),
    System("R0_Z1", ("R0", "Z1"), 12),
    System("R1_Z0", ("R1", "Z0"), 12),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def selector_data(lift, p: int) -> dict[str, int] | None:
    if lift.R == 0:
        return None
    a = (lift.R - inv(lift.R, p)) % p
    L = (lift.h - lift.g - 2 * lift.r) % p
    selector = (-(L + a) * (L - a)) % p
    selector = selector * lift.c % p * lift.R % p
    w = (L * L - a * a) % p
    return {
        "a": a,
        "L": L,
        "w": w,
        "selector": selector,
        "R": lift.R,
    }


def add_norms(row: dict[str, int | None], prefix: str, z: int, data: dict[str, int], p: int) -> None:
    lpa = (data["L"] + data["a"]) % p
    lma = (data["L"] - data["a"]) % p
    cR = data["R"] * row["c"] % p  # type: ignore[operator]
    row[f"{prefix}"] = z
    row[f"{prefix}_lpa"] = z * inv(lpa, p) % p if lpa else None
    row[f"{prefix}_lma"] = z * inv(lma, p) % p if lma else None
    row[f"{prefix}_cR"] = z * inv(cR, p) % p if cR else None


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
            stats[f"deg{degree}_monomials"] = 0
            stats[f"deg{degree}_rank"] = 0
            stats[f"deg{degree}_nullity"] = 0
            stats[f"deg{degree}_forced_nullity"] = 0
            stats[f"deg{degree}_extra_nullity"] = 0
        return stats
    return relation_stats_for_system(points, p, degrees)


def two_step_rows(p: int) -> tuple[list[dict[str, int | None]], list[dict[str, int | None]], Counter]:
    roots = sqrt_table(p)
    _, legal, d3_plus, _ = legal_sets(p)
    selector_rows: list[dict[str, int | None]] = []
    root_rows: list[dict[str, int | None]] = []
    stats: Counter = Counter()

    for A, x5 in sorted(d3_plus):
        first_lifts = conic_lifts(A, x5, p, roots)
        stats["d3_plus_Ax"] += 1
        stats["first_lifts"] += len(first_lifts)
        for first in first_lifts:
            d0 = selector_data(first, p)
            if d0 is None or d0["selector"] == 0:
                stats["first_degenerate_selector"] += 1
                continue
            z0_roots = roots[d0["selector"]]
            if not z0_roots:
                stats["d4_minus_first_lifts"] += 1
                continue
            stats["d4_plus_first_lifts"] += 1
            second_lifts = transition_lifts_table(first.c, first.R, p, roots)
            stats["second_lifts_after_d4plus"] += len(second_lifts)
            for second in second_lifts:
                d1 = selector_data(second, p)
                if d1 is None or d1["selector"] == 0:
                    stats["second_degenerate_selector"] += 1
                    continue
                z1_roots = roots[d1["selector"]]
                if z1_roots:
                    stats["d5_plus_second_lifts"] += 1
                else:
                    stats["d5_minus_second_lifts"] += 1
                base = {
                    "A": A,
                    "x0": x5,
                    "c": first.c,
                    "r0": first.r,
                    "R0": first.R,
                    "R1": second.R,
                    "a0": d0["a"],
                    "a1": d1["a"],
                    "L0": d0["L"],
                    "L1": d1["L"],
                    "w0": d0["w"],
                    "w1": d1["w"],
                    "S0": d0["selector"],
                    "S1": d1["selector"],
                }
                for z0 in z0_roots:
                    row = dict(base)
                    add_norms(row, "Z0", z0, d0, p)
                    selector_rows.append(row)
                    for z1 in z1_roots:
                        rrow = dict(row)
                        add_norms(rrow, "Z1", z1, d1, p)
                        rrow["Zratio"] = z1 * inv(z0, p) % p if z0 else None
                        rrow["Zprod"] = z1 * z0 % p
                        root_rows.append(rrow)

    stats["selector_rows"] = len(selector_rows)
    stats["root_rows"] = len(root_rows)
    stats["legal_Ax"] = len(legal)
    return selector_rows, root_rows, stats


def degrees_for(system: System, requested: list[int] | None) -> list[int]:
    if requested is not None:
        return requested
    return list(range(2, system.max_degree_default + 1, 2))


def screen_systems(
    label: str,
    rows: list[dict[str, int | None]],
    systems: list[System],
    p: int,
    requested: list[int] | None,
) -> list[tuple[str, Counter]]:
    out: list[tuple[str, Counter]] = []
    for system in systems:
        degrees = degrees_for(system, requested)
        points, transform_stats = transformed_points(rows, system)
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, degrees))
        stats["row_family"] = label
        out.append((system.name, stats))
    return out


def print_system(prefix: str, name: str, stats: Counter, degrees: list[int]) -> None:
    print(f"{prefix} {name}:")
    print(f"  transform_rows = {stats['transform_rows']}")
    print(f"  transform_unique = {stats['transform_unique']}")
    print(f"  transform_degenerate = {stats['transform_degenerate']}")
    for degree in degrees:
        key = f"deg{degree}"
        print(
            "  "
            f"{key}: monomials={stats[f'{key}_monomials']} "
            f"rank={stats[f'{key}_rank']} "
            f"nullity={stats[f'{key}_nullity']} "
            f"forced={stats[f'{key}_forced_nullity']} "
            f"extra={stats[f'{key}_extra_nullity']}"
        )
        if stats[f"{key}_extra_nullity"]:
            print(
                "  "
                f"{key}_relation_terms={stats[f'{key}_relation_terms']} "
                f"self_mismatches={stats[f'{key}_relation_self_mismatches']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--degrees", default="")
    parser.add_argument("--root-degrees", default="")
    args = parser.parse_args()

    requested = parse_ints(args.degrees) if args.degrees else None
    root_requested = parse_ints(args.root_degrees) if args.root_degrees else requested
    print("p27 conic-pair two-step Kummer probe")
    print("selector rows: d4-plus first lift plus next selector S1")
    print("root rows: additionally S1 square with Z1^2=S1")
    for p in parse_ints(args.small_primes):
        selector_rows, root_rows, base_stats = two_step_rows(p)
        print(f"q{p} base:")
        for key in sorted(base_stats):
            print(f"  {key} = {base_stats[key]}")
        for name, stats in screen_systems("selector", selector_rows, SELECTOR_SYSTEMS, p, requested):
            system = next(system for system in SELECTOR_SYSTEMS if system.name == name)
            print_system(f"q{p} selector", name, stats, degrees_for(system, requested))
        for name, stats in screen_systems("root", root_rows, ROOT_SYSTEMS, p, root_requested):
            system = next(system for system in ROOT_SYSTEMS if system.name == name)
            print_system(f"q{p} root", name, stats, degrees_for(system, root_requested))
    print("p27_conic_pair_two_step_kummer_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

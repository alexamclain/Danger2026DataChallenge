#!/usr/bin/env python3
"""Three-coordinate relation screen for the p27 two-step Kummer tower.

The pair screen found no simple quotient in (Z0,S1), (Z0,Z1), ratios, or
products.  This probe checks the next small family: low-degree surfaces in
three obvious tower coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_conic_pair_invariant_relation_probe import System
from p27_conic_pair_two_step_kummer_probe import (
    safe_relation_stats,
    transformed_points,
    two_step_rows,
)


SELECTOR_SYSTEMS = [
    System("A_Z0_S1", ("A", "Z0", "S1"), 6),
    System("A_R0_S1", ("A", "R0", "S1"), 6),
    System("A_R1_S1", ("A", "R1", "S1"), 6),
    System("A_L0_S1", ("A", "L0", "S1"), 6),
    System("A_L1_S1", ("A", "L1", "S1"), 6),
    System("Z0_R0_S1", ("Z0", "R0", "S1"), 6),
    System("Z0_R1_S1", ("Z0", "R1", "S1"), 6),
    System("Z0_lpa_lma_S1", ("Z0_lpa", "Z0_lma", "S1"), 6),
    System("Z0_lpa_cR_S1", ("Z0_lpa", "Z0_cR", "S1"), 6),
    System("L0_L1_S1", ("L0", "L1", "S1"), 6),
]

ROOT_SYSTEMS = [
    System("A_Z0_Z1", ("A", "Z0", "Z1"), 6),
    System("A_Zratio_Zprod", ("A", "Zratio", "Zprod"), 6),
    System("A_Z0_Zratio", ("A", "Z0", "Zratio"), 6),
    System("R0_Z0_Z1", ("R0", "Z0", "Z1"), 6),
    System("R1_Z0_Z1", ("R1", "Z0", "Z1"), 6),
    System("A_Z0lpa_Z1lpa", ("A", "Z0_lpa", "Z1_lpa"), 6),
    System("A_Z0lma_Z1lma", ("A", "Z0_lma", "Z1_lma"), 6),
    System("A_Z0cR_Z1cR", ("A", "Z0_cR", "Z1_cR"), 6),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def degrees_for(system: System, requested: list[int] | None) -> list[int]:
    if requested is not None:
        return requested
    return list(range(2, system.max_degree_default + 1, 2))


def screen_systems(
    rows: list[dict[str, int | None]],
    systems: list[System],
    p: int,
    requested: list[int] | None,
) -> list[tuple[str, Counter]]:
    out: list[tuple[str, Counter]] = []
    for system in systems:
        points, transform_stats = transformed_points(rows, system)
        stats = Counter({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(safe_relation_stats(points, p, degrees_for(system, requested)))
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

    print("p27 conic-pair two-step Kummer trivariate probe")
    print("selector rows: d4-plus first lift plus next selector S1")
    print("root rows: additionally S1 square with Z1^2=S1")
    for p in parse_ints(args.small_primes):
        selector_rows, root_rows, base_stats = two_step_rows(p)
        print(f"q{p} base:")
        for key in sorted(base_stats):
            print(f"  {key} = {base_stats[key]}")
        for name, stats in screen_systems(selector_rows, SELECTOR_SYSTEMS, p, requested):
            system = next(system for system in SELECTOR_SYSTEMS if system.name == name)
            print_system(f"q{p} selector", name, stats, degrees_for(system, requested))
        for name, stats in screen_systems(root_rows, ROOT_SYSTEMS, p, root_requested):
            system = next(system for system in ROOT_SYSTEMS if system.name == name)
            print_system(f"q{p} root", name, stats, degrees_for(system, root_requested))
    print("p27_conic_pair_two_step_kummer_trivar_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

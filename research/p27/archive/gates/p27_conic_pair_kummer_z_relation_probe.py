#!/usr/bin/env python3
"""Low-degree relation screen on the first conic-pair Kummer Z layer.

The repeated selector tower gives

    Z^2 = -(L+a)(L-a)cR,  a = R - 1/R.

Raw `(R,L)` and obvious invariant-pair screens are negative.  This probe tests
whether adjoining the first selector root exposes a low-degree quotient in
simple `(invariant, Z)` or normalized-Z coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_conic_pair_invariant_relation_probe import (
    System,
    invariant_values,
    relation_stats_for_system,
)
from p27_conic_pair_lowdegree_relation_probe import sampler_preimages_for_targets
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, legal_sets, sqrt_table


Z_SYSTEMS = [
    System("A_z", ("A", "z"), 14, "target A with selector root"),
    System("x_z", ("x", "z"), 14, "target x with selector root"),
    System("c_z", ("c", "z"), 14, "conic c with selector root"),
    System("r_z", ("r", "z"), 14, "conic r with selector root"),
    System("R_z", ("R", "z"), 14, "next R with selector root"),
    System("L_z", ("L", "z"), 14, "L with selector root"),
    System("s_z", ("s", "z"), 14, "R+1/R with selector root"),
    System("a2_z", ("a2", "z"), 14, "(R-1/R)^2 with selector root"),
    System("m_z", ("m", "z"), 14, "L+a^2/L with selector root"),
    System("n_z", ("n", "z"), 14, "L-a^2/L with selector root"),
    System("w_z", ("w", "z"), 14, "(L+a)(L-a) with selector root"),
    System("s_z_lpa", ("s", "z_lpa"), 14, "Z/(L+a) normalization"),
    System("s_z_lma", ("s", "z_lma"), 14, "Z/(L-a) normalization"),
    System("s_z_cR", ("s", "z_cR"), 14, "Z/(cR) normalization"),
    System("a2_z_lpa", ("a2", "z_lpa"), 14, "Z/(L+a) with a^2"),
    System("a2_z_lma", ("a2", "z_lma"), 14, "Z/(L-a) with a^2"),
    System("m_z_lpa", ("m", "z_lpa"), 14, "Z/(L+a) with m"),
    System("n_z_lma", ("n", "z_lma"), 14, "Z/(L-a) with n"),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def add_normalized_z(values: dict[str, int], z: int, p: int, invs: list[int]) -> dict[str, int | None]:
    out: dict[str, int | None] = dict(values)
    out["z"] = z
    lpa = (values["L"] + values["a"]) % p
    lma = (values["L"] - values["a"]) % p
    cR = values["c"] * values["R"] % p
    w = values["w"] % p
    out["z_lpa"] = z * invs[lpa] % p if lpa else None
    out["z_lma"] = z * invs[lma] % p if lma else None
    out["z_cR"] = z * invs[cR] % p if cR else None
    out["z_w"] = z * invs[w] % p if w else None
    return out


def z_layer_value_rows(p: int) -> tuple[list[dict[str, int | None]], Counter]:
    invs = inv_table(p)
    roots = sqrt_table(p)
    legal_stats, _, d3_plus, d3_minus = legal_sets(p)
    plus_points, plus_stats = sampler_preimages_for_targets(p, d3_plus)
    minus_points, minus_stats = sampler_preimages_for_targets(p, d3_minus)

    stats: Counter = Counter({f"legal_{key}": value for key, value in legal_stats.items()})
    stats.update({f"plus_{key}": value for key, value in plus_stats.items()})
    stats.update({f"minus_{key}": value for key, value in minus_stats.items()})
    stats["minus_unique_preimages"] = len(set(minus_points))

    rows: list[dict[str, int | None]] = []
    for point in plus_points:
        values = invariant_values(point, p, invs)
        if values is None:
            stats["degenerate_invariant"] += 1
            continue
        selector = (-(values["L"] + values["a"]) * (values["L"] - values["a"])) % p
        selector = selector * values["c"] % p * values["R"] % p
        z_roots = roots[selector]
        if not z_roots:
            stats["d4_minus_preimages"] += 1
            continue
        if selector == 0:
            stats["selector_zero_preimages"] += 1
            continue
        stats["d4_plus_preimages"] += 1
        for z in z_roots:
            rows.append(add_normalized_z(values, z, p, invs))
    stats["z_rows"] = len(rows)
    return rows, stats


def transformed_points(
    rows: list[dict[str, int | None]], system: System
) -> tuple[list[tuple[int, ...]], Counter]:
    out: list[tuple[int, ...]] = []
    stats: Counter = Counter()
    for row in rows:
        coords = []
        missing = False
        for name in system.coordinates:
            value = row.get(name)
            if value is None:
                missing = True
                break
            coords.append(int(value))
        if missing:
            stats["degenerate"] += 1
            continue
        out.append(tuple(coords))
    stats["rows"] = len(out)
    stats["unique"] = len(set(out))
    return out, stats


def degrees_for(system: System, requested: list[int] | None) -> list[int]:
    if requested is not None:
        return requested
    return list(range(2, system.max_degree_default + 1, 2))


def screen_field(p: int, systems: list[System], requested_degrees: list[int] | None) -> list[tuple[str, Counter]]:
    rows, base_stats = z_layer_value_rows(p)
    out: list[tuple[str, Counter]] = []
    for system in systems:
        transformed, transform_stats = transformed_points(rows, system)
        stats = Counter(base_stats)
        stats.update({f"transform_{key}": value for key, value in transform_stats.items()})
        stats.update(relation_stats_for_system(transformed, p, degrees_for(system, requested_degrees)))
        out.append((system.name, stats))
    return out


def print_system(prefix: str, system_name: str, stats: Counter, degrees: list[int]) -> None:
    print(f"{prefix} {system_name}:")
    print(f"  z_rows = {stats['z_rows']}")
    print(f"  d4_plus_preimages = {stats['d4_plus_preimages']}")
    print(f"  d4_minus_preimages = {stats['d4_minus_preimages']}")
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
    args = parser.parse_args()

    requested = parse_ints(args.degrees) if args.degrees else None
    print("p27 conic-pair Kummer-Z relation probe")
    print("points = d4-plus roots Z over legal d3-plus conic-pair preimages")
    print("Z^2 = -(L+a)(L-a)cR")
    print("nullity_extra = nullity beyond finite interpolation forced by unique count")
    for p in parse_ints(args.small_primes):
        for system_name, stats in screen_field(p, Z_SYSTEMS, requested):
            system = next(system for system in Z_SYSTEMS if system.name == system_name)
            print_system(f"q{p}", system_name, stats, degrees_for(system, requested))
    print("p27_conic_pair_kummer_z_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

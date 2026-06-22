#!/usr/bin/env python3
"""Frobenius-fiber profile for the p27 no-R reduced B-line cover.

The closed-point pressure says the no-R cover has no affine degree-1 points
over bases 7 and 23, but has degree-2 and degree-3 points.  This probe asks a
more local question: do those points live over base-field B values, or over
extension-degree B orbits, and is the gamma profile stable on Frobenius orbits?

This is a finite-field routing diagnostic for the CAS component/quotient/Prym
pass, not a replacement for normalization.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_localized_cover_layer_count_probe import count_field


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def frobenius_degree(field: GF, value: int) -> int:
    for d in divisors(field.n):
        if field.pow(value, field.p**d) == value:
            return d
    return field.n


def frobenius_orbit(field: GF, value: int) -> tuple[int, ...]:
    orbit = []
    cur = value
    while cur not in orbit:
        orbit.append(cur)
        cur = field.pow(cur, field.p)
    return tuple(sorted(orbit))


def run_field(p: int, n: int) -> None:
    field = GF(p, n)
    _, by_b = count_field(field)

    degree_stats: defaultdict[int, Counter] = defaultdict(Counter)
    pair_by_degree: defaultdict[int, Counter] = defaultdict(Counter)
    orbits: defaultdict[tuple[int, ...], list[tuple[int, Counter]]] = defaultdict(list)

    for b_value, row in by_b.items():
        degree = frobenius_degree(field, b_value)
        noR = row["noR_reduced_U_points"]
        gamma = row["noR_gamma_points"]
        active = noR > 0
        gamma_active = gamma > 0
        degree_stats[degree]["B_fibers"] += 1
        degree_stats[degree]["active_B_fibers"] += int(active)
        degree_stats[degree]["gamma_active_B_fibers"] += int(gamma_active)
        degree_stats[degree]["noR_points"] += noR
        degree_stats[degree]["gamma_points"] += gamma
        pair_by_degree[degree][(noR, gamma)] += 1
        orbits[frobenius_orbit(field, b_value)].append((b_value, row))

    orbit_stats: Counter = Counter()
    mismatched_orbits = 0
    active_orbits = 0
    for orbit, rows in orbits.items():
        signatures = {
            (
                row["valid_X"],
                row["noR_reduced_U_points"],
                row["noR_gamma_points"],
                row["full_reduced_U_points"],
                row["full_gamma_points"],
            )
            for _, row in rows
        }
        degree = len(orbit)
        noR_total = sum(row["noR_reduced_U_points"] for _, row in rows)
        gamma_total = sum(row["noR_gamma_points"] for _, row in rows)
        if noR_total:
            active_orbits += 1
        if len(signatures) != 1:
            mismatched_orbits += 1
        orbit_stats[(degree, len(rows), noR_total, gamma_total, len(signatures))] += 1

    print(f"GF({p}^{n}) q={field.q}")
    print(f"  B_fibers = {len(by_b)}")
    print(f"  Frobenius_B_orbits = {len(orbits)}")
    print(f"  active_Frobenius_B_orbits = {active_orbits}")
    print(f"  orbit_signature_mismatches = {mismatched_orbits}")
    for degree in sorted(degree_stats):
        row = degree_stats[degree]
        print(
            f"  degree_{degree}: B={row['B_fibers']} active={row['active_B_fibers']} "
            f"gamma_active={row['gamma_active_B_fibers']} noR={row['noR_points']} "
            f"gamma={row['gamma_points']}"
        )
        for (noR, gamma), count in pair_by_degree[degree].most_common(12):
            print(f"    pair_noR_gamma_({noR},{gamma}) = {count}")
    print("  orbit_summary_top:")
    for (degree, rows_seen, noR_total, gamma_total, sig_count), count in orbit_stats.most_common(16):
        print(
            f"    orbit(deg={degree}, rows={rows_seen}, noR={noR_total}, "
            f"gamma={gamma_total}, sigs={sig_count}) = {count}"
        )
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="7^2,7^3,23^2,23^3")
    args = parser.parse_args()

    print("p27 B-line no-R Frobenius fiber probe")
    print("interpretation = extension-degree B-fiber routing for no-R/gamma")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_frobenius_fiber_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

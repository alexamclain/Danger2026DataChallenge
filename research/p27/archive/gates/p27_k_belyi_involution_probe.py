#!/usr/bin/env python3
"""Belyi involution audit for the p27 K/S quotient route.

The K-line map has branch set {0, infinity, K^2+4=0}.  Over the algebraic
closure this branch set has extra involutions; over the p27 sign regime the
base-field-visible ones include

    K -> -K,  K -> 4/K,  K -> -4/K.

If d3 descends through one of these orbits, the K/S extraction target gets
smaller.  If the selected doubled stratum is not closed under them, then the
Belyi coordinate is only normalization data, not a further rational sampler.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_eprime_double_kummer_line_probe import KRow, to_krows
from p27_equotient_2isogeny_line_probe import quotient_rows
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_sroot_branch_divisor_probe import SRow, to_srows


@dataclass(frozen=True)
class Transform:
    name: str
    fn: Callable[[int, int], int | None]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def k_transforms() -> list[Transform]:
    return [
        Transform("K", lambda k, p: k % p),
        Transform("-K", lambda k, p: (-k) % p),
        Transform("4/K", lambda k, p: None if inv(k, p) is None else 4 * inv(k, p) % p),
        Transform("-4/K", lambda k, p: None if inv(k, p) is None else -4 * inv(k, p) % p),
    ]


def s_transforms() -> list[Transform]:
    return [
        Transform("S", lambda s, p: s % p),
        Transform("-S", lambda s, p: (-s) % p),
        Transform("2/S", lambda s, p: None if inv(s, p) is None else 2 * inv(s, p) % p),
        Transform("-2/S", lambda s, p: None if inv(s, p) is None else -2 * inv(s, p) % p),
    ]


def collect_rows(q: int) -> tuple[list[KRow], list[KRow], list[SRow], list[SRow], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    d3_rows, d4_rows, quotient_stats = quotient_bit_rows_from_candidates(candidates, q)
    qd3, d3_iso_stats = quotient_rows(d3_rows, q)
    qd4, d4_iso_stats = quotient_rows(d4_rows, q)
    kd3, d3_k_stats = to_krows(qd3, q)
    kd4, d4_k_stats = to_krows(qd4, q)
    sd3, d3_s_stats = to_srows(qd3, q)
    sd4, d4_s_stats = to_srows(qd4, q)
    stats: Counter = Counter()
    stats.update({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    stats.update({f"d3_eprime_{key}": value for key, value in d3_iso_stats.items()})
    stats.update({f"d4_eprime_{key}": value for key, value in d4_iso_stats.items()})
    stats.update({f"d3_k_{key}": value for key, value in d3_k_stats.items()})
    stats.update({f"d4_k_{key}": value for key, value in d4_k_stats.items()})
    stats.update({f"d3_s_{key}": value for key, value in d3_s_stats.items()})
    stats.update({f"d4_s_{key}": value for key, value in d4_s_stats.items()})
    return kd3, kd4, sd3, sd4, stats


def row_stats_k(rows: list[KRow], q: int) -> Counter:
    stats: Counter = Counter()
    for row in rows:
        stats["rows"] += 1
        stats[f"chi_K_{legendre(row.k, q)}"] += 1
        stats[f"chi_K2p4_{legendre((row.k * row.k + 4) % q, q)}"] += 1
        stats[f"target_{row.target}"] += 1
    return stats


def row_stats_s(rows: list[SRow], q: int) -> Counter:
    stats: Counter = Counter()
    for row in rows:
        stats["rows"] += 1
        stats[f"chi_S_{legendre(row.s, q)}"] += 1
        stats[f"chi_S2m2Sp2_{legendre((row.s * row.s - 2 * row.s + 2) % q, q)}"] += 1
        stats[f"chi_S2p2Sp2_{legendre((row.s * row.s + 2 * row.s + 2) % q, q)}"] += 1
        stats[f"target_{row.target}"] += 1
    return stats


def transform_stats(values: dict[int, int], q: int, transforms: list[Transform]) -> Counter:
    stats: Counter = Counter()
    for transform in transforms:
        paired_seen: set[tuple[int, int]] = set()
        for value, target in values.items():
            image = transform.fn(value, q)
            if image is None:
                stats[f"{transform.name}_undefined"] += 1
                continue
            image %= q
            if image not in values:
                stats[f"{transform.name}_missing"] += 1
                continue
            image_target = values[image]
            stats[f"{transform.name}_present"] += 1
            if image_target == target:
                stats[f"{transform.name}_same"] += 1
            else:
                stats[f"{transform.name}_opposite"] += 1
            pair = tuple(sorted((value, image)))
            if pair not in paired_seen:
                paired_seen.add(pair)
                stats[f"{transform.name}_orbit_pairs"] += 1
                if image_target == target:
                    stats[f"{transform.name}_same_orbit_pairs"] += 1
                else:
                    stats[f"{transform.name}_opposite_orbit_pairs"] += 1
    return stats


def group_orbit_stats(values: dict[int, int], q: int, transforms: list[Transform]) -> Counter:
    stats: Counter = Counter()
    unseen = set(values)
    while unseen:
        start = unseen.pop()
        orbit = {start}
        frontier = [start]
        while frontier:
            value = frontier.pop()
            for transform in transforms:
                image = transform.fn(value, q)
                if image is None or image not in values:
                    continue
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
                    unseen.discard(image)
        targets = {values[value] for value in orbit}
        stats["orbits"] += 1
        stats[f"orbit_size_{len(orbit)}"] += 1
        if len(targets) == 1:
            stats["constant_target_orbits"] += 1
        else:
            stats["mixed_target_orbits"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_family(label: str, rows: list[KRow] | list[SRow], q: int, coordinate: str) -> None:
    if coordinate == "K":
        values = {row.k: row.target for row in rows}  # type: ignore[attr-defined]
        transforms = k_transforms()
        print_counter(f"{label}_row_stats", row_stats_k(rows, q))  # type: ignore[arg-type]
    else:
        values = {row.s: row.target for row in rows}  # type: ignore[attr-defined]
        transforms = s_transforms()
        print_counter(f"{label}_row_stats", row_stats_s(rows, q))  # type: ignore[arg-type]
    print_counter(f"{label}_transform_stats", transform_stats(values, q, transforms))
    print_counter(f"{label}_group_orbit_stats", group_orbit_stats(values, q, transforms))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    args = parser.parse_args()

    print("p27 K/S Belyi involution audit")
    print("K transforms = K, -K, 4/K, -4/K")
    print("S transforms = S, -S, 2/S, -2/S")
    print("promotion = closure plus invariant/anti-invariant target on d3")
    for q in parse_ints(args.small_primes):
        kd3, kd4, sd3, sd4, setup_stats = collect_rows(q)
        print(f"q={q}:")
        print(f"  q_mod_8 = {q % 8}")
        print(f"  chi_minus_one = {legendre(-1, q)}")
        print_counter("  setup_stats", setup_stats)
        run_family(f"  q{q}_d3_K", kd3, q, "K")
        run_family(f"  q{q}_d4_K", kd4, q, "K")
        run_family(f"  q{q}_d3_S", sd3, q, "S")
        run_family(f"  q{q}_d4_S", sd4, q, "S")
    print("p27_k_belyi_involution_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

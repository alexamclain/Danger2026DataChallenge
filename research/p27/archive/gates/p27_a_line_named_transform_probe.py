#!/usr/bin/env python3
"""Restricted named-transform screen for p27 A-line selected classes.

The A-level prefix descent is real, but visible low-degree branch support on
P1_A is killed.  This probe tests the next cheapest possible escape hatch:
whether the selected A-classes are related by the small S3 group preserving the
visible A-branch set {-2, 2, infinity}.

This is deliberately not a generic PGL2 fit.  The transforms are fixed before
looking at the labels.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_a_level_prefix_descent_probe import (
    collect_field_ax,
    collect_p27_ax,
    parse_ints,
)
from p27_a_line_character_support_probe import target_rows
from p27_label2_alpha_branch_recurrence_probe import P


LabelMap = dict[int, int]


@dataclass(frozen=True)
class Transform:
    name: str
    formula: str
    fn: Callable[[int, int], int | None]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def branch_s3_transforms() -> list[Transform]:
    """Return S3 on z=(A+2)/4, branch set A in {-2, 2, infinity}."""

    return [
        Transform("id", "A", lambda a, p: a % p),
        Transform("swap_pm2", "2-A", lambda a, p: (2 - a) % p),
        Transform(
            "inv_minus2",
            "16/(A+2)-2",
            lambda a, p: None if inv(a + 2, p) is None else (16 * inv(a + 2, p) - 2) % p,
        ),
        Transform(
            "inv_plus2",
            "16/(2-A)-2",
            lambda a, p: None if inv(2 - a, p) is None else (16 * inv(2 - a, p) - 2) % p,
        ),
        Transform(
            "z_over_zminus1",
            "2*(A+6)/(A-2)",
            lambda a, p: None if inv(a - 2, p) is None else (2 * (a + 6) * inv(a - 2, p)) % p,
        ),
        Transform(
            "zminus1_over_z",
            "2*(A-6)/(A+2)",
            lambda a, p: None if inv(a + 2, p) is None else (2 * (a - 6) * inv(a + 2, p)) % p,
        ),
    ]


def row_label(bit: int) -> int:
    return 1 if bit == 0 else -1


def gate_maps(ax_points: set[tuple[int, int]], p: int, depth: int, min_rows: int) -> tuple[dict[int, LabelMap], Counter]:
    maps: dict[int, LabelMap] = {}
    stats: Counter = Counter()
    stats["base_A"] = len({A for A, _x in ax_points})
    stats["base_ax"] = len(ax_points)
    for gate in range(3, depth + 3):
        rows, row_stats = target_rows(ax_points, p, gate, depth)
        stats[f"d{gate}_rows"] = len(rows)
        stats[f"d{gate}_plus"] = row_stats["plus_A"]
        stats[f"d{gate}_minus"] = row_stats["minus_A"]
        stats[f"d{gate}_mixed"] = row_stats["mixed_A_groups"]
        if len(rows) >= min_rows or gate <= 4:
            maps[gate] = {A % p: row_label(bit) for A, bit in rows}
    return maps, stats


def transform_gate_stats(domain: LabelMap, base_domain: set[int], p: int, transforms: list[Transform]) -> Counter:
    stats: Counter = Counter()
    for transform in transforms:
        for A, label in domain.items():
            image = transform.fn(A, p)
            if image is None:
                stats[f"{transform.name}_undefined"] += 1
                continue
            image %= p
            if image in base_domain:
                stats[f"{transform.name}_image_in_base"] += 1
            else:
                stats[f"{transform.name}_image_out_base"] += 1
            if image not in domain:
                stats[f"{transform.name}_image_out_same_gate"] += 1
                continue
            stats[f"{transform.name}_image_in_same_gate"] += 1
            if domain[image] == label:
                stats[f"{transform.name}_same_label"] += 1
            else:
                stats[f"{transform.name}_opposite_label"] += 1
    return stats


def compare_successive_stats(
    current: LabelMap,
    previous: LabelMap,
    p: int,
    transforms: list[Transform],
) -> Counter:
    stats: Counter = Counter()
    for transform in transforms:
        same = 0
        opposite = 0
        covered = 0
        for A, label in current.items():
            image = transform.fn(A, p)
            if image is None:
                stats[f"{transform.name}_undefined"] += 1
                continue
            image %= p
            if image not in previous:
                stats[f"{transform.name}_uncovered"] += 1
                continue
            covered += 1
            if previous[image] == label:
                same += 1
            else:
                opposite += 1
        stats[f"{transform.name}_covered"] = covered
        stats[f"{transform.name}_same"] = same
        stats[f"{transform.name}_opposite"] = opposite
        stats[f"{transform.name}_best_polarity_hits"] = max(same, opposite)
    return stats


def orbit_stats(domain: LabelMap, p: int, transforms: list[Transform]) -> Counter:
    stats: Counter = Counter()
    unseen = set(domain)
    while unseen:
        start = unseen.pop()
        orbit = {start}
        frontier = [start]
        while frontier:
            A = frontier.pop()
            for transform in transforms:
                image = transform.fn(A, p)
                if image is None:
                    continue
                image %= p
                if image not in domain or image in orbit:
                    continue
                orbit.add(image)
                frontier.append(image)
                unseen.discard(image)
        stats["orbits"] += 1
        stats[f"orbit_size_{len(orbit)}"] += 1
        labels = {domain[A] for A in orbit}
        if len(labels) == 1:
            stats["constant_label_orbits"] += 1
        else:
            stats["mixed_label_orbits"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_transform_table(transforms: list[Transform]) -> None:
    print("transforms:")
    for transform in transforms:
        print(f"  {transform.name}: {transform.formula}")


def run_dataset(label: str, ax_points: set[tuple[int, int]], p: int, depth: int, min_rows: int) -> None:
    transforms = branch_s3_transforms()
    maps, stats = gate_maps(ax_points, p, depth, min_rows)
    base_domain = set(maps.get(3, {}))
    print_counter(f"{label}_gate_map_stats", stats)
    print(f"{label}_maps_kept: {','.join('d' + str(gate) for gate in sorted(maps))}")

    for gate in sorted(maps):
        print_counter(
            f"{label}_d{gate}_same_gate_transform_stats",
            transform_gate_stats(maps[gate], base_domain, p, transforms),
        )
        print_counter(
            f"{label}_d{gate}_orbit_stats",
            orbit_stats(maps[gate], p, transforms),
        )

    for gate in sorted(maps):
        if gate - 1 not in maps:
            continue
        print_counter(
            f"{label}_d{gate}_vs_d{gate - 1}_transform_stats",
            compare_successive_stats(maps[gate], maps[gate - 1], p, transforms),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=8)
    parser.add_argument("--p27-target", type=int, default=0)
    parser.add_argument("--p27-heldout-target", type=int, default=0)
    parser.add_argument("--p27-max-draws", type=int, default=3000000)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    args = parser.parse_args()

    print("p27 A-line named-transform probe")
    print("question = do visible A-branch S3 transforms preserve/relate selected A classes?")
    print("branch set = {-2, 2, infinity}")
    print_transform_table(branch_s3_transforms())
    print(f"depth = {args.depth}")
    print(f"min_rows = {args.min_rows}")

    for q in parse_ints(args.small_primes):
        ax_points, base_stats = collect_field_ax(q)
        print_counter(f"q{q}_base", base_stats)
        run_dataset(f"q{q}", ax_points, q, args.depth, args.min_rows)

    if args.p27_target:
        ax_points, base_stats = collect_p27_ax(args.p27_target, args.p27_seed, args.p27_max_draws)
        print_counter("p27_train_base", base_stats)
        run_dataset("p27_train", ax_points, P, args.depth, args.min_rows)

    if args.p27_heldout_target:
        ax_points, base_stats = collect_p27_ax(
            args.p27_heldout_target,
            args.p27_heldout_seed,
            args.p27_max_draws,
        )
        print_counter("p27_heldout_base", base_stats)
        run_dataset("p27_heldout", ax_points, P, args.depth, args.min_rows)

    print("p27_a_line_named_transform_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

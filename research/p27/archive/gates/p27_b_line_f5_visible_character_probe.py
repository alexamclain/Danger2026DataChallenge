#!/usr/bin/env python3
"""Visible B-character screen for mixed-f5 guard fields.

The mixed-f5 transition guard showed that, on selected f4=+1 B rows,
chi(W+2) agrees exactly with f5(B).  This probe asks the cheapest follow-up:
is that mixed f5(B) sign just a visible low-degree character on P1_B?

It tests named B atoms and split linear branch support of degree <= 2.  It is
not a broad coefficient search.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from p27_b_line_branch_support_probe import factor_columns, mask_for_rows, popcount
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_kline_reverse_z_relation_probe import parse_ints


DEFAULT_KUMMER = Path("research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json")


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def atom_functions(p: int) -> list[tuple[str, Callable[[int], int | None]]]:
    return [
        ("B", lambda b: b),
        ("B+2", lambda b: (b + 2) % p),
        ("B-2", lambda b: (b - 2) % p),
        ("B+4", lambda b: (b + 4) % p),
        ("B-4", lambda b: (b - 4) % p),
        ("B^2-4", lambda b: (b * b - 4) % p),
        ("B^2+4", lambda b: (b * b + 4) % p),
        ("B^2+2B+4", lambda b: (b * b + 2 * b + 4) % p),
        ("B^2-2B+4", lambda b: (b * b - 2 * b + 4) % p),
        ("B/(B+2)", lambda b: None if inv(b + 2, p) is None else b * inv(b + 2, p) % p),
        ("(B-2)/(B+2)", lambda b: None if inv(b + 2, p) is None else (b - 2) * inv(b + 2, p) % p),
    ]


def sign_bit(label: str) -> int:
    if label == "plus":
        return 0
    if label == "minus":
        return 1
    raise ValueError(label)


def load_field(packet: dict[str, Any], q: int) -> dict[str, Any]:
    for fixture in packet["fixtures"]:
        if int(fixture["field"]) == q:
            return fixture
    raise KeyError(q)


def family_rows(field: dict[str, Any], name: str) -> list[tuple[int, int]]:
    for family in field["families"]:
        if family["name"] == name:
            rows = []
            for row in family["rows"]:
                label = str(row["sign"])
                if label not in ("plus", "minus"):
                    continue
                rows.append((int(row["B"]), sign_bit(label)))
            return rows
    raise KeyError(name)


def mask_for_atom(rows: list[tuple[int, int]], p: int, fn: Callable[[int], int | None]) -> int | None:
    mask = 0
    for idx, (b, _bit) in enumerate(rows):
        value = fn(b)
        if value is None:
            return None
        chi = legendre(value % p, p)
        if chi == 0:
            return None
        if chi == -1:
            mask |= 1 << idx
    return mask


def distance(mask: int, target: int, full: int) -> tuple[int, int]:
    direct = popcount(mask ^ target)
    flipped = popcount((mask ^ full) ^ target)
    if direct <= flipped:
        return direct, 1
    return flipped, -1


def atom_screen(rows: list[tuple[int, int]], p: int) -> tuple[Counter, str, int, int]:
    stats: Counter = Counter()
    target = mask_for_rows(rows)
    full = (1 << len(rows)) - 1
    best_label = "none"
    best_distance = len(rows) + 1
    best_polarity = 1
    exact_label = "none"
    for label, fn in atom_functions(p):
        mask = mask_for_atom(rows, p, fn)
        if mask is None:
            stats["zero_or_pole_skip"] += 1
            continue
        stats["tested"] += 1
        dist, polarity = distance(mask, target, full)
        if dist < best_distance:
            best_label = label
            best_distance = dist
            best_polarity = polarity
        if dist == 0 and exact_label == "none":
            exact_label = f"{'-' if polarity == -1 else ''}{label}"
    return stats, exact_label, best_distance, best_polarity


def split_linear_degree2(rows: list[tuple[int, int]], p: int) -> tuple[Counter, str, int, int]:
    stats: Counter = Counter()
    target = mask_for_rows(rows)
    full = (1 << len(rows)) - 1
    cols = factor_columns(p, rows)
    stats["linear_factors"] = len(cols)
    masks: dict[int, int] = {}
    best_label = "none"
    best_distance = len(rows) + 1
    best_polarity = 1
    exact_label = "none"

    for a, mask in cols:
        masks.setdefault(mask, a)
        dist, polarity = distance(mask, target, full)
        if dist < best_distance:
            best_label = f"B-{a}"
            best_distance = dist
            best_polarity = polarity
        if dist == 0 and exact_label == "none":
            exact_label = f"{'-' if polarity == -1 else ''}B-{a}"

    for a, mask in cols:
        for desired, polarity in ((target, 1), (target ^ full, -1)):
            need = mask ^ desired
            b = masks.get(need)
            if b is None or b == a:
                continue
            exact_label = f"{'-' if polarity == -1 else ''}(B-{a})*(B-{b})"
            stats["degree2_exact"] = 1
            return stats, exact_label, 0, polarity

    stats["degree2_exact"] = 0
    return stats, exact_label, best_distance, best_polarity


def run_field(packet: dict[str, Any], q: int) -> None:
    field = load_field(packet, q)
    rows = family_rows(field, "f5_conditional")
    stats: Counter = Counter()
    stats["rows"] = len(rows)
    stats["plus_rows"] = sum(1 for _b, bit in rows if bit == 0)
    stats["minus_rows"] = sum(1 for _b, bit in rows if bit == 1)
    target = mask_for_rows(rows)
    stats["target_weight"] = popcount(target)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    if not rows or stats["plus_rows"] == 0 or stats["minus_rows"] == 0:
        print("  skipped = one_sided_or_empty")
        return

    atom_stats, atom_exact, atom_best_dist, atom_best_polarity = atom_screen(rows, q)
    print("  atom_screen:")
    print(f"    tested = {atom_stats['tested']}")
    print(f"    zero_or_pole_skip = {atom_stats['zero_or_pole_skip']}")
    print(f"    exact = {atom_exact}")
    print(f"    best_distance = {atom_best_dist}")
    print(f"    best_polarity = {atom_best_polarity}")

    linear_stats, linear_exact, linear_best_dist, linear_best_polarity = split_linear_degree2(rows, q)
    print("  split_linear_degree_le_2:")
    print(f"    linear_factors = {linear_stats['linear_factors']}")
    print(f"    degree2_exact = {linear_stats['degree2_exact']}")
    print(f"    exact = {linear_exact}")
    print(f"    best_single_linear_distance = {linear_best_dist}")
    print(f"    best_single_linear_polarity = {linear_best_polarity}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="4999,5783,6007,6247")
    parser.add_argument("--kummer-fixture", type=Path, default=DEFAULT_KUMMER)
    args = parser.parse_args()

    packet = json.loads(args.kummer_fixture.read_text())
    print("p27 B-line f5 visible character probe")
    print("target = f5(B) on mixed-f5 selected f4-plus guard fields")
    print("families = named atoms; split linear support degree <= 2")
    print(f"kummer_fixture = {args.kummer_fixture}")
    for q in parse_ints(args.small_primes):
        run_field(packet, q)
    print("p27_b_line_f5_visible_character_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

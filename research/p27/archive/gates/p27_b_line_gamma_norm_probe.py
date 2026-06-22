#!/usr/bin/env python3
"""Norm/coboundary screen for the staged B-line gamma class.

After the transition/orientation probe, the live second-gate class is

    gamma^2 = v + 2

on the staged cover

    F_A(u,v)=0,  rho^2=v^2-4.

This probe checks what the gamma norm sees on each actual materialized
two-root pair over a fixed (B,u).  If the norm is already an old square, then
the remaining f4 bit is a Hilbert-90/coboundary-style orientation class, not a
plain norm character.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
from typing import Callable, Optional

from p27_b_line_transition_closure_probe import (
    DEFAULT_FIRST,
    collect_actual_edges,
    load_field,
    transition_roots,
)
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre


AtomFn = Callable[[dict[str, int], int], Optional[int]]


def inv(a: int, p: int) -> Optional[int]:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def product(values: list[int], p: int) -> int:
    out = 1
    for value in values:
        out = out * (value % p) % p
    return out


def x_roots_for_u(row: dict, u: int, p: int) -> set[int]:
    roots = set()
    for raw_x in row["x_roots"]:
        x = int(raw_x) % p
        if x and (x + pow(x, p - 2, p)) % p == u % p:
            roots.add(x)
    return roots


def build_rows(q: int, first: dict) -> tuple[list[dict[str, int]], Counter]:
    first_field = load_field(first, q)
    actual_edges, _actual_by_b, edge_stats = collect_actual_edges(q)
    rows: list[dict[str, int]] = []
    stats: Counter = Counter(edge_stats)

    for fixture_row in first_field["rows"]:
        if str(fixture_row["sign"]) != "plus":
            continue
        B = int(fixture_row["B"]) % q
        A = (B * B - 2) % q
        for raw_u in fixture_row["u_roots"]:
            u = int(raw_u) % q
            actual = sorted(actual_edges.get((B, u), set()))
            generic = sorted(transition_roots(A, u, q))
            if len(actual) != 2 or len(generic) != 4:
                stats["bad_pair_shape"] += 1
                continue
            missing = [v for v in generic if v not in actual]
            if len(missing) != 2:
                stats["bad_missing_shape"] += 1
                continue
            x_roots = x_roots_for_u(fixture_row, u, q)
            if len(x_roots) != 2:
                stats["bad_x_roots_for_u"] += 1
                continue

            gamma_actual = product([(v + 2) % q for v in actual], q)
            gamma_missing = product([(v + 2) % q for v in missing], q)
            gamma_generic = product([(v + 2) % q for v in generic], q)
            denom = (4 * (2 - A)) % q
            denom_inv = inv(denom, q)
            if denom_inv is None:
                stats["zero_denom_4_2minusA"] += 1
                continue
            actual_scale = gamma_actual * denom_inv % q
            missing_scale = gamma_missing * denom_inv % q
            f4 = legendre((actual[0] + 2) % q, q)
            if any(legendre((v + 2) % q, q) != f4 for v in actual + missing):
                stats["gamma_not_constant_on_generic"] += 1

            rows.append(
                {
                    "B": B,
                    "A": A,
                    "u": u,
                    "v_sum": sum(actual) % q,
                    "v_prod": product(actual, q),
                    "v_disc": ((actual[0] - actual[1]) ** 2) % q,
                    "missing_sum": sum(missing) % q,
                    "missing_prod": product(missing, q),
                    "gamma_actual_norm": gamma_actual,
                    "gamma_missing_norm": gamma_missing,
                    "gamma_generic_norm": gamma_generic,
                    "actual_scale": actual_scale,
                    "missing_scale": missing_scale,
                    "f4": f4,
                    "x_roots": sorted(x_roots),
                }
            )

    stats["norm_rows"] = len(rows)
    stats["f4_plus"] = sum(1 for row in rows if row["f4"] == 1)
    stats["f4_minus"] = sum(1 for row in rows if row["f4"] == -1)
    return rows, stats


def atoms() -> list[tuple[str, AtomFn]]:
    out: list[tuple[str, AtomFn]] = []

    def add(name: str, fn: AtomFn) -> None:
        out.append((name, fn))

    for key in (
        "B",
        "A",
        "u",
        "v_sum",
        "v_prod",
        "v_disc",
        "missing_sum",
        "missing_prod",
        "gamma_actual_norm",
        "gamma_missing_norm",
        "gamma_generic_norm",
        "actual_scale",
        "missing_scale",
    ):
        add(key, lambda row, _p, kk=key: row[kk])

    for key in ("B", "A", "u", "v_sum", "v_prod", "actual_scale", "missing_scale"):
        for c in (-4, -2, -1, 1, 2, 4):
            add(f"{key}{c:+d}", lambda row, p, kk=key, cc=c: (row[kk] + cc) % p)

    add("A-2", lambda row, p: (row["A"] - 2) % p)
    add("2-A", lambda row, p: (2 - row["A"]) % p)
    add("B2-4", lambda row, p: (row["B"] * row["B"] - 4) % p)
    add("4-B2", lambda row, p: (4 - row["B"] * row["B"]) % p)
    add("u2-4", lambda row, p: (row["u"] * row["u"] - 4) % p)
    add("vsum2-4vprod", lambda row, p: (row["v_sum"] * row["v_sum"] - 4 * row["v_prod"]) % p)
    return out


def mask_from_signs(signs: list[int]) -> int:
    mask = 0
    for i, sign in enumerate(signs):
        if sign == -1:
            mask |= 1 << i
    return mask


def popcount(value: int) -> int:
    return bin(value).count("1")


def score_mask(mask: int, target: int, full: int) -> tuple[int, int]:
    matches = popcount(mask ^ target ^ full)
    opposite = popcount((mask ^ full) ^ target ^ full)
    return matches, opposite


def screen_pair_invariants(rows: list[dict[str, int]], q: int, max_weight: int, keep_best: int) -> tuple[Counter, list[str]]:
    stats: Counter = Counter()
    notes: list[str] = []
    full = (1 << len(rows)) - 1
    target = mask_from_signs([row["f4"] for row in rows])
    atom_masks: list[tuple[str, int]] = []
    for name, fn in atoms():
        signs = []
        zero_or_undefined = 0
        for row in rows:
            value = fn(row, q)
            if value is None:
                zero_or_undefined += 1
                signs.append(0)
                continue
            chi = legendre(value, q)
            if chi == 0:
                zero_or_undefined += 1
            signs.append(chi)
        if zero_or_undefined:
            stats[f"atom_{name}_zero_or_undefined"] = zero_or_undefined
            continue
        atom_masks.append((name, mask_from_signs(signs)))

    best: list[tuple[int, int, tuple[str, ...], int]] = []
    exact: list[tuple[int, int, tuple[str, ...], int]] = []
    for weight in range(1, max_weight + 1):
        for combo in combinations(atom_masks, weight):
            mask = 0
            names = tuple(name for name, _mask in combo)
            for _name, atom_mask in combo:
                mask ^= atom_mask
            matches, opposite = score_mask(mask, target, full)
            best_matches = max(matches, opposite)
            polarity = 1 if matches >= opposite else -1
            item = (best_matches, weight, names, polarity)
            best.append(item)
            if best_matches == len(rows):
                exact.append(item)
    best.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    stats["pair_atoms_usable"] = len(atom_masks)
    stats["pair_products_tested"] = len(best)
    stats["pair_exact_products"] = len(exact)
    if best:
        stats["pair_best_matches"] = best[0][0]
        stats["pair_best_match_x1000000"] = best[0][0] * 1_000_000 // len(rows)
        stats["pair_best_weight"] = best[0][1]

    notes.append("  exact_pair_invariant_products:")
    if exact:
        for matches, weight, names, polarity in exact[:keep_best]:
            notes.append(f"    weight={weight} polarity={polarity} atoms={' * '.join(names)}")
    else:
        notes.append("    none")
    notes.append("  best_pair_invariant_products:")
    for matches, weight, names, polarity in best[:keep_best]:
        notes.append(
            f"    matches={matches}/{len(rows)} polarity={polarity} "
            f"weight={weight} atoms={' * '.join(names)}"
        )
    return stats, notes


def run_field(q: int, first: dict, max_weight: int, keep_best: int) -> None:
    rows, stats = build_rows(q, first)
    expected_generic_bad = 0
    scale_miss = 0
    scale_nonsquare = 0
    norm_nonsquare = 0
    for row in rows:
        A = row["A"]
        expected = 16 * (A - 2) * (A - 2) % q
        if row["gamma_generic_norm"] != expected:
            expected_generic_bad += 1
        if row["actual_scale"] not in row["x_roots"]:
            scale_miss += 1
        if row["missing_scale"] not in row["x_roots"]:
            scale_miss += 1
        if legendre(row["actual_scale"], q) != 1 or legendre(row["missing_scale"], q) != 1:
            scale_nonsquare += 1
        if legendre(row["gamma_actual_norm"], q) != 1 or legendre(row["gamma_missing_norm"], q) != 1:
            norm_nonsquare += 1

    stats["generic_gamma_norm_formula_bad"] = expected_generic_bad
    stats["actual_or_missing_scale_not_xroot"] = scale_miss
    stats["actual_or_missing_scale_nonsquare"] = scale_nonsquare
    stats["actual_or_missing_gamma_norm_nonsquare"] = norm_nonsquare
    pair_stats, pair_notes = screen_pair_invariants(rows, q, max_weight, keep_best)
    stats.update(pair_stats)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for note in pair_notes:
        print(note)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--keep-best", type=int, default=12)
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    print("p27 B-line gamma norm/coboundary probe")
    print("question = does gamma^2=v+2 have only old-square norm over the materialized pair?")
    print(f"first_fixture = {args.first_fixture}")
    print(f"max_weight = {args.max_weight}")
    for q in parse_ints(args.small_primes):
        run_field(q, first, args.max_weight, args.keep_best)
    print("p27_b_line_gamma_norm_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

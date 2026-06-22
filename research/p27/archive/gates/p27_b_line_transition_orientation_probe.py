#!/usr/bin/env python3
"""Screen visible squareclasses for the B-line transition orientation half.

The transition closure probe shows that, for each legal f3-plus pair (B,u),
the generic quotient halving transition has four v roots, while the actual
selected source uses exactly two.  This probe asks whether that 2-of-4
orientation choice is a visible low-weight product of natural rational
squareclasses in B, u, and v.

A positive would be a real source/sampler lead.  A negative says the missing
half is not exposed by the obvious quotient atoms and should be handled as a
non-visible orientation/Kummer class.
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


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def maybe_div(num: int, den: int, p: int) -> int | None:
    iden = inv(den, p)
    if iden is None:
        return None
    return num % p * iden % p


def transition_derivative(A: int, u: int, v: int, p: int) -> int:
    n = (v * v - 4) % p
    d = (v + A) % p
    return (4 * v * n - 4 * u * ((2 * v * d + n) % p) + 32 * d) % p


def row_context(B: int, u: int, v: int, p: int) -> dict[str, int]:
    A = (B * B - 2) % p
    n = (v * v - 4) % p
    d = (v + A) % p
    x = maybe_div(n, 4 * d, p)
    return {
        "B": B % p,
        "A": A,
        "u": u % p,
        "v": v % p,
        "n": n,
        "d": d,
        "x": -1 if x is None else x,
        "Fv": transition_derivative(A, u, v, p),
    }


def atoms() -> list[tuple[str, AtomFn]]:
    out: list[tuple[str, AtomFn]] = []

    def add(name: str, fn: AtomFn) -> None:
        out.append((name, fn))

    for key in ("B", "A", "u", "v", "n", "d", "x", "Fv"):
        add(key, lambda row, _p, kk=key: None if row[kk] < 0 else row[kk])

    for key in ("v", "x"):
        for c in (-4, -2, -1, 1, 2, 4):
            add(f"{key}{c:+d}", lambda row, p, kk=key, cc=c: None if row[kk] < 0 else (row[kk] + cc) % p)

    for left, right in (
        ("v", "A"),
        ("v", "B"),
        ("v", "u"),
        ("x", "A"),
        ("x", "B"),
        ("x", "u"),
        ("n", "d"),
    ):
        add(f"{left}+{right}", lambda row, p, ll=left, rr=right: None if row[ll] < 0 or row[rr] < 0 else (row[ll] + row[rr]) % p)
        add(f"{left}-{right}", lambda row, p, ll=left, rr=right: None if row[ll] < 0 or row[rr] < 0 else (row[ll] - row[rr]) % p)

    add("v2+A*v+1", lambda row, p: (row["v"] * row["v"] + row["A"] * row["v"] + 1) % p)
    add("v2-A*v+1", lambda row, p: (row["v"] * row["v"] - row["A"] * row["v"] + 1) % p)
    add("v2-A2", lambda row, p: (row["v"] * row["v"] - row["A"] * row["A"]) % p)
    add("u2-4", lambda row, p: (row["u"] * row["u"] - 4) % p)
    add("B2-4", lambda row, p: (row["B"] * row["B"] - 4) % p)
    return out


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
            generic = transition_roots(A, u, q)
            actual = actual_edges.get((B, u), set())
            for v in sorted(generic):
                row = row_context(B, u, v, q)
                row["target"] = 1 if v in actual else -1
                rows.append(row)

    stats["orientation_rows"] = len(rows)
    stats["orientation_actual"] = sum(1 for row in rows if row["target"] == 1)
    stats["orientation_missing"] = sum(1 for row in rows if row["target"] == -1)
    return rows, stats


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


def run_field(q: int, first: dict, max_weight: int, keep_best: int) -> None:
    rows, stats = build_rows(q, first)
    full = (1 << len(rows)) - 1
    target = mask_from_signs([row["target"] for row in rows])
    atom_masks: list[tuple[str, int]] = []
    atom_stats = Counter()

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
            atom_stats[f"atom_{name}_zero_or_undefined"] = zero_or_undefined
            continue
        atom_masks.append((name, mask_from_signs(signs)))

    exact: list[tuple[int, int, tuple[str, ...], int]] = []
    best: list[tuple[int, int, tuple[str, ...], int]] = []
    for weight in range(1, max_weight + 1):
        for combo in combinations(atom_masks, weight):
            names = tuple(name for name, _mask in combo)
            mask = 0
            for _name, atom_mask in combo:
                mask ^= atom_mask
            matches, opposite = score_mask(mask, target, full)
            best_matches = max(matches, opposite)
            polarity = 1 if matches >= opposite else -1
            best.append((best_matches, weight, names, polarity))
            if best_matches == len(rows):
                exact.append((best_matches, weight, names, polarity))

    best.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    stats["usable_atoms"] = len(atom_masks)
    stats["exact_products"] = len(exact)
    stats["products_tested"] = len(best)
    if best:
        stats["best_matches"] = best[0][0]
        stats["best_match_x1000000"] = best[0][0] * 1_000_000 // len(rows)
        stats["best_weight"] = best[0][1]

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for key in sorted(atom_stats):
        print(f"  {key} = {atom_stats[key]}")
    print("  exact_products:")
    if exact:
        for matches, weight, names, polarity in exact[:keep_best]:
            print(f"    weight={weight} polarity={polarity} atoms={' * '.join(names)}")
    else:
        print("    none")
    print("  best_products:")
    for matches, weight, names, polarity in best[:keep_best]:
        print(
            f"    matches={matches}/{len(rows)} "
            f"polarity={polarity} weight={weight} atoms={' * '.join(names)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--keep-best", type=int, default=12)
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    print("p27 B-line transition orientation probe")
    print("question = is the generic-to-actual 2-of-4 v selector a visible squareclass product?")
    print(f"first_fixture = {args.first_fixture}")
    print(f"max_weight = {args.max_weight}")
    for q in parse_ints(args.small_primes):
        run_field(q, first, args.max_weight, args.keep_best)
    print("p27_b_line_transition_orientation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

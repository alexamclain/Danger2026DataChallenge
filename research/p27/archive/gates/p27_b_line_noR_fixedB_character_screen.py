#!/usr/bin/env python3
"""Visible base-B character screen for surviving fixed-B no-R subcovers.

This tests whether the surviving q^2 fixed-B mechanisms from
p27_b_line_noR_quadratic_subcover_classifier.py are pullbacks of simple
quadratic characters on the base B line.  It is intentionally exact: named
atoms, all linear factors, and all monic irreducible quadratic factors.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_quadratic_subcover_classifier import classify


TARGET_CLASSES = ("beta_U_fixedB", "hidden_mixed_fixedB")


@dataclass(frozen=True)
class BRow:
    b: int
    counts: dict[str, Counter]


def legendre_base(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def inv_base(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def base_value(field: GF, value: int) -> int | None:
    if element_degree(field, value) != 1:
        return None
    coeffs = field.coeffs[value]
    if any(coeffs[i] for i in range(1, field.n)):
        return None
    return coeffs[0] % field.p


def collect_rows(field: GF) -> list[BRow]:
    rows_by_b: defaultdict[int, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    for x, w, t, beta, bline, x5, unext, selector in enumerate_points(field):
        b = base_value(field, bline)
        if b is None:
            continue
        degrees = {
            "X": element_degree(field, x),
            "W": element_degree(field, w),
            "T": element_degree(field, t),
            "beta": element_degree(field, beta),
            "B": element_degree(field, bline),
            "x5": element_degree(field, x5),
            "U": element_degree(field, unext),
            "selector": element_degree(field, selector),
        }
        point_degree = lcm(list(degrees.values()))
        gamma_chi = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma_chi)
        if cls not in TARGET_CLASSES:
            continue
        rows_by_b[b][cls]["total"] += 1
        rows_by_b[b][cls][f"gamma_{gamma_chi}"] += 1
    return [BRow(b, dict(counts)) for b, counts in sorted(rows_by_b.items())]


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
        ("B/(B+2)", lambda b: None if inv_base(b + 2, p) is None else b * inv_base(b + 2, p) % p),
        ("(B-2)/(B+2)", lambda b: None if inv_base(b + 2, p) is None else (b - 2) * inv_base(b + 2, p) % p),
    ]


def target_mask(rows: list[BRow], cls: str, mode: str) -> int:
    mask = 0
    for idx, row in enumerate(rows):
        counts = row.counts.get(cls, Counter())
        if mode == "presence":
            active = counts["total"] > 0
        elif mode == "gamma_plus":
            active = counts["gamma_1"] > 0
        elif mode == "gamma_minus":
            active = counts["gamma_-1"] > 0
        elif mode == "plus_majority":
            active = counts["gamma_1"] > counts["gamma_-1"]
        else:
            raise ValueError(mode)
        if active:
            mask |= 1 << idx
    return mask


def mask_for_fn(rows: list[BRow], p: int, fn: Callable[[int], int | None]) -> int | None:
    mask = 0
    for idx, row in enumerate(rows):
        value = fn(row.b)
        if value is None:
            return None
        chi = legendre_base(value, p)
        if chi == 0:
            return None
        if chi == 1:
            mask |= 1 << idx
    return mask


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def screen_family(
    rows: list[BRow],
    p: int,
    target: int,
    family: str,
) -> tuple[Counter, tuple[str, int] | None, tuple[str, int] | None]:
    stats: Counter = Counter()
    exact: tuple[str, int] | None = None
    best: tuple[str, int] | None = None

    def consider(label: str, mask: int) -> None:
        nonlocal exact, best
        for polarity, candidate in (("", mask), ("-", mask ^ ((1 << len(rows)) - 1))):
            candidate_label = f"{polarity}{label}" if polarity else label
            distance = hamming(candidate, target)
            if best is None or distance < best[1]:
                best = (candidate_label, distance)
            if distance == 0 and exact is None:
                exact = (candidate_label, distance)

    if family == "atoms":
        for label, fn in atom_functions(p):
            mask = mask_for_fn(rows, p, fn)
            if mask is None:
                stats["zero_or_pole_skip"] += 1
                continue
            stats["tested"] += 1
            consider(label, mask)
    elif family == "linear":
        domain = {row.b for row in rows}
        for a in range(p):
            if a in domain:
                stats["zero_skip"] += 1
                continue
            mask = mask_for_fn(rows, p, lambda b, aa=a: (b - aa) % p)
            if mask is None:
                stats["zero_or_pole_skip"] += 1
                continue
            stats["tested"] += 1
            consider(f"B-{a}", mask)
    elif family == "irreducible_quadratic":
        for u in range(p):
            for v in range(p):
                disc = (u * u - 4 * v) % p
                if legendre_base(disc, p) != -1:
                    continue
                mask = mask_for_fn(rows, p, lambda b, uu=u, vv=v: (b * b + uu * b + vv) % p)
                if mask is None:
                    stats["zero_skip"] += 1
                    continue
                stats["tested"] += 1
                consider(f"B^2+{u}B+{v}", mask)
    else:
        raise ValueError(family)
    return stats, exact, best


def run_field(p: int, n: int) -> None:
    if n != 2:
        raise ValueError("fixed-B character screen expects q^2 fields")
    field = GF(p, n)
    rows = collect_rows(field)
    print(f"GF({p}^{n}) q={field.q}")
    print(f"  fixedB_rows = {len(rows)}")
    for cls in TARGET_CLASSES:
        total = sum(row.counts.get(cls, Counter())["total"] for row in rows)
        plus = sum(row.counts.get(cls, Counter())["gamma_1"] for row in rows)
        minus = sum(row.counts.get(cls, Counter())["gamma_-1"] for row in rows)
        print(f"  {cls}_points = {total}")
        print(f"  {cls}_gamma_plus = {plus}")
        print(f"  {cls}_gamma_minus = {minus}")
        for mode in ("presence", "gamma_plus", "gamma_minus", "plus_majority"):
            target = target_mask(rows, cls, mode)
            active = bin(target).count("1")
            print(f"  target {cls} {mode}: active_B = {active}/{len(rows)}")
            if active in (0, len(rows)):
                print("    trivial_target = true")
                continue
            for family in ("atoms", "linear", "irreducible_quadratic"):
                stats, exact, best = screen_family(rows, p, target, family)
                exact_label = exact[0] if exact else "none"
                best_label = best[0] if best else "none"
                best_dist = best[1] if best else -1
                print(
                    f"    {family}: tested={stats['tested']} "
                    f"exact={exact_label} best={best_label} best_distance={best_dist}"
                )
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,167^2")
    args = parser.parse_args()

    print("p27 B-line no-R fixed-B character screen")
    print("families = named atoms, linear B-a, irreducible quadratic B^2+uB+v")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_fixedB_character_screen_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

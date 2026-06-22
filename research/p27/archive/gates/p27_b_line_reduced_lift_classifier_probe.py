#!/usr/bin/env python3
"""Classify reduced-cover B-fiber lift profiles by visible characters.

The reduced-cover point-count probe shows that, over the p27 promotion fields,
each legal B fiber has 32 reduced U-points and the selector layer
gamma^2=U+2 has 0, 32, or 64 points.  Dividing by 32, this is a ternary
0/mixed/full lift profile.

This probe tests whether that ternary profile is explained by two simple
quadratic characters on P1_B:

    lift_units(B) = 1_{chi(F(B))=+1} + 1_{chi(G(B))=+1}.

It first tests named B-line atoms and all rational-linear pairs.  With
--quadratic-pair it also tests pairs of monic irreducible quadratics by a
meet-in-the-middle mask search.  This is an exact classifier screen, not a
scored fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Callable

from p27_b_line_reduced_cover_pointcount_probe import field_rows, legendre, parse_ints


DEFAULT_PRIMES = "1607,1847,2087"


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def squareclass_table(q: int) -> list[int]:
    chars = [-1] * q
    chars[0] = 0
    for a in range(1, q):
        chars[a * a % q] = 1
    return chars


def popcount(value: int) -> int:
    return bin(value).count("1")


def load_lift_rows(q: int, unit: int) -> tuple[list[tuple[int, int]], Counter]:
    stats, by_b = field_rows(q)
    out: list[tuple[int, int]] = []
    row_stats: Counter = Counter({f"pointcount_{key}": value for key, value in stats.items()})
    for b, row in sorted(by_b.items()):
        if row["legal_chart_points"] != unit or row["reduced_U_points"] != 2 * unit:
            row_stats["skipped_nondegenerate_B"] += 1
            continue
        plus = row["selector_chi_1"]
        minus = row["selector_chi_-1"]
        if plus + minus != 2 * unit or plus % unit:
            row_stats["skipped_nonternary_B"] += 1
            continue
        units = plus // unit
        if units not in (0, 1, 2):
            row_stats["skipped_bad_units_B"] += 1
            continue
        out.append((b, units))
        row_stats[f"lift_units_{units}"] += 1
    row_stats["classifier_rows"] = len(out)
    return out, row_stats


def target_masks(rows: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    target0 = 0
    target1 = 0
    target2 = 0
    for index, (_b, units) in enumerate(rows):
        if units == 0:
            target0 |= 1 << index
        elif units == 1:
            target1 |= 1 << index
        elif units == 2:
            target2 |= 1 << index
        else:
            raise ValueError(units)
    full = (1 << len(rows)) - 1
    return full, target0, target1, target2


def compatible_required(mask: int, full: int, target0: int, target1: int, target2: int) -> int | None:
    if mask & target0:
        return None
    if (mask & target2) != target2:
        return None
    return target2 | (target1 & (~mask & full))


def exact_pair_from_masks(
    masks: list[tuple[str, int]],
    full: int,
    target0: int,
    target1: int,
    target2: int,
) -> tuple[str, str] | None:
    seen: dict[int, str] = {}
    for label, mask in masks:
        required = compatible_required(mask, full, target0, target1, target2)
        if required is not None and required in seen:
            return seen[required], label
        seen.setdefault(mask, label)
    return None


def atom_functions(q: int) -> list[tuple[str, Callable[[int], int | None]]]:
    return [
        ("B", lambda b: b),
        ("B+2", lambda b: (b + 2) % q),
        ("B-2", lambda b: (b - 2) % q),
        ("B+4", lambda b: (b + 4) % q),
        ("B-4", lambda b: (b - 4) % q),
        ("B^2-4", lambda b: (b * b - 4) % q),
        ("B^2+4", lambda b: (b * b + 4) % q),
        ("B^2+2B+4", lambda b: (b * b + 2 * b + 4) % q),
        ("B^2-2B+4", lambda b: (b * b - 2 * b + 4) % q),
        ("B/(B+2)", lambda b: None if inv(b + 2, q) is None else b * inv(b + 2, q) % q),
        ("(B-2)/(B+2)", lambda b: None if inv(b + 2, q) is None else (b - 2) * inv(b + 2, q) % q),
    ]


def mask_from_values(rows: list[tuple[int, int]], q: int, fn: Callable[[int], int | None]) -> int | None:
    mask = 0
    for index, (b, _units) in enumerate(rows):
        value = fn(b)
        if value is None:
            return None
        chi = legendre(value, q)
        if chi == 0:
            return None
        if chi == 1:
            mask |= 1 << index
    return mask


def polarized(label: str, mask: int, full: int) -> list[tuple[str, int]]:
    return [(label, mask), (f"-({label})", mask ^ full)]


def atom_masks(rows: list[tuple[int, int]], q: int, full: int) -> tuple[list[tuple[str, int]], Counter]:
    stats: Counter = Counter()
    masks: list[tuple[str, int]] = []
    for label, fn in atom_functions(q):
        mask = mask_from_values(rows, q, fn)
        if mask is None:
            stats["atom_zero_or_pole"] += 1
            continue
        stats["atom_masks"] += 1
        masks.extend(polarized(label, mask, full))
    return masks, stats


def linear_masks(rows: list[tuple[int, int]], q: int, full: int) -> tuple[list[tuple[str, int]], Counter]:
    domain = {b for b, _units in rows}
    masks: list[tuple[str, int]] = []
    stats: Counter = Counter()
    for a in range(q):
        if a in domain:
            stats["linear_zero_skip"] += 1
            continue
        mask = 0
        for index, (b, _units) in enumerate(rows):
            if legendre(b - a, q) == 1:
                mask |= 1 << index
        stats["linear_masks"] += 1
        masks.extend(polarized(f"B-{a}", mask, full))
    return masks, stats


def quadratic_pair_search(
    rows: list[tuple[int, int]],
    q: int,
    full: int,
    target0: int,
    target1: int,
    target2: int,
) -> tuple[Counter, tuple[str, str] | None]:
    chars = squareclass_table(q)
    domain = [b for b, _units in rows]
    seen: dict[int, str] = {}
    stats: Counter = Counter()

    for u in range(q):
        for v in range(q):
            disc = (u * u - 4 * v) % q
            if chars[disc] != -1:
                continue
            mask = 0
            for index, b in enumerate(domain):
                value = (b * b + u * b + v) % q
                if chars[value] == 0:
                    stats["quadratic_zero_skip"] += 1
                    break
                if chars[value] == 1:
                    mask |= 1 << index
            else:
                stats["irreducible_quadratic_masks"] += 1
                label = f"B^2+{u}B+{v}"
                for candidate_label, candidate_mask in polarized(label, mask, full):
                    required = compatible_required(candidate_mask, full, target0, target1, target2)
                    if required is not None and required in seen:
                        stats["unique_quadratic_masks_before_hit"] = len(seen)
                        return stats, (seen[required], candidate_label)
                    seen.setdefault(candidate_mask, candidate_label)

    stats["unique_quadratic_masks"] = len(seen)
    return stats, None


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, unit: int, quadratic_pair: bool) -> None:
    rows, row_stats = load_lift_rows(q, unit)
    full, target0, target1, target2 = target_masks(rows)
    print_counter(f"q{q}_reduced_lift_profile_stats", row_stats)
    print(f"q{q}_target_masks:")
    print(f"  target0_none = {popcount(target0)}")
    print(f"  target1_mixed = {popcount(target1)}")
    print(f"  target2_full = {popcount(target2)}")

    atoms, atom_stats = atom_masks(rows, q, full)
    atom_solution = exact_pair_from_masks(atoms, full, target0, target1, target2)
    print_counter(f"q{q}_atom_pair_classifier_stats", atom_stats)
    if atom_solution:
        print(f"q{q}_atom_pair_classifier_result: {atom_solution[0]} ; {atom_solution[1]}")
    else:
        print("q{q}_atom_pair_classifier_result: none".format(q=q))

    linears, linear_stats = linear_masks(rows, q, full)
    linear_solution = exact_pair_from_masks(linears, full, target0, target1, target2)
    print_counter(f"q{q}_linear_pair_classifier_stats", linear_stats)
    if linear_solution:
        print(f"q{q}_linear_pair_classifier_result: {linear_solution[0]} ; {linear_solution[1]}")
    else:
        print("q{q}_linear_pair_classifier_result: none".format(q=q))

    if quadratic_pair:
        quadratic_stats, quadratic_solution = quadratic_pair_search(
            rows,
            q,
            full,
            target0,
            target1,
            target2,
        )
        print_counter(f"q{q}_quadratic_pair_classifier_stats", quadratic_stats)
        if quadratic_solution:
            print(
                f"q{q}_quadratic_pair_classifier_result: "
                f"{quadratic_solution[0]} ; {quadratic_solution[1]}"
            )
        else:
            print("q{q}_quadratic_pair_classifier_result: none".format(q=q))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default=DEFAULT_PRIMES)
    parser.add_argument("--unit", type=int, default=16)
    parser.add_argument("--quadratic-pair", action="store_true")
    args = parser.parse_args()

    print("p27 B-line reduced-lift classifier probe")
    print("question = is the 0/mixed/full reduced-cover lift profile two visible B-line characters?")
    print(f"small_primes = {args.small_primes}")
    print(f"unit = {args.unit}")
    print(f"quadratic_pair = {args.quadratic_pair}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.unit, args.quadratic_pair)
    print("p27_b_line_reduced_lift_classifier_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

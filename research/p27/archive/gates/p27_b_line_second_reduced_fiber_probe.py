#!/usr/bin/env python3
"""Probe the second reduced B-line fiber: f4 over the f3-plus domain.

The first reduced-fiber fixture describes the d3 class over legal B using
u=x6+1/x6 and selector chi(u+2).  This probe performs the analogous finite
field extraction one gate later:

  * restrict to legal B rows with d3=+1,
  * enumerate selected x6 branches,
  * halve once more to x7,
  * reduce by v=x7+1/x7,
  * record whether chi(v+2) agrees with the descended d4(B).

It also runs a small plane-relation screen on (B,v), plus/minus subcovers.
The goal is to create the first compact f4/f3 comparison artifact for offline
CAS, not to fit another B bucket.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Iterable

from p27_b_source_descent_probe import source_b_plus
from p27_b_line_fiber_invariant_probe import interpolation_degree, poly_roots_coeffs
from p27_conic_pair_invariant_relation_probe import relation_stats_for_system
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def collect_second_fibers(q: int) -> tuple[dict[int, list[int]], dict[int, int], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    groups: defaultdict[int, list[int]] = defaultdict(list)
    signs: dict[int, int] = {}
    d3_values_by_b: defaultdict[int, list[int]] = defaultdict(list)
    d4_values_by_b: defaultdict[int, list[int]] = defaultdict(list)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in dedupe_candidates(candidates):
        stats["deduped_candidates"] += 1
        A = int(cand["A"]) % q
        x5 = int(cand["x5"]) % q
        B = source_b_plus(int(cand["X"]) % q, q)
        if B is None:
            stats["b_degenerate"] += 1
            continue

        d2, x6s = halve_all(A, x5, q)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        d3_values = [legendre(x6, q) for x6 in x6s]
        d3 = normalize(d3_values)
        d3_values_by_b[B].append(d3 if d3 is not None else 0)
        if d3 != 1:
            continue

        for x6 in x6s:
            if legendre(x6, q) != 1:
                stats["d3_plus_x6_nonsquare"] += 1
                continue
            d3_halve, x7s = halve_all(A, x6, q)
            if d3_halve != 1:
                stats["d4_halve_not_square"] += 1
                d4_values_by_b[B].append(0)
                continue
            for x7 in x7s:
                chi = legendre(x7, q)
                d4_values_by_b[B].append(chi)
                groups[B].append(x7 % q)

    for B, values in d3_values_by_b.items():
        d3 = normalize(values)
        if d3 == 0:
            stats["d3_mixed_on_B"] += 1
        elif d3 == -1:
            stats["d3_minus_B"] += 1
        elif d3 == 1:
            stats["d3_plus_B"] += 1
            d4 = normalize(d4_values_by_b[B])
            if d4 in (-1, 1):
                signs[B] = d4
            elif d4 == 0:
                stats["d4_mixed_on_B"] += 1
            else:
                stats["d4_missing_on_B"] += 1
    stats["B_groups_with_x7"] = len(groups)
    stats["B_groups_with_d4_sign"] = len(signs)
    return dict(groups), signs, stats


def exact_power_sum_hits(
    rows: list[tuple[int, int, list[int]]],
    q: int,
    max_power: int,
    reciprocal: bool,
) -> tuple[list[tuple[int, str, int]], list[tuple[int, int, int, int]]]:
    exact: list[tuple[int, str, int]] = []
    near: list[tuple[int, int, int, int]] = []
    for exponent in range(1, max_power + 1):
        match = 0
        opposite = 0
        zero = 0
        for _B, sign, roots in rows:
            if reciprocal:
                value = sum(
                    (pow(root, exponent, q) + pow(inv(root, q), exponent, q)) % q
                    for root in roots
                    if root
                ) % q
            else:
                value = sum(pow(root, exponent, q) for root in roots) % q
            chi = legendre(value, q) if value else 0
            if chi == 0:
                zero += 1
            elif chi == sign:
                match += 1
            elif chi == -sign:
                opposite += 1
        total = len(rows) - zero
        best = max(match, opposite)
        if total and best == total:
            exact.append((exponent, "match" if match >= opposite else "opposite", zero))
        elif total and best * 4 >= 3 * total:
            near.append((exponent, best, total, zero))
    return exact, near


def coefficient_degrees(
    rows: list[tuple[int, int, list[int]]],
    q: int,
    use_v: bool,
) -> tuple[Counter, list[int] | None]:
    if use_v:
        root_sets = [
            (B, sorted({(root + inv(root, q)) % q for root in roots if root}))
            for B, _sign, roots in rows
        ]
    else:
        root_sets = [(B, sorted(set(roots))) for B, _sign, roots in rows]
    degree_hist = Counter(len(roots) for _B, roots in root_sets)
    if len(degree_hist) != 1:
        return degree_hist, None
    root_degree = next(iter(degree_hist))
    coeff_points: list[list[tuple[int, int]]] = [[] for _ in range(root_degree)]
    for B, roots in root_sets:
        coeffs = poly_roots_coeffs(roots, q)
        for i in range(root_degree):
            coeff_points[i].append((B, coeffs[i]))
    return degree_hist, [interpolation_degree(points, q) for points in coeff_points]


def relation_screen(rows: list[tuple[int, int, list[int]]], q: int, degrees: list[int]) -> None:
    systems: dict[str, list[tuple[int, int]]] = {
        "B_v": [],
        "B_vplus2": [],
        "B_v_plus": [],
        "B_v_minus": [],
    }
    for B, sign, roots in rows:
        v_roots = sorted({(root + inv(root, q)) % q for root in roots if root})
        for v in v_roots:
            systems["B_v"].append((B, v))
            systems["B_vplus2"].append((B, (v + 2) % q))
            if sign == 1:
                systems["B_v_plus"].append((B, v))
            elif sign == -1:
                systems["B_v_minus"].append((B, v))

    for name, points in systems.items():
        unique_points = sorted(set(points))
        stats = relation_stats_for_system(unique_points, q, degrees)
        print(f"  relation_{name}:")
        print(f"    rows = {len(points)}")
        print(f"    unique = {len(unique_points)}")
        for degree in degrees:
            prefix = f"deg{degree}"
            print(
                "    "
                f"{prefix}: monomials={stats[f'{prefix}_monomials']} "
                f"rank={stats[f'{prefix}_rank']} "
                f"nullity={stats[f'{prefix}_nullity']} "
                f"forced={stats[f'{prefix}_forced_nullity']} "
                f"extra={stats[f'{prefix}_extra_nullity']}"
            )


def print_field(q: int, max_power: int, degrees: list[int]) -> None:
    groups, signs, stats = collect_second_fibers(q)
    rows = [(B, signs[B], sorted(set(groups[B]))) for B in sorted(signs)]

    for B, roots in groups.items():
        unique_roots = sorted(set(roots))
        unique_v = sorted({(root + inv(root, q)) % q for root in unique_roots if root})
        stats[f"occurrence_x7_roots_{len(roots)}"] += 1
        stats[f"unique_x7_roots_{len(unique_roots)}"] += 1
        stats[f"unique_v_roots_{len(unique_v)}"] += 1
        if B in signs:
            stats[f"d4_sign_{signs[B]}"] += 1
        v_plus_signs = {legendre((v + 2) % q, q) for v in unique_v}
        stats[f"v_plus_2_sign_classes_{len(v_plus_signs)}"] += 1
        if B in signs and len(v_plus_signs) == 1 and next(iter(v_plus_signs)) == signs[B]:
            stats["v_plus_2_matches_d4"] += 1

    x_exact, x_near = exact_power_sum_hits(rows, q, max_power=max_power, reciprocal=False)
    r_exact, r_near = exact_power_sum_hits(rows, q, max_power=max_power, reciprocal=True)
    x_degree_hist, x_coeff_degrees = coefficient_degrees(rows, q, use_v=False)
    v_degree_hist, v_coeff_degrees = coefficient_degrees(rows, q, use_v=True)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print(f"  x7_degree_hist = {dict(sorted(x_degree_hist.items()))}")
    print(f"  x7_coeff_interpolation_degrees = {x_coeff_degrees if x_coeff_degrees is not None else 'varying'}")
    print(f"  v_degree_hist = {dict(sorted(v_degree_hist.items()))}")
    print(f"  v_coeff_interpolation_degrees = {v_coeff_degrees if v_coeff_degrees is not None else 'varying'}")
    print(f"  x7_power_sum_exact_hits = {x_exact if x_exact else 'none'}")
    print(f"  reciprocal_power_sum_exact_hits = {r_exact if r_exact else 'none'}")
    print(f"  x7_power_sum_near_75pct = {x_near if x_near else 'none'}")
    print(f"  reciprocal_power_sum_near_75pct = {r_near if r_near else 'none'}")
    relation_screen(rows, q, degrees)


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--max-power", type=int, default=64)
    parser.add_argument("--degrees", default="2,4,6,8,10,12,14")
    args = parser.parse_args()

    print("p27 B-line second reduced-fiber probe")
    print("question = what is the reduced f4 fiber over the f3-plus B-domain?")
    print(f"small_primes = {args.small_primes}")
    print(f"max_power = {args.max_power}")
    print(f"relation_degrees = {args.degrees}")
    degrees = parse_degrees(args.degrees)
    for q in parse_ints(args.small_primes):
        print_field(q, args.max_power, degrees)
    print("p27_b_line_second_reduced_fiber_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Low-degree relation screen for legal p27 conic-pair sampler preimages."""

from __future__ import annotations

import argparse
from collections import Counter

from p27_conic_pair_sampler_legal_incidence_probe import inv_table, legal_sets


def sampler_preimages_for_targets(
    p: int, targets: set[tuple[int, int]]
) -> tuple[list[tuple[int, int]], Counter]:
    invs = inv_table(p)
    inv2 = invs[2]
    inv4 = invs[4]
    points: list[tuple[int, int]] = []
    stats: Counter = Counter()
    for r_next in range(1, p):
        inv_r_next = invs[r_next]
        a_line = (r_next - inv_r_next) % p
        s = (r_next + inv_r_next) % p
        a2 = a_line * a_line % p
        for lam in range(1, p):
            stats["draws"] += 1
            a2_over_lam = a2 * invs[lam] % p
            d = (lam - a2_over_lam) * inv2 % p
            r = -(lam + a2_over_lam) * inv4 % p
            if r == 0:
                stats["degenerate_r"] += 1
                continue
            c = s * d % p * invs[(2 * r) % p] % p
            A = (2 - c * c) % p
            x = r * r % p
            if (A, x) in targets:
                points.append((r_next, lam))
    stats["target_preimages"] = len(points)
    return points, stats


def monomials_total_degree(max_degree: int) -> list[tuple[int, int]]:
    return [(i, j) for total in range(max_degree + 1) for i in range(total + 1) for j in [total - i]]


def row_for_point(point: tuple[int, int], monomials: list[tuple[int, int]], p: int) -> list[int]:
    r, l = point
    max_i = max(i for i, _ in monomials)
    max_j = max(j for _, j in monomials)
    rpows = [1] * (max_i + 1)
    lpows = [1] * (max_j + 1)
    for i in range(1, max_i + 1):
        rpows[i] = rpows[i - 1] * r % p
    for j in range(1, max_j + 1):
        lpows[j] = lpows[j - 1] * l % p
    return [rpows[i] * lpows[j] % p for i, j in monomials]


def rank_mod_p(rows: list[list[int]], p: int) -> int:
    basis: dict[int, list[int]] = {}
    rank = 0
    for raw in rows:
        row = raw[:]
        while True:
            pivot = next((i for i, value in enumerate(row) if value % p), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(row[pivot] % p, p - 2, p)
                row = [value * inv % p for value in row]
                basis[pivot] = row
                rank += 1
                break
            brow = basis[pivot]
            coeff = row[pivot] % p
            row = [(value - coeff * bvalue) % p for value, bvalue in zip(row, brow)]
    return rank


def relation_stats(points: list[tuple[int, int]], p: int, degrees: list[int]) -> Counter:
    stats: Counter = Counter()
    for degree in degrees:
        monomials = monomials_total_degree(degree)
        rows = [row_for_point(point, monomials, p) for point in points]
        rank = rank_mod_p(rows, p)
        nullity = len(monomials) - rank
        stats[f"deg{degree}_monomials"] = len(monomials)
        stats[f"deg{degree}_rank"] = rank
        stats[f"deg{degree}_nullity"] = nullity
    return stats


def screen_field(p: int, degrees: list[int]) -> Counter:
    legal_stats, _, d3_plus, d3_minus = legal_sets(p)
    plus_points, plus_stats = sampler_preimages_for_targets(p, d3_plus)
    minus_points, minus_stats = sampler_preimages_for_targets(p, d3_minus)
    stats: Counter = Counter({f"legal_{key}": value for key, value in legal_stats.items()})
    stats.update({f"plus_{key}": value for key, value in plus_stats.items()})
    stats.update({f"minus_{key}": value for key, value in minus_stats.items()})
    stats["plus_unique_preimages"] = len(set(plus_points))
    stats["minus_unique_preimages"] = len(set(minus_points))
    stats.update({f"plus_{key}": value for key, value in relation_stats(plus_points, p, degrees).items()})
    if minus_points:
        stats.update({f"minus_{key}": value for key, value in relation_stats(minus_points, p, degrees).items()})
    return stats


def print_counter(prefix: str, stats: Counter, degrees: list[int]) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for degree in degrees:
        n = stats[f"plus_deg{degree}_monomials"]
        nullity = stats[f"plus_deg{degree}_nullity"]
        print(f"  plus_deg{degree}_has_relation = {1 if nullity else 0} ({nullity}/{n})")
        if f"minus_deg{degree}_nullity" in stats:
            mn = stats[f"minus_deg{degree}_monomials"]
            mnullity = stats[f"minus_deg{degree}_nullity"]
            print(f"  minus_deg{degree}_has_relation = {1 if mnullity else 0} ({mnullity}/{mn})")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--degrees", default="4,6,8,10,12,14,16,18,20")
    args = parser.parse_args()

    degrees = parse_ints(args.degrees)
    print("p27 conic-pair low-degree relation probe")
    print("points = sampler preimages (R,L) of legal d3-plus classes")
    print(f"degrees = {','.join(str(d) for d in degrees)}")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", screen_field(p, degrees), degrees)
    print("p27_conic_pair_lowdegree_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

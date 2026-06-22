#!/usr/bin/env python3
"""Bidegree relation screen for the beta_U norm class.

The beta_U norm descent names a base-field class

    N = Norm_GF(q^2)/GF(q)(Unext + 2)

on the chi(B)=+1 fixed-B support.  This probe asks whether the point sets
(B, N), with optional gamma sign restriction, lie on a small bidegree plane
curve over the base field.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_betaU_norm_descent_probe import norm_to_base
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify
from p27_conic_pair_invariant_relation_probe import echelon_basis


def parse_bidegrees(raw: str) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for part in raw.split(","):
        part = part.strip().lower()
        if not part:
            continue
        left, right = part.split("x", 1)
        out.append((int(left), int(right)))
    return out


def betaU_norm_points(field: GF) -> dict[str, list[tuple[int, int]]]:
    sets = {
        "all": [],
        "gamma_plus": [],
        "gamma_minus": [],
    }
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
        if cls != "beta_U_fixedB":
            continue
        norm_base = base_value(field, norm_to_base(field, selector))
        if norm_base is None:
            continue
        pair = (b, norm_base)
        sets["all"].append(pair)
        if legendre_base(norm_base, field.p) == 1:
            sets["gamma_plus"].append(pair)
        elif legendre_base(norm_base, field.p) == -1:
            sets["gamma_minus"].append(pair)
    return sets


def monomials_bidegree(max_b: int, max_n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(max_b + 1) for j in range(max_n + 1)]


def row_for_pair(pair: tuple[int, int], monomials: list[tuple[int, int]], p: int) -> list[int]:
    b, n = pair
    max_b = max(i for i, _j in monomials)
    max_n = max(j for _i, j in monomials)
    bpows = [1] * (max_b + 1)
    npows = [1] * (max_n + 1)
    for i in range(1, max_b + 1):
        bpows[i] = bpows[i - 1] * b % p
    for j in range(1, max_n + 1):
        npows[j] = npows[j - 1] * n % p
    return [bpows[i] * npows[j] % p for i, j in monomials]


def relation_stats(points: list[tuple[int, int]], p: int, bidegrees: list[tuple[int, int]]) -> Counter:
    stats: Counter = Counter()
    unique = sorted(set(points))
    stats["rows"] = len(points)
    stats["unique"] = len(unique)
    for max_b, max_n in bidegrees:
        monomials = monomials_bidegree(max_b, max_n)
        rows = [row_for_pair(pair, monomials, p) for pair in unique]
        _basis, pivots = echelon_basis(rows, p)
        rank = len(pivots)
        nullity = len(monomials) - rank
        forced = max(0, len(monomials) - len(unique))
        extra = nullity - forced
        prefix = f"B{max_b}_N{max_n}"
        stats[f"{prefix}_monomials"] = len(monomials)
        stats[f"{prefix}_rank"] = rank
        stats[f"{prefix}_nullity"] = nullity
        stats[f"{prefix}_forced"] = forced
        stats[f"{prefix}_extra"] = extra
    return stats


def print_stats(label: str, stats: Counter, bidegrees: list[tuple[int, int]]) -> None:
    print(f"  {label}:")
    print(f"    rows = {stats['rows']}")
    print(f"    unique = {stats['unique']}")
    for max_b, max_n in bidegrees:
        prefix = f"B{max_b}_N{max_n}"
        print(
            f"    {prefix}: monomials={stats[f'{prefix}_monomials']} "
            f"rank={stats[f'{prefix}_rank']} nullity={stats[f'{prefix}_nullity']} "
            f"forced={stats[f'{prefix}_forced']} extra={stats[f'{prefix}_extra']}"
        )


def run_field(p: int, n: int, bidegrees: list[tuple[int, int]]) -> None:
    if n != 2:
        raise ValueError("betaU norm relation screen expects q^2 fields")
    field = GF(p, n)
    sets = betaU_norm_points(field)
    print(f"GF({p}^{n}) q={field.q}")
    for label in ("all", "gamma_plus", "gamma_minus"):
        print_stats(label, relation_stats(sets[label], p, bidegrees), bidegrees)
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="103^2,167^2,199^2,263^2")
    parser.add_argument("--bidegrees", default="2x4,4x8,6x8,8x12,10x16,12x16")
    args = parser.parse_args()

    bidegrees = parse_bidegrees(args.bidegrees)
    print("p27 B-line no-R beta_U norm relation probe")
    print("question = does (B, Norm(Unext+2)) have a small bidegree relation?")
    print(f"fields = {args.fields}")
    print(f"bidegrees = {bidegrees}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n, bidegrees)
    print("p27_b_line_noR_betaU_norm_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

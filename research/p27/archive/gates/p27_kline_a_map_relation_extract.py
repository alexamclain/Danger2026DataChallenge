#!/usr/bin/env python3
"""Extract and heldout-test p27 selected K/Sroot -> A relations."""

from __future__ import annotations

import argparse
from collections import Counter

from p27_conic_pair_invariant_relation_probe import (
    echelon_basis,
    evaluate_relation,
    monomials_total_degree,
    null_vector_from_basis,
    row_for_point,
)
from p27_kline_a_map_relation_probe import selected_rows_from_candidates, transformed_points
from p27_kline_reverse_z_relation_probe import p27_candidates
from p27_label2_alpha_branch_recurrence_probe import P


SYSTEM_COORDS = {
    "K_A": ("K", "A"),
    "S_A": ("S", "A"),
    "K_A_x5": ("K", "A", "x5"),
    "S_A_x5": ("S", "A", "x5"),
}


def signed(value: int, p: int) -> int:
    value %= p
    return value - p if value > p // 2 else value


def parse_system_degrees(raw: str) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        name, degree = part.split(":")
        if name not in SYSTEM_COORDS:
            raise ValueError(f"unknown system {name}")
        out.append((name, int(degree)))
    return out


def unique_points(rows: list[dict[str, int | None]], system: str) -> list[tuple[int, ...]]:
    coords = SYSTEM_COORDS[system]
    points: list[tuple[int, ...]] = []
    for row in rows:
        point = tuple(int(row[name]) for name in coords)
        points.append(point)
    return sorted(set(points))


def nullspace_basis(points: list[tuple[int, ...]], degree: int, p: int) -> tuple[list[tuple[int, ...]], list[list[int]], Counter]:
    monomials = monomials_total_degree(len(points[0]), degree) if points else []
    rows = [row_for_point(point, monomials, p) for point in points]
    basis, pivots = echelon_basis(rows, p)
    rank = len(pivots)
    forced = max(0, len(monomials) - len(points))
    stats = Counter(
        {
            "points": len(points),
            "monomials": len(monomials),
            "rank": rank,
            "nullity": len(monomials) - rank,
            "forced_nullity": forced,
            "extra_nullity": max(0, len(monomials) - rank - forced),
        }
    )

    vectors: list[list[int]] = []
    used_pivots = set(pivots)
    for free in [col for col in range(len(monomials)) if col not in used_pivots]:
        vec = [0] * len(monomials)
        vec[free] = 1
        for pivot in reversed(pivots):
            row = basis[pivot]
            acc = 0
            for col in range(pivot + 1, len(monomials)):
                acc = (acc + row[col] * vec[col]) % p
            vec[pivot] = (-acc) % p
        vectors.append(vec)
    return monomials, vectors, stats


def relation_terms(monomials: list[tuple[int, ...]], coeffs: list[int], p: int) -> list[tuple[int, tuple[int, ...]]]:
    out = [(signed(coeff, p), monomial) for coeff, monomial in zip(coeffs, monomials) if coeff % p]
    out.sort(key=lambda item: (sum(item[1]), item[1]))
    return out


def evaluate_many(points: list[tuple[int, ...]], monomials: list[tuple[int, ...]], coeffs: list[int], p: int) -> int:
    return sum(1 for point in points if evaluate_relation(point, monomials, coeffs, p) != 0)


def print_relation(system: str, degree: int, index: int, monomials: list[tuple[int, ...]], coeffs: list[int], p: int, max_terms: int) -> None:
    terms = relation_terms(monomials, coeffs, p)
    print(f"relation {system} degree={degree} basis_index={index} terms={len(terms)}")
    for coeff, monomial in terms[:max_terms]:
        print(f"  coeff={coeff} monomial={monomial}")
    if len(terms) > max_terms:
        print(f"  ... {len(terms) - max_terms} more terms")


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", default="K_A:8,S_A:12,K_A_x5:8")
    parser.add_argument("--train-target", type=int, default=1000)
    parser.add_argument("--heldout-target", type=int, default=1000)
    parser.add_argument("--train-seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=500000)
    parser.add_argument("--max-relations", type=int, default=8)
    parser.add_argument("--max-terms", type=int, default=40)
    args = parser.parse_args()

    print("p27 K-line selected A-map relation extractor")
    print("relations are trained over p27 and checked on independent heldout rows")
    systems = parse_system_degrees(args.systems)
    print(f"systems = {systems}")

    train_candidates, train_sample_stats = p27_candidates(args.train_target, args.train_seed, args.max_draws)
    train_rows, train_stats = selected_rows_from_candidates(train_candidates, P)
    held_candidates, held_sample_stats = p27_candidates(args.heldout_target, args.heldout_seed, args.max_draws)
    held_rows, held_stats = selected_rows_from_candidates(held_candidates, P)

    print_counter("train_sample_stats", train_sample_stats)
    print_counter("train_selected_stats", train_stats)
    print_counter("heldout_sample_stats", held_sample_stats)
    print_counter("heldout_selected_stats", held_stats)

    for system, degree in systems:
        train_points = unique_points(train_rows, system)
        held_points = unique_points(held_rows, system)
        monomials, vectors, stats = nullspace_basis(train_points, degree, P)
        print_counter(f"{system}_deg{degree}_train_nullspace", stats)
        print(f"{system}_deg{degree}_heldout_points = {len(held_points)}")
        for index, coeffs in enumerate(vectors[: args.max_relations]):
            train_bad = evaluate_many(train_points, monomials, coeffs, P)
            held_bad = evaluate_many(held_points, monomials, coeffs, P)
            print(
                f"{system}_deg{degree}_basis{index}: "
                f"train_bad={train_bad}/{len(train_points)} "
                f"heldout_bad={held_bad}/{len(held_points)} "
                f"terms={sum(1 for c in coeffs if c % P)}"
            )
            if train_bad == 0 and held_bad == 0:
                print_relation(system, degree, index, monomials, coeffs, P, args.max_terms)

    print("p27_kline_a_map_relation_extract_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

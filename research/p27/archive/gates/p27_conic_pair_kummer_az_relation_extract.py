#!/usr/bin/env python3
"""Extract candidate `(A,Z)` relations from the first Kummer-Z layer."""

from __future__ import annotations

import argparse

from p27_conic_pair_invariant_relation_probe import (
    echelon_basis,
    monomials_total_degree,
    row_for_point,
)
from p27_conic_pair_kummer_z_relation_probe import z_layer_value_rows


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def nullspace_vectors(basis: dict[int, list[int]], pivots: list[int], ncols: int, p: int) -> list[list[int]]:
    vectors: list[list[int]] = []
    free_cols = [col for col in range(ncols) if col not in basis]
    for free in free_cols:
        vec = [0] * ncols
        vec[free] = 1
        for pivot in reversed(pivots):
            row = basis[pivot]
            acc = 0
            for col in range(pivot + 1, ncols):
                acc = (acc + row[col] * vec[col]) % p
            vec[pivot] = (-acc) % p
        vectors.append(vec)
    return vectors


def centered(value: int, p: int) -> int:
    value %= p
    return value - p if value > p // 2 else value


def format_term(coeff: int, monomial: tuple[int, int], p: int) -> str:
    a_exp, z_exp = monomial
    c = centered(coeff, p)
    factors = []
    if a_exp:
        factors.append("A" if a_exp == 1 else f"A^{a_exp}")
    if z_exp:
        factors.append("Z" if z_exp == 1 else f"Z^{z_exp}")
    body = "*".join(factors) if factors else "1"
    return f"{c}*{body}"


def relation_summary(vec: list[int], monomials: list[tuple[int, int]], p: int, max_terms: int) -> list[str]:
    terms = [
        (monomial, coeff % p)
        for monomial, coeff in zip(monomials, vec)
        if coeff % p
    ]
    odd_z = sum(1 for (a_exp, z_exp), _ in terms if z_exp & 1)
    max_a = max((a_exp for (a_exp, _), _ in terms), default=0)
    max_z = max((z_exp for (_, z_exp), _ in terms), default=0)
    lines = [
        f"terms = {len(terms)}",
        f"odd_z_terms = {odd_z}",
        f"max_A_exp = {max_a}",
        f"max_Z_exp = {max_z}",
    ]
    shown = terms[:max_terms]
    for monomial, coeff in shown:
        lines.append(f"  {format_term(coeff, monomial, p)}")
    if len(terms) > len(shown):
        lines.append(f"  ... {len(terms) - len(shown)} more terms")
    return lines


def extract_field(p: int, degree: int, max_relations: int, max_terms: int) -> None:
    rows, stats = z_layer_value_rows(p)
    points = sorted({(int(row["A"]), int(row["z"])) for row in rows if row.get("z") is not None})
    monomials = monomials_total_degree(2, degree)
    matrix = [row_for_point(point, monomials, p) for point in points]
    basis, pivots = echelon_basis(matrix, p)
    vectors = nullspace_vectors(basis, pivots, len(monomials), p)
    print(f"q{p} degree{degree}:")
    print(f"  points = {len(points)}")
    print(f"  z_rows = {stats['z_rows']}")
    print(f"  monomials = {len(monomials)}")
    print(f"  rank = {len(pivots)}")
    print(f"  nullity = {len(vectors)}")
    for i, vec in enumerate(vectors[:max_relations]):
        print(f"  relation_{i}:")
        for line in relation_summary(vec, monomials, p, max_terms):
            print(f"    {line}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--degrees", default="18,20")
    parser.add_argument("--max-relations", type=int, default=3)
    parser.add_argument("--max-terms", type=int, default=40)
    args = parser.parse_args()

    print("p27 conic-pair Kummer A,Z relation extractor")
    for p in parse_ints(args.small_primes):
        for degree in parse_ints(args.degrees):
            extract_field(p, degree, args.max_relations, args.max_terms)
    print("p27_conic_pair_kummer_az_relation_extract_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

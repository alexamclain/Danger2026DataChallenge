#!/usr/bin/env python3
"""Projective relation audit for actual Lang-transformed CM columns.

Full Moore-arc behavior can be random-generic over the large split fields used
in small CM tests.  A stronger Reed-Solomon/LRS hint is projective low-degree
geometry.  For example, six points in `P^2(F_q)` are GRS-like only if they lie
on a conic; a random full arc usually does not.

This script reuses `lang_arc_strength_audit.py` to build actual CM Lang
columns, chooses an F_q-basis for their span, and tests whether all columns
lie on a homogeneous projective relation of a requested degree.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations_with_replacement
from math import gcd
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from lang_arc_strength_audit import transformed_blocks_for_row
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class ProjectiveRelationRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_lengths: tuple[int, ...]
    coordinate_count: int
    coordinate_rank: int
    relation_degree: int
    monomial_count: int
    relation_rank: int
    relation_nullity: int
    random_trials: int
    random_nullity_min: int
    random_nullity_max: int
    random_positive_nullity_count: int


def pivot_basis(values: list[tuple[int, ...]], q: int, dim: int) -> list[tuple[int, ...]]:
    basis: list[tuple[int, ...]] = []
    for value in values:
        if fq_rank(basis + [value], q) > len(basis):
            basis.append(value)
            if len(basis) == dim:
                return basis
    raise ValueError("values do not have requested rank")


def solve_in_basis(
    basis: list[tuple[int, ...]],
    value: tuple[int, ...],
    q: int,
) -> list[int]:
    rows = len(value)
    cols = len(basis)
    augmented = [
        [basis[col][row] % q for col in range(cols)] + [value[row] % q]
        for row in range(rows)
    ]
    rank = 0
    pivot_cols: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if augmented[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = pow(augmented[rank][col] % q, -1, q)
        augmented[rank] = [(inv * x) % q for x in augmented[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = augmented[row][col] % q
            if not scale:
                continue
            augmented[row] = [
                (left - scale * right) % q
                for left, right in zip(augmented[row], augmented[rank])
            ]
        pivot_cols.append(col)
        rank += 1
        if rank == cols:
            break
    if rank < cols:
        raise ValueError("basis matrix is not full rank")
    for row in range(rank, rows):
        if augmented[row][-1] % q:
            raise ValueError("value is not in basis span")
    solution = [0 for _ in range(cols)]
    for row, col in enumerate(pivot_cols):
        solution[col] = augmented[row][-1] % q
    return solution


def degree_monomials(dim: int, degree: int) -> list[tuple[int, ...]]:
    return list(combinations_with_replacement(range(dim), degree))


def monomial_row(point: list[int], monomials: list[tuple[int, ...]], q: int) -> list[int]:
    row: list[int] = []
    for monomial in monomials:
        value = 1
        for index in monomial:
            value = (value * point[index]) % q
        row.append(value)
    return row


def relation_nullity(points: list[list[int]], degree: int, q: int) -> tuple[int, int, int]:
    monomials = degree_monomials(len(points[0]), degree)
    matrix = [monomial_row(point, monomials, q) for point in points]
    rank = rank_mod_q(matrix, q)
    return len(monomials), rank, len(monomials) - rank


def random_nullities(
    q: int,
    point_count: int,
    dim: int,
    degree: int,
    trials: int,
    seed: int,
) -> list[int]:
    rng = random.Random(seed + 7919 * q + 101 * point_count + dim)
    out: list[int] = []
    for _ in range(trials):
        points = [[rng.randrange(q) for _coord in range(dim)] for _ in range(point_count)]
        _mono, _rank, nullity = relation_nullity(points, degree, q)
        out.append(nullity)
    return out


def audit_projective_relation(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    degree: int,
    random_trials: int,
    seed: int,
) -> ProjectiveRelationRow | None:
    extension_degree, _field, blocks = transformed_blocks_for_row(
        D, q, ell, cycle, m, factor, left, right, left_orbit, seed
    )
    values = [value for block in blocks for value in block]
    left_len = len(left_orbit)
    coordinate_rank = fq_rank(values, q)
    if coordinate_rank < left_len:
        return None
    basis = pivot_basis(values, q, left_len)
    points = [solve_in_basis(basis, value, q) for value in values]
    monomial_count, relation_rank, nullity = relation_nullity(points, degree, q)
    random_values = random_nullities(
        q, len(points), left_len, degree, random_trials, seed
    )
    return ProjectiveRelationRow(
        D=D,
        q=q,
        ell=ell,
        h=len(cycle),
        m=m,
        n=len(cycle) // m,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=left_len,
        right_orbit_lengths=tuple(len(orbit) for orbit in q_orbits(right, q)),
        coordinate_count=len(values),
        coordinate_rank=coordinate_rank,
        relation_degree=degree,
        monomial_count=monomial_count,
        relation_rank=relation_rank,
        relation_nullity=nullity,
        random_trials=random_trials,
        random_nullity_min=min(random_values) if random_values else 0,
        random_nullity_max=max(random_values) if random_values else 0,
        random_positive_nullity_count=sum(1 for x in random_values if x > 0),
    )


def scan(args: argparse.Namespace) -> ProjectiveRelationRow | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
        ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        case_had_cycle = False
        for q, roots in splits:
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_projective_relation(
                                    D,
                                    q,
                                    ell,
                                    shifted,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args.degree,
                                    args.random_trials,
                                    args.seed,
                                )
                                if row is not None:
                                    return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible actual-CM projective-relation row found")

    print("Lang projective-relation audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit_rep={row.left_orbit_rep}")
    print(f"left_orbit_len={row.left_orbit_len}")
    print(f"right_orbit_lengths={list(row.right_orbit_lengths)}")
    print(f"coordinate_count={row.coordinate_count}")
    print(f"coordinate_rank={row.coordinate_rank}")
    print(f"relation_degree={row.relation_degree}")
    print(f"monomial_count={row.monomial_count}")
    print(f"relation_rank={row.relation_rank}")
    print(f"relation_nullity={row.relation_nullity}")
    print(f"random_trials={row.random_trials}")
    print(f"random_nullity_range={row.random_nullity_min}..{row.random_nullity_max}")
    print(f"random_positive_nullity_count={row.random_positive_nullity_count}")
    print()
    print("interpretation")
    print("  positive_low_degree_relation_suggests_RS_like_projective_geometry=1")
    print("  random_baseline_distinguishes_structure_from_generic_full_arc=1")
    print("conclusion=reported_lang_projective_relation_audit")


if __name__ == "__main__":
    main()

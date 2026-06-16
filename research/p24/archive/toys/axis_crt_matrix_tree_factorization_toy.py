#!/usr/bin/env python3
"""Toy audit for matrix-tree factorization of CRT-axis Cauchy-Binet weights.

The CRT-axis support note shows that the selected-origin Fourier minor has
support on spanning hypertrees of a complete multipartite incidence model.
This script asks a sharper question:

    do the surviving Cauchy-Binet coefficients factor as ordinary edge
    weights on those trees?

If yes, a graph/matrix-tree determinant could be a real compression theorem.
If no, matrix-tree language still describes support, but not the weighted
CM determinant-line polynomial.

The test is purely finite and small.  For a coefficient function c(B) on
bases B, an ordinary edge-weight factorization

    c(B) = C * prod_{e in B} a_e

implies the pair-sum relation

    c(B1)c(B2) = c(B3)c(B4)

whenever the two pairs have the same edge-count vector

    1_{B1} + 1_{B2} = 1_{B3} + 1_{B4}.

A single violated pair-sum relation proves that no ordinary edge-weighted
matrix-tree polynomial can have these coefficients.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass
from math import comb

import sympy as sp

from axis_crt_fourier_coefficient_support import (
    axis_frequencies,
    first_prime_one_mod,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class BasisCoefficient:
    subset: tuple[int, ...]
    prefix_det: int
    axis_det: int
    full_coeff: int


@dataclass(frozen=True)
class RelationWitness:
    first_pair: tuple[int, int]
    second_pair: tuple[int, int]
    first_product: int
    second_product: int
    count_vector: tuple[int, ...]


def det_mod(matrix: list[list[int]], q: int) -> int:
    mat = [row[:] for row in matrix]
    n = len(mat)
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col] % q
        det = (det * pivot_value) % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            if not mat[row][col] % q:
                continue
            scale = (mat[row][col] * inv) % q
            for j in range(col, n):
                mat[row][j] = (mat[row][j] - scale * mat[col][j]) % q
    return det % q


def determinant_data(m: int, q: int | None) -> tuple[int, int, list[int], int]:
    q = first_prime_one_mod(m) if q is None else q
    zeta = primitive_root_of_order(q, m)
    frequencies = axis_frequencies(m)
    return q, zeta, frequencies, len(frequencies)


def prefix_det(subset: tuple[int, ...], zeta: int, q: int) -> int:
    k = len(subset)
    return det_mod(
        [[pow(zeta, (row * u) % (q - 1), q) for u in subset] for row in range(k)],
        q,
    )


def axis_det(subset: tuple[int, ...], frequencies: list[int], zeta: int, m: int, q: int) -> int:
    return det_mod(
        [[pow(zeta, (-u * s) % m, q) for s in frequencies] for u in subset],
        q,
    )


def sampled_subsets(m: int, k: int, max_subsets: int, seed: int) -> tuple[bool, list[tuple[int, ...]]]:
    total = comb(m, k)
    if total <= max_subsets:
        return True, list(itertools.combinations(range(m), k))
    rng = random.Random(seed + 7919 * m + 104729 * k)
    out: set[tuple[int, ...]] = set()
    while len(out) < max_subsets:
        out.add(tuple(sorted(rng.sample(range(m), k))))
    return False, sorted(out)


def basis_coefficients(
    m: int,
    q: int,
    zeta: int,
    frequencies: list[int],
    subsets: list[tuple[int, ...]],
) -> list[BasisCoefficient]:
    out: list[BasisCoefficient] = []
    for subset in subsets:
        axis = axis_det(subset, frequencies, zeta, m, q)
        if axis == 0:
            continue
        prefix = prefix_det(subset, zeta, q)
        if prefix == 0:
            raise AssertionError("prefix Fourier determinant vanished on distinct columns")
        out.append(
            BasisCoefficient(
                subset=subset,
                prefix_det=prefix,
                axis_det=axis,
                full_coeff=(prefix * axis) % q,
            )
        )
    return out


def count_vector(left: tuple[int, ...], right: tuple[int, ...], m: int) -> tuple[int, ...]:
    counts = [0] * m
    for edge in left:
        counts[edge] += 1
    for edge in right:
        counts[edge] += 1
    return tuple(counts)


def find_pair_sum_violation(
    bases: list[BasisCoefficient],
    coeff_name: str,
    m: int,
    q: int,
    max_pairs: int,
) -> tuple[int, RelationWitness | None]:
    seen: dict[tuple[int, ...], tuple[int, tuple[int, int]]] = {}
    tested = 0
    for i, left in enumerate(bases):
        left_value = getattr(left, coeff_name)
        for j in range(i, len(bases)):
            right = bases[j]
            counts = count_vector(left.subset, right.subset, m)
            product = (left_value * getattr(right, coeff_name)) % q
            tested += 1
            prior = seen.get(counts)
            if prior is None:
                seen[counts] = (product, (i, j))
            elif prior[0] != product:
                return tested, RelationWitness(
                    first_pair=prior[1],
                    second_pair=(i, j),
                    first_product=prior[0],
                    second_product=product,
                    count_vector=counts,
                )
            if tested >= max_pairs:
                return tested, None
    return tested, None


def format_subset(bases: list[BasisCoefficient], pair: tuple[int, int]) -> str:
    return f"{bases[pair[0]].subset} + {bases[pair[1]].subset}"


def run_case(m: int, q_arg: int | None, max_subsets: int, max_pairs: int, seed: int) -> None:
    q, zeta, frequencies, k = determinant_data(m, q_arg)
    exact, subsets = sampled_subsets(m, k, max_subsets, seed)
    bases = basis_coefficients(m, q, zeta, frequencies, subsets)
    print(f"m={m} q={q} zeta={zeta} axis_dim={k} subset_count={comb(m, k)}")
    print(f"  tested_subsets={len(subsets)} exact_subsets={int(exact)} full_rank_bases={len(bases)}")
    print(f"  frequencies={frequencies}")
    for coeff_name in ("axis_det", "prefix_det", "full_coeff"):
        tested_pairs, witness = find_pair_sum_violation(bases, coeff_name, m, q, max_pairs)
        status = "violated" if witness is not None else "no_violation_seen"
        print(f"  coeff={coeff_name} pair_sum_status={status} tested_pairs={tested_pairs}")
        if witness is None:
            continue
        print(f"    pair_a={format_subset(bases, witness.first_pair)}")
        print(f"    pair_b={format_subset(bases, witness.second_pair)}")
        print(f"    product_a={witness.first_product} product_b={witness.second_product}")
        active = [idx for idx, value in enumerate(witness.count_vector) if value]
        print(f"    shared_edge_multiset={[(idx, witness.count_vector[idx]) for idx in active]}")
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", action="append", type=int, default=None)
    ap.add_argument("--q", type=int, default=None)
    ap.add_argument("--max-subsets", type=int, default=20000)
    ap.add_argument("--max-pairs", type=int, default=500000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    m_values = args.m if args.m is not None else [6, 10, 15, 30]
    print("axis CRT matrix-tree edge-factorization toy")
    print(f"max_subsets={args.max_subsets} max_pairs={args.max_pairs} seed={args.seed}")
    print()
    for m in m_values:
        run_case(m, args.q, args.max_subsets, args.max_pairs, args.seed)
    print("interpretation")
    print("  pair_sum_status=violated disproves c(B)=C*prod_edge a_edge for that coefficient family.")
    print("  axis_det controls CRT-incidence support; prefix_det is the Vandermonde/Plucker factor.")
    print("  full_coeff is the actual Cauchy-Binet coefficient up to a common scalar.")
    print("conclusion=reported_axis_crt_matrix_tree_factorization_toy")


if __name__ == "__main__":
    main()

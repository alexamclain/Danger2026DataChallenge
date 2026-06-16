#!/usr/bin/env python3
"""Strong-Rayleigh obstruction for CRT-axis incidence support.

The CRT-axis Cauchy-Binet support is the basis set of a complete multipartite
incidence matroid.  A tempting CS/probability shortcut is to import
strongly-Rayleigh / real-stable basis-polynomial machinery, then try to turn
negative dependence into p-unit noncancellation.

This toy checks the support-level prerequisite in exact small analogues.  For
a multiaffine basis generating polynomial

    B(x) = sum_{basis U} prod_{u in U} x_u,

strong Rayleigh implies every Rayleigh difference

    d_i B d_j B - B d_i d_j B

is nonnegative at all positive real weights.  One exact negative integer
witness disproves strong Rayleigh for that support matroid.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, product


RANK_MODULUS = 1_000_003


@dataclass(frozen=True)
class IncidenceModel:
    parts: tuple[int, ...]
    edges: tuple[tuple[int, ...], ...]
    features: tuple[tuple[int, ...], ...]
    rank: int
    bases: tuple[tuple[int, ...], ...]
    masks: tuple[int, ...]


@dataclass(frozen=True)
class RayleighValue:
    pair: tuple[int, int]
    weights: tuple[int, ...]
    basis_value: int
    deriv_i: int
    deriv_j: int
    deriv_ij: int
    delta: int


def rank_mod_q(rows: list[tuple[int, ...]], q: int = RANK_MODULUS) -> int:
    mat = [list(row) for row in rows]
    if not mat:
        return 0
    row_count = len(mat)
    col_count = len(mat[0])
    rank = 0
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(row_count):
            if row == rank or not mat[row][col] % q:
                continue
            scale = mat[row][col] % q
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == col_count:
            break
    return rank


def feature_vector(edge: tuple[int, ...], parts: tuple[int, ...]) -> tuple[int, ...]:
    vector = [1]
    for coordinate, part_size in zip(edge, parts):
        vector.extend(1 if coordinate == level else 0 for level in range(1, part_size))
    return tuple(vector)


def build_model(parts: tuple[int, ...]) -> IncidenceModel:
    edges = tuple(product(*(range(part) for part in parts)))
    features = tuple(feature_vector(edge, parts) for edge in edges)
    expected_rank = 1 + sum(part - 1 for part in parts)
    bases: list[tuple[int, ...]] = []
    masks: list[int] = []
    for subset in combinations(range(len(edges)), expected_rank):
        if rank_mod_q([features[index] for index in subset]) != expected_rank:
            continue
        bases.append(subset)
        mask = 0
        for index in subset:
            mask |= 1 << index
        masks.append(mask)
    return IncidenceModel(
        parts=parts,
        edges=edges,
        features=features,
        rank=expected_rank,
        bases=tuple(bases),
        masks=tuple(masks),
    )


def rayleigh_value(
    model: IncidenceModel,
    weights: tuple[int, ...],
    pair: tuple[int, int],
) -> RayleighValue:
    i, j = pair
    bit_i = 1 << i
    bit_j = 1 << j
    basis_value = 0
    deriv_i = 0
    deriv_j = 0
    deriv_ij = 0
    for basis, mask in zip(model.bases, model.masks):
        monomial = 1
        for edge_index in basis:
            monomial *= weights[edge_index]
        basis_value += monomial
        if mask & bit_i:
            deriv_i += monomial // weights[i]
        if mask & bit_j:
            deriv_j += monomial // weights[j]
        if (mask & bit_i) and (mask & bit_j):
            deriv_ij += monomial // (weights[i] * weights[j])
    return RayleighValue(
        pair=pair,
        weights=weights,
        basis_value=basis_value,
        deriv_i=deriv_i,
        deriv_j=deriv_j,
        deriv_ij=deriv_ij,
        delta=deriv_i * deriv_j - basis_value * deriv_ij,
    )


def all_ones_minimum(model: IncidenceModel) -> RayleighValue:
    weights = tuple(1 for _ in model.edges)
    values = [
        rayleigh_value(model, weights, pair)
        for pair in combinations(range(len(model.edges)), 2)
    ]
    return min(values, key=lambda value: value.delta)


def p223_witness() -> tuple[tuple[int, ...], tuple[int, int], tuple[int, ...]]:
    """Exact positive integer witness from a deterministic log-weight search."""

    return (
        (2, 2, 3),
        (1, 2),
        (
            947_825_266,
            1_495_154,
            670_610_371,
            146_109_419,
            1_172,
            21_102_355,
            12_310_118,
            1_666_564,
            39_898,
            7_010_852,
            4_670,
            406_061,
        ),
    )


def format_edge(model: IncidenceModel, index: int) -> str:
    return "(" + ",".join(str(value) for value in model.edges[index]) + ")"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-ones-parts", default="2,2,2")
    args = parser.parse_args()

    all_ones_parts = tuple(int(part) for part in args.all_ones_parts.split(","))
    all_ones_model = build_model(all_ones_parts)
    all_ones = all_ones_minimum(all_ones_model)

    witness_parts, witness_pair, witness_weights = p223_witness()
    witness_model = build_model(witness_parts)
    witness = rayleigh_value(witness_model, witness_weights, witness_pair)

    print("axis CRT strong-Rayleigh obstruction toy")
    print(f"rank_modulus={RANK_MODULUS}")
    print(
        f"all_ones parts={list(all_ones_model.parts)} edges={len(all_ones_model.edges)} "
        f"rank={all_ones_model.rank} bases={len(all_ones_model.bases)}"
    )
    print(
        f"  min_rayleigh_delta={all_ones.delta} "
        f"pair={all_ones.pair} "
        f"edges={format_edge(all_ones_model, all_ones.pair[0])},"
        f"{format_edge(all_ones_model, all_ones.pair[1])}"
    )
    print(
        f"witness parts={list(witness_model.parts)} edges={len(witness_model.edges)} "
        f"rank={witness_model.rank} bases={len(witness_model.bases)}"
    )
    print(
        f"  pair={witness.pair} "
        f"edges={format_edge(witness_model, witness.pair[0])},"
        f"{format_edge(witness_model, witness.pair[1])}"
    )
    print(f"  weights={list(witness.weights)}")
    print(f"  B={witness.basis_value}")
    print(f"  d_i={witness.deriv_i}")
    print(f"  d_j={witness.deriv_j}")
    print(f"  d_ij={witness.deriv_ij}")
    print(f"  rayleigh_delta={witness.delta}")
    print(f"  strong_rayleigh_violated={int(witness.delta < 0)}")
    print()
    print("interpretation")
    print("  A positive all-ones test is only a weak balancedness check.")
    print("  The exact negative weighted Rayleigh delta kills strong-Rayleigh/stability")
    print("  for the tripartite incidence support itself.")
    print("  Probability/Hodge language can still name the matroid, but not certify")
    print("  the p24 selected-prime Plucker p-unit by a real-stability shortcut.")
    print("conclusion=reported_axis_crt_strong_rayleigh_obstruction_toy")


if __name__ == "__main__":
    main()

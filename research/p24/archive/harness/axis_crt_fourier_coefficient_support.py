#!/usr/bin/env python3
"""Cauchy-Binet coefficient support for CRT-axis Fourier columns.

The selected-origin trace-frame Toeplitz minor has rows

    T = {0, ..., k-1}

and columns equal to the smooth CRT axis

    S_axis = {0} union nonzero characters on each coprime component of m.

In the Fourier/Cauchy-Binet expansion, the prefix-row determinant is a
Vandermonde and is nonzero for every k-subset U of Z/mZ.  Thus coefficient
support is controlled by one question:

    does the U x S_axis Fourier feature matrix have full rank?

This script audits that support on small composite analogues.  If the CRT axis
caused a large coefficient collapse, this would be a plausible route to a
smaller determinant-line identity.  If support is dense/generic, the p24 proof
still needs p-unit noncancellation for the full determinant line.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass
from math import comb

import sympy as sp

from crt_partial_moment_projection_scan import coprime_components
from k_character_tensor_factor_block_scan import frequency_blocks


@dataclass(frozen=True)
class SupportSummary:
    m: int
    q: int
    components: tuple[int, ...]
    axis_dim: int
    subset_count: int
    tested_subsets: int
    full_rank_count: int
    zero_coefficient_count: int
    min_rank: int
    rank_histogram: tuple[tuple[int, int], ...]
    exact: bool


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1")
    root = pow(int(sp.primitive_root(q)), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("bad root")
    for prime in sp.factorint(order):
        if pow(root, order // int(prime), q) == 1:
            raise AssertionError("root is not primitive")
    return root


def first_prime_one_mod(m: int, start: int = 2) -> int:
    q = max(start, m + 1)
    while True:
        q = int(sp.nextprime(q))
        if q % m == 1:
            return q


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    mat = [row[:] for row in matrix]
    if not mat:
        return 0
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank or not mat[row][col] % q:
                continue
            scale = mat[row][col] % q
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def axis_frequencies(m: int) -> list[int]:
    return [freq for _name, freqs in frequency_blocks(m) for freq in freqs]


def feature_table(frequencies: list[int], zeta: int, m: int, q: int) -> list[list[int]]:
    return [
        [pow(zeta, (u * s) % m, q) for s in frequencies]
        for u in range(m)
    ]


def feature_matrix(subset: tuple[int, ...], table: list[list[int]]) -> list[list[int]]:
    return [table[u][:] for u in subset]


def sampled_subsets(m: int, k: int, max_subsets: int, seed: int) -> tuple[bool, list[tuple[int, ...]]]:
    total = comb(m, k)
    if total <= max_subsets:
        return True, list(itertools.combinations(range(m), k))
    rng = random.Random(seed + 17 * m + 1009 * k)
    out: set[tuple[int, ...]] = set()
    while len(out) < max_subsets:
        out.add(tuple(sorted(rng.sample(range(m), k))))
    return False, sorted(out)


def summarize_m(m: int, q: int | None, max_subsets: int, seed: int) -> SupportSummary:
    if q is None:
        q = first_prime_one_mod(m)
    zeta = primitive_root_of_order(q, m)
    frequencies = axis_frequencies(m)
    k = len(frequencies)
    table = feature_table(frequencies, zeta, m, q)
    exact, subsets = sampled_subsets(m, k, max_subsets, seed)
    rank_hist: dict[int, int] = {}
    full = 0
    min_rank = k
    for subset in subsets:
        rank = rank_mod_q(feature_matrix(subset, table), q)
        rank_hist[rank] = rank_hist.get(rank, 0) + 1
        min_rank = min(min_rank, rank)
        if rank == k:
            full += 1
    return SupportSummary(
        m=m,
        q=q,
        components=coprime_components(m),
        axis_dim=k,
        subset_count=comb(m, k),
        tested_subsets=len(subsets),
        full_rank_count=full,
        zero_coefficient_count=len(subsets) - full,
        min_rank=min_rank,
        rank_histogram=tuple(sorted(rank_hist.items())),
        exact=exact,
    )


def fmt_hist(hist: tuple[tuple[int, int], ...]) -> str:
    return "[" + ",".join(f"{rank}:{count}" for rank, count in hist) + "]"


def default_m_values(max_m: int) -> list[int]:
    out: list[int] = []
    for m in range(2, max_m + 1):
        components = coprime_components(m)
        if len(components) >= 2:
            k = 1 + sum(component - 1 for component in components)
            if k < m:
                out.append(m)
    # Prefer squarefree-ish analogues first, but keep deterministic order.
    return sorted(out, key=lambda value: (len(coprime_components(value)), value))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", action="append", type=int, default=None)
    ap.add_argument("--max-m", type=int, default=42)
    ap.add_argument("--q", type=int, default=None)
    ap.add_argument("--max-subsets", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    m_values = args.m if args.m is not None else default_m_values(args.max_m)
    print("axis CRT Fourier Cauchy-Binet coefficient-support scan")
    print(f"max_subsets={args.max_subsets}")
    print("columns: m q components axis_dim subset_count tested exact full_rank zero_coeff min_rank rank_hist full_fraction")
    for m in m_values:
        summary = summarize_m(m, args.q, args.max_subsets, args.seed)
        full_fraction = summary.full_rank_count / summary.tested_subsets if summary.tested_subsets else 0.0
        print(
            f"m={summary.m} q={summary.q} components={list(summary.components)} "
            f"axis_dim={summary.axis_dim} subset_count={summary.subset_count} "
            f"tested={summary.tested_subsets} exact={int(summary.exact)} "
            f"full_rank={summary.full_rank_count} "
            f"zero_coeff={summary.zero_coefficient_count} "
            f"min_rank={summary.min_rank} rank_hist={fmt_hist(summary.rank_histogram)} "
            f"full_fraction={full_fraction:.6f}"
        )
    print()
    print("interpretation")
    print("  zero_coeff counts Cauchy-Binet coefficients killed by CRT-axis Fourier rank.")
    print("  dense full_rank means the CRT axis does not create a large support collapse.")
    print("  sampled rows are theorem-lab evidence, not p24 proof.")
    print("conclusion=reported_axis_crt_fourier_coefficient_support")


if __name__ == "__main__":
    main()

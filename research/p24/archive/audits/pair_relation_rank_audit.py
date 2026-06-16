#!/usr/bin/env python3
"""Low-degree relation audit for strict verifier pairs (A, x).

Most p24 audits project the strict DANGER bucket onto the Montgomery A-line.
The actual verifier, however, accepts points on the Kummer certificate curve

    Z_k(A, x) = 0,   Z_{k-1}(A, x) != 0.

If this curve had a hidden low-degree component in the affine (A, x)-plane,
one might sample certificates from that component without first selecting a
rare trace-compatible A.  This script tests that shape at small scale for
primes p = n^2 + 7 by enumerating the exact verifier pairs and checking whether
their evaluations on low-degree monomials have a nontrivial linear relation.

Full rank for total degree D means there is no nonzero field-specific
polynomial of total degree <= D vanishing on the exact accepted pair set.  A
uniform formula over Q(n) would in particular give such a field-specific
relation, so a single full-rank calibration row rules out that degree.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import prime_rows


@dataclass(frozen=True)
class RowResult:
    n: int
    p: int
    k: int
    pairs: int
    total_rank: int
    total_monomials: int
    rect_rank: int
    rect_monomials: int


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def accepted_pairs_for_row(p: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Enumerate exact verifier pairs using vectorized x-loops for each A."""
    k = verifier_k(p)
    inv4 = pow(4, -1, p)
    xs0 = np.arange(p, dtype=np.int64)
    accepted_A: list[np.ndarray] = []
    accepted_x: list[np.ndarray] = []

    for A in range(p):
        if (A * A - 4) % p == 0:
            continue
        C = ((A + 2) * inv4) % p
        X = xs0.copy()
        Z = np.ones(p, dtype=np.int64)
        Zprev = Z
        for _ in range(k):
            Zprev = Z
            xpz = (X + Z) % p
            xmz = (X - Z) % p
            U = (xpz * xpz) % p
            V = (xmz * xmz) % p
            W = (U - V) % p
            X = (U * V) % p
            Z = (W * ((V + C * W) % p)) % p
        mask = (Z == 0) & (Zprev != 0)
        if np.any(mask):
            count = int(np.count_nonzero(mask))
            accepted_A.append(np.full(count, A, dtype=np.int64))
            accepted_x.append(xs0[mask].copy())

    if not accepted_A:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64), k
    return np.concatenate(accepted_A), np.concatenate(accepted_x), k


def total_degree_monomials(max_degree: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(max_degree + 1) for j in range(max_degree + 1 - i)]


def rectangular_monomials(max_a_degree: int, max_x_degree: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(max_a_degree + 1) for j in range(max_x_degree + 1)]


def eval_matrix_mod_p(A: np.ndarray, x: np.ndarray, p: int, monomials: list[tuple[int, int]]) -> list[list[int]]:
    if len(A) == 0:
        return []
    max_a = max(i for i, _j in monomials)
    max_x = max(j for _i, j in monomials)
    powers_a = [np.ones(len(A), dtype=np.int64)]
    powers_x = [np.ones(len(x), dtype=np.int64)]
    for _ in range(max_a):
        powers_a.append((powers_a[-1] * A) % p)
    for _ in range(max_x):
        powers_x.append((powers_x[-1] * x) % p)
    cols = [((powers_a[i] * powers_x[j]) % p).astype(np.int64) for i, j in monomials]
    matrix_np = np.stack(cols, axis=1)
    return matrix_np.tolist()


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 0
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % p, p - 2, p)
        mat[rank] = [(value * inv) % p for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % p
            if factor:
                mat[row] = [(x - factor * y) % p for x, y in zip(mat[row], mat[rank])]
        rank += 1
        if rank == cols:
            break
    return rank


def audit_row(
    n: int,
    p: int,
    total_degree: int,
    rect_a_degree: int,
    rect_x_degree: int,
) -> RowResult:
    A, x, k = accepted_pairs_for_row(p)
    total_mons = total_degree_monomials(total_degree)
    rect_mons = rectangular_monomials(rect_a_degree, rect_x_degree)
    total_rank = rank_mod_p(eval_matrix_mod_p(A, x, p, total_mons), p)
    rect_rank = rank_mod_p(eval_matrix_mod_p(A, x, p, rect_mons), p)
    return RowResult(
        n=n,
        p=p,
        k=k,
        pairs=len(A),
        total_rank=total_rank,
        total_monomials=len(total_mons),
        rect_rank=rect_rank,
        rect_monomials=len(rect_mons),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=500)
    ap.add_argument("--max-p", type=int, default=12_000)
    ap.add_argument("--max-rows", type=int, default=8)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--total-degree", type=int, default=8)
    ap.add_argument("--rect-a-degree", type=int, default=4)
    ap.add_argument("--rect-x-degree", type=int, default=4)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("strict verifier pair low-degree relation rank audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"total_degree={args.total_degree}")
    print(f"rect_a_degree={args.rect_a_degree}")
    print(f"rect_x_degree={args.rect_x_degree}")
    print("row n p k accepted_pairs total_rank/nullity rect_rank/nullity")

    results: list[RowResult] = []
    for index, (n, p) in enumerate(rows, start=1):
        result = audit_row(n, p, args.total_degree, args.rect_a_degree, args.rect_x_degree)
        results.append(result)
        print(
            f"{index:02d} {result.n} {result.p} {result.k} {result.pairs} "
            f"{result.total_rank}/{result.total_monomials - result.total_rank} "
            f"{result.rect_rank}/{result.rect_monomials - result.rect_rank}"
        )

    full_total = sum(row.total_rank == row.total_monomials for row in results)
    full_rect = sum(row.rect_rank == row.rect_monomials for row in results)
    print("aggregate")
    print(f"  full_total_degree_rank_rows={full_total}/{len(results)}")
    print(f"  full_rectangular_rank_rows={full_rect}/{len(results)}")
    print("conclusion=no_low_degree_pair_component_visible" if full_total and full_rect else "conclusion=review_low_degree_relation")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Boundary audit for CS-theory routes to the representative p-unit.

The p24 representative obstruction is:

    K = ker(a_2, a_3, a_5, a_6) has dimension 16,
    pi_16(a_1)|_K is injective.

This script does two lightweight things.

1. Print deterministic p24 arithmetic metadata for common "K is special"
   theorem candidates.  In particular, a 16-dimensional subfield of
   F_{p^156} is impossible, but a Frobenius-invariant 16-plane is not ruled
   out by dimensions alone.

2. Run small random linear controls with the same prefix/tail shape.  These
   controls show which properties are formal rank facts and which would be
   strong extra arithmetic structure if they held for the actual CM K.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
from collections import Counter


P24_P = 10**24 + 7
P24_LEFT_DEGREE = 156
P24_RIGHT_ORBIT_DEGREE = 35
P24_TAIL_DIM = 16


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def euler_phi(n: int) -> int:
    return sum(1 for a in range(1, n + 1) if math.gcd(a, n) == 1)


def multiplicative_order(a: int, n: int) -> int:
    if n == 1:
        return 1
    if math.gcd(a, n) != 1:
        raise ValueError("order requires coprime inputs")
    x = a % n
    order = 1
    while x != 1:
        x = (x * a) % n
        order += 1
    return order


def frobenius_component_degrees(p: int, degree: int) -> list[int]:
    """Irreducible factor degrees of x^degree - 1 over F_p."""

    out: list[int] = []
    for d in divisors(degree):
        order = multiplicative_order(p, d)
        out.extend([order] * (euler_phi(d) // order))
    return out


def subset_count_for_sum(values: list[int], target: int) -> int:
    counts = [0] * (target + 1)
    counts[0] = 1
    for value in values:
        for total in range(target - value, -1, -1):
            counts[total + value] += counts[total]
    return counts[target]


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [
        [value % q for value in row]
        for row in matrix
        if any(value % q for value in row)
    ]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
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
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    mat = [[value % q for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return mat[:rank], pivots


def nullspace_basis(matrix: list[list[int]], q: int, cols: int) -> list[list[int]]:
    reduced, pivots = rref(matrix, q)
    pivot_set = set(pivots)
    free_cols = [col for col in range(cols) if col not in pivot_set]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vec = [0] * cols
        vec[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-reduced[row][free_col]) % q
        basis.append(vec)
    return basis


def mat_vec(row: list[int], vec: list[int], q: int) -> int:
    return sum(left * right for left, right in zip(row, vec)) % q


def restrict_rows_to_basis(
    rows: list[list[int]],
    basis: list[list[int]],
    q: int,
) -> list[list[int]]:
    return [[mat_vec(row, vec, q) for vec in basis] for row in rows]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def cyclic_shift(vec: list[int], shift: int) -> list[int]:
    n = len(vec)
    shift %= n
    if shift == 0:
        return list(vec)
    return vec[-shift:] + vec[:-shift]


def subspace_stable_under_shift(basis: list[list[int]], shift: int, q: int) -> bool:
    dim = rank_mod(basis, q)
    shifted = [cyclic_shift(vec, shift) for vec in basis]
    return rank_mod(basis + shifted, q) == dim


def min_hamming_weight(
    basis: list[list[int]],
    q: int,
    max_enumerate: int,
) -> int | None:
    dim = len(basis)
    total = q**dim - 1
    if total > max_enumerate:
        return None
    best = len(basis[0]) + 1 if basis else 0
    for coeffs in itertools.product(range(q), repeat=dim):
        if all(coeff == 0 for coeff in coeffs):
            continue
        vec = [0] * len(basis[0])
        for coeff, base_vec in zip(coeffs, basis):
            if coeff == 0:
                continue
            vec = [(left + coeff * right) % q for left, right in zip(vec, base_vec)]
        best = min(best, sum(1 for value in vec if value % q))
    return best


def p24_metadata() -> dict[str, object]:
    subfield_dims = divisors(P24_LEFT_DEGREE)
    component_degrees = frobenius_component_degrees(P24_P, P24_LEFT_DEGREE)
    degree_hist = Counter(component_degrees)
    return {
        "p": P24_P,
        "left_degree": P24_LEFT_DEGREE,
        "right_orbit_degree": P24_RIGHT_ORBIT_DEGREE,
        "tail_dim": P24_TAIL_DIM,
        "subfield_dimensions": subfield_dims,
        "tail_dim_is_subfield_dimension": P24_TAIL_DIM in subfield_dims,
        "frobenius_component_degree_hist": dict(sorted(degree_hist.items())),
        "frobenius_component_count": len(component_degrees),
        "frobenius_invariant_tail_dim_possible": (
            subset_count_for_sum(component_degrees, P24_TAIL_DIM) > 0
        ),
        "frobenius_invariant_tail_dim_component_choices": subset_count_for_sum(
            component_degrees, P24_TAIL_DIM
        ),
    }


def run_random_controls(args: argparse.Namespace) -> dict[str, object]:
    rng = random.Random(args.seed)
    source_dim = args.prefix_blocks * args.right_degree + args.tail_dim
    prefix_dim = args.prefix_blocks * args.right_degree
    tail_dim = args.tail_dim
    shift_values = tuple(args.shifts)

    prefix_full = 0
    determinant_full = 0
    tail_injective_given_prefix = 0
    prefix_full_tail_fail = 0
    shift_stable_counts = Counter({shift: 0 for shift in shift_values})
    min_weight_hist: Counter[int | str] = Counter()
    kernel_dim_hist: Counter[int] = Counter()

    for _ in range(args.trials):
        prefix_rows = random_matrix(prefix_dim, source_dim, args.q, rng)
        tail_rows = random_matrix(tail_dim, source_dim, args.q, rng)
        full_rank = rank_mod(prefix_rows + tail_rows, args.q)
        determinant_full += int(full_rank == source_dim)

        prefix_rank = rank_mod(prefix_rows, args.q)
        kernel = nullspace_basis(prefix_rows, args.q, source_dim)
        kernel_dim = len(kernel)
        kernel_dim_hist[kernel_dim] += 1
        if prefix_rank == prefix_dim:
            prefix_full += 1
            tail_rank = rank_mod(restrict_rows_to_basis(tail_rows, kernel, args.q), args.q)
            if tail_rank == tail_dim:
                tail_injective_given_prefix += 1
            else:
                prefix_full_tail_fail += 1
            for shift in shift_values:
                if subspace_stable_under_shift(kernel, shift, args.q):
                    shift_stable_counts[shift] += 1
            min_weight = min_hamming_weight(kernel, args.q, args.max_enumerate)
            min_weight_hist["skipped" if min_weight is None else min_weight] += 1

    return {
        "q": args.q,
        "right_degree": args.right_degree,
        "prefix_blocks": args.prefix_blocks,
        "tail_dim": tail_dim,
        "source_dim": source_dim,
        "prefix_dim": prefix_dim,
        "trials": args.trials,
        "prefix_full": prefix_full,
        "determinant_full": determinant_full,
        "tail_injective_given_prefix": tail_injective_given_prefix,
        "prefix_full_tail_fail": prefix_full_tail_fail,
        "kernel_dim_hist": dict(sorted(kernel_dim_hist.items())),
        "shift_stable_counts": dict(sorted(shift_stable_counts.items())),
        "min_hamming_weight_hist": dict(sorted(min_weight_hist.items(), key=str)),
    }


def print_mapping(title: str, mapping: dict[str, object]) -> None:
    print(title)
    for key, value in mapping.items():
        print(f"{key}={value}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--right-degree", type=int, default=8)
    parser.add_argument("--prefix-blocks", type=int, default=4)
    parser.add_argument("--tail-dim", type=int, default=4)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--shifts", type=int, nargs="*", default=[1, 2, 4])
    parser.add_argument("--max-enumerate", type=int, default=20000)
    args = parser.parse_args()

    print_mapping("p24_arithmetic_metadata", p24_metadata())
    print_mapping("random_prefix_kernel_controls", run_random_controls(args))
    print("interpretation=subfield_K_ruled_out; frobenius_module_K_not_ruled_out; tail_injectivity_not_formal")


if __name__ == "__main__":
    main()

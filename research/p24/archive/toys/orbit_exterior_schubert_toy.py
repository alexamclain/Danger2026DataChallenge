#!/usr/bin/env python3
"""Tiny orbit-level exterior Schubert expansion toy.

The p24 trace-GCD orbit determinant has the shape

    Delta(t) = det(P diag(zeta^(u*t)) W),     u in O,

where O is one right Frobenius orbit, P is the fixed selected-head projection,
and W is the CM 16-plane in the split orbit algebra.  Cauchy-Binet expands
Delta(t) as a character polynomial whose coefficients are fixed Schubert
minors times Plucker coordinates of W.

This toy verifies the expansion in a small orbit and searches for the key
boundary case: every fixed Schubert coefficient is nonzero and every Plucker
coordinate of W is nonzero, but one Delta(t) vanishes by cancellation.  That
is the finite reason the p24 theorem needs arithmetic p-adic noncancellation,
not only nonzero Fourier minors and nonzero Plucker coordinates.
"""

from __future__ import annotations

import argparse
import itertools
import random

import sympy as sp


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


def frobenius_orbit(start: int, multiplier: int, modulus: int) -> tuple[int, ...]:
    out: list[int] = []
    seen: set[int] = set()
    value = start % modulus
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = value * multiplier % modulus
    return tuple(out)


def det_mod(matrix: list[list[int]], q: int) -> int:
    if not matrix:
        return 1
    return int(sp.Matrix(matrix).det()) % q


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    if not left:
        return []
    rows = len(left)
    inner = len(right)
    cols = len(right[0]) if right else 0
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(inner)) % q
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def diagonal(values: list[int]) -> list[list[int]]:
    return [
        [value if i == j else 0 for j, value in enumerate(values)]
        for i, value in enumerate(values)
    ]


def subcols(matrix: list[list[int]], cols: tuple[int, ...]) -> list[list[int]]:
    return [[row[col] for col in cols] for row in matrix]


def subrows(matrix: list[list[int]], rows: tuple[int, ...]) -> list[list[int]]:
    return [matrix[row] for row in rows]


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def delta_value(
    P: list[list[int]],
    W: list[list[int]],
    orbit: tuple[int, ...],
    zeta: int,
    t: int,
    q: int,
) -> int:
    weights = [pow(zeta, (u * t) % (q - 1), q) for u in orbit]
    return det_mod(matmul(matmul(P, diagonal(weights), q), W, q), q)


def expansion_terms(
    P: list[list[int]],
    W: list[list[int]],
    orbit: tuple[int, ...],
    zeta: int,
    rank: int,
    q: int,
) -> list[tuple[tuple[int, ...], int, int]]:
    terms: list[tuple[tuple[int, ...], int, int]] = []
    for subset in itertools.combinations(range(len(orbit)), rank):
        fixed = det_mod(subcols(P, subset), q)
        plucker = det_mod(subrows(W, subset), q)
        terms.append((subset, fixed, plucker))
    return terms


def expansion_value(
    terms: list[tuple[tuple[int, ...], int, int]],
    orbit: tuple[int, ...],
    zeta: int,
    t: int,
    q: int,
) -> int:
    total = 0
    for subset, fixed, plucker in terms:
        exponent = sum(orbit[index] for index in subset) * t
        character = pow(zeta, exponent % (q - 1), q)
        total = (total + fixed * plucker * character) % q
    return total


def all_terms_nonzero(terms: list[tuple[tuple[int, ...], int, int]]) -> bool:
    return all(fixed != 0 and plucker != 0 for _subset, fixed, plucker in terms)


def find_cancellation_example(args: argparse.Namespace) -> tuple[
    list[list[int]],
    list[list[int]],
    list[tuple[tuple[int, ...], int, int]],
    list[int],
    list[int],
] | None:
    rng = random.Random(args.seed)
    zeta = primitive_root_of_order(args.field_q, args.right)
    orbit = frobenius_orbit(args.orbit_start, args.multiplier, args.right)
    rank = args.rank
    if len(orbit) < rank:
        raise ValueError("orbit length must be at least rank")

    for _trial in range(args.trials):
        P = random_matrix(rank, len(orbit), args.field_q, rng)
        W = random_matrix(len(orbit), rank, args.field_q, rng)
        terms = expansion_terms(P, W, orbit, zeta, rank, args.field_q)
        if not all_terms_nonzero(terms):
            continue
        direct = [delta_value(P, W, orbit, zeta, t, args.field_q) for t in orbit]
        expanded = [expansion_value(terms, orbit, zeta, t, args.field_q) for t in orbit]
        if direct != expanded:
            raise AssertionError("Cauchy-Binet expansion mismatch")
        if any(value == 0 for value in direct):
            return P, W, terms, direct, expanded
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--field-q", type=int, default=29)
    parser.add_argument("--right", type=int, default=7)
    parser.add_argument("--multiplier", type=int, default=2)
    parser.add_argument("--orbit-start", type=int, default=1)
    parser.add_argument("--rank", type=int, default=2)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    zeta = primitive_root_of_order(args.field_q, args.right)
    orbit = frobenius_orbit(args.orbit_start, args.multiplier, args.right)
    result = find_cancellation_example(args)

    print("orbit exterior Schubert toy")
    print(f"field_q={args.field_q}")
    print(f"right={args.right}")
    print(f"multiplier={args.multiplier}")
    print(f"orbit={list(orbit)}")
    print(f"orbit_len={len(orbit)}")
    print(f"rank={args.rank}")
    print(f"zeta={zeta}")
    print(f"trials={args.trials}")
    print(f"subset_count={sp.binomial(len(orbit), args.rank)}")

    if result is None:
        print("found_cancellation=0")
        print("conclusion=no_cancellation_example_found_in_budget")
        return

    P, W, terms, direct, expanded = result
    orbit_product = 1
    for value in direct:
        orbit_product = orbit_product * value % args.field_q

    print("found_cancellation=1")
    print(f"P={P}")
    print(f"W={W}")
    print(f"terms_subset_fixed_plucker={terms}")
    print(f"direct_delta_on_orbit={direct}")
    print(f"expanded_delta_on_orbit={expanded}")
    print(f"expansion_matches={int(direct == expanded)}")
    print(f"all_fixed_coefficients_nonzero={int(all(fixed for _, fixed, _ in terms))}")
    print(f"all_plucker_coordinates_nonzero={int(all(plucker for _, _, plucker in terms))}")
    print(f"zero_delta_count={sum(value == 0 for value in direct)}")
    print(f"orbit_product={orbit_product}")
    print("interpretation")
    print("  orbit_schubert_determinant_is_character_polynomial=1")
    print("  nonzero_coefficients_and_pluckers_do_not_prevent_cancellation=1")
    print("  p24_needs_selected_prime_punit_or_non_cancellation_theorem=1")
    print("conclusion=reported_orbit_exterior_schubert_boundary")


if __name__ == "__main__":
    main()

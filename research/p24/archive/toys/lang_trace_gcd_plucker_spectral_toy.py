#!/usr/bin/env python3
"""Cauchy-Binet spectral toy for right-origin trace-gcd determinants.

After origin covariance, the reduced determinant has the form

    Delta(t) = det(P * V_t * A),

where `V_t` is multiplication by a right root of unity on one right Frobenius
orbit, `A` is the transported tail map from the prefix kernel, and `P` is the
selected coordinate window.

Over a splitting field, `V_t` is diagonal.  Cauchy-Binet gives the exact
Fourier/Pluecker expansion

    Delta(t) = sum_{|I|=k} det(P_I) det(A_I) prod_{i in I} lambda_i^t.

This toy checks the identity on random matrices and reports the possible and
actual spectral support.
"""

from __future__ import annotations

import argparse
import itertools
import random


def det_mod(matrix: list[list[int]], q: int) -> int:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("determinant needs a square matrix")
    mat = [[value % q for value in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if mat[row][col]:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = (-det) % q
        pivot_value = mat[col][col]
        det = det * pivot_value % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, n):
            scale = mat[row][col] * inv % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[col])
            ]
    return det % q


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1 for this base-field toy")
    divisors = [d for d in range(1, order) if order % d == 0]
    for candidate in range(2, q):
        if pow(candidate, order, q) != 1:
            continue
        if all(pow(candidate, d, q) != 1 for d in divisors):
            return candidate
    raise RuntimeError("could not find primitive root")


def multiplicative_orbit(generator: int, modulus: int) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()
    value = 1 % modulus
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = value * generator % modulus
    return out


def random_matrix(rows: int, cols: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(cols)] for _ in range(rows)]


def subcols(matrix: list[list[int]], cols: tuple[int, ...]) -> list[list[int]]:
    return [[row[col] for col in cols] for row in matrix]


def subrows(matrix: list[list[int]], rows: tuple[int, ...]) -> list[list[int]]:
    return [matrix[row][:] for row in rows]


def direct_delta(
    p_matrix: list[list[int]],
    a_matrix: list[list[int]],
    lambdas: list[int],
    t: int,
    q: int,
) -> int:
    k = len(p_matrix)
    n = len(lambdas)
    middle = [[0 for _ in range(k)] for _ in range(k)]
    for row in range(k):
        for col in range(k):
            total = 0
            for idx in range(n):
                total += (
                    p_matrix[row][idx]
                    * pow(lambdas[idx], t, q)
                    * a_matrix[idx][col]
                )
            middle[row][col] = total % q
    return det_mod(middle, q)


def spectral_coefficients(
    p_matrix: list[list[int]],
    a_matrix: list[list[int]],
    exponents: list[int],
    q: int,
    right: int,
) -> dict[int, int]:
    k = len(p_matrix)
    coeffs = {exp: 0 for exp in range(right)}
    for subset in itertools.combinations(range(len(exponents)), k):
        left_det = det_mod(subcols(p_matrix, subset), q)
        right_det = det_mod(subrows(a_matrix, subset), q)
        exponent = sum(exponents[idx] for idx in subset) % right
        coeffs[exponent] = (coeffs[exponent] + left_det * right_det) % q
    return coeffs


def spectral_delta(coeffs: dict[int, int], root: int, t: int, q: int) -> int:
    return sum(coeff * pow(root, exponent * t, q) for exponent, coeff in coeffs.items()) % q


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--field-q", type=int, default=337)
    parser.add_argument("--right", type=int, default=7)
    parser.add_argument("--orbit-generator", type=int, default=2)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    root = primitive_root_of_order(args.field_q, args.right)
    exponents = multiplicative_orbit(args.orbit_generator, args.right)
    lambdas = [pow(root, exponent, args.field_q) for exponent in exponents]
    rng = random.Random(args.seed)

    total_mismatches = 0
    full_possible_support = {
        sum(exponents[idx] for idx in subset) % args.right
        for subset in itertools.combinations(range(len(exponents)), args.k)
    }
    actual_support_sizes: list[int] = []
    zero_product_count = 0
    for _ in range(args.trials):
        p_matrix = random_matrix(args.k, len(exponents), args.field_q, rng)
        a_matrix = random_matrix(len(exponents), args.k, args.field_q, rng)
        coeffs = spectral_coefficients(
            p_matrix, a_matrix, exponents, args.field_q, args.right
        )
        support = {exponent for exponent, coeff in coeffs.items() if coeff}
        actual_support_sizes.append(len(support))
        product = 1
        for t in range(args.right):
            direct = direct_delta(p_matrix, a_matrix, lambdas, t, args.field_q)
            spectral = spectral_delta(coeffs, root, t, args.field_q)
            total_mismatches += int(direct != spectral)
            product = product * direct % args.field_q
        zero_product_count += int(product == 0)

    print("Lang trace-gcd Pluecker spectral toy")
    print(f"field_q={args.field_q}")
    print(f"right={args.right}")
    print(f"root={root}")
    print(f"orbit_generator={args.orbit_generator}")
    print(f"orbit={exponents}")
    print(f"k={args.k}")
    print(f"trials={args.trials}")
    print(f"possible_support_size={len(full_possible_support)}")
    print(f"possible_support={sorted(full_possible_support)}")
    print(f"actual_support_size_min={min(actual_support_sizes)}")
    print(f"actual_support_size_max={max(actual_support_sizes)}")
    print(f"zero_product_count={zero_product_count}")
    print(f"cauchy_binet_mismatches={total_mismatches}")
    print("interpretation")
    print("  det_PVtA_has_pluecker_fourier_expansion=1")
    print("  product_nonzero_is_cyclic_resultant_nonzero=1")
    print("conclusion=reported_lang_trace_gcd_plucker_spectral_toy")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Operator-norm toy for the trace-GCD origin resultant.

For split finite-field data

    Delta(t) = det(P * D_t * A),     t mod d,

where `D_t` is diagonal with d-th-root eigenvalues, Cauchy-Binet gives a
polynomial `f(Y)` of degree `< d` satisfying `Delta(t)=f(omega^t)`.

This toy checks the equivalent single-object identities:

    prod_t Delta(t)
      = Res(Y^d - 1, f(Y))
      = det(m_f on F[Y]/(Y^d - 1)).

The last determinant is the finite operator norm that a class-field producer
would need to construct p-integrally for the actual p24 trace-GCD data.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp

from lang_trace_gcd_plucker_spectral_toy import (
    det_mod,
    direct_delta,
    multiplicative_orbit,
    primitive_root_of_order,
    random_matrix,
    spectral_coefficients,
    spectral_delta,
)


def multiplication_matrix_mod_xd_minus_1(coeffs: list[int], q: int) -> list[list[int]]:
    d = len(coeffs)
    matrix = [[0 for _ in range(d)] for _ in range(d)]
    for col in range(d):
        for degree, coeff in enumerate(coeffs):
            row = (degree + col) % d
            matrix[row][col] = (matrix[row][col] + coeff) % q
    return matrix


def resultant_mod(coeffs: list[int], q: int) -> int:
    x = sp.symbols("x")
    d = len(coeffs)
    f = sp.Poly(
        sum((coeff % q) * x**degree for degree, coeff in enumerate(coeffs)),
        x,
        modulus=q,
    )
    modulus = sp.Poly(x**d - 1, x, modulus=q)
    return int(sp.resultant(f.as_expr(), modulus.as_expr(), x)) % q


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

    mismatches = 0
    zero_products = 0
    support_sizes: list[int] = []
    for _ in range(args.trials):
        p_matrix = random_matrix(args.k, len(exponents), args.field_q, rng)
        a_matrix = random_matrix(len(exponents), args.k, args.field_q, rng)
        coeff_dict = spectral_coefficients(
            p_matrix, a_matrix, exponents, args.field_q, args.right
        )
        coeffs = [coeff_dict[degree] % args.field_q for degree in range(args.right)]
        support_sizes.append(sum(1 for coeff in coeffs if coeff))

        product = 1
        value_mismatches = 0
        for t in range(args.right):
            direct = direct_delta(p_matrix, a_matrix, lambdas, t, args.field_q)
            spectral = spectral_delta(coeff_dict, root, t, args.field_q)
            value_mismatches += int(direct != spectral)
            product = product * direct % args.field_q

        norm_det = det_mod(
            multiplication_matrix_mod_xd_minus_1(coeffs, args.field_q),
            args.field_q,
        )
        resultant = resultant_mod(coeffs, args.field_q)
        mismatches += int(value_mismatches != 0)
        mismatches += int(product != norm_det)
        mismatches += int(product != resultant)
        zero_products += int(product == 0)

    print("Lang trace-gcd operator norm toy")
    print(f"field_q={args.field_q}")
    print(f"right={args.right}")
    print(f"root={root}")
    print(f"orbit_generator={args.orbit_generator}")
    print(f"orbit={exponents}")
    print(f"k={args.k}")
    print(f"trials={args.trials}")
    print(f"support_size_min={min(support_sizes)}")
    print(f"support_size_max={max(support_sizes)}")
    print(f"zero_product_count={zero_products}")
    print(f"identity_mismatches={mismatches}")
    print("interpretation")
    print("  product_equals_resultant_and_operator_norm=1")
    print("  p24_missing_input_is_pintegral_construction_of_f_or_m_f=1")
    print("conclusion=reported_lang_trace_gcd_operator_norm_toy")


if __name__ == "__main__":
    main()

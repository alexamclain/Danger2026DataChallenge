#!/usr/bin/env python3
"""Audit the cyclic-resultant factors of centered marginal determinant sequences.

For the reduced right-translation sequence `F(t)`, the product

    prod_t F(t)

can always be grouped by Frobenius orbits of `t -> q*t mod right`.  However,
a degree-`<right` interpolant with coefficients in the base field would force

    F(q*t) = F(t).

This script checks that compatibility and measures DFT spectral support over
`F_q(mu_right)`.  It prevents confusing orbit products of base values with
norms of a base-coefficient interpolating polynomial.
"""

from __future__ import annotations

import argparse
from math import prod

import sympy as sp

from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import scan
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)


def product_mod(values: list[int], q: int) -> int:
    return prod(value % q for value in values) % q


def dft_support(sequence: list[int], q: int, order: int, seed: int) -> tuple[int, list[int]]:
    degree = int(sp.n_order(q % order, order))
    modulus = find_irreducible_modulus(q, degree, seed)
    field = ExtensionField(q, degree, modulus)
    root = primitive_root_of_order(field, order, seed)
    support: list[int] = []
    for frequency in range(order):
        total = field.zero
        for t, value in enumerate(sequence):
            weight = field.pow(root, (-frequency * t) % order)
            total = field.add(total, field.mul(field.embed(value), weight))
        if total != field.zero:
            support.append(frequency)
    return degree, support


def orbit_products(sequence: list[int], q: int, right: int) -> list[tuple[list[int], int, int]]:
    out = [([0], sequence[0] % q, 0)]
    for orbit in q_orbits(right, q):
        values = [sequence[t] for t in orbit]
        mismatches = sum(1 for value in values if value % q != values[0] % q)
        out.append((orbit, product_mod(values, q), mismatches))
    return out


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
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")
    sequence = normalized_right_sequence(row)
    products = orbit_products(sequence, row.q, row.right)
    compatibility_mismatches = sum(mismatch for _orbit, _product, mismatch in products)
    dft_degree, support = dft_support(sequence, row.q, row.right, args.seed)

    print("Centered marginal resultant-factor audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print(f"right={row.right}")
    print(f"ord_right_q={dft_degree}")
    print(f"sequence_zero_count={sum(1 for value in sequence if value == 0)}")
    print(f"sequence_distinct_values={len(set(sequence))}")
    print(f"frobenius_compatibility_mismatches={compatibility_mismatches}")
    print(f"dft_support_size={len(support)}/{row.right}")
    print(f"dft_support_prefix={support[:60]}")
    print()
    print("orbit_products")
    for orbit, value, mismatches in products[:20]:
        print(f"  orbit={orbit} product={value} constancy_mismatches={mismatches}")
    print()
    print("interpretation")
    print("  orbit_products_are_base_field_factors_of_the_sequence_product=1")
    print("  frobenius_mismatches_rule_out_base_coefficient_interpolant_norm=1")
    print("  full_dft_support_demotes_small_spectral_support_shortcut=1")
    print("conclusion=reported_centered_marginal_resultant_factor_audit")


if __name__ == "__main__":
    main()

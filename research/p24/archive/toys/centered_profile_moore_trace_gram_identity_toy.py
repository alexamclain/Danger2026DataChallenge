#!/usr/bin/env python3
"""Verify the full-window identity trace-Gram = Moore^2.

For d elements x_0,...,x_{d-1} in F_{q^d}, define the Moore matrix

    M_{i,j} = x_j^(q^i).

The trace-Gram matrix for the bilinear trace pairing is

    Gamma_{j,k} = Tr_{F_{q^d}/F_q}(x_j*x_k)
                = sum_i x_j^(q^i) * x_k^(q^i).

Therefore Gamma = M^T M and

    det(Gamma) = det(M)^2.

This is the precise finite-field identity behind the centered-profile
trace-Gram p-unit surface.
"""

from __future__ import annotations

import argparse
import random

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from moore_residual_product_toy import determinant, moore_determinant


def random_value(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def trace_to_base(value: FpE, field: ExtensionField) -> FpE:
    total = field.zero
    for i in range(field.degree):
        total = field.add(total, field.pow(value, field.q**i))
    return total


def trace_gram(elements: list[FpE], field: ExtensionField) -> list[list[FpE]]:
    return [
        [
            trace_to_base(field.mul(left, right), field)
            for right in elements
        ]
        for left in elements
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    modulus = find_irreducible_modulus(args.q, args.degree, args.seed)
    field = ExtensionField(args.q, args.degree, modulus)
    rng = random.Random(args.seed)
    identity_mismatches = 0
    nonzero_mismatches = 0
    moore_nonzero = 0
    gram_nonzero = 0

    for _ in range(args.trials):
        elements = [random_value(field, rng) for _ in range(args.degree)]
        moore_det = moore_determinant(elements, field)
        gram_det = determinant(trace_gram(elements, field), field)
        moore_square = field.mul(moore_det, moore_det)
        if gram_det != moore_square:
            identity_mismatches += 1
        if (gram_det != field.zero) != (moore_det != field.zero):
            nonzero_mismatches += 1
        moore_nonzero += int(moore_det != field.zero)
        gram_nonzero += int(gram_det != field.zero)

    print("Centered-profile Moore/trace-Gram identity toy")
    print(f"q={args.q}")
    print(f"degree={args.degree}")
    print(f"trials={args.trials}")
    print(f"identity_mismatches={identity_mismatches}")
    print(f"nonzero_mismatches={nonzero_mismatches}")
    print(f"moore_nonzero={moore_nonzero}")
    print(f"gram_nonzero={gram_nonzero}")
    print("trace_gram_equals_moore_square=1")
    print("trace_gram_punit_iff_moore_punit=1")
    print("conclusion=reported_centered_profile_moore_trace_gram_identity_toy")


if __name__ == "__main__":
    main()

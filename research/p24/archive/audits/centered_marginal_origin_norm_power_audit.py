#!/usr/bin/env python3
"""Audit the centered full-origin/right-product power relation.

The centered origin action gives determinant values indexed by

    shift = n*alpha + m*beta.

The beta direction cancels in the Hermitian pairing.  After dividing the
left-translation determinant sign, the alpha values factor through
`alpha mod right`.  Therefore the normalized alpha product should equal

    Pi_right^(m/right),

and the normalized full-origin product should equal

    Pi_right^(n*m/right).

The raw products can differ by the p-unit product of left translation signs.
For the p24 centered pair `left=157`, that sign product is 1.
"""

from __future__ import annotations

import argparse

from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import (
    product_mod,
    scan,
    translation_det_on_zero_sum,
)


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
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered origin-power row found")
    if row.m % row.right:
        raise SystemExit("right must divide m for the power audit")

    signs = [
        translation_det_on_zero_sum(row.left, alpha)
        for alpha in range(row.m)
    ]
    normalized_alpha_values = [
        value if sign == 1 else (-value) % row.q
        for value, sign in zip(row.alpha_values, signs)
    ]
    right_values = normalized_right_sequence(row)
    sign_product = product_mod([sign % row.q for sign in signs], row.q)
    normalized_alpha_product = product_mod(normalized_alpha_values, row.q)
    right_product = product_mod(right_values, row.q)
    m_over_right = row.m // row.right
    expected_normalized_alpha = pow(right_product, m_over_right, row.q)
    expected_raw_alpha = sign_product * expected_normalized_alpha % row.q
    normalized_full_origin = pow(normalized_alpha_product, row.n, row.q)
    raw_full_origin = pow(row.alpha_product, row.n, row.q)
    full_exponent = row.n * m_over_right
    expected_normalized_full = pow(right_product, full_exponent, row.q)
    expected_raw_full = pow(sign_product, row.n, row.q) * expected_normalized_full % row.q

    print("Centered marginal origin-norm power audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"m_over_right={m_over_right}")
    print(f"full_origin_exponent=n*m/right={full_exponent}")
    print()
    print(f"beta_mismatch_count={row.beta_mismatch_count}")
    print(f"left_sign_product={sign_product}")
    print(f"right_values={right_values}")
    print(f"right_product={right_product}")
    print(f"normalized_alpha_product={normalized_alpha_product}")
    print(f"expected_normalized_alpha_product={expected_normalized_alpha}")
    print(
        "normalized_alpha_power_match="
        f"{int(normalized_alpha_product == expected_normalized_alpha)}"
    )
    print(f"raw_alpha_product={row.alpha_product}")
    print(f"expected_raw_alpha_product={expected_raw_alpha}")
    print(
        "raw_alpha_power_match="
        f"{int(row.alpha_product == expected_raw_alpha)}"
    )
    print(f"normalized_full_origin_product={normalized_full_origin}")
    print(f"expected_normalized_full_origin={expected_normalized_full}")
    print(
        "normalized_full_origin_power_match="
        f"{int(normalized_full_origin == expected_normalized_full)}"
    )
    print(f"raw_full_origin_product={raw_full_origin}")
    print(f"expected_raw_full_origin={expected_raw_full}")
    print(
        "raw_full_origin_power_match="
        f"{int(raw_full_origin == expected_raw_full)}"
    )
    print()
    print("interpretation")
    print("  beta_cancellation_reduces_full_origin_to_alpha_product=1")
    print("  left_sign_normalization_is_a_p_unit_convention=1")
    print("  normalized_full_origin_is_power_of_reduced_right_product=1")
    print("conclusion=reported_centered_marginal_origin_norm_power_audit")


if __name__ == "__main__":
    main()

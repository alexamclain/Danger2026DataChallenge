#!/usr/bin/env python3
"""Accounting for full-origin norm routes versus certificate-scale routes.

The origin-norm power theorem says a full-origin product can imply the
211-term trace-GCD right product.  This script keeps the degree accounting
honest: a full-origin product computed by expanding over the whole CM torsor
has class-number scale, while a closed modular product or selected tower
producer could still be sub-sqrt.
"""

from __future__ import annotations

import math


P = 10**24 + 7
H = 205_880_396_014
M = 66_254
N = 3_107_441
RIGHT = 211
LEFT_OTHER = M // RIGHT
FULL_ORIGIN_EXPONENT = N * LEFT_OTHER
SELECTED_CHAIN_DEGREES = (2, 157, 211, N)
FACTOR_ROUTE_DEGREES = (M, N)
RIGHT_VALUE_PAYLOAD = 2 * RIGHT
ORBIT_PRODUCT_PAYLOAD = 2 * 7
NORM_PAYLOAD = 2


def ratio(value: int, denominator: float) -> str:
    return f"{value / denominator:.12g}"


def main() -> None:
    sqrt_p = math.sqrt(P)
    print("full-origin norm versus class-enumeration accounting")
    print(f"p={P}")
    print(f"sqrt_p={sqrt_p:.0f}")
    print(f"h={H}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"right={RIGHT}")
    print(f"m_over_right={LEFT_OTHER}")
    print(f"n_m_over_right={FULL_ORIGIN_EXPONENT}")
    print()
    print("finite_payloads")
    print(f"  right_value_plus_inverse={RIGHT_VALUE_PAYLOAD}")
    print(f"  orbit_products_plus_inverse={ORBIT_PRODUCT_PAYLOAD}")
    print(f"  one_norm_plus_inverse={NORM_PAYLOAD}")
    print(f"  right_value_payload_over_sqrt={ratio(RIGHT_VALUE_PAYLOAD, sqrt_p)}")
    print(f"  one_norm_payload_over_sqrt={ratio(NORM_PAYLOAD, sqrt_p)}")
    print()
    print("producer_degree_surfaces")
    print(f"  full_class_torsor_degree={H}")
    print(f"  full_class_torsor_over_sqrt={ratio(H, sqrt_p)}")
    print(
        "  selected_chain_degree_sum="
        f"{sum(SELECTED_CHAIN_DEGREES)}"
    )
    print(
        "  selected_chain_over_sqrt="
        f"{ratio(sum(SELECTED_CHAIN_DEGREES), sqrt_p)}"
    )
    print(f"  factor_route_degree_sum={sum(FACTOR_ROUTE_DEGREES)}")
    print(
        "  factor_route_over_sqrt="
        f"{ratio(sum(FACTOR_ROUTE_DEGREES), sqrt_p)}"
    )
    print()
    print("interpretation")
    print("  full_origin_norm_from_H_D_coefficients_is_class_number_scale=1")
    print("  closed_Borcherds_or_Fitting_formula_could_still_be_subsqrt=1")
    print("  selected_chain_and_factor_routes_remain_the_subsqrt_degree_targets=1")
    print("conclusion=reported_full_origin_norm_vs_class_enumeration_accounting")


if __name__ == "__main__":
    main()

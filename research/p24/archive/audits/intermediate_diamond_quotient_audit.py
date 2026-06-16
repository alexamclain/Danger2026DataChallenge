#!/usr/bin/env python3
"""Audit intermediate diamond quotients between X1(2^k)/+- and X0(2^k).

The verifier needs a rational x-coordinate of exact order 2^k, so the relevant
oriented modular datum is X1(2^k) with P identified with -P.  X0(2^k) records
only the cyclic subgroup.  A natural remaining loophole is an intermediate
diamond quotient: perhaps remember enough of the generator to make construction
easier than X1, but not so little that the missing orientation tail is large.

For k >= 3 the diamond group after quotienting by +/-1 is cyclic of order

    phi(2^k)/2 = 2^(k-2).

Thus intermediate quotients are indexed by a single subgroup size 2^s.  If an
algorithm constructs the quotient where Frobenius is known only up to that
subgroup, it still has to select the strict class lambda = +/-1 among 2^s
remaining orientations.  The construction/lift product is invariant.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
K = 40


def gamma0_power2_index(k: int) -> int:
    return 3 * (1 << (k - 1))


def main() -> None:
    sqrt_p = math.isqrt(P24)
    diamond_mod_sign = 1 << (K - 2)
    gamma0 = gamma0_power2_index(K)

    print("p24 intermediate diamond quotient audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"Gamma0(2^k)_index={gamma0}")
    print(f"Gamma0_index_over_sqrt={gamma0 / sqrt_p:.6f}")
    print(f"diamond_group_mod_sign_order=phi(2^k)/2={diamond_mod_sign}")
    print("diamond_group_mod_sign_structure=cyclic_2_power")
    print()
    print(
        "subgroup_bits quotient_degree_to_X0 quotient_index_over_sqrt "
        "residual_orientation_count quotient_times_residual_over_sqrt"
    )

    best_index: tuple[float, int] | None = None
    best_product: tuple[float, int] | None = None
    for subgroup_bits in range(0, K - 1):
        subgroup_size = 1 << subgroup_bits
        quotient_degree_to_x0 = diamond_mod_sign // subgroup_size
        quotient_index = gamma0 * quotient_degree_to_x0
        residual_orientation = subgroup_size
        product = quotient_index * residual_orientation

        index_ratio = quotient_index / sqrt_p
        product_ratio = product / sqrt_p
        if best_index is None or index_ratio < best_index[0]:
            best_index = (index_ratio, subgroup_bits)
        if best_product is None or product_ratio < best_product[0]:
            best_product = (product_ratio, subgroup_bits)

        if subgroup_bits <= 8 or subgroup_bits % 4 == 0 or subgroup_bits >= K - 6:
            print(
                f"{subgroup_bits:13d} {quotient_degree_to_x0:21d} "
                f"{index_ratio:24.6e} {residual_orientation:26d} "
                f"{product_ratio:34.6e}"
            )

    assert best_index is not None and best_product is not None
    print()
    print(
        f"best_quotient_index=subgroup_bits={best_index[1]} "
        f"index_over_sqrt={best_index[0]:.6e}"
    )
    print(
        f"best_index_times_residual=subgroup_bits={best_product[1]} "
        f"product_over_sqrt={best_product[0]:.6e}"
    )
    print(
        "conclusion=intermediate_diamond_quotients_only_trade_modular_index_"
        "against_the_same_missing_orientation_fiber"
    )


if __name__ == "__main__":
    main()

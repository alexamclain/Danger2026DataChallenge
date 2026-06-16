#!/usr/bin/env python3
"""Toy audit for relative norm/product period selectors.

Gross-Zagier/Borcherds style formulas naturally compute Galois-symmetric
products/norms of singular moduli.  A tempting variant of the split-cycle route
is therefore:

    z_r = prod_{k=0}^{n-1} j_{r+mk}

instead of the additive period y_r=sum j_{r+mk}.  The values z_r also lie in
the embedded quotient field, and their degree-m polynomial is cheap once the
CM vertices are known.

This toy shows the catch.  The individual coset products are good embedded
quotient coordinates, but the global norm/product is only the product over all
z_r.  It loses the coset phase just as a genus/global trace loses the
high-order additive phase.  Computing the whole degree-m product polynomial is
exactly a relative norm N_{H/H^H}(X-j), i.e. the same subgroup enumeration or a
new non-enumerative relative-norm theorem.
"""

from __future__ import annotations

from character_period_transform_toy import Q, QUOTIENT_SIZE
from embedded_decomposition_calibration import D, ELL, H, isogeny_neighbors, monic_poly_from_roots, pari_linear_roots, walk_cycle
from cypari2 import Pari

SUBGROUP_SIZE = 3


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * value % q
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    cosets = [
        [cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)]
        for r in range(QUOTIENT_SIZE)
    ]
    period_sums = [sum(coset) % Q for coset in cosets]
    period_products = [product(coset, Q) for coset in cosets]
    product_poly = monic_poly_from_roots(period_products, Q)
    global_norm_from_roots = product(cycle, Q)
    global_norm_from_periods = product(period_products, Q)

    even_products = [period_products[r] for r in range(0, QUOTIENT_SIZE, 2)]
    odd_products = [period_products[r] for r in range(1, QUOTIENT_SIZE, 2)]
    genus_product_pair = [product(even_products, Q), product(odd_products, Q)]

    print("relative norm phase toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print()
    print(f"period_sums={period_sums}")
    print(f"period_products={period_products}")
    print(f"distinct_period_products={len(set(period_products))}")
    print(f"period_product_polynomial_degree={len(product_poly) - 1}")
    print(f"period_product_polynomial_coeffs_ascending_mod_q={product_poly}")
    print()
    print("galois_symmetric_norms")
    print(f"  global_norm_from_all_roots={global_norm_from_roots}")
    print(f"  global_norm_from_period_products={global_norm_from_periods}")
    print(f"  global_norms_match={int(global_norm_from_roots == global_norm_from_periods)}")
    print(f"  genus_even_odd_product_pair={genus_product_pair}")
    print()
    print("interpretation")
    print("  individual_coset_products_are_valid_quotient_coordinates=1")
    print("  global_norm_erases_the_quotient_coset_phase=1")
    print("  genus_norms_leave_large_odd_quotient_buckets=1")
    print("  full_relative_norm_polynomial_requires_all_coset_product_coefficients=1")
    print(
        "conclusion=norm_product_formulas_help_only_if_they_are_relative_to_"
        "the_desired_high_order_subgroup; global_or_genus_norms_do_not_select_a_cycle"
    )


if __name__ == "__main__":
    main()

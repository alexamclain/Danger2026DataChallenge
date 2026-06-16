#!/usr/bin/env python3
"""Audit the class-character period route for the p24 split-cycle quotient.

If G=Cl(O) is cyclic and H<=G is the subgroup corresponding to a split-prime
cycle, the period sums over H-cosets are inverse Fourier transforms of twisted
traces by the characters of G/H.  This is the exact analogue of Gaussian
periods in cyclotomic fields.

The DFT layer is cheap for the p24 cycle quotients.  The missing theorem would
have to compute the relevant class-character twisted traces of singular moduli
without enumerating the class group.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
SQRT_P = math.isqrt(P24)

CANDIDATES = [
    {
        "label": "ell_677_cycle",
        "ell": 677,
        "subgroup_size": 655670051,
        "quotient_size": 314,
    },
    {
        "label": "ell_7349_cycle",
        "ell": 7349,
        "subgroup_size": 487868237,
        "quotient_size": 422,
    },
    {
        "label": "balanced_abstract_split",
        "ell": 23,
        "subgroup_size": 3107441,
        "quotient_size": 66254,
    },
]


def multiplicative_order_mod_p(modulus: int) -> int | None:
    if math.gcd(P24, modulus) != 1:
        return None
    return int(sp.n_order(P24 % modulus, modulus))


def main() -> None:
    print("p24 class-character period route audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print(f"sqrt_floor_p={SQRT_P}")
    print()

    print("period_transform_requirements")
    print(
        "  label ell subgroup_size quotient_size twisted_traces "
        "phi(quotient) root_of_unity_extension over_sqrt_max_period_degree"
    )
    for row in CANDIDATES:
        m = row["quotient_size"]
        n = row["subgroup_size"]
        root_ext = multiplicative_order_mod_p(m)
        print(
            f"  {row['label']:24s} {row['ell']:5d} {n:13d} {m:13d} "
            f"{m:14d} {int(sp.totient(m)):13d} {root_ext:23d} "
            f"{max(m, n) / SQRT_P:27.6e}"
        )
    print()

    print("fourier_formulation")
    print("  Let G=<g> and H=<g^m>, with m=quotient_size and n=subgroup_size.")
    print("  Periods:       y_r = sum_{k=0}^{n-1} j(g^{r+mk})")
    print("  Twisted traces T_s = sum_{i=0}^{h-1} zeta_m^{s*i} j(g^i)")
    print("  Then y_r = m^{-1} sum_s zeta_m^{-sr} T_s.")
    print()

    print("known_theorem_boundary")
    print("  zagier_total_trace_available=1")
    print("  genus_character_twisted_traces_available=1")
    print("  arbitrary_large_ring_class_character_traces_available_as_cheap_formula=0")
    print("  p24_required_characters_are_non_genus=1")
    print("  p24_required_character_orders_include_157_or_211=1")
    print("  half_integral_weight_or_theta_lift_level_depends_on_D_or_character=1")
    print()

    print("interpretation")
    print("  dft_root_of_unity_extensions_are_not_the_main_obstruction=1")
    print("  ell_7349_needs_only_422_twisted_traces_and_extension_degree_35=1")
    print("  ell_677_needs_314_twisted_traces_and_extension_degree_156=1")
    print("  missing_primitive=sublinear_non_genus_twisted_trace_computation=1")
    print(
        "conclusion=class_character_periods_rephrase_the_split_cycle_selector_"
        "but_do_not_yet_supply_the_asymptotic_speedup"
    )


if __name__ == "__main__":
    main()

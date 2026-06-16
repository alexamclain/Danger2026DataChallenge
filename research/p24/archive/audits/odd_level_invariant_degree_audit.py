#!/usr/bin/env python3
"""Audit odd-level modular invariant degrees for the smooth p24 CM lead.

The smooth third target suggests odd quotients of the class group with factors
157, 211, and 3107441.  A modular function on X0(N) or an N-isogeny relation
could in principle provide an embedded invariant with a map back to j.

This script records the simple degree facts.  For prime N=ell, the relation
to j has degree roughly ell+1 (the degree of Phi_ell in each variable).  These
degrees may be far below sqrt(p), but constructing the relation or using the
isogeny graph without a seed target vertex is the hard part.
"""

from __future__ import annotations

from fractions import Fraction
import math

import sympy as sp

P24 = 10**24 + 7
TRACE = -1178414874616
CLASS_NUMBER = 205880396014
CLASS_FACTORS = [2, 157, 211, 3107441]
ODD_LEVELS = [23, 157, 211, 677, 2897, 7349, 14057, 3107441]


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 odd-level invariant degree audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_factors={CLASS_FACTORS}")
    print(f"sqrt_floor={sqrt_p}")
    print()
    print("level gamma0_index gamma0_over_sqrt phi_degree_proxy degree_proxy_over_sqrt")
    for level in ODD_LEVELS:
        idx = gamma0_index(level)
        # For prime ell this is ell+1; for composite N this remains the
        # natural X0(N)->X(1) degree proxy.
        degree_proxy = idx
        print(
            f"{level:8d} {idx:12d} {idx / sqrt_p:16.6e} "
            f"{degree_proxy:16d} {degree_proxy / sqrt_p:22.6e}"
        )
    print()
    print("composite_factor_levels")
    for level in [157 * 211, 157 * 3107441, 211 * 3107441, 157 * 211 * 3107441]:
        idx = gamma0_index(level)
        print(
            f"  level={level:15d} gamma0_index={idx:15d} "
            f"gamma0_over_sqrt={idx / sqrt_p:.6e}"
        )
    print()
    print("obstruction")
    print("  low_recovery_degree_possible_for_some_levels=1")
    print("  modular_polynomial_or_embedded_relation_required=1")
    print("  isogeny_action_requires_seed_target_vertex=1")
    print("  abstract_class_group_factorization_provides_seed=0")
    print(
        "conclusion=odd_level_invariants_have_subsqrt_recovery_degrees_but_"
        "do_not_supply_embedded_equations_or_seed_roots_for_free"
    )


if __name__ == "__main__":
    main()

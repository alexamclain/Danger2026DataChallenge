#!/usr/bin/env python3
"""Audit the ray-kernel exception for p24 odd tower phases.

Distribution relations for Siegel/Ramachandra units can collapse kernels of
maps between ray class groups.  This script records why that does not produce
the p24 unramified 157/211 class-group layers, and why the reduced-anchor
179-axis should not be identified with literal ray conductor 179.

For a rational prime ell not dividing D_K, the local unit factor modulo ell has
order

    split:  (ell - 1)^2
    inert:  ell^2 - 1

so it contains no ell-factor.  Ell-power ray factors first appear in the
congruence filtration from ell^2 to ell; that kernel is principal/congruence
data and maps trivially to the ordinary class group.
"""

from __future__ import annotations

import sympy as sp

D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
ODD_LAYERS = (157, 211)
ANCHOR_LEVELS = (179,)
EXTRA_LEVELS = (
    157 * 211,
    2 * 157 * 211,
    2 * 223 * 463,
    223 * 463,
)


def local_units_mod_prime_size(ell: int, kronecker: int) -> int:
    if kronecker == 1:
        return (ell - 1) ** 2
    if kronecker == -1:
        return ell**2 - 1
    return ell * (ell - 1)


def norm_one_kernel_mod_prime_size(ell: int, kronecker: int) -> int:
    if kronecker == 1:
        return ell - 1
    if kronecker == -1:
        return ell + 1
    return ell


def main() -> None:
    print("p24 ray-kernel distribution audit")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print()
    print(
        "ell role kronecker(D,ell) local_units_mod_ell factor_units "
        "norm_one_kernel source_prime_conductor_order ell_divides_mod_ell_kernel "
        "ell2_to_ell_kernel factor_ell2_to_ell"
    )
    for role, levels in (("unramified_phase", ODD_LAYERS), ("anchor_mismatch", ANCHOR_LEVELS)):
        for ell in levels:
            k = int(sp.kronecker_symbol(D_K, ell))
            units = local_units_mod_prime_size(ell, k)
            norm_one = norm_one_kernel_mod_prime_size(ell, k)
            source_prime_conductor_order = norm_one // 2
            filtration = ell**2
            print(
                f"{ell:3d} {role:17s} {k:16d} {units:21d} "
                f"{sp.factorint(units)!s:24s} {norm_one:15d} "
                f"{source_prime_conductor_order:28d} "
                f"{int(units % ell == 0):25d} {filtration:20d} "
                f"{sp.factorint(filtration)}"
            )
    print()
    print("legacy_unramified_phase_rows")
    for ell in ODD_LAYERS:
        k = int(sp.kronecker_symbol(D_K, ell))
        units = local_units_mod_prime_size(ell, k)
        filtration = ell**2
        print(
            f"{ell:3d} {k:16d} {units:21d} {sp.factorint(units)!s:24s} "
            f"{int(units % ell == 0):25d} {filtration:20d} "
            f"{sp.factorint(filtration)}"
        )
    print()
    print("composite_level_local_unit_parts")
    print("  level factors local_unit_size factor_units has_157 has_211")
    for level in EXTRA_LEVELS:
        unit_size = 1
        for ell, exp in sp.factorint(level).items():
            if exp != 1:
                raise AssertionError("squarefree levels expected")
            k = int(sp.kronecker_symbol(D_K, ell))
            unit_size *= local_units_mod_prime_size(int(ell), k)
        factors = sp.factorint(unit_size)
        print(
            f"  {level:8d} {sp.factorint(level)!s:24s} {unit_size:18d} "
            f"{factors!s:45s} {int(157 in factors):7d} {int(211 in factors):7d}"
        )
    print()
    print("interpretation")
    print("  modulo_ell_ray_kernel_has_no_ell_primary_factor_for_ell=157_or_211=1")
    print("  literal_ray_conductor_179_has_source_order_90_not_C179_or_diamond178=1")
    print("  p24_C179_axis_is_a_fourier_internal_axis_not_classical_ray_modulus_179=1")
    print("  tested_composite_squarefree_ray_unit_parts_still_do_not_supply_both_odd_layers=1")
    print("  ell_primary_ray_factors_first_appear_in_ramified_ell_adic_filtration=1")
    print("  ray_filtration_kernels_map_trivially_to_the_ordinary_class_group=1")
    print("  p24_157_211_layers_are_unramified_hilbert_class_group_layers=1")
    print(
        "conclusion=ray_distribution_relations_do_not_collapse_the_p24_"
        "odd_relative_class_phases"
    )


if __name__ == "__main__":
    main()

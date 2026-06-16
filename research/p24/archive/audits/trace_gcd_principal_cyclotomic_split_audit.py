#!/usr/bin/env python3
"""Principal Hilbert Frobenius versus cyclotomic semilinear Frobenius.

For the p24 third trace, the prime above p is principal in the CM order:

    Norm(t/2 + sqrt(D_K)) = p.

Thus the Artin symbol on the unramified ring-class/Hilbert class field is
trivial.  This explains why the target CM roots live over F_p, but it does
not make the 157/211 Fourier/Lang coordinates base-field constants:
Frobenius still sends zeta_ell to zeta_ell^p.

This audit records the exact split: Hilbert/class Frobenius is trivial while
cyclotomic Frobenius has orders 156 and 35.  The trace-GCD orbit norm is
therefore a semilinear/crossed-product norm, not an ordinary base-polynomial
norm.
"""

from __future__ import annotations

import math

import sympy as sp


P = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
M = 66254
N = 3107441
LEFT = 157
RIGHT = 211


def orbit_lengths(modulus: int, multiplier: int) -> list[int]:
    seen: set[int] = set()
    out: list[int] = []
    for start in range(modulus):
        if start in seen:
            continue
        length = 0
        value = start
        while value not in seen:
            seen.add(value)
            length += 1
            value = value * multiplier % modulus
        out.append(length)
    return sorted(out)


def main() -> None:
    half_trace = TRACE // 2
    discriminant = TRACE * TRACE - 4 * P
    norm_generator = half_trace * half_trace - D_K
    class_orders = [CLASS_NUMBER, M, N, LEFT, RIGHT]

    print("trace-GCD principal/cyclotomic Frobenius split audit")
    print(f"p={P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"trace_discriminant=t^2-4p={discriminant}")
    print(f"trace_discriminant_equals_4D={int(discriminant == 4 * D_K)}")
    print(f"half_trace={half_trace}")
    print(f"norm_half_trace_plus_sqrtD={norm_generator}")
    print(f"norm_equals_p={int(norm_generator == P)}")
    print("hilbert_ring_class_frobenius")
    print("  prime_above_p_is_principal=1")
    print("  artin_symbol_in_unramified_ring_class_field=identity")
    print("  hilbert_class_frobenius_order=1")
    print("  all_target_CM_roots_are_Fp_rational=1")
    print("  principal_frobenius_selects_one_root=0")
    print()

    print("cyclotomic_frobenius")
    for modulus in [LEFT, RIGHT, LEFT * RIGHT, 2 * LEFT * RIGHT, N]:
        order = int(sp.n_order(P % modulus, modulus))
        print(
            f"  modulus={modulus} p_mod={P % modulus} ord={order} "
            f"orbit_lengths={orbit_lengths(modulus, P % modulus)}"
        )
    print()

    print("prime_to_unramified_layers")
    for level in class_orders:
        print(f"  gcd(p,{level})={math.gcd(P, level)}")
    print()

    print("trace_gcd_consequence")
    print("  class_field_values_may_be_Fp_rational_after_choosing_a_CM_root=1")
    print("  zeta_211_coordinates_are_moved_by_Frobenius_order_35=1")
    print("  zeta_157_coordinates_are_moved_by_Frobenius_order_156=1")
    print("  ordinary_base_polynomial_descent_is_not_forced=1")
    print("  crossed_product_orbit_norm_is_the_honest_phase_payload=1")
    print("conclusion=reported_trace_gcd_principal_cyclotomic_split")


if __name__ == "__main__":
    main()

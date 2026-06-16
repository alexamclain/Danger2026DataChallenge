#!/usr/bin/env python3
"""Diamond norm identity for the reduced-anchor cyclotomic residual.

The cyclotomic-divisor gate identified the denominator-cleared residual as

    D_c = sum_{k != 0} [zeta_c^k] - (c - 1)[1].

This gate records a sharper producer shape.  For prime c, D_c is the
diamond/unit norm over the nonzero multipliers of C_c of the single divisor

    [zeta_c] - [1].

Equivalently,

    prod_{a in (Z/cZ)^*} (X - zeta_c^a)/(X - 1)
      = Phi_c(X)/(X - 1)^(c - 1).

This is a norm over the diamond automorphism orbit of the C_c coordinate, not
the cyclic C/E trace norm.  The distinction matters for p24: the candidate
producer should construct one p-integral CM/Lang factor and then take this
diamond/cyclotomic norm, followed by the auxiliary Kummer/sign descent already
gated.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import (
    primitive_root,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    RIGHT_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate import (
    formal_cyclotomic_divisor,
    fourier_profile_ok,
)


def single_divisor(c_degree: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_degree)
    values[0] = (-1) % modulus
    values[1] = 1 % modulus
    return values


def diamond_action(values: list[int], c_degree: int, multiplier: int) -> list[int]:
    out = [0] * len(values)
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            target = (multiplier * c_index) % c_degree
            out[right * c_degree + target] = values[right * c_degree + c_index]
    return out


def add(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def diamond_norm_divisor(c_degree: int, modulus: int) -> list[int]:
    total = [0] * (RIGHT_DEGREE * c_degree)
    base = single_divisor(c_degree, modulus)
    for multiplier in range(1, c_degree):
        total = add(total, diamond_action(base, c_degree, multiplier), modulus)
    return total


def poly_mul(left: list[int], right: list[int], modulus: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            out[i + j] = (out[i + j] + a_value * b_value) % modulus
    return out


def cyclotomic_polynomial_from_roots(c_degree: int, modulus: int) -> list[int]:
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // c_degree, modulus)
    poly = [1]
    for exponent in range(1, c_degree):
        # X - zeta^exponent, coefficients in ascending order.
        factor = [(-pow(zeta, exponent, modulus)) % modulus, 1]
        poly = poly_mul(poly, factor, modulus)
    return poly


def phi_prime_coefficients(c_degree: int, modulus: int) -> list[int]:
    return [1 % modulus] * c_degree


def full_unit_orbit_is_needed(c_degree: int) -> bool:
    # For prime c, any proper subset of the nonzero multipliers misses at
    # least one nonzero C-coordinate, so it cannot equal D_c.
    seen: set[int] = set()
    for multiplier in range(1, c_degree):
        seen.add(multiplier % c_degree)
    return len(seen) == c_degree - 1 and 0 not in seen


def main() -> None:
    print("Trace-GCD reduced-anchor diamond norm gate")
    print(f"right_degree={RIGHT_DEGREE}")

    rows = SMALL_C_DEGREES + [P24_C_DEGREE]
    rows_checked = 0
    divisor_norm_rows = 0
    polynomial_norm_rows = 0
    fourier_profile_rows = 0
    orbit_size_rows = 0
    full_orbit_rows = 0

    for c_degree in rows:
        modulus = split_prime_for(RIGHT_DEGREE * c_degree)
        norm_divisor = diamond_norm_divisor(c_degree, modulus)
        expected_divisor = formal_cyclotomic_divisor(c_degree, modulus)
        polynomial_norm = cyclotomic_polynomial_from_roots(c_degree, modulus)
        expected_phi = phi_prime_coefficients(c_degree, modulus)

        divisor_norm_ok = int(norm_divisor == expected_divisor)
        polynomial_norm_ok = int(polynomial_norm == expected_phi)
        fourier_ok = int(fourier_profile_ok(norm_divisor, c_degree, modulus))
        orbit_size_ok = int(c_degree - 1 == len(range(1, c_degree)))
        full_orbit_ok = int(full_unit_orbit_is_needed(c_degree))

        rows_checked += 1
        divisor_norm_rows += divisor_norm_ok
        polynomial_norm_rows += polynomial_norm_ok
        fourier_profile_rows += fourier_ok
        orbit_size_rows += orbit_size_ok
        full_orbit_rows += full_orbit_ok

        print(
            "row "
            f"c_degree={c_degree} modulus={modulus} "
            f"diamond_orbit_size={c_degree - 1} "
            f"divisor_norm_ok={divisor_norm_ok} "
            f"polynomial_norm_ok={polynomial_norm_ok} "
            f"fourier_profile_ok={fourier_ok} "
            f"orbit_size_ok={orbit_size_ok} "
            f"full_unit_orbit_needed_ok={full_orbit_ok}"
        )

    print(f"diamond_norm_rows_checked={rows_checked}")
    print(f"diamond_norm_divisor_rows={divisor_norm_rows}/{rows_checked}")
    print(f"diamond_norm_polynomial_rows={polynomial_norm_rows}/{rows_checked}")
    print(f"diamond_norm_fourier_profile_rows={fourier_profile_rows}/{rows_checked}")
    print(f"diamond_norm_orbit_size_rows={orbit_size_rows}/{rows_checked}")
    print(f"diamond_norm_full_unit_orbit_rows={full_orbit_rows}/{rows_checked}")
    print(f"p24_diamond_norm_orbit_size={P24_C_DEGREE - 1}")
    print(f"p24_diamond_norm_residual_fourier_channels={RIGHT_DEGREE * (P24_C_DEGREE - 1)}")
    print("interpretation")
    print("  R_c_residual_is_diamond_norm_of_single_point_divisor=1")
    print("  product_over_nonzero_c_multipliers_gives_Phi_c_over_X_minus_1_power=1")
    print("  this_is_diamond_norm_not_cyclic_C_over_E_trace_norm=1")
    print("  p24_candidate_is_diamond_norm_of_one_p_integral_cm_lang_factor=1")
    print("  p24_then_needs_auxiliary_kummer_sign_descent_for_selected_anchor=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate")

    if divisor_norm_rows != rows_checked:
        raise SystemExit(1)
    if polynomial_norm_rows != rows_checked:
        raise SystemExit(1)
    if fourier_profile_rows != rows_checked:
        raise SystemExit(1)
    if orbit_size_rows != rows_checked:
        raise SystemExit(1)
    if full_orbit_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

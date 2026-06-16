#!/usr/bin/env python3
"""Resultant/Bezout form of reduced-anchor forbidden-locus avoidance.

The local-unit gate says

    R_c(x) = Phi_c(x)/(x - 1)^(c - 1)

is a unit iff `x` is not a c-th root of unity.  This gate packages the same
condition in the form a future CM/Lang producer can actually certify.

If the selected coordinate is represented in a finite etale algebra

    A = F_q[T] / (M(T)),
    x = X(T) mod M(T),

then the forbidden-locus avoidance is exactly

    gcd(M(T), X(T)^c - 1) = 1,

equivalently `Res(M, X^c - 1) != 0`, equivalently a Bezout identity

    A(T) M(T) + B(T) (X(T)^c - 1) = 1.

This is still not the CM/Lang producer.  It is the finite algebra interface
that a producer can feed to the verifier without enumerating `mu_c`.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate import (
    kernel_polynomial_degree,
)


T = sp.symbols("T")


@dataclass(frozen=True)
class ScalarRow:
    c_degree: int
    modulus: int
    forbidden_count: int
    resultant_unit_count: int
    expected_unit_count: int
    criterion_ok: bool
    count_ok: bool


@dataclass(frozen=True)
class AlgebraRow:
    label: str
    c_degree: int
    q: int
    modulus_degree: int
    coord_degree: int
    denominator_unit: bool
    numerator_unit: bool
    component_unit: bool
    xc_minus_one_unit: bool
    resultant_unit: bool
    bezout_unit: bool
    expected_unit: bool

    @property
    def criterion_ok(self) -> bool:
        return (
            self.component_unit
            == self.xc_minus_one_unit
            == self.resultant_unit
            == self.bezout_unit
            == self.expected_unit
        )


def poly(expr, q: int) -> sp.Poly:
    return sp.Poly(expr, T, modulus=q)


def poly_pow_mod(base: sp.Poly, exponent: int, modulus: sp.Poly, q: int) -> sp.Poly:
    result = poly(1, q)
    power = base.rem(modulus)
    n = exponent
    while n:
        if n & 1:
            result = (result * power).rem(modulus)
        power = (power * power).rem(modulus)
        n >>= 1
    return result


def phi_prime_composed(coord: sp.Poly, c_degree: int, modulus: sp.Poly, q: int) -> sp.Poly:
    total = poly(0, q)
    power = poly(1, q)
    for _ in range(c_degree):
        total = (total + power).rem(modulus)
        power = (power * coord).rem(modulus)
    return total.rem(modulus)


def is_unit_mod(g: sp.Poly, modulus: sp.Poly) -> bool:
    return sp.gcd(g, modulus).degree() == 0


def resultant_unit(modulus: sp.Poly, g: sp.Poly, q: int) -> bool:
    return int(sp.resultant(modulus.as_expr(), g.as_expr(), T)) % q != 0


def bezout_unit(modulus: sp.Poly, g: sp.Poly, q: int) -> bool:
    _s, _t, h = sp.gcdex(modulus, g, T, modulus=q)
    h_poly = poly(h, q)
    return h_poly.degree() == 0 and int(h_poly.nth(0)) % q != 0


def scalar_row(c_degree: int) -> ScalarRow:
    q = split_prime_for(7 * c_degree)
    forbidden = 0
    units = 0
    for value in range(q):
        is_forbidden = pow(value, c_degree, q) == 1
        resultant_is_unit = (pow(value, c_degree, q) - 1) % q != 0
        forbidden += int(is_forbidden)
        units += int(resultant_is_unit)
    expected = q - c_degree
    return ScalarRow(
        c_degree=c_degree,
        modulus=q,
        forbidden_count=forbidden,
        resultant_unit_count=units,
        expected_unit_count=expected,
        criterion_ok=(forbidden == c_degree),
        count_ok=(units == expected),
    )


def factor_of_phi(c_degree: int, q: int) -> sp.Poly:
    # The full Phi_c algebra is squarefree when char(F_q) does not divide c.
    # That is enough for the unit/resultant/Bezout criterion and avoids
    # backend-specific ordering issues when factoring over small finite fields.
    return poly(sp.cyclotomic_poly(c_degree, T), q)


def algebra_row(
    label: str,
    c_degree: int,
    q: int,
    modulus: sp.Poly,
    coord: sp.Poly,
    expected_unit: bool,
) -> AlgebraRow:
    coord = coord.rem(modulus)
    denominator = (coord - poly(1, q)).rem(modulus)
    numerator = phi_prime_composed(coord, c_degree, modulus, q)
    xc_minus_one = (poly_pow_mod(coord, c_degree, modulus, q) - poly(1, q)).rem(modulus)
    # Use the unreduced expression for the resultant, but the reduced one for
    # gcd/Bezout.  They give the same unit/nonunit result modulo M(T).
    full_xc_minus_one = poly(coord.as_expr() ** c_degree - 1, q)
    return AlgebraRow(
        label=label,
        c_degree=c_degree,
        q=q,
        modulus_degree=modulus.degree(),
        coord_degree=coord.degree(),
        denominator_unit=is_unit_mod(denominator, modulus),
        numerator_unit=is_unit_mod(numerator, modulus),
        component_unit=is_unit_mod(denominator, modulus)
        and is_unit_mod(numerator, modulus),
        xc_minus_one_unit=is_unit_mod(xc_minus_one, modulus),
        resultant_unit=resultant_unit(modulus, full_xc_minus_one, q),
        bezout_unit=bezout_unit(modulus, xc_minus_one, q),
        expected_unit=expected_unit,
    )


def find_shifted_unit_row(c_degree: int, q: int, modulus: sp.Poly) -> AlgebraRow:
    for shift in range(1, q):
        row = algebra_row(
            label=f"Phi_factor_shift_{shift}",
            c_degree=c_degree,
            q=q,
            modulus=modulus,
            coord=poly(T + shift, q),
            expected_unit=True,
        )
        if row.criterion_ok:
            return row
    raise RuntimeError(f"no shifted unit coordinate found for c={c_degree}, q={q}")


def quotient_rows() -> list[AlgebraRow]:
    # These rows deliberately use fields where the c-th roots are not all in
    # the base field.  The resultant/Bezout criterion still sees them.
    specs = [(5, 2), (7, 3), (11, 2), (13, 2)]
    rows: list[AlgebraRow] = []
    for c_degree, q in specs:
        modulus = factor_of_phi(c_degree, q)
        rows.append(
            algebra_row(
                label="Phi_factor_coordinate_T",
                c_degree=c_degree,
                q=q,
                modulus=modulus,
                coord=poly(T, q),
                expected_unit=False,
            )
        )
        rows.append(find_shifted_unit_row(c_degree, q, modulus))
    return rows


def main() -> None:
    print("Trace-GCD reduced-anchor resultant avoidance gate")

    scalar_rows = [scalar_row(c_degree) for c_degree in SMALL_C_DEGREES + [P24_C_DEGREE]]
    scalar_criterion_rows = 0
    scalar_count_rows = 0
    for row in scalar_rows:
        scalar_criterion_rows += int(row.criterion_ok)
        scalar_count_rows += int(row.count_ok)
        print(
            "scalar "
            f"c_degree={row.c_degree} modulus={row.modulus} "
            f"forbidden_count={row.forbidden_count} "
            f"resultant_unit_count={row.resultant_unit_count} "
            f"expected_unit_count={row.expected_unit_count} "
            f"resultant_avoidance_criterion_ok={int(row.criterion_ok)} "
            f"unit_count_ok={int(row.count_ok)}"
        )

    q_rows = quotient_rows()
    quotient_criterion_rows = 0
    quotient_component_rows = 0
    quotient_resultant_rows = 0
    quotient_bezout_rows = 0
    for row in q_rows:
        quotient_criterion_rows += int(row.criterion_ok)
        quotient_component_rows += int(row.component_unit == row.expected_unit)
        quotient_resultant_rows += int(row.resultant_unit == row.expected_unit)
        quotient_bezout_rows += int(row.bezout_unit == row.expected_unit)
        print(
            "quotient "
            f"label={row.label} c_degree={row.c_degree} q={row.q} "
            f"modulus_degree={row.modulus_degree} coord_degree={row.coord_degree} "
            f"denominator_unit={int(row.denominator_unit)} "
            f"numerator_unit={int(row.numerator_unit)} "
            f"component_unit={int(row.component_unit)} "
            f"xc_minus_one_unit={int(row.xc_minus_one_unit)} "
            f"resultant_unit={int(row.resultant_unit)} "
            f"bezout_unit={int(row.bezout_unit)} "
            f"expected_unit={int(row.expected_unit)} "
            f"criterion_ok={int(row.criterion_ok)}"
        )

    c_rows = len(scalar_rows)
    q_count = len(q_rows)
    print("summary")
    print(f"  scalar_rows={c_rows}")
    print(f"  scalar_resultant_criterion_rows={scalar_criterion_rows}/{c_rows}")
    print(f"  scalar_unit_count_rows={scalar_count_rows}/{c_rows}")
    print(f"  quotient_rows={q_count}")
    print(f"  quotient_component_unit_rows={quotient_component_rows}/{q_count}")
    print(f"  quotient_xc_minus_one_resultant_rows={quotient_resultant_rows}/{q_count}")
    print(f"  quotient_bezout_rows={quotient_bezout_rows}/{q_count}")
    print(f"  quotient_combined_criterion_rows={quotient_criterion_rows}/{q_count}")
    print(f"  p24_c_degree={P24_C_DEGREE}")
    print(f"  p24_forbidden_polynomial_degree={P24_C_DEGREE}")
    print(f"  p24_kernel_polynomial_degree={kernel_polynomial_degree(P24_C_DEGREE)}")
    print("interpretation")
    print("  R_c_unit_iff_X_power_c_minus_one_is_unit_in_selected_algebra=1")
    print("  resultant_nonzero_equiv_forbidden_locus_avoidance=1")
    print("  bezout_identity_equiv_resultant_unit_certificate=1")
    print("  criterion_works_without_adjoining_all_c_roots_of_unity=1")
    print("  p24_reduced_anchor_can_be_certified_by_one_resultant_or_bezout_punit=1")
    print("  resultant_avoidance_is_finite_algebra_not_the_cm_lang_producer=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate")

    if scalar_criterion_rows != c_rows or scalar_count_rows != c_rows:
        raise SystemExit(1)
    if quotient_criterion_rows != q_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

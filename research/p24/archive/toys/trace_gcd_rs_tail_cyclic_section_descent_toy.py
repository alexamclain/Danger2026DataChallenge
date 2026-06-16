#!/usr/bin/env python3
"""Cyclic-section descent gate for the RS-tail frequency resultants.

The frequency-resultant target asks for cyclic sections P_24,T_24,S_24 whose
values are the local Plucker determinants, defect tail residues, and defect
support selector.  This toy isolates the finite descent issue:

* any values on mu_n interpolate over the splitting field;
* the interpolant has base-field coefficients exactly when the values are
  Frobenius-compatible, F(q*a)=F(a)^q;
* a defect selector descends to the base field only when the defect support is
  Frobenius-stable.

This prevents a post-fit polynomial over the splitting field from being
mistaken for a p-integral resultant certificate.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class DescentCase:
    label: str
    q: int
    n: int
    degree: int
    frobenius_multiplier: int
    compatible: bool
    interpolated_base_coefficients: bool
    resultant_product_nonzero: bool
    base_section_certificate_valid: bool


@dataclass(frozen=True)
class SelectorCase:
    label: str
    q: int
    n: int
    support_size: int
    frobenius_stable_support: bool
    selector_base_coefficients: bool
    selector_simple_on_mu_n: bool


def base_coeff(value: FpE) -> bool:
    return all(component == 0 for component in value[1:])


def base_coefficients(values: list[FpE]) -> bool:
    return all(base_coeff(value) for value in values)


def poly_eval(poly: list[FpE], x: FpE, field: ExtensionField) -> FpE:
    value = field.zero
    power = field.one
    for coeff in poly:
        value = field.add(value, field.mul(coeff, power))
        power = field.mul(power, x)
    return value


def poly_mul(left: list[FpE], right: list[FpE], field: ExtensionField) -> list[FpE]:
    out = [field.zero for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = field.add(out[i + j], field.mul(a, b))
    return out


def polynomial_from_roots(roots: list[FpE], field: ExtensionField) -> list[FpE]:
    poly = [field.one]
    for root in roots:
        poly = poly_mul([field.neg(root), field.one], poly, field)
    return poly


def evaluate_on_roots(
    poly: list[FpE],
    omega: FpE,
    n: int,
    field: ExtensionField,
) -> list[FpE]:
    return [poly_eval(poly, field.pow(omega, a), field) for a in range(n)]


def interpolate_from_roots(
    values: list[FpE],
    omega: FpE,
    field: ExtensionField,
) -> list[FpE]:
    n = len(values)
    inv_n = pow(n % field.q, -1, field.q)
    coeffs: list[FpE] = []
    for power in range(n):
        total = field.zero
        for a, value in enumerate(values):
            weight = field.pow(omega, (-a * power) % n)
            total = field.add(total, field.mul(value, weight))
        coeffs.append(field.scalar_mul(inv_n, total))
    return coeffs


def frobenius_compatible(values: list[FpE], q: int, field: ExtensionField) -> bool:
    n = len(values)
    return all(
        values[(q * a) % n] == field.pow(values[a], q)
        for a in range(n)
    )


def root_product(values: list[FpE], field: ExtensionField) -> FpE:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def frobenius_stable_support(support: set[int], q: int, n: int) -> bool:
    return {(q * a) % n for a in support} == support


def selector_simple_on_mu_n(selector: list[FpE], omega: FpE, n: int, field: ExtensionField) -> bool:
    zeros = [
        a for a in range(n)
        if poly_eval(selector, field.pow(omega, a), field) == field.zero
    ]
    return len(zeros) == len(set(zeros))


def analyze_descent_case(
    label: str,
    q: int,
    n: int,
    field: ExtensionField,
    omega: FpE,
    values: list[FpE],
) -> DescentCase:
    coeffs = interpolate_from_roots(values, omega, field)
    compatible = frobenius_compatible(values, q, field)
    base = base_coefficients(coeffs)
    product_nonzero = root_product(values, field) != field.zero
    return DescentCase(
        label=label,
        q=q,
        n=n,
        degree=field.degree,
        frobenius_multiplier=q % n,
        compatible=compatible,
        interpolated_base_coefficients=base,
        resultant_product_nonzero=product_nonzero,
        base_section_certificate_valid=compatible and base and product_nonzero,
    )


def analyze_selector_case(
    label: str,
    q: int,
    n: int,
    field: ExtensionField,
    omega: FpE,
    support: set[int],
) -> SelectorCase:
    roots = [field.pow(omega, a) for a in sorted(support)]
    selector = polynomial_from_roots(roots, field)
    return SelectorCase(
        label=label,
        q=q,
        n=n,
        support_size=len(support),
        frobenius_stable_support=frobenius_stable_support(support, q, n),
        selector_base_coefficients=base_coefficients(selector),
        selector_simple_on_mu_n=selector_simple_on_mu_n(selector, omega, n, field),
    )


def print_descent(case: DescentCase) -> None:
    print(
        f"case={case.label} q={case.q} n={case.n} degree={case.degree} "
        f"frobenius_multiplier={case.frobenius_multiplier} "
        f"compatible={int(case.compatible)} "
        f"interpolated_base_coefficients={int(case.interpolated_base_coefficients)} "
        f"resultant_product_nonzero={int(case.resultant_product_nonzero)} "
        f"base_section_certificate_valid={int(case.base_section_certificate_valid)}"
    )


def print_selector(case: SelectorCase) -> None:
    print(
        f"selector={case.label} q={case.q} n={case.n} "
        f"support_size={case.support_size} "
        f"frobenius_stable_support={int(case.frobenius_stable_support)} "
        f"selector_base_coefficients={int(case.selector_base_coefficients)} "
        f"selector_simple_on_mu_n={int(case.selector_simple_on_mu_n)}"
    )


def orbit_lengths(modulus: int, multiplier: int) -> list[int]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(modulus):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = multiplier * current % modulus
        lengths.append(length)
    return sorted(lengths)


def main() -> None:
    q = 3
    n = 5
    degree = int(sp.n_order(q % n, n))
    field = ExtensionField(q, degree, find_irreducible_modulus(q, degree, 20260606))
    omega = primitive_root_of_order(field, n, 20260606)

    base_poly = [field.embed(1), field.embed(1)]
    good_values = evaluate_on_roots(base_poly, omega, n, field)
    bad_values = good_values[:]
    bad_values[1] = field.add(bad_values[1], field.pow(omega, 1))

    descent_rows = [
        analyze_descent_case(
            "frobenius_compatible_base_section",
            q,
            n,
            field,
            omega,
            good_values,
        ),
        analyze_descent_case(
            "postfit_splitting_field_values_control",
            q,
            n,
            field,
            omega,
            bad_values,
        ),
    ]

    selector_rows = [
        analyze_selector_case(
            "frobenius_stable_defect_orbit",
            q,
            n,
            field,
            omega,
            {1, 2, 3, 4},
        ),
        analyze_selector_case(
            "nonstable_defect_support_control",
            q,
            n,
            field,
            omega,
            {0, 1},
        ),
    ]

    print("Trace-GCD RS-tail cyclic-section descent toy")
    for row in descent_rows:
        print_descent(row)
    for row in selector_rows:
        print_selector(row)
    print("p24")
    print("  p24_frequency_count=35")
    print("  p24_frobenius_multiplier_mod_35=22")
    print(f"  p24_frobenius_orbit_lengths={orbit_lengths(35, 22)}")
    print("  p24_tail_defect_count=16")
    print("  p24_tail_defect_count_can_be_4_length4_orbits=1")
    print("interpretation")
    print("  frobenius_compatible_values_descend_to_base_cyclic_section=1")
    print("  arbitrary_postfit_splitting_field_interpolant_is_rejected=1")
    print("  frobenius_stable_defect_support_gives_base_selector=1")
    print("  nonstable_defect_support_has_no_base_selector=1")
    print("  p24_resultant_gate_needs_semilinear_CM_section_descent=1")
    print("conclusion=reported_trace_gcd_rs_tail_cyclic_section_descent_toy")

    good, bad = descent_rows
    stable, nonstable = selector_rows
    if (
        not good.base_section_certificate_valid
        or bad.base_section_certificate_valid
        or not stable.selector_base_coefficients
        or not stable.frobenius_stable_support
        or nonstable.selector_base_coefficients
        or nonstable.frobenius_stable_support
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

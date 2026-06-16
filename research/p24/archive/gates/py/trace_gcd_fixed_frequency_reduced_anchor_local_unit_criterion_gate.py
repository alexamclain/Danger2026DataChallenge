#!/usr/bin/env python3
"""Local-unit criterion for the reduced-anchor residual.

The previous reduced-anchor gates identify the residual divisor as

    R_c(X) = Phi_c(X) / (X - 1)^(c - 1)

or, in elliptic subgroup language, as the kernel polynomial

    K_H(x) = prod_{Q in (H \ {O})/{+-1}} (x - x(Q)).

This gate records the exact local-unit condition after reduction modulo a
prime away from `c`.

Cyclotomic form:
    R_c(x) is a unit iff x is not a c-th root of unity.

Elliptic kernel form:
    K_H(T) is a unit iff T is neither O nor a nonzero point of H.

The p24 producer theorem can therefore be sharpened from "construct the
selected CM/Lang factor" to "construct it p-integrally and prove its reduction
avoids the forbidden anchor/subgroup locus."
"""

from __future__ import annotations

from dataclasses import dataclass

from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import (
    primitive_root,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    split_prime_for,
)
from trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate import (
    KernelExample,
    Point,
    find_example,
    kernel_polynomial_degree,
    mul,
    points,
)


@dataclass(frozen=True)
class CyclotomicRow:
    c_degree: int
    modulus: int
    forbidden_count: int
    unit_count: int
    expected_unit_count: int
    product_identity_ok: bool
    criterion_ok: bool


@dataclass(frozen=True)
class KernelUnitRow:
    c_degree: int
    q: int
    curve_order: int
    subgroup_size: int
    zero_count: int
    pole_count: int
    unit_count: int
    expected_unit_count: int
    criterion_ok: bool


def phi_prime_value(x: int, c_degree: int, modulus: int) -> int:
    value = 0
    power = 1
    for _ in range(c_degree):
        value = (value + power) % modulus
        power = power * x % modulus
    return value


def diamond_product_value(x: int, c_degree: int, modulus: int) -> int | None:
    denominator = (x - 1) % modulus
    if denominator == 0:
        return None
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // c_degree, modulus)
    total = 1
    den_inv = pow(denominator, -1, modulus)
    for exponent in range(1, c_degree):
        total = total * ((x - pow(zeta, exponent, modulus)) % modulus) % modulus
        total = total * den_inv % modulus
    return total


def rational_R_value(x: int, c_degree: int, modulus: int) -> int | None:
    denominator = pow((x - 1) % modulus, c_degree - 1, modulus)
    if denominator == 0:
        return None
    return phi_prime_value(x, c_degree, modulus) * pow(denominator, -1, modulus) % modulus


def cyclotomic_row(c_degree: int) -> CyclotomicRow:
    modulus = split_prime_for(7 * c_degree)
    forbidden = 0
    units = 0
    product_identity_ok = True
    criterion_ok = True
    for x in range(modulus):
        r_value = rational_R_value(x, c_degree, modulus)
        product_value = diamond_product_value(x, c_degree, modulus)
        is_forbidden = pow(x, c_degree, modulus) == 1
        is_unit = r_value is not None and r_value != 0
        forbidden += int(is_forbidden)
        units += int(is_unit)
        if r_value != product_value:
            product_identity_ok = False
        if is_unit == is_forbidden:
            criterion_ok = False
    return CyclotomicRow(
        c_degree=c_degree,
        modulus=modulus,
        forbidden_count=forbidden,
        unit_count=units,
        expected_unit_count=modulus - c_degree,
        product_identity_ok=product_identity_ok,
        criterion_ok=criterion_ok,
    )


def eval_kernel_at_x(example: KernelExample, x_value: int) -> int:
    value = 1
    for root in example.x_roots:
        value = value * ((x_value - root) % example.curve.q) % example.curve.q
    return value


def kernel_value(example: KernelExample, point: Point) -> int | None:
    if point is None:
        return None
    return eval_kernel_at_x(example, point[0])


def kernel_unit_row(c_degree: int) -> KernelUnitRow:
    example = find_example(c_degree)
    pts = points(example.curve)
    subgroup = {mul(example.curve, k, example.generator) for k in range(c_degree)}
    zeros = 0
    poles = 0
    units = 0
    criterion_ok = True
    for point in pts:
        value = kernel_value(example, point)
        is_forbidden = point in subgroup
        is_pole = point is None
        is_zero = value == 0
        is_unit = value is not None and value != 0
        zeros += int(is_zero)
        poles += int(is_pole)
        units += int(is_unit)
        if is_unit == is_forbidden:
            criterion_ok = False
    return KernelUnitRow(
        c_degree=c_degree,
        q=example.curve.q,
        curve_order=len(pts),
        subgroup_size=len(subgroup),
        zero_count=zeros,
        pole_count=poles,
        unit_count=units,
        expected_unit_count=len(pts) - c_degree,
        criterion_ok=criterion_ok,
    )


def main() -> None:
    print("Trace-GCD reduced-anchor local-unit criterion gate")

    cyclotomic_rows = [cyclotomic_row(c_degree) for c_degree in SMALL_C_DEGREES + [P24_C_DEGREE]]
    cyclotomic_product_rows = 0
    cyclotomic_criterion_rows = 0
    cyclotomic_unit_count_rows = 0
    for row in cyclotomic_rows:
        product_ok = int(row.product_identity_ok)
        criterion_ok = int(row.criterion_ok)
        count_ok = int(row.unit_count == row.expected_unit_count)
        cyclotomic_product_rows += product_ok
        cyclotomic_criterion_rows += criterion_ok
        cyclotomic_unit_count_rows += count_ok
        print(
            "cyclotomic "
            f"c_degree={row.c_degree} modulus={row.modulus} "
            f"forbidden_mu_c_count={row.forbidden_count} "
            f"unit_count={row.unit_count} "
            f"expected_unit_count={row.expected_unit_count} "
            f"diamond_product_identity_ok={product_ok} "
            f"local_unit_criterion_ok={criterion_ok} "
            f"unit_count_ok={count_ok}"
        )

    kernel_rows = [kernel_unit_row(c_degree) for c_degree in (5, 7, 11, 13)]
    kernel_criterion_rows = 0
    kernel_unit_count_rows = 0
    kernel_zero_pole_rows = 0
    for row in kernel_rows:
        criterion_ok = int(row.criterion_ok)
        count_ok = int(row.unit_count == row.expected_unit_count)
        zero_pole_ok = int(row.zero_count == row.c_degree - 1 and row.pole_count == 1)
        kernel_criterion_rows += criterion_ok
        kernel_unit_count_rows += count_ok
        kernel_zero_pole_rows += zero_pole_ok
        print(
            "kernel "
            f"c_degree={row.c_degree} q={row.q} curve_order={row.curve_order} "
            f"subgroup_size={row.subgroup_size} "
            f"kernel_degree={kernel_polynomial_degree(row.c_degree)} "
            f"zero_count={row.zero_count} pole_count={row.pole_count} "
            f"unit_count={row.unit_count} "
            f"expected_unit_count={row.expected_unit_count} "
            f"local_unit_criterion_ok={criterion_ok} "
            f"unit_count_ok={count_ok} "
            f"zero_pole_count_ok={zero_pole_ok}"
        )

    c_rows = len(cyclotomic_rows)
    k_rows = len(kernel_rows)
    print("summary")
    print(f"  cyclotomic_rows={c_rows}")
    print(f"  cyclotomic_diamond_product_identity_rows={cyclotomic_product_rows}/{c_rows}")
    print(f"  cyclotomic_local_unit_criterion_rows={cyclotomic_criterion_rows}/{c_rows}")
    print(f"  cyclotomic_unit_count_rows={cyclotomic_unit_count_rows}/{c_rows}")
    print(f"  kernel_rows={k_rows}")
    print(f"  kernel_local_unit_criterion_rows={kernel_criterion_rows}/{k_rows}")
    print(f"  kernel_unit_count_rows={kernel_unit_count_rows}/{k_rows}")
    print(f"  kernel_zero_pole_count_rows={kernel_zero_pole_rows}/{k_rows}")
    print(f"  p24_forbidden_cyclotomic_anchor_count={P24_C_DEGREE}")
    print("interpretation")
    print("  R_c_specialization_is_unit_iff_coordinate_avoids_mu_c=1")
    print("  K_H_specialization_is_unit_iff_point_avoids_H_and_O=1")
    print("  p24_producer_must_prove_selected_cm_lang_coordinate_avoids_forbidden_anchor_locus=1")
    print("  local_unit_criterion_is_finite_algebra_not_the_cm_lang_producer=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate")

    if cyclotomic_product_rows != c_rows:
        raise SystemExit(1)
    if cyclotomic_criterion_rows != c_rows:
        raise SystemExit(1)
    if cyclotomic_unit_count_rows != c_rows:
        raise SystemExit(1)
    if kernel_criterion_rows != k_rows:
        raise SystemExit(1)
    if kernel_unit_count_rows != k_rows:
        raise SystemExit(1)
    if kernel_zero_pole_rows != k_rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

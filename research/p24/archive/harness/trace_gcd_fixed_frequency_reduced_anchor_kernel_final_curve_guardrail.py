#!/usr/bin/env python3
"""Guardrail: the p24 179-kernel is not a final-curve F_p isogeny object.

The reduced-anchor residual has a formal `c=179` subgroup/kernel-polynomial
shape.  It is tempting to turn that into a computation on the final
Montgomery/CM curve over F_p: enumerate 179-subgroups, compute Vélu kernel
polynomials, and try the two anchor signs.

For the selected p24 trace this is the wrong search domain.  The final curve
order is

    #E(F_p) = p + 1 - t = 2^41 * 454747350887,

so 179 does not divide #E(F_p).  More strongly, the Frobenius discriminant is
a nonsquare modulo 179, so 179 is Atkin for the final curve: there is no
F_p-rational cyclic 179-subgroup and no F_p-rational 179-isogeny/kernel
polynomial.  The 179-kernel language must therefore be read as an auxiliary
CM/Lang/cyclotomic quotient object, not as a final-curve Vélu denominator to
enumerate over F_p.
"""

from __future__ import annotations

from dataclasses import dataclass


P24 = 10**24 + 7
TRACE = -1178414874616
C_DEGREE = 179
LEFT = 157
RIGHT = 211


@dataclass(frozen=True)
class PrimeTorsionRow:
    ell: int
    order_mod_ell: int
    frobenius_discriminant: int
    legendre_discriminant: int
    frobenius_roots: tuple[int, ...]
    divides_group_order: bool
    rational_isogeny_available: bool


def legendre(value: int, ell: int) -> int:
    residue = value % ell
    if residue == 0:
        return 0
    result = pow(residue, (ell - 1) // 2, ell)
    return -1 if result == ell - 1 else result


def multiplicative_order(value: int, modulus: int) -> int:
    x = value % modulus
    if x == 0:
        raise ValueError("zero has no multiplicative order")
    cur = 1
    acc = x
    while acc != 1:
        acc = acc * x % modulus
        cur += 1
    return cur


def frobenius_roots_mod_ell(ell: int) -> tuple[int, ...]:
    roots = [
        x
        for x in range(ell)
        if (x * x - TRACE * x + P24) % ell == 0
    ]
    return tuple(roots)


def row(ell: int) -> PrimeTorsionRow:
    group_order = P24 + 1 - TRACE
    disc = (TRACE * TRACE - 4 * P24) % ell
    roots = frobenius_roots_mod_ell(ell)
    leg = legendre(disc, ell)
    return PrimeTorsionRow(
        ell=ell,
        order_mod_ell=multiplicative_order(P24, ell),
        frobenius_discriminant=disc,
        legendre_discriminant=leg,
        frobenius_roots=roots,
        divides_group_order=(group_order % ell == 0),
        rational_isogeny_available=(leg in (0, 1)),
    )


def main() -> None:
    group_order = P24 + 1 - TRACE
    odd_part = group_order >> ((group_order & -group_order).bit_length() - 1)
    rows = [row(ell) for ell in (LEFT, C_DEGREE, RIGHT)]

    print("Trace-GCD reduced-anchor kernel final-curve guardrail")
    print(f"p={P24}")
    print(f"selected_trace={TRACE}")
    print(f"selected_group_order={group_order}")
    print(f"selected_group_order_odd_part={odd_part}")
    print()
    for item in rows:
        print(
            "row "
            f"ell={item.ell} "
            f"ord_ell_p={item.order_mod_ell} "
            f"frobenius_discriminant_mod_ell={item.frobenius_discriminant} "
            f"legendre_discriminant={item.legendre_discriminant} "
            f"frobenius_roots={list(item.frobenius_roots)} "
            f"divides_group_order={int(item.divides_group_order)} "
            f"rational_isogeny_available={int(item.rational_isogeny_available)}"
        )

    p24_c = next(item for item in rows if item.ell == C_DEGREE)
    print()
    print(f"p24_c_degree={C_DEGREE}")
    print(f"p24_c_divides_selected_group_order={int(p24_c.divides_group_order)}")
    print(f"p24_c_frobenius_discriminant_legendre={p24_c.legendre_discriminant}")
    print(f"p24_c_frobenius_roots_mod_c={list(p24_c.frobenius_roots)}")
    print(f"p24_c_final_curve_rational_isogeny_available={int(p24_c.rational_isogeny_available)}")
    print(f"p24_mu_c_field_degree_over_Fp={p24_c.order_mod_ell}")
    print("interpretation")
    print("  p24_179_kernel_is_not_rational_torsion_on_final_curve=1")
    print("  p24_179_kernel_is_not_an_Fp_rational_Velu_isogeny=1")
    print("  do_not_enumerate_final_curve_179_subgroups_as_the_compressed_search=1")
    print("  kernel_polynomial_target_must_live_in_auxiliary_cm_lang_or_cyclotomic_layer=1")
    print("conclusion=reported_trace_gcd_reduced_anchor_kernel_final_curve_guardrail")

    if p24_c.divides_group_order:
        raise SystemExit(1)
    if p24_c.rational_isogeny_available:
        raise SystemExit(1)
    if p24_c.legendre_discriminant != -1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

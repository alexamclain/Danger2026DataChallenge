#!/usr/bin/env python3
"""Frobenius/value contract for the p25 conductor-39 period norm.

The period-norm conductor gate reduces Norm_156(Y_507) to an inflated
conductor-39 quadratic character.  This gate records the finite-field arithmetic
that any value-side explanation has to respect: p does not contain primitive
39th roots in F_p, and the associated quadratic discriminant -39 is inert at p.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_period_norm_conductor_gate import (
    CONDUCTOR,
    profile_yang_y507_period_norm_conductor,
)


P25 = 10**25 + 13
DISCRIMINANT = -39


@dataclass(frozen=True)
class CyclotomicExtensionRow:
    modulus: int
    p_mod_modulus: int
    multiplicative_order: int
    first_root_field_degree: int
    ok: bool


@dataclass(frozen=True)
class PowerResidueRow:
    degree: int
    p_power_mod_39: int
    gcd_39_p_power_minus_1: int
    gcd_39_p_power_plus_1: int
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39FrobeniusContract:
    p: int
    p_mod_39: int
    conductor: int
    discriminant: int
    p_mod_4: int
    discriminant_mod_4: int
    cyclotomic_rows: tuple[CyclotomicExtensionRow, ...]
    power_rows: tuple[PowerResidueRow, ...]
    p_order_mod_39: int
    p_cubed_is_minus_one_mod_39: bool
    primitive_39_roots_first_in_degree_6: bool
    primitive_13_roots_first_in_degree_6: bool
    primitive_3_roots_first_in_degree_2: bool
    legendre_discriminant_mod_p: int
    discriminant_is_nonsquare_mod_p: bool
    conductor_gate_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def multiplicative_order_mod(base: int, modulus: int) -> int:
    if gcd(base, modulus) != 1:
        raise ValueError("base must be a unit modulo modulus")
    value = 1
    for exponent in range(1, modulus + 1):
        value = (value * base) % modulus
        if value == 1:
            return exponent
    raise AssertionError("multiplicative order search exceeded modulus")


def cyclotomic_row(modulus: int, expected_order: int) -> CyclotomicExtensionRow:
    p_mod = P25 % modulus
    order = multiplicative_order_mod(p_mod, modulus)
    return CyclotomicExtensionRow(
        modulus=modulus,
        p_mod_modulus=p_mod,
        multiplicative_order=order,
        first_root_field_degree=order,
        ok=order == expected_order,
    )


def power_row(degree: int, expected_minus: int, expected_plus: int) -> PowerResidueRow:
    value = pow(P25, degree, CONDUCTOR)
    minus_gcd = gcd(CONDUCTOR, (value - 1) % CONDUCTOR)
    plus_gcd = gcd(CONDUCTOR, (value + 1) % CONDUCTOR)
    return PowerResidueRow(
        degree=degree,
        p_power_mod_39=value,
        gcd_39_p_power_minus_1=minus_gcd,
        gcd_39_p_power_plus_1=plus_gcd,
        ok=minus_gcd == expected_minus and plus_gcd == expected_plus,
    )


def legendre_symbol(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    if residue == prime - 1:
        return -1
    return residue


def profile_yang_y507_conductor39_frobenius_contract() -> YangY507Conductor39FrobeniusContract:
    conductor = profile_yang_y507_period_norm_conductor()
    cyclotomic_rows = (
        cyclotomic_row(3, 2),
        cyclotomic_row(13, 6),
        cyclotomic_row(39, 6),
    )
    expected_minus = {1: 1, 2: 3, 3: 1, 4: 3, 5: 1, 6: 39}
    expected_plus = {1: 3, 2: 1, 3: 39, 4: 1, 5: 3, 6: 1}
    power_rows = tuple(
        power_row(degree, expected_minus[degree], expected_plus[degree])
        for degree in range(1, 7)
    )
    legendre = legendre_symbol(DISCRIMINANT, P25)
    direct_closer = False
    row_ok = (
        conductor.row_ok
        and CONDUCTOR == 39
        and P25 % 39 == 23
        and P25 % 4 == 1
        and DISCRIMINANT % 4 == 1
        and all(row.ok for row in cyclotomic_rows)
        and all(row.ok for row in power_rows)
        and cyclotomic_rows == (
            CyclotomicExtensionRow(3, 2, 2, 2, True),
            CyclotomicExtensionRow(13, 10, 6, 6, True),
            CyclotomicExtensionRow(39, 23, 6, 6, True),
        )
        and power_rows[2].p_power_mod_39 == 38
        and power_rows[5].p_power_mod_39 == 1
        and legendre == -1
        and not direct_closer
    )
    return YangY507Conductor39FrobeniusContract(
        p=P25,
        p_mod_39=P25 % 39,
        conductor=CONDUCTOR,
        discriminant=DISCRIMINANT,
        p_mod_4=P25 % 4,
        discriminant_mod_4=DISCRIMINANT % 4,
        cyclotomic_rows=cyclotomic_rows,
        power_rows=power_rows,
        p_order_mod_39=multiplicative_order_mod(P25 % 39, 39),
        p_cubed_is_minus_one_mod_39=pow(P25, 3, 39) == 38,
        primitive_39_roots_first_in_degree_6=cyclotomic_rows[2].first_root_field_degree == 6,
        primitive_13_roots_first_in_degree_6=cyclotomic_rows[1].first_root_field_degree == 6,
        primitive_3_roots_first_in_degree_2=cyclotomic_rows[0].first_root_field_degree == 2,
        legendre_discriminant_mod_p=legendre,
        discriminant_is_nonsquare_mod_p=legendre == -1,
        conductor_gate_ok=conductor.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The conductor-39 character is the right value-side shadow, but "
            "primitive 39th roots first appear over F_{p^6}; sqrt(-39) is not "
            "in F_p."
        ),
        first_missing_clause=(
            "this Frobenius contract is a routing constraint, not a finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "accept conductor-39 value explanations only if they include the "
            "degree-6 cyclotomic orbit or a conjugate/norm descent back to F_p; "
            "reject direct F_p order-39-root or sqrt(-39) scalar shortcuts"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_frobenius_contract()
    print("p25 KSY-y Yang Y_507 conductor-39 Frobenius/value contract gate")
    print(f"p_mod_39={profile.p_mod_39}")
    print(f"conductor={profile.conductor}")
    print(f"discriminant={profile.discriminant}")
    print(f"p_mod_4={profile.p_mod_4}")
    print(f"discriminant_mod_4={profile.discriminant_mod_4}")
    print("cyclotomic_extensions")
    for row in profile.cyclotomic_rows:
        print(
            "  "
            f"modulus={row.modulus} p_mod={row.p_mod_modulus} "
            f"order={row.multiplicative_order} "
            f"first_root_field_degree={row.first_root_field_degree} "
            f"ok={int(row.ok)}"
        )
    print("power_residues")
    for row in profile.power_rows:
        print(
            "  "
            f"degree={row.degree} p_power_mod_39={row.p_power_mod_39} "
            f"gcd_39_p_power_minus_1={row.gcd_39_p_power_minus_1} "
            f"gcd_39_p_power_plus_1={row.gcd_39_p_power_plus_1} "
            f"ok={int(row.ok)}"
        )
    print("checks")
    print(f"  conductor_gate_ok={int(profile.conductor_gate_ok)}")
    print(f"  p_order_mod_39={profile.p_order_mod_39}")
    print(f"  p_cubed_is_minus_one_mod_39={int(profile.p_cubed_is_minus_one_mod_39)}")
    print(
        "  primitive_39_roots_first_in_degree_6="
        f"{int(profile.primitive_39_roots_first_in_degree_6)}"
    )
    print(
        "  primitive_13_roots_first_in_degree_6="
        f"{int(profile.primitive_13_roots_first_in_degree_6)}"
    )
    print(
        "  primitive_3_roots_first_in_degree_2="
        f"{int(profile.primitive_3_roots_first_in_degree_2)}"
    )
    print(f"  legendre_discriminant_mod_p={profile.legendre_discriminant_mod_p}")
    print(f"  discriminant_is_nonsquare_mod_p={int(profile.discriminant_is_nonsquare_mod_p)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  conductor39_value_route_needs_degree6_cyclotomic_or_norm_descent=1")
    print("  direct_Fp_order39_root_or_sqrt_minus39_shortcut_is_invalid=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_frobenius_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 Frobenius contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

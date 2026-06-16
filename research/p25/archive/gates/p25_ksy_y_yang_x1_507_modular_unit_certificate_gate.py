#!/usr/bin/env python3
"""Yang/Yu X_1(507) modular-unit certificate for the p25 six-cell packet.

The Yang orbit-distribution bridge shows that the raw 150-term K trace descends
to six quotient cells.  This gate checks the next source-native question:
whether the six-cell quotient itself is a valid one-dimensional product of
Yang's E_a functions on X_1(507).

It is.  The product

    U_507 = E_25 E_197 E_369 / (E_138 E_310 E_482)

satisfies Yang's odd-level modularity congruences and the signed orbit
condition for the prime divisors of 507.  This certifies a modular-unit
provenance for the quotient packet, but it is not a p25 closer: it still does
not prove equality with the KSY normalized-y finite product, the period-156
value context, DANGER3 framing, or extraction.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_x1_orbit_distribution_bridge_gate import (
    YANG_SOURCE_HANDLE,
    YANG_SOURCE_URL,
    orbit_bad_count,
    packet_residue_exponents,
    prime_factors,
    profile_yang_x1_orbit_distribution_bridge,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
    source_packet,
)


@dataclass(frozen=True)
class YangResidueRow:
    residue: int
    exponent: int
    role: str


@dataclass(frozen=True)
class YangX1507ModularUnitCertificate:
    source_url: str
    source_handle: str
    level: int
    unit_expression: str
    residue_rows: tuple[YangResidueRow, ...]
    distinct_prime_factors: tuple[int, ...]
    exponent_sum: int
    exponent_sum_mod_12: int
    quadratic_sum: int
    quadratic_sum_mod_level: int
    odd_level_modularity_congruences_ok: bool
    general_even_formula_linear_sum_mod_2: int
    general_even_formula_quadratic_sum_mod_2_level: int
    general_even_formula_control_fails: bool
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    unsigned_orbit_bad_counts: tuple[tuple[int, int], ...]
    signed_orbit_condition_ok: bool
    unsigned_orbit_condition_fails_as_control: bool
    yang_orbit_distribution_bridge_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def residue_rows(exponents: dict[int, int]) -> tuple[YangResidueRow, ...]:
    rows: list[YangResidueRow] = []
    for residue, exponent in sorted(exponents.items()):
        role = "numerator" if exponent > 0 else "denominator"
        rows.append(YangResidueRow(residue, exponent, role))
    return tuple(rows)


def unit_expression(exponents: dict[int, int]) -> str:
    numerators = [f"E_{residue}" for residue, exponent in sorted(exponents.items()) if exponent > 0]
    denominators = [f"E_{residue}" for residue, exponent in sorted(exponents.items()) if exponent < 0]
    return f"{' '.join(numerators)} / ({' '.join(denominators)})"


def profile_yang_x1_507_modular_unit_certificate() -> YangX1507ModularUnitCertificate:
    exponents = packet_residue_exponents(source_packet())
    factors = prime_factors(QUOTIENT_LEVEL)
    exponent_sum = sum(exponents.values())
    quadratic_sum = sum(residue * residue * exponent for residue, exponent in exponents.items())
    linear_sum = sum(residue * exponent for residue, exponent in exponents.items())
    signed_bad = tuple(
        (prime, orbit_bad_count(exponents, prime, signed=True))
        for prime in factors
    )
    unsigned_bad = tuple(
        (prime, orbit_bad_count(exponents, prime, signed=False))
        for prime in factors
    )
    signed_ok = all(count == 0 for _prime, count in signed_bad)
    unsigned_control = any(count > 0 for _prime, count in unsigned_bad)
    odd_level_modularity_ok = (
        QUOTIENT_LEVEL % 2 == 1
        and exponent_sum % 12 == 0
        and quadratic_sum % QUOTIENT_LEVEL == 0
    )
    general_even_control_fails = (
        linear_sum % 2 != 0
        and quadratic_sum % (2 * QUOTIENT_LEVEL) != 0
    )
    bridge = profile_yang_x1_orbit_distribution_bridge()
    direct_closer = False
    expected_exponents = {
        25: 1,
        138: -1,
        197: 1,
        310: -1,
        369: 1,
        482: -1,
    }
    row_ok = (
        QUOTIENT_LEVEL == 507
        and factors == (3, 13)
        and exponents == expected_exponents
        and odd_level_modularity_ok
        and general_even_control_fails
        and signed_ok
        and unsigned_control
        and bridge.row_ok
        and not direct_closer
    )
    return YangX1507ModularUnitCertificate(
        source_url=YANG_SOURCE_URL,
        source_handle=YANG_SOURCE_HANDLE,
        level=QUOTIENT_LEVEL,
        unit_expression=unit_expression(exponents),
        residue_rows=residue_rows(exponents),
        distinct_prime_factors=factors,
        exponent_sum=exponent_sum,
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum=quadratic_sum,
        quadratic_sum_mod_level=quadratic_sum % QUOTIENT_LEVEL,
        odd_level_modularity_congruences_ok=odd_level_modularity_ok,
        general_even_formula_linear_sum_mod_2=linear_sum % 2,
        general_even_formula_quadratic_sum_mod_2_level=quadratic_sum % (2 * QUOTIENT_LEVEL),
        general_even_formula_control_fails=general_even_control_fails,
        signed_orbit_bad_counts=signed_bad,
        unsigned_orbit_bad_counts=unsigned_bad,
        signed_orbit_condition_ok=signed_ok,
        unsigned_orbit_condition_fails_as_control=unsigned_control,
        yang_orbit_distribution_bridge_ok=bridge.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "the six-cell quotient packet is a Yang/Yu-compatible modular "
            "unit product on X_1(507)"
        ),
        first_missing_clause=(
            "no source theorem yet identifies this X_1(507) unit with the KSY "
            "normalized-y finite product/value plus period-156 and DANGER3 "
            "extraction data"
        ),
        recommendation=(
            "use U_507 as the quotient-level modular-unit target; future "
            "source hits should connect KSY normalized-y or value identities "
            "to this exact unit, not merely prove modular-unit admissibility"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_x1_507_modular_unit_certificate()
    print("p25 KSY-y Yang X1(507) modular-unit certificate gate")
    print(f"source={profile.source_url}")
    print(f"source_handle={profile.source_handle}")
    print(f"level={profile.level}")
    print(f"unit_expression={profile.unit_expression}")
    print("residue_rows")
    for row in profile.residue_rows:
        print(f"  E_{row.residue}: exponent={row.exponent} role={row.role}")
    print("modularity_congruences")
    print(f"  exponent_sum={profile.exponent_sum}")
    print(f"  exponent_sum_mod_12={profile.exponent_sum_mod_12}")
    print(f"  quadratic_sum={profile.quadratic_sum}")
    print(f"  quadratic_sum_mod_level={profile.quadratic_sum_mod_level}")
    print(
        "  odd_level_modularity_congruences_ok="
        f"{int(profile.odd_level_modularity_congruences_ok)}"
    )
    print("controls")
    print(
        "  general_even_formula_linear_sum_mod_2="
        f"{profile.general_even_formula_linear_sum_mod_2}"
    )
    print(
        "  general_even_formula_quadratic_sum_mod_2_level="
        f"{profile.general_even_formula_quadratic_sum_mod_2_level}"
    )
    print(
        "  general_even_formula_control_fails="
        f"{int(profile.general_even_formula_control_fails)}"
    )
    print("orbit_condition")
    print(f"  distinct_prime_factors={profile.distinct_prime_factors}")
    print(f"  signed_orbit_bad_counts={profile.signed_orbit_bad_counts}")
    print(f"  unsigned_orbit_bad_counts={profile.unsigned_orbit_bad_counts}")
    print(f"  signed_orbit_condition_ok={int(profile.signed_orbit_condition_ok)}")
    print(
        "  unsigned_orbit_condition_fails_as_control="
        f"{int(profile.unsigned_orbit_condition_fails_as_control)}"
    )
    print(f"yang_orbit_distribution_bridge_ok={int(profile.yang_orbit_distribution_bridge_ok)}")
    print(f"direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  quotient_packet_is_valid_X1_507_modular_unit=1")
    print("  quotient_packet_is_not_yet_a_KSY_normalized_y_closure_theorem=1")
    print("  future_theorem_target_is_U_507_to_KSY_y_or_value_identity=1")
    print(
        "ksy_y_yang_x1_507_modular_unit_certificate_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang X1(507) modular-unit certificate regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

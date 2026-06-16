#!/usr/bin/env python3
"""Yang quotient descent for the p25 KSY normalized-y formula.

The previous Yang gates proved that the raw K trace descends to a six-cell
modular unit

    U_507 = E_25 E_197 E_369 / (E_138 E_310 E_482).

This gate applies the KSY formula y(Q) = -g(2Q)/g(Q)^4 after that descent.  The
raw 300-term KSY-y footprint is a union of 12 constant Yang orbits; quotient
level, it is exactly

    Y_507 = [2]^*U_507 / U_507^4.

This is a sharper theorem target, not a p25 closure theorem: it still needs a
source theorem identifying the finite-field value/divisor with the DANGER3
payload, plus period-156 and extraction data.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_ksy_y_yang_x1_507_modular_unit_certificate_gate import (
    profile_yang_x1_507_modular_unit_certificate,
)
from p25_ksy_y_yang_x1_orbit_distribution_bridge_gate import (
    packet_residue_exponents,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_LEVEL,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class YangOrbitDescentRow:
    quotient_residue: int
    coefficient: int
    raw_orbit_support: int
    raw_orbit_coefficients: tuple[int, ...]
    ok: bool


@dataclass(frozen=True)
class YangQuotientNormalizedYDescent:
    raw_footprint_support: int
    raw_footprint_coefficient_counts: tuple[tuple[int, int], ...]
    quotient_footprint_support: int
    quotient_footprint_coefficient_counts: tuple[tuple[int, int], ...]
    quotient_footprint: tuple[tuple[int, int], ...]
    doubled_u_residues: tuple[tuple[int, int], ...]
    u_residues: tuple[tuple[int, int], ...]
    formula_from_u507: tuple[tuple[int, int], ...]
    quotient_equals_doubled_u_over_u4: bool
    orbit_rows: tuple[YangOrbitDescentRow, ...]
    all_raw_orbits_constant: bool
    yang_modular_unit_certificate_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def raw_coord_to_level_12675(coord: Coord) -> int:
    right, c_log = coord
    for lift in range(RIGHT_ORDER):
        residue = c_log + C_ORDER * lift
        if residue % RIGHT_ORDER == right:
            return residue
    raise ValueError(f"no CRT lift for {coord}")


def collapse_raw_footprint_by_yang_orbit(raw_footprint: Ring) -> tuple[dict[int, int], tuple[YangOrbitDescentRow, ...]]:
    orbit_coefficients: dict[int, list[int]] = {}
    for coord, coefficient in raw_footprint.items():
        residue = raw_coord_to_level_12675(coord)
        quotient_residue = residue % QUOTIENT_LEVEL
        orbit_coefficients.setdefault(quotient_residue, []).append(coefficient)

    quotient: dict[int, int] = {}
    rows: list[YangOrbitDescentRow] = []
    for residue, coefficients in sorted(orbit_coefficients.items()):
        unique_coefficients = tuple(sorted(set(coefficients)))
        constant = len(unique_coefficients) == 1
        if constant:
            quotient[residue] = unique_coefficients[0]
        rows.append(
            YangOrbitDescentRow(
                quotient_residue=residue,
                coefficient=unique_coefficients[0] if constant else 0,
                raw_orbit_support=len(coefficients),
                raw_orbit_coefficients=unique_coefficients,
                ok=constant and len(coefficients) == 25,
            )
        )
    return dict(sorted(quotient.items())), tuple(rows)


def doubled_u_over_u4(source_exponents: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, exponent in source_exponents.items():
        doubled = (2 * residue) % QUOTIENT_LEVEL
        out[doubled] = out.get(doubled, 0) + exponent
        out[residue] = out.get(residue, 0) - 4 * exponent
    return dict(sorted((residue, exponent) for residue, exponent in out.items() if exponent))


def coefficient_counts(values: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(values.values()).items()))


def profile_yang_quotient_normalized_y_descent() -> YangQuotientNormalizedYDescent:
    raw = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    quotient, orbit_rows = collapse_raw_footprint_by_yang_orbit(raw)
    u = packet_residue_exponents(source_packet())
    formula = doubled_u_over_u4(u)
    certificate = profile_yang_x1_507_modular_unit_certificate()
    all_constant = all(row.ok for row in orbit_rows)
    direct_closer = False
    expected_quotient = {
        25: -4,
        50: 1,
        113: -1,
        138: 4,
        197: -4,
        231: 1,
        276: -1,
        310: 4,
        369: -4,
        394: 1,
        457: -1,
        482: 4,
    }
    row_ok = (
        len(raw) == 300
        and coefficient_counts({raw_coord_to_level_12675(coord): coeff for coord, coeff in raw.items()})
        == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and len(quotient) == 12
        and quotient == expected_quotient
        and formula == quotient
        and all_constant
        and tuple(sorted(row.raw_orbit_support for row in orbit_rows)) == (25,) * 12
        and certificate.row_ok
        and not direct_closer
    )
    return YangQuotientNormalizedYDescent(
        raw_footprint_support=len(raw),
        raw_footprint_coefficient_counts=coefficient_counts(
            {raw_coord_to_level_12675(coord): coeff for coord, coeff in raw.items()}
        ),
        quotient_footprint_support=len(quotient),
        quotient_footprint_coefficient_counts=coefficient_counts(quotient),
        quotient_footprint=tuple(sorted(quotient.items())),
        doubled_u_residues=tuple(sorted((2 * residue % QUOTIENT_LEVEL, exponent) for residue, exponent in u.items())),
        u_residues=tuple(sorted(u.items())),
        formula_from_u507=tuple(sorted(formula.items())),
        quotient_equals_doubled_u_over_u4=quotient == formula,
        orbit_rows=orbit_rows,
        all_raw_orbits_constant=all_constant,
        yang_modular_unit_certificate_ok=certificate.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "the KSY-y 300-term footprint descends to the quotient modular unit "
            "Y_507=[2]^*U_507/U_507^4"
        ),
        first_missing_clause=(
            "no source theorem yet proves the finite-field value or divisor "
            "identity for Y_507 with period-156 context and DANGER3 extraction"
        ),
        recommendation=(
            "make Y_507=[2]^*U_507/U_507^4 the quotient-level normalized-y "
            "target for future source/theorem hits"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_quotient_normalized_y_descent()
    print("p25 KSY-y Yang quotient normalized-y descent gate")
    print("raw")
    print(f"  raw_footprint_support={profile.raw_footprint_support}")
    print(f"  raw_footprint_coefficient_counts={profile.raw_footprint_coefficient_counts}")
    print("quotient")
    print(f"  quotient_footprint_support={profile.quotient_footprint_support}")
    print(f"  quotient_footprint_coefficient_counts={profile.quotient_footprint_coefficient_counts}")
    print(f"  quotient_footprint={profile.quotient_footprint}")
    print(f"  u_residues={profile.u_residues}")
    print(f"  doubled_u_residues={profile.doubled_u_residues}")
    print(f"  formula_from_u507={profile.formula_from_u507}")
    print(
        "  quotient_equals_doubled_u_over_u4="
        f"{int(profile.quotient_equals_doubled_u_over_u4)}"
    )
    print("yang_orbits")
    for row in profile.orbit_rows:
        print(
            "  "
            f"residue={row.quotient_residue} coeff={row.coefficient} "
            f"support={row.raw_orbit_support} constants={row.raw_orbit_coefficients} "
            f"ok={int(row.ok)}"
        )
    print("checks")
    print(f"  all_raw_orbits_constant={int(profile.all_raw_orbits_constant)}")
    print(f"  yang_modular_unit_certificate_ok={int(profile.yang_modular_unit_certificate_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  KSY_y_footprint_descends_to_Y_507=1")
    print("  Y_507_equals_doubled_U_507_divided_by_U_507_fourth_power=1")
    print("  quotient_descent_is_not_yet_a_finite_field_value_theorem=1")
    print(
        "ksy_y_yang_quotient_normalized_y_descent_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang quotient normalized-y descent regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

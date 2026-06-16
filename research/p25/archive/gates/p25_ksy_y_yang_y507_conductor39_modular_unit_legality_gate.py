#!/usr/bin/env python3
"""Modular-unit legality for conductor-39 Hilbert-90 potentials.

The Hilbert-90 boundary gate gives a balanced potential and two sparse
one-coset potentials for the conductor-39 word.  This gate separates formal
group-ring usefulness from Yang/Yu modular-unit legality:

* W = -6 chi_39 and V_bal = -3 chi_39 pass the odd-level modular-unit tests.
* The sparse support-12 gauges pass elementary congruences but fail the
  Yang/Yu orbit condition, so they are formal Hilbert-90 gauges rather than
  standalone X_1(39) modular units.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39


@dataclass(frozen=True)
class Conductor39UnitLegalityRow:
    name: str
    word: tuple[tuple[int, int], ...]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_sum_mod_level: int
    odd_level_modularity_congruences_ok: bool
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    unsigned_orbit_bad_counts: tuple[tuple[int, int], ...]
    signed_orbit_condition_ok: bool
    yang_yu_modular_unit_ok: bool
    expected_yang_yu_modular_unit_ok: bool
    first_failing_clause: str
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39ModularUnitLegality:
    level: int
    rows: tuple[Conductor39UnitLegalityRow, ...]
    legal_rows: int
    formal_only_rows: int
    hilbert90_boundary_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def prime_factors(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    remaining = value
    for divisor in range(2, isqrt(remaining) + 1):
        if remaining % divisor:
            continue
        factors.append(divisor)
        while remaining % divisor == 0:
            remaining //= divisor
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def orbit_bad_count(exponents: dict[int, int], prime: int, signed: bool) -> int:
    step = CONDUCTOR // prime
    seen: set[tuple[int, ...]] = set()
    bad = 0
    for residue in range(CONDUCTOR):
        orbit: set[int] = set()
        for layer in range(prime):
            point = (residue + layer * step) % CONDUCTOR
            orbit.add(point)
            if signed:
                orbit.add((-point) % CONDUCTOR)
        key = tuple(sorted(orbit))
        if key in seen:
            continue
        seen.add(key)
        if sum(exponents.get(point, 0) for point in key):
            bad += 1
    return bad


def character_word() -> dict[int, int]:
    return {residue: -6 * chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def balanced_potential_word() -> dict[int, int]:
    return {residue: -3 * chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def positive_sparse_word() -> dict[int, int]:
    return {residue: 6 for residue in range(CONDUCTOR) if chi39(residue) == -1}


def negative_sparse_word() -> dict[int, int]:
    return {residue: -6 for residue in range(CONDUCTOR) if chi39(residue) == 1}


def legality_row(
    name: str,
    word: dict[int, int],
    expected_yang_yu_modular_unit_ok: bool,
    first_failing_clause: str,
) -> Conductor39UnitLegalityRow:
    factors = prime_factors(CONDUCTOR)
    exponent_sum = sum(word.values())
    quadratic_sum = sum(residue * residue * coefficient for residue, coefficient in word.items())
    congruences_ok = (
        CONDUCTOR % 2 == 1
        and exponent_sum % 12 == 0
        and quadratic_sum % CONDUCTOR == 0
    )
    signed_bad = tuple((prime, orbit_bad_count(word, prime, signed=True)) for prime in factors)
    unsigned_bad = tuple((prime, orbit_bad_count(word, prime, signed=False)) for prime in factors)
    signed_ok = all(count == 0 for _prime, count in signed_bad)
    yang_ok = congruences_ok and signed_ok
    return Conductor39UnitLegalityRow(
        name=name,
        word=tuple(sorted(word.items())),
        support=len(word),
        coefficient_counts=coefficient_counts(word),
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_sum_mod_level=quadratic_sum % CONDUCTOR,
        odd_level_modularity_congruences_ok=congruences_ok,
        signed_orbit_bad_counts=signed_bad,
        unsigned_orbit_bad_counts=unsigned_bad,
        signed_orbit_condition_ok=signed_ok,
        yang_yu_modular_unit_ok=yang_ok,
        expected_yang_yu_modular_unit_ok=expected_yang_yu_modular_unit_ok,
        first_failing_clause=first_failing_clause,
        ok=yang_ok == expected_yang_yu_modular_unit_ok,
    )


def profile_yang_y507_conductor39_modular_unit_legality() -> YangY507Conductor39ModularUnitLegality:
    hilbert90 = profile_yang_y507_conductor39_hilbert90_boundary()
    rows = (
        legality_row(
            "period_norm_character_W",
            character_word(),
            True,
            "none; W is a valid X_1(39) Yang/Yu modular-unit exponent word",
        ),
        legality_row(
            "balanced_hilbert90_potential_V_bal",
            balanced_potential_word(),
            True,
            "none; V_bal is a valid X_1(39) Yang/Yu modular-unit exponent word",
        ),
        legality_row(
            "positive_sparse_formal_potential_V_pos",
            positive_sparse_word(),
            False,
            "Yang/Yu signed orbit condition fails despite elementary congruences",
        ),
        legality_row(
            "negative_sparse_formal_potential_V_neg",
            negative_sparse_word(),
            False,
            "Yang/Yu signed orbit condition fails despite elementary congruences",
        ),
    )
    legal = sum(row.yang_yu_modular_unit_ok for row in rows)
    formal_only = sum(not row.yang_yu_modular_unit_ok for row in rows)
    direct_closer = False
    row_ok = (
        hilbert90.row_ok
        and CONDUCTOR == 39
        and legal == 2
        and formal_only == 2
        and all(row.ok for row in rows)
        and rows[0].support == 24
        and rows[1].support == 24
        and rows[2].support == 12
        and rows[3].support == 12
        and rows[0].signed_orbit_bad_counts == ((3, 0), (13, 0))
        and rows[1].signed_orbit_bad_counts == ((3, 0), (13, 0))
        and rows[2].signed_orbit_bad_counts == ((3, 6), (13, 1))
        and rows[3].signed_orbit_bad_counts == ((3, 6), (13, 1))
        and not direct_closer
    )
    return YangY507Conductor39ModularUnitLegality(
        level=CONDUCTOR,
        rows=rows,
        legal_rows=legal,
        formal_only_rows=formal_only,
        hilbert90_boundary_ok=hilbert90.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "W=-6*chi_39 and V_bal=-3*chi_39 are legal X_1(39) modular-unit "
            "words; the sparse one-coset Hilbert-90 gauges are formal only."
        ),
        first_missing_clause=(
            "modular-unit legality does not provide the finite-field value/divisor "
            "theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask source theorems for the balanced legal modular-unit potential "
            "or for a formal Hilbert-90 ratio that explains why a sparse gauge "
            "is allowed; do not advertise V_pos/V_neg as standalone Yang units"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_yang_y507_conductor39_modular_unit_legality()
    print("p25 KSY-y Yang Y_507 conductor-39 modular-unit legality gate")
    print(f"level={profile.level}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: support={row.support} counts={row.coefficient_counts} "
            f"sum_mod12={row.exponent_sum_mod_12} "
            f"quad_mod_level={row.quadratic_sum_mod_level} "
            f"congruences={int(row.odd_level_modularity_congruences_ok)} "
            f"signed_bad={row.signed_orbit_bad_counts} "
            f"unsigned_bad={row.unsigned_orbit_bad_counts} "
            f"signed_ok={int(row.signed_orbit_condition_ok)} "
            f"yang_yu_ok={int(row.yang_yu_modular_unit_ok)} "
            f"expected={int(row.expected_yang_yu_modular_unit_ok)} "
            f"ok={int(row.ok)}"
        )
        print(f"    first_failing_clause={row.first_failing_clause}")
    print("checks")
    print(f"  legal_rows={profile.legal_rows}")
    print(f"  formal_only_rows={profile.formal_only_rows}")
    print(f"  hilbert90_boundary_ok={int(profile.hilbert90_boundary_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  balanced_hilbert90_potential_is_legal_X1_39_modular_unit=1")
    print("  sparse_one_coset_potentials_are_formal_not_Yang_units=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_modular_unit_legality_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 modular-unit legality regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

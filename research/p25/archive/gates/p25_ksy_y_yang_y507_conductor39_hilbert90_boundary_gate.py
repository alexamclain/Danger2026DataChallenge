#!/usr/bin/env python3
"""Hilbert-90 boundary shape for the p25 conductor-39 character word.

The Frobenius orbit gate proves that Frob_p sends the conductor-39 period-norm
word W to -W.  Therefore W is a norm-one exponent word.  This gate records the
explicit integral Hilbert-90 boundary:

    W = (1 - Frob_p) V.

There are two useful gauges: the balanced anti-invariant potential V = W/2
with coefficients +/-3, and sparse one-coset potentials with support 12 and
coefficients +/-6.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_frobenius_orbit_gate import (
    profile_yang_y507_conductor39_frobenius_orbit,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR, chi39
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25


@dataclass(frozen=True)
class PotentialProfile:
    name: str
    word: tuple[tuple[int, int], ...]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    boundary_equals_character_word: bool
    frobenius_image_equals_negative: bool
    nonnegative: bool
    nonpositive: bool
    ok: bool


@dataclass(frozen=True)
class OrbitGaugeRow:
    orbit: tuple[int, ...]
    balanced_values: tuple[int, ...]
    min_l_infty: int
    min_l_infty_shifts: tuple[int, ...]
    min_support: int
    min_support_shifts: tuple[int, ...]
    ok: bool


@dataclass(frozen=True)
class YangY507Conductor39Hilbert90Boundary:
    conductor: int
    p_mod_39: int
    character_word: tuple[tuple[int, int], ...]
    balanced_potential: PotentialProfile
    positive_sparse_potential: PotentialProfile
    negative_sparse_potential: PotentialProfile
    orbit_gauge_rows: tuple[OrbitGaugeRow, ...]
    total_min_l_infty: int
    total_min_support: int
    balanced_support: int
    sparse_support: int
    frobenius_orbit_gate_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, coefficient) for residue, coefficient in word.items() if coefficient))


def character_word() -> dict[int, int]:
    return {residue: -6 * chi39(residue) for residue in range(CONDUCTOR) if chi39(residue)}


def push_frobenius(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, coefficient in word.items():
        target = (P25 * residue) % CONDUCTOR
        out[target] = out.get(target, 0) + coefficient
    return nonzero(out)


def subtract_words(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for residue, coefficient in right.items():
        out[residue] = out.get(residue, 0) - coefficient
    return nonzero(out)


def coefficient_counts(word: dict[int, int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for coefficient in word.values():
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def negative_word(word: dict[int, int]) -> dict[int, int]:
    return {residue: -coefficient for residue, coefficient in word.items()}


def boundary(potential: dict[int, int]) -> dict[int, int]:
    return subtract_words(potential, push_frobenius(potential))


def balanced_potential_word(source: dict[int, int]) -> dict[int, int]:
    return {residue: coefficient // 2 for residue, coefficient in source.items()}


def sparse_potential_word(source: dict[int, int], sign: int) -> dict[int, int]:
    return {
        residue: coefficient
        for residue, coefficient in source.items()
        if coefficient * sign > 0
    }


def potential_profile(name: str, potential: dict[int, int], source: dict[int, int]) -> PotentialProfile:
    image = push_frobenius(potential)
    return PotentialProfile(
        name=name,
        word=tuple(sorted(potential.items())),
        support=len(potential),
        coefficient_counts=coefficient_counts(potential),
        boundary_equals_character_word=boundary(potential) == source,
        frobenius_image_equals_negative=image == negative_word(potential),
        nonnegative=all(coefficient > 0 for coefficient in potential.values()),
        nonpositive=all(coefficient < 0 for coefficient in potential.values()),
        ok=boundary(potential) == source,
    )


def frobenius_orbits(source: dict[int, int]) -> tuple[tuple[int, ...], ...]:
    seen: set[int] = set()
    rows: list[tuple[int, ...]] = []
    for residue in sorted(source):
        if residue in seen:
            continue
        orbit: list[int] = []
        current = residue
        while current not in orbit:
            orbit.append(current)
            seen.add(current)
            current = (P25 * current) % CONDUCTOR
        rows.append(tuple(orbit))
    return tuple(rows)


def orbit_gauge_row(orbit: tuple[int, ...], balanced: dict[int, int]) -> OrbitGaugeRow:
    values = tuple(balanced[residue] for residue in orbit)
    best_l_infty = min(max(abs(value + shift) for value in values) for shift in range(-12, 13))
    best_l_infty_shifts = tuple(
        shift
        for shift in range(-12, 13)
        if max(abs(value + shift) for value in values) == best_l_infty
    )
    best_support = min(sum(1 for value in values if value + shift) for shift in range(-12, 13))
    best_support_shifts = tuple(
        shift
        for shift in range(-12, 13)
        if sum(1 for value in values if value + shift) == best_support
    )
    return OrbitGaugeRow(
        orbit=orbit,
        balanced_values=values,
        min_l_infty=best_l_infty,
        min_l_infty_shifts=best_l_infty_shifts,
        min_support=best_support,
        min_support_shifts=best_support_shifts,
        ok=(
            values == (-3, 3, -3, 3, -3, 3)
            and best_l_infty == 3
            and best_l_infty_shifts == (0,)
            and best_support == 3
            and best_support_shifts == (-3, 3)
        ),
    )


def profile_yang_y507_conductor39_hilbert90_boundary() -> YangY507Conductor39Hilbert90Boundary:
    orbit_profile = profile_yang_y507_conductor39_frobenius_orbit()
    source = character_word()
    balanced = balanced_potential_word(source)
    positive_sparse = sparse_potential_word(source, 1)
    negative_sparse = sparse_potential_word(source, -1)
    balanced_profile = potential_profile("balanced_half_character", balanced, source)
    positive_profile = potential_profile("positive_sparse_coset", positive_sparse, source)
    negative_profile = potential_profile("negative_sparse_coset", negative_sparse, source)
    orbit_rows = tuple(orbit_gauge_row(orbit, balanced) for orbit in frobenius_orbits(source))
    direct_closer = False
    row_ok = (
        orbit_profile.row_ok
        and CONDUCTOR == 39
        and P25 % 39 == 23
        and tuple(sorted(source.items())) == orbit_profile.word_mod39
        and balanced_profile.ok
        and positive_profile.ok
        and negative_profile.ok
        and balanced_profile.frobenius_image_equals_negative
        and not positive_profile.frobenius_image_equals_negative
        and not negative_profile.frobenius_image_equals_negative
        and balanced_profile.support == 24
        and balanced_profile.coefficient_counts == ((-3, 12), (3, 12))
        and positive_profile.support == 12
        and positive_profile.coefficient_counts == ((6, 12),)
        and positive_profile.nonnegative
        and negative_profile.support == 12
        and negative_profile.coefficient_counts == ((-6, 12),)
        and negative_profile.nonpositive
        and len(orbit_rows) == 4
        and all(row.ok for row in orbit_rows)
        and not direct_closer
    )
    return YangY507Conductor39Hilbert90Boundary(
        conductor=CONDUCTOR,
        p_mod_39=P25 % 39,
        character_word=tuple(sorted(source.items())),
        balanced_potential=balanced_profile,
        positive_sparse_potential=positive_profile,
        negative_sparse_potential=negative_profile,
        orbit_gauge_rows=orbit_rows,
        total_min_l_infty=sum(row.min_l_infty for row in orbit_rows),
        total_min_support=sum(row.min_support for row in orbit_rows),
        balanced_support=balanced_profile.support,
        sparse_support=positive_profile.support,
        frobenius_orbit_gate_ok=orbit_profile.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The conductor-39 character word is the integral Hilbert-90 boundary "
            "(1-Frob_p)V, with balanced V=-3*chi_39 and sparse one-coset "
            "potentials of support 12."
        ),
        first_missing_clause=(
            "the boundary shape is a value-side routing target, not a finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask value-side sources for a Hilbert-90 ratio, twisted trace, or "
            "sparse one-coset potential whose (1-Frob_p) boundary is the "
            "conductor-39 word; reject ordinary norm-only claims"
        ),
        row_ok=row_ok,
    )


def print_potential(profile: PotentialProfile) -> None:
    print(f"  {profile.name}:")
    print(f"    support={profile.support}")
    print(f"    coefficient_counts={profile.coefficient_counts}")
    print(f"    boundary_equals_character_word={int(profile.boundary_equals_character_word)}")
    print(f"    frobenius_image_equals_negative={int(profile.frobenius_image_equals_negative)}")
    print(f"    nonnegative={int(profile.nonnegative)}")
    print(f"    nonpositive={int(profile.nonpositive)}")
    print(f"    word={profile.word}")
    print(f"    ok={int(profile.ok)}")


def main() -> int:
    profile = profile_yang_y507_conductor39_hilbert90_boundary()
    print("p25 KSY-y Yang Y_507 conductor-39 Hilbert-90 boundary gate")
    print(f"conductor={profile.conductor}")
    print(f"p_mod_39={profile.p_mod_39}")
    print(f"character_word={profile.character_word}")
    print("potentials")
    print_potential(profile.balanced_potential)
    print_potential(profile.positive_sparse_potential)
    print_potential(profile.negative_sparse_potential)
    print("orbit_gauge_rows")
    for row in profile.orbit_gauge_rows:
        print(
            "  "
            f"orbit={row.orbit} balanced_values={row.balanced_values} "
            f"min_l_infty={row.min_l_infty} "
            f"min_l_infty_shifts={row.min_l_infty_shifts} "
            f"min_support={row.min_support} "
            f"min_support_shifts={row.min_support_shifts} "
            f"ok={int(row.ok)}"
        )
    print("checks")
    print(f"  total_min_l_infty={profile.total_min_l_infty}")
    print(f"  total_min_support={profile.total_min_support}")
    print(f"  balanced_support={profile.balanced_support}")
    print(f"  sparse_support={profile.sparse_support}")
    print(f"  frobenius_orbit_gate_ok={int(profile.frobenius_orbit_gate_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  conductor39_word_is_integral_hilbert90_boundary=1")
    print("  balanced_half_character_is_unique_min_l_infty_gauge=1")
    print("  sparse_one_coset_potential_is_min_support_gauge=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_hilbert90_boundary_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Yang Y_507 conductor-39 Hilbert-90 boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

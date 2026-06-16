#!/usr/bin/env python3
"""Legal Hilbert-90 gauge family for the p25 conductor-39 word.

The boundary equation W=(1-Frob_p)V has many formal solutions: add any
Frobenius-invariant constant on each of the four length-6 Frobenius orbits.
This gate solves the Yang/Yu modular-unit constraints on those four constants.

The result is a useful refinement.  The all-positive/all-negative one-coset
sparse gauges are formal only, but there are four mixed sparse support-12
gauges that are genuine X_1(39) modular-unit exponent words.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (
    boundary,
    character_word,
    coefficient_counts,
    frobenius_orbits,
    balanced_potential_word,
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate import (
    legality_row,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR
from p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate import P25


@dataclass(frozen=True)
class SignedOrbitEquation:
    prime: int
    base_sum: int
    orbit_constant_coefficients: tuple[int, int, int, int]
    normalized_equation: str
    ok: bool


@dataclass(frozen=True)
class GaugeSample:
    name: str
    constants: tuple[int, int, int, int]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    boundary_equals_character_word: bool
    yang_yu_modular_unit_ok: bool
    signed_orbit_bad_counts: tuple[tuple[int, int], ...]
    expected_yang_yu_modular_unit_ok: bool
    word: tuple[tuple[int, int], ...]
    ok: bool


@dataclass(frozen=True)
class LegalGaugeFamilyProfile:
    conductor: int
    p_mod_39: int
    frobenius_orbits: tuple[tuple[int, ...], ...]
    formal_kernel_dimension: int
    legal_family_dimension: int
    signed_orbit_equations: tuple[SignedOrbitEquation, ...]
    balanced_sample: GaugeSample
    legal_sparse_samples: tuple[GaugeSample, ...]
    legal_mixed_support18_samples: tuple[GaugeSample, ...]
    formal_one_coset_samples: tuple[GaugeSample, ...]
    support12_legal_sparse_rows: int
    support12_formal_one_coset_rows: int
    min_legal_support: int
    min_support_parameter_rows: int
    min_l_infty: int
    min_l_infty_parameter_rows: int
    hilbert90_boundary_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def gauge_word(constants: tuple[int, int, int, int]) -> dict[int, int]:
    source = character_word()
    out = dict(balanced_potential_word(source))
    for constant, orbit in zip(constants, frobenius_orbits(source)):
        for residue in orbit:
            value = out.get(residue, 0) + constant
            if value:
                out[residue] = value
            elif residue in out:
                del out[residue]
    return dict(sorted(out.items()))


def gauge_from_parameters(a_value: int, b_value: int) -> tuple[int, int, int, int]:
    return (a_value, b_value, -a_value, -b_value)


def signed_orbit_equations() -> tuple[SignedOrbitEquation, ...]:
    source = character_word()
    balanced = balanced_potential_word(source)
    orbits = frobenius_orbits(source)
    rows: list[SignedOrbitEquation] = []
    seen: set[tuple[int, tuple[int, int, int, int]]] = set()
    for prime in (3, 13):
        step = CONDUCTOR // prime
        signed_orbits: set[tuple[int, ...]] = set()
        for residue in range(CONDUCTOR):
            signed_orbit: set[int] = set()
            for layer in range(prime):
                point = (residue + layer * step) % CONDUCTOR
                signed_orbit.add(point)
                signed_orbit.add((-point) % CONDUCTOR)
            signed_orbits.add(tuple(sorted(signed_orbit)))
        for signed_orbit in sorted(signed_orbits):
            base = sum(balanced.get(residue, 0) for residue in signed_orbit)
            coeffs = tuple(
                sum(1 for residue in signed_orbit if residue in orbit)
                for orbit in orbits
            )
            if not base and not any(coeffs):
                continue
            key = (base, coeffs)
            if key in seen:
                continue
            seen.add(key)
            if coeffs == (2, 0, 2, 0):
                normalized = "c0 + c2 = 0"
            elif coeffs == (0, 2, 0, 2):
                normalized = "c1 + c3 = 0"
            elif coeffs == (6, 6, 6, 6):
                normalized = "c0 + c1 + c2 + c3 = 0"
            else:
                normalized = "unexpected"
            rows.append(
                SignedOrbitEquation(
                    prime=prime,
                    base_sum=base,
                    orbit_constant_coefficients=coeffs,
                    normalized_equation=normalized,
                    ok=base == 0 and normalized != "unexpected",
                )
            )
    return tuple(rows)


def gauge_sample(
    name: str,
    constants: tuple[int, int, int, int],
    expected_yang_yu_modular_unit_ok: bool,
) -> GaugeSample:
    word = gauge_word(constants)
    row = legality_row(
        name,
        word,
        expected_yang_yu_modular_unit_ok,
        "formal Hilbert-90 gauge family legality sample",
    )
    source = character_word()
    boundary_ok = boundary(word) == source
    ok = (
        boundary_ok
        and row.yang_yu_modular_unit_ok == expected_yang_yu_modular_unit_ok
        and row.ok
    )
    return GaugeSample(
        name=name,
        constants=constants,
        support=len(word),
        coefficient_counts=coefficient_counts(word),
        boundary_equals_character_word=boundary_ok,
        yang_yu_modular_unit_ok=row.yang_yu_modular_unit_ok,
        signed_orbit_bad_counts=row.signed_orbit_bad_counts,
        expected_yang_yu_modular_unit_ok=expected_yang_yu_modular_unit_ok,
        word=tuple(sorted(word.items())),
        ok=ok,
    )


def legal_support(a_value: int, b_value: int) -> int:
    def orbit_support(constant: int) -> int:
        return 3 if abs(constant) == 3 else 6

    return 2 * orbit_support(a_value) + 2 * orbit_support(b_value)


def legal_l_infty(a_value: int, b_value: int) -> int:
    return 3 + max(abs(a_value), abs(b_value))


def profile_hilbert90_legal_gauge_family() -> LegalGaugeFamilyProfile:
    hilbert90 = profile_yang_y507_conductor39_hilbert90_boundary()
    source = character_word()
    orbits = frobenius_orbits(source)
    equations = signed_orbit_equations()
    balanced = gauge_sample("balanced_legal_V_bal", (0, 0, 0, 0), True)
    legal_sparse = tuple(
        gauge_sample(
            f"legal_sparse_mixed_a{a_value:+d}_b{b_value:+d}",
            gauge_from_parameters(a_value, b_value),
            True,
        )
        for a_value, b_value in ((3, 3), (3, -3), (-3, 3), (-3, -3))
    )
    support18 = tuple(
        gauge_sample(
            f"legal_mixed_support18_a{a_value:+d}_b{b_value:+d}",
            gauge_from_parameters(a_value, b_value),
            True,
        )
        for a_value, b_value in ((3, 0), (0, 3))
    )
    formal_one_coset = (
        gauge_sample("formal_positive_one_coset", (3, 3, 3, 3), False),
        gauge_sample("formal_negative_one_coset", (-3, -3, -3, -3), False),
    )
    support_box = tuple(
        legal_support(a_value, b_value)
        for a_value in range(-12, 13)
        for b_value in range(-12, 13)
    )
    linf_box = tuple(
        legal_l_infty(a_value, b_value)
        for a_value in range(-12, 13)
        for b_value in range(-12, 13)
    )
    min_support = min(support_box)
    min_linf = min(linf_box)
    direct_closer = False
    row_ok = (
        hilbert90.row_ok
        and CONDUCTOR == 39
        and P25 % 39 == 23
        and len(orbits) == 4
        and tuple(len(orbit) for orbit in orbits) == (6, 6, 6, 6)
        and tuple(row.normalized_equation for row in equations)
        == ("c0 + c2 = 0", "c1 + c3 = 0", "c0 + c1 + c2 + c3 = 0")
        and all(row.ok for row in equations)
        and balanced.ok
        and balanced.support == 24
        and all(row.ok and row.support == 12 for row in legal_sparse)
        and all(row.coefficient_counts == ((-6, 6), (6, 6)) for row in legal_sparse)
        and all(row.ok and row.support == 18 for row in support18)
        and all(row.ok and not row.yang_yu_modular_unit_ok for row in formal_one_coset)
        and tuple(row.signed_orbit_bad_counts for row in formal_one_coset)
        == (((3, 6), (13, 1)), ((3, 6), (13, 1)))
        and min_support == 12
        and support_box.count(12) == 4
        and min_linf == 3
        and linf_box.count(3) == 1
        and not direct_closer
    )
    return LegalGaugeFamilyProfile(
        conductor=CONDUCTOR,
        p_mod_39=P25 % 39,
        frobenius_orbits=orbits,
        formal_kernel_dimension=4,
        legal_family_dimension=2,
        signed_orbit_equations=equations,
        balanced_sample=balanced,
        legal_sparse_samples=legal_sparse,
        legal_mixed_support18_samples=support18,
        formal_one_coset_samples=formal_one_coset,
        support12_legal_sparse_rows=sum(row.support == 12 and row.yang_yu_modular_unit_ok for row in legal_sparse),
        support12_formal_one_coset_rows=sum(row.support == 12 and not row.yang_yu_modular_unit_ok for row in formal_one_coset),
        min_legal_support=min_support,
        min_support_parameter_rows=support_box.count(12),
        min_l_infty=min_linf,
        min_l_infty_parameter_rows=linf_box.count(3),
        hilbert90_boundary_ok=hilbert90.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "Yang/Yu legality cuts the four-constant Hilbert-90 gauge kernel "
            "to c=(a,b,-a,-b); this includes four legal mixed sparse support-12 "
            "potentials, while the two one-coset sparse gauges remain formal only."
        ),
        first_missing_clause=(
            "legal gauge classification is still not a finite-field value/divisor "
            "theorem or DANGER3 extraction"
        ),
        recommendation=(
            "accept value-side source hits that emit either V_bal=3*U_chi or one "
            "of the four legal mixed sparse Hilbert-90 gauges; reject all-positive "
            "or all-negative one-coset gauges unless a separate ratio boundary "
            "legitimizes them"
        ),
        row_ok=row_ok,
    )


def print_sample(sample: GaugeSample) -> None:
    print(
        "  "
        f"{sample.name}: constants={sample.constants} support={sample.support} "
        f"counts={sample.coefficient_counts} boundary={int(sample.boundary_equals_character_word)} "
        f"yang_yu={int(sample.yang_yu_modular_unit_ok)} "
        f"expected={int(sample.expected_yang_yu_modular_unit_ok)} "
        f"signed_bad={sample.signed_orbit_bad_counts} ok={int(sample.ok)}"
    )


def main() -> int:
    profile = profile_hilbert90_legal_gauge_family()
    print("p25 KSY-y Yang Y_507 conductor-39 Hilbert-90 legal gauge family gate")
    print(f"conductor={profile.conductor}")
    print(f"p_mod_39={profile.p_mod_39}")
    print(f"frobenius_orbits={profile.frobenius_orbits}")
    print("dimensions")
    print(f"  formal_kernel_dimension={profile.formal_kernel_dimension}")
    print(f"  legal_family_dimension={profile.legal_family_dimension}")
    print("signed_orbit_equations")
    for row in profile.signed_orbit_equations:
        print(
            "  "
            f"prime={row.prime} base={row.base_sum} "
            f"coefficients={row.orbit_constant_coefficients} "
            f"equation={row.normalized_equation} ok={int(row.ok)}"
        )
    print("balanced_sample")
    print_sample(profile.balanced_sample)
    print("legal_sparse_samples")
    for sample in profile.legal_sparse_samples:
        print_sample(sample)
    print("legal_support18_samples")
    for sample in profile.legal_mixed_support18_samples:
        print_sample(sample)
    print("formal_one_coset_samples")
    for sample in profile.formal_one_coset_samples:
        print_sample(sample)
    print("counts")
    print(f"  support12_legal_sparse_rows={profile.support12_legal_sparse_rows}")
    print(f"  support12_formal_one_coset_rows={profile.support12_formal_one_coset_rows}")
    print(f"  min_legal_support={profile.min_legal_support}")
    print(f"  min_support_parameter_rows={profile.min_support_parameter_rows}")
    print(f"  min_l_infty={profile.min_l_infty}")
    print(f"  min_l_infty_parameter_rows={profile.min_l_infty_parameter_rows}")
    print(f"  hilbert90_boundary_ok={int(profile.hilbert90_boundary_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  legal_hilbert90_gauges_are_exactly_c_equals_a_b_minus_a_minus_b=1")
    print("  four_mixed_sparse_support12_gauges_are_legal_X1_39_units=1")
    print("  one_coset_sparse_gauges_remain_formal_only=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Hilbert-90 legal gauge family regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Product normal form for legal sparse Hilbert-90 Yang lifts.

The sparse Yang-lift gate proves that each legal support-12 conductor-39 gauge
lifts to a support-156 level-507 potential.  This gate turns that into the
smallest current product target:

    H = 6 * (1_P - 1_N),

where P and N are 78-element Yang fibers.  The four legal choices are one
orbit of the canonical choice under the conductor-39 doubling subgroup <2>,
with a three-element stabilizer.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_ksy_y_yang_y507_conductor39_distribution_lift_gate import (
    LIFT_LENGTH,
    distribution_lift,
)
from p25_ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_gate import gauge_word
from p25_ksy_y_yang_y507_conductor39_hilbert90_sparse_selector_structure_gate import (
    profile_hilbert90_sparse_selector_structure,
)
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (
    boundary_507,
    coefficient_counts,
    profile_sparse_hilbert90_yang_lift,
)
from p25_ksy_y_yang_y507_modular_period_certificate_gate import SUPPORT_PERIOD
from p25_ksy_y_yang_y507_period_norm_character_gate import period_norm
from p25_ksy_y_yang_y507_primitive_factor_word_gate import (
    profile_yang_y507_primitive_factor_word,
)
from p25_ksy_y_yang_y507_period_norm_conductor_gate import CONDUCTOR
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import QUOTIENT_LEVEL


Word = dict[int, int]


@dataclass(frozen=True)
class SparseProductNormalFormRow:
    selector_name: str
    multiplier_from_canonical: int
    source_constants: tuple[int, int, int, int]
    source_positive_residues: tuple[int, ...]
    source_negative_residues: tuple[int, ...]
    source_positive_count: int
    source_negative_count: int
    lifted_positive_count: int
    lifted_negative_count: int
    lifted_support: int
    lifted_coefficient_counts: tuple[tuple[int, int], ...]
    boundary_equals_period_norm: bool
    equals_multiplier_image_of_canonical: bool
    product_formula: str
    row_ok: bool


@dataclass(frozen=True)
class SparseH90ProductNormalFormProfile:
    conductor: int
    target_level: int
    lift_length: int
    support_period: int
    doubling_subgroup: tuple[int, ...]
    canonical_stabilizer: tuple[int, ...]
    quotient_representatives: tuple[int, ...]
    canonical_positive_residues: tuple[int, ...]
    canonical_negative_residues: tuple[int, ...]
    canonical_positive_lift_count: int
    canonical_negative_lift_count: int
    legal_rows: tuple[SparseProductNormalFormRow, ...]
    legal_rows_form_one_doubling_orbit: bool
    legal_rows_are_78_over_78_products: bool
    formal_one_coset_controls_rejected: bool
    sparse_yang_lift_ok: bool
    direct_closer: bool
    positive_payload: str
    first_missing_clause: str
    recommendation: str
    row_ok: bool


def doubling_subgroup() -> tuple[int, ...]:
    values: list[int] = []
    current = 1
    while current not in values:
        values.append(current)
        current = (2 * current) % CONDUCTOR
    return tuple(values)


def push_source_word(word: Word, multiplier: int) -> Word:
    out: Word = {}
    for residue, coefficient in word.items():
        target = (multiplier * residue) % CONDUCTOR
        out[target] = out.get(target, 0) + coefficient
    return dict(sorted((residue, coefficient) for residue, coefficient in out.items() if coefficient))


def push_lift_word(word: Word, multiplier: int) -> Word:
    out: Word = {}
    for residue, coefficient in word.items():
        target = (multiplier * residue) % QUOTIENT_LEVEL
        out[target] = out.get(target, 0) + coefficient
    return dict(sorted((residue, coefficient) for residue, coefficient in out.items() if coefficient))


def positive_residues(word: Word) -> tuple[int, ...]:
    return tuple(sorted(residue for residue, coefficient in word.items() if coefficient > 0))


def negative_residues(word: Word) -> tuple[int, ...]:
    return tuple(sorted(residue for residue, coefficient in word.items() if coefficient < 0))


def row_formula(pos: tuple[int, ...], neg: tuple[int, ...]) -> str:
    return (
        "prod_{a in "
        + str(pos)
        + ", k=0..12} E_{a+39k}^6 / prod_{b in "
        + str(neg)
        + ", k=0..12} E_{b+39k}^6"
    )


def profile_sparse_h90_product_normal_form() -> SparseH90ProductNormalFormProfile:
    selector_profile = profile_hilbert90_sparse_selector_structure()
    sparse_lift = profile_sparse_hilbert90_yang_lift()
    y507 = profile_yang_y507_primitive_factor_word()
    period_norm_word = period_norm(dict(y507.y507_primitive_word), SUPPORT_PERIOD)

    canonical_selector = selector_profile.legal_sparse_rows[0]
    canonical_source = gauge_word(canonical_selector.constants)
    canonical_lift = distribution_lift(canonical_source)
    subgroup = doubling_subgroup()
    stabilizer = tuple(
        multiplier
        for multiplier in subgroup
        if push_source_word(canonical_source, multiplier) == canonical_source
    )

    legal_words = {
        tuple(sorted(gauge_word(row.constants).items())): row
        for row in selector_profile.legal_sparse_rows
    }
    reps: list[int] = []
    seen_words: set[tuple[tuple[int, int], ...]] = set()
    for multiplier in subgroup:
        image = tuple(sorted(push_source_word(canonical_source, multiplier).items()))
        if image not in seen_words:
            reps.append(multiplier)
            seen_words.add(image)
    rows: list[SparseProductNormalFormRow] = []
    for multiplier in reps:
        image_source = push_source_word(canonical_source, multiplier)
        image_lift = distribution_lift(image_source)
        selector = legal_words[tuple(sorted(image_source.items()))]
        pushed_lift = push_lift_word(canonical_lift, multiplier)
        pos = positive_residues(image_source)
        neg = negative_residues(image_source)
        boundary_ok = boundary_507(image_lift) == period_norm_word
        row_ok = (
            selector.ok
            and image_lift == pushed_lift
            and len(pos) == 6
            and len(neg) == 6
            and sum(1 for coefficient in image_lift.values() if coefficient > 0) == 78
            and sum(1 for coefficient in image_lift.values() if coefficient < 0) == 78
            and len(image_lift) == 156
            and coefficient_counts(image_lift) == ((-6, 78), (6, 78))
            and boundary_ok
        )
        rows.append(
            SparseProductNormalFormRow(
                selector_name=selector.name,
                multiplier_from_canonical=multiplier,
                source_constants=selector.constants,
                source_positive_residues=pos,
                source_negative_residues=neg,
                source_positive_count=len(pos),
                source_negative_count=len(neg),
                lifted_positive_count=sum(1 for coefficient in image_lift.values() if coefficient > 0),
                lifted_negative_count=sum(1 for coefficient in image_lift.values() if coefficient < 0),
                lifted_support=len(image_lift),
                lifted_coefficient_counts=coefficient_counts(image_lift),
                boundary_equals_period_norm=boundary_ok,
                equals_multiplier_image_of_canonical=image_lift == pushed_lift,
                product_formula=row_formula(pos, neg),
                row_ok=row_ok,
            )
        )

    formal_rejected = (
        sparse_lift.formal_one_coset_lift_count == 2
        and sparse_lift.all_formal_lifts_have_nonzero_axis_pushforwards
    )
    one_orbit = (
        len(rows) == 4
        and len(stabilizer) == 3
        and len(subgroup) == 12
        and set(tuple(sorted(gauge_word(row.source_constants).items())) for row in rows)
        == set(legal_words)
    )
    products_78 = all(
        row.source_positive_count == 6
        and row.source_negative_count == 6
        and row.lifted_positive_count == 78
        and row.lifted_negative_count == 78
        for row in rows
    )
    direct_closer = False
    row_ok = (
        selector_profile.row_ok
        and sparse_lift.row_ok
        and y507.row_ok
        and CONDUCTOR == 39
        and QUOTIENT_LEVEL == 507
        and LIFT_LENGTH == 13
        and SUPPORT_PERIOD == 156
        and subgroup == (1, 2, 4, 8, 16, 32, 25, 11, 22, 5, 10, 20)
        and stabilizer == (1, 16, 22)
        and tuple(reps) == (1, 2, 4, 8)
        and positive_residues(canonical_source) == (7, 17, 23, 34, 37, 38)
        and negative_residues(canonical_source) == (4, 8, 10, 11, 20, 25)
        and one_orbit
        and products_78
        and formal_rejected
        and all(row.row_ok for row in rows)
        and not direct_closer
    )
    return SparseH90ProductNormalFormProfile(
        conductor=CONDUCTOR,
        target_level=QUOTIENT_LEVEL,
        lift_length=LIFT_LENGTH,
        support_period=SUPPORT_PERIOD,
        doubling_subgroup=subgroup,
        canonical_stabilizer=stabilizer,
        quotient_representatives=tuple(reps),
        canonical_positive_residues=positive_residues(canonical_source),
        canonical_negative_residues=negative_residues(canonical_source),
        canonical_positive_lift_count=sum(1 for coefficient in canonical_lift.values() if coefficient > 0),
        canonical_negative_lift_count=sum(1 for coefficient in canonical_lift.values() if coefficient < 0),
        legal_rows=tuple(rows),
        legal_rows_form_one_doubling_orbit=one_orbit,
        legal_rows_are_78_over_78_products=products_78,
        formal_one_coset_controls_rejected=formal_rejected,
        sparse_yang_lift_ok=sparse_lift.row_ok,
        direct_closer=direct_closer,
        positive_payload=(
            "The four legal support-156 potentials are one <2>-orbit of a "
            "canonical 78-over-78 Yang-fiber product, with stabilizer "
            "{1,16,22}."
        ),
        first_missing_clause=(
            "product normal form is still a theorem target, not a finite-field "
            "value/divisor theorem or DANGER3 extraction"
        ),
        recommendation=(
            "ask source/value theorems for the canonical 78-over-78 product or "
            "any of its <2>-translates; reject one-coset products and isolated "
            "boundary identities"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_sparse_h90_product_normal_form()
    print("p25 KSY-y Yang Y_507 sparse H90 product-normal-form gate")
    print(f"conductor={profile.conductor}")
    print(f"target_level={profile.target_level}")
    print(f"lift_length={profile.lift_length}")
    print(f"support_period={profile.support_period}")
    print(f"doubling_subgroup={profile.doubling_subgroup}")
    print(f"canonical_stabilizer={profile.canonical_stabilizer}")
    print(f"quotient_representatives={profile.quotient_representatives}")
    print("canonical")
    print(f"  positive_residues={profile.canonical_positive_residues}")
    print(f"  negative_residues={profile.canonical_negative_residues}")
    print(f"  positive_lift_count={profile.canonical_positive_lift_count}")
    print(f"  negative_lift_count={profile.canonical_negative_lift_count}")
    print("legal_product_rows")
    for row in profile.legal_rows:
        print(
            "  "
            f"name={row.selector_name} multiplier={row.multiplier_from_canonical} "
            f"constants={row.source_constants} pos={row.source_positive_residues} "
            f"neg={row.source_negative_residues} lift=+{row.lifted_positive_count}/"
            f"-{row.lifted_negative_count} support={row.lifted_support} "
            f"boundary_norm={int(row.boundary_equals_period_norm)} "
            f"mult_image={int(row.equals_multiplier_image_of_canonical)} "
            f"ok={int(row.row_ok)}"
        )
    print("checks")
    print(f"  legal_rows_form_one_doubling_orbit={int(profile.legal_rows_form_one_doubling_orbit)}")
    print(f"  legal_rows_are_78_over_78_products={int(profile.legal_rows_are_78_over_78_products)}")
    print(f"  formal_one_coset_controls_rejected={int(profile.formal_one_coset_controls_rejected)}")
    print(f"  sparse_yang_lift_ok={int(profile.sparse_yang_lift_ok)}")
    print(f"  direct_closer={int(profile.direct_closer)}")
    print("interpretation")
    print("  four_legal_support156_potentials_are_one_doubling_orbit=1")
    print("  canonical_target_is_a_78_over_78_Yang_fiber_product=1")
    print("  stabilizer_of_canonical_product_inside_<2>_has_order_3=1")
    print("  still_missing_value_or_divisor_theorem_and_DANGER3_extraction=1")
    print(
        "ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("sparse H90 product-normal-form regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

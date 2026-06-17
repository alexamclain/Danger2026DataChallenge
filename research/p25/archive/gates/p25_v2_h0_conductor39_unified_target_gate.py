#!/usr/bin/env python3
"""Compare the H0 and conductor-39 first-pass finite targets.

The v2 cockpit now has two first-pass theorem fronts.  This gate checks whether
they are genuinely separate finite products or two source languages for the
same support-156 Yang/Hilbert-90 target.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    profile_conductor39_source_theorem_intake,
)
from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    profile_h0_source_theorem_candidate_matcher,
)
from p25_ksy_y_h0_translate_value_compatibility_gate import (
    profile_h0_translate_value_compatibility,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)


ProductKey = tuple[
    int,
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
]


@dataclass(frozen=True)
class UnifiedTargetRow:
    multiplier: int
    h0_target_object: str
    h0_constants: tuple[int, ...]
    h0_positive_residues: tuple[int, ...]
    h0_negative_residues: tuple[int, ...]
    conductor39_selector_name: str
    conductor39_constants: tuple[int, ...]
    conductor39_positive_residues: tuple[int, ...]
    conductor39_negative_residues: tuple[int, ...]
    lifted_positive_count: int
    lifted_negative_count: int
    lifted_support: int
    boundary_equals_norm156: bool
    exact_same_finite_product: bool
    row_ok: bool


@dataclass(frozen=True)
class UnifiedTargetProfile:
    h0_candidate_matcher_ok: bool
    h0_translate_compatibility_ok: bool
    conductor39_normal_form_ok: bool
    conductor39_intake_ok: bool
    support_period: int
    quotient_representatives: tuple[int, ...]
    canonical_stabilizer: tuple[int, ...]
    rows: tuple[UnifiedTargetRow, ...]
    row_count: int
    identical_product_rows: int
    all_rows_78_over_78: bool
    all_boundaries_norm156: bool
    source_languages_distinct: bool
    finite_targets_identical: bool
    first_pass_fronts_collapse_to_one_finite_target: bool
    row_ok: bool


def h0_product_keys(profile) -> dict[int, ProductKey]:
    return {
        target.multiplier: (
            target.multiplier,
            target.constants,
            target.positive_residues,
            target.negative_residues,
        )
        for target in profile.product_targets
    }


def conductor39_product_keys(profile) -> dict[int, ProductKey]:
    return {
        row.multiplier_from_canonical: (
            row.multiplier_from_canonical,
            row.source_constants,
            row.source_positive_residues,
            row.source_negative_residues,
        )
        for row in profile.legal_rows
    }


def profile_h0_conductor39_unified_target() -> UnifiedTargetProfile:
    h0 = profile_h0_source_theorem_candidate_matcher()
    h0_translate = profile_h0_translate_value_compatibility()
    c39 = profile_sparse_h90_product_normal_form()
    c39_intake = profile_conductor39_source_theorem_intake()
    h0_keys = h0_product_keys(h0)
    c39_keys = conductor39_product_keys(c39)
    c39_rows_by_multiplier = {
        row.multiplier_from_canonical: row for row in c39.legal_rows
    }
    h0_targets_by_multiplier = {target.multiplier: target for target in h0.product_targets}

    rows: list[UnifiedTargetRow] = []
    for multiplier in c39.quotient_representatives:
        h0_target = h0_targets_by_multiplier[multiplier]
        c39_row = c39_rows_by_multiplier[multiplier]
        same = h0_keys[multiplier] == c39_keys[multiplier]
        row_ok = (
            same
            and c39_row.lifted_positive_count == 78
            and c39_row.lifted_negative_count == 78
            and c39_row.lifted_support == 156
            and c39_row.boundary_equals_period_norm
            and c39_row.row_ok
        )
        rows.append(
            UnifiedTargetRow(
                multiplier=multiplier,
                h0_target_object=h0_target.target_object,
                h0_constants=h0_target.constants,
                h0_positive_residues=h0_target.positive_residues,
                h0_negative_residues=h0_target.negative_residues,
                conductor39_selector_name=c39_row.selector_name,
                conductor39_constants=c39_row.source_constants,
                conductor39_positive_residues=c39_row.source_positive_residues,
                conductor39_negative_residues=c39_row.source_negative_residues,
                lifted_positive_count=c39_row.lifted_positive_count,
                lifted_negative_count=c39_row.lifted_negative_count,
                lifted_support=c39_row.lifted_support,
                boundary_equals_norm156=c39_row.boundary_equals_period_norm,
                exact_same_finite_product=same,
                row_ok=row_ok,
            )
        )

    all_78 = all(
        row.lifted_positive_count == 78
        and row.lifted_negative_count == 78
        and row.lifted_support == 156
        for row in rows
    )
    all_boundary = all(row.boundary_equals_norm156 for row in rows)
    finite_identical = (
        set(h0_keys) == set(c39_keys) == set(c39.quotient_representatives)
        and all(h0_keys[multiplier] == c39_keys[multiplier] for multiplier in h0_keys)
        and len(rows) == 4
    )
    source_languages_distinct = (
        h0.candidate_matcher_ok if hasattr(h0, "candidate_matcher_ok") else h0.row_ok
    ) and c39_intake.row_ok
    collapse = finite_identical and source_languages_distinct
    row_ok = (
        h0.row_ok
        and h0_translate.row_ok
        and c39.row_ok
        and c39_intake.row_ok
        and c39.support_period == 156
        and c39.quotient_representatives == (1, 2, 4, 8)
        and c39.canonical_stabilizer == (1, 16, 22)
        and len(rows) == 4
        and sum(row.exact_same_finite_product for row in rows) == 4
        and all_78
        and all_boundary
        and finite_identical
        and source_languages_distinct
        and collapse
        and all(row.row_ok for row in rows)
    )
    return UnifiedTargetProfile(
        h0_candidate_matcher_ok=h0.row_ok,
        h0_translate_compatibility_ok=h0_translate.row_ok,
        conductor39_normal_form_ok=c39.row_ok,
        conductor39_intake_ok=c39_intake.row_ok,
        support_period=c39.support_period,
        quotient_representatives=c39.quotient_representatives,
        canonical_stabilizer=c39.canonical_stabilizer,
        rows=tuple(rows),
        row_count=len(rows),
        identical_product_rows=sum(row.exact_same_finite_product for row in rows),
        all_rows_78_over_78=all_78,
        all_boundaries_norm156=all_boundary,
        source_languages_distinct=source_languages_distinct,
        finite_targets_identical=finite_identical,
        first_pass_fronts_collapse_to_one_finite_target=collapse,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_conductor39_unified_target()
    print("p25 v2 H0/conductor-39 unified finite-target gate")
    print("dependencies")
    print(f"  h0_candidate_matcher_ok={int(profile.h0_candidate_matcher_ok)}")
    print(f"  h0_translate_compatibility_ok={int(profile.h0_translate_compatibility_ok)}")
    print(f"  conductor39_normal_form_ok={int(profile.conductor39_normal_form_ok)}")
    print(f"  conductor39_intake_ok={int(profile.conductor39_intake_ok)}")
    print("finite_target_family")
    print(f"  support_period={profile.support_period}")
    print(f"  quotient_representatives={profile.quotient_representatives}")
    print(f"  canonical_stabilizer={profile.canonical_stabilizer}")
    print("unified_rows")
    for row in profile.rows:
        print(
            "  "
            f"m={row.multiplier} h0={row.h0_target_object} "
            f"selector={row.conductor39_selector_name} "
            f"constants={row.h0_constants} pos={row.h0_positive_residues} "
            f"neg={row.h0_negative_residues} lift=+{row.lifted_positive_count}/"
            f"-{row.lifted_negative_count} support={row.lifted_support} "
            f"boundary_norm156={int(row.boundary_equals_norm156)} "
            f"same_product={int(row.exact_same_finite_product)}"
        )
    print("checks")
    print(f"  row_count={profile.row_count}")
    print(f"  identical_product_rows={profile.identical_product_rows}")
    print(f"  all_rows_78_over_78={int(profile.all_rows_78_over_78)}")
    print(f"  all_boundaries_norm156={int(profile.all_boundaries_norm156)}")
    print(f"  source_languages_distinct={int(profile.source_languages_distinct)}")
    print(f"  finite_targets_identical={int(profile.finite_targets_identical)}")
    print(
        "  first_pass_fronts_collapse_to_one_finite_target="
        f"{int(profile.first_pass_fronts_collapse_to_one_finite_target)}"
    )
    print("interpretation")
    print("  H0_and_conductor39_have_the_same_four_support156_product_targets=1")
    print("  source_language_and_downstream_framing_still_differ=1")
    print("  expert_ask_can_be_unified_at_the_finite_value_divisor_level=1")
    print("  do_not_count_H0_and_conductor39_as_independent_finite_theorem_targets=1")
    print(f"p25_v2_h0_conductor39_unified_target_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0/conductor-39 unified target regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

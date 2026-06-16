#!/usr/bin/env python3
"""Actual-CM basis-free frequency-section audit.

The basis-free frequency gate says the p24 fixed determinant can be proved
from local projection ranks:

* ordinary frequencies: W_a -> prefix has full rank;
* defect frequencies: W_a -> prefix has rank four, while W_a -> prefix+tail
  has one extra rank;
* the defect support descends under Frobenius and has the selected tail size.

This audit does not try to prove p24 from the small uploaded rows.  It asks a
more useful question: when the current actual-CM rows fail the p24 profile,
which part fails?  The answer matters for the next theorem.  A support-size
failure says we need a new arithmetic selector theorem; a Frobenius-covariance
failure would invalidate the cyclic-resultant packaging.
"""

from __future__ import annotations

from dataclasses import dataclass

from trace_gcd_actual_cm_frequency_defect_boundary import (
    ActualFrequencyDefectRow,
    rows_for_case,
)
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase


@dataclass(frozen=True)
class BasisFreeSectionRow:
    label: str
    D: int
    q: int
    right_len: int
    omitted: int
    prefix_blocks: int
    tail_dim: int
    selected_full: bool
    tail_residue_list: tuple[int, ...]
    prefix_defect_list: tuple[int, ...]
    tail_residue_stable: bool
    prefix_defect_stable: bool
    rank_profile_frobenius_covariant: bool
    support_size_matches_tail_dim: bool
    basis_free_section_candidate: bool
    failure_mode: str


def stable_support(support: set[int], multiplier: int, modulus: int) -> bool:
    return {(multiplier * value) % modulus for value in support} == support


def frequency_class(row: ActualFrequencyDefectRow, frequency: int) -> str:
    if frequency in row.prefix_defect_list:
        return "prefix_defect"
    if frequency in row.tail_residue_list:
        return "tail_jump"
    return "tail_inside_prefix"


def rank_profile_frobenius_covariant(row: ActualFrequencyDefectRow) -> bool:
    multiplier = row.q % row.right_len
    return all(
        frequency_class(row, (multiplier * frequency) % row.right_len)
        == frequency_class(row, frequency)
        for frequency in range(row.right_len)
    )


def failure_mode(row: ActualFrequencyDefectRow) -> str:
    if row.prefix_blocks <= 0:
        return "tail_only_no_prefix"
    if row.tail_dim <= 0:
        return "no_selected_tail_window"
    if row.prefix_defect_frequencies:
        return "prefix_rank_defect"
    if row.tail_residue_frequencies != row.tail_dim:
        return "wrong_defect_support_size"
    if not stable_support(set(row.tail_residue_list), row.q % row.right_len, row.right_len):
        return "defect_support_not_frobenius_stable"
    if not row.selected_full:
        return "selected_rank_not_full"
    return "candidate"


def analyze_row(row: ActualFrequencyDefectRow) -> BasisFreeSectionRow:
    tail_support = set(row.tail_residue_list)
    prefix_defects = set(row.prefix_defect_list)
    multiplier = row.q % row.right_len
    tail_stable = stable_support(tail_support, multiplier, row.right_len)
    prefix_stable = stable_support(prefix_defects, multiplier, row.right_len)
    covariant = rank_profile_frobenius_covariant(row)
    size_match = row.tail_residue_frequencies == row.tail_dim
    mode = failure_mode(row)
    return BasisFreeSectionRow(
        label=row.label,
        D=row.D,
        q=row.q,
        right_len=row.right_len,
        omitted=row.omitted,
        prefix_blocks=row.prefix_blocks,
        tail_dim=row.tail_dim,
        selected_full=row.selected_full,
        tail_residue_list=row.tail_residue_list,
        prefix_defect_list=row.prefix_defect_list,
        tail_residue_stable=tail_stable,
        prefix_defect_stable=prefix_stable,
        rank_profile_frobenius_covariant=covariant,
        support_size_matches_tail_dim=size_match,
        basis_free_section_candidate=(mode == "candidate"),
        failure_mode=mode,
    )


def main() -> None:
    cases = [
        RowspaceCase("pinned_tail_only_full_rank", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout_tail_only_full_rank", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_tail_only_full_rank", -4319, 4463, 28, 4, 7),
        RowspaceCase("actual_prefix_plus_tail_singular", -15791, 40127, 65, 5, 13),
    ]
    rows = [
        analyze_row(row)
        for case in cases
        for row in rows_for_case(case)
    ]
    print("Trace-GCD actual-CM basis-free frequency-section audit")
    print(
        "columns: label D q right_len omitted prefix_blocks tail_dim "
        "selected_full tail_residue_list prefix_defect_list "
        "tail_residue_stable prefix_defect_stable "
        "rank_profile_frobenius_covariant support_size_matches_tail_dim "
        "basis_free_section_candidate failure_mode"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} "
            f"right_len={row.right_len} omitted={row.omitted} "
            f"prefix_blocks={row.prefix_blocks} tail_dim={row.tail_dim} "
            f"selected_full={int(row.selected_full)} "
            f"tail_residue_list={list(row.tail_residue_list)} "
            f"prefix_defect_list={list(row.prefix_defect_list)} "
            f"tail_residue_stable={int(row.tail_residue_stable)} "
            f"prefix_defect_stable={int(row.prefix_defect_stable)} "
            "rank_profile_frobenius_covariant="
            f"{int(row.rank_profile_frobenius_covariant)} "
            f"support_size_matches_tail_dim={int(row.support_size_matches_tail_dim)} "
            f"basis_free_section_candidate={int(row.basis_free_section_candidate)} "
            f"failure_mode={row.failure_mode}"
        )

    prefix_tail_rows = [
        row for row in rows if row.prefix_blocks > 0 and row.tail_dim > 0
    ]
    covariant_rows = [row for row in rows if row.rank_profile_frobenius_covariant]
    candidate_rows = [row for row in rows if row.basis_free_section_candidate]
    wrong_size_prefix_tail = [
        row for row in prefix_tail_rows if row.failure_mode == "wrong_defect_support_size"
    ]
    nonstable_rows = [
        row for row in rows
        if not row.tail_residue_stable or not row.prefix_defect_stable
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  prefix_tail_rows={len(prefix_tail_rows)}/{len(rows)}")
    print(f"  rank_profile_frobenius_covariant_rows={len(covariant_rows)}/{len(rows)}")
    print(f"  nonstable_support_rows={len(nonstable_rows)}/{len(rows)}")
    print(f"  basis_free_section_candidate_rows={len(candidate_rows)}/{len(rows)}")
    print(
        "  prefix_tail_wrong_defect_size_rows="
        f"{len(wrong_size_prefix_tail)}/{len(prefix_tail_rows)}"
    )
    print("interpretation")
    print("  actual_cm_basis_free_profile_measured=1")
    print(
        "  current_actual_rows_do_not_supply_basis_free_section_candidate="
        f"{int(len(candidate_rows) == 0)}"
    )
    print(
        "  prefix_tail_rows_have_wrong_defect_size="
        f"{int(prefix_tail_rows and len(wrong_size_prefix_tail) == len(prefix_tail_rows))}"
    )
    print(
        "  obstruction_is_defect_support_size_not_descent="
        f"{int(len(covariant_rows) == len(rows) and len(wrong_size_prefix_tail) == len(prefix_tail_rows))}"
    )
    print("conclusion=reported_trace_gcd_actual_cm_basis_free_section_audit")

    if not rows or not prefix_tail_rows:
        raise SystemExit(1)
    if len(covariant_rows) != len(rows):
        raise SystemExit(1)
    if candidate_rows:
        raise SystemExit(1)
    if len(wrong_size_prefix_tail) != len(prefix_tail_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Actual-CM boundary audit for the RS-tail frequency-defect gate.

The p24 frequency-defect theorem would prove the selected `140+16` determinant
before forming the full Plucker chart.  After diagonalizing the common right
cyclic/Lang shift, the required local profile is:

* every frequency has full prefix projection;
* exactly `tail_dim` frequencies have a one-dimensional tail residue modulo the
  prefix projection;
* the remaining frequencies have the tail coordinate inside the prefix image.

This audit applies that diagnostic to the bounded actual-CM rows already used
by the Gaussian/RS-tail and full-chart boundary audits.  The current rows are
not expected to prove the p24 theorem: tail-only rows do not have a prefix, and
the nontrivial prefix-plus-tail rows are singular controls.  The point is to
localize which frequency-defect hypothesis fails instead of treating the rank
failure as opaque.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from k_character_tensor_rank_scan import primitive_root_of_order
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_actual_cm_full_plucker_chart_boundary import (
    all_transformed_blocks,
    selected_and_omitted_columns,
)
from trace_gcd_full_gaussian_rs_tail_toy import spectral_component
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED
from trace_gcd_residual_prefix_tail_bridge_audit import split_prefix_len


@dataclass(frozen=True)
class ActualFrequencyDefectRow:
    label: str
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    left_orbit: tuple[int, ...]
    omitted: int
    right_len: int
    k_degree: int
    block_count: int
    source_dim: int
    prefix_blocks: int
    tail_dim: int
    selected_rank: int
    selected_full: bool
    prefix_full_frequencies: int
    tail_residue_frequencies: int
    tail_inside_prefix_frequencies: int
    prefix_defect_frequencies: int
    frequency_profile_gate: bool
    clean_p24_like_shape: bool
    tail_residue_list: tuple[int, ...]
    prefix_defect_list: tuple[int, ...]


def rank_values(values: list[tuple[int, ...]], q: int) -> int:
    if not values:
        return 0
    return rank_mod_q([list(value) for value in values], q)


def first_component_spectrum(values, omega, field) -> list[tuple[int, ...]]:
    return [
        spectral_component(values, frequency, 0, omega, field)
        for frequency in range(len(values))
    ]


def rows_for_case(case: RowspaceCase) -> list[ActualFrequencyDefectRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[ActualFrequencyDefectRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        all_blocks = all_transformed_blocks(
            dft_matrix,
            left_orbit,
            right_orbits,
            case.left,
            case.right,
            case.q,
            field,
        )
        lengths = [len(block) for block in all_blocks]
        if not lengths or len(set(lengths)) != 1:
            continue
        right_len = lengths[0]
        k_degree = int(sp.n_order(case.q % right_len, right_len))
        omega = primitive_root_of_order(field, right_len, SEED + 705)
        spectra = [
            first_component_spectrum(block, omega, field)
            for block in all_blocks
        ]
        for omitted in range(len(right_orbits)):
            selected, _omitted_columns, _right_len, prefix_blocks, tail_dim = (
                selected_and_omitted_columns(
                    all_blocks,
                    omitted,
                    source_dim,
                    right_orbits,
                )
            )
            if not selected or right_len != _right_len:
                continue
            prefix_len = split_prefix_len(right_orbits, omitted, source_dim)
            if prefix_len % right_len:
                continue
            kept_indices = [
                index for index in range(len(all_blocks)) if index != omitted
            ]
            if prefix_blocks >= len(kept_indices):
                continue
            prefix_indices = kept_indices[:prefix_blocks]
            tail_index = kept_indices[prefix_blocks]

            prefix_full_frequencies = 0
            tail_residue_frequencies: list[int] = []
            tail_inside_prefix_frequencies = 0
            prefix_defect_frequencies: list[int] = []
            for frequency in range(right_len):
                prefix_values = [
                    spectra[index][frequency] for index in prefix_indices
                ]
                tail_value = spectra[tail_index][frequency]
                prefix_rank = rank_values(prefix_values, case.q)
                prefix_tail_rank = rank_values(prefix_values + [tail_value], case.q)
                if prefix_rank == prefix_blocks:
                    prefix_full_frequencies += 1
                    if prefix_tail_rank == prefix_rank + 1:
                        tail_residue_frequencies.append(frequency)
                    elif prefix_tail_rank == prefix_rank:
                        tail_inside_prefix_frequencies += 1
                else:
                    prefix_defect_frequencies.append(frequency)

            selected_rank = rank_values(selected, case.q)
            profile_gate = (
                prefix_full_frequencies == right_len
                and len(tail_residue_frequencies) == tail_dim
                and tail_inside_prefix_frequencies == right_len - tail_dim
            )
            clean_shape = (
                prefix_blocks > 0
                and tail_dim > 0
                and len(all_blocks) == prefix_blocks + 2
            )
            rows.append(
                ActualFrequencyDefectRow(
                    label=case.label,
                    D=case.D,
                    q=case.q,
                    h=h,
                    m=case.m,
                    n=n,
                    factor_degree=factor.degree(),
                    left=case.left,
                    right=case.right,
                    left_orbit=tuple(left_orbit),
                    omitted=omitted,
                    right_len=right_len,
                    k_degree=k_degree,
                    block_count=len(all_blocks),
                    source_dim=source_dim,
                    prefix_blocks=prefix_blocks,
                    tail_dim=tail_dim,
                    selected_rank=selected_rank,
                    selected_full=(selected_rank == source_dim),
                    prefix_full_frequencies=prefix_full_frequencies,
                    tail_residue_frequencies=len(tail_residue_frequencies),
                    tail_inside_prefix_frequencies=tail_inside_prefix_frequencies,
                    prefix_defect_frequencies=len(prefix_defect_frequencies),
                    frequency_profile_gate=profile_gate,
                    clean_p24_like_shape=clean_shape,
                    tail_residue_list=tuple(tail_residue_frequencies),
                    prefix_defect_list=tuple(prefix_defect_frequencies),
                )
            )
    return rows


def main() -> None:
    cases = [
        RowspaceCase("pinned_tail_only_full_rank", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout_tail_only_full_rank", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_tail_only_full_rank", -4319, 4463, 28, 4, 7),
        RowspaceCase("actual_prefix_plus_tail_singular", -15791, 40127, 65, 5, 13),
    ]
    rows = [row for case in cases for row in rows_for_case(case)]
    print("Trace-GCD actual-CM frequency-defect boundary audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "right_len k_degree block_count source_dim prefix_blocks tail_dim "
        "selected_rank selected_full prefix_full_frequencies "
        "tail_residue_frequencies tail_inside_prefix_frequencies "
        "prefix_defect_frequencies frequency_profile_gate clean_p24_like_shape "
        "tail_residue_list prefix_defect_list"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} right_len={row.right_len} "
            f"k_degree={row.k_degree} block_count={row.block_count} "
            f"source_dim={row.source_dim} prefix_blocks={row.prefix_blocks} "
            f"tail_dim={row.tail_dim} selected_rank={row.selected_rank} "
            f"selected_full={int(row.selected_full)} "
            f"prefix_full_frequencies={row.prefix_full_frequencies} "
            f"tail_residue_frequencies={row.tail_residue_frequencies} "
            f"tail_inside_prefix_frequencies={row.tail_inside_prefix_frequencies} "
            f"prefix_defect_frequencies={row.prefix_defect_frequencies} "
            f"frequency_profile_gate={int(row.frequency_profile_gate)} "
            f"clean_p24_like_shape={int(row.clean_p24_like_shape)} "
            f"tail_residue_list={list(row.tail_residue_list)} "
            f"prefix_defect_list={list(row.prefix_defect_list)}"
        )

    clean_rows = [row for row in rows if row.clean_p24_like_shape]
    profile_rows = [row for row in rows if row.frequency_profile_gate]
    selected_full_rows = [row for row in rows if row.selected_full]
    prefix_tail_rows = [
        row for row in rows if row.prefix_blocks > 0 and row.tail_dim > 0
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  clean_p24_like_shape_rows={len(clean_rows)}/{len(rows)}")
    print(f"  frequency_profile_gate_rows={len(profile_rows)}/{len(rows)}")
    print(f"  selected_full_rows={len(selected_full_rows)}/{len(rows)}")
    print(f"  prefix_tail_rows={len(prefix_tail_rows)}/{len(rows)}")
    print("interpretation")
    print("  actual_cm_frequency_profile_columns_measured=1")
    print("  tail_only_rows_are_not_frequency_defect_calibrations=1")
    print("  prefix_plus_tail_singular_rows_fail_local_frequency_gate=1")
    print("  p24_frequency_defect_punit_theorem_still_needs_new_arithmetic=1")
    print("conclusion=reported_trace_gcd_actual_cm_frequency_defect_boundary")

    if not rows or not prefix_tail_rows:
        raise SystemExit(1)
    if not any(not row.frequency_profile_gate for row in prefix_tail_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

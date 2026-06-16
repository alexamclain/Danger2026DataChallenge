#!/usr/bin/env python3
"""Actual-CM audit for the RS-tail Hilbert-90 fixed-relation map.

The p24 fixed square determinant is now phrased as the determinant of

    Psi_RS : F_p^28 + K^28 + F_p^16 -> L.

This audit checks the same finite rewrite on bounded actual-CM rows.  Starting
from the actual Lang blocks used by the Gaussian/RS-tail audit, it builds the
first-component spectral table and then the explicit Hilbert-90 fixed columns:

* fixed-frequency prefix columns `V_{a,j}`;
* length-orbit linearized prefix columns
  `sum_r kappa^(q^r) V_{q^r a,j}`;
* RS-tail columns `sum_a omega^(a*s) V_{a,tail}`.

The rank of these columns should match the original time-domain square map.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import FpE, primitive_root_of_order
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_actual_cm_gaussian_rs_tail_audit import (
    transformed_kept_blocks,
)
from trace_gcd_full_gaussian_rs_tail_toy import spectral_component
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED
from trace_gcd_residual_prefix_tail_bridge_audit import split_prefix_len


@dataclass(frozen=True)
class ActualRsTailSemilinearCoreRow:
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
    source_dim: int
    prefix_blocks: int
    tail_dim: int
    fixed_frequency_count: int
    moving_frequency_orbit_count: int
    fixed_prefix_columns: int
    moving_prefix_columns: int
    tail_columns: int
    explicit_column_count: int
    prefix_rank: int
    tail_quotient_rank: int
    time_rank: int
    psi_rank: int
    rank_match: bool
    full_rank: bool
    prefix_full: bool
    tail_quotient_full: bool


def frequency_orbits(length: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(length):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = (multiplier * current) % length
        out.append(orbit)
    return out


def rank_values(values: list[FpE], q: int) -> int:
    if not values:
        return 0
    return rank_mod_q([list(value) for value in values], q)


def add_many(values: list[FpE], field) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def first_component_spectrum(
    values: list[FpE],
    omega: FpE,
    field,
) -> list[FpE]:
    return [
        spectral_component(values, frequency, 0, omega, field)
        for frequency in range(len(values))
    ]


def explicit_fixed_relation_columns(
    prefix_values: list[list[FpE]],
    tail_values: list[FpE],
    tail_dim: int,
    k_basis: list[FpE],
    omega: FpE,
    q: int,
    field,
) -> tuple[list[FpE], int, int, int, int, int]:
    right_len = len(tail_values)
    prefix_spectra = [
        first_component_spectrum(block, omega, field)
        for block in prefix_values
    ]
    tail_spectrum = first_component_spectrum(tail_values, omega, field)
    orbits = frequency_orbits(right_len, q % right_len)

    columns: list[FpE] = []
    fixed_frequency_count = 0
    moving_frequency_orbit_count = 0
    fixed_prefix_columns = 0
    moving_prefix_columns = 0

    for orbit in orbits:
        if len(orbit) == 1:
            fixed_frequency_count += 1
            frequency = orbit[0]
            for block_spectrum in prefix_spectra:
                columns.append(block_spectrum[frequency])
                fixed_prefix_columns += 1
            continue
        moving_frequency_orbit_count += 1
        representative = orbit[0]
        for block_spectrum in prefix_spectra:
            for kappa in k_basis:
                terms: list[FpE] = []
                for step in range(len(orbit)):
                    frequency = (pow(q, step, right_len) * representative) % right_len
                    coeff = field.pow(kappa, q**step)
                    terms.append(field.mul(coeff, block_spectrum[frequency]))
                columns.append(add_many(terms, field))
                moving_prefix_columns += 1

    tail_columns = 0
    for tail_pos in range(tail_dim):
        terms = [
            field.mul(
                field.pow(omega, frequency * tail_pos),
                tail_spectrum[frequency],
            )
            for frequency in range(right_len)
        ]
        columns.append(add_many(terms, field))
        tail_columns += 1

    return (
        columns,
        fixed_frequency_count,
        moving_frequency_orbit_count,
        fixed_prefix_columns,
        moving_prefix_columns,
        tail_columns,
    )


def rows_for_case(case: RowspaceCase) -> list[ActualRsTailSemilinearCoreRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[ActualRsTailSemilinearCoreRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        for omitted in range(len(right_orbits)):
            blocks = transformed_kept_blocks(
                dft_matrix,
                left_orbit,
                right_orbits,
                omitted,
                case.left,
                case.right,
                case.q,
                field,
            )
            lengths = [len(block) for block in blocks]
            if len(set(lengths)) != 1:
                continue
            right_len = lengths[0]
            if sum(lengths) < source_dim:
                continue
            prefix_len = split_prefix_len(right_orbits, omitted, source_dim)
            if prefix_len % right_len:
                continue
            prefix_blocks = prefix_len // right_len
            tail_dim = source_dim - prefix_len
            if tail_dim <= 0 or prefix_blocks >= len(blocks):
                continue
            k_degree = int(sp.n_order(case.q % right_len, right_len))
            if field.degree % k_degree:
                continue
            k_basis = subfield_power_basis(case.q, k_degree, field, SEED + 504)
            omega = primitive_root_of_order(field, right_len, SEED + 505)
            prefix_values = blocks[:prefix_blocks]
            tail_values = blocks[prefix_blocks]
            time_columns = [
                value for block in prefix_values for value in block
            ] + tail_values[:tail_dim]
            time_rank = rank_values(time_columns, case.q)
            (
                psi_columns,
                fixed_frequency_count,
                moving_frequency_orbit_count,
                fixed_prefix_columns,
                moving_prefix_columns,
                tail_columns,
            ) = explicit_fixed_relation_columns(
                prefix_values,
                tail_values,
                tail_dim,
                k_basis,
                omega,
                case.q,
                field,
            )
            prefix_column_count = fixed_prefix_columns + moving_prefix_columns
            prefix_columns = psi_columns[:prefix_column_count]
            prefix_rank = rank_values(prefix_columns, case.q)
            psi_rank = rank_values(psi_columns, case.q)
            tail_quotient_rank = psi_rank - prefix_rank
            rows.append(
                ActualRsTailSemilinearCoreRow(
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
                    source_dim=source_dim,
                    prefix_blocks=prefix_blocks,
                    tail_dim=tail_dim,
                    fixed_frequency_count=fixed_frequency_count,
                    moving_frequency_orbit_count=moving_frequency_orbit_count,
                    fixed_prefix_columns=fixed_prefix_columns,
                    moving_prefix_columns=moving_prefix_columns,
                    tail_columns=tail_columns,
                    explicit_column_count=len(psi_columns),
                    prefix_rank=prefix_rank,
                    tail_quotient_rank=tail_quotient_rank,
                    time_rank=time_rank,
                    psi_rank=psi_rank,
                    rank_match=time_rank == psi_rank,
                    full_rank=time_rank == source_dim,
                    prefix_full=prefix_rank == prefix_column_count,
                    tail_quotient_full=tail_quotient_rank == tail_columns,
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
    print("Trace-GCD actual-CM RS-tail semilinear-core audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "right_len k_degree source_dim prefix_blocks tail_dim fixed_freqs "
        "moving_freq_orbits fixed_prefix_cols moving_prefix_cols tail_cols "
        "explicit_cols prefix_rank tail_quotient_rank time_rank psi_rank "
        "rank_match full_rank prefix_full tail_quotient_full"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} right_len={row.right_len} "
            f"k_degree={row.k_degree} source_dim={row.source_dim} "
            f"prefix_blocks={row.prefix_blocks} tail_dim={row.tail_dim} "
            f"fixed_freqs={row.fixed_frequency_count} "
            f"moving_freq_orbits={row.moving_frequency_orbit_count} "
            f"fixed_prefix_cols={row.fixed_prefix_columns} "
            f"moving_prefix_cols={row.moving_prefix_columns} "
            f"tail_cols={row.tail_columns} "
            f"explicit_cols={row.explicit_column_count} "
            f"prefix_rank={row.prefix_rank} "
            f"tail_quotient_rank={row.tail_quotient_rank} "
            f"time_rank={row.time_rank} psi_rank={row.psi_rank} "
            f"rank_match={int(row.rank_match)} full_rank={int(row.full_rank)} "
            f"prefix_full={int(row.prefix_full)} "
            f"tail_quotient_full={int(row.tail_quotient_full)}"
        )

    rank_failures = [row for row in rows if not row.rank_match]
    count_failures = [row for row in rows if row.explicit_column_count != row.source_dim]
    full_rows = [row for row in rows if row.full_rank]
    singular_rows = [row for row in rows if not row.full_rank]
    prefix_tail_rows = [
        row for row in rows if row.prefix_blocks > 0 and row.tail_dim > 0
    ]
    prefix_failures = [row for row in prefix_tail_rows if not row.prefix_full]
    tail_quotient_failures = [
        row for row in prefix_tail_rows if not row.tail_quotient_full
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  explicit_column_count_mismatches={len(count_failures)}")
    print(f"  rank_mismatches={len(rank_failures)}")
    print(f"  full_rank_rows={len(full_rows)}/{len(rows)}")
    print(f"  singular_control_rows={len(singular_rows)}/{len(rows)}")
    print(f"  actual_prefix_plus_tail_rows={len(prefix_tail_rows)}/{len(rows)}")
    print(f"  prefix_failures_on_prefix_tail_rows={len(prefix_failures)}")
    print(
        "  tail_quotient_failures_on_prefix_tail_rows="
        f"{len(tail_quotient_failures)}"
    )
    print("interpretation")
    print("  actual_cm_rs_tail_fixed_columns_match_time_rank=1")
    print("  actual_cm_hilbert90_fixed_relation_shape_survives=1")
    print("  actual_cm_rs_tail_schur_split_measured=1")
    print("  actual_cm_prefix_plus_tail_singular_control_detected=1")
    print("conclusion=reported_trace_gcd_actual_cm_rs_tail_semilinear_core_audit")

    if (
        not rows
        or rank_failures
        or count_failures
        or not full_rows
        or not singular_rows
        or not prefix_tail_rows
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

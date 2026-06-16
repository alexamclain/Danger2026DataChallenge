#!/usr/bin/env python3
"""Actual-CM audit for the Gaussian-DFT/RS-tail full coinvariant form.

The square coinvariant map uses full right-orbit blocks for the prefix and a
truncated tail window.  For a right Lang block of length `r`, scalar extension
to `K = F_q(mu_r)` diagonalizes full blocks by a length-`r` DFT.  A truncated
tail of length `s < r` becomes the Reed-Solomon subspace spanned by the first
`s` inverse-DFT rows.

This audit applies that finite identity to small actual-CM rows, including
the nontrivial-prefix singular row with shape `4 = 3 + 1`.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import primitive_root_of_order
from trace_gcd_full_gaussian_rs_tail_toy import audit_tuple
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED
from trace_gcd_residual_prefix_tail_bridge_audit import split_prefix_len


@dataclass(frozen=True)
class ActualGaussianRsTailRow:
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
    time_rank: int
    spectral_k_rank: int
    tail_reconstruction_failures: int
    rank_match: bool
    full_rank: bool


def transformed_kept_blocks(
    dft_matrix,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    omitted: int,
    left: int,
    right: int,
    q: int,
    field,
) -> list[list]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    kept = [orbit for index, orbit in enumerate(right_orbits) if index != omitted]
    blocks: list[list] = []
    inverses: dict[int, list[list]] = {}
    for orbit in kept:
        orbit_len = len(orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(q, orbit_len, field, SEED)
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in orbit
        ]
        blocks.append(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return blocks


def rows_for_case(case: RowspaceCase) -> list[ActualGaussianRsTailRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[ActualGaussianRsTailRow] = []
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
            k_basis = subfield_power_basis(case.q, k_degree, field, SEED + 404)
            omega = primitive_root_of_order(field, right_len, SEED + 405)
            prefix_values = blocks[:prefix_blocks]
            tail_values = blocks[prefix_blocks]
            toy_row = audit_tuple(
                case.label,
                prefix_values,
                tail_values,
                tail_dim,
                k_basis,
                omega,
                field,
            )
            rows.append(
                ActualGaussianRsTailRow(
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
                    time_rank=toy_row.time_rank,
                    spectral_k_rank=toy_row.spectral_k_rank,
                    tail_reconstruction_failures=toy_row.tail_reconstruction_failures,
                    rank_match=toy_row.rank_match,
                    full_rank=toy_row.full_rank,
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
    print("Trace-GCD actual-CM Gaussian DFT / RS-tail audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted right_len "
        "k_degree source_dim prefix_blocks tail_dim time_rank spectral_k_rank "
        "tail_reconstruction_failures rank_match full_rank"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} right_len={row.right_len} "
            f"k_degree={row.k_degree} source_dim={row.source_dim} "
            f"prefix_blocks={row.prefix_blocks} tail_dim={row.tail_dim} "
            f"time_rank={row.time_rank} spectral_k_rank={row.spectral_k_rank} "
            f"tail_reconstruction_failures={row.tail_reconstruction_failures} "
            f"rank_match={int(row.rank_match)} full_rank={int(row.full_rank)}"
        )
    rank_failures = [row for row in rows if not row.rank_match]
    reconstruction_failures = sum(row.tail_reconstruction_failures for row in rows)
    full_rows = [row for row in rows if row.full_rank]
    singular_rows = [row for row in rows if not row.full_rank]
    prefix_tail_rows = [
        row for row in rows if row.prefix_blocks > 0 and row.tail_dim > 0
    ]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  rank_mismatches={len(rank_failures)}")
    print(f"  tail_reconstruction_failures={reconstruction_failures}")
    print(f"  full_rank_rows={len(full_rows)}/{len(rows)}")
    print(f"  singular_control_rows={len(singular_rows)}/{len(rows)}")
    print(f"  actual_prefix_plus_tail_rows={len(prefix_tail_rows)}/{len(rows)}")
    print("interpretation")
    print("  actual_cm_lang_blocks_match_gaussian_dft_rs_tail_rank=1")
    print("  actual_cm_prefix_plus_tail_singular_control_detected=1")
    print("conclusion=reported_trace_gcd_actual_cm_gaussian_rs_tail_audit")

    if (
        not rows
        or rank_failures
        or reconstruction_failures
        or not full_rows
        or not singular_rows
        or not prefix_tail_rows
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Actual-CM bridge for the square coinvariant trace-GCD target.

The proof-facing fixed-orbit target is the square map

    Phi_full : R^k + C_tail -> E/(tau_R - 1)E.

After Lang trivialization and the trace quotient
`E/(tau_R - 1)E ~= L`, this map is represented by the selected leading
coordinates `c_i in L`: the coordinate-basis vector `e_i` maps to `c_i`.
The trace-GCD matrix is the trace adjoint

    B_ij = Tr_{L/F_q}(lambda_j * c_i).

This audit checks the exact determinant-line relation on small actual-CM
rows:

    det(B) = det(Phi_full) * det(Tr(lambda_i lambda_j))

and verifies that the square coinvariant determinant, trace-pairing
determinant, and residual prefix/tail product have the same zero event.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    subfield_power_basis,
)
from kernel_tail_schur_identity_toy import det_mod
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED
from trace_gcd_prefix_adjoint_trace_toy import coordinate_vector, trace_to_base
from trace_gcd_residual_prefix_tail_bridge_audit import (
    audit_coordinates,
    leading_coordinates,
    split_prefix_len,
)


@dataclass(frozen=True)
class ActualSquareCoinvariantRow:
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
    source_dim: int
    prefix_len: int
    tail_len: int
    coord_rank: int
    coinvariant_rank: int
    trace_rank: int
    prefix_rank: int
    tail_pivots: int
    coinvariant_det: int | None
    trace_det: int | None
    trace_gram_det: int | None
    full_product: int | None
    prefix_product: int | None
    tail_product: int | None
    trace_det_matches_gram_twist: bool
    nonzero_events_match: bool
    prefix_tail_event_match: bool


def transpose(columns: list[list[int]]) -> list[list[int]]:
    if not columns:
        return []
    return [
        [columns[col][row] for col in range(len(columns))]
        for row in range(len(columns[0]))
    ]


def trace_pairing_matrix(coords, basis, degree: int, field) -> list[list[int]]:
    return [
        [
            trace_to_base(field.mul(lam, coord), degree, field)
            for lam in basis
        ]
        for coord in coords
    ]


def trace_gram_matrix(basis, degree: int, field) -> list[list[int]]:
    return [
        [
            trace_to_base(field.mul(left, right), degree, field)
            for right in basis
        ]
        for left in basis
    ]


def square_coinvariant_rows_for_case(
    case: RowspaceCase,
) -> list[ActualSquareCoinvariantRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[ActualSquareCoinvariantRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        basis = subfield_power_basis(case.q, source_dim, field, SEED + 157)
        basis_inverse = lang_inverse_for_orbit(case.q, source_dim, field, SEED + 157)
        gram_det = det_mod(trace_gram_matrix(basis, source_dim, field), case.q)
        for omitted in range(len(right_orbits)):
            coords = leading_coordinates(
                dft_matrix,
                left_orbit,
                right_orbits,
                omitted,
                case.left,
                case.right,
                source_dim,
                case.q,
                field,
            )
            if len(coords) < source_dim:
                continue

            prefix_len = split_prefix_len(right_orbits, omitted, source_dim)
            prefix_tail = audit_coordinates(
                case.label,
                coords,
                prefix_len,
                source_dim,
                field,
                D=case.D,
                h=h,
                m=case.m,
                n=n,
                factor_degree=factor.degree(),
                left=case.left,
                right=case.right,
                left_orbit=tuple(left_orbit),
                omitted=omitted,
            )
            coord_columns = [
                coordinate_vector(coord, source_dim, basis_inverse, field)
                for coord in coords
            ]
            coinvariant_matrix = transpose(coord_columns)
            coinvariant_rank = rank_mod_q(coinvariant_matrix, case.q)
            coinvariant_det = det_mod(coinvariant_matrix, case.q)
            trace_matrix = trace_pairing_matrix(coords, basis, source_dim, field)
            trace_rank = rank_mod_q(trace_matrix, case.q)
            trace_det = det_mod(trace_matrix, case.q)
            coord_rank = fq_rank(coords, case.q)
            gram_relation = (
                coinvariant_det is not None
                and trace_det is not None
                and gram_det is not None
                and trace_det % case.q == (coinvariant_det * gram_det) % case.q
            )
            coinvariant_nonzero = (
                coinvariant_det is not None and coinvariant_det % case.q != 0
            )
            trace_nonzero = trace_det is not None and trace_det % case.q != 0
            residual_nonzero = (
                prefix_tail.full_product is not None
                and prefix_tail.full_product % case.q != 0
            )
            rows.append(
                ActualSquareCoinvariantRow(
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
                    source_dim=source_dim,
                    prefix_len=prefix_tail.prefix_len,
                    tail_len=prefix_tail.tail_len,
                    coord_rank=coord_rank,
                    coinvariant_rank=coinvariant_rank,
                    trace_rank=trace_rank,
                    prefix_rank=prefix_tail.prefix_rank,
                    tail_pivots=prefix_tail.tail_pivots,
                    coinvariant_det=coinvariant_det,
                    trace_det=trace_det,
                    trace_gram_det=gram_det,
                    full_product=prefix_tail.full_product,
                    prefix_product=prefix_tail.prefix_product,
                    tail_product=prefix_tail.tail_product,
                    trace_det_matches_gram_twist=gram_relation,
                    nonzero_events_match=(
                        coord_rank == coinvariant_rank == trace_rank
                        and (coord_rank == source_dim)
                        == coinvariant_nonzero
                        == trace_nonzero
                        == residual_nonzero
                    ),
                    prefix_tail_event_match=prefix_tail.event_match,
                )
            )
    return rows


def main() -> None:
    cases = [
        RowspaceCase("pinned_full_rank", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout_full_rank", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_full_rank", -4319, 4463, 28, 4, 7),
        RowspaceCase(
            "actual_nontrivial_prefix_singular", -15791, 40127, 65, 5, 13
        ),
    ]
    rows = [row for case in cases for row in square_coinvariant_rows_for_case(case)]
    print("Trace-GCD actual-CM square coinvariant bridge audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "source_dim prefix_len tail_len coord_rank coinv_rank trace_rank "
        "prefix_rank tail_pivots coinv_det trace_det gram_det full_product "
        "prefix_product tail_product gram_relation event_match prefix_tail_match"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} source_dim={row.source_dim} "
            f"prefix_len={row.prefix_len} tail_len={row.tail_len} "
            f"coord_rank={row.coord_rank} coinv_rank={row.coinvariant_rank} "
            f"trace_rank={row.trace_rank} prefix_rank={row.prefix_rank} "
            f"tail_pivots={row.tail_pivots} coinv_det={row.coinvariant_det} "
            f"trace_det={row.trace_det} gram_det={row.trace_gram_det} "
            f"full_product={row.full_product} "
            f"prefix_product={row.prefix_product} tail_product={row.tail_product} "
            f"gram_relation={int(row.trace_det_matches_gram_twist)} "
            f"event_match={int(row.nonzero_events_match)} "
            f"prefix_tail_match={int(row.prefix_tail_event_match)}"
        )

    gram_failures = [row for row in rows if not row.trace_det_matches_gram_twist]
    event_failures = [row for row in rows if not row.nonzero_events_match]
    prefix_tail_failures = [row for row in rows if not row.prefix_tail_event_match]
    nontrivial_prefix = [row for row in rows if row.prefix_len > 0 and row.tail_len > 0]
    full_rank = [row for row in rows if row.coord_rank == row.source_dim]
    singular = [row for row in rows if row.coord_rank < row.source_dim]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  gram_relation_failures={len(gram_failures)}")
    print(f"  nonzero_event_mismatches={len(event_failures)}")
    print(f"  prefix_tail_event_mismatches={len(prefix_tail_failures)}")
    print(f"  full_rank_rows={len(full_rank)}/{len(rows)}")
    print(f"  singular_control_rows={len(singular)}/{len(rows)}")
    print(f"  actual_nontrivial_prefix_tail_rows={len(nontrivial_prefix)}/{len(rows)}")
    print("interpretation")
    print("  square_coinvariant_determinant_is_trace_pairing_adjoint_up_to_gram_unit=1")
    print("  actual_cm_phi_full_trace_det_and_residual_product_same_zero_event=1")
    print("  actual_cm_nontrivial_prefix_singular_control_detected=1")
    print("conclusion=reported_trace_gcd_actual_cm_square_coinvariant_audit")

    if (
        not rows
        or gram_failures
        or event_failures
        or prefix_tail_failures
        or not full_rank
        or not singular
        or not nontrivial_prefix
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

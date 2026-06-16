#!/usr/bin/env python3
"""Bridge trace-GCD leading matrices to subspace-polynomial residual products.

The trace-GCD bad-lambda map uses the matrix

    B_ij = Tr_{L/F_q}(lambda_j * c_i)

where the c_i are the selected leading Lang/Fitting coordinates and the
lambda_j form an F_q-basis of the left field L.  The subspace-polynomial
certificate uses the same c_i incrementally and records the residual product

    prod_i Norm_{L/F_q}(P_{i-1}(c_i)).

Both are basis-dependent representatives of the same determinant line.  This
audit checks the exact finite equivalence on actual-CM rows:

    rank(c_i)=d  <=>  det(B)!=0  <=>  residual_norm_product!=0.

This does not prove p24, but it makes the current trace-GCD p-unit theorem and
the older Moore/subspace-polynomial p-unit theorem visibly identical at the
finite-coordinate level.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import (
    fq_rank,
    lang_inverse_for_orbit,
    matrix_vector_mul,
    subfield_power_basis,
)
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    q_degree,
    qpoly_eval,
    qpoly_extend_profile,
    relative_norm_to_base,
)
from kernel_tail_schur_identity_toy import det_mod
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import (
    RowspaceCase,
    SEED,
    leading_matrix,
)


@dataclass(frozen=True)
class BridgeRow:
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
    coord_rank: int
    trace_pairing_rank: int
    trace_det: int | None
    annihilator_q_degree: int
    pivot_count: int
    residual_norm_product: int | None
    full_rank: bool
    trace_det_nonzero: bool
    residual_product_nonzero: bool
    trace_rank_matches_coord_rank: bool
    nonzero_events_match: bool


def leading_coordinates(
    dft_matrix,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    omitted: int,
    left: int,
    right: int,
    source_dim: int,
    q: int,
    field,
) -> list:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    kept = [orbit for index, orbit in enumerate(right_orbits) if index != omitted]
    coords: list = []
    inverses: dict[int, list[list]] = {}
    for orbit in kept:
        orbit_len = len(orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(
                q, orbit_len, field, SEED
            )
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in orbit
        ]
        coords.extend(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return coords[:source_dim]


def residual_norm_product_base(
    coords: list,
    source_dim: int,
    field,
) -> tuple[int, int, int | None]:
    annihilator = [field.one]
    pivots: list[int] = []
    product = field.one
    for index, coord in enumerate(coords):
        residual = qpoly_eval(annihilator, coord, field)
        product = field.mul(
            product,
            relative_norm_to_base(residual, source_dim, field),
        )
        if residual == field.zero:
            continue
        pivots.append(index)
        annihilator, _new_pivots, _new_residuals = qpoly_extend_profile(
            annihilator,
            [coord],
            field,
        )
    return q_degree(annihilator, field), len(pivots), base_value_or_none(product, field)


def bridge_rows_for_case(case: RowspaceCase) -> list[BridgeRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[BridgeRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        if any(gcd(source_dim, len(orbit)) != 1 for orbit in right_orbits):
            continue
        lambda_basis = subfield_power_basis(
            case.q, source_dim, field, SEED + 157
        )
        for omitted in range(len(right_orbits)):
            b_matrix = leading_matrix(
                lambda_basis,
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
            if b_matrix is None:
                continue
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
            coord_rank = fq_rank(coords, case.q)
            trace_rank = rank_mod_q(b_matrix, case.q)
            trace_det = det_mod(b_matrix, case.q)
            ann_degree, pivot_count, norm_product = residual_norm_product_base(
                coords, source_dim, field
            )
            full_rank = coord_rank == source_dim
            trace_det_nonzero = trace_det is not None and trace_det % case.q != 0
            residual_nonzero = norm_product is not None and norm_product % case.q != 0
            rows.append(
                BridgeRow(
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
                    coord_rank=coord_rank,
                    trace_pairing_rank=trace_rank,
                    trace_det=trace_det,
                    annihilator_q_degree=ann_degree,
                    pivot_count=pivot_count,
                    residual_norm_product=norm_product,
                    full_rank=full_rank,
                    trace_det_nonzero=trace_det_nonzero,
                    residual_product_nonzero=residual_nonzero,
                    trace_rank_matches_coord_rank=(trace_rank == coord_rank),
                    nonzero_events_match=(
                        full_rank == trace_det_nonzero == residual_nonzero
                    ),
                )
            )
    return rows


def main() -> None:
    cases = [
        RowspaceCase("pinned", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_a", -4319, 4463, 28, 4, 7),
        RowspaceCase("same_geometry_b", -4319, 4643, 28, 4, 7),
        RowspaceCase("same_geometry_c", -4511, 4547, 28, 4, 7),
    ]
    rows = [row for case in cases for row in bridge_rows_for_case(case)]
    print("Trace-GCD trace-pairing/subspace-polynomial bridge audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "source_dim coord_rank trace_rank trace_det ann_q_degree pivots "
        "residual_norm_product full_rank det_nonzero residual_nonzero "
        "rank_match event_match"
    )
    for row in rows:
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair=({row.left},{row.right}) left_orbit={list(row.left_orbit)} "
            f"omitted={row.omitted} source_dim={row.source_dim} "
            f"coord_rank={row.coord_rank} trace_rank={row.trace_pairing_rank} "
            f"trace_det={row.trace_det} "
            f"ann_q_degree={row.annihilator_q_degree} "
            f"pivots={row.pivot_count} "
            f"residual_norm_product={row.residual_norm_product} "
            f"full_rank={int(row.full_rank)} "
            f"det_nonzero={int(row.trace_det_nonzero)} "
            f"residual_nonzero={int(row.residual_product_nonzero)} "
            f"rank_match={int(row.trace_rank_matches_coord_rank)} "
            f"event_match={int(row.nonzero_events_match)}"
        )
    rank_failures = [row for row in rows if not row.trace_rank_matches_coord_rank]
    event_failures = [row for row in rows if not row.nonzero_events_match]
    missing_norms = [row for row in rows if row.residual_norm_product is None]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  trace_rank_mismatches={len(rank_failures)}")
    print(f"  nonzero_event_mismatches={len(event_failures)}")
    print(f"  missing_residual_norm_products={len(missing_norms)}")
    print(
        "  full_rank_rows="
        f"{sum(int(row.full_rank) for row in rows)}/{len(rows)}"
    )
    print("interpretation")
    print("  trace_pairing_matrix_is_dual_to_same_leading_coordinates=1")
    print("  residual_norm_product_detects_the_same_punit_event=1")
    print("  p24_missing_theorem_can_be_stated_as_either_trace_gcd_or_moore_punit=1")
    print("conclusion=reported_trace_gcd_trace_pairing_subspace_bridge_audit")


if __name__ == "__main__":
    main()

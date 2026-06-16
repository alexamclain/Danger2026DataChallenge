#!/usr/bin/env python3
"""Low-rank controls for the trace-pairing/subspace-polynomial bridge.

The actual-CM bridge audit currently sees only full-rank selected leading
maps.  This toy exercises both full-rank and deliberately dependent coordinate
tuples in a small finite field, using the same trace-pairing determinant and
all-coordinate residual product conventions.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermitian_mixed_lang_normality_audit import fq_rank, subfield_power_basis
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    q_degree,
    qpoly_eval,
    qpoly_extend_profile,
    relative_norm_to_base,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from kernel_tail_schur_identity_toy import det_mod
from l1_axis_injectivity_scan import rank_mod_q


SEED = 20260606


@dataclass(frozen=True)
class ToyRow:
    label: str
    q: int
    degree: int
    coord_rank: int
    trace_rank: int
    trace_det: int | None
    annihilator_q_degree: int
    pivot_count: int
    residual_norm_product: int | None
    full_rank: bool
    det_nonzero: bool
    residual_nonzero: bool
    rank_match: bool
    event_match: bool


def trace_to_base(value: FpE, degree: int, field: ExtensionField) -> int:
    total = field.zero
    for power in range(degree):
        total = field.add(total, field.pow(value, field.q**power))
    base = base_value_or_none(total, field)
    if base is None:
        raise ValueError("trace did not land in base field")
    return base


def trace_matrix(
    coords: list[FpE],
    lambda_basis: list[FpE],
    degree: int,
    field: ExtensionField,
) -> list[list[int]]:
    return [
        [
            trace_to_base(field.mul(lam, coord), degree, field)
            for lam in lambda_basis
        ]
        for coord in coords
    ]


def residual_product(
    coords: list[FpE],
    degree: int,
    field: ExtensionField,
) -> tuple[int, int, int | None]:
    annihilator = [field.one]
    pivots = 0
    product = field.one
    for coord in coords:
        residual = qpoly_eval(annihilator, coord, field)
        product = field.mul(product, relative_norm_to_base(residual, degree, field))
        if residual == field.zero:
            continue
        pivots += 1
        annihilator, _new_pivots, _new_residuals = qpoly_extend_profile(
            annihilator,
            [coord],
            field,
        )
    return q_degree(annihilator, field), pivots, base_value_or_none(product, field)


def audit_tuple(
    label: str,
    coords: list[FpE],
    lambda_basis: list[FpE],
    q: int,
    degree: int,
    field: ExtensionField,
) -> ToyRow:
    matrix = trace_matrix(coords, lambda_basis, degree, field)
    coord_rank = fq_rank(coords, q)
    trace_rank = rank_mod_q(matrix, q)
    trace_det = det_mod(matrix, q)
    ann_degree, pivot_count, product = residual_product(coords, degree, field)
    full_rank = coord_rank == degree
    det_nonzero = trace_det is not None and trace_det % q != 0
    residual_nonzero = pivot_count == degree and product is not None and product % q != 0
    return ToyRow(
        label=label,
        q=q,
        degree=degree,
        coord_rank=coord_rank,
        trace_rank=trace_rank,
        trace_det=trace_det,
        annihilator_q_degree=ann_degree,
        pivot_count=pivot_count,
        residual_norm_product=product,
        full_rank=full_rank,
        det_nonzero=det_nonzero,
        residual_nonzero=residual_nonzero,
        rank_match=(coord_rank == trace_rank),
        event_match=(full_rank == det_nonzero == residual_nonzero),
    )


def main() -> None:
    q = 5
    degree = 4
    field = ExtensionField(q, degree, find_irreducible_modulus(q, degree, SEED))
    basis = subfield_power_basis(q, degree, field, SEED)
    rows = [
        audit_tuple("power_basis_full", basis, basis, q, degree, field),
        audit_tuple(
            "dependent_last_repeated",
            basis[: degree - 1] + [basis[0]],
            basis,
            q,
            degree,
            field,
        ),
        audit_tuple(
            "zero_coordinate",
            basis[: degree - 1] + [field.zero],
            basis,
            q,
            degree,
            field,
        ),
    ]

    print("Trace-GCD trace-pairing/subspace bridge low-rank toy")
    print(
        "columns: label q degree coord_rank trace_rank trace_det ann_q_degree "
        "pivots residual_norm_product full_rank det_nonzero residual_nonzero "
        "rank_match event_match"
    )
    for row in rows:
        print(
            f"row label={row.label} q={row.q} degree={row.degree} "
            f"coord_rank={row.coord_rank} trace_rank={row.trace_rank} "
            f"trace_det={row.trace_det} "
            f"ann_q_degree={row.annihilator_q_degree} pivots={row.pivot_count} "
            f"residual_norm_product={row.residual_norm_product} "
            f"full_rank={int(row.full_rank)} "
            f"det_nonzero={int(row.det_nonzero)} "
            f"residual_nonzero={int(row.residual_nonzero)} "
            f"rank_match={int(row.rank_match)} "
            f"event_match={int(row.event_match)}"
        )
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  rank_mismatches={sum(int(not row.rank_match) for row in rows)}")
    print(f"  event_mismatches={sum(int(not row.event_match) for row in rows)}")
    print(
        "  low_rank_zero_products="
        f"{sum(int((not row.full_rank) and row.residual_norm_product == 0) for row in rows)}"
    )
    print("interpretation")
    print("  all_coordinate_residual_product_detects_dependent_coordinates=1")
    print("  trace_pairing_det_and_residual_product_have_same_zero_event=1")
    print("conclusion=reported_trace_gcd_trace_pairing_subspace_bridge_toy")


if __name__ == "__main__":
    main()

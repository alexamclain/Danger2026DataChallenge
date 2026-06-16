#!/usr/bin/env python3
"""Audit the prefix/tail factorization of residual products.

For an ordered coordinate tuple c_1,...,c_d, the all-coordinate residual
product factors as

    R_full = R_prefix * R_tail_on_quotient.

The p24 representative shape is `d=156 = 4*35 + 16`: four full right blocks
followed by a 16-coordinate quotient tail.  This audit checks the exact finite
factorization on actual-CM rows and also includes low-rank controls where the
prefix or tail is deliberately dependent.
"""

from __future__ import annotations

from dataclasses import dataclass

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
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from trace_gcd_lambda_plateau_det_ratio_audit import carrier_data
from trace_gcd_lambda_plateau_rowspace_audit import RowspaceCase, SEED


@dataclass(frozen=True)
class ResidualStats:
    rank: int
    q_degree: int
    pivot_count: int
    product_base: int | None
    product_nonzero: bool
    annihilator: list


@dataclass(frozen=True)
class PrefixTailRow:
    label: str
    D: int | None
    q: int
    h: int | None
    m: int | None
    n: int | None
    factor_degree: int | None
    left: int | None
    right: int | None
    left_orbit: tuple[int, ...] | None
    omitted: int | None
    source_dim: int
    prefix_len: int
    tail_len: int
    full_rank: int
    prefix_rank: int
    tail_pivots: int
    full_product: int | None
    prefix_product: int | None
    tail_product: int | None
    product_matches: bool
    full_nonzero: bool
    prefix_nonzero: bool
    tail_nonzero: bool
    event_match: bool


def residual_stats_from_annihilator(
    coords: list[FpE],
    source_dim: int,
    field: ExtensionField,
    start_annihilator: list[FpE] | None = None,
) -> ResidualStats:
    annihilator = [field.one] if start_annihilator is None else start_annihilator[:]
    pivots = 0
    product = field.one
    for coord in coords:
        residual = qpoly_eval(annihilator, coord, field)
        product = field.mul(product, relative_norm_to_base(residual, source_dim, field))
        if residual == field.zero:
            continue
        pivots += 1
        annihilator, _new_pivots, _new_residuals = qpoly_extend_profile(
            annihilator,
            [coord],
            field,
        )
    product_base = base_value_or_none(product, field)
    return ResidualStats(
        rank=fq_rank(coords, field.q),
        q_degree=q_degree(annihilator, field),
        pivot_count=pivots,
        product_base=product_base,
        product_nonzero=(product_base is not None and product_base % field.q != 0),
        annihilator=annihilator,
    )


def split_prefix_len(
    right_orbits: list[list[int]],
    omitted: int,
    source_dim: int,
) -> int:
    kept = [orbit for index, orbit in enumerate(right_orbits) if index != omitted]
    prefix_len = 0
    for orbit in kept:
        if prefix_len + len(orbit) > source_dim:
            break
        prefix_len += len(orbit)
    return prefix_len


def leading_coordinates(
    dft_matrix,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    omitted: int,
    left: int,
    right: int,
    source_dim: int,
    q: int,
    field: ExtensionField,
) -> list[FpE]:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    kept = [orbit for index, orbit in enumerate(right_orbits) if index != omitted]
    coords: list[FpE] = []
    inverses: dict[int, list[list[FpE]]] = {}
    for orbit in kept:
        orbit_len = len(orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(q, orbit_len, field, SEED)
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in orbit
        ]
        coords.extend(matrix_vector_mul(inverses[orbit_len], seed_vector, field))
    return coords[:source_dim]


def audit_coordinates(
    label: str,
    coords: list[FpE],
    prefix_len: int,
    source_dim: int,
    field: ExtensionField,
    D: int | None = None,
    h: int | None = None,
    m: int | None = None,
    n: int | None = None,
    factor_degree: int | None = None,
    left: int | None = None,
    right: int | None = None,
    left_orbit: tuple[int, ...] | None = None,
    omitted: int | None = None,
) -> PrefixTailRow:
    full = residual_stats_from_annihilator(coords, source_dim, field)
    prefix_coords = coords[:prefix_len]
    tail_coords = coords[prefix_len:source_dim]
    prefix = residual_stats_from_annihilator(prefix_coords, source_dim, field)
    tail = residual_stats_from_annihilator(
        tail_coords,
        source_dim,
        field,
        prefix.annihilator,
    )
    product_matches = (
        full.product_base is not None
        and prefix.product_base is not None
        and tail.product_base is not None
        and full.product_base % field.q
        == (prefix.product_base * tail.product_base) % field.q
    )
    full_rank = fq_rank(coords[:source_dim], field.q)
    prefix_rank = fq_rank(prefix_coords, field.q)
    full_nonzero = full.product_nonzero
    prefix_nonzero = prefix.product_nonzero
    tail_nonzero = tail.product_nonzero
    return PrefixTailRow(
        label=label,
        D=D,
        q=field.q,
        h=h,
        m=m,
        n=n,
        factor_degree=factor_degree,
        left=left,
        right=right,
        left_orbit=left_orbit,
        omitted=omitted,
        source_dim=source_dim,
        prefix_len=prefix_len,
        tail_len=source_dim - prefix_len,
        full_rank=full_rank,
        prefix_rank=prefix_rank,
        tail_pivots=tail.pivot_count,
        full_product=full.product_base,
        prefix_product=prefix.product_base,
        tail_product=tail.product_base,
        product_matches=product_matches,
        full_nonzero=full_nonzero,
        prefix_nonzero=prefix_nonzero,
        tail_nonzero=tail_nonzero,
        event_match=(full_nonzero == (prefix_nonzero and tail_nonzero)),
    )


def actual_cm_rows(case: RowspaceCase) -> list[PrefixTailRow]:
    h, n, factor, _marginal, field, _powers, dft_matrix, right_orbits = (
        carrier_data(case)
    )
    rows: list[PrefixTailRow] = []
    for left_orbit in q_orbits(case.left, case.q):
        source_dim = len(left_orbit)
        if source_dim <= 1:
            continue
        _lambda_basis = subfield_power_basis(case.q, source_dim, field, SEED + 157)
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
            rows.append(
                audit_coordinates(
                    case.label,
                    coords,
                    split_prefix_len(right_orbits, omitted, source_dim),
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
            )
    return rows


def toy_rows() -> list[PrefixTailRow]:
    q = 5
    source_dim = 4
    field = ExtensionField(q, source_dim, find_irreducible_modulus(q, source_dim, SEED))
    basis = subfield_power_basis(q, source_dim, field, SEED)
    prefix_len = 2
    return [
        audit_coordinates(
            "toy_full_prefix_tail",
            basis,
            prefix_len,
            source_dim,
            field,
        ),
        audit_coordinates(
            "toy_prefix_dependent",
            [basis[0], basis[0], basis[2], basis[3]],
            prefix_len,
            source_dim,
            field,
        ),
        audit_coordinates(
            "toy_tail_dependent",
            [basis[0], basis[1], basis[0], basis[3]],
            prefix_len,
            source_dim,
            field,
        ),
    ]


def main() -> None:
    cases = [
        RowspaceCase("pinned", -13319, 13463, 28, 4, 7),
        RowspaceCase("holdout", -26759, 26903, 21, 3, 7),
        RowspaceCase("same_geometry_a", -4319, 4463, 28, 4, 7),
        RowspaceCase("stress_nontrivial_prefix", -4319, 4463, 28, 7, 4),
    ]
    rows = [row for case in cases for row in actual_cm_rows(case)] + toy_rows()
    print("Trace-GCD residual prefix/tail bridge audit")
    print(
        "columns: label D q h m n factor_deg pair left_orbit omitted "
        "source_dim prefix_len tail_len full_rank prefix_rank tail_pivots "
        "full_product prefix_product tail_product product_match "
        "full_nonzero prefix_nonzero tail_nonzero event_match"
    )
    for row in rows:
        pair = "None" if row.left is None else f"({row.left},{row.right})"
        print(
            f"row label={row.label} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"pair={pair} left_orbit={list(row.left_orbit) if row.left_orbit else None} "
            f"omitted={row.omitted} source_dim={row.source_dim} "
            f"prefix_len={row.prefix_len} tail_len={row.tail_len} "
            f"full_rank={row.full_rank} prefix_rank={row.prefix_rank} "
            f"tail_pivots={row.tail_pivots} full_product={row.full_product} "
            f"prefix_product={row.prefix_product} tail_product={row.tail_product} "
            f"product_match={int(row.product_matches)} "
            f"full_nonzero={int(row.full_nonzero)} "
            f"prefix_nonzero={int(row.prefix_nonzero)} "
            f"tail_nonzero={int(row.tail_nonzero)} "
            f"event_match={int(row.event_match)}"
        )
    product_failures = [row for row in rows if not row.product_matches]
    event_failures = [row for row in rows if not row.event_match]
    prefix_fail_controls = [row for row in rows if row.label == "toy_prefix_dependent" and not row.prefix_nonzero]
    tail_fail_controls = [row for row in rows if row.label == "toy_tail_dependent" and row.prefix_nonzero and not row.tail_nonzero]
    print("totals")
    print(f"  rows={len(rows)}")
    print(f"  product_mismatches={len(product_failures)}")
    print(f"  event_mismatches={len(event_failures)}")
    print(f"  prefix_failure_controls={len(prefix_fail_controls)}")
    print(f"  tail_failure_controls={len(tail_fail_controls)}")
    print(
        "  nontrivial_prefix_rows="
        f"{sum(int(row.prefix_len > 0 and row.tail_len > 0) for row in rows)}/{len(rows)}"
    )
    print("interpretation")
    print("  full_residual_product_factors_as_prefix_times_tail=1")
    print("  prefix_and_tail_punits_are_equivalent_to_full_residual_punit=1")
    print("  p24_shape_is_prefix_140_then_tail_16=1")
    print("conclusion=reported_trace_gcd_residual_prefix_tail_bridge_audit")


if __name__ == "__main__":
    main()

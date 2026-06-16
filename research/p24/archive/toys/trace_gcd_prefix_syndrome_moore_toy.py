#!/usr/bin/env python3
"""Toy for the fixed-adjoint syndrome Moore certificate."""

from __future__ import annotations

from dataclasses import dataclass
import random

from hermitian_mixed_lang_normality_audit import fq_rank, subfield_power_basis
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    relative_norm_to_base,
)
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from l1_axis_injectivity_scan import rank_mod_q
from moore_residual_product_toy import all_step_residuals, product
from trace_gcd_prefix_semilinear_core_toy import random_table
from trace_gcd_prefix_semilinear_fixed_adjoint_toy import trace_to_base


@dataclass(frozen=True)
class MooreCase:
    label: str
    coordinate_count: int
    coordinate_rank: int
    trace_matrix_rank: int
    residual_product_zero: bool
    residual_norm: int | None
    full_rank: bool
    event_match: bool


def syndrome_coordinate_elements(
    table: list[list[FpE]],
    k_basis: list[FpE],
    q: int,
    field: ExtensionField,
) -> list[FpE]:
    """Return fixed scalar elements plus basis coordinates of K-syndromes.

    The toy has one fixed frequency, represented by table[0], and one
    length-2 frequency orbit, represented by table[1], table[2].
    """

    out = list(table[0])
    for block in range(len(table[0])):
        for theta in k_basis:
            out.append(
                field.add(
                    field.mul(theta, table[1][block]),
                    field.mul(field.pow(theta, q), table[2][block]),
                )
            )
    return out


def trace_matrix_rank(
    coords: list[FpE],
    lambda_basis: list[FpE],
    field: ExtensionField,
) -> int:
    matrix = [
        [
            trace_to_base(field.mul(lam, coord), field)
            for lam in lambda_basis
        ]
        for coord in coords
    ]
    return rank_mod_q(matrix, field.q)


def residual_norm_base(value: FpE, field: ExtensionField) -> int | None:
    return base_value_or_none(relative_norm_to_base(value, field.degree, field), field)


def analyze_case(
    label: str,
    table: list[list[FpE]],
    k_basis: list[FpE],
    lambda_basis: list[FpE],
    q: int,
    field: ExtensionField,
) -> MooreCase:
    coords = syndrome_coordinate_elements(table, k_basis, q, field)
    coord_rank = fq_rank(coords, q)
    t_rank = trace_matrix_rank(coords, lambda_basis, field)
    _ann, residuals = all_step_residuals([field.one], coords, field)
    residual = product(residuals, field)
    residual_zero = residual == field.zero
    full_rank = coord_rank == len(coords)
    return MooreCase(
        label=label,
        coordinate_count=len(coords),
        coordinate_rank=coord_rank,
        trace_matrix_rank=t_rank,
        residual_product_zero=residual_zero,
        residual_norm=None if residual_zero else residual_norm_base(residual, field),
        full_rank=full_rank,
        event_match=(
            coord_rank == t_rank
            and full_rank == (not residual_zero)
        ),
    )


def main() -> None:
    q = 2
    length = 3
    k_degree = 2
    l_degree = 8
    block_count = 2
    seed = 20260606

    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, seed))
    k_basis = subfield_power_basis(q, k_degree, field, seed)
    lambda_basis = subfield_power_basis(q, l_degree, field, seed + 1)
    rng = random.Random(seed)

    good_table = None
    for _ in range(200):
        candidate = random_table(length, block_count, field, rng)
        coords = syndrome_coordinate_elements(candidate, k_basis, q, field)
        if fq_rank(coords, q) == len(coords):
            good_table = candidate
            break
    if good_table is None:
        raise RuntimeError("did not find random-good syndrome Moore example")

    forced_table = [row[:] for row in good_table]
    forced_table[0][1] = forced_table[0][0]

    rows = [
        analyze_case("random_good", good_table, k_basis, lambda_basis, q, field),
        analyze_case(
            "forced_fixed_frequency_relation",
            forced_table,
            k_basis,
            lambda_basis,
            q,
            field,
        ),
    ]

    p24_p = 10**24 + 7
    p24_q35 = p24_p % 35
    fixed_frequency_count = sum(1 for a in range(35) if (p24_q35 * a) % 35 == a)
    length4_orbit_count = (35 - fixed_frequency_count) // 4
    p24_blocks = 4

    print("Trace-GCD prefix syndrome Moore toy")
    print(f"q={q}")
    print(f"length={length}")
    print(f"k_degree={k_degree}")
    print(f"l_degree={l_degree}")
    print(f"block_count={block_count}")
    for row in rows:
        print(
            "case="
            f"{row.label} coordinate_count={row.coordinate_count} "
            f"coordinate_rank={row.coordinate_rank} "
            f"trace_matrix_rank={row.trace_matrix_rank} "
            f"residual_product_zero={int(row.residual_product_zero)} "
            f"residual_norm={row.residual_norm} "
            f"full_rank={int(row.full_rank)} "
            f"event_match={int(row.event_match)}"
        )
    print("p24")
    print(f"  p24_fixed_frequency_count={fixed_frequency_count}")
    print(f"  p24_length4_frequency_orbit_count={length4_orbit_count}")
    print(f"  p24_syndrome_coordinate_count={fixed_frequency_count * p24_blocks + length4_orbit_count * p24_blocks * 4}")
    print("interpretation")
    print("  syndrome_coordinate_elements_represent_fixed_adjoint=1")
    print("  trace_pairing_rank_equals_coordinate_span_rank=1")
    print("  syndrome_moore_residual_nonzero_iff_full_rank=1")
    print("conclusion=reported_trace_gcd_prefix_syndrome_moore_toy")


if __name__ == "__main__":
    main()

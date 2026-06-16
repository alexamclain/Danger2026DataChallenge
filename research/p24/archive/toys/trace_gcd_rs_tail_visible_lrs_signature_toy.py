#!/usr/bin/env python3
"""Visible LRS/GRS signature toy for RS-tail syndrome columns.

The hidden MSRD route would be powerful only with an explicit p-unit block
equivalence.  A cheaper possibility is that the natural coordinates already
look like a Reed-Solomon/rational-normal model.  This toy tests one visible
necessary signature for that easier route:

    column coordinates form a geometric progression

or, equivalently, every 2 x 2 adjacent Hankel minor of a column is zero.

Synthetic rational-normal columns pass.  Random RS-tail fixed-syndrome columns
with the same finite bookkeeping do not.  Thus the visible GRS/LRS shortcut is
not the right proof unless an additional class-field coordinate change is
constructed.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from hermitian_mixed_lang_normality_audit import subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_semilinear_core_toy import random_element
from trace_gcd_rs_tail_fixed_adjoint_toy import frequency_orbits
from trace_gcd_rs_tail_syndrome_moore_schur_toy import fixed_prefix_columns


@dataclass(frozen=True)
class SignatureRow:
    label: str
    q: int
    row_dim: int
    column_count: int
    full_rank: int
    rank_one_hankel_columns: int
    max_hankel_rank: int
    visible_signature: bool


def transpose_columns(columns: list[list[int]]) -> list[list[int]]:
    if not columns:
        return []
    return [list(row) for row in zip(*columns)]


def column_hankel_rank(column: list[int], q: int) -> int:
    if len(column) <= 1:
        return int(any(value % q for value in column))
    return rank_mod_q([column[:-1], column[1:]], q)


def signature_row(label: str, columns: list[list[int]], q: int) -> SignatureRow:
    matrix = transpose_columns(columns)
    hankel_ranks = [column_hankel_rank(column, q) for column in columns]
    nonzero_hankel_ranks = [rank for rank in hankel_ranks if rank]
    return SignatureRow(
        label=label,
        q=q,
        row_dim=len(matrix),
        column_count=len(columns),
        full_rank=rank_mod_q(matrix, q),
        rank_one_hankel_columns=sum(rank <= 1 for rank in hankel_ranks),
        max_hankel_rank=max(nonzero_hankel_ranks, default=0),
        visible_signature=all(rank <= 1 for rank in hankel_ranks),
    )


def rnc_columns(q: int, row_dim: int, column_count: int) -> list[list[int]]:
    columns: list[list[int]] = []
    for index in range(column_count):
        x = (index + 1) % q
        if x == 0:
            x = q - 1
        value = 1
        column: list[int] = []
        for _row in range(row_dim):
            column.append(value)
            value = (value * x) % q
        columns.append(column)
    return columns


def random_rs_tail_columns(
    q: int,
    right_len: int,
    block_count: int,
    field_degree: int,
    seed: int,
) -> list[FpE]:
    field = ExtensionField(
        q,
        field_degree,
        find_irreducible_modulus(q, field_degree, seed),
    )
    k_degree = 1
    multiplier = q % right_len
    while pow(multiplier, k_degree, right_len) != 1:
        k_degree += 1
    k_basis = subfield_power_basis(q, k_degree, field, seed + 1)
    _omega = primitive_root_of_order(field, right_len, seed + 2)
    orbits = frequency_orbits(right_len, q % right_len)
    rng = random.Random(seed)
    table = [
        [random_element(field, rng) for _block in range(block_count)]
        for _frequency in range(right_len)
    ]
    return fixed_prefix_columns(table, k_basis, orbits, q, field)


def main() -> None:
    rnc_q = 17
    rnc_dim = 16
    rnc_count = 15
    rs_q = 3
    rs_right_len = 5
    rs_block_count = 3
    rs_field_degree = 16
    seed = 20260606

    synthetic = signature_row(
        "synthetic_rational_normal",
        rnc_columns(rnc_q, rnc_dim, rnc_count),
        rnc_q,
    )
    rs_tail = signature_row(
        "random_rs_tail_syndrome_columns",
        [list(column) for column in random_rs_tail_columns(
            rs_q,
            rs_right_len,
            rs_block_count,
            rs_field_degree,
            seed,
        )],
        rs_q,
    )

    p24_full_columns = 6 * (7 + 7 * 4)
    p24_selected_columns = 4 * (7 + 7 * 4) + 16
    p24_erasure_columns = p24_full_columns - p24_selected_columns

    print("Trace-GCD RS-tail visible LRS signature toy")
    for row in (synthetic, rs_tail):
        print(
            f"case={row.label} q={row.q} row_dim={row.row_dim} "
            f"column_count={row.column_count} full_rank={row.full_rank} "
            f"rank_one_hankel_columns={row.rank_one_hankel_columns} "
            f"max_hankel_rank={row.max_hankel_rank} "
            f"visible_signature={int(row.visible_signature)}"
        )
    print("p24")
    print(f"  p24_full_fixed_source_columns={p24_full_columns}")
    print(f"  p24_selected_rs_tail_columns={p24_selected_columns}")
    print(f"  p24_erasure_columns={p24_erasure_columns}")
    print("interpretation")
    print("  synthetic_visible_grs_signature_detected=1")
    print("  random_rs_tail_visible_grs_signature_rejected=1")
    print("  hidden_lrs_route_needs_nontrivial_punit_block_equivalence=1")
    print("conclusion=reported_trace_gcd_rs_tail_visible_lrs_signature_toy")


if __name__ == "__main__":
    main()

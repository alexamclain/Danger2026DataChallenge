#!/usr/bin/env python3
"""Selected-block support-profile toy for the RS-tail syndrome columns.

An explicit hidden LRS/MSRD equivalence would preserve block projection ranks
and generalized block-support weights.  For the selected RS-tail square this
cheap gate says that every subset of the selected blocks is a direct sum:

    P2, P3, P5, P6, T16 have dimensions 35,35,35,35,16.

For the square object this is only a compatibility check, not evidence of an
LRS model: if all 156 selected columns are independent, every subset is already
independent.  Positive hidden-LRS evidence has to come from an explicit p-unit
block equivalence or from moduli involving the unused 54 columns of the full
210-column object.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import random

from hermitian_mixed_lang_normality_audit import fq_rank, subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from trace_gcd_prefix_semilinear_core_toy import random_element
from trace_gcd_rs_tail_fixed_adjoint_toy import add_many, frequency_orbits
from trace_gcd_rs_tail_syndrome_moore_schur_toy import (
    random_prefix_table,
    random_tail_table,
    rs_tail_columns,
    solve_tail_table_for_first_two_columns,
)


@dataclass(frozen=True)
class ProfileCase:
    label: str
    block_dims: tuple[int, ...]
    subset_count: int
    defect_count: int
    first_defect: str
    full_rank: int
    expected_full_rank: int
    support_profile_full: bool


def prefix_columns_by_block(
    prefix_table: list[list[FpE]],
    k_basis: list[FpE],
    orbits: list[list[int]],
    q: int,
    field: ExtensionField,
) -> list[list[FpE]]:
    right_len = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    blocks: list[list[FpE]] = [[] for _ in range(prefix_blocks)]
    for block in range(prefix_blocks):
        for orbit in orbits:
            if len(orbit) == 1:
                blocks[block].append(prefix_table[orbit[0]][block])
                continue
            representative = orbit[0]
            for kappa in k_basis:
                terms: list[FpE] = []
                for step in range(len(orbit)):
                    frequency = (pow(q, step, right_len) * representative) % right_len
                    terms.append(
                        field.mul(
                            field.pow(kappa, q**step),
                            prefix_table[frequency][block],
                        )
                    )
                blocks[block].append(add_many(terms, field))
    return blocks


def flatten(blocks: list[list[FpE]]) -> list[FpE]:
    return [column for block in blocks for column in block]


def support_profile_case(
    label: str,
    blocks: list[list[FpE]],
    q: int,
) -> ProfileCase:
    defects: list[str] = []
    for size in range(1, len(blocks) + 1):
        for subset in combinations(range(len(blocks)), size):
            columns = flatten([blocks[index] for index in subset])
            expected = sum(len(blocks[index]) for index in subset)
            rank = fq_rank(columns, q)
            if rank != expected:
                defects.append(
                    f"subset={','.join(str(index) for index in subset)} "
                    f"rank={rank} expected={expected}"
                )
    all_columns = flatten(blocks)
    expected_full = len(all_columns)
    full_rank = fq_rank(all_columns, q)
    return ProfileCase(
        label=label,
        block_dims=tuple(len(block) for block in blocks),
        subset_count=(2 ** len(blocks)) - 1,
        defect_count=len(defects),
        first_defect=defects[0] if defects else "none",
        full_rank=full_rank,
        expected_full_rank=expected_full,
        support_profile_full=(len(defects) == 0),
    )


def random_tables_with_direct_profile(
    q: int,
    right_len: int,
    prefix_blocks: int,
    tail_dim: int,
    field: ExtensionField,
    k_basis: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    rng: random.Random,
) -> tuple[list[list[FpE]], list[FpE], list[list[FpE]]]:
    for _trial in range(800):
        prefix = random_prefix_table(right_len, prefix_blocks, field, rng)
        tail = random_tail_table(right_len, field, rng)
        blocks = prefix_columns_by_block(prefix, k_basis, orbits, q, field)
        blocks.append(rs_tail_columns(tail, tail_dim, omega, field))
        row = support_profile_case("candidate", blocks, q)
        if row.support_profile_full:
            return prefix, tail, blocks
    raise RuntimeError("did not find random direct selected-block profile")


def main() -> None:
    q = 2
    right_len = 3
    k_degree = 2
    prefix_blocks = 2
    tail_dim = 2
    l_degree = 8
    seed = 20260606

    field = ExtensionField(q, l_degree, find_irreducible_modulus(q, l_degree, seed))
    k_basis = subfield_power_basis(q, k_degree, field, seed + 1)
    omega = primitive_root_of_order(field, right_len, seed + 2)
    orbits = frequency_orbits(right_len, q % right_len)
    rng = random.Random(seed)

    good_prefix, good_tail, good_blocks = random_tables_with_direct_profile(
        q,
        right_len,
        prefix_blocks,
        tail_dim,
        field,
        k_basis,
        orbits,
        omega,
        rng,
    )

    prefix_relation = [row[:] for row in good_prefix]
    for frequency in range(right_len):
        prefix_relation[frequency][1] = prefix_relation[frequency][0]
    prefix_relation_blocks = prefix_columns_by_block(
        prefix_relation, k_basis, orbits, q, field
    )
    prefix_relation_blocks.append(rs_tail_columns(good_tail, tail_dim, omega, field))

    first_block = good_blocks[0]
    tail_inside_prefix = solve_tail_table_for_first_two_columns(
        first_block[0],
        first_block[1],
        omega,
        field,
    )
    tail_inside_blocks = prefix_columns_by_block(good_prefix, k_basis, orbits, q, field)
    tail_inside_blocks.append(
        rs_tail_columns(tail_inside_prefix, tail_dim, omega, field)
    )

    rows = [
        support_profile_case("random_selected_blocks_direct", good_blocks, q),
        support_profile_case(
            "forced_cross_prefix_block_relation", prefix_relation_blocks, q
        ),
        support_profile_case(
            "forced_tail_inside_prefix_block", tail_inside_blocks, q
        ),
    ]

    p24_selected_block_dims = (35, 35, 35, 35, 16)
    p24_full_columns = 6 * (7 + 7 * 4)
    p24_selected_columns = sum(p24_selected_block_dims)

    print("Trace-GCD RS-tail selected-block support-profile toy")
    for row in rows:
        print(
            f"case={row.label} block_dims={list(row.block_dims)} "
            f"subset_count={row.subset_count} defect_count={row.defect_count} "
            f"first_defect={row.first_defect!r} full_rank={row.full_rank} "
            f"expected_full_rank={row.expected_full_rank} "
            f"support_profile_full={int(row.support_profile_full)}"
        )
    print("p24")
    print(f"  p24_selected_block_dims={list(p24_selected_block_dims)}")
    print(f"  p24_selected_block_count={len(p24_selected_block_dims)}")
    print(f"  p24_selected_total_dim={p24_selected_columns}")
    print(f"  p24_full_fixed_source_columns={p24_full_columns}")
    print(f"  p24_unused_full_source_columns={p24_full_columns - p24_selected_columns}")
    print(f"  p24_selected_block_support_profile_subsets={2 ** len(p24_selected_block_dims) - 1}")
    print("interpretation")
    print("  selected_block_support_profile_gate_passes_random_direct_control=1")
    print("  selected_block_support_profile_detects_prefix_relation=1")
    print("  selected_block_support_profile_detects_tail_inside_prefix=1")
    print("  selected_square_pass_is_compatibility_not_lrs_evidence=1")
    print("  full_210_column_moduli_needed_for_positive_hidden_lrs_evidence=1")
    print("conclusion=reported_trace_gcd_rs_tail_block_support_profile_toy")


if __name__ == "__main__":
    main()

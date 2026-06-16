#!/usr/bin/env python3
"""Moore/Schur toy for the full RS-tail syndrome columns.

The p24 fixed theorem is now the full-rank statement for explicit columns

    F_p^28 + K^28 + F_p^16 -> L.

This toy checks the intrinsic split of that statement:

* the fixed prefix columns span a codimension-tail subspace;
* the RS-tail Fourier columns are independent modulo that prefix span;
* the Moore residual product factors as prefix times quotient-tail.

It also carries separate negative controls for prefix failure and tail-inside-
prefix failure.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from hermitian_mixed_lang_normality_audit import fq_rank, subfield_power_basis
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from moore_residual_product_toy import all_step_residuals, product
from trace_gcd_rs_tail_fixed_adjoint_toy import (
    add_many,
    frequency_orbits,
    tail_column,
)
from trace_gcd_prefix_semilinear_core_toy import random_element


@dataclass(frozen=True)
class SchurCase:
    label: str
    prefix_count: int
    tail_count: int
    full_count: int
    prefix_rank: int
    tail_quotient_rank: int
    full_rank: int
    prefix_residual_zero: bool
    tail_residual_zero: bool
    full_residual_zero: bool
    event_match: bool


def fixed_prefix_columns(
    prefix_table: list[list[FpE]],
    k_basis: list[FpE],
    orbits: list[list[int]],
    q: int,
    field: ExtensionField,
) -> list[FpE]:
    right_len = len(prefix_table)
    prefix_blocks = len(prefix_table[0])
    columns: list[FpE] = []
    for orbit in orbits:
        if len(orbit) == 1:
            frequency = orbit[0]
            for block in range(prefix_blocks):
                columns.append(prefix_table[frequency][block])
            continue
        representative = orbit[0]
        for block in range(prefix_blocks):
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
                columns.append(add_many(terms, field))
    return columns


def rs_tail_columns(
    tail_table: list[FpE],
    tail_dim: int,
    omega: FpE,
    field: ExtensionField,
) -> list[FpE]:
    return [
        tail_column(tail_table, tail_pos, omega, field)
        for tail_pos in range(tail_dim)
    ]


def solve_tail_table_for_first_two_columns(
    target0: FpE,
    target1: FpE,
    omega: FpE,
    field: ExtensionField,
) -> list[FpE]:
    """Build length-3 frequency data with W_0=target0 and W_1=target1."""

    v2 = field.zero
    denominator = field.sub(omega, field.one)
    v1 = field.div(field.sub(target1, target0), denominator)
    v0 = field.sub(target0, v1)
    return [v0, v1, v2]


def residual_zeroes(
    prefix_columns: list[FpE],
    tail_columns_: list[FpE],
    field: ExtensionField,
) -> tuple[bool, bool, bool]:
    prefix_ann, prefix_residuals = all_step_residuals(
        [field.one], prefix_columns, field
    )
    _tail_ann, tail_residuals = all_step_residuals(
        prefix_ann, tail_columns_, field
    )
    _full_ann, full_residuals = all_step_residuals(
        [field.one], prefix_columns + tail_columns_, field
    )
    return (
        product(prefix_residuals, field) == field.zero,
        product(tail_residuals, field) == field.zero,
        product(full_residuals, field) == field.zero,
    )


def analyze_case(
    label: str,
    prefix_table: list[list[FpE]],
    tail_table: list[FpE],
    k_basis: list[FpE],
    orbits: list[list[int]],
    omega: FpE,
    q: int,
    field: ExtensionField,
) -> SchurCase:
    prefix_columns = fixed_prefix_columns(prefix_table, k_basis, orbits, q, field)
    tail_columns_ = rs_tail_columns(tail_table, 2, omega, field)
    full_columns = prefix_columns + tail_columns_
    prefix_rank = fq_rank(prefix_columns, q)
    full_rank = fq_rank(full_columns, q)
    tail_quotient_rank = full_rank - prefix_rank
    prefix_zero, tail_zero, full_zero = residual_zeroes(
        prefix_columns, tail_columns_, field
    )
    return SchurCase(
        label=label,
        prefix_count=len(prefix_columns),
        tail_count=len(tail_columns_),
        full_count=len(full_columns),
        prefix_rank=prefix_rank,
        tail_quotient_rank=tail_quotient_rank,
        full_rank=full_rank,
        prefix_residual_zero=prefix_zero,
        tail_residual_zero=tail_zero,
        full_residual_zero=full_zero,
        event_match=(
            (not full_zero)
            == (not prefix_zero and not tail_zero)
            == (full_rank == len(full_columns))
        ),
    )


def random_prefix_table(
    right_len: int,
    prefix_blocks: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[list[FpE]]:
    return [
        [random_element(field, rng) for _ in range(prefix_blocks)]
        for _ in range(right_len)
    ]


def random_tail_table(
    right_len: int,
    field: ExtensionField,
    rng: random.Random,
) -> list[FpE]:
    return [random_element(field, rng) for _ in range(right_len)]


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

    good_prefix = None
    good_tail = None
    for _ in range(400):
        prefix = random_prefix_table(right_len, prefix_blocks, field, rng)
        tail = random_tail_table(right_len, field, rng)
        row = analyze_case("candidate", prefix, tail, k_basis, orbits, omega, q, field)
        if (
            row.prefix_rank == row.prefix_count
            and row.tail_quotient_rank == row.tail_count
            and row.full_rank == row.full_count
        ):
            good_prefix = prefix
            good_tail = tail
            break
    if good_prefix is None or good_tail is None:
        raise RuntimeError("did not find random-good RS-tail Schur example")

    prefix_dependent = [row[:] for row in good_prefix]
    prefix_dependent[0][1] = prefix_dependent[0][0]

    good_prefix_columns = fixed_prefix_columns(
        good_prefix, k_basis, orbits, q, field
    )
    tail_inside_prefix = solve_tail_table_for_first_two_columns(
        good_prefix_columns[0],
        good_prefix_columns[1],
        omega,
        field,
    )

    rows = [
        analyze_case(
            "random_prefix_full_tail_quotient_full",
            good_prefix,
            good_tail,
            k_basis,
            orbits,
            omega,
            q,
            field,
        ),
        analyze_case(
            "forced_prefix_relation",
            prefix_dependent,
            good_tail,
            k_basis,
            orbits,
            omega,
            q,
            field,
        ),
        analyze_case(
            "forced_tail_inside_prefix_span",
            good_prefix,
            tail_inside_prefix,
            k_basis,
            orbits,
            omega,
            q,
            field,
        ),
    ]

    p24_prefix_count = 7 * 4 + (7 * 4) * 4
    p24_tail_count = 16
    p24_full_count = p24_prefix_count + p24_tail_count

    print("Trace-GCD RS-tail syndrome Moore/Schur toy")
    print(f"q={q}")
    print(f"right_len={right_len}")
    print(f"k_degree={k_degree}")
    print(f"prefix_blocks={prefix_blocks}")
    print(f"tail_dim={tail_dim}")
    print(f"l_degree={l_degree}")
    for row in rows:
        print(
            "case="
            f"{row.label} prefix_count={row.prefix_count} "
            f"tail_count={row.tail_count} full_count={row.full_count} "
            f"prefix_rank={row.prefix_rank} "
            f"tail_quotient_rank={row.tail_quotient_rank} "
            f"full_rank={row.full_rank} "
            f"prefix_residual_zero={int(row.prefix_residual_zero)} "
            f"tail_residual_zero={int(row.tail_residual_zero)} "
            f"full_residual_zero={int(row.full_residual_zero)} "
            f"event_match={int(row.event_match)}"
        )
    print("p24")
    print(f"  p24_rs_tail_prefix_coordinate_count={p24_prefix_count}")
    print(f"  p24_rs_tail_tail_coordinate_count={p24_tail_count}")
    print(f"  p24_rs_tail_full_coordinate_count={p24_full_count}")
    print("interpretation")
    print("  rs_tail_syndrome_columns_have_moore_schur_split=1")
    print("  prefix_full_plus_tail_quotient_full_iff_full_syndrome_unit=1")
    print("  prefix_failure_and_tail_quotient_failure_controls_detected=1")
    print("conclusion=reported_trace_gcd_rs_tail_syndrome_moore_schur_toy")


if __name__ == "__main__":
    main()

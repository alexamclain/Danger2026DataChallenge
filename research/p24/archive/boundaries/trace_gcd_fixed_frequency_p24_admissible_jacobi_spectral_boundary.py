#!/usr/bin/env python3
"""Spectral fingerprint of the admissible C-axis Jacobi-carry span.

The rank-621 p24 target should not remain a black-box linear subspace.  This
gate computes the Fourier-side shape of the admissible carry span in small
exact C_7 x C_c models.

Observed pattern:

* the C-trivial slice has rank 1, only in the right-trivial channel;
* every nontrivial C-character slice projects with full right rank 7;
* each conjugate C-character pair projects with rank 8, not 14;
* adding conjugate pairs cumulatively gives increments 1, 7, ..., 7, 4.

Thus the p24 rank formula

    621 = 1 + 7*88 + 4

has a spectral interpretation: most conjugate C-pairs add a full right profile,
while the last three dimensions are killed by global admissible-carry
compatibility.  A proof of membership should target these pair-compatibility
relations, not just forbidden bidegree support.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate import primitive_root
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import (
    RIGHT_DEGREE,
    admissible_c_axis_carry_rows,
    rank_mod,
    split_prime_for,
)


SMALL_C_DEGREES = [5, 11, 13]
P24_C_DEGREE = 179


def dft_rows(rows: list[list[int]], c_degree: int, field_q: int) -> list[list[int]]:
    root = primitive_root(field_q)
    omega_right = pow(root, (field_q - 1) // RIGHT_DEGREE, field_q)
    omega_c = pow(root, (field_q - 1) // c_degree, field_q)
    out: list[list[int]] = []
    for row in rows:
        transformed: list[int] = []
        for right_character in range(RIGHT_DEGREE):
            for c_character in range(c_degree):
                total = 0
                for right_index in range(RIGHT_DEGREE):
                    right_weight = pow(
                        omega_right,
                        (-right_character * right_index) % RIGHT_DEGREE,
                        field_q,
                    )
                    for c_index in range(c_degree):
                        c_weight = pow(
                            omega_c,
                            (-c_character * c_index) % c_degree,
                            field_q,
                        )
                        total = (
                            total
                            + row[right_index * c_degree + c_index]
                            * right_weight
                            * c_weight
                        ) % field_q
                transformed.append(total)
        out.append(transformed)
    return out


def c_slice_rank(dft: list[list[int]], c_degree: int, c_character: int, field_q: int) -> int:
    columns = [right_character * c_degree + c_character for right_character in range(RIGHT_DEGREE)]
    return rank_mod([[row[column] for column in columns] for row in dft], field_q)


def c_pair_columns(c_degree: int, c_character: int) -> list[int]:
    conjugate = (-c_character) % c_degree
    return [
        right_character * c_degree + c_character
        for right_character in range(RIGHT_DEGREE)
    ] + [
        right_character * c_degree + conjugate
        for right_character in range(RIGHT_DEGREE)
    ]


def projected_rank(dft: list[list[int]], columns: list[int], field_q: int) -> int:
    return rank_mod([[row[column] for column in columns] for row in dft], field_q)


def expected_cumulative_increments(c_degree: int) -> list[int]:
    pair_count = (c_degree - 1) // 2
    return [1] + [RIGHT_DEGREE] * (pair_count - 1) + [4]


def main() -> None:
    all_rows_match = 0

    print("Trace-GCD fixed-frequency p24 admissible Jacobi spectral boundary")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        rows = admissible_c_axis_carry_rows(c_degree, field_q)
        dft = dft_rows(rows, c_degree, field_q)
        value_rank = rank_mod(rows, field_q)
        dft_rank = rank_mod(dft, field_q)
        c0_rank = c_slice_rank(dft, c_degree, 0, field_q)
        nontrivial_slice_ranks = [
            c_slice_rank(dft, c_degree, c_character, field_q)
            for c_character in range(1, c_degree)
        ]
        pair_ranks = [
            projected_rank(dft, c_pair_columns(c_degree, c_character), field_q)
            for c_character in range(1, (c_degree + 1) // 2)
        ]

        cumulative_columns = [right_character * c_degree for right_character in range(RIGHT_DEGREE)]
        cumulative_ranks: list[int] = []
        increments: list[int] = []
        previous_rank = 0
        for c_character in range(0, (c_degree + 1) // 2):
            if c_character:
                cumulative_columns.extend(c_pair_columns(c_degree, c_character))
            rank = projected_rank(dft, cumulative_columns, field_q)
            cumulative_ranks.append(rank)
            increments.append(rank - previous_rank)
            previous_rank = rank

        expected_increments = expected_cumulative_increments(c_degree)
        row_match = int(
            value_rank == dft_rank
            and c0_rank == 1
            and all(rank == RIGHT_DEGREE for rank in nontrivial_slice_ranks)
            and all(rank == RIGHT_DEGREE + 1 for rank in pair_ranks)
            and increments == expected_increments
            and dft_rank == RIGHT_DEGREE * ((c_degree - 1) // 2) - 2
        )
        all_rows_match += row_match
        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"value_rank={value_rank} dft_rank={dft_rank} "
            f"c_trivial_slice_rank={c0_rank} "
            f"nontrivial_slice_ranks={nontrivial_slice_ranks} "
            f"conjugate_pair_ranks={pair_ranks} "
            f"cumulative_ranks={cumulative_ranks} "
            f"cumulative_increments={increments} "
            f"expected_increments={expected_increments} "
            f"spectral_pattern_match={row_match}"
        )

    p24_pair_count = (P24_C_DEGREE - 1) // 2
    p24_spectral_rank = 1 + RIGHT_DEGREE * (p24_pair_count - 1) + 4
    print(f"spectral_pattern_matches={all_rows_match}/{len(SMALL_C_DEGREES)}")
    print(f"p24_c_degree={P24_C_DEGREE}")
    print(f"p24_conjugate_C_pair_count={p24_pair_count}")
    print(f"p24_spectral_rank_formula=1+7*88+4={p24_spectral_rank}")
    print("interpretation")
    print("  admissible_span_has_conjugate_C_pair_rank_8_not_14=1")
    print("  p24_rank_621_has_spectral_formula_1_plus_7_times_88_plus_4=1")
    print("  proof_target_is_pair_compatibility_not_only_forbidden_support=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary")

    if all_rows_match != len(SMALL_C_DEGREES):
        raise SystemExit(1)
    if p24_spectral_rank != 621:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

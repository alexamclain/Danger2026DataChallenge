#!/usr/bin/env python3
"""Mixed-character module gate for p25 Lane B.

The CM-Artin source gate says the first p25 Lane B lab couples an inert right
source to a split C-axis source.  This gate records the finite character-module
shape that such a ray-local producer must realize.

After scalar normalization, every admissible Jacobi carry decomposes as:

    normalized packet = pure-C line + mixed right-character module.

The mixed module is generically rank 2 over the coefficient field.  It drops to
rank 1 exactly on the explicit degenerate line

    u + 2v == 0 mod c.

That gives a sharper producer falsifier: a construction landing only on the
rank-1 line is an accidental low-rank artifact, not the full inert/split
coupling needed by the p25 moonshot.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import (
    remove_scalar_component,
    packet_matrix,
    rank_mod,
)
from p25_laneB_literal_jacobi_packet_model import (
    admissible_pairs,
    carry_packet,
    representative_pairs,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class MixedModuleCase:
    name: str
    c_axis: int
    exhaustive: bool


CASES = (
    MixedModuleCase("tiny_C3xC13", 13, True),
    MixedModuleCase("prime_axis_C3xC53", 53, True),
    MixedModuleCase("square_axis_C3xC169", 169, False),
)


def decompose_packet(
    c_axis: int, modulus: int, u_value: int, v_value: int
) -> tuple[list[list[int]], list[int], list[list[int]]]:
    packet, _scalar = remove_scalar_component(
        carry_packet(c_axis, u_value, v_value, modulus), modulus
    )
    matrix = packet_matrix(packet, c_axis)
    inv_right = pow(RIGHT_DEGREE, -1, modulus)
    pure_c = [
        sum(matrix[right][c_index] for right in range(RIGHT_DEGREE))
        * inv_right
        % modulus
        for c_index in range(c_axis)
    ]
    mixed = [
        [
            (matrix[right][c_index] - pure_c[c_index]) % modulus
            for c_index in range(c_axis)
        ]
        for right in range(RIGHT_DEGREE)
    ]
    return matrix, pure_c, mixed


def is_degenerate_line(c_axis: int, u_value: int, v_value: int) -> bool:
    return (u_value + 2 * v_value) % c_axis == 0


def support_count(values: list[int] | list[list[int]], modulus: int) -> int:
    if values and isinstance(values[0], list):
        return sum(1 for row in values for value in row if value % modulus)
    return sum(1 for value in values if value % modulus)


def audit_case(case: MixedModuleCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = (
        admissible_pairs(case.c_axis)
        if case.exhaustive
        else representative_pairs(case.c_axis)
    )

    full_rank_counts: dict[int, int] = {}
    pure_c_rank_counts: dict[int, int] = {}
    mixed_rank_counts: dict[int, int] = {}
    pure_c_support_counts: dict[int, int] = {}
    mixed_support_counts: dict[int, int] = {}
    degenerate_count = 0
    degenerate_rank1_hits = 0
    nondegenerate_rank2_hits = 0
    direct_sum_hits = 0
    pure_c_full_support_hits = 0
    examples_rank1: list[tuple[int, int]] = []
    examples_rank2: list[tuple[int, int]] = []

    for u_value, v_value in pairs:
        matrix, pure_c, mixed = decompose_packet(
            case.c_axis, modulus, u_value, v_value
        )
        full_rank = rank_mod(matrix, modulus)
        pure_c_matrix = [pure_c[:] for _ in range(RIGHT_DEGREE)]
        pure_c_rank = rank_mod(pure_c_matrix, modulus)
        mixed_rank = rank_mod(mixed, modulus)
        degenerate = is_degenerate_line(case.c_axis, u_value, v_value)

        full_rank_counts[full_rank] = full_rank_counts.get(full_rank, 0) + 1
        pure_c_rank_counts[pure_c_rank] = pure_c_rank_counts.get(pure_c_rank, 0) + 1
        mixed_rank_counts[mixed_rank] = mixed_rank_counts.get(mixed_rank, 0) + 1
        pure_support = support_count(pure_c, modulus)
        mixed_support = support_count(mixed, modulus)
        pure_c_support_counts[pure_support] = pure_c_support_counts.get(pure_support, 0) + 1
        mixed_support_counts[mixed_support] = mixed_support_counts.get(mixed_support, 0) + 1

        degenerate_count += int(degenerate)
        degenerate_rank1_hits += int(degenerate and mixed_rank == 1 and full_rank == 2)
        nondegenerate_rank2_hits += int(
            (not degenerate) and mixed_rank == 2 and full_rank == 3
        )
        direct_sum_hits += int(full_rank == pure_c_rank + mixed_rank)
        pure_c_full_support_hits += int(pure_support == case.c_axis)

        if mixed_rank == 1 and len(examples_rank1) < 6:
            examples_rank1.append((u_value, v_value))
        if mixed_rank == 2 and len(examples_rank2) < 6:
            examples_rank2.append((u_value, v_value))

    pair_count = len(pairs)
    expected_degenerate = 2 * (case.c_axis - 1) if case.exhaustive else degenerate_count
    row_ok = (
        pure_c_rank_counts == {1: pair_count}
        and pure_c_full_support_hits == pair_count
        and direct_sum_hits == pair_count
        and degenerate_count == expected_degenerate
        and degenerate_rank1_hits == degenerate_count
        and nondegenerate_rank2_hits == pair_count - degenerate_count
    )

    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"pairs_checked={pair_count} exhaustive={int(case.exhaustive)} "
            f"degenerate_line_pairs={degenerate_count} "
            f"expected_degenerate_line_pairs={expected_degenerate} "
            f"pure_c_rank_counts={dict(sorted(pure_c_rank_counts.items()))} "
            f"mixed_rank_counts={dict(sorted(mixed_rank_counts.items()))} "
            f"full_rank_counts={dict(sorted(full_rank_counts.items()))} "
            f"pure_c_full_support_hits={pure_c_full_support_hits}/{pair_count} "
            f"direct_sum_hits={direct_sum_hits}/{pair_count} "
            f"degenerate_rank1_hits={degenerate_rank1_hits}/{degenerate_count} "
            f"nondegenerate_rank2_hits={nondegenerate_rank2_hits}/{pair_count - degenerate_count} "
            f"ok={int(row_ok)}"
        ),
        f"  pure_c_support_counts={dict(sorted(pure_c_support_counts.items()))}",
        f"  mixed_support_counts={dict(sorted(mixed_support_counts.items()))}",
        f"  rank1_examples={examples_rank1}",
        f"  rank2_examples={examples_rank2}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B mixed-character module gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"mixed_character_module_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  scalar_normalized_packet_splits_as_pure_C_line_plus_mixed_module=1")
    print("  mixed_module_is_generically_rank_2_over_the_right_axis=1")
    print("  rank_1_drop_occurs_exactly_on_u_plus_2v_equals_0_mod_c=1")
    print("  producer_should_target_non_degenerate_rank_2_inert_split_coupling=1")
    print("  rank_1_only_constructions_are_accidental_degenerate_artifacts=1")
    print("conclusion=reported_p25_laneB_mixed_character_module_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

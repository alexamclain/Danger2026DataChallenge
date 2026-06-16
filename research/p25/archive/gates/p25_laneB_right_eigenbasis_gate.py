#!/usr/bin/env python3
"""Right-character eigenbasis gate for p25 Lane B.

The mixed-character module gate shows that the scalar-normalized packet splits
as a pure-C line plus a mixed right module.  This gate diagonalizes that mixed
module under the right C_3 action.

The producer-facing meaning is simple: the inert right source has two
nontrivial C_3 characters.  A serious ray-local producer must supply two
independent C-axis coefficient vectors for those two characters.  The explicit
degenerate line u + 2v == 0 mod c is exactly where those two eigenvectors
coincide, dropping the mixed module to rank 1.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root, rank_mod
from p25_laneB_literal_jacobi_packet_model import (
    admissible_pairs,
    representative_pairs,
)
from p25_laneB_mixed_character_module_gate import (
    decompose_packet,
    is_degenerate_line,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class EigenCase:
    name: str
    c_axis: int
    exhaustive: bool


CASES = (
    EigenCase("tiny_C3xC13", 13, True),
    EigenCase("prime_axis_C3xC53", 53, True),
    EigenCase("square_axis_C3xC169", 169, False),
)


def right_root(modulus: int) -> int:
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    if zeta == 1 or pow(zeta, RIGHT_DEGREE, modulus) != 1:
        raise AssertionError("bad right root")
    return zeta


def right_eigenvectors(
    mixed: list[list[int]], c_axis: int, modulus: int
) -> tuple[list[int], list[int], list[int]]:
    zeta = right_root(modulus)
    inv_right = pow(RIGHT_DEGREE, -1, modulus)
    vectors: list[list[int]] = []
    for character in range(RIGHT_DEGREE):
        vector: list[int] = []
        for c_index in range(c_axis):
            total = 0
            for right in range(RIGHT_DEGREE):
                total += mixed[right][c_index] * pow(zeta, character * right, modulus)
            vector.append(total * inv_right % modulus)
        vectors.append(vector)
    return vectors[0], vectors[1], vectors[2]


def reconstruct_mixed(
    eigen_1: list[int], eigen_2: list[int], modulus: int
) -> list[list[int]]:
    zeta = right_root(modulus)
    c_axis = len(eigen_1)
    rows: list[list[int]] = []
    for right in range(RIGHT_DEGREE):
        row: list[int] = []
        for c_index in range(c_axis):
            value = (
                eigen_1[c_index] * pow(zeta, -right, modulus)
                + eigen_2[c_index] * pow(zeta, -2 * right, modulus)
            ) % modulus
            row.append(value)
        rows.append(row)
    return rows


def support_count(vector: list[int], modulus: int) -> int:
    return sum(1 for value in vector if value % modulus)


def scalar_ratio(left: list[int], right: list[int], modulus: int) -> int | None:
    ratio: int | None = None
    for left_value, right_value in zip(left, right):
        if left_value % modulus:
            current = right_value * pow(left_value, -1, modulus) % modulus
            if ratio is None:
                ratio = current
            elif ratio != current:
                return None
        elif right_value % modulus:
            return None
    return ratio


def audit_case(case: EigenCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = (
        admissible_pairs(case.c_axis)
        if case.exhaustive
        else representative_pairs(case.c_axis)
    )

    e0_zero_hits = 0
    reconstruction_hits = 0
    both_nonzero_hits = 0
    eigen_rank_counts: dict[int, int] = {}
    ratio_counts: dict[str, int] = {}
    support_pair_counts: dict[tuple[int, int], int] = {}
    degenerate_count = 0
    degenerate_equal_hits = 0
    nondegenerate_independent_hits = 0
    canonical_summary: str | None = None

    for u_value, v_value in pairs:
        _matrix, _pure_c, mixed = decompose_packet(
            case.c_axis, modulus, u_value, v_value
        )
        eigen_0, eigen_1, eigen_2 = right_eigenvectors(mixed, case.c_axis, modulus)
        eigen_rank = rank_mod([eigen_1, eigen_2], modulus)
        ratio = scalar_ratio(eigen_1, eigen_2, modulus)
        degenerate = is_degenerate_line(case.c_axis, u_value, v_value)
        reconstructed = reconstruct_mixed(eigen_1, eigen_2, modulus)
        support_pair = (
            support_count(eigen_1, modulus),
            support_count(eigen_2, modulus),
        )

        e0_zero_hits += int(all(value % modulus == 0 for value in eigen_0))
        reconstruction_hits += int(reconstructed == mixed)
        both_nonzero_hits += int(support_pair[0] > 0 and support_pair[1] > 0)
        eigen_rank_counts[eigen_rank] = eigen_rank_counts.get(eigen_rank, 0) + 1
        ratio_key = "independent" if ratio is None else str(ratio)
        ratio_counts[ratio_key] = ratio_counts.get(ratio_key, 0) + 1
        support_pair_counts[support_pair] = support_pair_counts.get(support_pair, 0) + 1
        degenerate_count += int(degenerate)
        degenerate_equal_hits += int(degenerate and ratio == 1 and eigen_rank == 1)
        nondegenerate_independent_hits += int(
            (not degenerate) and ratio is None and eigen_rank == 2
        )

        if u_value == RIGHT_DEGREE and v_value == 1:
            canonical_summary = (
                f"canonical_theta_3_1: eigen_rank={eigen_rank} "
                f"support_pair={support_pair} ratio={ratio_key} "
                f"degenerate={int(degenerate)}"
            )

    pair_count = len(pairs)
    expected_degenerate = 2 * (case.c_axis - 1) if case.exhaustive else degenerate_count
    row_ok = (
        e0_zero_hits == pair_count
        and reconstruction_hits == pair_count
        and both_nonzero_hits == pair_count
        and degenerate_count == expected_degenerate
        and degenerate_equal_hits == degenerate_count
        and nondegenerate_independent_hits == pair_count - degenerate_count
        and canonical_summary is not None
    )

    degenerate_denominator = degenerate_count if degenerate_count else 1
    nondegenerate_count = pair_count - degenerate_count
    nondegenerate_denominator = nondegenerate_count if nondegenerate_count else 1
    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"pairs_checked={pair_count} exhaustive={int(case.exhaustive)} "
            f"e0_zero_hits={e0_zero_hits}/{pair_count} "
            f"reconstruction_hits={reconstruction_hits}/{pair_count} "
            f"both_nonzero_hits={both_nonzero_hits}/{pair_count} "
            f"degenerate_line_pairs={degenerate_count} "
            f"expected_degenerate_line_pairs={expected_degenerate} "
            f"eigen_rank_counts={dict(sorted(eigen_rank_counts.items()))} "
            f"ratio_counts={dict(sorted(ratio_counts.items()))} "
            f"degenerate_equal_hits={degenerate_equal_hits}/{degenerate_denominator} "
            f"nondegenerate_independent_hits={nondegenerate_independent_hits}/{nondegenerate_denominator} "
            f"ok={int(row_ok)}"
        ),
        f"  support_pair_counts={dict(sorted(support_pair_counts.items()))}",
        f"  {canonical_summary}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B right-character eigenbasis gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"right_eigenbasis_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  mixed_module_diagonalizes_into_two_nontrivial_right_character_eigenvectors=1")
    print("  both_eigenvectors_are_nonzero_for_every_admissible_packet=1")
    print("  nondegenerate_packets_have_independent_right_eigenvectors=1")
    print("  degenerate_line_is_exactly_eigenvector_equality_E1_equals_E2=1")
    print("  producer_must_supply_two_independent_C_axis_coefficient_vectors=1")
    print("conclusion=reported_p25_laneB_right_eigenbasis_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

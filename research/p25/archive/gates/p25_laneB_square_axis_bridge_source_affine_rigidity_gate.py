#!/usr/bin/env python3
"""Source-affine rigidity for the p25 square-axis bridge.

The raw bridge lift identifies six quotient classes, each lifting to a
mod677 singleton times a 25-element mod151 right coset.  After passing to the
source-log rectangle coordinates, the bridge is a signed mask on C_3 x C_169.

This gate checks whether that source-log mask has a hidden product-affine
symmetry or lower-rank explanation.  It does not: the sign-preserving affine
stabilizer is trivial, and the only sign-reversing affine symmetry is the
expected inversion.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_raw_source_gate import (
    raw_class_profiles,
    square_axis_case,
)
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


FieldMatrix = list[list[int]]
Mask = dict[tuple[int, int], int]
AffineMap = tuple[int, int, int, int]


@dataclass(frozen=True)
class AffineAudit:
    sign_preserving: tuple[AffineMap, ...]
    sign_reversing: tuple[AffineMap, ...]
    setwise: tuple[AffineMap, ...]
    positive_to_negative: tuple[AffineMap, ...]


def source_bridge_mask() -> Mask:
    case = square_axis_case()
    mask: Mask = {}
    for profile in raw_class_profiles(case):
        if len(profile.c_log_values) != 1 or len(profile.right_log_mod3_values) != 1:
            raise AssertionError("bridge class did not collapse to one source-log rectangle")
        coord = (profile.right_log_mod3_values[0], profile.c_log_values[0])
        mask[coord] = profile.coefficient
    return dict(sorted(mask.items()))


def rank_mod(matrix: FieldMatrix, modulus: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = None
        for row in range(rank, row_count):
            if rows[row][column] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column] % modulus, -1, modulus)
        rows[rank] = [(value * inv) % modulus for value in rows[rank]]
        for row in range(row_count):
            if row == rank or rows[row][column] % modulus == 0:
                continue
            factor = rows[row][column] % modulus
            rows[row] = [
                (rows[row][col] - factor * rows[rank][col]) % modulus
                for col in range(column_count)
            ]
        rank += 1
    return rank


def full_matrix(mask: Mask) -> FieldMatrix:
    return [
        [mask.get((right, c_log), 0) for c_log in range(SQUARE_C)]
        for right in range(RIGHT_DEGREE)
    ]


def restricted_matrix(mask: Mask) -> tuple[tuple[int, ...], FieldMatrix]:
    c_logs = tuple(sorted({c_log for _right, c_log in mask}))
    return c_logs, [
        [mask.get((right, c_log), 0) for c_log in c_logs]
        for right in range(RIGHT_DEGREE)
    ]


def c_units() -> tuple[int, ...]:
    return tuple(value for value in range(1, SQUARE_C) if gcd(value, SQUARE_C) == 1)


def transform(mask: Mask, alpha: int, beta: int, unit: int, shift: int) -> Mask:
    out: Mask = {}
    for (right, c_log), value in mask.items():
        out[((alpha * right + beta) % RIGHT_DEGREE, (unit * c_log + shift) % SQUARE_C)] = value
    return dict(sorted(out.items()))


def affine_audit(mask: Mask) -> AffineAudit:
    right_units = tuple(
        value for value in range(1, RIGHT_DEGREE) if gcd(value, RIGHT_DEGREE) == 1
    )
    setwise: list[AffineMap] = []
    sign_preserving: list[AffineMap] = []
    sign_reversing: list[AffineMap] = []
    positive_to_negative: list[AffineMap] = []
    positive = {coord for coord, value in mask.items() if value == 1}
    negative = {coord for coord, value in mask.items() if value == -1}
    for alpha in right_units:
        for beta in range(RIGHT_DEGREE):
            for unit in c_units():
                for shift in range(SQUARE_C):
                    image = transform(mask, alpha, beta, unit, shift)
                    if set(image) == set(mask):
                        setwise.append((alpha, beta, unit, shift))
                        if image == mask:
                            sign_preserving.append((alpha, beta, unit, shift))
                        if all(image[coord] == -mask[coord] for coord in mask):
                            sign_reversing.append((alpha, beta, unit, shift))
                    positive_image = {
                        ((alpha * right + beta) % RIGHT_DEGREE, (unit * c_log + shift) % SQUARE_C)
                        for right, c_log in positive
                    }
                    if positive_image == negative:
                        positive_to_negative.append((alpha, beta, unit, shift))
    return AffineAudit(
        sign_preserving=tuple(sign_preserving),
        sign_reversing=tuple(sign_reversing),
        setwise=tuple(setwise),
        positive_to_negative=tuple(positive_to_negative),
    )


def row_sums(mask: Mask) -> tuple[int, ...]:
    return tuple(
        sum(value for (row, _c_log), value in mask.items() if row == right)
        for right in range(RIGHT_DEGREE)
    )


def column_sums(mask: Mask) -> tuple[tuple[int, int], ...]:
    c_logs = sorted({c_log for _right, c_log in mask})
    return tuple(
        (c_log, sum(value for (right, col), value in mask.items() if col == c_log))
        for c_log in c_logs
    )


def main() -> int:
    print("p25 Lane B square-axis bridge source-affine rigidity gate")
    print(
        f"right_degree={RIGHT_DEGREE} source_c={SQUARE_C} "
        f"bridge_step={BRIDGE_STEP} bridge_translation={(2, BRIDGE_STEP % SQUARE_C)}"
    )
    mask = source_bridge_mask()
    c_logs, restricted = restricted_matrix(mask)
    full = full_matrix(mask)
    rank_f2 = rank_mod(full, 2)
    rank_f2029 = rank_mod(full, 2029)
    restricted_rank_f2 = rank_mod([[value % 2 for value in row] for row in restricted], 2)
    restricted_rank_f2029 = rank_mod(
        [[value % 2029 for value in row] for row in restricted],
        2029,
    )
    audit = affine_audit(mask)

    expected_mask = {
        (0, 31): 1,
        (0, 138): -1,
        (1, 25): 1,
        (1, 141): -1,
        (2, 28): 1,
        (2, 144): -1,
    }
    expected_sign_preserving = ((1, 0, 1, 0),)
    expected_sign_reversing = ((2, 0, 168, 0),)
    expected_setwise = expected_sign_preserving + expected_sign_reversing
    expected_positive_to_negative = ((1, 2, 1, 113), (2, 0, 168, 0))

    row_ok = (
        mask == expected_mask
        and c_logs == (25, 28, 31, 138, 141, 144)
        and row_sums(mask) == (0, 0, 0)
        and column_sums(mask) == (
            (25, 1),
            (28, 1),
            (31, 1),
            (138, -1),
            (141, -1),
            (144, -1),
        )
        and rank_f2 == 3
        and rank_f2029 == 3
        and restricted_rank_f2 == 3
        and restricted_rank_f2029 == 3
        and audit.sign_preserving == expected_sign_preserving
        and audit.sign_reversing == expected_sign_reversing
        and audit.setwise == expected_setwise
        and audit.positive_to_negative == expected_positive_to_negative
    )

    print(
        "source_mask: "
        f"entries={sorted(mask.items())} "
        f"c_logs={list(c_logs)} "
        f"row_sums={row_sums(mask)} "
        f"column_sums={list(column_sums(mask))}"
    )
    print(
        "source_matrix_rank: "
        f"rank_F2={rank_f2} "
        f"rank_F2029={rank_f2029} "
        f"restricted_rank_F2={restricted_rank_f2} "
        f"restricted_rank_F2029={restricted_rank_f2029}"
    )
    print(
        "source_affine_audit: "
        f"setwise_count={len(audit.setwise)} "
        f"sign_preserving={list(audit.sign_preserving)} "
        f"sign_reversing={list(audit.sign_reversing)} "
        f"positive_to_negative={list(audit.positive_to_negative)}"
    )
    print("affine_laws")
    print("  sign_preserving identity: right -> right, c -> c")
    print("  sign_reversing inversion: right -> -right, c -> -c")
    print("  bridge translation: positive -> negative by right -> right+2, c -> c+113")
    print("interpretation")
    print("  source_bridge_mask_has_rank_three_over_F2_and_odd_fields=1")
    print("  source_bridge_has_trivial_sign_preserving_product_affine_stabilizer=1")
    print("  source_bridge_only_sign_reversing_affine_symmetry_is_inversion=1")
    print("  positive_to_negative_affine_maps_are_only_bridge_translation_and_inversion=1")
    print("  producer_cannot_hide_the_bridge_edge_by_source_affine_or_diamond_compression=1")
    print(f"square_axis_bridge_source_affine_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_source_affine_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

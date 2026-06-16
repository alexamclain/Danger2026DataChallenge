#!/usr/bin/env python3
"""Source-line lift normal form for the p25 square-axis bridge.

The source-affine rigidity gate shows that the signed bridge mask has no
hidden product-affine disguise.  This gate records the positive source
geometry that remains:

* the positive and negative layers are two parallel length-three D-segments in
  C_3 x C_169, with D = (1,3);
* the bridge edge is the translation T = (2,113);
* although a nonzero C_13 shadow survives, the full C_169 lift is uniquely
  selected by requiring the T-translate of the D-segment to be its inversion.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import (
    Mask,
    rank_mod,
    source_bridge_mask,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


Coord = tuple[int, int]


@dataclass(frozen=True)
class ProjectionProfile:
    modulus: int
    support: tuple[tuple[Coord, int], ...]
    support_size: int
    rank_f2: int
    rank_f2029: int


def translate(points: set[Coord], shift: Coord, modulus: int = SQUARE_C) -> set[Coord]:
    return {
        ((right + shift[0]) % RIGHT_DEGREE, (c_log + shift[1]) % modulus)
        for right, c_log in points
    }


def invert(points: set[Coord], modulus: int = SQUARE_C) -> set[Coord]:
    return {
        ((-right) % RIGHT_DEGREE, (-c_log) % modulus)
        for right, c_log in points
    }


def d_segment(base: Coord, modulus: int = SQUARE_C) -> set[Coord]:
    return translate(
        {base},
        (0, 0),
        modulus,
    ) | {
        ((base[0] + index) % RIGHT_DEGREE, (base[1] + 3 * index) % modulus)
        for index in range(3)
    }


def project_mask(mask: Mask, modulus: int) -> ProjectionProfile:
    projected: dict[Coord, int] = {}
    for (right, c_log), value in mask.items():
        coord = (right, c_log % modulus)
        projected[coord] = projected.get(coord, 0) + value
    projected = {coord: value for coord, value in sorted(projected.items()) if value}
    matrix = [
        [projected.get((right, c_log), 0) for c_log in range(modulus)]
        for right in range(RIGHT_DEGREE)
    ]
    return ProjectionProfile(
        modulus=modulus,
        support=tuple(sorted(projected.items())),
        support_size=len(projected),
        rank_f2=rank_mod([[value % 2 for value in row] for row in matrix], 2),
        rank_f2029=rank_mod([[value % 2029 for value in row] for row in matrix], 2029),
    )


def inversion_compatible_segments(bridge_shift: Coord) -> tuple[tuple[Coord, tuple[Coord, ...], tuple[Coord, ...]], ...]:
    rows: list[tuple[Coord, tuple[Coord, ...], tuple[Coord, ...]]] = []
    for right in range(RIGHT_DEGREE):
        for c_log in range(SQUARE_C):
            positive = d_segment((right, c_log))
            negative = translate(positive, bridge_shift)
            if invert(positive) == negative:
                rows.append(
                    (
                        (right, c_log),
                        tuple(sorted(positive)),
                        tuple(sorted(negative)),
                    )
                )
    return tuple(rows)


def main() -> int:
    print("p25 Lane B square-axis bridge source-line lift gate")
    d_shift = (S_STEP % RIGHT_DEGREE, S_STEP % SQUARE_C)
    bridge_shift = (BRIDGE_STEP % RIGHT_DEGREE, BRIDGE_STEP % SQUARE_C)
    print(
        f"source_group=C_{RIGHT_DEGREE}xC_{SQUARE_C} "
        f"D_shift={d_shift} bridge_shift={bridge_shift}"
    )
    mask = source_bridge_mask()
    positive = {coord for coord, value in mask.items() if value == 1}
    negative = {coord for coord, value in mask.items() if value == -1}
    expected_positive = d_segment((1, 25))
    expected_negative = translate(expected_positive, bridge_shift)
    projections = tuple(project_mask(mask, modulus) for modulus in (1, 13, SQUARE_C))
    compatible_segments = inversion_compatible_segments(bridge_shift)

    expected_projections = (
        ProjectionProfile(1, (), 0, 0, 0),
        ProjectionProfile(
            13,
            (
                ((0, 5), 1),
                ((0, 8), -1),
                ((1, 11), -1),
                ((1, 12), 1),
                ((2, 1), -1),
                ((2, 2), 1),
            ),
            6,
            3,
            3,
        ),
        ProjectionProfile(
            SQUARE_C,
            tuple(sorted(mask.items())),
            6,
            3,
            3,
        ),
    )
    row_ok = (
        d_shift == (1, 3)
        and bridge_shift == (2, 113)
        and positive == expected_positive
        and negative == expected_negative == invert(expected_positive)
        and compatible_segments
        == (((1, 25), tuple(sorted(expected_positive)), tuple(sorted(expected_negative))),)
        and projections == expected_projections
    )

    print(
        "source_line_normal_form: "
        f"positive={sorted(positive)} "
        f"negative={sorted(negative)} "
        f"positive_is_D_segment={int(positive == expected_positive)} "
        f"negative_is_T_translate={int(negative == expected_negative)} "
        f"negative_is_inversion={int(negative == invert(positive))}"
    )
    print(
        "lift_uniqueness: "
        f"candidate_D_segments={RIGHT_DEGREE * SQUARE_C} "
        f"inversion_compatible={len(compatible_segments)} "
        f"compatible_segments={compatible_segments}"
    )
    print("projection_profiles")
    for profile in projections:
        print(f"  {profile}")
    print("source_line_laws")
    print("  D segment: (right,c) -> (right+1,c+3)")
    print("  bridge edge: (right,c) -> (right+2,c+113)")
    print("  C13 shadow is nonzero and rank 3, but C169 inversion-compatible lift is unique")
    print("interpretation")
    print("  bridge_is_two_parallel_D_segments_in_source_logs=1")
    print("  bridge_translation_and_inversion_select_a_unique_C169_lift=1")
    print("  C13_shadow_survives_but_does_not_remove_the_C169_lift_requirement=1")
    print("  producer_must_explain_the_specific_D_segment_lift_not_only_its_C13_shadow=1")
    print(f"square_axis_bridge_source_line_lift_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_source_line_lift_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

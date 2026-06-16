#!/usr/bin/env python3
"""Square-axis imprimitive-lift obstruction for p25 Lane B.

The C_169 square-axis route has a helpful degree-13 Kummer descent, so the next
question is whether it is merely a C_13 lift in disguise.  It is not.

The canonical C_3 x C_169 carry mask has a C_13 trace shadow: summing along
each residue class modulo 13 gives a constant background 6 plus the C_3 x C_13
half-arc mask.  But every C_13 residue class is mixed, the mask is not
13-periodic, and its Fourier support uses every primitive/non-lifted C_169
character.

Thus a square-axis producer cannot just inflate a C_13 producer.  It must
supply a genuine 13-adic refinement of the half-arc while retaining the C_13
trace shadow and the degree-13 anchor descent.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_residue_mask_character_support_gate import character_coefficients
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


BASE_C = 13
SQUARE_C = BASE_C * BASE_C


@dataclass(frozen=True)
class ImprimitiveProfile:
    period_hits: int
    period_total: int
    constant_residue_classes: int
    residue_class_total: int
    trace_shadow_hits: int
    trace_shadow_total: int
    scalar_support: int
    pure_lift_support: int
    pure_nonlift_support: int
    mixed_lift_support: int
    mixed_nonlift_support: int


def mask_matrix(c_axis: int) -> list[list[int]]:
    return [
        [template_bits(c_axis, c_index)[right] for c_index in range(c_axis)]
        for right in range(RIGHT_DEGREE)
    ]


def trace_down_counts(square_mask: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(square_mask[right][residue + BASE_C * fiber] for fiber in range(BASE_C))
            for residue in range(BASE_C)
        ]
        for right in range(RIGHT_DEGREE)
    ]


def character_support_profile() -> tuple[int, int, int, int, int]:
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    coefficients = character_coefficients(SQUARE_C, modulus)
    scalar = 0
    pure_lift = 0
    pure_nonlift = 0
    mixed_lift = 0
    mixed_nonlift = 0
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(SQUARE_C):
            value = coefficients[right_frequency * SQUARE_C + c_frequency]
            if not value:
                continue
            if right_frequency == 0 and c_frequency == 0:
                scalar += 1
            elif right_frequency == 0:
                if c_frequency % BASE_C == 0:
                    pure_lift += 1
                else:
                    pure_nonlift += 1
            elif c_frequency:
                if c_frequency % BASE_C == 0:
                    mixed_lift += 1
                else:
                    mixed_nonlift += 1
    return scalar, pure_lift, pure_nonlift, mixed_lift, mixed_nonlift


def profile() -> ImprimitiveProfile:
    square_mask = mask_matrix(SQUARE_C)
    base_mask = mask_matrix(BASE_C)
    period_hits = sum(
        int(square_mask[right][c_index] == square_mask[right][(c_index + BASE_C) % SQUARE_C])
        for right in range(RIGHT_DEGREE)
        for c_index in range(SQUARE_C)
    )
    constant_residue_classes = 0
    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            values = [
                square_mask[right][residue + BASE_C * fiber]
                for fiber in range(BASE_C)
            ]
            constant_residue_classes += int(len(set(values)) == 1)

    traced = trace_down_counts(square_mask)
    trace_shadow_hits = 0
    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            trace_shadow_hits += int(
                traced[right][residue] == 6 + base_mask[right][residue]
            )

    support = character_support_profile()
    return ImprimitiveProfile(
        period_hits=period_hits,
        period_total=RIGHT_DEGREE * SQUARE_C,
        constant_residue_classes=constant_residue_classes,
        residue_class_total=RIGHT_DEGREE * BASE_C,
        trace_shadow_hits=trace_shadow_hits,
        trace_shadow_total=RIGHT_DEGREE * BASE_C,
        scalar_support=support[0],
        pure_lift_support=support[1],
        pure_nonlift_support=support[2],
        mixed_lift_support=support[3],
        mixed_nonlift_support=support[4],
    )


def main() -> int:
    print("p25 Lane B square-axis imprimitive-lift obstruction gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C}")
    current = profile()
    row_ok = (
        current.period_hits < current.period_total
        and current.constant_residue_classes == 0
        and current.trace_shadow_hits == current.trace_shadow_total
        and current.scalar_support == 1
        and current.pure_lift_support == BASE_C - 1
        and current.pure_nonlift_support == SQUARE_C - BASE_C
        and current.mixed_lift_support == (RIGHT_DEGREE - 1) * (BASE_C - 1)
        and current.mixed_nonlift_support
        == (RIGHT_DEGREE - 1) * (SQUARE_C - BASE_C)
    )
    print(
        f"case square_axis_C3xC169: "
        f"period_13_hits={current.period_hits}/{current.period_total} "
        f"period_13_failures={current.period_total - current.period_hits} "
        f"constant_residue_classes={current.constant_residue_classes}/{current.residue_class_total} "
        f"trace_down_C13_shadow_hits={current.trace_shadow_hits}/{current.trace_shadow_total} "
        f"scalar_support={current.scalar_support}/1 "
        f"pure_lift_support={current.pure_lift_support}/{BASE_C - 1} "
        f"pure_nonlift_support={current.pure_nonlift_support}/{SQUARE_C - BASE_C} "
        f"mixed_lift_support={current.mixed_lift_support}/{(RIGHT_DEGREE - 1) * (BASE_C - 1)} "
        f"mixed_nonlift_support={current.mixed_nonlift_support}/{(RIGHT_DEGREE - 1) * (SQUARE_C - BASE_C)} "
        f"ok={int(row_ok)}"
    )
    print(f"square_axis_imprimitive_lift_obstruction_rows={int(row_ok)}/1")
    print("interpretation")
    print("  C169_mask_is_not_13_periodic_or_a_pullback_from_C13=1")
    print("  C169_mask_traces_down_to_constant_background_plus_C13_half_arc=1")
    print("  C169_mask_uses_every_lifted_and_nonlifted_C_axis_character=1")
    print("  square_axis_producer_needs_genuine_13_adic_refinement_beyond_C13=1")
    print("conclusion=reported_p25_laneB_square_axis_imprimitive_lift_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

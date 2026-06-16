#!/usr/bin/env python3
"""Raw trace-rectangle structure for the p25 square-axis bridge.

The raw source-character and factor-Kummer gates show that the positive bridge
layer is a kernel trace times a short D segment.  This gate records the exact
support geometry in the raw cyclic source C_12675.

The positive support is not a 75-element subgroup or subgroup coset.  It is a
25-kernel trace rectangle over a length-three D segment, with stabilizer
exactly the 25-element trace kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_raw_source_character_gate import BASE_POINT
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_inversion_partner_uniqueness_gate import PARTNER_BASE
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER


KERNEL_RAW_STEP = QUOTIENT_ORDER
D_RAW_STEP = S_STEP
BRIDGE_RAW_STEP = BRIDGE_STEP
POSITIVE_BASE = PARTNER_BASE


@dataclass(frozen=True)
class TraceRectangleProfile:
    raw_order: int
    positive_support_size: int
    negative_support_size: int
    signed_support_size: int
    kernel_order: int
    positive_stabilizer: tuple[int, ...]
    signed_preserving_translations: tuple[int, ...]
    signed_reversing_translations: tuple[int, ...]
    positive_is_subgroup_coset: bool
    positive_closure_fail_witness: tuple[int, int, int]
    d_coordinate_base: int
    kernel_step_in_d_coordinates: int
    bridge_step_in_d_coordinates: int
    d_coordinate_support: tuple[int, ...]
    mod_507_projection: tuple[int, ...]
    mod_75_projection_size: int


def positive_support() -> set[int]:
    return {
        (POSITIVE_BASE + d_index * D_RAW_STEP + kernel_index * KERNEL_RAW_STEP) % RAW_ORDER
        for d_index in range(3)
        for kernel_index in range(25)
    }


def translate(values: set[int], shift: int) -> set[int]:
    return {(value + shift) % RAW_ORDER for value in values}


def closure_fail_witness(values: set[int], base: int) -> tuple[int, int, int]:
    normalized = {(value - base) % RAW_ORDER for value in values}
    for left in sorted(normalized):
        for right in sorted(normalized):
            total = (left + right) % RAW_ORDER
            if total not in normalized:
                return (left, right, total)
    raise AssertionError("set is closed")


def translation_stabilizer(values: set[int]) -> tuple[int, ...]:
    return tuple(
        shift for shift in range(RAW_ORDER) if translate(values, shift) == values
    )


def signed_translation_profiles(positive: set[int], negative: set[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    coefficients = {value: 1 for value in positive}
    coefficients.update({value: -1 for value in negative})
    support = set(coefficients)
    preserving: list[int] = []
    reversing: list[int] = []
    for shift in range(RAW_ORDER):
        if translate(support, shift) != support:
            continue
        if all(coefficients[(value + shift) % RAW_ORDER] == coefficients[value] for value in support):
            preserving.append(shift)
        if all(coefficients[(value + shift) % RAW_ORDER] == -coefficients[value] for value in support):
            reversing.append(shift)
    return tuple(preserving), tuple(reversing)


def trace_rectangle_profile() -> TraceRectangleProfile:
    positive = positive_support()
    negative = translate(positive, BRIDGE_RAW_STEP)
    d_inverse = pow(D_RAW_STEP, -1, RAW_ORDER)
    d_coordinate_base = POSITIVE_BASE * d_inverse % RAW_ORDER
    d_coordinates = tuple(
        sorted(((value - POSITIVE_BASE) * d_inverse) % RAW_ORDER for value in positive)
    )
    positive_stabilizer = translation_stabilizer(positive)
    signed_preserving, signed_reversing = signed_translation_profiles(positive, negative)
    kernel_subgroup = tuple(kernel_index * KERNEL_RAW_STEP for kernel_index in range(25))
    return TraceRectangleProfile(
        raw_order=RAW_ORDER,
        positive_support_size=len(positive),
        negative_support_size=len(negative),
        signed_support_size=len(positive | negative),
        kernel_order=len(kernel_subgroup),
        positive_stabilizer=positive_stabilizer,
        signed_preserving_translations=signed_preserving,
        signed_reversing_translations=signed_reversing,
        positive_is_subgroup_coset=False,
        positive_closure_fail_witness=closure_fail_witness(positive, POSITIVE_BASE),
        d_coordinate_base=d_coordinate_base,
        kernel_step_in_d_coordinates=KERNEL_RAW_STEP * d_inverse % RAW_ORDER,
        bridge_step_in_d_coordinates=BRIDGE_RAW_STEP * d_inverse % RAW_ORDER,
        d_coordinate_support=d_coordinates,
        mod_507_projection=tuple(sorted({coord % QUOTIENT_ORDER for coord in d_coordinates})),
        mod_75_projection_size=len({coord % 75 for coord in d_coordinates}),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge trace-rectangle gate")
    print(
        f"raw_order={RAW_ORDER} base={POSITIVE_BASE} "
        f"kernel_step={KERNEL_RAW_STEP} D_step={D_RAW_STEP} T_step={BRIDGE_RAW_STEP} "
        f"source_base={BASE_POINT}"
    )
    profile = trace_rectangle_profile()
    expected_kernel = tuple(kernel_index * KERNEL_RAW_STEP for kernel_index in range(25))
    expected_d_coords = tuple(
        sorted(kernel_index * QUOTIENT_ORDER + d_index for kernel_index in range(25) for d_index in range(3))
    )
    row_ok = (
        gcd(D_RAW_STEP, RAW_ORDER) == 1
        and profile.positive_support_size == 75
        and profile.negative_support_size == 75
        and profile.signed_support_size == 150
        and profile.kernel_order == 25
        and profile.positive_stabilizer == expected_kernel
        and profile.signed_preserving_translations == expected_kernel
        and profile.signed_reversing_translations == ()
        and not profile.positive_is_subgroup_coset
        and profile.positive_closure_fail_witness == (D_RAW_STEP, 2 * D_RAW_STEP, 3 * D_RAW_STEP)
        and profile.d_coordinate_base == 11275
        and profile.kernel_step_in_d_coordinates == 4056
        and profile.bridge_step_in_d_coordinates == 6854
        and profile.d_coordinate_support == expected_d_coords
        and profile.mod_507_projection == (0, 1, 2)
        and profile.mod_75_projection_size == 75
    )

    print(f"trace_rectangle_profile={profile}")
    print("normal_forms")
    print("  positive = base + <507>_25 + {0,D,2D}")
    print("  in D-coordinates: positive - base = <507>_25 + {0,1,2}")
    print("  positive stabilizer = <507>, exactly 25 elements")
    print("  positive is not a subgroup/coset: raw witness D + 2D = 3D outside the normalized set")
    print("interpretation")
    print("  positive_raw_bridge_layer_is_a_kernel_trace_rectangle_not_a_subgroup_coset=1")
    print("  signed_bridge_translation_stabilizer_is_exactly_the_kernel_trace=1")
    print("  no_translation_flips_positive_and_negative_layers=1")
    print("  producer_must_realize_a_trace_rectangle_not_a_single_raw_subgroup_trace=1")
    print(f"square_axis_bridge_trace_rectangle_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_trace_rectangle_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

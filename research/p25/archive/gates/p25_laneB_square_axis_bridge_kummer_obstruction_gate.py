#!/usr/bin/env python3
"""Kummer obstruction gate for the square-axis bridge source multiplier.

The bridge-primitivity gate shows that the bridge step is a primitive raw
source motion.  This gate checks the corresponding Kummer classes of the
actual local source multipliers:

    45  mod 151,
    667 mod 677.

If a producer tries to explain the bridge by taking roots of this source edge,
the finite fields give no cheap descent.  The C_169 source multiplier has a
primitive C_169 Kummer class, the raw right source has a primitive C_75 Kummer
class, and the sign is already a power in both fields, so changing sign does
not help.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_kummer_sign_descent_gate import KummerClass, kummer_class
from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_raw_source_gate import (
    source_generators,
    square_axis_case,
)


@dataclass(frozen=True)
class BridgeKummerProfile:
    name: str
    modulus: int
    c_axis: int
    multiplier: int
    primitive_root: int
    multiplier_class: KummerClass
    negative_multiplier_class: KummerClass
    sign_class: KummerClass
    class_order: int


def class_order(c_axis: int, class_index: int) -> int:
    if class_index % c_axis == 0:
        return 1
    return c_axis // gcd(c_axis, class_index)


def profile(name: str, modulus: int, c_axis: int, multiplier: int) -> BridgeKummerProfile:
    generator = primitive_root(modulus)
    multiplier_row = kummer_class(
        "multiplier", multiplier, c_axis, modulus, generator
    )
    negative_row = kummer_class(
        "-multiplier", -multiplier, c_axis, modulus, generator
    )
    sign_row = kummer_class("-1", -1, c_axis, modulus, generator)
    return BridgeKummerProfile(
        name=name,
        modulus=modulus,
        c_axis=c_axis,
        multiplier=multiplier % modulus,
        primitive_root=generator,
        multiplier_class=multiplier_row,
        negative_multiplier_class=negative_row,
        sign_class=sign_row,
        class_order=class_order(c_axis, multiplier_row.class_index),
    )


def profile_ok(row: BridgeKummerProfile, expected_index: int, expected_degree: int) -> bool:
    return (
        row.multiplier_class.class_index == expected_index
        and row.negative_multiplier_class.class_index == expected_index
        and row.sign_class.class_index == 0
        and row.class_order == expected_degree
        and not row.multiplier_class.base_has_root
        and row.multiplier_class.minimal_extension_degree == expected_degree
        and row.multiplier_class.root_degrees_up_to_c == (expected_degree,)
        and not row.negative_multiplier_class.base_has_root
        and row.negative_multiplier_class.minimal_extension_degree == expected_degree
        and row.negative_multiplier_class.root_degrees_up_to_c == (expected_degree,)
        and row.sign_class.base_has_root
        and row.sign_class.minimal_extension_degree == 1
        and row.sign_class.root_degrees_up_to_c == tuple(range(1, row.c_axis + 1))
    )


def main() -> int:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_multiplier = pow(right_generator, BRIDGE_STEP, right_source.modulus)
    c_multiplier = pow(c_generator, BRIDGE_STEP, c_source.modulus)

    rows = (
        profile("right_raw_C75", right_source.modulus, right_source.expected_order, right_multiplier),
        profile("right_visible_C3", right_source.modulus, 3, right_multiplier),
        profile("c_axis_C169", c_source.modulus, c_source.expected_order, c_multiplier),
        profile("c_trace_shadow_C13", c_source.modulus, 13, c_multiplier),
    )
    expected = {
        "right_raw_C75": (49, 75),
        "right_visible_C3": (1, 3),
        "c_axis_C169": (128, 169),
        "c_trace_shadow_C13": (11, 13),
    }
    ok_rows = 0
    for row in rows:
        expected_index, expected_degree = expected[row.name]
        ok_rows += int(profile_ok(row, expected_index, expected_degree))

    simultaneous_raw_root_degree = 75 * 169 // gcd(75, 169)
    row_ok = (
        right_multiplier == 45
        and c_multiplier == 667
        and BRIDGE_STEP % right_source.expected_order == 38
        and BRIDGE_STEP % c_source.expected_order == 113
        and ok_rows == len(rows)
        and simultaneous_raw_root_degree == case.raw_order == 12675
    )

    print("p25 Lane B square-axis bridge Kummer obstruction gate")
    print(
        f"case={case.name} bridge_step={BRIDGE_STEP} "
        f"right_multiplier={right_multiplier} c_multiplier={c_multiplier} "
        f"simultaneous_raw_root_degree_lcm={simultaneous_raw_root_degree}"
    )
    for row in rows:
        expected_index, expected_degree = expected[row.name]
        row_pass = profile_ok(row, expected_index, expected_degree)
        print(
            f"profile {row.name}: "
            f"modulus={row.modulus} c_axis={row.c_axis} "
            f"primitive_root={row.primitive_root} "
            f"multiplier={row.multiplier} "
            f"class_index={row.multiplier_class.class_index} "
            f"class_order={row.class_order} "
            f"minimal_extension_degree={row.multiplier_class.minimal_extension_degree} "
            f"root_degrees={list(row.multiplier_class.root_degrees_up_to_c)} "
            f"negative_class_index={row.negative_multiplier_class.class_index} "
            f"negative_minimal_extension_degree={row.negative_multiplier_class.minimal_extension_degree} "
            f"sign_class_index={row.sign_class.class_index} "
            f"sign_base_has_root={int(row.sign_class.base_has_root)} "
            f"expected_index={expected_index} "
            f"expected_degree={expected_degree} "
            f"ok={int(row_pass)}"
        )
    print("interpretation")
    print("  bridge_source_multiplier_has_primitive_C169_kummer_class=1")
    print("  bridge_raw_right_multiplier_has_primitive_C75_kummer_class=1")
    print("  visible_C3_and_C13_shadows_still_need_full_visible_degrees=1")
    print("  sign_choice_does_not_change_any_bridge_multiplier_class=1")
    print("  root_based_raw_source_explanation_would_need_degree_lcm_12675=1")
    print(f"square_axis_bridge_kummer_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_kummer_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

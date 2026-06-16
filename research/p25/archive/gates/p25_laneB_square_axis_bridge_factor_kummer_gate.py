#!/usr/bin/env python3
"""Local source factor orders for the p25 square-axis bridge.

The raw source-character gate factors the raw bridge as

    base * kernel-trace * D-segment * bridge-edge.

This gate translates those three moving factors into actual local source
multipliers and Kummer/order costs.  It also records the raw monodromy:
D^3 equals the quotient Y-shift only after adding the 25-kernel shift.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_kummer_sign_descent_gate import kummer_class
from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP
from p25_laneB_square_axis_bridge_raw_source_gate import (
    source_generators,
    square_axis_case,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Y_RAW_SHIFT = (9, 9)
D_CUBED_SHIFT = ((3 * D_SHIFT[0]) % RIGHT_ORDER, (3 * D_SHIFT[1]) % C_ORDER)


@dataclass(frozen=True)
class FactorOrderProfile:
    name: str
    shift: tuple[int, int]
    right_multiplier: int
    c_multiplier: int
    right_order: int
    c_order: int
    combined_order: int
    right_c75_class_index: int
    right_c75_min_degree: int
    right_c3_class_index: int
    right_c3_min_degree: int
    c_c169_class_index: int
    c_c169_min_degree: int
    c_c13_class_index: int
    c_c13_min_degree: int


def multiplicative_order(value: int, modulus: int, limit: int) -> int:
    acc = 1
    for order in range(1, limit + 1):
        acc = acc * value % modulus
        if acc == 1:
            return order
    raise AssertionError(f"order exceeds {limit}")


def factor_profile(name: str, shift: tuple[int, int]) -> FactorOrderProfile:
    case = square_axis_case()
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    right_multiplier = pow(right_generator, shift[0], right_source.modulus)
    c_multiplier = pow(c_generator, shift[1], c_source.modulus)
    right_order = multiplicative_order(
        right_multiplier,
        right_source.modulus,
        right_source.expected_order,
    )
    c_order = multiplicative_order(
        c_multiplier,
        c_source.modulus,
        c_source.expected_order,
    )
    combined_order = right_order * c_order // gcd(right_order, c_order)
    right_root = primitive_root(right_source.modulus)
    c_root = primitive_root(c_source.modulus)
    right_c75 = kummer_class(name, right_multiplier, right_source.expected_order, right_source.modulus, right_root)
    right_c3 = kummer_class(name, right_multiplier, 3, right_source.modulus, right_root)
    c_c169 = kummer_class(name, c_multiplier, c_source.expected_order, c_source.modulus, c_root)
    c_c13 = kummer_class(name, c_multiplier, 13, c_source.modulus, c_root)
    return FactorOrderProfile(
        name=name,
        shift=shift,
        right_multiplier=right_multiplier,
        c_multiplier=c_multiplier,
        right_order=right_order,
        c_order=c_order,
        combined_order=combined_order,
        right_c75_class_index=right_c75.class_index,
        right_c75_min_degree=right_c75.minimal_extension_degree,
        right_c3_class_index=right_c3.class_index,
        right_c3_min_degree=right_c3.minimal_extension_degree,
        c_c169_class_index=c_c169.class_index,
        c_c169_min_degree=c_c169.minimal_extension_degree,
        c_c13_class_index=c_c13.class_index,
        c_c13_min_degree=c_c13.minimal_extension_degree,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge factor Kummer/order gate")
    print(
        f"raw_source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"kernel={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT} "
        f"Y_raw={Y_RAW_SHIFT} D_cubed={D_CUBED_SHIFT}"
    )
    profiles = (
        factor_profile("kernel_trace", KERNEL_SHIFT),
        factor_profile("D_segment", D_SHIFT),
        factor_profile("bridge_edge", BRIDGE_SHIFT),
        factor_profile("Y_raw", Y_RAW_SHIFT),
        factor_profile("D_cubed", D_CUBED_SHIFT),
    )
    expected = (
        FactorOrderProfile("kernel_trace", (57, 0), 125, 1, 25, 1, 25, 36, 25, 0, 1, 0, 1, 0, 1),
        FactorOrderProfile("D_segment", (22, 3), 55, 85, 75, 169, 12675, 56, 75, 2, 3, 138, 169, 8, 13),
        FactorOrderProfile("bridge_edge", (38, 113), 45, 667, 75, 169, 12675, 49, 75, 1, 3, 128, 169, 11, 13),
        FactorOrderProfile("Y_raw", (9, 9), 123, 86, 25, 169, 4225, 57, 25, 0, 1, 76, 169, 11, 13),
        FactorOrderProfile("D_cubed", (66, 9), 124, 86, 25, 169, 4225, 18, 25, 0, 1, 76, 169, 11, 13),
    )
    d3_minus_y = (
        (D_CUBED_SHIFT[0] - Y_RAW_SHIFT[0]) % RIGHT_ORDER,
        (D_CUBED_SHIFT[1] - Y_RAW_SHIFT[1]) % C_ORDER,
    )
    row_ok = (
        profiles == expected
        and BRIDGE_SHIFT == (BRIDGE_STEP % RIGHT_ORDER, BRIDGE_STEP % C_ORDER)
        and d3_minus_y == KERNEL_SHIFT
        and KERNEL_SHIFT[0] % 3 == 0
        and KERNEL_SHIFT[1] == 0
    )

    print("factor_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print(
        "raw_monodromy: "
        f"D_cubed_minus_Y={d3_minus_y} "
        f"equals_kernel={int(d3_minus_y == KERNEL_SHIFT)} "
        f"kernel_invisible_mod_C3xC169={int(KERNEL_SHIFT[0] % 3 == 0 and KERNEL_SHIFT[1] == 0)}"
    )
    print("interpretation")
    print("  kernel_trace_factor_has_order_25_and_kummer_degree_25_on_right_source=1")
    print("  D_segment_factor_is_primitive_order_12675_on_raw_sources=1")
    print("  bridge_edge_factor_is_primitive_order_12675_on_raw_sources=1")
    print("  D_cubed_equals_Y_only_after_the_25_kernel_shift_is_traced_out=1")
    print("  producer_must_account_for_kernel_trace_D_segment_and_bridge_edge_separately=1")
    print(f"square_axis_bridge_factor_kummer_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_factor_kummer_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

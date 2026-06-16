#!/usr/bin/env python3
"""Split-right versus nonsplit-C local source contrast for the p25 bridge.

The formal bridge word has two very different local axes:

* the right source modulo 151 is cyclic C_75, and because 75 = 3 * 25 with
  coprime factors it splits as C_3 x C_25.  The 25-point K factor is an honest
  trace over the right kernel, and the visible C_3 classes have order-3
  representatives;
* the C source modulo 677 is cyclic C_169.  Its kernel over the visible C_13
  quotient has no C_13 complement, so the C_169 carry cannot be split into
  independent low/fiber units.

This gate records that asymmetry explicitly.  It helps future producer
candidates aim at the real hard part: the right K-trace is a normal split
trace, while the C-axis bridge factors must use primitive cyclic C_169 units.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_factor_kummer_gate import factor_profile
from p25_laneB_square_axis_bridge_raw_source_gate import source_generators, square_axis_case
from p25_laneB_square_axis_bridge_raw_source_character_gate import BRIDGE_SHIFT, D_SHIFT, KERNEL_SHIFT


@dataclass(frozen=True)
class AxisSplitContrastProfile:
    right_modulus: int
    right_generator: int
    right_order: int
    right_kernel_generator: int
    right_kernel_order: int
    right_order3_exponents: tuple[int, ...]
    right_complement_exponents: tuple[int, int, int]
    right_complement_values: tuple[int, int, int]
    right_nonzero_low_order3_lifts: tuple[tuple[int, int], ...]
    right_split_exists: bool
    c_modulus: int
    c_generator: int
    c_order: int
    c_kernel_generator: int
    c_kernel_order: int
    c_order13_exponents: tuple[int, ...]
    c_order13_low_residues: tuple[int, ...]
    c_nonzero_low_section_orders: tuple[tuple[int, tuple[int, ...]], ...]
    c_split_exists: bool
    k_right_low: int
    k_right_kernel_index: int
    d_right_low: int
    d_right_kernel_index: int
    t_right_low: int
    t_right_kernel_index: int
    d_c_low: int
    d_c_section_orders: tuple[int, ...]
    t_c_low: int
    t_c_section_orders: tuple[int, ...]
    k_right_min_degree: int
    d_right_visible_min_degree: int
    t_right_visible_min_degree: int
    d_c_visible_min_degree: int
    t_c_visible_min_degree: int
    d_c_full_min_degree: int
    t_c_full_min_degree: int


def cyclic_order(order: int, exponent: int) -> int:
    if exponent % order == 0:
        return 1
    return order // gcd(order, exponent)


def right_kernel_index(exponent: int) -> int:
    low = exponent % 3
    complement_exponent = 25 * low
    kernel_exponent = (exponent - complement_exponent) % 75
    if kernel_exponent % 3 != 0:
        raise AssertionError("right kernel component is not in <g^3>")
    return (kernel_exponent // 3) % 25


def c_section_orders(low: int) -> tuple[int, ...]:
    return tuple(sorted({cyclic_order(169, low + 13 * fiber) for fiber in range(13)}))


def profile_axis_contrast() -> AxisSplitContrastProfile:
    case = square_axis_case()
    right_generator, c_generator = source_generators(case)
    right_modulus = case.right_sources[0].modulus
    c_modulus = case.c_source.modulus
    right_order3_exponents = tuple(exponent for exponent in range(75) if cyclic_order(75, exponent) == 3)
    right_complement_exponents = (0, 25, 50)
    right_complement_values = tuple(pow(right_generator, exponent, right_modulus) for exponent in right_complement_exponents)
    right_low_lifts = tuple((low, 25 * low) for low in (1, 2))
    c_order13_exponents = tuple(exponent for exponent in range(1, 169) if cyclic_order(169, exponent) == 13)
    c_order13_low_residues = tuple(sorted({exponent % 13 for exponent in c_order13_exponents}))
    c_sections = tuple((low, c_section_orders(low)) for low in range(1, 13))

    k_profile = factor_profile("kernel_trace", KERNEL_SHIFT)
    d_profile = factor_profile("D_segment", D_SHIFT)
    t_profile = factor_profile("bridge_edge", BRIDGE_SHIFT)

    return AxisSplitContrastProfile(
        right_modulus=right_modulus,
        right_generator=right_generator,
        right_order=cyclic_order(75, 1),
        right_kernel_generator=pow(right_generator, 3, right_modulus),
        right_kernel_order=cyclic_order(75, 3),
        right_order3_exponents=right_order3_exponents,
        right_complement_exponents=right_complement_exponents,
        right_complement_values=right_complement_values,
        right_nonzero_low_order3_lifts=right_low_lifts,
        right_split_exists=all(cyclic_order(75, exponent) == 3 for _low, exponent in right_low_lifts),
        c_modulus=c_modulus,
        c_generator=c_generator,
        c_order=cyclic_order(169, 1),
        c_kernel_generator=pow(c_generator, 13, c_modulus),
        c_kernel_order=cyclic_order(169, 13),
        c_order13_exponents=c_order13_exponents,
        c_order13_low_residues=c_order13_low_residues,
        c_nonzero_low_section_orders=c_sections,
        c_split_exists=any(13 in orders for _low, orders in c_sections),
        k_right_low=KERNEL_SHIFT[0] % 3,
        k_right_kernel_index=right_kernel_index(KERNEL_SHIFT[0]),
        d_right_low=D_SHIFT[0] % 3,
        d_right_kernel_index=right_kernel_index(D_SHIFT[0]),
        t_right_low=BRIDGE_SHIFT[0] % 3,
        t_right_kernel_index=right_kernel_index(BRIDGE_SHIFT[0]),
        d_c_low=D_SHIFT[1] % 13,
        d_c_section_orders=c_section_orders(D_SHIFT[1] % 13),
        t_c_low=BRIDGE_SHIFT[1] % 13,
        t_c_section_orders=c_section_orders(BRIDGE_SHIFT[1] % 13),
        k_right_min_degree=k_profile.right_c75_min_degree,
        d_right_visible_min_degree=d_profile.right_c3_min_degree,
        t_right_visible_min_degree=t_profile.right_c3_min_degree,
        d_c_visible_min_degree=d_profile.c_c13_min_degree,
        t_c_visible_min_degree=t_profile.c_c13_min_degree,
        d_c_full_min_degree=d_profile.c_c169_min_degree,
        t_c_full_min_degree=t_profile.c_c169_min_degree,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge local-axis split contrast gate")
    profile = profile_axis_contrast()
    row_ok = (
        profile.right_modulus == 151
        and profile.right_generator == 62
        and profile.right_order == 75
        and profile.right_kernel_generator == 50
        and profile.right_kernel_order == 25
        and profile.right_order3_exponents == (25, 50)
        and profile.right_complement_exponents == (0, 25, 50)
        and profile.right_complement_values == (1, 32, 118)
        and profile.right_nonzero_low_order3_lifts == ((1, 25), (2, 50))
        and profile.right_split_exists
        and profile.c_modulus == 677
        and profile.c_generator == 354
        and profile.c_order == 169
        and profile.c_kernel_generator == 246
        and profile.c_kernel_order == 13
        and profile.c_order13_exponents == tuple(range(13, 169, 13))
        and profile.c_order13_low_residues == (0,)
        and profile.c_nonzero_low_section_orders == tuple((low, (169,)) for low in range(1, 13))
        and not profile.c_split_exists
        and profile.k_right_low == 0
        and profile.k_right_kernel_index == 19
        and profile.d_right_low == 1
        and profile.d_right_kernel_index == 24
        and profile.t_right_low == 2
        and profile.t_right_kernel_index == 21
        and profile.d_c_low == 3
        and profile.d_c_section_orders == (169,)
        and profile.t_c_low == 9
        and profile.t_c_section_orders == (169,)
        and profile.k_right_min_degree == 25
        and profile.d_right_visible_min_degree == 3
        and profile.t_right_visible_min_degree == 3
        and profile.d_c_visible_min_degree == 13
        and profile.t_c_visible_min_degree == 13
        and profile.d_c_full_min_degree == 169
        and profile.t_c_full_min_degree == 169
    )

    print(f"axis_split_contrast_profile={profile}")
    print("right_axis_laws")
    print("  mod151 source is cyclic C75 generated by 62")
    print("  C75 splits as C25 kernel <62^3=50> times C3 complement {1,62^25,62^50}")
    print("  K=(57,0) is a pure right-kernel trace component with kernel index 19")
    print("  D and T have visible right C3 classes plus right-kernel indices 24 and 21")
    print("c_axis_laws")
    print("  mod677 source is cyclic C169 generated by 354")
    print("  order-13 C elements are exactly the projection kernel and have low residue 0")
    print("  every nonzero visible C13 class has only order-169 lifts")
    print("  D_c and T_c therefore require primitive C169 source units")
    print("interpretation")
    print("  right_kernel_trace_is_a_split_local_trace=1")
    print("  c_axis_carry_is_the_nonsplit_hard_part=1")
    print("  producer_can_split_the_right_axis_but_not_the_C169_axis=1")
    print("  independent_C13_fiber_units_are_not_available_on_the_actual_C_source=1")
    print(f"square_axis_bridge_local_axis_split_contrast_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_local_axis_split_contrast_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

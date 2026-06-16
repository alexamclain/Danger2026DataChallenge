#!/usr/bin/env python3
"""Primitive D-coordinate normal form for the p25 square-axis bridge.

The bridge factor gates work in raw source axes C_75 x C_169.  The D segment
step itself is primitive in that product, so the same finite payload has a
one-generator group-ring expression:

    z^11275 * (sum_{j=0}^{24} z^(4056*j)) * (1 + z + z^2) * (1 - z^6854).

This is a positive producer-facing normal form.  It does not remove the
Kummer/monodromy cost, but it says an arithmetic realization can target one
primitive local source coordinate instead of treating K, D, and T as unrelated
axes.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_candidate_harness_gate import profile_candidate, target_raw_bridge
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_laneB_square_axis_bridge_raw_source_gate import source_generators, square_axis_case
from p25_laneB_square_axis_bridge_factor_kummer_gate import factor_profile
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


Coord = tuple[int, int]
Poly = dict[int, int]


@dataclass(frozen=True)
class PrimitiveDCoordinateProfile:
    d_shift: Coord
    d_right_multiplier: int
    d_c_multiplier: int
    d_order: int
    d_combined_kummer_order: int
    base_exponent: int
    kernel_exponent: int
    bridge_exponent: int
    y_exponent: int
    kernel_order: int
    bridge_order: int
    y_order: int
    d_cubed_relation: bool
    kernel_trace_exponents_first: tuple[int, ...]
    kernel_trace_exponents_last: tuple[int, ...]
    product_support: int
    product_degree: int
    coefficient_counts: tuple[tuple[int, int], ...]
    source_mask_exact: bool
    harness_ok: bool
    one_generator_payload_below_sqrt: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def scale_coord(step: Coord, count: int) -> Coord:
    return ((step[0] * count) % RIGHT_ORDER, (step[1] * count) % C_ORDER)


def coordinate_order(step: Coord) -> int:
    for order in range(1, RAW_ORDER + 1):
        if scale_coord(step, order) == (0, 0):
            return order
    raise AssertionError("coordinate order exceeds raw order")


def solve_d_exponent(target: Coord) -> int:
    for exponent in range(RAW_ORDER):
        if scale_coord(D_SHIFT, exponent) == target:
            return exponent
    raise AssertionError(f"target {target} is not in the D-generated source")


def poly_multiply(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for left_exp, left_coeff in left.items():
        for right_exp, right_coeff in right.items():
            exp = (left_exp + right_exp) % RAW_ORDER
            out[exp] = out.get(exp, 0) + left_coeff * right_coeff
            if out[exp] == 0:
                del out[exp]
    return dict(sorted(out.items()))


def primitive_d_poly(base_exp: int, kernel_exp: int, bridge_exp: int) -> Poly:
    factors = (
        {base_exp: 1},
        {(kernel_exp * index) % RAW_ORDER: 1 for index in range(25)},
        {0: 1, 1: 1, 2: 1},
        {0: 1, bridge_exp: -1},
    )
    product: Poly = {0: 1}
    for factor in factors:
        product = poly_multiply(product, factor)
    return product


def poly_to_source_mask(poly: Poly) -> dict[Coord, int]:
    out: dict[Coord, int] = {}
    for exponent, coefficient in poly.items():
        coord = scale_coord(D_SHIFT, exponent)
        out[coord] = out.get(coord, 0) + coefficient
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def poly_to_raw(poly: Poly) -> list[int]:
    from p25_laneB_square_axis_bridge_candidate_harness_gate import crt_source_to_raw

    raw = [0] * RAW_ORDER
    for coord, coefficient in poly_to_source_mask(poly).items():
        raw[crt_source_to_raw(*coord)] = coefficient
    return raw


def profile_primitive_d_coordinate() -> PrimitiveDCoordinateProfile:
    case = square_axis_case()
    right_generator, c_generator = source_generators(case)
    d_profile = factor_profile("D_segment", D_SHIFT)
    base_exp = solve_d_exponent(BASE_POINT)
    kernel_exp = solve_d_exponent(KERNEL_SHIFT)
    bridge_exp = solve_d_exponent(BRIDGE_SHIFT)
    y_exp = solve_d_exponent((9, 9))
    poly = primitive_d_poly(base_exp, kernel_exp, bridge_exp)
    candidate = profile_candidate("primitive_D_coordinate_bridge", poly_to_raw(poly), target_raw_bridge())
    return PrimitiveDCoordinateProfile(
        d_shift=D_SHIFT,
        d_right_multiplier=pow(right_generator, D_SHIFT[0], case.right_sources[0].modulus),
        d_c_multiplier=pow(c_generator, D_SHIFT[1], case.c_source.modulus),
        d_order=coordinate_order(D_SHIFT),
        d_combined_kummer_order=d_profile.combined_order,
        base_exponent=base_exp,
        kernel_exponent=kernel_exp,
        bridge_exponent=bridge_exp,
        y_exponent=y_exp,
        kernel_order=RAW_ORDER // gcd(kernel_exp, RAW_ORDER),
        bridge_order=RAW_ORDER // gcd(bridge_exp, RAW_ORDER),
        y_order=RAW_ORDER // gcd(y_exp, RAW_ORDER),
        d_cubed_relation=(3 - kernel_exp - y_exp) % RAW_ORDER == 0,
        kernel_trace_exponents_first=tuple((kernel_exp * index) % RAW_ORDER for index in range(6)),
        kernel_trace_exponents_last=tuple((kernel_exp * index) % RAW_ORDER for index in range(22, 25)),
        product_support=len(poly),
        product_degree=sum(poly.values()),
        coefficient_counts=tuple(sorted(Counter(poly.values()).items())),
        source_mask_exact=poly_to_source_mask(poly) == raw_source_mask(),
        harness_ok=candidate.ok,
        one_generator_payload_below_sqrt=len(poly) < 3_162_277_660_168,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge primitive D-coordinate gate")
    profile = profile_primitive_d_coordinate()
    row_ok = (
        profile.d_shift == (22, 3)
        and profile.d_right_multiplier == 55
        and profile.d_c_multiplier == 85
        and profile.d_order == RAW_ORDER == 12675
        and profile.d_combined_kummer_order == 12675
        and profile.base_exponent == 11275
        and profile.kernel_exponent == 4056
        and profile.bridge_exponent == 6854
        and profile.y_exponent == 8622
        and profile.kernel_order == 25
        and profile.bridge_order == 12675
        and profile.y_order == 4225
        and profile.d_cubed_relation
        and profile.kernel_trace_exponents_first == (0, 4056, 8112, 12168, 3549, 7605)
        and profile.kernel_trace_exponents_last == (507, 4563, 8619)
        and profile.product_support == 150
        and profile.product_degree == 0
        and profile.coefficient_counts == ((-1, 75), (1, 75))
        and profile.source_mask_exact
        and profile.harness_ok
        and profile.one_generator_payload_below_sqrt
    )

    print(f"primitive_d_coordinate_profile={profile}")
    print("one_generator_word")
    print("  z^11275 * (sum_{j=0}^{24} z^(4056*j)) * (1 + z + z^2) * (1 - z^6854)")
    print("  D=(22,3) is primitive of order 12675 on C75 x C169")
    print("  K=(57,0)=D^4056 is the order-25 trace step")
    print("  T=(38,113)=D^6854 is still primitive")
    print("  Y_raw=(9,9)=D^8622 and D^3=K*Y_raw")
    print("interpretation")
    print("  bridge_has_a_single_primitive_source_coordinate_normal_form=1")
    print("  kernel_trace_D_segment_and_T_edge_are_not_unrelated_axes=1")
    print("  one_generator_form_is_positive_but_keeps_full_raw_kummer_order=1")
    print("  producer_can_target_this_cyclic_word_but_not_a_low_order_quotient=1")
    print(f"square_axis_bridge_primitive_d_coordinate_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_primitive_d_coordinate_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

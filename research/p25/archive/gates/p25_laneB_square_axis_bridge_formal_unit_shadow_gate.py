#!/usr/bin/env python3
"""Formal-unit shadow for the p25 square-axis bridge.

The bridge candidate harness gives a finite acceptance contract.  This gate
builds the exact accepted bridge from a producer-shaped formal group-ring word
on the raw source axes C_75 x C_169:

    x^base * (1 + K + ... + K^24) * (1 + D + D^2) * (1 - T).

This is the local shadow a modular-unit or CM-Artin producer would need to
realize arithmetically.  The shadow itself is tiny and passes the harness; the
remaining problem is the arithmetic lift/Kummer cost, not the finite payload.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    crt_source_to_raw,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_factor_kummer_gate import factor_profile
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


SQRT_FLOOR = 3_162_277_660_168
Y_RAW_SHIFT = (Y_STEP % RIGHT_ORDER, Y_STEP % C_ORDER)
D_CUBED_SHIFT = ((3 * D_SHIFT[0]) % RIGHT_ORDER, (3 * D_SHIFT[1]) % C_ORDER)

Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class FormalShadowProfile:
    factor_supports: tuple[tuple[str, int, int], ...]
    product_support: int
    product_degree: int
    coefficient_counts: tuple[tuple[int, int], ...]
    collision_free: bool
    source_mask_exact: bool
    harness_ok: bool
    payload_below_sqrt: bool
    kernel_boundary_zero: bool
    d_segment_boundary: tuple[tuple[Coord, int], ...]
    d_cubed_minus_y: Coord
    d_cubed_equals_y_mod_kernel: bool
    factor_min_degrees: tuple[tuple[str, int, int, int], ...]


def add_coord(left: Coord, right: Coord) -> Coord:
    return (
        (left[0] + right[0]) % RIGHT_ORDER,
        (left[1] + right[1]) % C_ORDER,
    )


def scale_coord(step: Coord, scale: int) -> Coord:
    return ((step[0] * scale) % RIGHT_ORDER, (step[1] * scale) % C_ORDER)


def add_ring(left: Ring, right: Ring) -> Ring:
    out = dict(left)
    for coord, value in right.items():
        out[coord] = out.get(coord, 0) + value
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def multiply_ring(left: Ring, right: Ring) -> Ring:
    out: Ring = {}
    for l_coord, l_value in left.items():
        for r_coord, r_value in right.items():
            coord = add_coord(l_coord, r_coord)
            out[coord] = out.get(coord, 0) + l_value * r_value
            if out[coord] == 0:
                del out[coord]
    return dict(sorted(out.items()))


def monomial(coord: Coord, coefficient: int = 1) -> Ring:
    return {coord: coefficient}


def geometric_factor(step: Coord, length: int) -> Ring:
    return {scale_coord(step, index): 1 for index in range(length)}


def edge_factor(step: Coord) -> Ring:
    return {(0, 0): 1, step: -1}


def translate_ring(ring: Ring, step: Coord, coefficient: int = 1) -> Ring:
    return {add_coord(coord, step): coefficient * value for coord, value in ring.items()}


def ring_degree(ring: Ring) -> int:
    return sum(ring.values())


def boundary(ring: Ring, step: Coord) -> Ring:
    return add_ring(ring, translate_ring(ring, step, coefficient=-1))


def source_mask_to_raw(ring: Ring) -> list[int]:
    raw = [0] * RAW_ORDER
    for (right_log, c_log), value in ring.items():
        raw[crt_source_to_raw(right_log, c_log)] = value
    return raw


def formal_factors() -> tuple[tuple[str, Ring], ...]:
    return (
        ("base", monomial(BASE_POINT)),
        ("kernel_trace", geometric_factor(KERNEL_SHIFT, 25)),
        ("D_segment", geometric_factor(D_SHIFT, 3)),
        ("bridge_edge", edge_factor(BRIDGE_SHIFT)),
    )


def multiply_factors(factors: tuple[tuple[str, Ring], ...]) -> Ring:
    product = monomial((0, 0))
    for _name, factor in factors:
        product = multiply_ring(product, factor)
    return product


def factor_support_summary(factors: tuple[tuple[str, Ring], ...]) -> tuple[tuple[str, int, int], ...]:
    return tuple((name, len(factor), ring_degree(factor)) for name, factor in factors)


def profile_formal_shadow() -> tuple[FormalShadowProfile, tuple[CandidateProfile, ...]]:
    factors = formal_factors()
    product = multiply_factors(factors)
    target = target_raw_bridge()
    full_profile = profile_candidate("formal_unit_shadow", source_mask_to_raw(product), target)

    shortcut_profiles = (
        profile_candidate(
            "formal_no_kernel_trace",
            source_mask_to_raw(multiply_factors((factors[0], factors[2], factors[3]))),
            target,
        ),
        profile_candidate(
            "formal_no_D_segment",
            source_mask_to_raw(multiply_factors((factors[0], factors[1], factors[3]))),
            target,
        ),
        profile_candidate(
            "formal_no_bridge_edge",
            source_mask_to_raw(multiply_factors((factors[0], factors[1], factors[2]))),
            target,
        ),
    )

    kernel = factors[1][1]
    d_segment = factors[2][1]
    kernel_boundary_zero = boundary(kernel, KERNEL_SHIFT) == {}
    d_segment_boundary = tuple(sorted(boundary(d_segment, D_SHIFT).items()))
    d_cubed_minus_y = (
        (D_CUBED_SHIFT[0] - Y_RAW_SHIFT[0]) % RIGHT_ORDER,
        (D_CUBED_SHIFT[1] - Y_RAW_SHIFT[1]) % C_ORDER,
    )
    factor_costs = tuple(
        (profile.name, profile.right_c75_min_degree, profile.c_c169_min_degree, profile.combined_order)
        for profile in (
            factor_profile("kernel_trace", KERNEL_SHIFT),
            factor_profile("D_segment", D_SHIFT),
            factor_profile("bridge_edge", BRIDGE_SHIFT),
        )
    )
    expected_raw_size = 1
    for _name, factor in factors:
        expected_raw_size *= len(factor)

    profile = FormalShadowProfile(
        factor_supports=factor_support_summary(factors),
        product_support=len(product),
        product_degree=ring_degree(product),
        coefficient_counts=tuple(sorted(Counter(product.values()).items())),
        collision_free=len(product) == expected_raw_size,
        source_mask_exact=product == raw_source_mask(),
        harness_ok=full_profile.ok,
        payload_below_sqrt=len(product) < SQRT_FLOOR,
        kernel_boundary_zero=kernel_boundary_zero,
        d_segment_boundary=d_segment_boundary,
        d_cubed_minus_y=d_cubed_minus_y,
        d_cubed_equals_y_mod_kernel=d_cubed_minus_y == KERNEL_SHIFT,
        factor_min_degrees=factor_costs,
    )
    return profile, (full_profile,) + shortcut_profiles


def main() -> int:
    print("p25 Lane B square-axis bridge formal-unit shadow gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} base={BASE_POINT} "
        f"K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile, candidate_profiles = profile_formal_shadow()
    by_name = {candidate.name: candidate for candidate in candidate_profiles}

    expected_d_boundary = (((0, 0), 1), (scale_coord(D_SHIFT, 3), -1))
    row_ok = (
        profile.factor_supports
        == (("base", 1, 1), ("kernel_trace", 25, 25), ("D_segment", 3, 3), ("bridge_edge", 2, 0))
        and profile.product_support == 150
        and profile.product_degree == 0
        and profile.coefficient_counts == ((-1, 75), (1, 75))
        and profile.collision_free
        and profile.source_mask_exact
        and profile.harness_ok
        and profile.payload_below_sqrt
        and profile.kernel_boundary_zero
        and profile.d_segment_boundary == expected_d_boundary
        and profile.d_cubed_minus_y == KERNEL_SHIFT
        and profile.d_cubed_equals_y_mod_kernel
        and profile.factor_min_degrees
        == (
            ("kernel_trace", 25, 1, 25),
            ("D_segment", 75, 169, 12675),
            ("bridge_edge", 75, 169, 12675),
        )
        and by_name["formal_unit_shadow"].ok
        and by_name["formal_no_kernel_trace"].raw_support == 6
        and by_name["formal_no_kernel_trace"].kernel_modes == tuple(range(25))
        and by_name["formal_no_kernel_trace"].raw_relation_mismatches > 0
        and not by_name["formal_no_kernel_trace"].ok
        and by_name["formal_no_D_segment"].raw_support == 50
        and by_name["formal_no_D_segment"].kernel_modes == (0,)
        and not by_name["formal_no_D_segment"].ok
        and by_name["formal_no_bridge_edge"].raw_support == 75
        and by_name["formal_no_bridge_edge"].kernel_modes == (0,)
        and not by_name["formal_no_bridge_edge"].ok
    )

    print(f"formal_shadow_profile={profile}")
    print("candidate_profiles")
    for candidate in candidate_profiles:
        print(f"  {candidate}")
    print("formal_group_ring_word")
    print("  x^base * (1 + K + ... + K^24) * (1 + D + D^2) * (1 - T)")
    print("  K has zero first boundary because it is the order-25 trace factor")
    print("  (1 - D) * (1 + D + D^2) = 1 - D^3, and D^3 = Y only modulo K")
    print("  the full product has 150 signed raw source cells, far below sqrt(p)")
    print("shortcut_falsifiers")
    print("  omitting K gives a tiny sparse section but all 25 kernel modes and raw relation failures")
    print("  omitting D gives a kernel-trivial two-edge object, not the length-three segment")
    print("  omitting T gives the positive segment only, not the anti-invariant bridge")
    print("interpretation")
    print("  formal_unit_shadow_passes_the_bridge_candidate_harness=1")
    print("  the_finite_payload_is_small_and_exact_but_not_yet_an_arithmetic_certificate=1")
    print("  any_modular_unit_realization_must_supply_K_D_segment_and_T_edge_together=1")
    print("  remaining_obstruction_is_arithmetic_realization_with_controlled_Kummer_cost=1")
    print(f"square_axis_bridge_formal_unit_shadow_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_formal_unit_shadow_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

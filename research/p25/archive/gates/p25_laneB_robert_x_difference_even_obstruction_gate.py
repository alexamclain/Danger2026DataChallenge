#!/usr/bin/env python3
"""Robert x-difference evenness obstruction for the p25 square-axis bridge.

The next Robert/Coates-Wiles microscope wants a finite table resembling

    x(Q_c) - x(P_r)

on the local source coordinates C_75 x C_169.  A literal x-only table has an
immediate symmetry: x(-P)=x(P) and x(-Q)=x(Q), so any scalar function of this
table is even under simultaneous source inversion

    (r,c) -> (-r,-c).

The target bridge is the opposite: it is anti-invariant under that involution.
This gate records the obstruction and gives a concrete cyclotomic x-coordinate
degeneration as a control.  It does not kill Robert elliptic units; it kills
the unoriented x-only version.  A viable Robert/Siegel producer must add an
oriented quotient, y/differential data, a unit phase, or another mechanism that
breaks x-evenness into the bridge's signed anti-invariant line.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_robert_source_matrix_harness_gate import (
    raw_from_source_matrix,
    source_matrix_from_raw,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    MODULUS,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


@dataclass(frozen=True)
class InvolutionProfile:
    support: int
    even: bool
    anti: bool
    anti_projection_support: int
    even_projection_support: int


@dataclass(frozen=True)
class XDifferenceProfile:
    zero_count: int
    zero_positions: tuple[tuple[int, int], ...]
    quadratic_distribution: tuple[tuple[int, int], ...]
    x_table_even: bool
    zero_mask_even: bool
    quadratic_mask_even: bool


def source_index(right_log: int, c_log: int) -> int:
    return right_log * C_ORDER + c_log


def involution_coord(right_log: int, c_log: int) -> tuple[int, int]:
    return (-right_log) % RIGHT_ORDER, (-c_log) % C_ORDER


def involution_index(index: int) -> int:
    right_log, c_log = divmod(index, C_ORDER)
    inv_right, inv_c = involution_coord(right_log, c_log)
    return source_index(inv_right, inv_c)


def involution_profile(matrix: list[int]) -> InvolutionProfile:
    even = True
    anti = True
    anti_projection_support = 0
    even_projection_support = 0
    support = sum(int(value != 0) for value in matrix)
    for index, value in enumerate(matrix):
        inv_value = matrix[involution_index(index)]
        even = even and value == inv_value
        anti = anti and value == -inv_value
        anti_projection_support += int(value - inv_value != 0)
        even_projection_support += int(value + inv_value != 0)
    return InvolutionProfile(
        support=support,
        even=even,
        anti=anti,
        anti_projection_support=anti_projection_support,
        even_projection_support=even_projection_support,
    )


def signed_mod(value: int) -> int:
    value %= MODULUS
    if value > MODULUS // 2:
        return value - MODULUS
    return value


def cyclotomic_x_values(order: int) -> list[int]:
    root = primitive_root(MODULUS)
    zeta = pow(root, (MODULUS - 1) // order, MODULUS)
    return [
        (pow(zeta, exponent, MODULUS) + pow(zeta, (-exponent) % order, MODULUS))
        % MODULUS
        for exponent in range(order)
    ]


def x_difference_matrix() -> list[int]:
    right_x = cyclotomic_x_values(RIGHT_ORDER)
    c_x = cyclotomic_x_values(C_ORDER)
    return [
        signed_mod(c_x[c_log] - right_x[right_log])
        for right_log in range(RIGHT_ORDER)
        for c_log in range(C_ORDER)
    ]


def quadratic_character(value: int) -> int:
    value %= MODULUS
    if value == 0:
        return 0
    return 1 if pow(value, (MODULUS - 1) // 2, MODULUS) == 1 else -1


def x_difference_profile() -> tuple[XDifferenceProfile, list[int], list[int], list[int]]:
    xdiff = x_difference_matrix()
    zero_positions: list[tuple[int, int]] = []
    zero_mask = [0] * RAW_ORDER
    quadratic_mask = [0] * RAW_ORDER
    distribution = {-1: 0, 0: 0, 1: 0}
    for right_log in range(RIGHT_ORDER):
        for c_log in range(C_ORDER):
            index = source_index(right_log, c_log)
            value = xdiff[index]
            if value == 0:
                zero_positions.append((right_log, c_log))
                zero_mask[index] = 1
            q_value = quadratic_character(value)
            quadratic_mask[index] = q_value
            distribution[q_value] += 1
    profile = XDifferenceProfile(
        zero_count=len(zero_positions),
        zero_positions=tuple(zero_positions),
        quadratic_distribution=tuple(sorted(distribution.items())),
        x_table_even=involution_profile(xdiff).even,
        zero_mask_even=involution_profile(zero_mask).even,
        quadratic_mask_even=involution_profile(quadratic_mask).even,
    )
    return profile, xdiff, zero_mask, quadratic_mask


def main() -> int:
    print("p25 Lane B Robert x-difference evenness obstruction gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} modulus={MODULUS} "
        "involution=(right,c)->(-right,-c)"
    )
    target = target_raw_bridge()
    target_matrix = source_matrix_from_raw(target)
    unsigned_matrix = [abs(value) for value in target_matrix]
    x_profile, _xdiff, zero_mask, quadratic_mask = x_difference_profile()

    target_inv = involution_profile(target_matrix)
    unsigned_inv = involution_profile(unsigned_matrix)
    zero_inv = involution_profile(zero_mask)
    quadratic_inv = involution_profile(quadratic_mask)

    target_candidate = profile_candidate(
        "target_bridge_source_matrix",
        raw_from_source_matrix(target_matrix),
        target,
    )
    unsigned_candidate = profile_candidate(
        "unsigned_inversion_even_hull",
        raw_from_source_matrix(unsigned_matrix),
        target,
    )
    zero_candidate = profile_candidate(
        "cyclotomic_x_difference_zero_mask",
        raw_from_source_matrix(zero_mask),
        target,
    )
    quadratic_candidate = profile_candidate(
        "cyclotomic_x_difference_quadratic_character",
        raw_from_source_matrix(quadratic_mask),
        target,
    )

    row_ok = (
        target_candidate.ok
        and target_inv.anti
        and not target_inv.even
        and target_inv.anti_projection_support == 150
        and unsigned_inv.even
        and not unsigned_inv.anti
        and not unsigned_candidate.ok
        and x_profile.zero_count == 1
        and x_profile.zero_positions == ((0, 0),)
        and x_profile.quadratic_distribution == ((-1, 6274), (0, 1), (1, 6400))
        and x_profile.x_table_even
        and x_profile.zero_mask_even
        and x_profile.quadratic_mask_even
        and zero_inv.even
        and quadratic_inv.even
        and not zero_candidate.ok
        and not quadratic_candidate.ok
    )

    print(f"target_involution_profile={target_inv}")
    print(f"unsigned_hull_involution_profile={unsigned_inv}")
    print(f"x_difference_profile={x_profile}")
    print(f"zero_mask_involution_profile={zero_inv}")
    print(f"quadratic_mask_involution_profile={quadratic_inv}")
    print("candidate_profiles")
    print(f"  target={target_candidate}")
    print(f"  unsigned_hull={unsigned_candidate}")
    print(f"  x_zero_mask={zero_candidate}")
    print(f"  x_quadratic_character={quadratic_candidate}")
    print("evenness_law")
    print("  literal x-only Robert tables are invariant under (right,c)->(-right,-c)")
    print("  the p25 bridge is anti-invariant under the same involution")
    print("  any scalar function of an even x-difference table has zero anti-invariant projection")
    print(f"robert_x_difference_even_obstruction_rows={int(row_ok)}/1")
    print("interpretation")
    print("  literal_x_difference_or_x_value_only_table_cannot_be_the_bridge=1")
    print("  robert_lane_requires_oriented_quotient_y_differential_or_unit_phase=1")
    print("  cyclotomic_x_degeneration_controls_are_even_and_fail_the_bridge_harness=1")
    print("conclusion=reported_p25_laneB_robert_x_difference_even_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

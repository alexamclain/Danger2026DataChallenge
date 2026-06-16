#!/usr/bin/env python3
"""Source-character factorization for the p25 square-axis bridge.

The source-line lift gate writes the bridge in C_3 x C_169 as

    base * (1 + D + D^2) * (1 - T),

with D=(1,3) and T=(2,113).  This gate records the dual character-side
consequence and the important limitation: the C_13 shadow has the same zero
pattern as the full C_169 lift, so Fourier zeros alone cannot select the lift.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_source_affine_rigidity_gate import Mask, source_bridge_mask
from p25_laneB_square_axis_local_graph_residue_gate import SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


MODULUS = 2029
D_SHIFT = (1, 3)
BRIDGE_SHIFT = (2, 113)
BASE_POINT = (1, 25)


@dataclass(frozen=True)
class ZeroProfile:
    c_axis: int
    support_size: int
    character_count: int
    zero_count: int
    nonzero_count: int
    d_segment_zeros: tuple[tuple[int, int], ...]
    bridge_edge_zeros: tuple[tuple[int, int], ...]
    other_zeros: tuple[tuple[int, int], ...]
    nonlifted_nonzero_count: int | None
    factorization_ok: bool


def project_mask(mask: Mask, c_axis: int) -> Mask:
    projected: Mask = {}
    for (right, c_log), value in mask.items():
        coord = (right, c_log % c_axis)
        projected[coord] = projected.get(coord, 0) + value
    return {coord: value for coord, value in sorted(projected.items()) if value}


def character_value(zeta_3: int, zeta_c: int, a_char: int, b_char: int, coord: tuple[int, int]) -> int:
    right, c_log = coord
    return (
        pow(zeta_3, a_char * right, MODULUS)
        * pow(zeta_c, b_char * c_log, MODULUS)
    ) % MODULUS


def zero_profile(c_axis: int) -> ZeroProfile:
    root = primitive_root(MODULUS)
    zeta_3 = pow(root, (MODULUS - 1) // RIGHT_DEGREE, MODULUS)
    zeta_c = pow(root, (MODULUS - 1) // c_axis, MODULUS)
    mask = project_mask(source_bridge_mask(), c_axis)
    base = (BASE_POINT[0], BASE_POINT[1] % c_axis)
    d_shift = (D_SHIFT[0], D_SHIFT[1] % c_axis)
    bridge_shift = (BRIDGE_SHIFT[0], BRIDGE_SHIFT[1] % c_axis)

    d_zeros: list[tuple[int, int]] = []
    edge_zeros: list[tuple[int, int]] = []
    other_zeros: list[tuple[int, int]] = []
    nonzero_count = 0
    nonlifted_nonzero_count = 0
    factorization_ok = True

    for a_char in range(RIGHT_DEGREE):
        for b_char in range(c_axis):
            total = sum(
                coefficient * character_value(zeta_3, zeta_c, a_char, b_char, coord)
                for coord, coefficient in mask.items()
            ) % MODULUS
            chi_base = character_value(zeta_3, zeta_c, a_char, b_char, base)
            chi_d = character_value(zeta_3, zeta_c, a_char, b_char, d_shift)
            chi_t = character_value(zeta_3, zeta_c, a_char, b_char, bridge_shift)
            factored = chi_base * (1 + chi_d + chi_d * chi_d) * (1 - chi_t)
            if total != factored % MODULUS:
                factorization_ok = False

            is_d_zero = (1 + chi_d + chi_d * chi_d) % MODULUS == 0
            is_edge_zero = (1 - chi_t) % MODULUS == 0
            if total == 0:
                if is_d_zero:
                    d_zeros.append((a_char, b_char))
                if is_edge_zero:
                    edge_zeros.append((a_char, b_char))
                if not is_d_zero and not is_edge_zero:
                    other_zeros.append((a_char, b_char))
            else:
                nonzero_count += 1
                if c_axis == SQUARE_C and b_char % 13:
                    nonlifted_nonzero_count += 1

    zero_count = RIGHT_DEGREE * c_axis - nonzero_count
    return ZeroProfile(
        c_axis=c_axis,
        support_size=len(mask),
        character_count=RIGHT_DEGREE * c_axis,
        zero_count=zero_count,
        nonzero_count=nonzero_count,
        d_segment_zeros=tuple(d_zeros),
        bridge_edge_zeros=tuple(edge_zeros),
        other_zeros=tuple(other_zeros),
        nonlifted_nonzero_count=nonlifted_nonzero_count if c_axis == SQUARE_C else None,
        factorization_ok=factorization_ok,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge source-character gate")
    print(
        f"modulus={MODULUS} source_group=C_{RIGHT_DEGREE}xC_{SQUARE_C} "
        f"D={D_SHIFT} T={BRIDGE_SHIFT} base={BASE_POINT}"
    )
    profiles = (zero_profile(13), zero_profile(SQUARE_C))
    expected_c13 = ZeroProfile(
        c_axis=13,
        support_size=6,
        character_count=39,
        zero_count=3,
        nonzero_count=36,
        d_segment_zeros=((1, 0), (2, 0)),
        bridge_edge_zeros=((0, 0),),
        other_zeros=(),
        nonlifted_nonzero_count=None,
        factorization_ok=True,
    )
    expected_c169 = ZeroProfile(
        c_axis=SQUARE_C,
        support_size=6,
        character_count=507,
        zero_count=3,
        nonzero_count=504,
        d_segment_zeros=((1, 0), (2, 0)),
        bridge_edge_zeros=((0, 0),),
        other_zeros=(),
        nonlifted_nonzero_count=468,
        factorization_ok=True,
    )
    row_ok = profiles == (expected_c13, expected_c169)

    print("zero_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("character_factorization")
    print("  bridge_hat(a,b) = chi(base) * (1 + chi(D) + chi(D)^2) * (1 - chi(T))")
    print("  D-segment zeros: (a,b)=(1,0),(2,0)")
    print("  bridge-edge zero: (a,b)=(0,0)")
    print("  all other source characters are nonzero")
    print("interpretation")
    print("  source_character_zeros_are_exactly_D_segment_plus_bridge_edge_zeros=1")
    print("  C13_shadow_has_the_same_zero_pattern_as_the_C169_lift=1")
    print("  all_468_nonlifted_C169_characters_are_nonzero=1")
    print("  spectral_zero_tests_alone_cannot_select_the_unique_C169_lift=1")
    print("  producer_must_realize_the_source_line_lift_geometry_not_only_character_zeros=1")
    print(f"square_axis_bridge_source_character_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_source_character_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

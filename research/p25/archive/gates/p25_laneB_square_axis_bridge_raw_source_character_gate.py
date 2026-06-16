#!/usr/bin/env python3
"""Raw source-character factorization for the p25 square-axis bridge.

The source-character gate factors the quotient source mask on C_3 x C_169.
This gate records the raw source lift on C_75 x C_169.  The raw bridge is the
same D-segment and bridge-edge geometry multiplied by the 25-point right-kernel
trace factor.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_factorization_gate import BRIDGE_STEP, bridge_coefficients
from p25_laneB_square_axis_bridge_raw_source_gate import square_axis_case
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP


RIGHT_ORDER = 75
C_ORDER = 169
MODULUS = 126751
BASE_POINT = (25, 25)
KERNEL_SHIFT = (507 % RIGHT_ORDER, 0)
D_SHIFT = (S_STEP % RIGHT_ORDER, S_STEP % C_ORDER)
BRIDGE_SHIFT = (BRIDGE_STEP % RIGHT_ORDER, BRIDGE_STEP % C_ORDER)


Coord = tuple[int, int]


@dataclass(frozen=True)
class RawZeroProfile:
    support_size: int
    character_count: int
    zero_count: int
    nonzero_count: int
    kernel_trace_zeros: int
    quotient_character_count: int
    d_segment_zeros: tuple[Coord, ...]
    bridge_edge_zeros: tuple[Coord, ...]
    other_zeros: tuple[Coord, ...]
    nonzero_a_values: tuple[int, ...]
    factorization_ok: bool


def raw_source_mask() -> dict[Coord, int]:
    case = square_axis_case()
    out: dict[Coord, int] = {}
    for q_value, coefficient in bridge_coefficients().items():
        for layer in range(case.b_trace):
            e_value = q_value + 507 * layer
            coord = (e_value % RIGHT_ORDER, e_value % C_ORDER)
            out[coord] = out.get(coord, 0) + coefficient
    return {coord: value for coord, value in sorted(out.items()) if value}


def character_value(zeta_right: int, zeta_c: int, a_char: int, b_char: int, coord: Coord) -> int:
    right_log, c_log = coord
    return (
        pow(zeta_right, a_char * right_log, MODULUS)
        * pow(zeta_c, b_char * c_log, MODULUS)
    ) % MODULUS


def raw_zero_profile() -> RawZeroProfile:
    root = primitive_root(MODULUS)
    zeta_right = pow(root, (MODULUS - 1) // RIGHT_ORDER, MODULUS)
    zeta_c = pow(root, (MODULUS - 1) // C_ORDER, MODULUS)
    mask = raw_source_mask()

    kernel_trace_zeros = 0
    d_zeros: list[Coord] = []
    edge_zeros: list[Coord] = []
    other_zeros: list[Coord] = []
    nonzero_count = 0
    nonzero_a_values: set[int] = set()
    factorization_ok = True

    for a_char in range(RIGHT_ORDER):
        for b_char in range(C_ORDER):
            total = sum(
                coefficient * character_value(zeta_right, zeta_c, a_char, b_char, coord)
                for coord, coefficient in mask.items()
            ) % MODULUS
            chi_base = character_value(zeta_right, zeta_c, a_char, b_char, BASE_POINT)
            chi_kernel = character_value(zeta_right, zeta_c, a_char, b_char, KERNEL_SHIFT)
            chi_d = character_value(zeta_right, zeta_c, a_char, b_char, D_SHIFT)
            chi_t = character_value(zeta_right, zeta_c, a_char, b_char, BRIDGE_SHIFT)
            kernel_factor = sum(pow(chi_kernel, layer, MODULUS) for layer in range(25)) % MODULUS
            d_factor = (1 + chi_d + chi_d * chi_d) % MODULUS
            edge_factor = (1 - chi_t) % MODULUS
            factored = chi_base * kernel_factor * d_factor * edge_factor
            if total != factored % MODULUS:
                factorization_ok = False

            is_kernel_zero = kernel_factor == 0
            is_d_zero = d_factor == 0
            is_edge_zero = edge_factor == 0
            if total == 0:
                if is_kernel_zero:
                    kernel_trace_zeros += 1
                elif is_d_zero:
                    d_zeros.append((a_char, b_char))
                elif is_edge_zero:
                    edge_zeros.append((a_char, b_char))
                else:
                    other_zeros.append((a_char, b_char))
            else:
                nonzero_count += 1
                nonzero_a_values.add(a_char)

    return RawZeroProfile(
        support_size=len(mask),
        character_count=RIGHT_ORDER * C_ORDER,
        zero_count=RIGHT_ORDER * C_ORDER - nonzero_count,
        nonzero_count=nonzero_count,
        kernel_trace_zeros=kernel_trace_zeros,
        quotient_character_count=3 * C_ORDER,
        d_segment_zeros=tuple(d_zeros),
        bridge_edge_zeros=tuple(edge_zeros),
        other_zeros=tuple(other_zeros),
        nonzero_a_values=tuple(sorted(nonzero_a_values)),
        factorization_ok=factorization_ok,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge raw source-character gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} modulus={MODULUS} "
        f"base={BASE_POINT} kernel={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    case = square_axis_case()
    profile = raw_zero_profile()
    expected = RawZeroProfile(
        support_size=150,
        character_count=12675,
        zero_count=12171,
        nonzero_count=504,
        kernel_trace_zeros=12168,
        quotient_character_count=507,
        d_segment_zeros=((25, 0), (50, 0)),
        bridge_edge_zeros=((0, 0),),
        other_zeros=(),
        nonzero_a_values=(0, 25, 50),
        factorization_ok=True,
    )
    row_ok = (
        case.raw_order == 12675
        and case.b_trace == 25
        and KERNEL_SHIFT == (57, 0)
        and D_SHIFT == (22, 3)
        and BRIDGE_SHIFT == (38, 113)
        and profile == expected
    )

    print(f"raw_zero_profile={profile}")
    print("raw_character_factorization")
    print("  bridge_hat(a,b) = chi(base) * K(a) * (1 + chi(D) + chi(D)^2) * (1 - chi(T))")
    print("  K(a) = sum_{j=0}^{24} chi(57,0)^j")
    print("  kernel-trace zeros: all a not in {0,25,50}")
    print("  quotient surviving a-values: 0,25,50")
    print("  D-segment zeros: (25,0),(50,0)")
    print("  bridge-edge zero: (0,0)")
    print("interpretation")
    print("  raw_bridge_is_kernel_trace_times_D_segment_times_bridge_edge=1")
    print("  raw_kernel_trace_accounts_for_12168_character_zeros=1")
    print("  surviving_raw_characters_are_exactly_the_C3xC169_quotient_characters=1")
    print("  producer_must_realize_the_25_point_right_kernel_trace_not_a_hidden_kernel_phase=1")
    print(f"square_axis_bridge_raw_source_character_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_raw_source_character_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Canonical half-arc gate for p25 Lane B.

The diamond-conjugacy gate compresses the producer target to one C-axis vector
V plus the prescribed negative-inversion conjugate.  This gate specializes to
the canonical carry theta_{3,1} and records the exact finite divisor shape of
that one vector.

For c = 4m + 1, the raw theta_{3,1} carry on C_3 x C_c has four C-axis zones:

    0..m       : no right row carries;
    m+1..2m   : exactly one right row carries, cycling through C_3;
    2m+1..3m  : exactly two right rows carry, equivalently minus the missing row;
    3m+1..4m  : all right rows carry.

After subtracting scalar/pure-C parts and projecting to a nontrivial right
character, only the middle half-arc remains.  Thus the canonical p25 producer
target is a very concrete half-arc vector, not an opaque full C-axis vector.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_literal_jacobi_packet_model import carry_packet, crt
from p25_laneB_mixed_character_module_gate import decompose_packet
from p25_laneB_right_eigenbasis_gate import right_eigenvectors, right_root
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class HalfArcCase:
    name: str
    c_axis: int


CASES = (
    HalfArcCase("tiny_C3xC13", 13),
    HalfArcCase("prime_axis_C3xC53", 53),
    HalfArcCase("square_axis_C3xC169", 169),
)


def carry_bits_from_crt(c_axis: int, c_index: int) -> tuple[int, int, int]:
    order = RIGHT_DEGREE * c_axis
    bits: list[int] = []
    for right in range(RIGHT_DEGREE):
        point = crt(right, c_index, c_axis)
        u_part = (RIGHT_DEGREE * point) % order
        bits.append(int(u_part + point >= order))
    return tuple(bits)


def one_hot(index: int) -> tuple[int, int, int]:
    return tuple(int(row == index % RIGHT_DEGREE) for row in range(RIGHT_DEGREE))


def template_bits(c_axis: int, c_index: int) -> tuple[int, int, int]:
    if c_axis % 4 != 1:
        raise AssertionError("half-arc template expects c = 1 mod 4")
    m_value = (c_axis - 1) // 4
    if c_index <= m_value:
        return (0, 0, 0)
    if c_index <= 2 * m_value:
        return one_hot(c_index - (m_value + 1))
    if c_index <= 3 * m_value:
        missing = one_hot(c_index)
        return tuple(1 - bit for bit in missing)
    return (1, 1, 1)


def expected_eigenvalue(
    c_axis: int, modulus: int, bits: tuple[int, int, int], character: int
) -> int:
    zeta = right_root(modulus)
    total = sum(bits[row] * pow(zeta, character * row, modulus) for row in range(3))
    return c_axis * total % modulus


def support_interval(vector: list[int], modulus: int) -> tuple[int | None, int | None, int]:
    support = [index for index, value in enumerate(vector) if value % modulus]
    if not support:
        return None, None, 0
    return support[0], support[-1], len(support)


def bit_count_profile(bits_by_index: list[tuple[int, int, int]]) -> dict[int, int]:
    profile: dict[int, int] = {}
    for bits in bits_by_index:
        count = sum(bits)
        profile[count] = profile.get(count, 0) + 1
    return dict(sorted(profile.items()))


def audit_case(case: HalfArcCase) -> tuple[list[str], bool]:
    c_axis = case.c_axis
    modulus = split_prime_for(RIGHT_DEGREE * c_axis)
    m_value = (c_axis - 1) // 4
    packet = carry_packet(c_axis, RIGHT_DEGREE, 1, modulus)
    _matrix, _pure_c, mixed = decompose_packet(c_axis, modulus, RIGHT_DEGREE, 1)
    _eigen_0, eigen_1, eigen_2 = right_eigenvectors(mixed, c_axis, modulus)

    template_hit_count = 0
    packet_hit_count = 0
    eigen_1_hits = 0
    eigen_2_hits = 0
    pure_zone_hits = 0
    mixed_zone_hits = 0
    bits_by_index: list[tuple[int, int, int]] = []
    expected_eigen_1: list[int] = []
    expected_eigen_2: list[int] = []

    for c_index in range(c_axis):
        bits = carry_bits_from_crt(c_axis, c_index)
        expected_bits = template_bits(c_axis, c_index)
        bits_by_index.append(bits)
        template_hit_count += int(bits == expected_bits)

        for right in range(RIGHT_DEGREE):
            packet_value = packet[right * c_axis + c_index]
            packet_hit_count += int(packet_value == RIGHT_DEGREE * c_axis * bits[right] % modulus)

        expected_1 = expected_eigenvalue(c_axis, modulus, bits, 1)
        expected_2 = expected_eigenvalue(c_axis, modulus, bits, 2)
        expected_eigen_1.append(expected_1)
        expected_eigen_2.append(expected_2)
        eigen_1_hits += int(eigen_1[c_index] == expected_1)
        eigen_2_hits += int(eigen_2[c_index] == expected_2)

        pure_zone = c_index <= m_value or c_index > 3 * m_value
        mixed_zone = m_value < c_index <= 3 * m_value
        pure_zone_hits += int(
            pure_zone and eigen_1[c_index] == 0 and eigen_2[c_index] == 0
        )
        mixed_zone_hits += int(
            mixed_zone and eigen_1[c_index] != 0 and eigen_2[c_index] != 0
        )

    support_1 = support_interval(eigen_1, modulus)
    support_2 = support_interval(eigen_2, modulus)
    expected_support = (m_value + 1, 3 * m_value, 2 * m_value)
    row_ok = (
        template_hit_count == c_axis
        and packet_hit_count == RIGHT_DEGREE * c_axis
        and eigen_1_hits == c_axis
        and eigen_2_hits == c_axis
        and pure_zone_hits == (m_value + 1) + m_value
        and mixed_zone_hits == 2 * m_value
        and support_1 == expected_support
        and support_2 == expected_support
    )

    lines = [
        (
            f"case {case.name}: c={c_axis} modulus={modulus} m={m_value} "
            f"template_bit_hits={template_hit_count}/{c_axis} "
            f"packet_carry_hits={packet_hit_count}/{RIGHT_DEGREE * c_axis} "
            f"eigen_1_template_hits={eigen_1_hits}/{c_axis} "
            f"eigen_2_template_hits={eigen_2_hits}/{c_axis} "
            f"pure_zone_zero_hits={pure_zone_hits}/{2 * m_value + 1} "
            f"mixed_zone_nonzero_hits={mixed_zone_hits}/{2 * m_value} "
            f"support_1={support_1} support_2={support_2} "
            f"expected_support={expected_support} "
            f"ok={int(row_ok)}"
        ),
        f"  bit_count_profile={bit_count_profile(bits_by_index)}",
        (
            "  zone_lengths="
            f"zero:{m_value + 1} one_hot:{m_value} "
            f"two_hot:{m_value} all_rows:{m_value}"
        ),
        (
            "  canonical_payload_values="
            f"first_nonzero={expected_eigen_1[m_value + 1]} "
            f"middle_boundary=({expected_eigen_1[2 * m_value]}, "
            f"{expected_eigen_1[2 * m_value + 1]}) "
            f"last_nonzero={expected_eigen_1[3 * m_value]}"
        ),
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B canonical half-arc gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"canonical_half_arc_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  canonical_theta_3_1_raw_carry_has_four_C_axis_zones=1")
    print("  nontrivial_right_projection_is_supported_on_the_middle_half_arc=1")
    print("  one_hot_and_two_hot_zones_give_the_full_canonical_payload_vector=1")
    print("  pure_zero_and_all_rows_zones_vanish_after_right_character_projection=1")
    print("conclusion=reported_p25_laneB_canonical_half_arc_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())

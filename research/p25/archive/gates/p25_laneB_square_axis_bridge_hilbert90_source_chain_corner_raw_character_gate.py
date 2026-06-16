#!/usr/bin/env python3
"""Raw character factorization for p25 Hilbert-90 source-chain corners.

The corner K-trace selector says the active half-bridge corner must be lifted as
a 25-point right-kernel block.  This gate records the corresponding character
factorization: each active raw corner is exactly

    K_trace * quotient_corner,

where K_trace kills all non-quotient raw characters and the quotient corner has
only the forced C_3 row-balance zeros.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate import (
    profile as corner_raw_k_trace_profile,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    KERNEL_SHIFT,
    MODULUS,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Coord = tuple[int, int]


@dataclass(frozen=True)
class CornerRawCharacterRow:
    orientation_mask: int
    boundary_direction_q: int
    chain_q_values: tuple[int, ...]
    coefficient: int
    raw_support: int
    character_count: int
    zero_count: int
    nonzero_count: int
    kernel_trace_zeros: int
    quotient_zero_chars: tuple[Coord, ...]
    other_zero_chars: tuple[Coord, ...]
    nonzero_a_values: tuple[int, ...]
    factorization_ok: bool


@dataclass(frozen=True)
class CornerRawCharacterProfile:
    row_count: int
    rows: tuple[CornerRawCharacterRow, ...]
    all_rows_factor: bool
    all_rows_have_kernel_trace_zeros: bool
    all_rows_have_only_forced_row_zeros: bool
    all_rows_survive_on_quotient_characters_only: bool


def character_value(zeta_right: int, zeta_c: int, a_char: int, b_char: int, coord: Coord) -> int:
    right_log, c_log = coord
    return (
        pow(zeta_right, a_char * right_log, MODULUS)
        * pow(zeta_c, b_char * c_log, MODULUS)
    ) % MODULUS


def quotient_corner_coords(q_values: tuple[int, ...]) -> tuple[Coord, ...]:
    return tuple((q_value % RIGHT_ORDER, q_value % C_ORDER) for q_value in q_values)


def raw_corner_coords(q_values: tuple[int, ...]) -> tuple[Coord, ...]:
    coords: list[Coord] = []
    for q_value in q_values:
        for layer in range(25):
            e_value = q_value + QUOTIENT_ORDER * layer
            coords.append((e_value % RIGHT_ORDER, e_value % C_ORDER))
    return tuple(coords)


def row_profile(block_row) -> CornerRawCharacterRow:
    root = primitive_root(MODULUS)
    zeta_right = pow(root, (MODULUS - 1) // RIGHT_ORDER, MODULUS)
    zeta_c = pow(root, (MODULUS - 1) // C_ORDER, MODULUS)
    coefficient = block_row.coefficient % MODULUS
    quotient_coords = quotient_corner_coords(block_row.chain_q_values)
    raw_coords = raw_corner_coords(block_row.chain_q_values)

    zero_count = 0
    kernel_trace_zeros = 0
    quotient_zero_chars: list[Coord] = []
    other_zero_chars: list[Coord] = []
    nonzero_a_values: set[int] = set()
    factorization_ok = True

    for a_char in range(RIGHT_ORDER):
        for b_char in range(C_ORDER):
            raw_total = sum(
                coefficient * character_value(zeta_right, zeta_c, a_char, b_char, coord)
                for coord in raw_coords
            ) % MODULUS
            quotient_total = sum(
                coefficient * character_value(zeta_right, zeta_c, a_char, b_char, coord)
                for coord in quotient_coords
            ) % MODULUS
            chi_kernel = character_value(zeta_right, zeta_c, a_char, b_char, KERNEL_SHIFT)
            kernel_factor = sum(pow(chi_kernel, layer, MODULUS) for layer in range(25)) % MODULUS
            if raw_total != kernel_factor * quotient_total % MODULUS:
                factorization_ok = False

            if raw_total == 0:
                zero_count += 1
                if kernel_factor == 0:
                    kernel_trace_zeros += 1
                elif quotient_total == 0:
                    quotient_zero_chars.append((a_char, b_char))
                else:
                    other_zero_chars.append((a_char, b_char))
            else:
                nonzero_a_values.add(a_char)

    character_count = RIGHT_ORDER * C_ORDER
    return CornerRawCharacterRow(
        orientation_mask=block_row.orientation_mask,
        boundary_direction_q=block_row.boundary_direction_q,
        chain_q_values=block_row.chain_q_values,
        coefficient=block_row.coefficient,
        raw_support=block_row.raw_support,
        character_count=character_count,
        zero_count=zero_count,
        nonzero_count=character_count - zero_count,
        kernel_trace_zeros=kernel_trace_zeros,
        quotient_zero_chars=tuple(quotient_zero_chars),
        other_zero_chars=tuple(other_zero_chars),
        nonzero_a_values=tuple(sorted(nonzero_a_values)),
        factorization_ok=factorization_ok,
    )


def corner_raw_character_profile() -> CornerRawCharacterProfile:
    rows = tuple(row_profile(row) for row in corner_raw_k_trace_profile().block_k_trace_rows)
    return CornerRawCharacterProfile(
        row_count=len(rows),
        rows=rows,
        all_rows_factor=all(row.factorization_ok for row in rows),
        all_rows_have_kernel_trace_zeros=all(row.kernel_trace_zeros == 12168 for row in rows),
        all_rows_have_only_forced_row_zeros=all(
            row.quotient_zero_chars == ((25, 0), (50, 0))
            and row.other_zero_chars == ()
            for row in rows
        ),
        all_rows_survive_on_quotient_characters_only=all(
            row.nonzero_a_values == (0, 25, 50)
            for row in rows
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain corner raw-character gate")
    profile = corner_raw_character_profile()
    expected_rows = (
        CornerRawCharacterRow(1, 197, (0, 172, 482), -1, 75, 12675, 12170, 505, 12168, ((25, 0), (50, 0)), (), (0, 25, 50), True),
        CornerRawCharacterRow(1, 310, (172, 197, 369), 1, 75, 12675, 12170, 505, 12168, ((25, 0), (50, 0)), (), (0, 25, 50), True),
        CornerRawCharacterRow(6, 197, (138, 310, 335), -1, 75, 12675, 12170, 505, 12168, ((25, 0), (50, 0)), (), (0, 25, 50), True),
        CornerRawCharacterRow(6, 310, (0, 25, 335), 1, 75, 12675, 12170, 505, 12168, ((25, 0), (50, 0)), (), (0, 25, 50), True),
    )
    row_ok = (
        profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_rows_factor
        and profile.all_rows_have_kernel_trace_zeros
        and profile.all_rows_have_only_forced_row_zeros
        and profile.all_rows_survive_on_quotient_characters_only
    )

    print(
        "corner_raw_character_summary: "
        f"row_count={profile.row_count} "
        f"factorization={int(profile.all_rows_factor)} "
        f"kernel_trace_zeros={int(profile.all_rows_have_kernel_trace_zeros)} "
        f"only_forced_row_zeros={int(profile.all_rows_have_only_forced_row_zeros)} "
        f"quotient_characters_only={int(profile.all_rows_survive_on_quotient_characters_only)}"
    )
    print("corner_raw_character_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("raw_character_factorization")
    print("  corner_hat_raw(a,b) = K(a) * corner_hat_quotient(a,b)")
    print("  K(a) = sum_{j=0}^{24} chi(57,0)^j")
    print("  K(a) kills every raw right character with a not in {0,25,50}")
    print("  surviving quotient-corner zeros are exactly the two C3 row-balance characters")
    print("interpretation")
    print("  forced_K_trace_cleanly_projects_the_corner_to_C3xC169=1")
    print("  quotient_corner_has_no_extra_low_frequency_or_proper_quotient_zero=1")
    print("  producer_must_still_realize_the_active_quotient_corner_after_the_K_trace=1")
    print(f"square_axis_bridge_hilbert90_source_chain_corner_raw_character_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_character_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

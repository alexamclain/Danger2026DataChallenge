#!/usr/bin/env python3
"""Fourier footprint screen for p25 Hilbert-90 source chains.

The coefficient-rigidity gate pins the bridge target to four support-three
source graphs with all-equal coefficients and a rigid 197/310 first boundary.
This gate checks the character-side content of that target.

The result is deliberately mixed.  The active chain has only the two forced
C_3 row-sum zeros; the primitive first boundary adds only the scalar zero,
which gives the bridge's full zero set.  But this Fourier footprint does not
select the active C_169 lift: among the thirteen primitive lifts of the same
C_13 projective shadow, eleven have the same forced-zero profile.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    MODULUS,
    boundary,
    coord_from_q,
    inversion_boundary,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    CoefficientRigidityRow,
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate import (
    DiffTriple,
    projective_shape_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, SQUARE_C
from p25_selected_defect_value_gate import RIGHT_DEGREE


CharacterPair = tuple[int, int]
Poly = dict[int, int]

FORCED_ROW_ZEROS: tuple[CharacterPair, ...] = ((1, 0), (2, 0))
BRIDGE_ZERO_PAIRS: tuple[CharacterPair, ...] = ((0, 0), (1, 0), (2, 0))
ACTIVE_LIFT: DiffTriple = (1, 18, 150)


@dataclass(frozen=True)
class ActiveChainFourierRow:
    orientation_mask: int
    boundary_direction_q: int
    boundary_direction_coord: tuple[int, int]
    q_values: tuple[int, ...]
    source_coords: tuple[tuple[int, int], ...]
    coefficients: tuple[int, ...]
    chain_support: int
    first_boundary_support: int
    bridge_image_support: int
    chain_zero_pairs: tuple[CharacterPair, ...]
    first_boundary_zero_pairs: tuple[CharacterPair, ...]
    bridge_image_zero_pairs: tuple[CharacterPair, ...]
    chain_zero_frequencies: tuple[int, ...]
    first_boundary_zero_frequencies: tuple[int, ...]
    bridge_image_matches_bridge: bool


@dataclass(frozen=True)
class LiftFourierRow:
    lift_shape_c169: DiffTriple
    representative_c_values: tuple[int, int, int]
    representative_q_values: tuple[int, int, int]
    c13_zero_pairs: tuple[CharacterPair, ...]
    c169_zero_pairs: tuple[CharacterPair, ...]
    c169_extra_zero_pairs: tuple[CharacterPair, ...]
    forced_only_c13: bool
    forced_only_c169: bool


@dataclass(frozen=True)
class ChainFourierProfile:
    active_rows: tuple[ActiveChainFourierRow, ...]
    lift_rows: tuple[LiftFourierRow, ...]
    active_row_count: int
    all_active_chains_have_only_forced_row_zeros: bool
    all_active_boundaries_add_only_scalar_zero: bool
    all_active_bridge_images_match_bridge: bool
    c13_lift_count: int
    all_c13_lifts_have_only_forced_shadow_zeros: bool
    c169_generic_lift_count: int
    c169_extra_zero_lifts: tuple[tuple[DiffTriple, tuple[CharacterPair, ...]], ...]
    active_lift_has_generic_fourier_profile: bool


def source_character_roots(c_axis: int) -> tuple[int, int]:
    root = primitive_root(MODULUS)
    zeta_3 = pow(root, (MODULUS - 1) // RIGHT_DEGREE, MODULUS)
    zeta_c = pow(root, (MODULUS - 1) // c_axis, MODULUS)
    return zeta_3, zeta_c


def source_zero_pairs(poly: Poly, c_axis: int) -> tuple[CharacterPair, ...]:
    zeta_3, zeta_c = source_character_roots(c_axis)
    zeros: list[CharacterPair] = []
    for a_char in range(RIGHT_DEGREE):
        for b_char in range(c_axis):
            total = sum(
                coefficient
                * pow(zeta_3, a_char * (q_value % RIGHT_DEGREE), MODULUS)
                * pow(zeta_c, b_char * (q_value % c_axis), MODULUS)
                for q_value, coefficient in poly.items()
            ) % MODULUS
            if total == 0:
                zeros.append((a_char, b_char))
    return tuple(zeros)


def source_pair_to_quotient_frequency(pair: CharacterPair) -> int:
    a_char, b_char = pair
    return (SQUARE_C * a_char + RIGHT_DEGREE * b_char) % QUOTIENT_ORDER


def zero_frequencies(pairs: tuple[CharacterPair, ...]) -> tuple[int, ...]:
    return tuple(sorted(source_pair_to_quotient_frequency(pair) for pair in pairs))


def q_from_coord(row: int, c_value: int) -> int:
    return (c_value + SQUARE_C * ((row - c_value) % RIGHT_DEGREE)) % QUOTIENT_ORDER


def representative_chain_for_lift(lift: DiffTriple) -> tuple[tuple[int, int, int], Poly]:
    c_values = (0, lift[0], (lift[0] + lift[1]) % SQUARE_C)
    q_values = tuple(q_from_coord(row, c_values[row]) for row in range(RIGHT_DEGREE))
    return c_values, {q_value: 1 for q_value in q_values}


def active_chain_row(row: CoefficientRigidityRow) -> ActiveChainFourierRow:
    chain = dict(zip(row.q_values, row.recorded_coefficients))
    first_boundary = boundary(chain, row.boundary_direction_q)
    bridge_image = inversion_boundary(first_boundary)
    chain_zero_pairs = source_zero_pairs(chain, SQUARE_C)
    first_boundary_zero_pairs = source_zero_pairs(first_boundary, SQUARE_C)
    bridge_image_zero_pairs = source_zero_pairs(bridge_image, SQUARE_C)
    return ActiveChainFourierRow(
        orientation_mask=row.orientation_mask,
        boundary_direction_q=row.boundary_direction_q,
        boundary_direction_coord=coord_from_q(row.boundary_direction_q),
        q_values=row.q_values,
        source_coords=tuple(coord_from_q(q_value) for q_value in row.q_values),
        coefficients=row.recorded_coefficients,
        chain_support=len(chain),
        first_boundary_support=len(first_boundary),
        bridge_image_support=len(bridge_image),
        chain_zero_pairs=chain_zero_pairs,
        first_boundary_zero_pairs=first_boundary_zero_pairs,
        bridge_image_zero_pairs=bridge_image_zero_pairs,
        chain_zero_frequencies=zero_frequencies(chain_zero_pairs),
        first_boundary_zero_frequencies=zero_frequencies(first_boundary_zero_pairs),
        bridge_image_matches_bridge=bridge_image == bridge_coefficients(),
    )


def lift_fourier_row(lift: DiffTriple) -> LiftFourierRow:
    c_values, chain = representative_chain_for_lift(lift)
    q_values = tuple(chain)
    c13_zeros = source_zero_pairs(chain, 13)
    c169_zeros = source_zero_pairs(chain, SQUARE_C)
    extra_zeros = tuple(pair for pair in c169_zeros if pair not in FORCED_ROW_ZEROS)
    return LiftFourierRow(
        lift_shape_c169=lift,
        representative_c_values=c_values,
        representative_q_values=q_values,  # type: ignore[arg-type]
        c13_zero_pairs=c13_zeros,
        c169_zero_pairs=c169_zeros,
        c169_extra_zero_pairs=extra_zeros,
        forced_only_c13=c13_zeros == FORCED_ROW_ZEROS,
        forced_only_c169=c169_zeros == FORCED_ROW_ZEROS,
    )


def chain_fourier_profile() -> ChainFourierProfile:
    active_rows = tuple(active_chain_row(row) for row in coefficient_rigidity_profile().rows)
    lift_rows = tuple(
        lift_fourier_row(lift)
        for lift in projective_shape_profile().canonical_c13_lifts
    )
    extra_zero_lifts = tuple(
        (row.lift_shape_c169, row.c169_extra_zero_pairs)
        for row in lift_rows
        if row.c169_extra_zero_pairs
    )
    active_lift_row = next(row for row in lift_rows if row.lift_shape_c169 == ACTIVE_LIFT)
    return ChainFourierProfile(
        active_rows=active_rows,
        lift_rows=lift_rows,
        active_row_count=len(active_rows),
        all_active_chains_have_only_forced_row_zeros=all(
            row.chain_zero_pairs == FORCED_ROW_ZEROS for row in active_rows
        ),
        all_active_boundaries_add_only_scalar_zero=all(
            row.first_boundary_zero_pairs == BRIDGE_ZERO_PAIRS
            and row.bridge_image_zero_pairs == BRIDGE_ZERO_PAIRS
            for row in active_rows
        ),
        all_active_bridge_images_match_bridge=all(
            row.bridge_image_matches_bridge for row in active_rows
        ),
        c13_lift_count=len(lift_rows),
        all_c13_lifts_have_only_forced_shadow_zeros=all(
            row.forced_only_c13 for row in lift_rows
        ),
        c169_generic_lift_count=sum(row.forced_only_c169 for row in lift_rows),
        c169_extra_zero_lifts=extra_zero_lifts,
        active_lift_has_generic_fourier_profile=active_lift_row.forced_only_c169,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain Fourier gate")
    profile = chain_fourier_profile()
    expected_extra_zero_lifts = (
        ((1, 4, 164), ((2, 16),)),
        ((1, 10, 158), ((2, 167),)),
    )
    row_ok = (
        profile.active_row_count == 4
        and profile.all_active_chains_have_only_forced_row_zeros
        and profile.all_active_boundaries_add_only_scalar_zero
        and profile.all_active_bridge_images_match_bridge
        and profile.c13_lift_count == 13
        and profile.all_c13_lifts_have_only_forced_shadow_zeros
        and profile.c169_generic_lift_count == 11
        and profile.c169_extra_zero_lifts == expected_extra_zero_lifts
        and profile.active_lift_has_generic_fourier_profile
    )

    print(
        "active_chain_fourier_summary: "
        f"active_row_count={profile.active_row_count} "
        f"chain_zero_pairs={FORCED_ROW_ZEROS} "
        f"bridge_zero_pairs={BRIDGE_ZERO_PAIRS} "
        f"all_active_chains_have_only_forced_row_zeros="
        f"{int(profile.all_active_chains_have_only_forced_row_zeros)} "
        f"all_active_boundaries_add_only_scalar_zero="
        f"{int(profile.all_active_boundaries_add_only_scalar_zero)} "
        f"all_active_bridge_images_match_bridge="
        f"{int(profile.all_active_bridge_images_match_bridge)}"
    )
    print("active_chain_fourier_rows")
    for row in profile.active_rows:
        print(f"  {row}")
    print(
        "c13_shadow_lift_fourier_summary: "
        f"c13_lift_count={profile.c13_lift_count} "
        f"all_c13_lifts_have_only_forced_shadow_zeros="
        f"{int(profile.all_c13_lifts_have_only_forced_shadow_zeros)} "
        f"c169_generic_lift_count={profile.c169_generic_lift_count} "
        f"extra_zero_lifts={profile.c169_extra_zero_lifts} "
        f"active_lift_has_generic_fourier_profile="
        f"{int(profile.active_lift_has_generic_fourier_profile)}"
    )
    print("lift_fourier_rows")
    for row in profile.lift_rows:
        print(f"  {row}")
    print("interpretation")
    print("  active_support_three_chains_have_only_the_two_forced_C3_row_sum_zeros=1")
    print("  primitive_197_310_first_boundary_adds_only_the_scalar_zero=1")
    print("  first_boundary_then_inversion_has_exactly_the_bridge_fourier_zero_set=1")
    print("  C13_shadow_zero_profile_is_identical_for_all_thirteen_C169_lifts=1")
    print("  Fourier_zero_profile_prunes_only_two_of_thirteen_lifts_and_not_the_active_lift=1")
    print("  spectral_zeros_alone_cannot_select_the_active_nonsplit_C169_source_chain_lift=1")
    print(f"square_axis_bridge_hilbert90_source_chain_fourier_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_fourier_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

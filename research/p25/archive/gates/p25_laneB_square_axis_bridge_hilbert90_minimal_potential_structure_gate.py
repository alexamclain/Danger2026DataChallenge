#!/usr/bin/env python3
"""Structure screen for the p25 bridge Hilbert-90 minimal potentials.

The previous gate classified the eight smallest degree-zero Hilbert-90
potentials.  This gate asks whether those four-block targets have an easy
producer-facing explanation:

* a hidden affine parallelogram / signed 2 x 2 product;
* sparse or bridge-compatible Fourier zeros;
* a sparse quotient-circulant multiplier H with H * F = bridge.

The answer is negative.  The best bridge-compatible quotient multipliers are
still dense on at least 500 of 507 quotient classes, and two of the eight
potentials have an extra primitive zero where the bridge is nonzero.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate import (
    MinimalPotential,
    minimal_potential_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


MODULUS = 2029


Poly = dict[int, int]


@dataclass(frozen=True)
class RatioProfile:
    possible: bool
    obstruction_zeros: tuple[int, ...]
    free_frequencies: tuple[int, ...]
    best_zero_count: int | None
    minimal_multiplier_support: int | None
    best_free_modes: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class PotentialStructure:
    orientation_mask: int
    trace_values: tuple[tuple[int, int], ...]
    affine_parallelogram_count: int
    signed_2x2_product_count: int
    fourier_zeros: tuple[int, ...]
    fourier_zero_gcd_histogram: tuple[tuple[int, int], ...]
    bridge_zero_subset_ok: bool
    bridge_ratio: RatioProfile


@dataclass(frozen=True)
class MinimalPotentialStructureProfile:
    bridge_zeros: tuple[int, ...]
    product_obstruction_count: int
    ratio_possible_masks: tuple[int, ...]
    ratio_impossible_masks: tuple[int, ...]
    best_ratio_support_by_mask: tuple[tuple[int, int], ...]
    bridge_zero_match_masks: tuple[int, ...]
    extra_primitive_zero_masks: tuple[tuple[int, tuple[int, ...]], ...]
    structures: tuple[PotentialStructure, ...]


def potential_poly(row: MinimalPotential) -> Poly:
    return dict(row.trace_values)


def dft(poly: Poly, zeta: int) -> list[int]:
    return [
        sum(coefficient * pow(zeta, frequency * q_value, MODULUS) for q_value, coefficient in poly.items())
        % MODULUS
        for frequency in range(QUOTIENT_ORDER)
    ]


def inverse_dft(values: list[int], zeta: int) -> list[int]:
    inverse_order = pow(QUOTIENT_ORDER, -1, MODULUS)
    return [
        sum(values[frequency] * pow(zeta, -frequency * q_value, MODULUS) for frequency in range(QUOTIENT_ORDER))
        * inverse_order
        % MODULUS
        for q_value in range(QUOTIENT_ORDER)
    ]


def fourier_zeros(poly: Poly, zeta: int) -> tuple[int, ...]:
    coefficients = dft(poly, zeta)
    return tuple(index for index, value in enumerate(coefficients) if value == 0)


def zero_gcd_histogram(zeros: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(gcd(zero, QUOTIENT_ORDER) for zero in zeros).items()))


def affine_parallelogram_count(poly: Poly) -> int:
    support = tuple(poly)
    count = 0
    for base in support:
        shifted = [((q_value - base) % QUOTIENT_ORDER) for q_value in support if q_value != base]
        shifted_set = set(shifted)
        for a_index, a_value in enumerate(shifted):
            for b_value in shifted[a_index + 1 :]:
                if (a_value + b_value) % QUOTIENT_ORDER in shifted_set:
                    count += 1
    return count


def signed_2x2_product_count(poly: Poly) -> int:
    count = 0
    support = tuple(poly)
    for base in support:
        shifted = {
            (q_value - base) % QUOTIENT_ORDER: coefficient
            for q_value, coefficient in poly.items()
        }
        nonzero = [q_value for q_value in shifted if q_value != 0]
        for a_value in nonzero:
            for b_value in nonzero:
                if a_value == b_value:
                    continue
                c_value = (a_value + b_value) % QUOTIENT_ORDER
                if c_value not in shifted or len({0, a_value, b_value, c_value}) != 4:
                    continue
                # A scalar multiple of (1+s*x^a)(1+t*x^b) must satisfy this.
                if shifted[0] * shifted[c_value] == shifted[a_value] * shifted[b_value]:
                    count += 1
    return count


def optimize_free_ratio_support(canonical_multiplier: list[int], free_frequencies: tuple[int, ...]) -> tuple[int, int, tuple[tuple[int, int, int], ...]]:
    if free_frequencies == (0,):
        value, zero_count = Counter(canonical_multiplier).most_common(1)[0]
        return zero_count, QUOTIENT_ORDER - zero_count, ((0, value, zero_count),)

    if free_frequencies == (0, 169, 338):
        best_zero_count = 0
        modes: list[tuple[int, int, int]] = []
        for residue in range(3):
            value, zero_count = Counter(
                canonical_multiplier[q_value]
                for q_value in range(QUOTIENT_ORDER)
                if q_value % 3 == residue
            ).most_common(1)[0]
            best_zero_count += zero_count
            modes.append((residue, value, zero_count))
        return best_zero_count, QUOTIENT_ORDER - best_zero_count, tuple(modes)

    raise AssertionError(f"unexpected free frequencies {free_frequencies}")


def ratio_profile(poly: Poly, bridge: Poly, zeta: int, bridge_zeros: tuple[int, ...]) -> RatioProfile:
    potential_coefficients = dft(poly, zeta)
    bridge_coefficients_dft = dft(bridge, zeta)
    potential_zeros = tuple(index for index, value in enumerate(potential_coefficients) if value == 0)
    obstruction_zeros = tuple(index for index in potential_zeros if index not in bridge_zeros)
    if obstruction_zeros:
        return RatioProfile(
            possible=False,
            obstruction_zeros=obstruction_zeros,
            free_frequencies=potential_zeros,
            best_zero_count=None,
            minimal_multiplier_support=None,
            best_free_modes=(),
        )

    frequency_multiplier = [
        0 if potential_coefficients[index] == 0 else bridge_coefficients_dft[index] * pow(potential_coefficients[index], -1, MODULUS) % MODULUS
        for index in range(QUOTIENT_ORDER)
    ]
    canonical_multiplier = inverse_dft(frequency_multiplier, zeta)
    best_zero_count, minimal_support, modes = optimize_free_ratio_support(
        canonical_multiplier,
        potential_zeros,
    )
    return RatioProfile(
        possible=True,
        obstruction_zeros=(),
        free_frequencies=potential_zeros,
        best_zero_count=best_zero_count,
        minimal_multiplier_support=minimal_support,
        best_free_modes=modes,
    )


def structure_profile() -> MinimalPotentialStructureProfile:
    root = primitive_root(MODULUS)
    zeta = pow(root, (MODULUS - 1) // QUOTIENT_ORDER, MODULUS)
    bridge = bridge_coefficients()
    bridge_zeros = fourier_zeros(bridge, zeta)
    minimal = minimal_potential_profile()
    structures: list[PotentialStructure] = []

    for row in minimal.potentials:
        poly = potential_poly(row)
        zeros = fourier_zeros(poly, zeta)
        structures.append(
            PotentialStructure(
                orientation_mask=row.orientation_mask,
                trace_values=row.trace_values,
                affine_parallelogram_count=affine_parallelogram_count(poly),
                signed_2x2_product_count=signed_2x2_product_count(poly),
                fourier_zeros=zeros,
                fourier_zero_gcd_histogram=zero_gcd_histogram(zeros),
                bridge_zero_subset_ok=all(index in bridge_zeros for index in zeros),
                bridge_ratio=ratio_profile(poly, bridge, zeta, bridge_zeros),
            )
        )

    ratio_possible = tuple(row.orientation_mask for row in structures if row.bridge_ratio.possible)
    ratio_impossible = tuple(row.orientation_mask for row in structures if not row.bridge_ratio.possible)
    best_support = tuple(
        (row.orientation_mask, row.bridge_ratio.minimal_multiplier_support)
        for row in structures
        if row.bridge_ratio.minimal_multiplier_support is not None
    )
    bridge_zero_match = tuple(
        row.orientation_mask for row in structures if row.fourier_zeros == bridge_zeros
    )
    extra_primitive = tuple(
        (row.orientation_mask, row.bridge_ratio.obstruction_zeros)
        for row in structures
        if row.bridge_ratio.obstruction_zeros
    )
    return MinimalPotentialStructureProfile(
        bridge_zeros=bridge_zeros,
        product_obstruction_count=sum(
            row.affine_parallelogram_count == 0 and row.signed_2x2_product_count == 0
            for row in structures
        ),
        ratio_possible_masks=ratio_possible,
        ratio_impossible_masks=ratio_impossible,
        best_ratio_support_by_mask=best_support,  # type: ignore[arg-type]
        bridge_zero_match_masks=bridge_zero_match,
        extra_primitive_zero_masks=extra_primitive,
        structures=tuple(structures),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 minimal-potential structure gate")
    profile = structure_profile()
    expected_structures = (
        PotentialStructure(0, ((0, -3), (25, 1), (197, 1), (369, 1)), 0, 0, (0,), ((507, 1),), True, RatioProfile(True, (), (0,), 4, 503, ((0, 1821, 4),))),
        PotentialStructure(1, ((0, -1), (197, 1), (369, 1), (482, -1)), 0, 0, (0, 169, 338), ((169, 2), (507, 1)), True, RatioProfile(True, (), (0, 169, 338), 7, 500, ((0, 895, 2), (1, 861, 3), (2, 1358, 2)))),
        PotentialStructure(2, ((0, -1), (25, 1), (310, -1), (369, 1)), 0, 0, (0, 169, 258, 338), ((3, 1), (169, 2), (507, 1)), False, RatioProfile(False, (258,), (0, 169, 258, 338), None, None, ())),
        PotentialStructure(3, ((0, 1), (310, -1), (369, 1), (482, -1)), 0, 0, (0,), ((507, 1),), True, RatioProfile(True, (), (0,), 3, 504, ((0, 1384, 3),))),
        PotentialStructure(4, ((0, -1), (25, 1), (138, -1), (197, 1)), 0, 0, (0,), ((507, 1),), True, RatioProfile(True, (), (0,), 3, 504, ((0, 1384, 3),))),
        PotentialStructure(5, ((0, 1), (138, -1), (197, 1), (482, -1)), 0, 0, (0, 169, 249, 338), ((3, 1), (169, 2), (507, 1)), False, RatioProfile(False, (249,), (0, 169, 249, 338), None, None, ())),
        PotentialStructure(6, ((0, 1), (25, 1), (138, -1), (310, -1)), 0, 0, (0, 169, 338), ((169, 2), (507, 1)), True, RatioProfile(True, (), (0, 169, 338), 7, 500, ((0, 1031, 2), (1, 839, 2), (2, 861, 3)))),
        PotentialStructure(7, ((0, 3), (138, -1), (310, -1), (482, -1)), 0, 0, (0,), ((507, 1),), True, RatioProfile(True, (), (0,), 4, 503, ((0, 1821, 4),))),
    )
    row_ok = (
        profile.bridge_zeros == (0, 169, 338)
        and profile.product_obstruction_count == 8
        and profile.ratio_possible_masks == (0, 1, 3, 4, 6, 7)
        and profile.ratio_impossible_masks == (2, 5)
        and profile.best_ratio_support_by_mask == ((0, 503), (1, 500), (3, 504), (4, 504), (6, 500), (7, 503))
        and profile.bridge_zero_match_masks == (1, 6)
        and profile.extra_primitive_zero_masks == ((2, (258,)), (5, (249,)))
        and profile.structures == expected_structures
    )

    print(f"bridge_zeros={profile.bridge_zeros}")
    print(
        "structure_summary: "
        f"product_obstruction_count={profile.product_obstruction_count}/8 "
        f"ratio_possible_masks={profile.ratio_possible_masks} "
        f"ratio_impossible_masks={profile.ratio_impossible_masks} "
        f"best_ratio_support_by_mask={profile.best_ratio_support_by_mask} "
        f"bridge_zero_match_masks={profile.bridge_zero_match_masks} "
        f"extra_primitive_zero_masks={profile.extra_primitive_zero_masks}"
    )
    print("minimal_potential_structures")
    for row in profile.structures:
        print(f"  {row}")
    print("interpretation")
    print("  no_minimal_potential_support_is_an_affine_parallelogram=1")
    print("  no_unit_coefficient_minimum_is_a_hidden_signed_2x2_product=1")
    print("  masks_2_and_5_have_extra_primitive_zeros_where_the_bridge_is_nonzero=1")
    print("  masks_1_and_6_match_the_bridge_zero_set_but_need_dense_quotient_multipliers=1")
    print("  every_possible_quotient_circulant_bridge_ratio_has_support_at_least_500_of_507=1")
    print("  hilbert90_minimal_potential_route_still_needs_a_genuine_nonsplit_anti_invariant_ratio=1")
    print(f"square_axis_bridge_hilbert90_minimal_potential_structure_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_minimal_potential_structure_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

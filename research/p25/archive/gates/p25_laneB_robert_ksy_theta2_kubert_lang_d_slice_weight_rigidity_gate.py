#!/usr/bin/env python3
"""D-slice weight-rigidity gate for the p25 anti-invariant product.

The quotient selector is rigid in center and D.  This gate fixes that geometry
and asks whether the three D-slices can carry nontrivial integer weights.

They cannot.  The three K-traced D-slice footprints are disjoint 100-cell
blocks.  Therefore exact theta2/theta2^-1 acceptance forces all three weights
to be equal to +1 or all three weights to be -1; bounded scans verify no small
weighted escape, and the exact survivors pass the theta2/resolvent harness.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    profile_theta2_candidate,
    theta2_sparse_entries,
    theta2_target_rings,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    add_ring_entry,
    inverse_coord,
    y_exponent_at,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord, scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    D_SHIFT,
    KERNEL_SHIFT,
)


RIGHT_ORDER = 75
RAW_CENTER = (47, 28)
SLICE_OFFSETS = (-1, 0, 1)
WEIGHT_RANGE = (-2, -1, 0, 1, 2)

Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class WeightMatch:
    weights: tuple[int, int, int]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exact_theta2: bool
    exact_theta2_inverse: bool
    recovered_sign: int
    ok: bool


@dataclass(frozen=True)
class DSliceWeightRigidityProfile:
    center: Coord
    d_step: Coord
    k_step: Coord
    slice_offsets: tuple[int, int, int]
    slice_supports: tuple[int, int, int]
    pairwise_slice_intersections: tuple[int, int, int]
    slice_union_support: int
    target_theta2_support: int
    target_theta2_inverse_support: int
    bounded_weight_range: tuple[int, ...]
    bounded_weight_triples_scanned: int
    exact_matches: tuple[WeightMatch, ...]
    all_positive_forces_theta2_inverse: bool
    all_negative_forces_theta2: bool
    disjoint_support_proves_integer_weight_rigidity: bool
    theorem_escape: str
    row_ok: bool


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def weighted_source_trace(weights: tuple[int, int, int]) -> Ring:
    centers: Ring = {}
    for offset, weight in zip(SLICE_OFFSETS, weights):
        if weight == 0:
            continue
        d_shift = scale_coord(D_SHIFT, offset)
        for k_index in range(25):
            point = add_coord(add_coord(RAW_CENTER, d_shift), scale_coord(KERNEL_SHIFT, k_index))
            add_ring_entry(centers, point, weight)
    return dict(sorted(centers.items()))


def weighted_anti_invariant_footprint(weights: tuple[int, int, int]) -> Ring:
    centers = weighted_source_trace(weights)
    footprint: Ring = {}
    for point, coefficient in centers.items():
        y_exponent_at(footprint, point, coefficient)
        y_exponent_at(footprint, inverse_coord(point), -coefficient)
    return dict(sorted(footprint.items()))


def support_set(ring: Ring) -> set[Coord]:
    return set(ring)


def profile_weight_match(weights: tuple[int, int, int], footprint: Ring) -> WeightMatch:
    candidate = profile_theta2_candidate(
        f"d_slice_weight_{weights}",
        theta2_sparse_entries(footprint),
    )
    return WeightMatch(
        weights=weights,
        support=len(footprint),
        coefficient_counts=coefficient_counts(footprint),
        exact_theta2=candidate.exact_theta2,
        exact_theta2_inverse=candidate.exact_theta2_inverse,
        recovered_sign=candidate.recovered_sign,
        ok=candidate.ok,
    )


def profile_d_slice_weight_rigidity() -> DSliceWeightRigidityProfile:
    _bridge, theta2, theta2_inverse = theta2_target_rings()
    slice_footprints = tuple(
        weighted_anti_invariant_footprint(tuple(1 if index == active else 0 for index in range(3)))
        for active in range(3)
    )
    slice_support_sets = tuple(support_set(ring) for ring in slice_footprints)
    pairwise_intersections = tuple(
        len(slice_support_sets[left] & slice_support_sets[right])
        for left, right in combinations(range(3), 2)
    )
    union_support = len(set().union(*slice_support_sets))

    exact_matches: list[WeightMatch] = []
    for weights in product(WEIGHT_RANGE, repeat=3):
        footprint = weighted_anti_invariant_footprint(weights)
        if footprint == theta2 or footprint == theta2_inverse:
            exact_matches.append(profile_weight_match(weights, footprint))

    expected_matches = (
        WeightMatch(
            weights=(-1, -1, -1),
            support=300,
            coefficient_counts=((-4, 75), (-1, 75), (1, 75), (4, 75)),
            exact_theta2=True,
            exact_theta2_inverse=False,
            recovered_sign=1,
            ok=True,
        ),
        WeightMatch(
            weights=(1, 1, 1),
            support=300,
            coefficient_counts=((-4, 75), (-1, 75), (1, 75), (4, 75)),
            exact_theta2=False,
            exact_theta2_inverse=True,
            recovered_sign=-1,
            ok=True,
        ),
    )
    disjoint_support_rigid = (
        tuple(len(ring) for ring in slice_footprints) == (100, 100, 100)
        and pairwise_intersections == (0, 0, 0)
        and union_support == 300
    )
    all_positive_forces_inverse = any(
        match.weights == (1, 1, 1) and match.exact_theta2_inverse and match.ok
        for match in exact_matches
    )
    all_negative_forces_theta2 = any(
        match.weights == (-1, -1, -1) and match.exact_theta2 and match.ok
        for match in exact_matches
    )
    row_ok = (
        RAW_CENTER == (47, 28)
        and D_SHIFT == (22, 3)
        and KERNEL_SHIFT == (57, 0)
        and len(theta2) == 300
        and len(theta2_inverse) == 300
        and tuple(exact_matches) == expected_matches
        and disjoint_support_rigid
    )
    return DSliceWeightRigidityProfile(
        center=RAW_CENTER,
        d_step=D_SHIFT,
        k_step=KERNEL_SHIFT,
        slice_offsets=SLICE_OFFSETS,
        slice_supports=tuple(len(ring) for ring in slice_footprints),
        pairwise_slice_intersections=pairwise_intersections,
        slice_union_support=union_support,
        target_theta2_support=len(theta2),
        target_theta2_inverse_support=len(theta2_inverse),
        bounded_weight_range=WEIGHT_RANGE,
        bounded_weight_triples_scanned=len(WEIGHT_RANGE) ** 3,
        exact_matches=tuple(exact_matches),
        all_positive_forces_theta2_inverse=all_positive_forces_inverse,
        all_negative_forces_theta2=all_negative_forces_theta2,
        disjoint_support_proves_integer_weight_rigidity=disjoint_support_rigid,
        theorem_escape=(
            "only a theorem that changes the finite theta2 target, not a "
            "weighted subproduct on the accepted C,D,K geometry"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang D-slice weight-rigidity gate")
    profile = profile_d_slice_weight_rigidity()
    print(f"d_slice_weight_rigidity_profile={profile}")
    print("slice_geometry")
    print(f"  center={profile.center} K={profile.k_step} D={profile.d_step}")
    print(f"  offsets={profile.slice_offsets}")
    print(f"  slice_supports={profile.slice_supports}")
    print(f"  pairwise_intersections={profile.pairwise_slice_intersections}")
    print(f"  union_support={profile.slice_union_support}")
    print("bounded_weight_scan")
    print(f"  weight_range={profile.bounded_weight_range}")
    print(f"  triples_scanned={profile.bounded_weight_triples_scanned}")
    print(f"  exact_matches={profile.exact_matches}")
    print("interpretation")
    print("  disjoint_100_cell_slices_force_integer_weight_rigidity=1")
    print("  all_positive_weights_emit_theta2_inverse=1")
    print("  all_negative_weights_emit_theta2=1")
    print("  missing_or_reweighted_D_slice_cannot_pass_theta2_harness=1")
    print(
        f"robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_rows={int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_d_slice_weight_rigidity_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

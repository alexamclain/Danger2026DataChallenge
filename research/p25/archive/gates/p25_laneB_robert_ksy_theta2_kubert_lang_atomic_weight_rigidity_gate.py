#!/usr/bin/env python3
"""Atomic weight-rigidity gate for the p25 anti-invariant product.

The center, D segment, and D-slice weights are already rigid.  This gate fixes
the accepted raw C,D,K geometry and allows an independent integer/rational
weight on every one of the 75 source atoms

    A = C + jD + kK,  j in {-1,0,1}, k in {0,...,24}.

Each atom contributes a disjoint four-cell anti-invariant normalized-y
footprint.  Therefore the exact theta2/theta2^-1 target reads off every atomic
weight independently: all +1 for theta2^-1, all -1 for theta2, with no null
direction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

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
from p25_laneB_square_axis_bridge_raw_source_character_gate import D_SHIFT, KERNEL_SHIFT


RAW_CENTER = (47, 28)
SLICE_OFFSETS = (-1, 0, 1)
K_LENGTH = 25

Coord = tuple[int, int]
AtomLabel = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class AtomicWeightSolution:
    target_name: str
    valid: bool
    weight_counts: tuple[tuple[str, int], ...]
    all_integral: bool
    all_equal: bool
    candidate_exact_theta2: bool
    candidate_exact_theta2_inverse: bool
    recovered_sign: int
    candidate_ok: bool


@dataclass(frozen=True)
class AtomicWeightRigidityProfile:
    center: Coord
    d_step: Coord
    k_step: Coord
    atom_count: int
    atom_support_sizes: tuple[int, ...]
    pairwise_intersecting_atom_pairs: int
    max_pairwise_atom_intersection: int
    atom_union_support: int
    linear_rank_from_disjoint_support: int
    linear_nullity_from_disjoint_support: int
    theta2_support: int
    theta2_inverse_support: int
    theta2_inverse_solution: AtomicWeightSolution
    theta2_solution: AtomicWeightSolution
    missing_atom_rejected: bool
    alternating_k_weights_rejected: bool
    theorem_escape: str
    row_ok: bool


def atom_labels() -> tuple[AtomLabel, ...]:
    return tuple((offset, k_index) for offset in SLICE_OFFSETS for k_index in range(K_LENGTH))


def atomic_footprint(offset: int, k_index: int) -> Ring:
    point = add_coord(
        add_coord(RAW_CENTER, scale_coord(D_SHIFT, offset)),
        scale_coord(KERNEL_SHIFT, k_index),
    )
    footprint: Ring = {}
    y_exponent_at(footprint, point, 1)
    y_exponent_at(footprint, inverse_coord(point), -1)
    return dict(sorted(footprint.items()))


def add_scaled_ring(out: Ring, ring: Ring, scalar: int) -> None:
    for coord, coefficient in ring.items():
        add_ring_entry(out, coord, scalar * coefficient)


def weighted_atom_footprint(weights: dict[AtomLabel, int]) -> Ring:
    out: Ring = {}
    for label in atom_labels():
        weight = weights.get(label, 0)
        if weight:
            add_scaled_ring(out, atomic_footprint(*label), weight)
    return dict(sorted(out.items()))


def fraction_counts(weights: tuple[Fraction, ...]) -> tuple[tuple[str, int], ...]:
    counts = Counter(str(weight) for weight in weights)
    return tuple(sorted(counts.items()))


def solve_disjoint_weights(target: Ring, atom_rings: tuple[Ring, ...]) -> tuple[bool, tuple[Fraction, ...]]:
    atom_union = set().union(*(set(ring) for ring in atom_rings))
    if set(target) - atom_union:
        return False, ()

    weights: list[Fraction] = []
    for atom in atom_rings:
        ratios = {Fraction(target.get(coord, 0), coefficient) for coord, coefficient in atom.items()}
        if len(ratios) != 1:
            return False, ()
        weights.append(ratios.pop())
    return True, tuple(weights)


def profile_solution(
    target_name: str,
    target: Ring,
    atom_rings: tuple[Ring, ...],
) -> AtomicWeightSolution:
    valid, weights = solve_disjoint_weights(target, atom_rings)
    all_integral = valid and all(weight.denominator == 1 for weight in weights)
    all_equal = valid and len(set(weights)) == 1
    candidate_ok = False
    exact_theta2 = False
    exact_theta2_inverse = False
    recovered_sign = 0
    if all_integral:
        integer_weights = {
            label: int(weight)
            for label, weight in zip(atom_labels(), weights)
            if weight
        }
        footprint = weighted_atom_footprint(integer_weights)
        candidate = profile_theta2_candidate(
            f"atomic_weight_solution_{target_name}",
            theta2_sparse_entries(footprint),
        )
        candidate_ok = candidate.ok
        exact_theta2 = candidate.exact_theta2
        exact_theta2_inverse = candidate.exact_theta2_inverse
        recovered_sign = candidate.recovered_sign
    return AtomicWeightSolution(
        target_name=target_name,
        valid=valid,
        weight_counts=fraction_counts(weights),
        all_integral=all_integral,
        all_equal=all_equal,
        candidate_exact_theta2=exact_theta2,
        candidate_exact_theta2_inverse=exact_theta2_inverse,
        recovered_sign=recovered_sign,
        candidate_ok=candidate_ok,
    )


def profile_atomic_weight_rigidity() -> AtomicWeightRigidityProfile:
    _bridge, theta2, theta2_inverse = theta2_target_rings()
    atom_rings = tuple(atomic_footprint(*label) for label in atom_labels())
    atom_supports = tuple(set(ring) for ring in atom_rings)
    pairwise_intersections = tuple(
        len(atom_supports[left] & atom_supports[right])
        for left in range(len(atom_supports))
        for right in range(left + 1, len(atom_supports))
    )
    intersecting_pairs = sum(1 for value in pairwise_intersections if value)
    max_intersection = max(pairwise_intersections, default=0)
    union_support = len(set().union(*atom_supports))
    rank = len(atom_rings) if max_intersection == 0 and all(atom_supports) else 0
    nullity = len(atom_rings) - rank

    theta2_inverse_solution = profile_solution("theta2_inverse", theta2_inverse, atom_rings)
    theta2_solution = profile_solution("theta2", theta2, atom_rings)

    all_one_weights = {label: 1 for label in atom_labels()}
    missing_atom_weights = dict(all_one_weights)
    missing_atom_weights[atom_labels()[0]] = 0
    missing_atom = profile_theta2_candidate(
        "atomic_weight_missing_atom_control",
        theta2_sparse_entries(weighted_atom_footprint(missing_atom_weights)),
    )
    alternating_weights = {
        label: 1 if label[1] % 2 == 0 else -1
        for label in atom_labels()
    }
    alternating_k = profile_theta2_candidate(
        "atomic_weight_alternating_k_control",
        theta2_sparse_entries(weighted_atom_footprint(alternating_weights)),
    )

    row_ok = (
        RAW_CENTER == (47, 28)
        and D_SHIFT == (22, 3)
        and KERNEL_SHIFT == (57, 0)
        and len(atom_rings) == 75
        and set(len(ring) for ring in atom_rings) == {4}
        and intersecting_pairs == 0
        and max_intersection == 0
        and union_support == 300
        and rank == 75
        and nullity == 0
        and len(theta2) == 300
        and len(theta2_inverse) == 300
        and theta2_inverse_solution.valid
        and theta2_inverse_solution.weight_counts == (("1", 75),)
        and theta2_inverse_solution.candidate_exact_theta2_inverse
        and theta2_inverse_solution.recovered_sign == -1
        and theta2_inverse_solution.candidate_ok
        and theta2_solution.valid
        and theta2_solution.weight_counts == (("-1", 75),)
        and theta2_solution.candidate_exact_theta2
        and theta2_solution.recovered_sign == 1
        and theta2_solution.candidate_ok
        and not missing_atom.ok
        and not alternating_k.ok
    )
    return AtomicWeightRigidityProfile(
        center=RAW_CENTER,
        d_step=D_SHIFT,
        k_step=KERNEL_SHIFT,
        atom_count=len(atom_rings),
        atom_support_sizes=tuple(sorted(set(len(ring) for ring in atom_rings))),
        pairwise_intersecting_atom_pairs=intersecting_pairs,
        max_pairwise_atom_intersection=max_intersection,
        atom_union_support=union_support,
        linear_rank_from_disjoint_support=rank,
        linear_nullity_from_disjoint_support=nullity,
        theta2_support=len(theta2),
        theta2_inverse_support=len(theta2_inverse),
        theta2_inverse_solution=theta2_inverse_solution,
        theta2_solution=theta2_solution,
        missing_atom_rejected=not missing_atom.ok,
        alternating_k_weights_rejected=not alternating_k.ok,
        theorem_escape=(
            "only an identity producing the exact equal-weight K-traced "
            "anti-invariant product, or a different accepted theta2 payload"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang atomic weight-rigidity gate")
    profile = profile_atomic_weight_rigidity()
    print(f"atomic_weight_rigidity_profile={profile}")
    print("atomic_geometry")
    print(f"  center={profile.center} K={profile.k_step} D={profile.d_step}")
    print(f"  atom_count={profile.atom_count}")
    print(f"  atom_support_sizes={profile.atom_support_sizes}")
    print(f"  pairwise_intersecting_atom_pairs={profile.pairwise_intersecting_atom_pairs}")
    print(f"  max_pairwise_atom_intersection={profile.max_pairwise_atom_intersection}")
    print(f"  atom_union_support={profile.atom_union_support}")
    print("linear_readoff")
    print(f"  rank={profile.linear_rank_from_disjoint_support}")
    print(f"  nullity={profile.linear_nullity_from_disjoint_support}")
    print(f"  theta2_inverse_solution={profile.theta2_inverse_solution}")
    print(f"  theta2_solution={profile.theta2_solution}")
    print("controls")
    print(f"  missing_atom_rejected={int(profile.missing_atom_rejected)}")
    print(f"  alternating_k_weights_rejected={int(profile.alternating_k_weights_rejected)}")
    print("interpretation")
    print("  every_K_traced_atom_has_a_disjoint_four_cell_footprint=1")
    print("  theta2_inverse_forces_all_75_atom_weights_to_plus_one=1")
    print("  theta2_forces_all_75_atom_weights_to_minus_one=1")
    print("  no_nonuniform_K_trace_or_atomic_weight_null_direction=1")
    print(f"robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

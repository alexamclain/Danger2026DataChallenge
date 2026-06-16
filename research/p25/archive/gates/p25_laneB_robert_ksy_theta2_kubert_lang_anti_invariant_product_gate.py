#!/usr/bin/env python3
"""Anti-invariant normalized-y product intake for the p25 KL/KSY lane.

The raw K-trace reflection gate shows that the KSY product y(A)/y(A+T) can be
viewed as y(A)/y(-A) after the full K trace.  This gate turns that observation
into an accepted theorem-output interface:

    center C, D step, K trace, and orientation.

The forward anti-invariant product emits theta2^-1; the reversed product emits
theta2.  Both feed the existing theta2 resolvent/certificate path.  Controls
show that the full K trace, the symmetric length-three D segment, and the
specific center are all required.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    KsyTheta2CandidateProfile,
    profile_theta2_candidate,
    theta2_sparse_entries,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_gate import (
    profile_raw_ktrace_reflection,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord, scale_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]


@dataclass(frozen=True)
class AntiInvariantProductRow:
    name: str
    orientation: str
    center: Coord
    k_step: Coord
    d_step: Coord
    k_length: int
    d_offsets: tuple[int, ...]
    center_support: int
    footprint_support: int
    footprint_coefficient_counts: tuple[tuple[int, int], ...]
    exact_theta2: bool
    exact_theta2_inverse: bool
    recovered_sign: int
    candidate_profile: KsyTheta2CandidateProfile
    ok: bool


@dataclass(frozen=True)
class AntiInvariantProductIntakeProfile:
    theorem_interface: str
    raw_center: Coord
    raw_base: Coord
    raw_k_step: Coord
    raw_d_step: Coord
    d_offsets: tuple[int, ...]
    compact_parameter_cells: int
    raw_reflection_bridge_ok: bool
    kernel_shifted_t_representatives_ok: int
    forward_product: AntiInvariantProductRow
    reverse_product: AntiInvariantProductRow
    missing_k_rejected: bool
    collapsed_k_rejected: bool
    truncated_d_rejected: bool
    wrong_d_rejected: bool
    shifted_center_rejected: bool
    source_parameter_budget: int
    theta2_payload_support: int
    bridge_support: int
    support_resolvent_term_budget: int
    support_resolvent_union_support: int
    next_debt: str
    row_ok: bool


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % RIGHT_ORDER, (-coord[1]) % C_ORDER)


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def y_exponent_at(out: Ring, point: Coord, coefficient: int) -> None:
    add_ring_entry(out, scale_coord(point, 2), coefficient)
    add_ring_entry(out, point, -4 * coefficient)


def centered_source_trace(
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
) -> Ring:
    centers: Ring = {}
    for offset in d_offsets:
        d_shift = scale_coord(d_step, offset)
        for k_index in range(k_length):
            point = add_coord(add_coord(center, d_shift), scale_coord(k_step, k_index))
            add_ring_entry(centers, point, 1)
    return dict(sorted(centers.items()))


def anti_invariant_y_footprint(
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
    reverse: bool = False,
) -> tuple[Ring, Ring]:
    centers = centered_source_trace(center, k_step, d_step, k_length, d_offsets)
    footprint: Ring = {}
    for point, coefficient in centers.items():
        left = inverse_coord(point) if reverse else point
        right = point if reverse else inverse_coord(point)
        y_exponent_at(footprint, left, coefficient)
        y_exponent_at(footprint, right, -coefficient)
    return centers, dict(sorted(footprint.items()))


def profile_anti_invariant_product(
    name: str,
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
    reverse: bool = False,
) -> AntiInvariantProductRow:
    centers, footprint = anti_invariant_y_footprint(
        center,
        k_step,
        d_step,
        k_length,
        d_offsets,
        reverse,
    )
    candidate = profile_theta2_candidate(name, theta2_sparse_entries(footprint))
    row_ok = (
        candidate.ok
        and len(centers) == 75
        and len(footprint) == 300
        and candidate.recovered_sign in (-1, 1)
    )
    return AntiInvariantProductRow(
        name=name,
        orientation="y(-A)/y(A)" if reverse else "y(A)/y(-A)",
        center=center,
        k_step=k_step,
        d_step=d_step,
        k_length=k_length,
        d_offsets=d_offsets,
        center_support=len(centers),
        footprint_support=len(footprint),
        footprint_coefficient_counts=coefficient_counts(footprint),
        exact_theta2=candidate.exact_theta2,
        exact_theta2_inverse=candidate.exact_theta2_inverse,
        recovered_sign=candidate.recovered_sign,
        candidate_profile=candidate,
        ok=row_ok,
    )


def profile_anti_invariant_product_intake() -> AntiInvariantProductIntakeProfile:
    raw_center = add_coord(BASE_POINT, D_SHIFT)
    raw_reflection = profile_raw_ktrace_reflection()
    forward = profile_anti_invariant_product(
        "anti_invariant_product_theta2_inverse",
        raw_center,
        KERNEL_SHIFT,
        D_SHIFT,
    )
    reverse = profile_anti_invariant_product(
        "anti_invariant_product_theta2",
        raw_center,
        KERNEL_SHIFT,
        D_SHIFT,
        reverse=True,
    )
    missing_k = profile_anti_invariant_product(
        "anti_invariant_product_missing_k_control",
        raw_center,
        KERNEL_SHIFT,
        D_SHIFT,
        k_length=1,
    )
    collapsed_k = profile_anti_invariant_product(
        "anti_invariant_product_collapsed_k_control",
        raw_center,
        (0, 0),
        D_SHIFT,
    )
    truncated_d = profile_anti_invariant_product(
        "anti_invariant_product_truncated_d_control",
        raw_center,
        KERNEL_SHIFT,
        D_SHIFT,
        d_offsets=(-1, 0),
    )
    wrong_d = profile_anti_invariant_product(
        "anti_invariant_product_wrong_d_control",
        raw_center,
        KERNEL_SHIFT,
        (D_SHIFT[0], (D_SHIFT[1] + 1) % C_ORDER),
    )
    shifted_center = profile_anti_invariant_product(
        "anti_invariant_product_shifted_center_control",
        add_coord(raw_center, D_SHIFT),
        KERNEL_SHIFT,
        D_SHIFT,
    )
    row_ok = (
        raw_center == (47, 28)
        and raw_reflection.row_ok
        and raw_reflection.kernel_shifted_t_representatives_ok == 25
        and forward.ok
        and forward.exact_theta2_inverse
        and forward.recovered_sign == -1
        and reverse.ok
        and reverse.exact_theta2
        and reverse.recovered_sign == 1
        and forward.center_support == 75
        and forward.footprint_support == 300
        and forward.footprint_coefficient_counts == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and forward.candidate_profile.shifted_theta2_term_budget == 46800
        and forward.candidate_profile.shifted_theta2_union_support == 11700
        and forward.candidate_profile.recovered_support == 150
        and not missing_k.ok
        and not collapsed_k.ok
        and not truncated_d.ok
        and not wrong_d.ok
        and not shifted_center.ok
    )
    return AntiInvariantProductIntakeProfile(
        theorem_interface="center C, primitive K trace, D step, orientation",
        raw_center=raw_center,
        raw_base=add_coord(raw_center, scale_coord(D_SHIFT, -1)),
        raw_k_step=KERNEL_SHIFT,
        raw_d_step=D_SHIFT,
        d_offsets=(-1, 0, 1),
        compact_parameter_cells=3,
        raw_reflection_bridge_ok=raw_reflection.row_ok,
        kernel_shifted_t_representatives_ok=raw_reflection.kernel_shifted_t_representatives_ok,
        forward_product=forward,
        reverse_product=reverse,
        missing_k_rejected=not missing_k.ok,
        collapsed_k_rejected=not collapsed_k.ok,
        truncated_d_rejected=not truncated_d.ok,
        wrong_d_rejected=not wrong_d.ok,
        shifted_center_rejected=not shifted_center.ok,
        source_parameter_budget=3,
        theta2_payload_support=forward.footprint_support,
        bridge_support=forward.candidate_profile.recovered_support,
        support_resolvent_term_budget=forward.candidate_profile.shifted_theta2_term_budget,
        support_resolvent_union_support=forward.candidate_profile.shifted_theta2_union_support,
        next_debt=(
            "prove a challenge-legal arithmetic identity for the raw "
            "K-traced anti-invariant normalized-y product; the finite intake "
            "now accepts center/D/K/orientation without an independent T edge"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang anti-invariant product gate")
    profile = profile_anti_invariant_product_intake()
    print(f"anti_invariant_product_intake_profile={profile}")
    print("accepted_interface")
    print(
        "  "
        f"center={profile.raw_center} K={profile.raw_k_step} D={profile.raw_d_step} "
        f"offsets={profile.d_offsets} parameter_cells={profile.compact_parameter_cells}"
    )
    print("products")
    print(
        "  "
        f"forward={profile.forward_product.orientation} "
        f"theta2_inverse={int(profile.forward_product.exact_theta2_inverse)} "
        f"recovered_sign={profile.forward_product.recovered_sign} "
        f"ok={int(profile.forward_product.ok)}"
    )
    print(
        "  "
        f"reverse={profile.reverse_product.orientation} "
        f"theta2={int(profile.reverse_product.exact_theta2)} "
        f"recovered_sign={profile.reverse_product.recovered_sign} "
        f"ok={int(profile.reverse_product.ok)}"
    )
    print("budgets")
    print(f"  theta2_payload_support={profile.theta2_payload_support}")
    print(f"  bridge_support={profile.bridge_support}")
    print(f"  support_resolvent_term_budget={profile.support_resolvent_term_budget}")
    print(f"  support_resolvent_union_support={profile.support_resolvent_union_support}")
    print("controls")
    print(f"  missing_K_rejected={int(profile.missing_k_rejected)}")
    print(f"  collapsed_K_rejected={int(profile.collapsed_k_rejected)}")
    print(f"  truncated_D_rejected={int(profile.truncated_d_rejected)}")
    print(f"  wrong_D_rejected={int(profile.wrong_d_rejected)}")
    print(f"  shifted_center_rejected={int(profile.shifted_center_rejected)}")
    print("interpretation")
    print("  anti_invariant_y_A_over_y_minus_A_emits_theta2_inverse=1")
    print("  reversed_anti_invariant_product_emits_theta2=1")
    print("  theorem_output_can_be_center_D_K_orientation_without_independent_T=1")
    print("  full_K_trace_symmetric_D_segment_and_exact_center_are_required=1")
    print(f"robert_ksy_theta2_kubert_lang_anti_invariant_product_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

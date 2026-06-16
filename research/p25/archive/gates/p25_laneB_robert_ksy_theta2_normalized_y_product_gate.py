#!/usr/bin/env python3
"""Normalized-y product source law for the p25 KSY theta2 route.

The D=2 obligation gate says a theorem should emit theta2 data.  This gate
spells out the most concrete KSY source template:

    prod_{A in base*K_trace*D_segment} y(A) / y(A+T),
    y(Q) = -g(2Q) / g(Q)^4.

At the finite divisor-footprint level this is exactly theta2^-1.  Reversing the
quotient emits theta2.  This is still not an arithmetic proof of the KSY
identity; it is the finite source-law target that such a proof must justify.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    KsyTheta2CandidateProfile,
    profile_theta2_candidate,
    theta2_sparse_entries,
)
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    half_step,
    inverse_step,
    normalized_y_exponent_footprint,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    geometric_factor,
    monomial,
    multiply_factors,
    scale_coord,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class NormalizedYProductProfile:
    name: str
    base: Coord
    k_step: Coord
    d_step: Coord
    t_step: Coord
    k_length: int
    d_length: int
    orientation: str
    center_base: Coord
    half_shift: Coord
    footprint_support: int
    footprint_coefficient_counts: tuple[tuple[int, int], ...]
    footprint_equals_compact_ksy: bool
    exact_theta2: bool
    exact_theta2_inverse: bool
    candidate_profile: KsyTheta2CandidateProfile
    ok: bool


@dataclass(frozen=True)
class NormalizedYProductSourceLawProfile:
    target_inverse_ok: bool
    target_theta2_ok: bool
    missing_k_rejected: bool
    collapsed_k_rejected: bool
    truncated_d_rejected: bool
    wrong_d_rejected: bool
    wrong_t_rejected: bool
    target_support: int
    source_parameter_budget: int
    theorem_source_law: str
    row_ok: bool


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def y_exponent_at(out: Ring, point: Coord, coefficient: int) -> None:
    # y(Q) = -g(2Q)/g(Q)^4 at divisor-footprint level.
    add_ring_entry(out, scale_coord(point, 2), coefficient)
    add_ring_entry(out, point, -4 * coefficient)


def source_centers(
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int,
    d_length: int,
) -> Ring:
    return multiply_factors(
        (
            ("base", monomial(base)),
            ("K_trace", geometric_factor(k_step, k_length)),
            ("D_segment", geometric_factor(d_step, d_length)),
        )
    )


def normalized_y_product_footprint(
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
    k_length: int = 25,
    d_length: int = 3,
    reverse: bool = False,
) -> Ring:
    centers = source_centers(base, k_step, d_step, k_length, d_length)
    out: Ring = {}
    for point, coefficient in centers.items():
        left = add_coord(point, t_step) if reverse else point
        right = point if reverse else add_coord(point, t_step)
        y_exponent_at(out, left, coefficient)
        y_exponent_at(out, right, -coefficient)
    return dict(sorted(out.items()))


def profile_normalized_y_product(
    name: str,
    base: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
    k_length: int = 25,
    d_length: int = 3,
    reverse: bool = False,
) -> NormalizedYProductProfile:
    footprint = normalized_y_product_footprint(
        base,
        k_step,
        d_step,
        t_step,
        k_length,
        d_length,
        reverse,
    )
    candidate = profile_theta2_candidate(name, theta2_sparse_entries(footprint))
    half = half_step(t_step)
    center_base = add_coord(base, half)
    half_shift = inverse_step(half)
    compact_reference = normalized_y_exponent_footprint(center_base, half_shift)
    if reverse:
        compact_reference = {coord: -coefficient for coord, coefficient in compact_reference.items()}
    row_ok = (
        candidate.ok
        and len(footprint) == 300
        and candidate.candidate_support == 300
        and footprint == compact_reference
    )
    return NormalizedYProductProfile(
        name=name,
        base=base,
        k_step=k_step,
        d_step=d_step,
        t_step=t_step,
        k_length=k_length,
        d_length=d_length,
        orientation="y(A+T)/y(A)" if reverse else "y(A)/y(A+T)",
        center_base=center_base,
        half_shift=half_shift,
        footprint_support=len(footprint),
        footprint_coefficient_counts=coefficient_counts(footprint),
        footprint_equals_compact_ksy=footprint == compact_reference,
        exact_theta2=candidate.exact_theta2,
        exact_theta2_inverse=candidate.exact_theta2_inverse,
        candidate_profile=candidate,
        ok=row_ok,
    )


def profile_normalized_y_product_source_law() -> NormalizedYProductSourceLawProfile:
    target_inverse = profile_normalized_y_product(
        "normalized_y_product_target_theta2_inverse",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    target_theta2 = profile_normalized_y_product(
        "normalized_y_product_target_theta2",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
        reverse=True,
    )
    missing_k = profile_normalized_y_product(
        "normalized_y_product_missing_k_control",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
        k_length=1,
    )
    collapsed_k = profile_normalized_y_product(
        "normalized_y_product_collapsed_k_control",
        BASE_POINT,
        (0, 0),
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    truncated_d = profile_normalized_y_product(
        "normalized_y_product_truncated_d_control",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
        d_length=2,
    )
    wrong_d = profile_normalized_y_product(
        "normalized_y_product_wrong_d_control",
        BASE_POINT,
        KERNEL_SHIFT,
        (D_SHIFT[0], (D_SHIFT[1] + 1) % C_ORDER),
        BRIDGE_SHIFT,
    )
    wrong_t = profile_normalized_y_product(
        "normalized_y_product_wrong_t_control",
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        add_coord(BRIDGE_SHIFT, D_SHIFT),
    )
    row_ok = (
        target_inverse.ok
        and target_inverse.exact_theta2_inverse
        and target_inverse.candidate_profile.recovered_sign == -1
        and target_theta2.ok
        and target_theta2.exact_theta2
        and target_theta2.candidate_profile.recovered_sign == 1
        and target_inverse.center_base == (44, 166)
        and target_inverse.half_shift == (56, 28)
        and target_inverse.footprint_support == 300
        and target_inverse.footprint_coefficient_counts == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and not missing_k.ok
        and not collapsed_k.ok
        and not truncated_d.ok
        and not wrong_d.ok
        and not wrong_t.ok
    )
    return NormalizedYProductSourceLawProfile(
        target_inverse_ok=target_inverse.ok,
        target_theta2_ok=target_theta2.ok,
        missing_k_rejected=not missing_k.ok,
        collapsed_k_rejected=not collapsed_k.ok,
        truncated_d_rejected=not truncated_d.ok,
        wrong_d_rejected=not wrong_d.ok,
        wrong_t_rejected=not wrong_t.ok,
        target_support=target_inverse.footprint_support,
        source_parameter_budget=31,
        theorem_source_law="prod_{A in base*K_trace*D_segment} y(A)/y(A+T)",
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY normalized-y product source-law gate")
    print(f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    profile = profile_normalized_y_product_source_law()
    print(f"normalized_y_product_source_law_profile={profile}")
    print("source_law")
    print("  y(Q) = -g(2Q)/g(Q)^4")
    print("  product_A_y_A_over_y_A_plus_T_on_base_Ktrace_Dsegment_emits_theta2_inverse=1")
    print("  reversed_product_emits_theta2=1")
    print("  compact_center_base_44_166_and_half_shift_56_28_are_recovered=1")
    print("controls")
    print("  missing_K_collapsed_K_truncated_D_wrong_D_and_wrong_T_are_rejected=1")
    print("interpretation")
    print("  this_is_the_finite_KSY_source_law_target_for_a_D2_theorem=1")
    print("  arithmetic_legality_of_the_normalized_y_product_remains_the_missing_proof=1")
    print(f"robert_ksy_theta2_normalized_y_product_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_normalized_y_product_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

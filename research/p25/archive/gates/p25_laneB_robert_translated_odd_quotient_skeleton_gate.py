#!/usr/bin/env python3
"""Translated odd quotient skeleton for the p25 Robert/Siegel lane.

The targeted literature search pointed away from x-only tables and toward
translated odd quotients such as

    Dtheta(P+T) / Dtheta(P-T)
    y(P+T) / y(P-T)

with the explicit edge `T=(2,113)` on `C_3 x C_169` (raw representative
`(38,113)`).  This gate checks the finite source-shape such a quotient must
have before any analytic elliptic-unit values are attempted.

The exact bridge is:

    base * K_trace * D_segment * (1 - T).

The checks here keep the Robert/Siegel route narrow:

* a translated point quotient with only the kernel trace is too small;
* the D-segment/K-trace translated odd quotient is exactly the bridge;
* the inverse edge has the wrong orientation;
* even/symmetrized edge quotients destroy the signed bridge support.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    edge_factor,
    geometric_factor,
    monomial,
    multiply_factors,
    source_mask_to_raw,
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
class TranslatedOddQuotientSkeletonProfile:
    target_edge: Coord
    quotient_edge: Coord
    point_kernel_profile: CandidateProfile
    d_kernel_edge_profile: CandidateProfile
    inverse_edge_profile: CandidateProfile
    even_pair_profile: CandidateProfile
    squared_edge_profile: CandidateProfile
    no_kernel_profile: CandidateProfile
    point_kernel_too_small: bool
    d_kernel_edge_is_exact_bridge: bool
    inverse_edge_wrong_orientation: bool
    even_pair_symmetrization_killed: bool
    squared_edge_symmetrization_killed: bool
    no_kernel_trace_killed: bool


def inverse_step(step: Coord) -> Coord:
    return ((-step[0]) % RIGHT_ORDER, (-step[1]) % C_ORDER)


def candidate_profile(name: str, factors: tuple[tuple[str, dict[Coord, int]], ...]) -> CandidateProfile:
    raw = source_mask_to_raw(multiply_factors(factors))
    return profile_candidate(name, raw, target_raw_bridge())


def skeleton_profile() -> TranslatedOddQuotientSkeletonProfile:
    base = ("base", monomial(BASE_POINT))
    kernel = ("kernel_trace", geometric_factor(KERNEL_SHIFT, 25))
    d_segment = ("D_segment", geometric_factor(D_SHIFT, 3))
    edge = ("edge_T", edge_factor(BRIDGE_SHIFT))
    inverse_edge = ("edge_-T", edge_factor(inverse_step(BRIDGE_SHIFT)))
    even_pair_edge = ("edge_T_edge_-T", multiply_factors((edge, inverse_edge)))
    squared_edge = ("edge_T_squared", multiply_factors((edge, edge)))

    point_kernel = candidate_profile(
        "translated_point_quotient_kernel_trace_only",
        (base, kernel, edge),
    )
    d_kernel_edge = candidate_profile(
        "translated_D_segment_kernel_trace_odd_quotient",
        (base, kernel, d_segment, edge),
    )
    inverse = candidate_profile(
        "translated_D_segment_kernel_trace_inverse_edge",
        (base, kernel, d_segment, inverse_edge),
    )
    even_pair = candidate_profile(
        "translated_D_segment_kernel_trace_even_pair_edge",
        (base, kernel, d_segment, even_pair_edge),
    )
    squared = candidate_profile(
        "translated_D_segment_kernel_trace_squared_edge",
        (base, kernel, d_segment, squared_edge),
    )
    no_kernel = candidate_profile(
        "translated_D_segment_odd_quotient_no_kernel_trace",
        (base, d_segment, edge),
    )

    quotient_edge = (BRIDGE_SHIFT[0] % 3, BRIDGE_SHIFT[1])
    return TranslatedOddQuotientSkeletonProfile(
        target_edge=BRIDGE_SHIFT,
        quotient_edge=quotient_edge,
        point_kernel_profile=point_kernel,
        d_kernel_edge_profile=d_kernel_edge,
        inverse_edge_profile=inverse,
        even_pair_profile=even_pair,
        squared_edge_profile=squared,
        no_kernel_profile=no_kernel,
        point_kernel_too_small=(
            point_kernel.raw_support == 50
            and point_kernel.quotient_support == 2
            and not point_kernel.ok
        ),
        d_kernel_edge_is_exact_bridge=d_kernel_edge.ok,
        inverse_edge_wrong_orientation=(
            inverse.raw_support == 150
            and inverse.quotient_support == 6
            and not inverse.trace_correct
            and not inverse.ok
        ),
        even_pair_symmetrization_killed=(
            even_pair.raw_support == 225
            and even_pair.quotient_support == 9
            and not even_pair.ok
        ),
        squared_edge_symmetrization_killed=(
            squared.raw_support == 225
            and squared.quotient_support == 9
            and not squared.ok
        ),
        no_kernel_trace_killed=(
            no_kernel.raw_support == 6
            and no_kernel.quotient_support == 6
            and no_kernel.kernel_modes == tuple(range(25))
            and no_kernel.raw_relation_mismatches == 12
            and not no_kernel.ok
        ),
    )


def main() -> int:
    print("p25 Lane B Robert/Siegel translated odd quotient skeleton gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile = skeleton_profile()
    row_ok = (
        profile.target_edge == (38, 113)
        and profile.quotient_edge == (2, 113)
        and profile.point_kernel_too_small
        and profile.d_kernel_edge_is_exact_bridge
        and profile.inverse_edge_wrong_orientation
        and profile.even_pair_symmetrization_killed
        and profile.squared_edge_symmetrization_killed
        and profile.no_kernel_trace_killed
    )

    print(f"translated_odd_quotient_skeleton_profile={profile}")
    print("candidate_profiles")
    for candidate in (
        profile.point_kernel_profile,
        profile.d_kernel_edge_profile,
        profile.inverse_edge_profile,
        profile.even_pair_profile,
        profile.squared_edge_profile,
        profile.no_kernel_profile,
    ):
        print(f"  {candidate}")
    print("translated_odd_quotient_laws")
    print("  point_quotient_kernel_trace_only_has_raw_support_50_and_is_too_small=1")
    print("  D_segment_kernel_trace_odd_quotient_is_exact_bridge=1")
    print("  inverse_edge_has_wrong_orientation=1")
    print("  even_or_squared_edge_symmetrization_expands_to_225_raw_cells=1")
    print("  no_kernel_trace_keeps_all_25_kernel_modes_and_fails_raw_relation=1")
    print("interpretation")
    print("  robert_siegel_candidate_must_emit_D_segment_K_trace_translated_odd_quotient=1")
    print("  kill_x_only_even_or_12N_power_symmetrized_edge_before_DK_support=1")
    print(f"robert_translated_odd_quotient_skeleton_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_translated_odd_quotient_skeleton_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

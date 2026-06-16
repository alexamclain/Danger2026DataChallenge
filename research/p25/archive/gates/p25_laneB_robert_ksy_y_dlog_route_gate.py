#!/usr/bin/env python3
"""KSY y / Kato-Siegel dlog route gate for the p25 Robert lane.

The latest scout narrows the live Robert/Siegel route to a primitive level-169
odd coordinate or logarithmic derivative, not a literal subgroup divisor or a
plain character tag.  This gate makes that route policy executable at the
finite-shadow layer.

Accepted finite shadow:

    base * K_trace * D_segment * (1 - T)

Controls record the nearby failures a theorem candidate must avoid:

* edge-only translated quotient is too small;
* missing K trace exposes all right-kernel modes and raw relation failures;
* inverse T has wrong orientation;
* even/x-like edge loses the signed bridge;
* D-boundary-only support is too small;
* split C13 shadow of T loses the primitive C169 edge;
* literal subgroup divisors cannot supply the D segment.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_kato_subgroup_support_falsifier_gate import (
    kato_subgroup_support_profile,
)
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_c169_nonsplit_gate import profile_nonsplit
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
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
from p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness import (
    sign_sparse_source_profile,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_triangle_candidate_harness import (
    triangle_candidate_profile,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class KsyYDlogRouteProfile:
    accepted_profile: CandidateProfile
    edge_only_profile: CandidateProfile
    missing_k_profile: CandidateProfile
    inverse_t_profile: CandidateProfile
    even_t_profile: CandidateProfile
    d_boundary_profile: CandidateProfile
    split_c13_t_profile: CandidateProfile
    literal_subgroup_divisor_killed: bool
    c169_edge_is_primitive: bool
    c169_source_nonsplit: bool
    canonical_sign_sparse_ok: bool
    canonical_triangle_ok: bool
    split_triangle_control_ok: bool
    row_ok: bool


def inverse_step(step: Coord) -> Coord:
    return ((-step[0]) % RIGHT_ORDER, (-step[1]) % C_ORDER)


def unsigned_edge_factor(step: Coord) -> Ring:
    return {(0, 0): 1, step: 1}


def route_profile(name: str, factors: tuple[tuple[str, Ring], ...]) -> CandidateProfile:
    return profile_candidate(
        name,
        source_mask_to_raw(multiply_factors(factors)),
        target_raw_bridge(),
    )


def profile_ksy_y_dlog_route() -> KsyYDlogRouteProfile:
    base = ("base", monomial(BASE_POINT))
    k_trace = ("K_trace", geometric_factor(KERNEL_SHIFT, 25))
    d_segment = ("D_segment", geometric_factor(D_SHIFT, 3))
    t_edge = ("odd_T_edge", edge_factor(BRIDGE_SHIFT))
    inverse_t = ("inverse_T_edge", edge_factor(inverse_step(BRIDGE_SHIFT)))
    even_t = ("even_T_edge", unsigned_edge_factor(BRIDGE_SHIFT))
    d_boundary = ("D_boundary", edge_factor(D_SHIFT))
    split_c13_t = ("split_C13_T_edge", edge_factor((BRIDGE_SHIFT[0], BRIDGE_SHIFT[1] % 13)))

    accepted = route_profile(
        "ksy_y_dlog_odd_translated_DK_route",
        (base, k_trace, d_segment, t_edge),
    )
    edge_only = route_profile(
        "ksy_y_dlog_edge_only_control",
        (base, k_trace, t_edge),
    )
    missing_k = route_profile(
        "ksy_y_dlog_missing_K_trace_control",
        (base, d_segment, t_edge),
    )
    inverse = route_profile(
        "ksy_y_dlog_inverse_T_control",
        (base, k_trace, d_segment, inverse_t),
    )
    even = route_profile(
        "ksy_y_dlog_even_x_like_T_control",
        (base, k_trace, d_segment, even_t),
    )
    d_boundary_only = route_profile(
        "ksy_y_dlog_D_boundary_only_control",
        (base, k_trace, d_boundary, t_edge),
    )
    split_t = route_profile(
        "ksy_y_dlog_split_C13_T_control",
        (base, k_trace, d_segment, split_c13_t),
    )

    subgroup_profile = kato_subgroup_support_profile()
    nonsplit_profile = profile_nonsplit()
    sign_profile = sign_sparse_source_profile("ksy_y_dlog_canonical_sign_probe", 1, -1)
    canonical_triangle = triangle_candidate_profile(
        "ksy_y_dlog_canonical_triangle_probe",
        ((0, 0), (3, 0), (1, 11)),
        (-1, -1, -1),
    )
    split_triangle = triangle_candidate_profile(
        "ksy_y_dlog_split_triangle_control",
        ((0, 0), (3, 0), (1, 0)),
        (-1, -1, -1),
    )

    literal_subgroup_killed = subgroup_profile.literal_subgroup_divisor_killed
    c169_edge_primitive = (
        nonsplit_profile.t_low == BRIDGE_SHIFT[1] % 13
        and nonsplit_profile.t_section_orders == (169,)
        and nonsplit_profile.t_c169_min_degree == 169
    )
    c169_source_nonsplit = (
        not nonsplit_profile.complement_exists
        and nonsplit_profile.order13_low_residues == (0,)
    )
    row_ok = (
        accepted.ok
        and accepted.raw_support == 150
        and accepted.target_raw_exact
        and accepted.source_mask_exact
        and edge_only.raw_support == 50
        and edge_only.quotient_support == 2
        and not edge_only.ok
        and missing_k.raw_support == 6
        and missing_k.kernel_modes == tuple(range(25))
        and missing_k.raw_relation_mismatches == 12
        and not missing_k.ok
        and inverse.raw_support == 150
        and inverse.quotient_support == 6
        and not inverse.trace_correct
        and not inverse.ok
        and even.raw_support == 150
        and even.quotient_scalar_nonzero == 1
        and not even.ok
        and d_boundary_only.raw_support == 100
        and d_boundary_only.quotient_support == 4
        and not d_boundary_only.ok
        and split_t.raw_support == 150
        and not split_t.trace_correct
        and not split_t.ok
        and literal_subgroup_killed
        and c169_edge_primitive
        and c169_source_nonsplit
        and sign_profile.ok
        and canonical_triangle.ok
        and not split_triangle.ok
    )
    return KsyYDlogRouteProfile(
        accepted_profile=accepted,
        edge_only_profile=edge_only,
        missing_k_profile=missing_k,
        inverse_t_profile=inverse,
        even_t_profile=even,
        d_boundary_profile=d_boundary_only,
        split_c13_t_profile=split_t,
        literal_subgroup_divisor_killed=literal_subgroup_killed,
        c169_edge_is_primitive=c169_edge_primitive,
        c169_source_nonsplit=c169_source_nonsplit,
        canonical_sign_sparse_ok=sign_profile.ok,
        canonical_triangle_ok=canonical_triangle.ok,
        split_triangle_control_ok=split_triangle.ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY-y / Kato-Siegel dlog route gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile = profile_ksy_y_dlog_route()
    print(f"ksy_y_dlog_route_profile={profile}")
    print("route_candidate_profiles")
    for candidate in (
        profile.accepted_profile,
        profile.edge_only_profile,
        profile.missing_k_profile,
        profile.inverse_t_profile,
        profile.even_t_profile,
        profile.d_boundary_profile,
        profile.split_c13_t_profile,
    ):
        print(f"  {candidate}")
    print("route_laws")
    print("  normalized_odd_y_or_dlog_route_targets_base_K_Dsegment_1_minus_T=1")
    print("  edge_only_translated_quotient_is_too_small=1")
    print("  missing_K_trace_exposes_all_25_kernel_modes=1")
    print("  inverse_T_has_wrong_orientation=1")
    print("  even_x_like_T_loses_the_signed_bridge=1")
    print("  D_boundary_only_has_support_100_not_150=1")
    print("  split_C13_shadow_of_T_fails_the_primitive_C169_bridge=1")
    print("  literal_subgroup_divisor_is_killed=1")
    print("  canonical_triangle_probe_passes_and_split_triangle_control_fails=1")
    print("interpretation")
    print("  continue_only_KSY_normalized_y_or_Kato_Siegel_dlog_translated_DK_route=1")
    print("  kill_pure_x_plain_character_literal_subgroup_or_split_C13_models=1")
    print(f"robert_ksy_y_dlog_route_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_y_dlog_route_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

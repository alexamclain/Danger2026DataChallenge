#!/usr/bin/env python3
"""Half-edge and normalized-y footprint gate for the p25 KSY route.

The route gate accepts the finite bridge edge `T`.  But an analytic odd
quotient has the symmetric form

    y(P + h) / y(P - h),

so the source shift `h` is a half-edge: the finite separation is `2h`.
This gate records the correct convention and prevents using the bridge edge as
the half-shift.  It also expands the normalized Koo-Shin-Yoon coordinate

    y(Q) = -g(2Q) / g(Q)^4

at the source-exponent footprint level.  The 300-term Siegel-footprint is an
upstream unit divisor footprint, not the 150-term bridge payload itself.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    geometric_factor,
    monomial,
    multiply_factors,
    ring_degree,
    scale_coord,
    source_mask_to_raw,
    translate_ring,
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
class NormalizedYFootprint:
    support: int
    degree: int
    coefficient_counts: tuple[tuple[int, int], ...]
    max_abs_coefficient: int
    profile: CandidateProfile


@dataclass(frozen=True)
class KsyYHalfEdgeProfile:
    bridge_edge: Coord
    half_edge: Coord
    negative_half_edge: Coord
    accepted_center_base: Coord
    half_edge_doubles_to_bridge_edge: bool
    negative_half_separation_is_bridge_edge: bool
    accepted_symmetric_profile: CandidateProfile
    wrong_half_orientation_profile: CandidateProfile
    full_edge_as_half_profile: CandidateProfile
    accepted_normalized_y_footprint: NormalizedYFootprint
    pure_g_edge_profile: CandidateProfile
    row_ok: bool


def inverse_step(step: Coord) -> Coord:
    return ((-step[0]) % RIGHT_ORDER, (-step[1]) % C_ORDER)


def half_step(step: Coord) -> Coord:
    return (
        (step[0] * pow(2, -1, RIGHT_ORDER)) % RIGHT_ORDER,
        (step[1] * pow(2, -1, C_ORDER)) % C_ORDER,
    )


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def route_centers(center_base: Coord) -> Ring:
    return multiply_factors(
        (
            ("center_base", monomial(center_base)),
            ("K_trace", geometric_factor(KERNEL_SHIFT, 25)),
            ("D_segment", geometric_factor(D_SHIFT, 3)),
        )
    )


def symmetric_edge_ring(center_base: Coord, half_shift: Coord) -> Ring:
    centers = route_centers(center_base)
    positive = translate_ring(centers, half_shift)
    negative = translate_ring(centers, inverse_step(half_shift), coefficient=-1)
    out: Ring = {}
    for ring in (positive, negative):
        for coord, coefficient in ring.items():
            add_ring_entry(out, coord, coefficient)
    return dict(sorted(out.items()))


def y_exponent_at(out: Ring, point: Coord, coefficient: int) -> None:
    add_ring_entry(out, scale_coord(point, 2), coefficient)
    add_ring_entry(out, point, -4 * coefficient)


def normalized_y_exponent_footprint(center_base: Coord, half_shift: Coord) -> Ring:
    centers = route_centers(center_base)
    out: Ring = {}
    for point, coefficient in centers.items():
        y_exponent_at(out, add_coord(point, half_shift), coefficient)
        y_exponent_at(out, add_coord(point, inverse_step(half_shift)), -coefficient)
    return dict(sorted(out.items()))


def bridge_profile(name: str, ring: Ring) -> CandidateProfile:
    return profile_candidate(name, source_mask_to_raw(ring), target_raw_bridge())


def footprint_profile(name: str, ring: Ring) -> NormalizedYFootprint:
    return NormalizedYFootprint(
        support=len(ring),
        degree=ring_degree(ring),
        coefficient_counts=tuple(sorted(Counter(ring.values()).items())),
        max_abs_coefficient=max(abs(value) for value in ring.values()),
        profile=bridge_profile(name, ring),
    )


def profile_half_edge_footprint() -> KsyYHalfEdgeProfile:
    half_edge = half_step(BRIDGE_SHIFT)
    negative_half = inverse_step(half_edge)
    accepted_center_base = add_coord(BASE_POINT, half_edge)

    accepted_ring = symmetric_edge_ring(accepted_center_base, negative_half)
    wrong_half_ring = symmetric_edge_ring(add_coord(BASE_POINT, negative_half), half_edge)
    full_edge_as_half_ring = symmetric_edge_ring(
        add_coord(BASE_POINT, inverse_step(BRIDGE_SHIFT)),
        BRIDGE_SHIFT,
    )
    normalized_y_ring = normalized_y_exponent_footprint(accepted_center_base, negative_half)

    accepted_profile = bridge_profile("ksy_symmetric_half_edge_accepted", accepted_ring)
    wrong_profile = bridge_profile("ksy_symmetric_wrong_half_orientation_control", wrong_half_ring)
    full_edge_profile = bridge_profile("ksy_full_bridge_edge_used_as_half_shift_control", full_edge_as_half_ring)
    y_footprint = footprint_profile("ksy_normalized_y_siegel_exponent_footprint", normalized_y_ring)
    pure_g_profile = bridge_profile("ksy_pure_g_half_edge_footprint_control", accepted_ring)

    row_ok = (
        BRIDGE_SHIFT == (38, 113)
        and half_edge == (19, 141)
        and negative_half == (56, 28)
        and accepted_center_base == (44, 166)
        and scale_coord(half_edge, 2) == BRIDGE_SHIFT
        and scale_coord(negative_half, -2) == BRIDGE_SHIFT
        and accepted_profile.ok
        and accepted_profile.raw_support == 150
        and wrong_profile.raw_support == 150
        and not wrong_profile.trace_correct
        and not wrong_profile.ok
        and full_edge_profile.raw_support == 150
        and not full_edge_profile.trace_correct
        and not full_edge_profile.ok
        and y_footprint.support == 300
        and y_footprint.degree == 0
        and y_footprint.coefficient_counts == ((-4, 75), (-1, 75), (1, 75), (4, 75))
        and y_footprint.max_abs_coefficient == 4
        and y_footprint.profile.raw_support == 300
        and y_footprint.profile.quotient_support == 12
        and not y_footprint.profile.ok
        and pure_g_profile.ok
    )
    return KsyYHalfEdgeProfile(
        bridge_edge=BRIDGE_SHIFT,
        half_edge=half_edge,
        negative_half_edge=negative_half,
        accepted_center_base=accepted_center_base,
        half_edge_doubles_to_bridge_edge=scale_coord(half_edge, 2) == BRIDGE_SHIFT,
        negative_half_separation_is_bridge_edge=scale_coord(negative_half, -2) == BRIDGE_SHIFT,
        accepted_symmetric_profile=accepted_profile,
        wrong_half_orientation_profile=wrong_profile,
        full_edge_as_half_profile=full_edge_profile,
        accepted_normalized_y_footprint=y_footprint,
        pure_g_edge_profile=pure_g_profile,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY-y half-edge footprint gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile = profile_half_edge_footprint()
    print(f"ksy_y_half_edge_profile={profile}")
    print("half_edge_laws")
    print("  bridge_edge_T=(38,113)")
    print("  half_edge_H=(19,141), with 2H=T")
    print("  accepted symmetric quotient uses h=-H and center_base=base+H")
    print("  using H gives inverse orientation; using T as h gives edge 2T")
    print("normalized_y_footprint_laws")
    print("  y(Q)=-g(2Q)/g(Q)^4 expands to coefficients +1,-4 at 2Q,Q")
    print("  y(P+h)/y(P-h) over the accepted centers has 300 Siegel-exponent cells")
    print("  coefficient counts are -4,-1,+1,+4 each on 75 cells")
    print("  this footprint is an upstream unit divisor, not the 150-cell bridge payload")
    print("interpretation")
    print("  KSY_y_or_dlog_candidate_must_use_half_edge_not_bridge_edge_as_half_shift=1")
    print("  do_not_feed_normalized_y_siegel_exponent_footprint_as_sparse_bridge_payload=1")
    print(f"robert_ksy_y_half_edge_footprint_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_y_half_edge_footprint_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

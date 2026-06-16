#!/usr/bin/env python3
"""Compact KSY theta2 parameter intake for p25.

The sparse theta2 harness accepts a 300-term source table.  A theorem or hand
derivation may naturally identify the much smaller KSY recipe instead:

    center_base, half_shift, and optional inversion.

This harness expands that recipe through the existing normalized-y footprint,
then reuses the theta2 sparse candidate harness.  The final bridge contract is
unchanged; this file only lowers the input burden for KSY/theta theorem hits.
"""

from __future__ import annotations

import argparse
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
    profile_half_edge_footprint,
)
from p25_laneB_robert_ksy_y_projection_gate import scale_ring
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import Ring, add_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    RIGHT_ORDER,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class KsyTheta2CompactProfile:
    name: str
    center_base: Coord
    half_shift: Coord
    invert: bool
    footprint_support: int
    footprint_coefficient_counts: tuple[tuple[int, int], ...]
    half_shift_doubles_to_bridge_edge: bool
    separation_is_bridge_edge: bool
    candidate_profile: KsyTheta2CandidateProfile
    ok: bool


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def compact_footprint(center_base: Coord, half_shift: Coord, invert: bool) -> Ring:
    footprint = normalized_y_exponent_footprint(center_base, half_shift)
    return scale_ring(footprint, -1) if invert else footprint


def profile_compact_theta2(
    name: str,
    center_base: Coord,
    half_shift: Coord,
    invert: bool,
) -> KsyTheta2CompactProfile:
    footprint = compact_footprint(center_base, half_shift, invert)
    candidate = profile_theta2_candidate(name, theta2_sparse_entries(footprint))
    separation = (
        ((-2 * half_shift[0]) % RIGHT_ORDER, (-2 * half_shift[1]) % C_ORDER)
    )
    row_ok = (
        candidate.ok
        and footprint
        and len(footprint) == 300
        and candidate.candidate_support == 300
        and candidate.shifted_theta2_term_budget == 46800
        and candidate.shifted_theta2_union_support == 11700
    )
    return KsyTheta2CompactProfile(
        name=name,
        center_base=center_base,
        half_shift=half_shift,
        invert=invert,
        footprint_support=len(footprint),
        footprint_coefficient_counts=coefficient_counts(footprint),
        half_shift_doubles_to_bridge_edge=(
            ((2 * half_shift[0]) % RIGHT_ORDER, (2 * half_shift[1]) % C_ORDER)
            == BRIDGE_SHIFT
        ),
        separation_is_bridge_edge=separation == BRIDGE_SHIFT,
        candidate_profile=candidate,
        ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit compact KSY theta2 parameters: center_base, half_shift, "
            "and optional inversion."
        )
    )
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--half-right", type=int)
    parser.add_argument("--half-c", type=int)
    parser.add_argument("--invert", action="store_true")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/theta2 compact parameter harness")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"base={BASE_POINT} bridge_edge={BRIDGE_SHIFT}"
    )

    supplied = (
        args.center_right is not None,
        args.center_c is not None,
        args.half_right is not None,
        args.half_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("--center-right --center-c --half-right --half-c must be supplied together")
        profile = profile_compact_theta2(
            "compact_theta2_candidate",
            (args.center_right % RIGHT_ORDER, args.center_c % C_ORDER),
            (args.half_right % RIGHT_ORDER, args.half_c % C_ORDER),
            args.invert,
        )
        print("mode=compact_theta2_candidate")
        print(f"compact_theta2_profile={profile}")
        print("candidate_contract")
        print("  pass requires compact footprint to expand to exact theta2 or theta2_inverse")
        print("  pass then reuses the sparse theta2 resolvent and bridge contract")
        print(f"robert_ksy_theta2_compact_harness_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_compact_harness_candidate")
        return 0 if profile.ok else 1

    half_profile = profile_half_edge_footprint()
    accepted_inverse = profile_compact_theta2(
        "compact_accepted_theta2_inverse",
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
        False,
    )
    accepted_theta2 = profile_compact_theta2(
        "compact_accepted_theta2",
        half_profile.accepted_center_base,
        half_profile.negative_half_edge,
        True,
    )
    wrong_orientation = profile_compact_theta2(
        "compact_wrong_half_orientation_control",
        add_coord(BASE_POINT, half_profile.negative_half_edge),
        half_profile.half_edge,
        False,
    )
    full_edge_as_half = profile_compact_theta2(
        "compact_full_edge_as_half_control",
        add_coord(BASE_POINT, inverse_step(BRIDGE_SHIFT)),
        BRIDGE_SHIFT,
        False,
    )
    bridge_half_no_center_shift = profile_compact_theta2(
        "compact_half_edge_without_center_shift_control",
        BASE_POINT,
        half_step(BRIDGE_SHIFT),
        False,
    )

    row_ok = (
        accepted_inverse.ok
        and accepted_theta2.ok
        and accepted_inverse.candidate_profile.exact_theta2_inverse
        and accepted_inverse.candidate_profile.recovered_sign == -1
        and accepted_theta2.candidate_profile.exact_theta2
        and accepted_theta2.candidate_profile.recovered_sign == 1
        and accepted_inverse.separation_is_bridge_edge
        and not accepted_inverse.half_shift_doubles_to_bridge_edge
        and not wrong_orientation.ok
        and not full_edge_as_half.ok
        and not bridge_half_no_center_shift.ok
    )

    print(f"accepted_inverse_profile={accepted_inverse}")
    print(f"accepted_theta2_profile={accepted_theta2}")
    print(f"wrong_orientation_control={wrong_orientation}")
    print(f"full_edge_as_half_control={full_edge_as_half}")
    print(f"half_edge_without_center_shift_control={bridge_half_no_center_shift}")
    print("compact_intake_laws")
    print("  accepted compact recipe uses center_base=base+H and half_shift=-H=56,28=1")
    print("  compact recipe may emit theta2_inverse directly or theta2 by inversion=1")
    print("  sparse theta2 resolvent and bridge contract are reused unchanged=1")
    print("  wrong_half_orientation_full_edge_as_half_and_missing_center_shift_controls_fail=1")
    print(f"robert_ksy_theta2_compact_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_compact_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

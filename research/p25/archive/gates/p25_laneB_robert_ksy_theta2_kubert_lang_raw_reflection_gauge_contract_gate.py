#!/usr/bin/env python3
"""Raw reflection-gauge contract for p25 KL/KSY theorem candidates.

The quotient reflection-center contract accepts C=(2,28), D=(1,3), and a
primitive K.  A theorem source may instead emit raw C_75 x C_169
representatives.  This gate records the exact raw freedom:

    raw C = (47,28) + aK
    raw D = +/-(22,3) + bK
    K     = primitive multiplier of (57,0)

for a,b mod 25.  These kernel-gauge and D-reversal choices give the same full
K-traced center set and anti-invariant theta2 payload.  Non-kernel center/D
shifts and nonprimitive K do not.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    anti_invariant_y_footprint,
    centered_source_trace,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate import (
    profile_reflection_center_contract,
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
RAW_CENTER = add_coord(BASE_POINT, D_SHIFT)


@dataclass(frozen=True)
class RawReflectionGaugeCandidateProfile:
    name: str
    raw_center: Coord
    raw_d: Coord
    k_multiplier: int
    raw_k_step: Coord
    k_multiplier_primitive: bool
    center_kernel_gauge_index: int | None
    d_forward_kernel_gauge_index: int | None
    d_reverse_kernel_gauge_index: int | None
    d_orientation: int
    quotient_center: Coord
    quotient_d: Coord
    source_trace_support: int
    source_trace_matches_target: bool
    theta2_footprint_support: int
    theta2_footprint_matches_target: bool
    fixed_t_kernel_offset: int | None
    ok: bool


@dataclass(frozen=True)
class RawReflectionGaugeContractProfile:
    target_profile: RawReflectionGaugeCandidateProfile
    primitive_k_profile: RawReflectionGaugeCandidateProfile
    nonprimitive_k_profile: RawReflectionGaugeCandidateProfile
    collapsed_k_profile: RawReflectionGaugeCandidateProfile
    d_reversal_profile: RawReflectionGaugeCandidateProfile
    wrong_center_controls: tuple[RawReflectionGaugeCandidateProfile, ...]
    wrong_d_controls: tuple[RawReflectionGaugeCandidateProfile, ...]
    center_kernel_gauge_hits: int
    d_forward_kernel_gauge_hits: int
    d_reverse_kernel_gauge_hits: int
    oriented_d_kernel_gauge_hits: int
    combined_center_d_oriented_kernel_gauge_hits: int
    primitive_k_multiplier_hits: int
    combined_raw_gauge_parameter_count: int
    quotient_reflection_center_contract_ok: bool
    all_combined_gauges_match_source_trace: bool
    all_combined_gauges_match_theta2_footprint: bool
    nonkernel_controls_rejected: bool
    candidate_contract: str
    row_ok: bool


def normalize(coord: Coord) -> Coord:
    return (coord[0] % RIGHT_ORDER, coord[1] % C_ORDER)


def quotient_coord(coord: Coord) -> Coord:
    return (coord[0] % 3, coord[1] % C_ORDER)


def sub_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] - right[0]) % RIGHT_ORDER, (left[1] - right[1]) % C_ORDER)


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % RIGHT_ORDER, (-coord[1]) % C_ORDER)


def kernel_gauge_index(delta: Coord) -> int | None:
    for index in range(25):
        if scale_coord(KERNEL_SHIFT, index) == delta:
            return index
    return None


def d_orientation_and_gauge(d_step: Coord) -> tuple[int, int | None, int | None]:
    forward_gauge = kernel_gauge_index(sub_coord(d_step, D_SHIFT))
    reverse_gauge = kernel_gauge_index(sub_coord(d_step, scale_coord(D_SHIFT, -1)))
    if forward_gauge is not None:
        return 1, forward_gauge, reverse_gauge
    if reverse_gauge is not None:
        return -1, forward_gauge, reverse_gauge
    return 0, forward_gauge, reverse_gauge


def primitive_k_step(k_multiplier: int) -> Coord:
    return scale_coord(KERNEL_SHIFT, k_multiplier % 25)


def target_source_trace() -> dict[Coord, int]:
    return centered_source_trace(RAW_CENTER, KERNEL_SHIFT, D_SHIFT)


def target_theta2_footprint() -> dict[Coord, int]:
    _centers, footprint = anti_invariant_y_footprint(RAW_CENTER, KERNEL_SHIFT, D_SHIFT)
    return footprint


def fixed_t_kernel_offset(raw_center: Coord) -> int | None:
    negative_double_center = inverse_coord(scale_coord(raw_center, 2))
    return kernel_gauge_index(sub_coord((38, 113), negative_double_center))


def profile_raw_reflection_gauge_candidate(
    name: str,
    raw_center: Coord,
    raw_d: Coord,
    k_multiplier: int,
) -> RawReflectionGaugeCandidateProfile:
    center = normalize(raw_center)
    d_step = normalize(raw_d)
    k_step = primitive_k_step(k_multiplier)
    primitive = gcd(k_multiplier % 25, 25) == 1
    centers = centered_source_trace(center, k_step, d_step)
    _footprint_centers, footprint = anti_invariant_y_footprint(center, k_step, d_step)
    source_matches = centers == target_source_trace()
    footprint_matches = footprint == target_theta2_footprint()
    center_gauge = kernel_gauge_index(sub_coord(center, RAW_CENTER))
    d_orientation, d_forward_gauge, d_reverse_gauge = d_orientation_and_gauge(d_step)
    row_ok = (
        primitive
        and center_gauge is not None
        and d_orientation in (-1, 1)
        and quotient_coord(center) == (2, 28)
        and quotient_coord(d_step) in ((1, 3), (2, 166))
        and len(centers) == 75
        and len(footprint) == 300
        and source_matches
        and footprint_matches
        and fixed_t_kernel_offset(center) is not None
    )
    return RawReflectionGaugeCandidateProfile(
        name=name,
        raw_center=center,
        raw_d=d_step,
        k_multiplier=k_multiplier % 25,
        raw_k_step=k_step,
        k_multiplier_primitive=primitive,
        center_kernel_gauge_index=center_gauge,
        d_forward_kernel_gauge_index=d_forward_gauge,
        d_reverse_kernel_gauge_index=d_reverse_gauge,
        d_orientation=d_orientation,
        quotient_center=quotient_coord(center),
        quotient_d=quotient_coord(d_step),
        source_trace_support=len(centers),
        source_trace_matches_target=source_matches,
        theta2_footprint_support=len(footprint),
        theta2_footprint_matches_target=footprint_matches,
        fixed_t_kernel_offset=fixed_t_kernel_offset(center),
        ok=row_ok,
    )


def shifted(step: Coord, gauge_index: int) -> Coord:
    return add_coord(step, scale_coord(KERNEL_SHIFT, gauge_index))


def profile_raw_reflection_gauge_contract() -> RawReflectionGaugeContractProfile:
    target = profile_raw_reflection_gauge_candidate("target_raw_reflection_gauge", RAW_CENTER, D_SHIFT, 1)
    primitive_k = profile_raw_reflection_gauge_candidate(
        "primitive_k_raw_reflection_gauge",
        RAW_CENTER,
        D_SHIFT,
        2,
    )
    nonprimitive_k = profile_raw_reflection_gauge_candidate(
        "nonprimitive_k_raw_reflection_gauge",
        RAW_CENTER,
        D_SHIFT,
        5,
    )
    collapsed_k = profile_raw_reflection_gauge_candidate(
        "collapsed_k_raw_reflection_gauge",
        RAW_CENTER,
        D_SHIFT,
        0,
    )
    wrong_centers = (
        profile_raw_reflection_gauge_candidate("center_plus_D_control", add_coord(RAW_CENTER, D_SHIFT), D_SHIFT, 1),
        profile_raw_reflection_gauge_candidate("center_plus_C_axis_control", add_coord(RAW_CENTER, (0, 1)), D_SHIFT, 1),
        profile_raw_reflection_gauge_candidate("center_plus_right_axis_control", add_coord(RAW_CENTER, (1, 0)), D_SHIFT, 1),
    )
    d_reversal = profile_raw_reflection_gauge_candidate(
        "D_reversal_orientation_control",
        RAW_CENTER,
        scale_coord(D_SHIFT, -1),
        1,
    )
    wrong_ds = (
        profile_raw_reflection_gauge_candidate("D_plus_C_axis_control", RAW_CENTER, add_coord(D_SHIFT, (0, 1)), 1),
        profile_raw_reflection_gauge_candidate("D_plus_right_axis_control", RAW_CENTER, add_coord(D_SHIFT, (1, 0)), 1),
    )

    target_trace = target_source_trace()
    target_footprint = target_theta2_footprint()
    center_hits = 0
    d_forward_hits = 0
    d_reverse_hits = 0
    combined_trace_hits = 0
    combined_footprint_hits = 0
    for center_gauge in range(25):
        center = shifted(RAW_CENTER, center_gauge)
        center_hits += int(centered_source_trace(center, KERNEL_SHIFT, D_SHIFT) == target_trace)
    for d_gauge in range(25):
        d_step = shifted(D_SHIFT, d_gauge)
        d_forward_hits += int(centered_source_trace(RAW_CENTER, KERNEL_SHIFT, d_step) == target_trace)
        d_reverse = shifted(scale_coord(D_SHIFT, -1), d_gauge)
        d_reverse_hits += int(centered_source_trace(RAW_CENTER, KERNEL_SHIFT, d_reverse) == target_trace)
    for center_gauge in range(25):
        center = shifted(RAW_CENTER, center_gauge)
        for d_orientation in (1, -1):
            d_base = D_SHIFT if d_orientation == 1 else scale_coord(D_SHIFT, -1)
            for d_gauge in range(25):
                d_step = shifted(d_base, d_gauge)
                centers, footprint = anti_invariant_y_footprint(center, KERNEL_SHIFT, d_step)
                combined_trace_hits += int(centers == target_trace)
                combined_footprint_hits += int(footprint == target_footprint)

    primitive_k_hits = sum(
        int(profile_raw_reflection_gauge_candidate(f"k_multiplier_{multiplier}", RAW_CENTER, D_SHIFT, multiplier).ok)
        for multiplier in range(25)
    )
    quotient_contract = profile_reflection_center_contract()
    nonkernel_rejected = (
        not nonprimitive_k.ok
        and not collapsed_k.ok
        and all(not control.ok for control in wrong_centers)
        and all(not control.ok for control in wrong_ds)
    )
    row_ok = (
        RIGHT_ORDER == 75
        and C_ORDER == 169
        and RAW_CENTER == (47, 28)
        and D_SHIFT == (22, 3)
        and KERNEL_SHIFT == (57, 0)
        and target.ok
        and primitive_k.ok
        and d_reversal.ok
        and d_reversal.d_orientation == -1
        and center_hits == 25
        and d_forward_hits == 25
        and d_reverse_hits == 25
        and combined_trace_hits == 1250
        and combined_footprint_hits == 1250
        and primitive_k_hits == 20
        and quotient_contract.row_ok
        and nonkernel_rejected
    )
    return RawReflectionGaugeContractProfile(
        target_profile=target,
        primitive_k_profile=primitive_k,
        nonprimitive_k_profile=nonprimitive_k,
        collapsed_k_profile=collapsed_k,
        d_reversal_profile=d_reversal,
        wrong_center_controls=wrong_centers,
        wrong_d_controls=wrong_ds,
        center_kernel_gauge_hits=center_hits,
        d_forward_kernel_gauge_hits=d_forward_hits,
        d_reverse_kernel_gauge_hits=d_reverse_hits,
        oriented_d_kernel_gauge_hits=d_forward_hits + d_reverse_hits,
        combined_center_d_oriented_kernel_gauge_hits=combined_trace_hits,
        primitive_k_multiplier_hits=primitive_k_hits,
        combined_raw_gauge_parameter_count=combined_trace_hits * primitive_k_hits,
        quotient_reflection_center_contract_ok=quotient_contract.row_ok,
        all_combined_gauges_match_source_trace=combined_trace_hits == 1250,
        all_combined_gauges_match_theta2_footprint=combined_footprint_hits == 1250,
        nonkernel_controls_rejected=nonkernel_rejected,
        candidate_contract=(
            "emit raw C=(47,28)+aK, raw D=+/-(22,3)+bK, and primitive K; "
            "kernel-gauge and D-reversal representatives are equivalent, "
            "non-kernel shifts fail"
        ),
        row_ok=row_ok,
    )


def print_candidate(prefix: str, profile: RawReflectionGaugeCandidateProfile) -> None:
    print(
        "  "
        f"{prefix}: C={profile.raw_center} D={profile.raw_d} "
        f"Kmult={profile.k_multiplier} primitive={int(profile.k_multiplier_primitive)} "
        f"Cgauge={profile.center_kernel_gauge_index} "
        f"Dorient={profile.d_orientation} "
        f"Dfgauge={profile.d_forward_kernel_gauge_index} "
        f"Drgauge={profile.d_reverse_kernel_gauge_index} "
        f"qC={profile.quotient_center} qD={profile.quotient_d} "
        f"trace_ok={int(profile.source_trace_matches_target)} "
        f"theta2_ok={int(profile.theta2_footprint_matches_target)} "
        f"T_kernel_offset={profile.fixed_t_kernel_offset} ok={int(profile.ok)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit raw C_75 x C_169 reflection-gauge data for the p25 KL/KSY "
            "anti-invariant product."
        )
    )
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang raw reflection-gauge contract gate")
    print(f"raw_group=C_{RIGHT_ORDER}xC_{C_ORDER}")
    supplied = (
        args.center_right is not None,
        args.center_c is not None,
        args.d_right is not None,
        args.d_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all four raw center/D coordinates must be supplied together")
        candidate = profile_raw_reflection_gauge_candidate(
            "raw_reflection_gauge_candidate",
            (args.center_right, args.center_c),
            (args.d_right, args.d_c),
            args.k_multiplier,
        )
        print("mode=raw_reflection_gauge_candidate")
        print_candidate("candidate_profile", candidate)
        print("candidate_contract")
        print("  pass requires C=(47,28)+aK, D=+/-(22,3)+bK, primitive K")
        print("  pass requires same K-traced center set and theta2 footprint")
        print(
            "robert_ksy_theta2_kubert_lang_raw_reflection_gauge_candidate_rows="
            f"{int(candidate.ok)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_candidate")
        return 0 if candidate.ok else 1

    profile = profile_raw_reflection_gauge_contract()
    print("raw_reflection_gauge_contract_summary")
    print(f"  center_kernel_gauge_hits={profile.center_kernel_gauge_hits}")
    print(f"  d_forward_kernel_gauge_hits={profile.d_forward_kernel_gauge_hits}")
    print(f"  d_reverse_kernel_gauge_hits={profile.d_reverse_kernel_gauge_hits}")
    print(f"  oriented_d_kernel_gauge_hits={profile.oriented_d_kernel_gauge_hits}")
    print(f"  combined_center_d_oriented_kernel_gauge_hits={profile.combined_center_d_oriented_kernel_gauge_hits}")
    print(f"  primitive_k_multiplier_hits={profile.primitive_k_multiplier_hits}")
    print(f"  combined_raw_gauge_parameter_count={profile.combined_raw_gauge_parameter_count}")
    print(f"  quotient_reflection_center_contract_ok={int(profile.quotient_reflection_center_contract_ok)}")
    print(f"  nonkernel_controls_rejected={int(profile.nonkernel_controls_rejected)}")
    print_candidate("target_profile", profile.target_profile)
    print_candidate("primitive_k_profile", profile.primitive_k_profile)
    print_candidate("nonprimitive_k_profile", profile.nonprimitive_k_profile)
    print_candidate("collapsed_k_profile", profile.collapsed_k_profile)
    print_candidate("d_reversal_profile", profile.d_reversal_profile)
    print("wrong_center_controls")
    for control in profile.wrong_center_controls:
        print_candidate("control", control)
    print("wrong_d_controls")
    for control in profile.wrong_d_controls:
        print_candidate("control", control)
    print("interpretation")
    print("  raw_center_kernel_shifts_and_D_kernel_or_reversal_shifts_are_gauge=1")
    print("  primitive_K_multipliers_preserve_the_trace=1")
    print("  nonkernel_center_D_shifts_and_nonprimitive_K_fail=1")
    print(
        "robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

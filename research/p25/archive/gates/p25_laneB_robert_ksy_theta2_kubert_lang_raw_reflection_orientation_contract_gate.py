#!/usr/bin/env python3
"""Raw reflection orientation contract for p25 KL/KSY theorem candidates.

The raw reflection-gauge contract records representative freedom for the
forward anti-invariant product, which emits theta2 inverse.  Formula sources
may also emit the reversed quotient or use the inverse center.  This gate
classifies the four equivalent orientation branches:

    C,  y(A)/y(-A)       -> theta2 inverse
    C,  y(-A)/y(A)       -> theta2
    -C, y(A)/y(-A)       -> theta2
    -C, y(-A)/y(A)       -> theta2 inverse

with the same kernel-gauge, D-reversal, and primitive-K freedoms.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    anti_invariant_y_footprint,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_gate import (
    d_orientation_and_gauge,
    kernel_gauge_index,
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
RAW_INVERSE_CENTER = ((-RAW_CENTER[0]) % RIGHT_ORDER, (-RAW_CENTER[1]) % C_ORDER)


@dataclass(frozen=True)
class RawOrientationCandidateProfile:
    name: str
    raw_center: Coord
    raw_d: Coord
    k_multiplier: int
    product_orientation: str
    center_sign: int
    center_kernel_gauge_index: int | None
    d_orientation: int
    k_multiplier_primitive: bool
    footprint_support: int
    emits_theta2_inverse: bool
    emits_theta2: bool
    emits_accepted_theta_payload: bool
    ok: bool


@dataclass(frozen=True)
class RawOrientationBranchProfile:
    branch_name: str
    raw_center: Coord
    product_orientation: str
    emits: str
    center_kernel_gauge_hits: int
    oriented_d_gauge_hits: int
    primitive_k_hits: int
    branch_parameter_presentations: int
    ok: bool


@dataclass(frozen=True)
class RawReflectionOrientationContractProfile:
    branch_profiles: tuple[RawOrientationBranchProfile, ...]
    theta2_inverse_branches: int
    theta2_branches: int
    branch_parameter_presentations: int
    theta2_inverse_raw_presentations: int
    theta2_raw_presentations: int
    total_accepted_raw_presentations: int
    wrong_center_profile: RawOrientationCandidateProfile
    wrong_d_profile: RawOrientationCandidateProfile
    nonprimitive_k_profile: RawOrientationCandidateProfile
    raw_reflection_orientation_contract: str
    row_ok: bool


def normalize(coord: Coord) -> Coord:
    return (coord[0] % RIGHT_ORDER, coord[1] % C_ORDER)


def sub_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] - right[0]) % RIGHT_ORDER, (left[1] - right[1]) % C_ORDER)


def primitive_k_step(k_multiplier: int) -> Coord:
    return scale_coord(KERNEL_SHIFT, k_multiplier % 25)


def target_footprints() -> tuple[dict[Coord, int], dict[Coord, int]]:
    _centers, theta2_inverse = anti_invariant_y_footprint(
        RAW_CENTER,
        KERNEL_SHIFT,
        D_SHIFT,
        reverse=False,
    )
    _centers, theta2 = anti_invariant_y_footprint(
        RAW_CENTER,
        KERNEL_SHIFT,
        D_SHIFT,
        reverse=True,
    )
    return theta2_inverse, theta2


def center_sign_and_gauge(center: Coord) -> tuple[int, int | None]:
    forward_gauge = kernel_gauge_index(sub_coord(center, RAW_CENTER))
    if forward_gauge is not None:
        return 1, forward_gauge
    inverse_gauge = kernel_gauge_index(sub_coord(center, RAW_INVERSE_CENTER))
    if inverse_gauge is not None:
        return -1, inverse_gauge
    return 0, None


def profile_orientation_candidate(
    name: str,
    raw_center: Coord,
    raw_d: Coord,
    k_multiplier: int,
    reverse: bool,
) -> RawOrientationCandidateProfile:
    center = normalize(raw_center)
    d_step = normalize(raw_d)
    k_step = primitive_k_step(k_multiplier)
    _centers, footprint = anti_invariant_y_footprint(
        center,
        k_step,
        d_step,
        reverse=reverse,
    )
    theta2_inverse, theta2 = target_footprints()
    center_sign, center_gauge = center_sign_and_gauge(center)
    d_orientation, _d_forward, _d_reverse = d_orientation_and_gauge(d_step)
    primitive = gcd(k_multiplier % 25, 25) == 1
    emits_inverse = footprint == theta2_inverse
    emits_theta2 = footprint == theta2
    accepted = emits_inverse or emits_theta2
    ok = (
        primitive
        and center_sign in (-1, 1)
        and center_gauge is not None
        and d_orientation in (-1, 1)
        and len(footprint) == 300
        and accepted
    )
    return RawOrientationCandidateProfile(
        name=name,
        raw_center=center,
        raw_d=d_step,
        k_multiplier=k_multiplier % 25,
        product_orientation="reverse_y(-A)/y(A)" if reverse else "forward_y(A)/y(-A)",
        center_sign=center_sign,
        center_kernel_gauge_index=center_gauge,
        d_orientation=d_orientation,
        k_multiplier_primitive=primitive,
        footprint_support=len(footprint),
        emits_theta2_inverse=emits_inverse,
        emits_theta2=emits_theta2,
        emits_accepted_theta_payload=accepted,
        ok=ok,
    )


def shifted(base: Coord, gauge_index: int) -> Coord:
    return add_coord(base, scale_coord(KERNEL_SHIFT, gauge_index))


def profile_branch(branch_name: str, center_base: Coord, reverse: bool) -> RawOrientationBranchProfile:
    target_candidate = profile_orientation_candidate(
        branch_name,
        center_base,
        D_SHIFT,
        1,
        reverse,
    )
    emits = "theta2_inverse" if target_candidate.emits_theta2_inverse else "theta2"
    center_hits = sum(
        int(
            profile_orientation_candidate(
                f"{branch_name}_center_gauge_{index}",
                shifted(center_base, index),
                D_SHIFT,
                1,
                reverse,
            ).ok
        )
        for index in range(25)
    )
    d_hits = 0
    for d_base in (D_SHIFT, scale_coord(D_SHIFT, -1)):
        for index in range(25):
            d_hits += int(
                profile_orientation_candidate(
                    f"{branch_name}_d_gauge_{index}",
                    center_base,
                    shifted(d_base, index),
                    1,
                    reverse,
                ).ok
            )
    primitive_k_hits = sum(
        int(
            profile_orientation_candidate(
                f"{branch_name}_k_{multiplier}",
                center_base,
                D_SHIFT,
                multiplier,
                reverse,
            ).ok
        )
        for multiplier in range(25)
    )
    branch_count = center_hits * d_hits * primitive_k_hits
    ok = (
        target_candidate.ok
        and center_hits == 25
        and d_hits == 50
        and primitive_k_hits == 20
        and branch_count == 25000
    )
    return RawOrientationBranchProfile(
        branch_name=branch_name,
        raw_center=normalize(center_base),
        product_orientation=target_candidate.product_orientation,
        emits=emits,
        center_kernel_gauge_hits=center_hits,
        oriented_d_gauge_hits=d_hits,
        primitive_k_hits=primitive_k_hits,
        branch_parameter_presentations=branch_count,
        ok=ok,
    )


def profile_raw_reflection_orientation_contract() -> RawReflectionOrientationContractProfile:
    branches = (
        profile_branch("center_forward", RAW_CENTER, False),
        profile_branch("center_reverse", RAW_CENTER, True),
        profile_branch("inverse_center_forward", RAW_INVERSE_CENTER, False),
        profile_branch("inverse_center_reverse", RAW_INVERSE_CENTER, True),
    )
    inverse_branches = sum(int(branch.emits == "theta2_inverse") for branch in branches)
    theta2_branches = sum(int(branch.emits == "theta2") for branch in branches)
    branch_count = branches[0].branch_parameter_presentations
    wrong_center = profile_orientation_candidate(
        "wrong_center",
        add_coord(RAW_CENTER, (0, 1)),
        D_SHIFT,
        1,
        False,
    )
    wrong_d = profile_orientation_candidate(
        "wrong_d",
        RAW_CENTER,
        add_coord(D_SHIFT, (0, 1)),
        1,
        False,
    )
    nonprimitive_k = profile_orientation_candidate(
        "nonprimitive_k",
        RAW_CENTER,
        D_SHIFT,
        5,
        False,
    )
    row_ok = (
        RAW_CENTER == (47, 28)
        and RAW_INVERSE_CENTER == (28, 141)
        and all(branch.ok for branch in branches)
        and tuple((branch.branch_name, branch.emits) for branch in branches)
        == (
            ("center_forward", "theta2_inverse"),
            ("center_reverse", "theta2"),
            ("inverse_center_forward", "theta2"),
            ("inverse_center_reverse", "theta2_inverse"),
        )
        and inverse_branches == 2
        and theta2_branches == 2
        and branch_count == 25000
        and inverse_branches * branch_count == 50000
        and theta2_branches * branch_count == 50000
        and not wrong_center.ok
        and not wrong_d.ok
        and not nonprimitive_k.ok
    )
    return RawReflectionOrientationContractProfile(
        branch_profiles=branches,
        theta2_inverse_branches=inverse_branches,
        theta2_branches=theta2_branches,
        branch_parameter_presentations=branch_count,
        theta2_inverse_raw_presentations=inverse_branches * branch_count,
        theta2_raw_presentations=theta2_branches * branch_count,
        total_accepted_raw_presentations=(inverse_branches + theta2_branches) * branch_count,
        wrong_center_profile=wrong_center,
        wrong_d_profile=wrong_d,
        nonprimitive_k_profile=nonprimitive_k,
        raw_reflection_orientation_contract=(
            "accept either theta2 or theta2_inverse orientation: C/forward and "
            "-C/reverse emit theta2_inverse; C/reverse and -C/forward emit theta2"
        ),
        row_ok=row_ok,
    )


def print_candidate(prefix: str, profile: RawOrientationCandidateProfile) -> None:
    print(
        "  "
        f"{prefix}: C={profile.raw_center} D={profile.raw_d} "
        f"Kmult={profile.k_multiplier} orientation={profile.product_orientation} "
        f"Csign={profile.center_sign} Cgauge={profile.center_kernel_gauge_index} "
        f"Dorient={profile.d_orientation} primitive={int(profile.k_multiplier_primitive)} "
        f"theta2_inverse={int(profile.emits_theta2_inverse)} "
        f"theta2={int(profile.emits_theta2)} ok={int(profile.ok)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Classify raw anti-invariant product orientation for the p25 "
            "KL/KSY theta2 payload."
        )
    )
    parser.add_argument("--center-right", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--d-right", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    parser.add_argument("--reverse", action="store_true", help="use y(-A)/y(A)")
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang raw reflection-orientation contract gate")
    supplied = (
        args.center_right is not None,
        args.center_c is not None,
        args.d_right is not None,
        args.d_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all four raw center/D coordinates must be supplied together")
        candidate = profile_orientation_candidate(
            "raw_orientation_candidate",
            (args.center_right, args.center_c),
            (args.d_right, args.d_c),
            args.k_multiplier,
            args.reverse,
        )
        print("mode=raw_orientation_candidate")
        print_candidate("candidate_profile", candidate)
        print(
            "robert_ksy_theta2_kubert_lang_raw_reflection_orientation_candidate_rows="
            f"{int(candidate.ok)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_candidate")
        return 0 if candidate.ok else 1

    profile = profile_raw_reflection_orientation_contract()
    print("orientation_branches")
    for branch in profile.branch_profiles:
        print(
            "  "
            f"{branch.branch_name}: center={branch.raw_center} "
            f"orientation={branch.product_orientation} emits={branch.emits} "
            f"center_gauges={branch.center_kernel_gauge_hits} "
            f"D_gauges={branch.oriented_d_gauge_hits} "
            f"K_primitive={branch.primitive_k_hits} "
            f"presentations={branch.branch_parameter_presentations} "
            f"ok={int(branch.ok)}"
        )
    print("orientation_counts")
    print(f"  theta2_inverse_branches={profile.theta2_inverse_branches}")
    print(f"  theta2_branches={profile.theta2_branches}")
    print(f"  theta2_inverse_raw_presentations={profile.theta2_inverse_raw_presentations}")
    print(f"  theta2_raw_presentations={profile.theta2_raw_presentations}")
    print(f"  total_accepted_raw_presentations={profile.total_accepted_raw_presentations}")
    print_candidate("wrong_center_profile", profile.wrong_center_profile)
    print_candidate("wrong_d_profile", profile.wrong_d_profile)
    print_candidate("nonprimitive_k_profile", profile.nonprimitive_k_profile)
    print("interpretation")
    print("  C_forward_and_inverseC_reverse_emit_theta2_inverse=1")
    print("  C_reverse_and_inverseC_forward_emit_theta2=1")
    print("  wrong_center_wrong_D_and_nonprimitive_K_fail=1")
    print(
        "robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

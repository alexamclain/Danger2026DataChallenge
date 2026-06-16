#!/usr/bin/env python3
"""Quotient reflection-center contract for p25 KL/KSY theorem candidates.

The reflection-anchor gate shows that the row-selected packet is equivalently
described by a center and a D step:

    C=(2,28), D=(1,3), base=C-D, T=-2C.

This gate is a compact candidate intake for theorem outputs that naturally
emit the anti-invariant center and D segment rather than all six quotient
cells.  It derives base and T, then reuses the quotient-factor and source
packet contracts.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    add_quotient,
    scale_quotient,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_reflection_anchor_gate import (
    half_coord,
    inverse_coord,
    profile_reflection_anchor,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate import (
    RowLabeledPairCandidateProfile,
    profile_row_labeled_pair_candidate,
)
from p25_laneB_robert_ksy_theta2_quotient_factor_certificate_harness import (
    QuotientFactorCertificateProfile,
    profile_quotient_factor_certificate,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    profile_source_quotient_packet,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class ReflectionCenterCandidateProfile:
    name: str
    center_class: Coord
    d_class: Coord
    base_from_center: Coord
    t_from_reflection: Coord
    half_t: Coord
    negative_center: Coord
    half_t_is_negative_center: bool
    k_multiplier: int
    quotient_packet: tuple[tuple[Coord, int], ...]
    quotient_factor_profile: QuotientFactorCertificateProfile
    source_packet_profile: SourceQuotientPacketProfile
    row_labeled_pair_profile: RowLabeledPairCandidateProfile
    ok: bool


@dataclass(frozen=True)
class ReflectionCenterContractProfile:
    target_profile: ReflectionCenterCandidateProfile
    primitive_k_profile: ReflectionCenterCandidateProfile
    nonprimitive_k_profile: ReflectionCenterCandidateProfile
    wrong_center_row_profiles: tuple[ReflectionCenterCandidateProfile, ...]
    wrong_center_c_profile: ReflectionCenterCandidateProfile
    wrong_d_profile: ReflectionCenterCandidateProfile
    reflection_anchor_ok: bool
    target_center_d_derives_base_t: bool
    wrong_centers_rejected: bool
    wrong_d_rejected: bool
    candidate_contract: str
    row_ok: bool


def normalize(coord: Coord) -> Coord:
    return (coord[0] % QUOTIENT_RIGHT_ORDER, coord[1] % C_ORDER)


def packet_tuple(packet: Ring) -> tuple[tuple[Coord, int], ...]:
    return tuple(sorted(packet.items()))


def profile_reflection_center_candidate(
    name: str,
    center_class: Coord,
    d_class: Coord,
    k_multiplier: int = 1,
) -> ReflectionCenterCandidateProfile:
    center = normalize(center_class)
    d_step = normalize(d_class)
    base = add_quotient(center, scale_quotient(d_step, -1))
    t_step = inverse_coord(scale_quotient(center, 2))
    packet = source_packet(base, d_step, t_step)
    quotient_factor = profile_quotient_factor_certificate(
        name,
        base,
        d_step,
        t_step,
        k_multiplier,
    )
    source_profile = profile_source_quotient_packet(
        name,
        packet_entries(packet),
        k_multiplier,
    )
    row_pair_profile = profile_row_labeled_pair_candidate(
        name,
        packet,
        k_multiplier,
    )
    half_t = half_coord(t_step)
    negative_center = inverse_coord(center)
    row_ok = (
        center == (2, 28)
        and d_step == (1, 3)
        and base == (1, 25)
        and t_step == (2, 113)
        and half_t == negative_center == (1, 141)
        and quotient_factor.ok
        and source_profile.ok
        and row_pair_profile.ok
    )
    return ReflectionCenterCandidateProfile(
        name=name,
        center_class=center,
        d_class=d_step,
        base_from_center=base,
        t_from_reflection=t_step,
        half_t=half_t,
        negative_center=negative_center,
        half_t_is_negative_center=half_t == negative_center,
        k_multiplier=k_multiplier % 25,
        quotient_packet=packet_tuple(packet),
        quotient_factor_profile=quotient_factor,
        source_packet_profile=source_profile,
        row_labeled_pair_profile=row_pair_profile,
        ok=row_ok,
    )


def profile_reflection_center_contract() -> ReflectionCenterContractProfile:
    target = profile_reflection_center_candidate("target_reflection_center", (2, 28), (1, 3), 1)
    primitive_k = profile_reflection_center_candidate(
        "primitive_k_reflection_center",
        (2, 28),
        (1, 3),
        2,
    )
    nonprimitive_k = profile_reflection_center_candidate(
        "nonprimitive_k_reflection_center",
        (2, 28),
        (1, 3),
        5,
    )
    wrong_centers = tuple(
        profile_reflection_center_candidate(
            f"wrong_center_row_{row}",
            (row, 28),
            (1, 3),
            1,
        )
        for row in (0, 1)
    )
    wrong_center_c = profile_reflection_center_candidate(
        "wrong_center_c",
        (2, 29),
        (1, 3),
        1,
    )
    wrong_d = profile_reflection_center_candidate(
        "wrong_d",
        (2, 28),
        (1, 4),
        1,
    )
    anchor = profile_reflection_anchor()
    wrong_centers_rejected = (
        all(not profile.ok for profile in wrong_centers)
        and not wrong_center_c.ok
        and tuple(profile.t_from_reflection for profile in wrong_centers)
        == ((0, 113), (1, 113))
    )
    wrong_d_rejected = not wrong_d.ok
    target_derives = (
        target.center_class == (2, 28)
        and target.d_class == (1, 3)
        and target.base_from_center == (1, 25)
        and target.t_from_reflection == (2, 113)
        and target.half_t_is_negative_center
    )
    row_ok = (
        anchor.row_ok
        and target.ok
        and primitive_k.ok
        and not nonprimitive_k.ok
        and wrong_centers_rejected
        and wrong_d_rejected
        and target_derives
        and target.quotient_factor_profile.factor_certificate_profile.product_support == 150
        and target.source_packet_profile.packet_support == 6
        and target.row_labeled_pair_profile.row_labeled_pairs_exact
    )
    return ReflectionCenterContractProfile(
        target_profile=target,
        primitive_k_profile=primitive_k,
        nonprimitive_k_profile=nonprimitive_k,
        wrong_center_row_profiles=wrong_centers,
        wrong_center_c_profile=wrong_center_c,
        wrong_d_profile=wrong_d,
        reflection_anchor_ok=anchor.row_ok,
        target_center_d_derives_base_t=target_derives,
        wrong_centers_rejected=wrong_centers_rejected,
        wrong_d_rejected=wrong_d_rejected,
        candidate_contract=(
            "emit quotient center C=(2,28), D=(1,3), and primitive K; "
            "base=C-D and T=-2C are derived before quotient-factor and "
            "row-labeled-pair verification"
        ),
        row_ok=row_ok,
    )


def print_candidate(prefix: str, profile: ReflectionCenterCandidateProfile) -> None:
    print(
        "  "
        f"{prefix}: "
        f"C={profile.center_class} D={profile.d_class} "
        f"base={profile.base_from_center} T={profile.t_from_reflection} "
        f"factor_ok={int(profile.quotient_factor_profile.ok)} "
        f"source_ok={int(profile.source_packet_profile.ok)} "
        f"pairs_ok={int(profile.row_labeled_pair_profile.ok)} "
        f"ok={int(profile.ok)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit quotient reflection-center data for the p25 KL/KSY target: "
            "center C and D, deriving base=C-D and T=-2C."
        )
    )
    parser.add_argument("--center-right-class", type=int)
    parser.add_argument("--center-c", type=int)
    parser.add_argument("--d-right-class", type=int)
    parser.add_argument("--d-c", type=int)
    parser.add_argument("--k-multiplier", type=int, default=1)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang reflection-center contract gate")
    print(f"quotient_group=C_{QUOTIENT_RIGHT_ORDER}xC_{C_ORDER}")
    supplied = (
        args.center_right_class is not None,
        args.center_c is not None,
        args.d_right_class is not None,
        args.d_c is not None,
    )
    if any(supplied):
        if not all(supplied):
            raise SystemExit("all four center/D coordinates must be supplied together")
        candidate = profile_reflection_center_candidate(
            "reflection_center_candidate",
            (args.center_right_class, args.center_c),
            (args.d_right_class, args.d_c),
            args.k_multiplier,
        )
        print("mode=reflection_center_candidate")
        print_candidate("reflection_center_candidate_profile", candidate)
        print("candidate_contract")
        print("  pass requires C=(2,28), D=(1,3), primitive K")
        print("  base=C-D and T=-2C are derived")
        print("  derived packet must pass quotient-factor and row-labeled-pair contracts")
        print(
            "robert_ksy_theta2_kubert_lang_reflection_center_candidate_rows="
            f"{int(candidate.ok)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_candidate")
        return 0 if candidate.ok else 1

    profile = profile_reflection_center_contract()
    print("reflection_center_contract_summary")
    print(f"  reflection_anchor_ok={int(profile.reflection_anchor_ok)}")
    print(f"  target_center_d_derives_base_t={int(profile.target_center_d_derives_base_t)}")
    print(f"  wrong_centers_rejected={int(profile.wrong_centers_rejected)}")
    print(f"  wrong_d_rejected={int(profile.wrong_d_rejected)}")
    print_candidate("target_profile", profile.target_profile)
    print_candidate("primitive_k_profile", profile.primitive_k_profile)
    print_candidate("nonprimitive_k_profile", profile.nonprimitive_k_profile)
    print("wrong_center_row_profiles")
    for control in profile.wrong_center_row_profiles:
        print_candidate("  control", control)
    print_candidate("wrong_center_c_profile", profile.wrong_center_c_profile)
    print_candidate("wrong_d_profile", profile.wrong_d_profile)
    print("interpretation")
    print("  quotient_center_D_payload_derives_base_and_T=1")
    print("  target_C_2_28_D_1_3_primitive_K_passes=1")
    print("  wrong_center_rows_wrong_center_c_wrong_D_and_nonprimitive_K_fail=1")
    print(
        "robert_ksy_theta2_kubert_lang_reflection_center_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

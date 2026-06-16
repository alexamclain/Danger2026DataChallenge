#!/usr/bin/env python3
"""Source-quotient six-cell packet intake for the p25 KSY theta2 route.

The quotient-factor harness accepts the factorized quotient data

    base=(1,25), D=(1,3), T=(2,113)

in `(C_75/K) x C_169`.  This harness accepts the equivalent six-cell source
quotient packet directly:

    base * (1 + D + D^2) * (1 - T).

It then lifts the packet through a primitive 25-point K trace and reuses the
existing raw bridge contract.  This is useful for theorem or literature hits
that naturally emit a finite quotient divisor packet rather than a factorized
word.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from math import gcd
from pathlib import Path

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    scale_coord,
    source_mask_to_raw,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q


QuotientCoord = tuple[int, int]
QuotientEntry = tuple[int, int, int]

QUOTIENT_RIGHT_ORDER = 3
BASE_CLASS = (1, 25)
D_CLASS = (1, 3)
T_CLASS = (2, 113)


@dataclass(frozen=True)
class SourceQuotientPacketProfile:
    name: str
    k_multiplier: int
    k_step: tuple[int, int]
    k_multiplier_primitive: bool
    input_terms: int
    active_packet_terms: int
    duplicate_packet_terms: int
    packet_support: int
    packet_coefficient_counts: tuple[tuple[int, int], ...]
    packet_exact: bool
    lifted_source_support: int
    bridge_profile: CandidateProfile
    ok: bool


def add_quotient_coord(left: QuotientCoord, right: QuotientCoord) -> QuotientCoord:
    return (
        (left[0] + right[0]) % QUOTIENT_RIGHT_ORDER,
        (left[1] + right[1]) % C_ORDER,
    )


def scale_quotient_coord(coord: QuotientCoord, scalar: int) -> QuotientCoord:
    return (
        (coord[0] * scalar) % QUOTIENT_RIGHT_ORDER,
        (coord[1] * scalar) % C_ORDER,
    )


def add_packet_entry(packet: dict[QuotientCoord, int], coord: QuotientCoord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def target_source_quotient_packet() -> dict[QuotientCoord, int]:
    packet: dict[QuotientCoord, int] = {}
    for index in range(3):
        positive = add_quotient_coord(BASE_CLASS, scale_quotient_coord(D_CLASS, index))
        negative = add_quotient_coord(positive, T_CLASS)
        add_packet_entry(packet, positive, 1)
        add_packet_entry(packet, negative, -1)
    return dict(sorted(packet.items()))


def q_cycle_confusion_packet() -> dict[QuotientCoord, int]:
    return {
        coord_from_q(q_value): coefficient
        for q_value, coefficient in bridge_coefficients().items()
    }


def primitive_k_step(k_multiplier: int) -> tuple[int, int]:
    return scale_coord(KERNEL_SHIFT, k_multiplier % 25)


def lift_packet_to_source(packet: dict[QuotientCoord, int], k_step: tuple[int, int]) -> Ring:
    out: Ring = {}
    for (right_class, c_log), coefficient in packet.items():
        base = (right_class % QUOTIENT_RIGHT_ORDER, c_log % C_ORDER)
        for index in range(25):
            coord = add_coord(base, scale_coord(k_step, index))
            out[coord] = out.get(coord, 0) + coefficient
            if out[coord] == 0:
                del out[coord]
    return dict(sorted(out.items()))


def entries_to_packet(entries: tuple[QuotientEntry, ...]) -> tuple[dict[QuotientCoord, int], int, int]:
    packet: dict[QuotientCoord, int] = {}
    duplicate_terms = 0
    for right_class, c_log, coefficient in entries:
        coord = (right_class % QUOTIENT_RIGHT_ORDER, c_log % C_ORDER)
        duplicate_terms += int(coord in packet)
        add_packet_entry(packet, coord, coefficient)
    return dict(sorted(packet.items())), len(packet), duplicate_terms


def packet_entries(packet: dict[QuotientCoord, int]) -> tuple[QuotientEntry, ...]:
    return tuple((right_class, c_log, coefficient) for (right_class, c_log), coefficient in packet.items())


def coefficient_counts(packet: dict[QuotientCoord, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(packet.values()).items()))


def parse_packet(path: Path) -> tuple[QuotientEntry, ...]:
    entries: list[QuotientEntry] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        clean = line.split("#", 1)[0]
        for char in ",()[]":
            clean = clean.replace(char, " ")
        if not clean.strip():
            continue
        parts = clean.split()
        if len(parts) != 3:
            raise ValueError(f"{path}:{line_number} expected three integers: right_class c coeff")
        entries.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return tuple(entries)


def profile_source_quotient_packet(
    name: str,
    entries: tuple[QuotientEntry, ...],
    k_multiplier: int,
) -> SourceQuotientPacketProfile:
    packet, active_terms, duplicate_terms = entries_to_packet(entries)
    k_step = primitive_k_step(k_multiplier)
    primitive = gcd(k_multiplier % 25, 25) == 1
    lifted = lift_packet_to_source(packet, k_step)
    bridge_profile = profile_candidate(name, source_mask_to_raw(lifted), target_raw_bridge())
    target_packet = target_source_quotient_packet()
    row_ok = (
        primitive
        and packet == target_packet
        and len(packet) == 6
        and coefficient_counts(packet) == ((-1, 3), (1, 3))
        and len(lifted) == 150
        and bridge_profile.ok
    )
    return SourceQuotientPacketProfile(
        name=name,
        k_multiplier=k_multiplier % 25,
        k_step=k_step,
        k_multiplier_primitive=primitive,
        input_terms=len(entries),
        active_packet_terms=active_terms,
        duplicate_packet_terms=duplicate_terms,
        packet_support=len(packet),
        packet_coefficient_counts=coefficient_counts(packet),
        packet_exact=packet == target_packet,
        lifted_source_support=len(lifted),
        bridge_profile=bridge_profile,
        ok=row_ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a six-cell source quotient packet on C_3 x C_169 and lift "
            "it through a primitive K trace to the p25 bridge contract."
        )
    )
    parser.add_argument("--packet", type=Path, help="optional triples: right_class c coeff")
    parser.add_argument("--k-multiplier", type=int, default=1)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY/theta2 source-quotient packet harness")
    print(f"quotient_source_group=C_{QUOTIENT_RIGHT_ORDER}xC_{C_ORDER}")

    if args.packet is not None:
        profile = profile_source_quotient_packet(
            str(args.packet),
            parse_packet(args.packet),
            args.k_multiplier,
        )
        print("mode=source_quotient_packet_candidate")
        print(f"source_quotient_packet_profile={profile}")
        print("candidate_contract")
        print("  pass requires exact source quotient six-cell packet")
        print("  pass requires primitive K multiplier modulo 25")
        print("  pass lifts to the existing bridge contract")
        print(f"robert_ksy_theta2_source_quotient_packet_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_source_quotient_packet_candidate")
        return 0 if profile.ok else 1

    target = target_source_quotient_packet()
    target_profile = profile_source_quotient_packet(
        "target_source_quotient_packet",
        packet_entries(target),
        1,
    )
    primitive_k_profile = profile_source_quotient_packet(
        "primitive_K_multiplier_control",
        packet_entries(target),
        2,
    )
    nonprimitive_k_profile = profile_source_quotient_packet(
        "nonprimitive_K_multiplier_control",
        packet_entries(target),
        5,
    )
    positive_only_profile = profile_source_quotient_packet(
        "positive_only_packet_control",
        packet_entries({coord: coeff for coord, coeff in target.items() if coeff > 0}),
        1,
    )
    wrong_c_packet = dict(target)
    wrong_c_packet[((0, 138))] = 0
    wrong_c_packet.pop((0, 138), None)
    wrong_c_packet[(0, 139)] = -1
    wrong_c_profile = profile_source_quotient_packet(
        "wrong_c_packet_control",
        packet_entries(wrong_c_packet),
        1,
    )
    q_cycle_profile = profile_source_quotient_packet(
        "q_cycle_convention_confusion_control",
        packet_entries(q_cycle_confusion_packet()),
        1,
    )
    row_ok = (
        target_profile.ok
        and primitive_k_profile.ok
        and not nonprimitive_k_profile.ok
        and not positive_only_profile.ok
        and not wrong_c_profile.ok
        and not q_cycle_profile.ok
        and target_profile.packet_support == 6
        and target_profile.lifted_source_support == 150
        and target_profile.packet_coefficient_counts == ((-1, 3), (1, 3))
        and q_cycle_profile.packet_support == 6
        and not q_cycle_profile.packet_exact
    )
    print(f"target_source_quotient_packet_profile={target_profile}")
    print(f"primitive_K_multiplier_control_profile={primitive_k_profile}")
    print(f"nonprimitive_K_multiplier_control_profile={nonprimitive_k_profile}")
    print(f"positive_only_packet_control_profile={positive_only_profile}")
    print(f"wrong_c_packet_control_profile={wrong_c_profile}")
    print(f"q_cycle_convention_confusion_control_profile={q_cycle_profile}")
    print("source_quotient_packet_laws")
    print("  target_packet_is_base_times_1_plus_D_plus_D2_times_1_minus_T=1")
    print("  target_packet_has_3_positive_and_3_negative_cells=1")
    print("  primitive_K_trace_lift_has_150_source_cells_and_passes_bridge_contract=1")
    print("  nonprimitive_K_positive_only_wrong_c_and_q_cycle_convention_controls_fail=1")
    print(f"robert_ksy_theta2_source_quotient_packet_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_source_quotient_packet_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Executable intake for the p25 row-labeled Kubert-Lang pair payload.

The graph-separability gate leaves a very specific theorem target: not a
row-only mask times the C_169 projection, but the exact six-cell packet viewed
as three row-labeled signed pairs:

    row 0: c31 - c138
    row 1: c25 - c141
    row 2: c28 - c144

This gate turns that shape into a candidate contract.  A theorem hit may emit
the six quotient triples directly; passing requires the exact row-labeled
pair packet and the existing primitive-K source packet lift.  Controls show
that row-only projections, fixed-T row translates, and wrong row pairings with
the same C-axis projection do not pass.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_graph_row_law_gate import (
    sign_affine_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_graph_separability_gate import (
    C_AXIS_COLUMNS,
    profile_graph_separability,
    row_mask_packet,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    parse_packet,
    profile_source_quotient_packet,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class RowLabeledPair:
    row: int
    positive_c: int
    negative_c: int


@dataclass(frozen=True)
class RowLabeledPairCandidateProfile:
    name: str
    input_support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    row_pair_count: int
    malformed_rows: tuple[int, ...]
    rows_with_terms: tuple[int, ...]
    c_axis_projection: tuple[int, ...]
    c_axis_projection_matches_target: bool
    row_labeled_pairs: tuple[RowLabeledPair, ...]
    row_labeled_pairs_exact: bool
    source_packet_profile: SourceQuotientPacketProfile
    ok: bool


@dataclass(frozen=True)
class RowLabeledPairContractProfile:
    target_profile: RowLabeledPairCandidateProfile
    wrong_fixed_t_translate_profiles: tuple[RowLabeledPairCandidateProfile, ...]
    row_only_projection_profiles: tuple[RowLabeledPairCandidateProfile, ...]
    wrong_pairing_same_projection_profile: RowLabeledPairCandidateProfile
    graph_separability_ok: bool
    target_is_three_exact_row_labeled_pairs: bool
    wrong_fixed_t_translates_rejected: bool
    row_only_projection_shortcuts_rejected: bool
    wrong_pairing_same_projection_rejected: bool
    candidate_contract: str
    row_ok: bool


TARGET_ROW_LABELED_PAIRS = (
    RowLabeledPair(0, 31, 138),
    RowLabeledPair(1, 25, 141),
    RowLabeledPair(2, 28, 144),
)


def add_packet_entry(packet: Ring, coord: Coord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def coefficient_counts(packet: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(packet.values()).items()))


def c_axis_projection_vector(packet: Ring) -> tuple[int, ...]:
    return tuple(
        sum(coefficient for (row, c_log), coefficient in packet.items() if c_log == column)
        for column in C_AXIS_COLUMNS
    )


def row_labeled_pairs(packet: Ring) -> tuple[tuple[RowLabeledPair, ...], tuple[int, ...]]:
    pairs: list[RowLabeledPair] = []
    malformed_rows: list[int] = []
    for row in range(QUOTIENT_RIGHT_ORDER):
        positives = sorted(
            c_log
            for (right_row, c_log), coefficient in packet.items()
            if right_row == row and coefficient > 0
        )
        negatives = sorted(
            c_log
            for (right_row, c_log), coefficient in packet.items()
            if right_row == row and coefficient < 0
        )
        if not positives and not negatives:
            continue
        if len(positives) != 1 or len(negatives) != 1:
            malformed_rows.append(row)
            continue
        pairs.append(RowLabeledPair(row, positives[0], negatives[0]))
    return tuple(pairs), tuple(malformed_rows)


def rows_with_terms(packet: Ring) -> tuple[int, ...]:
    return tuple(sorted({row for row, _c_log in packet}))


def shift_rows(packet: Ring, delta: int) -> Ring:
    shifted: Ring = {}
    for (row, c_log), coefficient in packet.items():
        add_packet_entry(shifted, ((row + delta) % QUOTIENT_RIGHT_ORDER, c_log), coefficient)
    return dict(sorted(shifted.items()))


def wrong_pairing_same_projection_packet() -> Ring:
    packet: Ring = {}
    for pair in (
        RowLabeledPair(0, 31, 141),
        RowLabeledPair(1, 25, 144),
        RowLabeledPair(2, 28, 138),
    ):
        add_packet_entry(packet, (pair.row, pair.positive_c), 1)
        add_packet_entry(packet, (pair.row, pair.negative_c), -1)
    return dict(sorted(packet.items()))


def profile_row_labeled_pair_candidate(
    name: str,
    packet: Ring,
    k_multiplier: int = 1,
) -> RowLabeledPairCandidateProfile:
    pairs, malformed_rows = row_labeled_pairs(packet)
    c_projection = c_axis_projection_vector(packet)
    source_profile = profile_source_quotient_packet(
        name,
        packet_entries(packet),
        k_multiplier,
    )
    exact_pairs = pairs == TARGET_ROW_LABELED_PAIRS and not malformed_rows
    c_projection_matches = c_projection == (1, 1, 1, -1, -1, -1)
    ok = (
        len(packet) == 6
        and coefficient_counts(packet) == ((-1, 3), (1, 3))
        and rows_with_terms(packet) == (0, 1, 2)
        and exact_pairs
        and c_projection_matches
        and source_profile.ok
    )
    return RowLabeledPairCandidateProfile(
        name=name,
        input_support=len(packet),
        coefficient_counts=coefficient_counts(packet),
        row_pair_count=len(pairs),
        malformed_rows=malformed_rows,
        rows_with_terms=rows_with_terms(packet),
        c_axis_projection=c_projection,
        c_axis_projection_matches_target=c_projection_matches,
        row_labeled_pairs=pairs,
        row_labeled_pairs_exact=exact_pairs,
        source_packet_profile=source_profile,
        ok=ok,
    )


def profile_row_labeled_pair_contract() -> RowLabeledPairContractProfile:
    target = source_packet()
    target_profile = profile_row_labeled_pair_candidate("target_row_labeled_pairs", target)
    wrong_fixed_t_profiles = tuple(
        profile_row_labeled_pair_candidate(
            f"wrong_fixed_T_row_translate_{delta}",
            shift_rows(target, delta),
        )
        for delta in (1, 2)
    )
    row_only_profiles = tuple(
        profile_row_labeled_pair_candidate(
            f"row_only_projection_mask_{''.join(str(row) for row in mask)}",
            row_mask_packet(mask),
        )
        for mask in ((0,), (1,), (2,), (0, 1, 2))
    )
    wrong_pairing_profile = profile_row_labeled_pair_candidate(
        "wrong_pairing_same_C_projection",
        wrong_pairing_same_projection_packet(),
    )
    separability = profile_graph_separability()
    wrong_translates_rejected = all(not profile.ok for profile in wrong_fixed_t_profiles)
    row_only_rejected = (
        all(not profile.ok for profile in row_only_profiles)
        and separability.row_only_masks_all_fail_source_contract
    )
    wrong_pairing_rejected = (
        wrong_pairing_profile.c_axis_projection_matches_target
        and wrong_pairing_profile.row_pair_count == 3
        and not wrong_pairing_profile.ok
    )
    row_ok = (
        C_ORDER == 169
        and QUOTIENT_RIGHT_ORDER == 3
        and target_profile.ok
        and target_profile.row_labeled_pairs == TARGET_ROW_LABELED_PAIRS
        and target_profile.source_packet_profile.lifted_source_support == 150
        and wrong_translates_rejected
        and tuple(
            profile.source_packet_profile.packet_support
            for profile in wrong_fixed_t_profiles
        )
        == (6, 6)
        and row_only_rejected
        and tuple(profile.input_support for profile in row_only_profiles) == (6, 6, 6, 18)
        and wrong_pairing_rejected
        and separability.row_ok
    )
    return RowLabeledPairContractProfile(
        target_profile=target_profile,
        wrong_fixed_t_translate_profiles=wrong_fixed_t_profiles,
        row_only_projection_profiles=row_only_profiles,
        wrong_pairing_same_projection_profile=wrong_pairing_profile,
        graph_separability_ok=separability.row_ok,
        target_is_three_exact_row_labeled_pairs=target_profile.ok,
        wrong_fixed_t_translates_rejected=wrong_translates_rejected,
        row_only_projection_shortcuts_rejected=row_only_rejected,
        wrong_pairing_same_projection_rejected=wrong_pairing_rejected,
        candidate_contract=(
            "emit the exact six quotient triples, equivalently the three "
            "row-labeled signed pairs row0:c31-c138, row1:c25-c141, "
            "row2:c28-c144; the primitive-K lift must pass the source contract"
        ),
        row_ok=row_ok,
    )


def packet_from_entries(entries: tuple[tuple[int, int, int], ...]) -> Ring:
    packet: Ring = {}
    for row, c_log, coefficient in entries:
        add_packet_entry(packet, (row % QUOTIENT_RIGHT_ORDER, c_log % C_ORDER), coefficient)
    return dict(sorted(packet.items()))


def print_candidate_profile(prefix: str, profile: RowLabeledPairCandidateProfile) -> None:
    print(f"{prefix}={profile}")
    print(
        "  "
        f"support={profile.input_support} pairs={profile.row_pair_count} "
        f"malformed_rows={profile.malformed_rows} "
        f"c_projection_ok={int(profile.c_axis_projection_matches_target)} "
        f"exact_pairs={int(profile.row_labeled_pairs_exact)} "
        f"source_ok={int(profile.source_packet_profile.ok)} "
        f"ok={int(profile.ok)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a theorem candidate for the p25 row-labeled Kubert-Lang "
            "pair payload.  Input triples are: right_row c_log coefficient."
        )
    )
    parser.add_argument("--packet", type=Path, help="optional quotient triples file")
    parser.add_argument("--k-multiplier", type=int, default=1)
    args = parser.parse_args()

    print("p25 Lane B Robert KSY Kubert-Lang row-labeled pair contract gate")
    print(f"quotient_group=C_{QUOTIENT_RIGHT_ORDER}xC_{C_ORDER}")

    if args.packet is not None:
        candidate = profile_row_labeled_pair_candidate(
            str(args.packet),
            packet_from_entries(parse_packet(args.packet)),
            args.k_multiplier,
        )
        print("mode=row_labeled_pair_candidate")
        print_candidate_profile("row_labeled_pair_candidate_profile", candidate)
        print("candidate_contract")
        print("  pass requires exact row-labeled signed pairs")
        print("  pass requires exact C-axis projection")
        print("  pass requires primitive-K source packet lift")
        print(
            "robert_ksy_theta2_kubert_lang_row_labeled_pair_candidate_rows="
            f"{int(candidate.ok)}/1"
        )
        print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_candidate")
        return 0 if candidate.ok else 1

    profile = profile_row_labeled_pair_contract()
    print(f"row_labeled_pair_contract_profile={profile}")
    print_candidate_profile("target_profile", profile.target_profile)
    print("wrong_fixed_T_row_translates")
    for control in profile.wrong_fixed_t_translate_profiles:
        print_candidate_profile("  control", control)
    print("row_only_projection_shortcuts")
    for control in profile.row_only_projection_profiles:
        print_candidate_profile("  control", control)
    print_candidate_profile(
        "wrong_pairing_same_projection_profile",
        profile.wrong_pairing_same_projection_profile,
    )
    print("interpretation")
    print("  exact_three_row_labeled_signed_pairs_pass=1")
    print("  wrong_fixed_T_row_translates_fail=1")
    print("  row_only_projection_shortcuts_fail=1")
    print("  wrong_pairing_with_same_C_projection_fails=1")
    print("  theorem_payload_is_mixed_row_C_not_separable_projection=1")
    print(
        "robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

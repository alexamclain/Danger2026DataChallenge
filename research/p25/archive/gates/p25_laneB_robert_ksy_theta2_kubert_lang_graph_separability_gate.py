#!/usr/bin/env python3
"""Separable row/C obstruction for the p25 Kubert-Lang graph packet.

The graph row-law gate showed that the C_169 projection plus KL congruences
does not select the p25 row graph.  This gate checks the tempting shortcut:
recover the row anchor by multiplying the C-axis projection by a row-only
character, mask, or phase.

That cannot work as a single separated row/C factor.  The exact packet is a
rank-3 row-by-C matrix.  Any row-only factor times a C-axis vector has rank 1.
The positive form left behind is the row-labeled anti-invariant pair
decomposition:

    row 1:  c25  - c141
    row 2:  c28  - c144
    row 0:  c31  - c138.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    QUOTIENT_RIGHT_ORDER,
    Ring,
    c_axis_projection,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    profile_source_quotient_packet,
)


C_AXIS_COLUMNS = (25, 28, 31, 138, 141, 144)


@dataclass(frozen=True)
class RowMaskProfile:
    row_mask: tuple[int, ...]
    support: int
    matrix_rank: int
    source_packet_ok: bool


@dataclass(frozen=True)
class RowPair:
    row: int
    positive_c: int
    negative_c: int


@dataclass(frozen=True)
class GraphSeparabilityProfile:
    c_axis_columns: tuple[int, ...]
    target_matrix: tuple[tuple[int, ...], ...]
    target_rank: int
    target_row_sums: tuple[int, int, int]
    target_column_sums: tuple[int, ...]
    c_axis_projection_vector: tuple[int, ...]
    row_only_masks_scanned: int
    row_only_mask_profiles: tuple[RowMaskProfile, ...]
    row_only_support_counts: tuple[tuple[int, int], ...]
    row_only_rank_counts: tuple[tuple[int, int], ...]
    row_only_masks_all_fail_source_contract: bool
    minimal_separable_rank_one_terms: int
    row_labeled_pair_decomposition: tuple[RowPair, ...]
    row_character_shortcut_killed: bool
    next_debt: str
    row_ok: bool


def add_packet_entry(packet: Ring, coord: tuple[int, int], coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def matrix_from_packet(packet: Ring) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = []
    for row in range(QUOTIENT_RIGHT_ORDER):
        rows.append([packet.get((row, c_log), 0) for c_log in C_AXIS_COLUMNS])
    return tuple(tuple(row) for row in rows)


def rational_rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    col_count = len(work[0]) if work else 0
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][col]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(row_count):
            if row == rank or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def c_projection_vector() -> tuple[int, ...]:
    projected = c_axis_projection(source_packet())
    return tuple(projected.get((0, c_log), 0) for c_log in C_AXIS_COLUMNS)


def row_mask_packet(row_mask: tuple[int, ...]) -> Ring:
    vector = c_projection_vector()
    packet: Ring = {}
    for row in row_mask:
        for c_log, coefficient in zip(C_AXIS_COLUMNS, vector):
            if coefficient:
                add_packet_entry(packet, (row, c_log), coefficient)
    return dict(sorted(packet.items()))


def profile_row_mask(row_mask: tuple[int, ...]) -> RowMaskProfile:
    packet = row_mask_packet(row_mask)
    source_profile = profile_source_quotient_packet(
        f"row_only_mask_{''.join(str(row) for row in row_mask)}",
        packet_entries(packet),
        1,
    )
    return RowMaskProfile(
        row_mask=row_mask,
        support=len(packet),
        matrix_rank=rational_rank(matrix_from_packet(packet)),
        source_packet_ok=source_profile.ok,
    )


def row_pair_decomposition(packet: Ring) -> tuple[RowPair, ...]:
    pairs: list[RowPair] = []
    for row in range(QUOTIENT_RIGHT_ORDER):
        positives = [c_log for c_log in C_AXIS_COLUMNS if packet.get((row, c_log), 0) > 0]
        negatives = [c_log for c_log in C_AXIS_COLUMNS if packet.get((row, c_log), 0) < 0]
        if positives or negatives:
            if len(positives) != 1 or len(negatives) != 1:
                raise AssertionError("row is not a single anti-invariant pair")
            pairs.append(RowPair(row, positives[0], negatives[0]))
    return tuple(pairs)


def profile_graph_separability() -> GraphSeparabilityProfile:
    target = source_packet()
    target_matrix = matrix_from_packet(target)
    row_profiles = tuple(
        profile_row_mask(tuple(row for row in range(QUOTIENT_RIGHT_ORDER) if mask & (1 << row)))
        for mask in range(1, 1 << QUOTIENT_RIGHT_ORDER)
    )
    support_counts = tuple(sorted(Counter(profile.support for profile in row_profiles).items()))
    rank_counts = tuple(sorted(Counter(profile.matrix_rank for profile in row_profiles).items()))
    row_only_all_fail = all(not profile.source_packet_ok for profile in row_profiles)
    row_pairs = row_pair_decomposition(target)
    target_rank = rational_rank(target_matrix)
    row_ok = (
        QUOTIENT_RIGHT_ORDER == 3
        and C_AXIS_COLUMNS == (25, 28, 31, 138, 141, 144)
        and target_matrix
        == (
            (0, 0, 1, -1, 0, 0),
            (1, 0, 0, 0, -1, 0),
            (0, 1, 0, 0, 0, -1),
        )
        and target_rank == 3
        and tuple(sum(row) for row in target_matrix) == (0, 0, 0)
        and tuple(sum(target_matrix[row][col] for row in range(QUOTIENT_RIGHT_ORDER)) for col in range(len(C_AXIS_COLUMNS)))
        == (1, 1, 1, -1, -1, -1)
        and c_projection_vector() == (1, 1, 1, -1, -1, -1)
        and len(row_profiles) == 7
        and support_counts == ((6, 3), (12, 3), (18, 1))
        and rank_counts == ((1, 7),)
        and row_only_all_fail
        and row_pairs
        == (
            RowPair(0, 31, 138),
            RowPair(1, 25, 141),
            RowPair(2, 28, 144),
        )
    )
    return GraphSeparabilityProfile(
        c_axis_columns=C_AXIS_COLUMNS,
        target_matrix=target_matrix,
        target_rank=target_rank,
        target_row_sums=tuple(sum(row) for row in target_matrix),  # type: ignore[arg-type]
        target_column_sums=tuple(
            sum(target_matrix[row][col] for row in range(QUOTIENT_RIGHT_ORDER))
            for col in range(len(C_AXIS_COLUMNS))
        ),
        c_axis_projection_vector=c_projection_vector(),
        row_only_masks_scanned=len(row_profiles),
        row_only_mask_profiles=row_profiles,
        row_only_support_counts=support_counts,
        row_only_rank_counts=rank_counts,
        row_only_masks_all_fail_source_contract=row_only_all_fail,
        minimal_separable_rank_one_terms=target_rank,
        row_labeled_pair_decomposition=row_pairs,
        row_character_shortcut_killed=(target_rank > 1 and row_only_all_fail),
        next_debt=(
            "the exact KL/Siegel formula must provide a mixed row-C graph or "
            "the three row-labeled anti-invariant pairs; a row-only character "
            "or mask applied to the C169 projection is rank-one and fails"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang graph separability gate")
    profile = profile_graph_separability()
    print(f"kl_graph_separability_profile={profile}")
    print("target_matrix")
    for row in profile.target_matrix:
        print(f"  {row}")
    print("row_only_masks")
    for row_profile in profile.row_only_mask_profiles:
        print(
            "  "
            f"rows={row_profile.row_mask} support={row_profile.support} "
            f"rank={row_profile.matrix_rank} ok={int(row_profile.source_packet_ok)}"
        )
    print("row_labeled_pairs")
    for pair in profile.row_labeled_pair_decomposition:
        print(f"  row={pair.row}: c{pair.positive_c} - c{pair.negative_c}")
    print("interpretation")
    print("  target_row_by_C_matrix_has_rank_3=1")
    print("  row_only_character_or_mask_times_C169_projection_has_rank_1=1")
    print("  row_only_masks_all_fail_source_packet_contract=1")
    print("  exact_formula_must_supply_three_row_labeled_anti_invariant_pairs=1")
    print(
        "robert_ksy_theta2_kubert_lang_graph_separability_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_graph_separability_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

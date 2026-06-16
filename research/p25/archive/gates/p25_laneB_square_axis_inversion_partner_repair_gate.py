#!/usr/bin/env python3
"""Inversion-partner completion gate for the square-axis anomaly.

The scalar-balance selected-defect gate leaves a three-point diagonal defect
with value -1 at

    (right,c) = (0,46), (1,47), (2,48).

That defect fails only because the off-C-zero inversion sums are not constant.
This gate checks the smallest local non-cancelling completion: add +1 at the
three inversion partners of those points.  The resulting six-point row is
degree zero, anti-invariant under inversion, and satisfies both the selected
defect value identities and the raw producer identities in the quotient and
raw split fields.

This is not a certificate.  It is a producer-facing positive artifact: a
candidate source no longer needs to explain a dense scalar background, but it
must explain why the fixed anomaly slice is paired with its inversion-partner
slice or an equivalent value-side completion.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    coord_from_q,
    q_from_coord,
)
from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    raw_producer_conditions,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


SQUARE_C = 169
QUOTIENT_ORDER = RIGHT_DEGREE * SQUARE_C
RAW_KERNEL_SIZE = 25


Coord = tuple[int, int]


@dataclass(frozen=True)
class PairProfile:
    anomaly_q: int
    anomaly_coord: Coord
    partner_q: int
    partner_coord: Coord


@dataclass(frozen=True)
class RepairProfile:
    modulus_name: str
    modulus: int
    defect_support: tuple[Coord, ...]
    repair_support: tuple[Coord, ...]
    completed_support: tuple[Coord, ...]
    completed_q_support: tuple[int, ...]
    defect_degree: int
    completed_degree: int
    defect_row_sums: tuple[int, int, int]
    completed_row_sums: tuple[int, int, int]
    defect_inversion_sums: tuple[int, ...]
    completed_inversion_sums: tuple[int, ...]
    defect_value_conditions_ok: bool
    completed_value_conditions_ok: bool
    defect_raw_producer_ok: bool
    completed_raw_producer_ok: bool
    selected_defect_self: bool
    anti_invariant: bool
    bad_pair_count: int
    off_pair_count: int
    target_zero_local_lower_bound: int
    target_minus_one_lower_bound: int


def inversion_coord(coord: Coord) -> Coord:
    right, c_coord = coord
    return ((-right) % RIGHT_DEGREE, (-c_coord) % SQUARE_C)


def packet_from_entries(entries: list[tuple[Coord, int]], modulus: int) -> list[int]:
    packet = [0] * QUOTIENT_ORDER
    for (right, c_coord), value in entries:
        packet[right * SQUARE_C + c_coord] = (
            packet[right * SQUARE_C + c_coord] + value
        ) % modulus
    return packet


def add_packets(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def support_coords(packet: list[int], modulus: int) -> tuple[Coord, ...]:
    coords: list[Coord] = []
    for right in range(RIGHT_DEGREE):
        for c_coord in range(SQUARE_C):
            if packet[right * SQUARE_C + c_coord] % modulus:
                coords.append((right, c_coord))
    return tuple(coords)


def support_qs(packet: list[int], modulus: int) -> tuple[int, ...]:
    return tuple(
        sorted(q_from_coord(right, c_coord) for right, c_coord in support_coords(packet, modulus))
    )


def row_sums(packet: list[int], modulus: int) -> tuple[int, int, int]:
    return tuple(
        sum(packet[right * SQUARE_C : (right + 1) * SQUARE_C]) % modulus
        for right in range(RIGHT_DEGREE)
    )  # type: ignore[return-value]


def inversion_sum_values(packet: list[int], modulus: int) -> tuple[int, ...]:
    values: set[int] = set()
    for right in range(RIGHT_DEGREE):
        for c_coord in range(1, SQUARE_C):
            values.add(
                (
                    packet[right * SQUARE_C + c_coord]
                    + packet[
                        ((-right) % RIGHT_DEGREE) * SQUARE_C
                        + ((-c_coord) % SQUARE_C)
                    ]
                )
                % modulus
            )
    return tuple(sorted(values))


def unordered_off_pairs() -> list[tuple[Coord, Coord]]:
    pairs: list[tuple[Coord, Coord]] = []
    seen: set[frozenset[Coord]] = set()
    for right in range(RIGHT_DEGREE):
        for c_coord in range(1, SQUARE_C):
            coord = (right, c_coord)
            partner = inversion_coord(coord)
            key = frozenset((coord, partner))
            if key in seen:
                continue
            seen.add(key)
            pairs.append((coord, partner))
    return pairs


def bad_pairs(packet: list[int], modulus: int, target_sum: int = 0) -> list[tuple[Coord, Coord]]:
    out: list[tuple[Coord, Coord]] = []
    for coord, partner in unordered_off_pairs():
        value = (
            packet[coord[0] * SQUARE_C + coord[1]]
            + packet[partner[0] * SQUARE_C + partner[1]]
        ) % modulus
        if value != target_sum % modulus:
            out.append((coord, partner))
    return out


def anti_invariant(packet: list[int], modulus: int) -> bool:
    for right in range(RIGHT_DEGREE):
        for c_coord in range(SQUARE_C):
            partner = inversion_coord((right, c_coord))
            if (
                packet[right * SQUARE_C + c_coord]
                + packet[partner[0] * SQUARE_C + partner[1]]
            ) % modulus:
                return False
    return True


def pair_profiles() -> tuple[PairProfile, ...]:
    rows: list[PairProfile] = []
    for q_value in anomaly_orbit():
        coord = coord_from_q(q_value)
        partner = inversion_coord(coord)
        rows.append(
            PairProfile(
                anomaly_q=q_value,
                anomaly_coord=coord,
                partner_q=q_from_coord(*partner),
                partner_coord=partner,
            )
        )
    return tuple(rows)


def repair_profile(modulus_name: str, modulus: int) -> RepairProfile:
    pairs = pair_profiles()
    defect = packet_from_entries(
        [(row.anomaly_coord, -1) for row in pairs],
        modulus,
    )
    repair = packet_from_entries(
        [(row.partner_coord, 1) for row in pairs],
        modulus,
    )
    completed = add_packets(defect, repair, modulus)
    off_pairs = unordered_off_pairs()
    zero_bad_pairs = bad_pairs(defect, modulus, target_sum=0)
    minus_one_good_pairs = bad_pairs(defect, modulus, target_sum=modulus - 1)
    return RepairProfile(
        modulus_name=modulus_name,
        modulus=modulus,
        defect_support=support_coords(defect, modulus),
        repair_support=support_coords(repair, modulus),
        completed_support=support_coords(completed, modulus),
        completed_q_support=support_qs(completed, modulus),
        defect_degree=sum(defect) % modulus,
        completed_degree=sum(completed) % modulus,
        defect_row_sums=row_sums(defect, modulus),
        completed_row_sums=row_sums(completed, modulus),
        defect_inversion_sums=inversion_sum_values(defect, modulus),
        completed_inversion_sums=inversion_sum_values(completed, modulus),
        defect_value_conditions_ok=value_conditions_hold(defect, SQUARE_C, modulus),
        completed_value_conditions_ok=value_conditions_hold(completed, SQUARE_C, modulus),
        defect_raw_producer_ok=raw_producer_conditions(defect, SQUARE_C, modulus),
        completed_raw_producer_ok=raw_producer_conditions(completed, SQUARE_C, modulus),
        selected_defect_self=selected_defect(completed, SQUARE_C, modulus) == completed,
        anti_invariant=anti_invariant(completed, modulus),
        bad_pair_count=len(zero_bad_pairs),
        off_pair_count=len(off_pairs),
        target_zero_local_lower_bound=len(zero_bad_pairs),
        target_minus_one_lower_bound=len(minus_one_good_pairs),
    )


def main() -> int:
    print("p25 Lane B square-axis inversion-partner repair gate")
    print(f"square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    pairs = pair_profiles()
    print("inversion_partner_pairs")
    for row in pairs:
        print(
            f"  anomaly_q={row.anomaly_q} anomaly_coord={row.anomaly_coord} "
            f"partner_q={row.partner_q} partner_coord={row.partner_coord}"
        )

    expected_anomaly = ((0, 46), (1, 47), (2, 48))
    expected_repair = ((0, 123), (1, 121), (2, 122))
    expected_completed = (
        (0, 46),
        (0, 123),
        (1, 47),
        (1, 121),
        (2, 48),
        (2, 122),
    )
    expected_completed_qs = (25, 138, 197, 310, 369, 482)
    expected_pairs_ok = (
        tuple(row.anomaly_q for row in pairs) == tuple(anomaly_orbit())
        and tuple(row.anomaly_coord for row in pairs) == expected_anomaly
        and tuple(sorted(row.partner_coord for row in pairs)) == expected_repair
        and tuple(sorted(row.partner_q for row in pairs)) == (25, 197, 369)
    )

    field_rows = (
        ("quotient", split_prime_for(QUOTIENT_ORDER)),
        ("raw_split", split_prime_for(RAW_KERNEL_SIZE * QUOTIENT_ORDER)),
    )
    ok_rows = 0
    for modulus_name, modulus in field_rows:
        row = repair_profile(modulus_name, modulus)
        row_ok = (
            expected_pairs_ok
            and row.defect_support == expected_anomaly
            and row.repair_support == expected_repair
            and row.completed_support == expected_completed
            and row.completed_q_support == expected_completed_qs
            and row.defect_degree == modulus - 3
            and row.completed_degree == 0
            and row.defect_row_sums == (modulus - 1,) * RIGHT_DEGREE
            and row.completed_row_sums == (0, 0, 0)
            and row.defect_inversion_sums == (0, modulus - 1)
            and row.completed_inversion_sums == (0,)
            and not row.defect_value_conditions_ok
            and row.completed_value_conditions_ok
            and not row.defect_raw_producer_ok
            and row.completed_raw_producer_ok
            and row.selected_defect_self
            and row.anti_invariant
            and row.bad_pair_count == 3
            and row.off_pair_count == 252
            and row.target_zero_local_lower_bound == 3
            and row.target_minus_one_lower_bound == 249
        )
        ok_rows += int(row_ok)
        print(
            f"profile {row.modulus_name}: "
            f"modulus={row.modulus} "
            f"defect_support={list(row.defect_support)} "
            f"repair_support={list(row.repair_support)} "
            f"completed_q_support={list(row.completed_q_support)} "
            f"defect_degree={row.defect_degree} "
            f"completed_degree={row.completed_degree} "
            f"defect_row_sums={list(row.defect_row_sums)} "
            f"completed_row_sums={list(row.completed_row_sums)} "
            f"defect_inversion_sums={list(row.defect_inversion_sums)} "
            f"completed_inversion_sums={list(row.completed_inversion_sums)} "
            f"defect_value_conditions_ok={int(row.defect_value_conditions_ok)} "
            f"completed_value_conditions_ok={int(row.completed_value_conditions_ok)} "
            f"defect_raw_producer_ok={int(row.defect_raw_producer_ok)} "
            f"completed_raw_producer_ok={int(row.completed_raw_producer_ok)} "
            f"selected_defect_self={int(row.selected_defect_self)} "
            f"anti_invariant={int(row.anti_invariant)} "
            f"bad_pair_count={row.bad_pair_count}/{row.off_pair_count} "
            f"local_zero_completion_lower_bound={row.target_zero_local_lower_bound} "
            f"constant_minus_one_completion_lower_bound={row.target_minus_one_lower_bound} "
            f"ok={int(row_ok)}"
        )

    print("interpretation")
    print("  diagonal_anomaly_alone_fails_selected_defect_and_raw_producer=1")
    print("  inversion_partner_completion_is_six_point_degree_zero=1")
    print("  completed_row_is_anti_invariant_and_value_side_admissible=1")
    print("  local_completion_touches_one_partner_in_each_bad_inversion_pair=1")
    print("  producer_target_is_now_anomaly_plus_inversion_partner_slice=1")
    print(f"square_axis_inversion_partner_repair_rows={ok_rows}/{len(field_rows)}")
    print("conclusion=reported_p25_laneB_square_axis_inversion_partner_repair_gate")
    return 0 if ok_rows == len(field_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

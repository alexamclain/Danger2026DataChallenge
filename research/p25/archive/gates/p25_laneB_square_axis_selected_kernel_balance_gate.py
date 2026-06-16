#!/usr/bin/env python3
"""Selected-defect-kernel balance gate for the square-axis anomaly.

The scalar-balance escape used a global constant to make the visible
q-binomial anomaly degree zero.  The full selected-defect kernel is slightly
larger: functions that are constant in the C direction separately on each
right row.

This gate checks whether that larger row-constant kernel gives a useful local
repair.  It does not.  Degree zero can be achieved with one dense row plus the
two remaining anomaly points, so it is less dense than the global scalar, but
the selected-defect diagonal anomaly is unchanged.  Moreover a fixed inversion
pair witnesses failure of the raw producer contract for every row-constant
choice.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q
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


@dataclass(frozen=True)
class BalanceProfile:
    modulus_name: str
    modulus: int
    name: str
    row_constants: tuple[int, int, int]
    support: int
    raw_block_support: int
    degree: int
    selected_defect_unchanged: bool
    value_conditions_ok: bool
    raw_producer_ok: bool
    inversion_witness_delta: int


@dataclass(frozen=True)
class PatternProfile:
    pattern: tuple[str, str, str]
    exists: bool
    support_cost: int
    example_constants: tuple[int, int, int] | None


def negative_anomaly_packet(modulus: int) -> list[int]:
    packet = [0] * QUOTIENT_ORDER
    for q_value in anomaly_orbit():
        right, c_coord = coord_from_q(q_value)
        packet[right * SQUARE_C + c_coord] = modulus - 1
    return packet


def row_constant_packet(constants: tuple[int, int, int], modulus: int) -> list[int]:
    packet: list[int] = []
    for right in range(RIGHT_DEGREE):
        packet.extend([constants[right] % modulus] * SQUARE_C)
    return packet


def add_packets(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def support_size(packet: list[int], modulus: int) -> int:
    return sum(1 for value in packet if value % modulus)


def packet_degree(packet: list[int], modulus: int) -> int:
    return sum(packet) % modulus


def degree_zero_row_sum_target(modulus: int) -> int:
    return 3 * pow(SQUARE_C, -1, modulus) % modulus


def classify_support_cost(value: int | str) -> int:
    if value == "zero":
        return 1
    if value == "one":
        return SQUARE_C - 1
    return SQUARE_C


def pattern_examples(modulus: int) -> list[PatternProfile]:
    target = degree_zero_row_sum_target(modulus)
    profiles: list[PatternProfile] = []
    labels = ("zero", "one", "other")
    for pattern in product(labels, repeat=RIGHT_DEGREE):
        fixed = 0
        other_indices: list[int] = []
        constants = [0, 0, 0]
        for index, label in enumerate(pattern):
            if label == "zero":
                constants[index] = 0
            elif label == "one":
                constants[index] = 1
                fixed = (fixed + 1) % modulus
            else:
                other_indices.append(index)
        residual = (target - fixed) % modulus
        exists = False
        example: tuple[int, int, int] | None = None
        if not other_indices:
            exists = residual == 0
            example = tuple(constants) if exists else None  # type: ignore[assignment]
        elif len(other_indices) == 1:
            value = residual
            exists = value not in (0, 1)
            if exists:
                constants[other_indices[0]] = value
                example = tuple(constants)  # type: ignore[assignment]
        else:
            # The fields used here are large.  Find a small explicit assignment
            # for all but the last "other" slot and check the final one.
            trial_values = range(2, min(modulus, 32))
            for trial in product(trial_values, repeat=len(other_indices) - 1):
                candidate = constants[:]
                subtotal = fixed
                for index, value in zip(other_indices[:-1], trial):
                    candidate[index] = value
                    subtotal = (subtotal + value) % modulus
                last_value = (target - subtotal) % modulus
                if last_value not in (0, 1):
                    candidate[other_indices[-1]] = last_value
                    exists = True
                    example = tuple(candidate)  # type: ignore[assignment]
                    break
        profiles.append(
            PatternProfile(
                pattern=pattern,
                exists=exists,
                support_cost=sum(classify_support_cost(label) for label in pattern),
                example_constants=example,
            )
        )
    return profiles


def balance_profile(
    modulus_name: str,
    modulus: int,
    name: str,
    constants: tuple[int, int, int],
) -> BalanceProfile:
    anomaly = negative_anomaly_packet(modulus)
    row_constants = row_constant_packet(constants, modulus)
    packet = add_packets(anomaly, row_constants, modulus)
    defect = selected_defect(packet, SQUARE_C, modulus)
    anomaly_defect = selected_defect(anomaly, SQUARE_C, modulus)

    # This fixed pair is independent of the row constants:
    # (0,1)+(0,-1) has no anomaly, while (0,46)+(0,-46) includes one.
    generic_sum = (
        packet[0 * SQUARE_C + 1] + packet[0 * SQUARE_C + (SQUARE_C - 1)]
    ) % modulus
    anomaly_sum = (
        packet[0 * SQUARE_C + 46] + packet[0 * SQUARE_C + (SQUARE_C - 46)]
    ) % modulus
    witness_delta = (anomaly_sum - generic_sum) % modulus

    return BalanceProfile(
        modulus_name=modulus_name,
        modulus=modulus,
        name=name,
        row_constants=constants,
        support=support_size(packet, modulus),
        raw_block_support=RAW_KERNEL_SIZE * support_size(packet, modulus),
        degree=packet_degree(packet, modulus),
        selected_defect_unchanged=defect == anomaly_defect,
        value_conditions_ok=value_conditions_hold(defect, SQUARE_C, modulus),
        raw_producer_ok=raw_producer_conditions(packet, SQUARE_C, modulus),
        inversion_witness_delta=witness_delta,
    )


def main() -> int:
    print("p25 Lane B square-axis selected-kernel balance gate")
    print(f"square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    field_rows = (
        ("quotient", split_prime_for(QUOTIENT_ORDER)),
        ("raw_split", split_prime_for(RAW_KERNEL_SIZE * QUOTIENT_ORDER)),
    )
    total_ok = 0
    for modulus_name, modulus in field_rows:
        target = degree_zero_row_sum_target(modulus)
        scalar = 3 * pow(QUOTIENT_ORDER, -1, modulus) % modulus
        patterns = pattern_examples(modulus)
        existing = [profile for profile in patterns if profile.exists]
        min_cost = min(profile.support_cost for profile in existing)
        min_examples = [
            profile for profile in existing if profile.support_cost == min_cost
        ]
        row_min_constants = min_examples[0].example_constants
        if row_min_constants is None:
            raise AssertionError("missing row-minimum constants")
        profiles = [
            balance_profile(
                modulus_name,
                modulus,
                "global_scalar",
                (scalar, scalar, scalar),
            ),
            balance_profile(
                modulus_name,
                modulus,
                "row_minimum",
                row_min_constants,
            ),
            balance_profile(
                modulus_name,
                modulus,
                "cancel_one_anomaly_point",
                (1, 0, (target - 1) % modulus),
            ),
        ]
        row_ok = (
            min_cost == SQUARE_C + 2
            and len(min_examples) == 3
            and all(profile.degree == 0 for profile in profiles)
            and profiles[0].support == QUOTIENT_ORDER
            and profiles[1].support == SQUARE_C + 2
            and profiles[2].support == 2 * SQUARE_C
            and all(profile.selected_defect_unchanged for profile in profiles)
            and not any(profile.value_conditions_ok for profile in profiles)
            and not any(profile.raw_producer_ok for profile in profiles)
            and all(profile.inversion_witness_delta == modulus - 1 for profile in profiles)
        )
        total_ok += int(row_ok)
        print(
            f"field {modulus_name}: modulus={modulus} "
            f"row_sum_target={target} scalar={scalar} "
            f"existing_patterns={len(existing)}/27 "
            f"min_support={min_cost} "
            f"min_pattern_count={len(min_examples)} "
            f"min_patterns={[profile.pattern for profile in min_examples]} "
            f"ok={int(row_ok)}"
        )
        for profile in profiles:
            print(
                f"  balance {profile.name}: "
                f"row_constants={list(profile.row_constants)} "
                f"support={profile.support} "
                f"raw_block_support={profile.raw_block_support} "
                f"degree={profile.degree} "
                f"selected_defect_unchanged={int(profile.selected_defect_unchanged)} "
                f"value_conditions_ok={int(profile.value_conditions_ok)} "
                f"raw_producer_ok={int(profile.raw_producer_ok)} "
                f"inversion_witness_delta={profile.inversion_witness_delta} "
            )
    row_ok = total_ok == len(field_rows)
    print(f"square_axis_selected_kernel_balance_rows={total_ok}/{len(field_rows)}")
    print("interpretation")
    print("  selected_defect_kernel_is_row_constant_not_only_global_scalar=1")
    print("  degree_zero_row_constant_balance_can_reduce_support_to_one_dense_row_plus_two_points=1")
    print("  row_constant_balance_never_changes_the_visible_selected_defect_anomaly=1")
    print("  fixed_inversion_witness_rules_out_the_raw_producer_contract=1")
    print("conclusion=reported_p25_laneB_square_axis_selected_kernel_balance_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

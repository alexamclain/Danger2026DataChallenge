#!/usr/bin/env python3
"""p25 selected-defect value gate for the Lane B quotient targets.

This is the p25 specialization of the p24 fixed-frequency value-side gate.
It is finite linear algebra on C_right x C_c; it does not materialize a CM
packet.  Its job is to keep the next producer target honest:

    raw packet g
    selected defect f(r,c) = g(r,c) - g(r,0)

For p25 Lane B the quotient arithmetic points to right=3 with c=13 and c=53
as the first useful targets.  The square c=169 target is included as a larger
sanity row because it came from the same negative-trace skeleton.
"""

from __future__ import annotations

import random
from typing import Optional


RIGHT_DEGREE = 3
TARGET_C_DEGREES = (13, 53, 169)
TRIALS = 32
SEED = 20260612


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def split_prime_for(order: int) -> int:
    multiplier = 2
    while True:
        candidate = multiplier * order + 1
        if is_prime(candidate):
            return candidate
        multiplier += 1


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    mat = [row[:] for row in matrix if any(value % modulus for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % modulus, -1, modulus)
        mat[rank] = [(value * inv) % modulus for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % modulus
            if factor:
                mat[row] = [
                    (value - factor * pivot_value) % modulus
                    for value, pivot_value in zip(mat[row], mat[rank])
                ]
        rank += 1
    return rank


def selected_defect(raw: list[int], c_degree: int, field_q: int) -> list[int]:
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        base = raw[right * c_degree]
        for c_index in range(c_degree):
            out.append((raw[right * c_degree + c_index] - base) % field_q)
    return out


def c_row_sums_independent(row: list[int], c_degree: int, field_q: int) -> bool:
    row_sums = [
        sum(row[right * c_degree : (right + 1) * c_degree]) % field_q
        for right in range(RIGHT_DEGREE)
    ]
    return all(value == row_sums[0] for value in row_sums)


def c_zero_fiber_vanishes(row: list[int], c_degree: int, field_q: int) -> bool:
    return all(row[right * c_degree] % field_q == 0 for right in range(RIGHT_DEGREE))


def inversion_constant_off_c_zero(row: list[int], c_degree: int, field_q: int) -> bool:
    constant: Optional[int] = None
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            value = (
                row[right * c_degree + c_index]
                + row[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
            ) % field_q
            if constant is None:
                constant = value
            elif value != constant:
                return False
    return constant is not None


def value_conditions_hold(row: list[int], c_degree: int, field_q: int) -> bool:
    return (
        c_row_sums_independent(row, c_degree, field_q)
        and c_zero_fiber_vanishes(row, c_degree, field_q)
        and inversion_constant_off_c_zero(row, c_degree, field_q)
    )


def value_condition_rows(c_degree: int, field_q: int) -> list[list[int]]:
    width = RIGHT_DEGREE * c_degree
    rows: list[list[int]] = []

    def row_with(entries: list[tuple[int, int]]) -> list[int]:
        row = [0] * width
        for column, value in entries:
            row[column] = (row[column] + value) % field_q
        return row

    for right in range(1, RIGHT_DEGREE):
        entries: list[tuple[int, int]] = []
        for c_index in range(c_degree):
            entries.append((right * c_degree + c_index, 1))
            entries.append((c_index, -1))
        rows.append(row_with(entries))

    for right in range(RIGHT_DEGREE):
        rows.append(row_with([(right * c_degree, 1)]))

    base_entries = [
        (1, 1),
        (((-0) % RIGHT_DEGREE) * c_degree + ((-1) % c_degree), 1),
    ]
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            if right == 0 and c_index == 1:
                continue
            entries = [
                (right * c_degree + c_index, 1),
                (((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree), 1),
            ]
            for column, value in base_entries:
                entries.append((column, -value))
            rows.append(row_with(entries))

    return rows


def expected_constraint_count(c_degree: int) -> int:
    return (
        (RIGHT_DEGREE - 1)
        + RIGHT_DEGREE * ((c_degree - 1) // 2)
        + ((RIGHT_DEGREE - 1) // 2)
    )


def raw_two_level_inversion_complement(
    raw: list[int], c_degree: int, field_q: int
) -> bool:
    off_constant: Optional[int] = None
    zero_constant: Optional[int] = None
    for right in range(RIGHT_DEGREE):
        zero_value = (
            raw[right * c_degree]
            + raw[((-right) % RIGHT_DEGREE) * c_degree]
        ) % field_q
        if zero_constant is None:
            zero_constant = zero_value
        elif zero_value != zero_constant:
            return False

        for c_index in range(1, c_degree):
            value = (
                raw[right * c_degree + c_index]
                + raw[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
            ) % field_q
            if off_constant is None:
                off_constant = value
            elif value != off_constant:
                return False
    return off_constant is not None and zero_constant is not None


def raw_selected_affine_row_balance(
    raw: list[int], c_degree: int, field_q: int
) -> bool:
    balances = []
    for right in range(RIGHT_DEGREE):
        row = raw[right * c_degree : (right + 1) * c_degree]
        balances.append((sum(row) - c_degree * row[0]) % field_q)
    return all(value == balances[0] for value in balances)


def raw_producer_conditions(raw: list[int], c_degree: int, field_q: int) -> bool:
    return raw_two_level_inversion_complement(
        raw, c_degree, field_q
    ) and raw_selected_affine_row_balance(raw, c_degree, field_q)


def random_raw(width: int, field_q: int, rng: random.Random) -> list[int]:
    return [rng.randrange(field_q) for _ in range(width)]


def force_two_level_inversion(
    c_degree: int, field_q: int, rng: random.Random
) -> list[int]:
    raw = [0] * (RIGHT_DEGREE * c_degree)
    zero_constant = rng.randrange(field_q)
    off_constant = rng.randrange(field_q)
    seen: set[tuple[int, int]] = set()
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_degree):
            if (right, c_index) in seen:
                continue
            partner = ((-right) % RIGHT_DEGREE, (-c_index) % c_degree)
            seen.add((right, c_index))
            seen.add(partner)
            constant = zero_constant if c_index == 0 else off_constant
            if partner == (right, c_index):
                raw[right * c_degree + c_index] = constant * pow(2, -1, field_q) % field_q
            else:
                value = rng.randrange(field_q)
                raw[right * c_degree + c_index] = value
                raw[partner[0] * c_degree + partner[1]] = (constant - value) % field_q
    return raw


def force_affine_balance(
    c_degree: int, field_q: int, rng: random.Random
) -> list[int]:
    raw = random_raw(RIGHT_DEGREE * c_degree, field_q, rng)
    target = rng.randrange(field_q)
    for right in range(RIGHT_DEGREE):
        row_start = right * c_degree
        current = (
            sum(raw[row_start : row_start + c_degree])
            - c_degree * raw[row_start]
        ) % field_q
        delta = (target - current) % field_q
        raw[row_start + 1] = (raw[row_start + 1] + delta) % field_q
    return raw


def force_both_conditions(
    c_degree: int, field_q: int, rng: random.Random
) -> list[int]:
    raw = [0] * (RIGHT_DEGREE * c_degree)
    off_constant = rng.randrange(field_q)
    row_defect_sum = rng.randrange(field_q)

    seen: set[tuple[int, int]] = set()
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            if (right, c_index) in seen:
                continue
            partner = ((-right) % RIGHT_DEGREE, (-c_index) % c_degree)
            seen.add((right, c_index))
            seen.add(partner)
            value = rng.randrange(field_q)
            raw[right * c_degree + c_index] = value
            raw[partner[0] * c_degree + partner[1]] = (off_constant - value) % field_q

    seen_right: set[int] = set()
    zero_constant: Optional[int] = None
    inv = pow(c_degree - 1, -1, field_q)
    for right in range(RIGHT_DEGREE):
        if right in seen_right:
            continue
        partner_right = (-right) % RIGHT_DEGREE
        seen_right.add(right)
        seen_right.add(partner_right)
        off_sum_right = sum(raw[right * c_degree + 1 : (right + 1) * c_degree]) % field_q
        base_right = (off_sum_right - row_defect_sum) * inv % field_q
        raw[right * c_degree] = base_right

        if partner_right == right:
            zero_constant = (2 * base_right) % field_q
            continue

        off_sum_partner = sum(
            raw[partner_right * c_degree + 1 : (partner_right + 1) * c_degree]
        ) % field_q
        base_partner = (off_sum_partner - row_defect_sum) * inv % field_q
        raw[partner_right * c_degree] = base_partner
        pair_constant = (base_right + base_partner) % field_q
        if zero_constant is None:
            zero_constant = pair_constant
        elif pair_constant != zero_constant:
            raise AssertionError("forced zero complement drifted")

    if not raw_producer_conditions(raw, c_degree, field_q):
        raise AssertionError("failed to force raw producer conditions")
    return raw


def main() -> int:
    rng = random.Random(SEED)
    rows_checked = 0
    rank_matches = 0
    equivalence_rows = 0
    forced_rows = 0
    selected_only_rows = 0
    inversion_only_rows = 0
    affine_only_rows = 0

    print("p25 selected-defect value gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in TARGET_C_DEGREES:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        width = RIGHT_DEGREE * c_degree
        value_rows = value_condition_rows(c_degree, field_q)
        value_rank = rank_mod(value_rows, field_q)
        expected_rank = expected_constraint_count(c_degree)
        expected_dim = width - expected_rank
        rank_ok = int(value_rank == expected_rank)

        equivalence_trials = 0
        forced_hits = 0
        selected_only_controls = 0
        inversion_only_controls = 0
        affine_only_controls = 0

        for _ in range(TRIALS):
            raw = random_raw(width, field_q, rng)
            defect = selected_defect(raw, c_degree, field_q)
            equivalence_trials += int(
                raw_producer_conditions(raw, c_degree, field_q)
                == value_conditions_hold(defect, c_degree, field_q)
            )
            selected_only_controls += int(
                c_zero_fiber_vanishes(defect, c_degree, field_q)
                and not value_conditions_hold(defect, c_degree, field_q)
            )

            raw_inversion = force_two_level_inversion(c_degree, field_q, rng)
            defect_inversion = selected_defect(raw_inversion, c_degree, field_q)
            inversion_only_controls += int(
                raw_two_level_inversion_complement(raw_inversion, c_degree, field_q)
                and not raw_selected_affine_row_balance(raw_inversion, c_degree, field_q)
                and c_zero_fiber_vanishes(defect_inversion, c_degree, field_q)
                and inversion_constant_off_c_zero(defect_inversion, c_degree, field_q)
                and not c_row_sums_independent(defect_inversion, c_degree, field_q)
            )

            raw_affine = force_affine_balance(c_degree, field_q, rng)
            defect_affine = selected_defect(raw_affine, c_degree, field_q)
            affine_only_controls += int(
                raw_selected_affine_row_balance(raw_affine, c_degree, field_q)
                and not raw_two_level_inversion_complement(raw_affine, c_degree, field_q)
                and c_zero_fiber_vanishes(defect_affine, c_degree, field_q)
                and c_row_sums_independent(defect_affine, c_degree, field_q)
                and not inversion_constant_off_c_zero(defect_affine, c_degree, field_q)
            )

            raw_both = force_both_conditions(c_degree, field_q, rng)
            defect_both = selected_defect(raw_both, c_degree, field_q)
            forced_hits += int(
                raw_producer_conditions(raw_both, c_degree, field_q)
                and value_conditions_hold(defect_both, c_degree, field_q)
            )

        equivalence_ok = int(equivalence_trials == TRIALS)
        forced_ok = int(forced_hits == TRIALS)
        selected_only_ok = int(selected_only_controls == TRIALS)
        inversion_only_ok = int(inversion_only_controls == TRIALS)
        affine_only_ok = int(affine_only_controls == TRIALS)

        rank_matches += rank_ok
        equivalence_rows += equivalence_ok
        forced_rows += forced_ok
        selected_only_rows += selected_only_ok
        inversion_only_rows += inversion_only_ok
        affine_only_rows += affine_only_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"width={width} value_condition_rank={value_rank} "
            f"expected_rank={expected_rank} expected_dimension={expected_dim} "
            f"rank_ok={rank_ok} "
            f"producer_equivalence={equivalence_trials}/{TRIALS} "
            f"forced_raw_producer_hits={forced_hits}/{TRIALS} "
            f"selected_defect_only_controls={selected_only_controls}/{TRIALS} "
            f"inversion_only_controls={inversion_only_controls}/{TRIALS} "
            f"affine_only_controls={affine_only_controls}/{TRIALS} "
            f"equivalence_ok={equivalence_ok} forced_ok={forced_ok} "
            f"selected_only_ok={selected_only_ok} "
            f"inversion_only_ok={inversion_only_ok} "
            f"affine_only_ok={affine_only_ok}"
        )

    print(f"rank_matches={rank_matches}/{rows_checked}")
    print(f"selected_defect_producer_equivalence={equivalence_rows}/{rows_checked}")
    print(f"forced_raw_producer_hits={forced_rows}/{rows_checked}")
    print(f"selected_defect_only_controls={selected_only_rows}/{rows_checked}")
    print(f"inversion_only_controls={inversion_only_rows}/{rows_checked}")
    print(f"affine_only_controls={affine_only_rows}/{rows_checked}")
    print("interpretation")
    print("  p25_value_gate_is_right3_specialization_of_p24_selected_defect_gate=1")
    print("  selected_defect_target_is_raw_complement_plus_affine_balance=1")
    print("  C3xC13_is_the_first_materialized_packet_falsifier=1")
    print("  C3xC53_is_the_clean_prime_axis_followup=1")
    print("conclusion=reported_p25_selected_defect_value_gate")

    if rank_matches != rows_checked:
        return 1
    if equivalence_rows != rows_checked:
        return 1
    if forced_rows != rows_checked:
        return 1
    if selected_only_rows != rows_checked:
        return 1
    if inversion_only_rows != rows_checked:
        return 1
    if affine_only_rows != rows_checked:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

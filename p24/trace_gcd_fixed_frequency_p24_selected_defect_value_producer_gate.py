#!/usr/bin/env python3
"""Selected-defect producer criterion for the p24 value-side identities.

Let g(r,c) be a raw packet on C_7 x C_c, and let

    f(r,c) = g(r,c) - g(r,0)

be the selected-child defect packet.  Then f(r,0)=0 automatically.  The two
remaining value-side identities for f are equivalent to raw identities for g:

  * two-level inversion complement:
      g(r,c)+g(-r,-c) is constant for c != 0, and
      g(r,0)+g(-r,0) is constant on the C-zero fiber;

  * selected affine row balance:
      sum_c g(r,c) - c*g(r,0) is independent of r.

This gate checks the equivalence and supplies controls showing that selected
defect alone, inversion complement alone, and affine balance alone are each
insufficient.
"""

from __future__ import annotations

import random

from trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate import (
    RIGHT_DEGREE,
    P24_C_DEGREE,
    SMALL_C_DEGREES,
    c_row_sums_independent,
    c_zero_fiber_vanishes,
    inversion_constant_off_c_zero,
    value_conditions_hold,
)
from trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary import split_prime_for


TRIALS = 24
SEED = 20260607


def selected_defect(raw: list[int], c_degree: int, field_q: int) -> list[int]:
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        base = raw[right * c_degree]
        for c_index in range(c_degree):
            out.append((raw[right * c_degree + c_index] - base) % field_q)
    return out


def raw_two_level_inversion_complement(
    raw: list[int], c_degree: int, field_q: int
) -> bool:
    off_constant: int | None = None
    zero_constant: int | None = None
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


def root_of_order(order: int, field_q: int) -> int:
    for candidate in range(2, field_q):
        root = pow(candidate, (field_q - 1) // order, field_q)
        if root != 1 and pow(root, order, field_q) == 1:
            return root
    raise RuntimeError(f"no root of order {order} in F_{field_q}")


def right_projected_degree_zero(
    packet: list[int], c_degree: int, field_q: int
) -> bool:
    """KL/Robert finite shadow: nontrivial right projections have C-sum zero."""
    omega = root_of_order(RIGHT_DEGREE, field_q)
    row_sums = [
        sum(packet[right * c_degree : (right + 1) * c_degree]) % field_q
        for right in range(RIGHT_DEGREE)
    ]
    for character in range(1, RIGHT_DEGREE):
        total = 0
        for right, row_sum in enumerate(row_sums):
            weight = pow(omega, (-character * right) % RIGHT_DEGREE, field_q)
            total = (total + weight * row_sum) % field_q
        if total:
            return False
    return True


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
        # Adjust one nonzero C entry; this changes the affine balance by delta.
        delta = (target - current) % field_q
        raw[row_start + 1] = (raw[row_start + 1] + delta) % field_q
    return raw


def force_both_conditions(
    c_degree: int, field_q: int, rng: random.Random
) -> list[int]:
    # Start with an off-fiber constant complement and C-zero constant zero.
    # Then choose row bases so the selected defect has equal row sums.
    raw = [0] * (RIGHT_DEGREE * c_degree)
    off_constant = rng.randrange(field_q)
    row_defect_sum = rng.randrange(field_q)

    # Fill off-zero inversion pairs with arbitrary values summing to off_constant.
    seen: set[tuple[int, int]] = set()
    for right in range(RIGHT_DEGREE):
        for c_index in range(1, c_degree):
            if (right, c_index) in seen:
                continue
            partner = ((-right) % RIGHT_DEGREE, (-c_index) % c_degree)
            seen.add((right, c_index))
            seen.add(partner)
            if partner == (right, c_index):
                raw[right * c_degree + c_index] = off_constant * pow(2, -1, field_q) % field_q
            else:
                value = rng.randrange(field_q)
                raw[right * c_degree + c_index] = value
                raw[partner[0] * c_degree + partner[1]] = (off_constant - value) % field_q

    # Choose C-zero entries in inversion pairs so both the zero complement is
    # constant and the selected affine row balance equals row_defect_sum.
    # Adjusting row base b changes affine balance by -c*b plus b already in sum,
    # i.e. by -(c-1)*b relative to off-zero sum.
    seen_right: set[int] = set()
    for right in range(RIGHT_DEGREE):
        if right in seen_right:
            continue
        partner_right = (-right) % RIGHT_DEGREE
        seen_right.add(right)
        seen_right.add(partner_right)
        off_sum_right = sum(raw[right * c_degree + 1 : (right + 1) * c_degree]) % field_q
        off_sum_partner = sum(
            raw[partner_right * c_degree + 1 : (partner_right + 1) * c_degree]
        ) % field_q
        inv = pow(c_degree - 1, -1, field_q)
        base_right = (off_sum_right - row_defect_sum) * inv % field_q
        base_partner = (off_sum_partner - row_defect_sum) * inv % field_q
        # The off-zero complement construction forces off sums in paired rows
        # to make these bases sum to a constant independent of the pair.
        raw[right * c_degree] = base_right
        raw[partner_right * c_degree] = base_partner
    return raw


def main() -> None:
    rng = random.Random(SEED)
    rows_checked = 0
    equivalence_rows = 0
    forced_both_rows = 0
    selected_defect_only_controls = 0
    inversion_only_controls = 0
    affine_only_controls = 0
    kl_degree_zero_rows = 0
    affine_degree_zero_rows = 0
    inversion_not_degree_zero_rows = 0

    print("Trace-GCD fixed-frequency p24 selected-defect value producer gate")
    print(f"right_degree={RIGHT_DEGREE}")

    for c_degree in SMALL_C_DEGREES[:3]:
        field_q = split_prime_for(RIGHT_DEGREE * c_degree)
        width = RIGHT_DEGREE * c_degree
        equivalence_trials = 0
        random_hits = 0
        defect_only_failures = 0
        inversion_only_failures = 0
        affine_only_failures = 0
        kl_degree_zero_equivalence = 0
        affine_degree_zero_hits = 0
        inversion_not_degree_zero_hits = 0
        forced_hits = 0

        for _ in range(TRIALS):
            raw = random_raw(width, field_q, rng)
            defect = selected_defect(raw, c_degree, field_q)
            producer = raw_producer_conditions(raw, c_degree, field_q)
            target = value_conditions_hold(defect, c_degree, field_q)
            equivalence_trials += int(producer == target)
            random_hits += int(target)
            kl_degree_zero_equivalence += int(
                right_projected_degree_zero(defect, c_degree, field_q)
                == c_row_sums_independent(defect, c_degree, field_q)
            )

            raw_inversion = force_two_level_inversion(c_degree, field_q, rng)
            defect_inversion = selected_defect(raw_inversion, c_degree, field_q)
            inversion_only_failures += int(
                raw_two_level_inversion_complement(raw_inversion, c_degree, field_q)
                and not raw_selected_affine_row_balance(raw_inversion, c_degree, field_q)
                and c_zero_fiber_vanishes(defect_inversion, c_degree, field_q)
                and inversion_constant_off_c_zero(defect_inversion, c_degree, field_q)
                and not c_row_sums_independent(defect_inversion, c_degree, field_q)
            )
            inversion_not_degree_zero_hits += int(
                raw_two_level_inversion_complement(raw_inversion, c_degree, field_q)
                and not right_projected_degree_zero(
                    defect_inversion, c_degree, field_q
                )
            )

            raw_affine = force_affine_balance(c_degree, field_q, rng)
            defect_affine = selected_defect(raw_affine, c_degree, field_q)
            affine_only_failures += int(
                raw_selected_affine_row_balance(raw_affine, c_degree, field_q)
                and not raw_two_level_inversion_complement(raw_affine, c_degree, field_q)
                and c_zero_fiber_vanishes(defect_affine, c_degree, field_q)
                and c_row_sums_independent(defect_affine, c_degree, field_q)
                and not inversion_constant_off_c_zero(defect_affine, c_degree, field_q)
            )
            affine_degree_zero_hits += int(
                raw_selected_affine_row_balance(raw_affine, c_degree, field_q)
                and right_projected_degree_zero(defect_affine, c_degree, field_q)
            )

            defect_only = selected_defect(raw, c_degree, field_q)
            defect_only_failures += int(
                c_zero_fiber_vanishes(defect_only, c_degree, field_q)
                and not value_conditions_hold(defect_only, c_degree, field_q)
            )

            raw_both = force_both_conditions(c_degree, field_q, rng)
            defect_both = selected_defect(raw_both, c_degree, field_q)
            forced_hits += int(
                raw_producer_conditions(raw_both, c_degree, field_q)
                and value_conditions_hold(defect_both, c_degree, field_q)
            )

        equivalence_ok = int(equivalence_trials == TRIALS and random_hits == 0)
        forced_ok = int(forced_hits == TRIALS)
        defect_only_ok = int(defect_only_failures == TRIALS)
        inversion_only_ok = int(inversion_only_failures == TRIALS)
        affine_only_ok = int(affine_only_failures == TRIALS)
        kl_degree_zero_ok = int(kl_degree_zero_equivalence == TRIALS)
        affine_degree_zero_ok = int(affine_degree_zero_hits == TRIALS)
        inversion_not_degree_zero_ok = int(inversion_not_degree_zero_hits == TRIALS)

        equivalence_rows += equivalence_ok
        forced_both_rows += forced_ok
        selected_defect_only_controls += defect_only_ok
        inversion_only_controls += inversion_only_ok
        affine_only_controls += affine_only_ok
        kl_degree_zero_rows += kl_degree_zero_ok
        affine_degree_zero_rows += affine_degree_zero_ok
        inversion_not_degree_zero_rows += inversion_not_degree_zero_ok
        rows_checked += 1

        print(
            "row "
            f"c_degree={c_degree} field_q={field_q} "
            f"equivalence_trials={equivalence_trials}/{TRIALS} "
            f"random_target_hits={random_hits}/{TRIALS} "
            f"forced_both_hits={forced_hits}/{TRIALS} "
            f"selected_defect_only_control={defect_only_failures}/{TRIALS} "
            f"inversion_only_control={inversion_only_failures}/{TRIALS} "
            f"affine_only_control={affine_only_failures}/{TRIALS} "
            f"kl_degree_zero_equivalence={kl_degree_zero_equivalence}/{TRIALS} "
            f"affine_degree_zero_hits={affine_degree_zero_hits}/{TRIALS} "
            f"inversion_not_degree_zero_hits={inversion_not_degree_zero_hits}/{TRIALS} "
            f"equivalence_ok={equivalence_ok} "
            f"forced_ok={forced_ok} "
            f"defect_only_ok={defect_only_ok} "
            f"inversion_only_ok={inversion_only_ok} "
            f"affine_only_ok={affine_only_ok} "
            f"kl_degree_zero_ok={kl_degree_zero_ok} "
            f"affine_degree_zero_ok={affine_degree_zero_ok} "
            f"inversion_not_degree_zero_ok={inversion_not_degree_zero_ok}"
        )

    print(f"selected_defect_producer_equivalence={equivalence_rows}/{rows_checked}")
    print(f"forced_raw_producer_hits={forced_both_rows}/{rows_checked}")
    print(f"selected_defect_only_controls={selected_defect_only_controls}/{rows_checked}")
    print(f"inversion_only_controls={inversion_only_controls}/{rows_checked}")
    print(f"affine_only_controls={affine_only_controls}/{rows_checked}")
    print(f"kl_degree_zero_equiv_row_balance={kl_degree_zero_rows}/{rows_checked}")
    print(f"affine_balance_forces_kl_degree_zero={affine_degree_zero_rows}/{rows_checked}")
    print(
        "inversion_complement_does_not_force_kl_degree_zero="
        f"{inversion_not_degree_zero_rows}/{rows_checked}"
    )
    print(f"p24_c_degree={P24_C_DEGREE}")
    print("interpretation")
    print("  selected_defect_automatically_gives_C_zero_fiber=1")
    print("  kl_robert_degree_zero_shadow_is_row_sum_independence=1")
    print("  raw_two_level_inversion_plus_selected_affine_balance_iff_value_identities=1")
    print("  raw_inversion_without_affine_balance_leaks_row_sums=1")
    print("  raw_affine_balance_without_inversion_leaks_structural_symmetry=1")
    print("  robert_reciprocity_must_supply_more_than_degree_zero_for_full_value_identity=1")
    print("  selected_defect_producer_target_is_raw_complement_plus_affine_balance=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate")

    if equivalence_rows != rows_checked:
        raise SystemExit(1)
    if forced_both_rows != rows_checked:
        raise SystemExit(1)
    if selected_defect_only_controls != rows_checked:
        raise SystemExit(1)
    if inversion_only_controls != rows_checked:
        raise SystemExit(1)
    if affine_only_controls != rows_checked:
        raise SystemExit(1)
    if kl_degree_zero_rows != rows_checked:
        raise SystemExit(1)
    if affine_degree_zero_rows != rows_checked:
        raise SystemExit(1)
    if inversion_not_degree_zero_rows != rows_checked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

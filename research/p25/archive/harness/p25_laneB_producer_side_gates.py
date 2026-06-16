#!/usr/bin/env python3
"""Producer-side finite gates for the p25 Lane B moonshot.

The p25 quotient and selected-defect gates identify the packet target.  This
file ports the producer-facing p24 checks to the p25 right-3 quotients:

1. additive raw identities <=> multiplicative product-formula identities;
2. the single degenerate-anchor correction has the expected selected-defect
   fingerprint;
3. a full cyclic unramified character, if supplied by arithmetic, descends
   exactly to the post-B quotient and is determined by the rho/axis values.

These are necessary finite contracts, not a construction of the missing
selected weighted packet Y[e].
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    c_row_sums_independent,
    c_zero_fiber_vanishes,
    force_affine_balance,
    force_both_conditions,
    force_two_level_inversion,
    inversion_constant_off_c_zero,
    raw_producer_conditions,
    raw_selected_affine_row_balance,
    raw_two_level_inversion_complement,
    random_raw,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


TRIALS = 24
SEED = 20260612


@dataclass(frozen=True)
class ProducerCase:
    name: str
    c_axis: int
    b_trace: int
    raw_order: int


CASES = (
    ProducerCase("tiny_C3xC13", 13, 325, 12675),
    ProducerCase("prime_axis_C3xC53", 53, 25, 3975),
    ProducerCase("square_axis_C3xC169", 169, 25, 12675),
)


def factor(n: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def primitive_root(modulus: int) -> int:
    phi = modulus - 1
    factors = factor(phi)
    for candidate in range(2, modulus):
        if all(pow(candidate, phi // prime, modulus) != 1 for prime in factors):
            return candidate
    raise RuntimeError(f"no primitive root for {modulus}")


def torus_root(exponent_modulus: int) -> tuple[int, int]:
    torus_field = split_prime_for(exponent_modulus)
    root = primitive_root(torus_field)
    omega = pow(root, (torus_field - 1) // exponent_modulus, torus_field)
    if omega == 1 or pow(omega, exponent_modulus, torus_field) != 1:
        raise RuntimeError("failed to construct torus root")
    return torus_field, omega


def exponentiate(
    raw: list[int], exponent_modulus: int, torus_field: int, omega: int
) -> list[int]:
    return [pow(omega, value % exponent_modulus, torus_field) for value in raw]


def multiplicative_two_level_complement(
    values: list[int], c_degree: int, torus_field: int
) -> bool:
    zero_constant = None
    off_constant = None
    for right in range(RIGHT_DEGREE):
        zero_value = (
            values[right * c_degree]
            * values[((-right) % RIGHT_DEGREE) * c_degree]
        ) % torus_field
        if zero_constant is None:
            zero_constant = zero_value
        elif zero_value != zero_constant:
            return False

        for c_index in range(1, c_degree):
            value = (
                values[right * c_degree + c_index]
                * values[((-right) % RIGHT_DEGREE) * c_degree + ((-c_index) % c_degree)]
            ) % torus_field
            if off_constant is None:
                off_constant = value
            elif value != off_constant:
                return False
    return zero_constant is not None and off_constant is not None


def multiplicative_selected_row_ratio(
    values: list[int], c_degree: int, torus_field: int
) -> bool:
    ratios: list[int] = []
    for right in range(RIGHT_DEGREE):
        product = 1
        for c_index in range(c_degree):
            product = product * values[right * c_degree + c_index] % torus_field
        denominator = pow(values[right * c_degree], c_degree, torus_field)
        ratios.append(product * pow(denominator, -1, torus_field) % torus_field)
    return all(value == ratios[0] for value in ratios)


def multiplicative_producer_conditions(
    raw: list[int],
    c_degree: int,
    exponent_modulus: int,
    torus_field: int,
    omega: int,
) -> bool:
    values = exponentiate(raw, exponent_modulus, torus_field, omega)
    return multiplicative_two_level_complement(
        values, c_degree, torus_field
    ) and multiplicative_selected_row_ratio(values, c_degree, torus_field)


def multiplicative_dictionary_row(case: ProducerCase, rng: random.Random) -> dict[str, int]:
    exponent_modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    torus_field, omega = torus_root(exponent_modulus)
    width = RIGHT_DEGREE * case.c_axis
    equivalence_trials = 0
    random_hits = 0
    forced_hits = 0
    inversion_only_controls = 0
    affine_only_controls = 0

    for _ in range(TRIALS):
        raw = random_raw(width, exponent_modulus, rng)
        additive = raw_producer_conditions(raw, case.c_axis, exponent_modulus)
        multiplicative = multiplicative_producer_conditions(
            raw, case.c_axis, exponent_modulus, torus_field, omega
        )
        equivalence_trials += int(additive == multiplicative)
        random_hits += int(multiplicative)

        raw_both = force_both_conditions(case.c_axis, exponent_modulus, rng)
        forced_hits += int(
            raw_producer_conditions(raw_both, case.c_axis, exponent_modulus)
            and multiplicative_producer_conditions(
                raw_both, case.c_axis, exponent_modulus, torus_field, omega
            )
        )

        raw_inversion = force_inversion_only(case.c_axis, exponent_modulus, rng)
        inversion_values = exponentiate(
            raw_inversion, exponent_modulus, torus_field, omega
        )
        inversion_only_controls += int(
            raw_two_level_inversion_complement(
                raw_inversion, case.c_axis, exponent_modulus
            )
            and multiplicative_two_level_complement(
                inversion_values, case.c_axis, torus_field
            )
            and not raw_selected_affine_row_balance(
                raw_inversion, case.c_axis, exponent_modulus
            )
            and not multiplicative_selected_row_ratio(
                inversion_values, case.c_axis, torus_field
            )
        )

        raw_affine = force_affine_only(case.c_axis, exponent_modulus, rng)
        affine_values = exponentiate(raw_affine, exponent_modulus, torus_field, omega)
        affine_only_controls += int(
            raw_selected_affine_row_balance(raw_affine, case.c_axis, exponent_modulus)
            and multiplicative_selected_row_ratio(
                affine_values, case.c_axis, torus_field
            )
            and not raw_two_level_inversion_complement(
                raw_affine, case.c_axis, exponent_modulus
            )
            and not multiplicative_two_level_complement(
                affine_values, case.c_axis, torus_field
            )
        )

    return {
        "exponent_modulus": exponent_modulus,
        "torus_field": torus_field,
        "equivalence_trials": equivalence_trials,
        "random_hits": random_hits,
        "forced_hits": forced_hits,
        "inversion_only_controls": inversion_only_controls,
        "affine_only_controls": affine_only_controls,
    }


def force_inversion_only(c_degree: int, modulus: int, rng: random.Random) -> list[int]:
    for _ in range(1000):
        raw = force_two_level_inversion(c_degree, modulus, rng)
        if not raw_selected_affine_row_balance(raw, c_degree, modulus):
            return raw
    raise RuntimeError("could not produce inversion-only control")


def force_affine_only(c_degree: int, modulus: int, rng: random.Random) -> list[int]:
    for _ in range(1000):
        raw = force_affine_balance(c_degree, modulus, rng)
        if not raw_two_level_inversion_complement(raw, c_degree, modulus):
            return raw
    raise RuntimeError("could not produce affine-only control")


def raw_anchor_correction(c_degree: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_degree)
    values[0] = (-1) % modulus
    return values


def punctured_right_zero_row(c_degree: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_degree)
    for c_index in range(1, c_degree):
        values[c_index] = 1 % modulus
    return values


def right_difference_profile_ok(values: list[int], c_degree: int, modulus: int) -> bool:
    punctured = [0] + [1 % modulus] * (c_degree - 1)
    negative_punctured = [(-value) % modulus for value in punctured]
    for right in range(RIGHT_DEGREE):
        diff = [
            (
                values[((right + 1) % RIGHT_DEGREE) * c_degree + c_index]
                - values[right * c_degree + c_index]
            )
            % modulus
            for c_index in range(c_degree)
        ]
        if right == 0:
            expected = negative_punctured
        elif right == RIGHT_DEGREE - 1:
            expected = punctured
        else:
            expected = [0] * c_degree
        if diff != expected:
            return False
    return True


def anchor_fingerprint_row(case: ProducerCase) -> dict[str, int]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    raw = raw_anchor_correction(case.c_axis, modulus)
    defect = selected_defect(raw, case.c_axis, modulus)
    expected = punctured_right_zero_row(case.c_axis, modulus)
    return {
        "modulus": modulus,
        "selected_defect_ok": int(defect == expected),
        "support_size": sum(1 for value in defect if value % modulus),
        "expected_support": case.c_axis - 1,
        "c_zero": int(c_zero_fiber_vanishes(defect, case.c_axis, modulus)),
        "row_sums": int(c_row_sums_independent(defect, case.c_axis, modulus)),
        "inversion": int(inversion_constant_off_c_zero(defect, case.c_axis, modulus)),
        "all_value_identities": int(value_conditions_hold(defect, case.c_axis, modulus)),
        "right_difference": int(right_difference_profile_ok(defect, case.c_axis, modulus)),
    }


def axis_decomposition(case: ProducerCase) -> tuple[int, int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    for right_power in range(RIGHT_DEGREE):
        for c_power in range(case.c_axis):
            if (case.c_axis * right_power + RIGHT_DEGREE * c_power) % quotient_order == 1:
                return right_power, c_power
    raise AssertionError("no axis decomposition")


def unramified_selector_row(case: ProducerCase) -> dict[str, int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    if case.raw_order != quotient_order * case.b_trace:
        raise AssertionError("raw order does not match quotient*B")
    quotient_exponent = case.b_trace
    kernel_generator_exponent = quotient_order
    right_axis_step = case.c_axis
    c_axis_step = RIGHT_DEGREE
    quotient_character_exponents = {
        (quotient_exponent * a_value) % case.raw_order
        for a_value in range(quotient_order)
    }
    right_power, c_power = axis_decomposition(case)

    pair_checks = 0
    same_axis_iff_same_character = 1
    for a_value in range(quotient_order):
        for b_value in range(quotient_order):
            same_axes = (
                (a_value * right_axis_step - b_value * right_axis_step)
                % quotient_order
                == 0
                and (a_value * c_axis_step - b_value * c_axis_step)
                % quotient_order
                == 0
            )
            same_character = (a_value - b_value) % quotient_order == 0
            if same_axes != same_character:
                same_axis_iff_same_character = 0
            pair_checks += 1

    coordinates = {
        (case.c_axis * right + RIGHT_DEGREE * c_index) % quotient_order
        for right in range(RIGHT_DEGREE)
        for c_index in range(case.c_axis)
    }

    return {
        "raw_order": case.raw_order,
        "bc_kernel_order": case.b_trace,
        "post_b_quotient_order": quotient_order,
        "quotient_twist_exponent": quotient_exponent,
        "quotient_twist_order": case.raw_order // gcd(case.raw_order, quotient_exponent),
        "quotient_twist_trivial_on_b_kernel": int(
            (quotient_exponent * kernel_generator_exponent) % case.raw_order == 0
        ),
        "quotient_twist_right_axis_order": case.raw_order
        // gcd(case.raw_order, quotient_exponent * right_axis_step),
        "quotient_twist_c_axis_order": case.raw_order
        // gcd(case.raw_order, quotient_exponent * c_axis_step),
        "quotient_character_exponents_count": len(quotient_character_exponents),
        "quotient_character_exponents_are_trace_survivors": int(
            quotient_character_exponents
            == {
                exponent
                for exponent in range(case.raw_order)
                if exponent % case.b_trace == 0
            }
        ),
        "coordinate_exponents_cover_modulus": int(len(coordinates) == quotient_order),
        "rho_from_right_axis_power": right_power,
        "rho_from_c_axis_power": c_power,
        "bezout_reconstructs_rho": int(
            (case.c_axis * right_power + RIGHT_DEGREE * c_power) % quotient_order == 1
        ),
        "axis_values_determine_character_pair_checks": pair_checks,
        "same_axis_values_iff_same_character": same_axis_iff_same_character,
        "unramified_twist_supplies_post_b_selector": 1,
        "unramified_twist_alone_supplies_embedded_packet": 0,
    }


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def main() -> int:
    rng = random.Random(SEED)
    multiplicative_ok = 0
    anchor_ok = 0
    selector_ok = 0

    print("p25 Lane B producer-side gates")
    print(f"right_degree={RIGHT_DEGREE}")

    for case in CASES:
        mult = multiplicative_dictionary_row(case, rng)
        mult_ok = int(
            mult["equivalence_trials"] == TRIALS
            and mult["random_hits"] == 0
            and mult["forced_hits"] == TRIALS
            and mult["inversion_only_controls"] == TRIALS
            and mult["affine_only_controls"] == TRIALS
        )
        multiplicative_ok += mult_ok
        print(
            "multiplicative_row "
            f"name={case.name} c={case.c_axis} "
            f"exponent_modulus={mult['exponent_modulus']} "
            f"torus_field={mult['torus_field']} "
            f"equivalence={mult['equivalence_trials']}/{TRIALS} "
            f"random_hits={mult['random_hits']}/{TRIALS} "
            f"forced={mult['forced_hits']}/{TRIALS} "
            f"inversion_only={mult['inversion_only_controls']}/{TRIALS} "
            f"affine_only={mult['affine_only_controls']}/{TRIALS} ok={mult_ok}"
        )

        anchor = anchor_fingerprint_row(case)
        anchor_row_ok = int(
            anchor["selected_defect_ok"]
            and anchor["support_size"] == anchor["expected_support"]
            and anchor["c_zero"]
            and not anchor["all_value_identities"]
            and anchor["right_difference"]
        )
        anchor_ok += anchor_row_ok
        print(
            "anchor_row "
            f"name={case.name} c={case.c_axis} modulus={anchor['modulus']} "
            f"support={anchor['support_size']}/{anchor['expected_support']} "
            f"selected_defect_ok={anchor['selected_defect_ok']} "
            f"c_zero={anchor['c_zero']} row_sums={anchor['row_sums']} "
            f"inversion={anchor['inversion']} "
            f"all_value_identities={anchor['all_value_identities']} "
            f"right_difference={anchor['right_difference']} ok={anchor_row_ok}"
        )

        selector = unramified_selector_row(case)
        selector_row_ok = int(
            selector["quotient_twist_order"] == selector["post_b_quotient_order"]
            and selector["quotient_twist_trivial_on_b_kernel"]
            and selector["quotient_twist_right_axis_order"] == RIGHT_DEGREE
            and selector["quotient_twist_c_axis_order"] == case.c_axis
            and selector["quotient_character_exponents_count"]
            == selector["post_b_quotient_order"]
            and selector["quotient_character_exponents_are_trace_survivors"]
            and selector["coordinate_exponents_cover_modulus"]
            and selector["bezout_reconstructs_rho"]
            and selector["same_axis_values_iff_same_character"]
        )
        selector_ok += selector_row_ok
        print(
            "selector_row "
            f"name={case.name} raw_order={selector['raw_order']} "
            f"B={selector['bc_kernel_order']} "
            f"quotient={selector['post_b_quotient_order']} "
            f"twist_order={selector['quotient_twist_order']} "
            f"right_axis_order={selector['quotient_twist_right_axis_order']} "
            f"c_axis_order={selector['quotient_twist_c_axis_order']} "
            f"rho_axis_powers=({selector['rho_from_right_axis_power']},"
            f"{selector['rho_from_c_axis_power']}) "
            f"trace_survivors={selector['quotient_character_exponents_are_trace_survivors']} "
            f"axis_determines={selector['same_axis_values_iff_same_character']} "
            f"embedded_packet_from_twist={selector['unramified_twist_alone_supplies_embedded_packet']} "
            f"ok={selector_row_ok}"
        )

    rows = len(CASES)
    print(f"multiplicative_dictionary_rows={multiplicative_ok}/{rows}")
    print(f"single_anchor_fingerprint_rows={anchor_ok}/{rows}")
    print(f"unramified_selector_rows={selector_ok}/{rows}")
    print("interpretation")
    print("  product_formula_producer_target_matches_p25_additive_gate=1")
    print("  single_anchor_correction_has_expected_punctured_right_zero_fingerprint=1")
    print("  anchor_alone_is_not_the_full_value_identity=1")
    print("  unramified_character_selector_can_supply_post_B_quotient_axes=1")
    print("  remaining_missing_object_is_embedded_selected_weighted_packet_Y=1")
    print("conclusion=reported_p25_laneB_producer_side_gates")

    if multiplicative_ok != rows:
        return 1
    if anchor_ok != rows:
        return 1
    if selector_ok != rows:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

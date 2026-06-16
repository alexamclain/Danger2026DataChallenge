#!/usr/bin/env python3
"""Packet-inversion boundary for the fixed-frequency product-sum target.

After class-character expansion, the p24 order-7 target has the form

    sum_a L_a R_{-a} = 0.

The relative packet is stable under inversion `a -> -a`, and it is tempting
to hope that Hermitian/inversion symmetry alone cancels the sum.  This finite
gate records the exact algebraic issue: inversion symmetry pairs the terms,
but it does not cancel them unless the two paired factors have opposite
parity.  Generic inversion-even packets keep every product term nonzero and
the total sum nonzero.
"""

from __future__ import annotations

import random


Q = 421
RELATIVE = 5
PACKET = (1, 2, 3, 4)
PAIRS = ((1, 4), (2, 3))


def random_nonzero(rng: random.Random) -> int:
    value = 0
    while value == 0:
        value = rng.randrange(Q)
    return value


def product_sum(left: dict[int, int], right: dict[int, int]) -> int:
    return sum(left[a] * right[(-a) % RELATIVE] for a in PACKET) % Q


def nonzero_product_terms(left: dict[int, int], right: dict[int, int]) -> int:
    return sum(int(left[a] * right[(-a) % RELATIVE] % Q != 0) for a in PACKET)


def random_packet(rng: random.Random) -> tuple[dict[int, int], dict[int, int]]:
    return (
        {a: random_nonzero(rng) for a in PACKET},
        {a: random_nonzero(rng) for a in PACKET},
    )


def inversion_even_packet(rng: random.Random) -> tuple[dict[int, int], dict[int, int]]:
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    for a, neg_a in PAIRS:
        left_value = random_nonzero(rng)
        right_value = random_nonzero(rng)
        left[a] = left[neg_a] = left_value
        right[a] = right[neg_a] = right_value
    return left, right


def paired_multiplier_packet(rng: random.Random) -> tuple[dict[int, int], dict[int, int]]:
    # This models the most general paired symmetry whose left and right
    # multipliers multiply to +1 on each inversion pair.  The paired
    # contribution doubles instead of canceling.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    for a, neg_a in PAIRS:
        alpha = random_nonzero(rng)
        left_a = random_nonzero(rng)
        right_neg_a = random_nonzero(rng)
        left[a] = left_a
        left[neg_a] = alpha * left_a % Q
        right[neg_a] = right_neg_a
        right[a] = pow(alpha, -1, Q) * right_neg_a % Q
    return left, right


def anti_inversion_packet(rng: random.Random) -> tuple[dict[int, int], dict[int, int]]:
    # A sufficient but extra sign: left is even and right is odd under
    # inversion, so every pair cancels.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    for a, neg_a in PAIRS:
        left_value = random_nonzero(rng)
        right_value = random_nonzero(rng)
        left[a] = left[neg_a] = left_value
        right[a] = right_value
        right[neg_a] = -right_value % Q
    return left, right


def termwise_right_zero_packet(rng: random.Random) -> tuple[dict[int, int], dict[int, int]]:
    left = {a: random_nonzero(rng) for a in PACKET}
    right = {a: 0 for a in PACKET}
    return left, right


def count_nonzero(factory, trials: int, rng: random.Random) -> tuple[int, int]:
    nonzero_sums = 0
    all_terms_nonzero = 0
    for _ in range(trials):
        # Avoid accidental zero sums when the point of the model is a
        # structural nonzero control; this keeps the output deterministic
        # without turning the script into a probability experiment.
        for _attempt in range(100):
            left, right = factory(rng)
            value = product_sum(left, right)
            if value != 0 or factory in (anti_inversion_packet, termwise_right_zero_packet):
                break
        nonzero_sums += int(product_sum(left, right) != 0)
        all_terms_nonzero += int(nonzero_product_terms(left, right) == len(PACKET))
    return nonzero_sums, all_terms_nonzero


def main() -> None:
    rng = random.Random(20260606)
    trials = 16
    random_nonzero_sums, random_all_terms = count_nonzero(random_packet, trials, rng)
    even_nonzero_sums, even_all_terms = count_nonzero(inversion_even_packet, trials, rng)
    paired_nonzero_sums, paired_all_terms = count_nonzero(paired_multiplier_packet, trials, rng)
    anti_nonzero_sums, anti_all_terms = count_nonzero(anti_inversion_packet, trials, rng)
    termwise_nonzero_sums, termwise_all_terms = count_nonzero(termwise_right_zero_packet, trials, rng)

    print("Trace-GCD fixed-frequency packet-inversion boundary")
    print(f"field_q={Q}")
    print(f"relative={RELATIVE}")
    print(f"packet={list(PACKET)}")
    print(f"inversion_pairs={PAIRS}")
    print(f"trials={trials}")
    print(f"random_packet_nonzero_sums={random_nonzero_sums}/{trials}")
    print(f"random_packet_all_terms_nonzero={random_all_terms}/{trials}")
    print(f"inversion_even_nonzero_sums={even_nonzero_sums}/{trials}")
    print(f"inversion_even_all_terms_nonzero={even_all_terms}/{trials}")
    print(f"paired_multiplier_product_plus_one_nonzero_sums={paired_nonzero_sums}/{trials}")
    print(f"paired_multiplier_product_plus_one_all_terms_nonzero={paired_all_terms}/{trials}")
    print(f"anti_inversion_nonzero_sums={anti_nonzero_sums}/{trials}")
    print(f"anti_inversion_all_terms_nonzero={anti_all_terms}/{trials}")
    print(f"termwise_right_zero_nonzero_sums={termwise_nonzero_sums}/{trials}")
    print(f"termwise_right_zero_all_terms_nonzero={termwise_all_terms}/{trials}")
    print("interpretation")
    print("  packet_inversion_symmetry_pairs_terms_but_does_not_cancel_them=1")
    print("  paired_multiplier_product_plus_one_is_not_enough=1")
    print("  anti_inversion_parity_would_be_sufficient_extra_structure=1")
    print("  termwise_right_combo_vanishing_would_be_sufficient_extra_structure=1")
    print("  p24_packet_cancellation_needs_more_than_hermitian_packet_stability=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_packet_inversion_boundary")

    if random_nonzero_sums != trials or random_all_terms != trials:
        raise SystemExit(1)
    if even_nonzero_sums != trials or even_all_terms != trials:
        raise SystemExit(1)
    if paired_nonzero_sums != trials or paired_all_terms != trials:
        raise SystemExit(1)
    if anti_nonzero_sums != 0 or anti_all_terms != trials:
        raise SystemExit(1)
    if termwise_nonzero_sums != 0 or termwise_all_terms != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

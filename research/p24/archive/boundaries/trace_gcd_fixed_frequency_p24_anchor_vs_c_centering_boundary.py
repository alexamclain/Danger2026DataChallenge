#!/usr/bin/env python3
"""Boundary between trace-defect anchors and C/E-centering.

The recombined anchor for one right quotient character is the nontrivial
right-spectrum vanishing of

    D_q = Tr_relative(packet)_q - |internal| * selected_q.

The bidegree/internal-trace target is different: after B/C trace, the
nontrivial right channels should have no trivial C/E component.  In quotient
coordinates this says the full internal trace profile itself has no
nontrivial right component.

This gate checks, in the exact p24 quotient dimensions C_7 x C_179 x C_31,
that selected-section subtraction can mask a forbidden bidegree.  Therefore
the proof cannot be "the trace defect is centered, hence the C/E-trivial
component is gone" unless it also controls the selected child right profile.
"""

from __future__ import annotations

import random


FIELD_Q = 43  # 43 - 1 is divisible by 7; char is prime to 31 and 179.
RIGHT_DEGREE = 7
C_DEGREE = 179
B_OVER_C_DEGREE = 31
INTERNAL_SIZE = C_DEGREE * B_OVER_C_DEGREE
SEED = 20260607
TRIALS = 32


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def nontrivial_right_spectrum_zero(profile: list[int], omega7: int) -> bool:
    for character in range(1, RIGHT_DEGREE):
        total = 0
        for index, value in enumerate(profile):
            total = (
                total
                + value * pow(omega7, (-character * index) % RIGHT_DEGREE, FIELD_Q)
            ) % FIELD_Q
        if total:
            return False
    return True


def is_constant(profile: list[int]) -> bool:
    return all(value == profile[0] for value in profile)


def random_profile(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _index in range(RIGHT_DEGREE)]


def nonconstant_profile(rng: random.Random) -> list[int]:
    while True:
        profile = random_profile(rng)
        if not is_constant(profile):
            return profile


def trace_defect(full_trace: list[int], selected: list[int]) -> list[int]:
    return [
        (full - INTERNAL_SIZE * child) % FIELD_Q
        for full, child in zip(full_trace, selected)
    ]


def make_packet_with_profiles(
    full_trace: list[int],
    selected: list[int],
) -> list[list[list[int]]]:
    packet = [
        [[0 for _b in range(B_OVER_C_DEGREE)] for _c in range(C_DEGREE)]
        for _q in range(RIGHT_DEGREE)
    ]
    for q_index, (full, child) in enumerate(zip(full_trace, selected)):
        packet[q_index][0][0] = child % FIELD_Q
        packet[q_index][0][1] = (full - child) % FIELD_Q
    return packet


def full_internal_trace(packet: list[list[list[int]]]) -> list[int]:
    return [
        sum(
            packet[q_index][c_index][b_index]
            for c_index in range(C_DEGREE)
            for b_index in range(B_OVER_C_DEGREE)
        )
        % FIELD_Q
        for q_index in range(RIGHT_DEGREE)
    ]


def selected_profile(packet: list[list[list[int]]]) -> list[int]:
    return [packet[q_index][0][0] for q_index in range(RIGHT_DEGREE)]


def main() -> None:
    root = primitive_root(FIELD_Q)
    omega7 = pow(root, (FIELD_Q - 1) // RIGHT_DEGREE, FIELD_Q)
    rng = random.Random(SEED)

    random_anchor_pass_bidegree_pass = 0
    random_anchor_fail_bidegree_fail = 0
    forced_anchor_pass_bidegree_fail = 0
    forced_bidegree_pass_anchor_fail = 0
    forced_both_pass = 0
    packet_realization_failures = 0

    for _trial in range(TRIALS):
        full = random_profile(rng)
        selected = random_profile(rng)
        defect = trace_defect(full, selected)
        anchor_pass = nontrivial_right_spectrum_zero(defect, omega7)
        bidegree_pass = nontrivial_right_spectrum_zero(full, omega7)
        random_anchor_pass_bidegree_pass += int(anchor_pass and bidegree_pass)
        random_anchor_fail_bidegree_fail += int((not anchor_pass) and (not bidegree_pass))

        # Force anchor pass by setting full = |internal|*selected + constant.
        selected_bad = nonconstant_profile(rng)
        constant = rng.randrange(FIELD_Q)
        full_bad = [(INTERNAL_SIZE * value + constant) % FIELD_Q for value in selected_bad]
        packet = make_packet_with_profiles(full_bad, selected_bad)
        packet_realization_failures += int(full_internal_trace(packet) != full_bad)
        packet_realization_failures += int(selected_profile(packet) != selected_bad)
        defect_bad = trace_defect(full_internal_trace(packet), selected_profile(packet))
        forced_anchor_pass_bidegree_fail += int(
            nontrivial_right_spectrum_zero(defect_bad, omega7)
            and not nontrivial_right_spectrum_zero(full_internal_trace(packet), omega7)
        )

        # Force bidegree pass with a constant full trace but nonconstant selected child.
        selected_leaky = nonconstant_profile(rng)
        full_constant = [rng.randrange(FIELD_Q)] * RIGHT_DEGREE
        defect_leaky = trace_defect(full_constant, selected_leaky)
        forced_bidegree_pass_anchor_fail += int(
            nontrivial_right_spectrum_zero(full_constant, omega7)
            and not nontrivial_right_spectrum_zero(defect_leaky, omega7)
        )

        selected_good = [rng.randrange(FIELD_Q)] * RIGHT_DEGREE
        full_good = [rng.randrange(FIELD_Q)] * RIGHT_DEGREE
        forced_both_pass += int(
            nontrivial_right_spectrum_zero(full_good, omega7)
            and nontrivial_right_spectrum_zero(trace_defect(full_good, selected_good), omega7)
        )

    print("Trace-GCD fixed-frequency p24 anchor-vs-C-centering boundary")
    print(f"field_q={FIELD_Q}")
    print(f"omega7={omega7}")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"c_degree={C_DEGREE}")
    print(f"b_over_c_degree={B_OVER_C_DEGREE}")
    print(f"internal_size={INTERNAL_SIZE}")
    print(f"internal_size_mod_field={INTERNAL_SIZE % FIELD_Q}")
    print(f"packet_realization_failures={packet_realization_failures}")
    print(f"random_anchor_and_bidegree_both_pass={random_anchor_pass_bidegree_pass}/{TRIALS}")
    print(f"random_anchor_and_bidegree_both_fail={random_anchor_fail_bidegree_fail}/{TRIALS}")
    print(f"forced_anchor_pass_bidegree_fail={forced_anchor_pass_bidegree_fail}/{TRIALS}")
    print(f"forced_bidegree_pass_anchor_fail={forced_bidegree_pass_anchor_fail}/{TRIALS}")
    print(f"forced_anchor_and_bidegree_both_pass={forced_both_pass}/{TRIALS}")
    print("interpretation")
    print("  trace_defect_anchor_zero_does_not_imply_C_trivial_bidegree_zero=1")
    print("  C_trivial_bidegree_zero_does_not_imply_trace_defect_anchor_zero=1")
    print("  selected_section_subtraction_can_mask_forbidden_bidegree=1")
    print("  proof_must_control_selected_child_right_profile_or_C_centering=1")
    print("  anchor_and_C_centering_are_distinct_arithmetic_inputs=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_anchor_vs_c_centering_boundary")

    if packet_realization_failures:
        raise SystemExit(1)
    if random_anchor_pass_bidegree_pass:
        raise SystemExit(1)
    if random_anchor_fail_bidegree_fail != TRIALS:
        raise SystemExit(1)
    if forced_anchor_pass_bidegree_fail != TRIALS:
        raise SystemExit(1)
    if forced_bidegree_pass_anchor_fail != TRIALS:
        raise SystemExit(1)
    if forced_both_pass != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

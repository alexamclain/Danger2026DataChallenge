#!/usr/bin/env python3
"""Bidegree support gate for the p24 right/C-character frontier.

After B/C trace the remaining packet lives on

    right quotient C_7  x  internal C/E quotient C_179.

The final C/E trace of a nontrivial right quotient projector is exactly the
trivial C-character bidegree of that right channel.  Thus the current theorem
is the vanishing of the six bidegrees

    (right character k, C-character 0),  k=1,...,6.

This gate checks the finite algebra in a C_7 x C_5 toy model and records the
important p24 warning: since gcd(7,179)=1, a nontrivial right-to-C character
graph is not a group-homomorphism artifact.  If the actual packet avoids the
trivial C-character in nontrivial right channels, that must come from the
trace-GCD weighted/section-aware CM packet.
"""

from __future__ import annotations

import random
from math import gcd


FIELD_Q = 211
RIGHT_DEGREE = 7
TOY_C_DEGREE = 5
P24_C_DEGREE = 179
SEED = 20260607
TRIALS = 48


Matrix = list[list[int]]


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


def zero_matrix() -> Matrix:
    return [[0 for _c in range(TOY_C_DEGREE)] for _r in range(RIGHT_DEGREE)]


def add_matrix(left: Matrix, right: Matrix) -> Matrix:
    return [
        [(a + b) % FIELD_Q for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def sub_matrix(left: Matrix, right: Matrix) -> Matrix:
    return [
        [(a - b) % FIELD_Q for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def scale_matrix(scalar: int, matrix: Matrix) -> Matrix:
    return [[scalar * value % FIELD_Q for value in row] for row in matrix]


def is_zero_matrix(matrix: Matrix) -> bool:
    return all(value % FIELD_Q == 0 for row in matrix for value in row)


def is_zero_vector(values: list[int]) -> bool:
    return all(value % FIELD_Q == 0 for value in values)


def random_matrix(rng: random.Random) -> Matrix:
    return [
        [rng.randrange(FIELD_Q) for _c in range(TOY_C_DEGREE)]
        for _r in range(RIGHT_DEGREE)
    ]


def pure_character_matrix(right_index: int, c_index: int, omega7: int, omega_c: int) -> Matrix:
    return [
        [
            pow(omega7, right_index * r % RIGHT_DEGREE, FIELD_Q)
            * pow(omega_c, c_index * c % TOY_C_DEGREE, FIELD_Q)
            % FIELD_Q
            for c in range(TOY_C_DEGREE)
        ]
        for r in range(RIGHT_DEGREE)
    ]


def right_projector(matrix: Matrix, omega7: int, right_index: int) -> Matrix:
    inv = pow(RIGHT_DEGREE, -1, FIELD_Q)
    out = zero_matrix()
    for target in range(RIGHT_DEGREE):
        for source in range(RIGHT_DEGREE):
            weight = pow(
                omega7,
                (-right_index * (source - target)) % RIGHT_DEGREE,
                FIELD_Q,
            )
            for c in range(TOY_C_DEGREE):
                out[target][c] = (out[target][c] + inv * weight * matrix[source][c]) % FIELD_Q
    return out


def c_projector(matrix: Matrix, omega_c: int, c_index: int) -> Matrix:
    inv = pow(TOY_C_DEGREE, -1, FIELD_Q)
    out = zero_matrix()
    for r in range(RIGHT_DEGREE):
        for target in range(TOY_C_DEGREE):
            for source in range(TOY_C_DEGREE):
                weight = pow(
                    omega_c,
                    (-c_index * (source - target)) % TOY_C_DEGREE,
                    FIELD_Q,
                )
                out[r][target] = (out[r][target] + inv * weight * matrix[r][source]) % FIELD_Q
    return out


def bidegree_projector(matrix: Matrix, omega7: int, omega_c: int, right_index: int, c_index: int) -> Matrix:
    return c_projector(right_projector(matrix, omega7, right_index), omega_c, c_index)


def c_trace_after_right_projector(matrix: Matrix, omega7: int, right_index: int) -> list[int]:
    projected = right_projector(matrix, omega7, right_index)
    return [sum(row) % FIELD_Q for row in projected]


def remove_forbidden_bidegrees(matrix: Matrix, omega7: int, omega_c: int) -> Matrix:
    adjusted = [row[:] for row in matrix]
    for right_index in range(1, RIGHT_DEGREE):
        adjusted = sub_matrix(
            adjusted,
            bidegree_projector(adjusted, omega7, omega_c, right_index, 0),
        )
    return adjusted


def all_nontrivial_right_final_traces_zero(matrix: Matrix, omega7: int) -> bool:
    return all(
        is_zero_vector(c_trace_after_right_projector(matrix, omega7, right_index))
        for right_index in range(1, RIGHT_DEGREE)
    )


def all_forbidden_bidegrees_zero(matrix: Matrix, omega7: int, omega_c: int) -> bool:
    return all(
        is_zero_matrix(bidegree_projector(matrix, omega7, omega_c, right_index, 0))
        for right_index in range(1, RIGHT_DEGREE)
    )


def graph_supported_packet(omega7: int, omega_c: int) -> Matrix:
    packet = zero_matrix()
    for right_index in range(1, RIGHT_DEGREE):
        c_index = 1 + ((right_index - 1) % (TOY_C_DEGREE - 1))
        packet = add_matrix(
            packet,
            pure_character_matrix(right_index, c_index, omega7, omega_c),
        )
    return packet


def trivial_c_supported_packet(omega7: int, omega_c: int) -> Matrix:
    packet = zero_matrix()
    for right_index in range(1, RIGHT_DEGREE):
        packet = add_matrix(
            packet,
            pure_character_matrix(right_index, 0, omega7, omega_c),
        )
    return packet


def main() -> None:
    root = primitive_root(FIELD_Q)
    omega7 = pow(root, (FIELD_Q - 1) // RIGHT_DEGREE, FIELD_Q)
    omega_c = pow(root, (FIELD_Q - 1) // TOY_C_DEGREE, FIELD_Q)
    rng = random.Random(SEED)

    projector_commutation_failures = 0
    final_trace_iff_bidegree_failures = 0
    random_packets_with_trivial_c_leakage = 0
    forced_no_trivial_c_bidegree_passes = 0

    for _trial in range(TRIALS):
        matrix = random_matrix(rng)
        for right_index in range(1, RIGHT_DEGREE):
            for c_index in range(TOY_C_DEGREE):
                left = c_projector(
                    right_projector(matrix, omega7, right_index),
                    omega_c,
                    c_index,
                )
                right = right_projector(
                    c_projector(matrix, omega_c, c_index),
                    omega7,
                    right_index,
                )
                projector_commutation_failures += int(left != right)

        final_zero = all_nontrivial_right_final_traces_zero(matrix, omega7)
        forbidden_zero = all_forbidden_bidegrees_zero(matrix, omega7, omega_c)
        final_trace_iff_bidegree_failures += int(final_zero != forbidden_zero)
        random_packets_with_trivial_c_leakage += int(not final_zero)

        forced = remove_forbidden_bidegrees(matrix, omega7, omega_c)
        forced_no_trivial_c_bidegree_passes += int(
            all_nontrivial_right_final_traces_zero(forced, omega7)
            and all_forbidden_bidegrees_zero(forced, omega7, omega_c)
        )

    graph_packet = graph_supported_packet(omega7, omega_c)
    trivial_packet = trivial_c_supported_packet(omega7, omega_c)
    graph_support_passes = int(all_nontrivial_right_final_traces_zero(graph_packet, omega7))
    graph_support_nonzero = int(not is_zero_matrix(graph_packet))
    trivial_c_leaks = int(not all_nontrivial_right_final_traces_zero(trivial_packet, omega7))
    trivial_c_forbidden_nonzero = sum(
        int(not is_zero_matrix(bidegree_projector(trivial_packet, omega7, omega_c, right_index, 0)))
        for right_index in range(1, RIGHT_DEGREE)
    )

    print("Trace-GCD fixed-frequency p24 right/C bidegree support gate")
    print(f"field_q={FIELD_Q}")
    print(f"omega7={omega7}")
    print(f"omega_c={omega_c}")
    print(f"toy_right_degree={RIGHT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"p24_C_degree={P24_C_DEGREE}")
    print(f"toy_gcd_C7_C5={gcd(RIGHT_DEGREE, TOY_C_DEGREE)}")
    print(f"p24_gcd_C7_C179={gcd(RIGHT_DEGREE, P24_C_DEGREE)}")
    print(f"bidegree_projector_commutation_failures={projector_commutation_failures}")
    print(f"final_trace_iff_no_trivial_C_bidegree_failures={final_trace_iff_bidegree_failures}")
    print(f"random_packets_with_trivial_C_leakage={random_packets_with_trivial_c_leakage}/{TRIALS}")
    print(f"forced_no_trivial_C_bidegree_passes={forced_no_trivial_c_bidegree_passes}/{TRIALS}")
    print(f"graph_nontrivial_C_support_final_trace_zero={graph_support_passes}")
    print(f"graph_nontrivial_C_support_nonzero={graph_support_nonzero}")
    print(f"trivial_C_support_leaks={trivial_c_leaks}")
    print(f"trivial_C_forbidden_bidegrees_nonzero={trivial_c_forbidden_nonzero}/6")
    print("interpretation")
    print("  final_internal_trace_zero_is_absence_of_right_nontrivial_C_trivial_bidegrees=1")
    print("  nontrivial_C_bidegree_support_is_sufficient_for_projector_trace_zero=1")
    print("  p24_has_no_nontrivial_group_hom_from_C7_to_C179=1")
    print("  bidegree_support_separation_must_come_from_weighted_packet_not_group_hom=1")
    print("  remaining_theorem_is_vanishing_of_right_nontrivial_C_trivial_bidegrees=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_c_bidegree_support_gate")

    if gcd(RIGHT_DEGREE, TOY_C_DEGREE) != 1 or gcd(RIGHT_DEGREE, P24_C_DEGREE) != 1:
        raise SystemExit(1)
    if projector_commutation_failures or final_trace_iff_bidegree_failures:
        raise SystemExit(1)
    if random_packets_with_trivial_c_leakage != TRIALS:
        raise SystemExit(1)
    if forced_no_trivial_c_bidegree_passes != TRIALS:
        raise SystemExit(1)
    if not graph_support_passes or not graph_support_nonzero:
        raise SystemExit(1)
    if not trivial_c_leaks or trivial_c_forbidden_nonzero != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

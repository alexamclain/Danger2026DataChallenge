#!/usr/bin/env python3
"""Internal-trace equivalence for the p24 matching right coboundary.

The obstruction gate shows that formal right-character covariance lands in the
epsilon eigenspace of sigma, so it is not itself a matching coboundary.  This
gate records the positive replacement in a cyclic model with the p24 shape

    raw order = 7 * 179 * 31.

For an epsilon-quotient right packet, membership in

    im(sigma - epsilon)

is equivalent to vanishing of the nested internal trace obstruction.  Thus a
noncircular proof may proceed by proving the nested internal trace vanishes
from CM/Lang packet structure, then applying the explicit Hilbert-90 inverse.
The inverse step is formal only after the independent internal-trace identity.
"""

from __future__ import annotations

import random


FIELD_Q = 43
ORDER7 = 7
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3
TOY_INTERNAL_DEGREE = TOY_C_DEGREE * TOY_B_OVER_C_DEGREE
TOY_TOTAL_DEGREE = ORDER7 * TOY_INTERNAL_DEGREE
SEED = 20260606


Vector = list[int]


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


def add(left: Vector, right: Vector) -> Vector:
    return [(a + b) % FIELD_Q for a, b in zip(left, right)]


def sub(left: Vector, right: Vector) -> Vector:
    return [(a - b) % FIELD_Q for a, b in zip(left, right)]


def scalar_mul(scalar: int, vector: Vector) -> Vector:
    return [(scalar * value) % FIELD_Q for value in vector]


def sigma(vector: Vector, power: int = 1) -> Vector:
    shift = power % len(vector)
    if shift == 0:
        return vector[:]
    return vector[-shift:] + vector[:-shift]


def zero() -> Vector:
    return [0] * TOY_TOTAL_DEGREE


def is_zero(vector: Vector) -> bool:
    return all(value % FIELD_Q == 0 for value in vector)


def trace_over_powers(vector: Vector, step: int, count: int) -> Vector:
    out = zero()
    for index in range(count):
        out = add(out, sigma(vector, step * index))
    return out


def trace_b_over_c(vector: Vector) -> Vector:
    return trace_over_powers(
        vector,
        ORDER7 * TOY_C_DEGREE,
        TOY_B_OVER_C_DEGREE,
    )


def trace_c_over_e(vector: Vector) -> Vector:
    return trace_over_powers(vector, ORDER7, TOY_C_DEGREE)


def nested_internal_trace(vector: Vector) -> Vector:
    return trace_c_over_e(trace_b_over_c(vector))


def direct_internal_trace(vector: Vector) -> Vector:
    return trace_over_powers(vector, ORDER7, TOY_INTERNAL_DEGREE)


def full_twisted_trace(vector: Vector, epsilon: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_epsilon = pow(epsilon, -1, FIELD_Q)
    for index in range(TOY_TOTAL_DEGREE):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_epsilon % FIELD_Q
    return out


def quotient_twisted_trace(vector: Vector, epsilon: int) -> Vector:
    out = zero()
    coeff = 1
    inverse_epsilon = pow(epsilon, -1, FIELD_Q)
    for index in range(ORDER7):
        out = add(out, scalar_mul(coeff, sigma(vector, index)))
        coeff = coeff * inverse_epsilon % FIELD_Q
    return out


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if rows[row][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, q)
        rows[rank] = [value * inv % q for value in rows[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
    return rank


def coboundary_matrix(epsilon: int) -> list[list[int]]:
    columns: list[Vector] = []
    for index in range(TOY_TOTAL_DEGREE):
        basis = zero()
        basis[index] = 1
        columns.append(sub(sigma(basis), scalar_mul(epsilon, basis)))
    return [
        [columns[col][row] for col in range(TOY_TOTAL_DEGREE)]
        for row in range(TOY_TOTAL_DEGREE)
    ]


def in_column_span(matrix: list[list[int]], target: Vector) -> bool:
    augmented = [row[:] + [target[index]] for index, row in enumerate(matrix)]
    return rank_mod(matrix, FIELD_Q) == rank_mod(augmented, FIELD_Q)


def quotient_eigen_packet(epsilon: int, internal_seed: list[int]) -> Vector:
    # q_index=0 component is the seed.  Recurrence sigma(x)=epsilon*x would
    # force x[q+1,r] = epsilon^(-1)*x[q,r], up to the raw cyclic wrap that
    # moves the internal coordinate after seven steps.
    vector = zero()
    inv_epsilon = pow(epsilon, -1, FIELD_Q)
    for internal_index, value in enumerate(internal_seed):
        coeff = 1
        for quotient_index in range(ORDER7):
            vector[quotient_index + ORDER7 * internal_index] = coeff * value % FIELD_Q
            coeff = coeff * inv_epsilon % FIELD_Q
    return vector


def random_internal_seed(rng: random.Random) -> list[int]:
    while True:
        seed = [rng.randrange(FIELD_Q) for _index in range(TOY_INTERNAL_DEGREE)]
        if any(seed):
            return seed


def trace_zero_internal_seed(rng: random.Random) -> list[int]:
    seed = [rng.randrange(FIELD_Q) for _index in range(TOY_INTERNAL_DEGREE - 1)]
    seed.append((-sum(seed)) % FIELD_Q)
    if not any(seed):
        seed[0] = 1
        seed[-1] = FIELD_Q - 1
    return seed


def main() -> None:
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    epsilons = [pow(zeta7, k, FIELD_Q) for k in range(1, ORDER7)]
    rng = random.Random(SEED)

    direct_nested_mismatches = 0
    full_factorization_mismatches = 0
    membership_trace_equivalence_failures = 0
    random_memberships = 0
    forced_memberships = 0
    random_internal_trace_zeroes = 0
    forced_internal_trace_zeroes = 0
    coboundary_ranks: list[int] = []
    trials = 0

    for epsilon in epsilons:
        matrix = coboundary_matrix(epsilon)
        coboundary_ranks.append(rank_mod(matrix, FIELD_Q))
        for _trial in range(4):
            random_packet = quotient_eigen_packet(epsilon, random_internal_seed(rng))
            forced_packet = quotient_eigen_packet(epsilon, trace_zero_internal_seed(rng))
            for packet, forced in ((random_packet, False), (forced_packet, True)):
                nested = nested_internal_trace(packet)
                direct = direct_internal_trace(packet)
                full_trace = full_twisted_trace(packet, epsilon)
                quotient_after_nested = quotient_twisted_trace(nested, epsilon)
                internal_obstruction_zero = is_zero(quotient_after_nested)
                in_image = in_column_span(matrix, packet)

                direct_nested_mismatches += int(nested != direct)
                full_factorization_mismatches += int(full_trace != quotient_after_nested)
                membership_trace_equivalence_failures += int(in_image != internal_obstruction_zero)
                if forced:
                    forced_memberships += int(in_image)
                    forced_internal_trace_zeroes += int(internal_obstruction_zero)
                else:
                    random_memberships += int(in_image)
                    random_internal_trace_zeroes += int(internal_obstruction_zero)
                trials += 1

    forced_trials = len(epsilons) * 4
    random_trials = len(epsilons) * 4

    print("Trace-GCD fixed-frequency p24 right coboundary internal-trace gate")
    print(f"field_q={FIELD_Q}")
    print(f"zeta7={zeta7}")
    print(f"toy_quotient_degree={ORDER7}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"toy_internal_degree={TOY_INTERNAL_DEGREE}")
    print(f"toy_total_degree={TOY_TOTAL_DEGREE}")
    print(f"coboundary_ranks={coboundary_ranks}")
    print(f"nested_internal_equals_direct_failures={direct_nested_mismatches}")
    print(f"full_trace_equals_quotient_after_nested_failures={full_factorization_mismatches}")
    print(f"membership_iff_internal_trace_zero_failures={membership_trace_equivalence_failures}")
    print(f"random_internal_trace_zeroes={random_internal_trace_zeroes}/{random_trials}")
    print(f"random_coboundary_memberships={random_memberships}/{random_trials}")
    print(f"forced_internal_trace_zeroes={forced_internal_trace_zeroes}/{forced_trials}")
    print(f"forced_coboundary_memberships={forced_memberships}/{forced_trials}")
    print("interpretation")
    print("  matching_right_coboundary_equiv_nested_internal_trace_zero=1")
    print("  internal_trace_identity_is_the_non_circular_cm_lang_target=1")
    print("  hilbert90_inverse_is_formal_after_internal_trace_zero=1")
    print("  generic_right_packets_do_not_satisfy_internal_trace_zero=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_coboundary_internal_trace_gate")

    if coboundary_ranks != [TOY_TOTAL_DEGREE - 1] * 6:
        raise SystemExit(1)
    if direct_nested_mismatches or full_factorization_mismatches:
        raise SystemExit(1)
    if membership_trace_equivalence_failures:
        raise SystemExit(1)
    if forced_internal_trace_zeroes != forced_trials or forced_memberships != forced_trials:
        raise SystemExit(1)
    if random_internal_trace_zeroes != random_memberships:
        raise SystemExit(1)
    if random_memberships == random_trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

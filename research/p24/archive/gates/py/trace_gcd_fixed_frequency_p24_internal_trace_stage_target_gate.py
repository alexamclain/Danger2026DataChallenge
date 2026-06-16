#!/usr/bin/env python3
"""Stage target for the p24 internal-trace cancellation theorem.

The right-coboundary internal-trace gate says the matching right potential
exists iff the nested internal trace vanishes.  Since

    5549 = 31 * 179,
    Tr_{B/E} = Tr_{C/E} o Tr_{B/C},

there are two possible proof strengths:

* prove Tr_{B/C}(obstruction)=0;
* prove only Tr_{C/E}(Tr_{B/C}(obstruction))=0.

This gate records the dimension distinction in a cyclic model.  For quotient
eigenpackets, the first target is much stronger: it imposes the whole
intermediate vector to vanish.  The certificate-shaped target is the weaker
one: after the degree-31 trace, prove the degree-179 trace to E vanishes.
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
    return trace_over_powers(vector, ORDER7 * TOY_C_DEGREE, TOY_B_OVER_C_DEGREE)


def trace_c_over_e(vector: Vector) -> Vector:
    return trace_over_powers(vector, ORDER7, TOY_C_DEGREE)


def nested_internal_trace(vector: Vector) -> Vector:
    return trace_c_over_e(trace_b_over_c(vector))


def quotient_eigen_packet(epsilon: int, internal_seed: list[int]) -> Vector:
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


def nested_zero_b_nonzero_seed(rng: random.Random) -> list[int]:
    # Work in C buckets.  Each bucket has B_OVER_C entries.  Make the bucket
    # sums nonzero but total bucket-sum zero.
    bucket_sums = [rng.randrange(1, FIELD_Q) for _index in range(TOY_C_DEGREE - 1)]
    bucket_sums.append((-sum(bucket_sums)) % FIELD_Q)
    if bucket_sums[-1] == 0:
        bucket_sums[-1] = 1
        bucket_sums[0] = (bucket_sums[0] - 1) % FIELD_Q
    seed = [0] * TOY_INTERNAL_DEGREE
    for bucket, bucket_sum in enumerate(bucket_sums):
        seed[bucket] = bucket_sum
    return seed


def b_trace_zero_seed(rng: random.Random) -> list[int]:
    seed = [0] * TOY_INTERNAL_DEGREE
    for bucket in range(TOY_C_DEGREE):
        values = [rng.randrange(FIELD_Q) for _index in range(TOY_B_OVER_C_DEGREE - 1)]
        values.append((-sum(values)) % FIELD_Q)
        for index, value in enumerate(values):
            seed[bucket + TOY_C_DEGREE * index] = value
    if not any(seed):
        seed[0] = 1
        seed[1] = FIELD_Q - 1
    return seed


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


def internal_seed_linear_map(fn) -> list[list[int]]:
    columns: list[Vector] = []
    for index in range(TOY_INTERNAL_DEGREE):
        seed = [0] * TOY_INTERNAL_DEGREE
        seed[index] = 1
        packet = quotient_eigen_packet(1, seed)
        columns.append(fn(packet))
    return [[columns[col][row] for col in range(TOY_INTERNAL_DEGREE)] for row in range(TOY_TOTAL_DEGREE)]


def main() -> None:
    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    epsilons = [pow(zeta7, k, FIELD_Q) for k in range(1, ORDER7)]
    rng = random.Random(SEED)

    b_trace_rank = rank_mod(internal_seed_linear_map(trace_b_over_c), FIELD_Q)
    nested_trace_rank = rank_mod(internal_seed_linear_map(nested_internal_trace), FIELD_Q)

    random_nested_zeroes = 0
    random_b_zeroes = 0
    forced_nested_not_b = 0
    forced_b_zeroes = 0
    forced_b_zero_implies_nested = 0
    trials = 0

    for epsilon in epsilons:
        for _trial in range(8):
            random_packet = quotient_eigen_packet(epsilon, random_internal_seed(rng))
            random_nested_zeroes += int(is_zero(nested_internal_trace(random_packet)))
            random_b_zeroes += int(is_zero(trace_b_over_c(random_packet)))

            weak_packet = quotient_eigen_packet(epsilon, nested_zero_b_nonzero_seed(rng))
            forced_nested_not_b += int(
                is_zero(nested_internal_trace(weak_packet))
                and not is_zero(trace_b_over_c(weak_packet))
            )

            strong_packet = quotient_eigen_packet(epsilon, b_trace_zero_seed(rng))
            strong_b_zero = is_zero(trace_b_over_c(strong_packet))
            forced_b_zeroes += int(strong_b_zero)
            forced_b_zero_implies_nested += int(
                strong_b_zero and is_zero(nested_internal_trace(strong_packet))
            )
            trials += 1

    print("Trace-GCD fixed-frequency p24 internal-trace stage target gate")
    print(f"field_q={FIELD_Q}")
    print(f"zeta7={zeta7}")
    print(f"toy_quotient_degree={ORDER7}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"toy_internal_degree={TOY_INTERNAL_DEGREE}")
    print(f"toy_total_degree={TOY_TOTAL_DEGREE}")
    print(f"b_over_c_trace_rank_on_quotient_eigenpackets={b_trace_rank}")
    print(f"nested_trace_rank_on_quotient_eigenpackets={nested_trace_rank}")
    print(f"p24_B_over_C_trace_rank_target=179")
    print(f"p24_nested_trace_rank_target=1")
    print(f"random_nested_trace_zeroes={random_nested_zeroes}/{trials}")
    print(f"random_B_over_C_trace_zeroes={random_b_zeroes}/{trials}")
    print(f"forced_nested_zero_b_trace_nonzero={forced_nested_not_b}/{trials}")
    print(f"forced_B_over_C_trace_zeroes={forced_b_zeroes}/{trials}")
    print(f"forced_B_over_C_zero_implies_nested_zero={forced_b_zero_implies_nested}/{trials}")
    print("interpretation")
    print("  B_over_C_trace_zero_is_sufficient_but_too_strong=1")
    print("  nested_internal_trace_zero_is_the_minimal_stage_target=1")
    print("  prove_C_over_E_trace_of_B_over_C_trace_zero_not_B_over_C_zero=1")
    print("  p24_internal_trace_stage_target_has_codimension_one=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_internal_trace_stage_target_gate")

    if b_trace_rank != TOY_C_DEGREE:
        raise SystemExit(1)
    if nested_trace_rank != 1:
        raise SystemExit(1)
    if forced_nested_not_b != trials:
        raise SystemExit(1)
    if forced_b_zeroes != trials or forced_b_zero_implies_nested != trials:
        raise SystemExit(1)
    if random_b_zeroes > random_nested_zeroes:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

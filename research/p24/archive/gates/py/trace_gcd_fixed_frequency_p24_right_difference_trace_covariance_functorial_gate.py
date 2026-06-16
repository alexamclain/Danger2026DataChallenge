#!/usr/bin/env python3
"""Functorial handoff from polynomial covariance to adjacent trace covariance.

The covariance-telescope gate needs adjacent trace values T_i satisfying

    T_{i+6} = rho(T_i).

This gate isolates when that covariance is formal.  If the evaluated adjacent
right-difference polynomials satisfy

    P_{i+6}(zeta^(h a)) = rho(P_i(zeta^a))

and h lies in the trace subgroup W=<p>, then the decomposition trace over W
does not permute the eight quotient cosets, hence

    Tr_W(P_{i+6})(D) = rho(Tr_W(P_i)(D)).

The script checks this in a small split value-table model and records negative
controls: random tables fail, and using a multiplier outside W permutes the
quotient trace coordinates instead of giving same-coset covariance.
"""

from __future__ import annotations

import random


FIELD_Q = 43
RIGHT_QUOTIENT = 7
SHIFT = 6
TOY_N = 73
TOY_RELATIVE_QUOTIENT = 8
TOY_W_ORDER = (TOY_N - 1) // TOY_RELATIVE_QUOTIENT
SEED = 20260607
TRIALS = 64

P24_N = 3107441
P24_W_ORDER = 388430
P24_RELATIVE_QUOTIENT = 8
P24_RIGHT_SHIFT = 6


Vector = tuple[int, ...]
ValueTable = list[dict[int, Vector]]


def zero() -> Vector:
    return (0,) * RIGHT_QUOTIENT


def add(left: Vector, right: Vector) -> Vector:
    return tuple((left[index] + right[index]) % FIELD_Q for index in range(RIGHT_QUOTIENT))


def rho(value: Vector) -> Vector:
    return value[1:] + value[:1]


def rho_power(value: Vector, exponent: int) -> Vector:
    out = value
    for _step in range(exponent % RIGHT_QUOTIENT):
        out = rho(out)
    return out


def random_vector(rng: random.Random) -> Vector:
    return tuple(rng.randrange(FIELD_Q) for _index in range(RIGHT_QUOTIENT))


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


def primitive_root_mod_prime(modulus: int) -> int:
    factors = factor_distinct(modulus - 1)
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_table(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def subgroup_order_elements(modulus: int, order: int) -> list[int]:
    generator = primitive_root_mod_prime(modulus)
    step = (modulus - 1) // order
    h_generator = pow(generator, step, modulus)
    out: list[int] = []
    value = 1
    for _index in range(order):
        out.append(value)
        value = value * h_generator % modulus
    if value != 1 or len(set(out)) != order:
        raise RuntimeError("bad subgroup")
    return out


def cosets_of_subgroup(modulus: int, subgroup: list[int]) -> list[list[int]]:
    remaining = set(range(1, modulus))
    cosets: list[list[int]] = []
    while remaining:
        rep = min(remaining)
        coset = sorted((rep * u) % modulus for u in subgroup)
        cosets.append(coset)
        remaining.difference_update(coset)
    return cosets


def quotient_index(value: int, logs: dict[int, int]) -> int:
    return logs[value] % TOY_RELATIVE_QUOTIENT


def random_table(rng: random.Random) -> ValueTable:
    return [
        {exponent: random_vector(rng) for exponent in range(1, TOY_N)}
        for _index in range(RIGHT_QUOTIENT)
    ]


def covariant_table(rng: random.Random, multiplier: int) -> ValueTable:
    table: ValueTable = [dict() for _index in range(RIGHT_QUOTIENT)]
    seen: set[tuple[int, int]] = set()
    for start_index in range(RIGHT_QUOTIENT):
        for start_exponent in range(1, TOY_N):
            if (start_index, start_exponent) in seen:
                continue
            seed = random_vector(rng)
            index = start_index
            exponent = start_exponent
            step = 0
            orbit: list[tuple[int, int]] = []
            while (index, exponent) not in orbit:
                orbit.append((index, exponent))
                index = (index + SHIFT) % RIGHT_QUOTIENT
                exponent = (multiplier * exponent) % TOY_N
            for step, (index, exponent) in enumerate(orbit):
                table[index][exponent] = rho_power(seed, step)
                seen.add((index, exponent))
    return table


def trace_vectors(table: ValueTable, cosets: list[list[int]]) -> list[list[Vector]]:
    traces: list[list[Vector]] = []
    for index in range(RIGHT_QUOTIENT):
        row: list[Vector] = []
        for coset in cosets:
            total = zero()
            for exponent in coset:
                total = add(total, table[index][exponent])
            row.append(total)
        traces.append(row)
    return traces


def trace_row(row: dict[int, Vector], cosets: list[list[int]]) -> list[Vector]:
    traces: list[Vector] = []
    for coset in cosets:
        total = zero()
        for exponent in coset:
            total = add(total, row[exponent])
        traces.append(total)
    return traces


def same_coset_trace_covariance_failures(traces: list[list[Vector]]) -> int:
    failures = 0
    for index in range(RIGHT_QUOTIENT):
        next_index = (index + SHIFT) % RIGHT_QUOTIENT
        for coset_index in range(TOY_RELATIVE_QUOTIENT):
            failures += int(traces[next_index][coset_index] != rho(traces[index][coset_index]))
    return failures


def permuted_trace_covariance_failures(
    traces: list[list[Vector]],
    multiplier: int,
    cosets: list[list[int]],
    logs: dict[int, int],
) -> int:
    failures = 0
    coset_map = {
        coset_index: quotient_index((multiplier * coset[0]) % TOY_N, logs)
        for coset_index, coset in enumerate(cosets)
    }
    for index in range(RIGHT_QUOTIENT):
        next_index = (index + SHIFT) % RIGHT_QUOTIENT
        for coset_index in range(TOY_RELATIVE_QUOTIENT):
            failures += int(
                traces[next_index][coset_map[coset_index]] != rho(traces[index][coset_index])
            )
    return failures


def point_covariance_failures(table: ValueTable, multiplier: int) -> int:
    failures = 0
    for index in range(RIGHT_QUOTIENT):
        next_index = (index + SHIFT) % RIGHT_QUOTIENT
        for exponent in range(1, TOY_N):
            failures += int(
                table[next_index][(multiplier * exponent) % TOY_N]
                != rho(table[index][exponent])
            )
    return failures


def main() -> None:
    rng = random.Random(SEED)
    generator = primitive_root_mod_prime(TOY_N)
    logs = log_table(TOY_N, generator)
    subgroup = subgroup_order_elements(TOY_N, TOY_W_ORDER)
    cosets = cosets_of_subgroup(TOY_N, subgroup)
    coset_position_by_qindex = {
        quotient_index(coset[0], logs): position
        for position, coset in enumerate(cosets)
    }
    inside_multiplier = subgroup[1]
    outside_multiplier = generator

    inside_point_failures = 0
    inside_same_coset_failures = 0
    random_same_coset_covariant = 0
    outside_one_step_same_coset_fails = 0
    outside_one_step_permuted_failures = 0

    for _trial in range(TRIALS):
        inside = covariant_table(rng, inside_multiplier)
        inside_traces = trace_vectors(inside, cosets)
        inside_point_failures += point_covariance_failures(inside, inside_multiplier)
        inside_same_coset_failures += same_coset_trace_covariance_failures(inside_traces)

        random_traces = trace_vectors(random_table(rng), cosets)
        random_same_coset_covariant += int(
            same_coset_trace_covariance_failures(random_traces) == 0
        )

        base_row = {exponent: random_vector(rng) for exponent in range(1, TOY_N)}
        next_row: dict[int, Vector] = {}
        for exponent, value in base_row.items():
            next_row[(outside_multiplier * exponent) % TOY_N] = rho(value)
        base_trace = trace_row(base_row, cosets)
        next_trace = trace_row(next_row, cosets)
        same_failures = 0
        permuted_failures = 0
        for coset_index, coset in enumerate(cosets):
            mapped_qindex = quotient_index((outside_multiplier * coset[0]) % TOY_N, logs)
            mapped_index = coset_position_by_qindex[mapped_qindex]
            same_failures += int(next_trace[coset_index] != rho(base_trace[coset_index]))
            permuted_failures += int(next_trace[mapped_index] != rho(base_trace[coset_index]))
        outside_one_step_same_coset_fails += int(same_failures > 0)
        outside_one_step_permuted_failures += permuted_failures

    p24_rho_mod_n = pow(10**24 + 7, 780, P24_N)

    print("Trace-GCD fixed-frequency p24 right-difference trace covariance functorial gate")
    print(f"field_q={FIELD_Q}")
    print(f"toy_n={TOY_N}")
    print(f"toy_generator={generator}")
    print(f"toy_w_order={TOY_W_ORDER}")
    print(f"toy_relative_quotient={TOY_RELATIVE_QUOTIENT}")
    print(f"toy_inside_multiplier={inside_multiplier}")
    print(f"toy_inside_multiplier_quotient_index={quotient_index(inside_multiplier, logs)}")
    print(f"toy_outside_multiplier={outside_multiplier}")
    print(f"toy_outside_multiplier_quotient_index={quotient_index(outside_multiplier, logs)}")
    print(f"inside_point_covariance_failures={inside_point_failures}")
    print(f"inside_same_coset_trace_covariance_failures={inside_same_coset_failures}")
    print(f"random_same_coset_trace_covariant={random_same_coset_covariant}/{TRIALS}")
    print(f"outside_one_step_same_coset_trace_fails={outside_one_step_same_coset_fails}/{TRIALS}")
    print(f"outside_one_step_permuted_trace_covariance_failures={outside_one_step_permuted_failures}")
    print(f"p24_n={P24_N}")
    print(f"p24_w_order={P24_W_ORDER}")
    print(f"p24_relative_quotient={P24_RELATIVE_QUOTIENT}")
    print(f"p24_rho_mod_n={p24_rho_mod_n}")
    print("interpretation")
    print("  pointwise_semilinear_covariance_with_multiplier_inside_trace_subgroup_implies_trace_covariance=1")
    print("  multiplier_inside_trace_subgroup_keeps_decomposition_trace_cosets_fixed=1")
    print("  random_value_tables_do_not_satisfy_trace_covariance=1")
    print("  multiplier_outside_trace_subgroup_only_gives_permuted_coset_covariance=1")
    print("  remaining_covariance_theorem_is_pointwise_cm_lang_frobenius_functoriality_for_P_i=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_difference_trace_covariance_functorial_gate")

    if quotient_index(inside_multiplier, logs) != 0:
        raise SystemExit(1)
    if quotient_index(outside_multiplier, logs) == 0:
        raise SystemExit(1)
    if inside_point_failures or inside_same_coset_failures:
        raise SystemExit(1)
    if random_same_coset_covariant:
        raise SystemExit(1)
    if outside_one_step_same_coset_fails != TRIALS:
        raise SystemExit(1)
    if outside_one_step_permuted_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

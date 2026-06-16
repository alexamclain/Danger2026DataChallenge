#!/usr/bin/env python3
"""Class-character expansion of the fixed-frequency multiplicative target.

This toy expands the new orthogonality target

    sum_v chi(v) <A_u, B_v>

in the class-character basis of a cyclic quotient-plus-relative packet.
It verifies the exact factorization

    sum_v chi(v) <A_u, B_v>
      = sum_a T_{u,0,a} * (sum_v chi(v) T_{0,v,-a}),

where `a` runs over the relative packet characters.

The point is theorem-shaping: the p24 order-7 target is not just "a
class-character resolvent vanishes".  It is a cancellation among products of
non-genus relative class-character resolvents, unless one proves the stronger
right multiplicative packet vanishing term-by-term.
"""

from __future__ import annotations

import random


FIELD_Q = 421  # 420 is divisible by 3*7*5 and by the order-3 quotient roots.
LEFT = 3
RIGHT = 7
RELATIVE = 5
M = LEFT * RIGHT
H = M * RELATIVE
RIGHT_GEN = 3
QUOTIENT_ORDER = 3
LEFT_U = 1
PACKET = (1, 2, 3, 4)  # primitive 5th-root packet in the split toy field.


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


def log_table(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def roots() -> tuple[int, int, int, int, int]:
    root = primitive_root(FIELD_Q)
    return (
        root,
        pow(root, (FIELD_Q - 1) // LEFT, FIELD_Q),
        pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q),
        pow(root, (FIELD_Q - 1) // RELATIVE, FIELD_Q),
        pow(root, (FIELD_Q - 1) // QUOTIENT_ORDER, FIELD_Q),
    )


def random_j(rng: random.Random) -> list[int]:
    return [rng.randrange(FIELD_Q) for _ in range(H)]


def right_neutral_j(rng: random.Random) -> list[int]:
    # Depends on left coordinate and relative coordinate, but not on the right
    # CRT coordinate.  This is a sufficient toy reason for right nonzero
    # additive/multiplicative projections to vanish; it is much stronger than
    # the p24 theorem and is only a control.
    values = [rng.randrange(FIELD_Q) for _ in range(LEFT * RELATIVE)]
    out = [0] * H
    for index in range(H):
        r = index % M
        k = index // M
        out[index] = values[(r % LEFT) + LEFT * k]
    return out


def fiber_value(j_values: list[int], r: int, a: int, zeta_rel: int) -> int:
    return sum(
        j_values[r + M * k] * pow(zeta_rel, (a * k) % RELATIVE, FIELD_Q)
        for k in range(RELATIVE)
    ) % FIELD_Q


def A_value(j_values: list[int], u: int, a: int, zeta_left: int, zeta_rel: int) -> int:
    return sum(
        pow(zeta_left, (u * (r % LEFT)) % LEFT, FIELD_Q)
        * fiber_value(j_values, r, a, zeta_rel)
        for r in range(M)
    ) % FIELD_Q


def B_value(j_values: list[int], v: int, a: int, zeta_right: int, zeta_rel: int) -> int:
    return sum(
        pow(zeta_right, (v * (r % RIGHT)) % RIGHT, FIELD_Q)
        * fiber_value(j_values, r, a, zeta_rel)
        for r in range(M)
    ) % FIELD_Q


def class_trace(
    j_values: list[int],
    u_left: int,
    v_right: int,
    a_relative: int,
    zeta_left: int,
    zeta_right: int,
    zeta_rel: int,
) -> int:
    return sum(
        j_values[index]
        * pow(zeta_left, (u_left * (index % LEFT)) % LEFT, FIELD_Q)
        * pow(zeta_right, (v_right * (index % RIGHT)) % RIGHT, FIELD_Q)
        * pow(zeta_rel, (a_relative * (index // M)) % RELATIVE, FIELD_Q)
        for index in range(H)
    ) % FIELD_Q


def mixed_pairing(
    j_values: list[int],
    u: int,
    v: int,
    zeta_left: int,
    zeta_right: int,
    zeta_rel: int,
) -> int:
    return sum(
        A_value(j_values, u, a, zeta_left, zeta_rel)
        * B_value(j_values, v, -a, zeta_right, zeta_rel)
        for a in PACKET
    ) % FIELD_Q


def quotient_character(v: int, logs: dict[int, int], zeta_q: int, k: int = 1) -> int:
    return pow(zeta_q, (k * logs[v]) % QUOTIENT_ORDER, FIELD_Q)


def multiplicative_projection(
    periods: list[int],
    logs: dict[int, int],
    zeta_q: int,
) -> int:
    return sum(
        quotient_character(v, logs, zeta_q) * periods[v]
        for v in range(1, RIGHT)
    ) % FIELD_Q


def expanded_projection(
    j_values: list[int],
    logs: dict[int, int],
    zeta_left: int,
    zeta_right: int,
    zeta_rel: int,
    zeta_q: int,
) -> tuple[int, list[int]]:
    terms: list[int] = []
    for a in PACKET:
        left_trace = class_trace(j_values, LEFT_U, 0, a, zeta_left, zeta_right, zeta_rel)
        right_combo = sum(
            quotient_character(v, logs, zeta_q)
            * class_trace(j_values, 0, v, -a, zeta_left, zeta_right, zeta_rel)
            for v in range(1, RIGHT)
        ) % FIELD_Q
        terms.append(left_trace * right_combo % FIELD_Q)
    return sum(terms) % FIELD_Q, terms


def audit_case(j_values: list[int], roots_tuple: tuple[int, int, int, int, int], logs: dict[int, int]):
    _root, zeta_left, zeta_right, zeta_rel, zeta_q = roots_tuple
    periods = [0] * RIGHT
    pairing_factor_mismatches = 0
    for v in range(1, RIGHT):
        periods[v] = mixed_pairing(j_values, LEFT_U, v, zeta_left, zeta_right, zeta_rel)
        expanded_direct = sum(
            class_trace(j_values, LEFT_U, 0, a, zeta_left, zeta_right, zeta_rel)
            * class_trace(j_values, 0, v, -a, zeta_left, zeta_right, zeta_rel)
            for a in PACKET
        ) % FIELD_Q
        pairing_factor_mismatches += int(periods[v] != expanded_direct)
    direct_projection = multiplicative_projection(periods, logs, zeta_q)
    expanded, terms = expanded_projection(
        j_values,
        logs,
        zeta_left,
        zeta_right,
        zeta_rel,
        zeta_q,
    )
    nonzero_left = 0
    nonzero_right_combos = 0
    for a in PACKET:
        nonzero_left += int(
            class_trace(j_values, LEFT_U, 0, a, zeta_left, zeta_right, zeta_rel) != 0
        )
        nonzero_right_combos += int(
            sum(
                quotient_character(v, logs, zeta_q)
                * class_trace(j_values, 0, v, -a, zeta_left, zeta_right, zeta_rel)
                for v in range(1, RIGHT)
            )
            % FIELD_Q
            != 0
        )
    return {
        "pairing_factor_mismatches": pairing_factor_mismatches,
        "projection_mismatch": int(direct_projection != expanded),
        "projection": direct_projection,
        "nonzero_terms": sum(int(term != 0) for term in terms),
        "nonzero_left": nonzero_left,
        "nonzero_right_combos": nonzero_right_combos,
    }


def main() -> None:
    rng = random.Random(20260606)
    roots_tuple = roots()
    logs = log_table(RIGHT, RIGHT_GEN)
    random_results = [audit_case(random_j(rng), roots_tuple, logs) for _ in range(12)]
    neutral_result = audit_case(right_neutral_j(rng), roots_tuple, logs)

    print("Trace-GCD fixed-frequency class-character expansion toy")
    print(f"field_q={FIELD_Q}")
    print(f"field_primitive_root={roots_tuple[0]}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"relative={RELATIVE}")
    print(f"quotient_order={QUOTIENT_ORDER}")
    print(f"packet={list(PACKET)}")
    print(f"random_trials={len(random_results)}")
    print(
        "pairing_factor_mismatches="
        f"{sum(row['pairing_factor_mismatches'] for row in random_results)}"
    )
    print(
        "projection_expansion_mismatches="
        f"{sum(row['projection_mismatch'] for row in random_results)}"
    )
    print(
        "random_projection_nonzeroes="
        f"{sum(int(row['projection'] != 0) for row in random_results)}/{len(random_results)}"
    )
    print(
        "random_all_left_packet_traces_nonzeroes="
        f"{sum(int(row['nonzero_left'] == len(PACKET)) for row in random_results)}/{len(random_results)}"
    )
    print(
        "random_all_right_multiplicative_packet_combos_nonzeroes="
        f"{sum(int(row['nonzero_right_combos'] == len(PACKET)) for row in random_results)}/{len(random_results)}"
    )
    print(
        "random_all_product_terms_nonzeroes="
        f"{sum(int(row['nonzero_terms'] == len(PACKET)) for row in random_results)}/{len(random_results)}"
    )
    print(f"right_neutral_projection_zero={int(neutral_result['projection'] == 0)}")
    print(f"right_neutral_right_combos_nonzero={neutral_result['nonzero_right_combos']}/{len(PACKET)}")
    print("interpretation")
    print("  multiplicative_resolvent_target_expands_into_packet_product_sum=1")
    print("  nonzero_class_character_resolvents_do_not_force_target_vanishing=1")
    print("  termwise_right_multiplicative_vanishing_is_sufficient_but_too_strong=1")
    print("  p24_needs_packet_cancellation_or_stronger_right_combo_vanishing=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_class_character_expansion_toy")

    if any(row["pairing_factor_mismatches"] for row in random_results):
        raise SystemExit(1)
    if any(row["projection_mismatch"] for row in random_results):
        raise SystemExit(1)
    if not all(row["projection"] != 0 for row in random_results):
        raise SystemExit(1)
    if not all(row["nonzero_left"] == len(PACKET) for row in random_results):
        raise SystemExit(1)
    if not all(row["nonzero_right_combos"] == len(PACKET) for row in random_results):
        raise SystemExit(1)
    if not all(row["nonzero_terms"] == len(PACKET) for row in random_results):
        raise SystemExit(1)
    if neutral_result["projection"] != 0 or neutral_result["nonzero_right_combos"] != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

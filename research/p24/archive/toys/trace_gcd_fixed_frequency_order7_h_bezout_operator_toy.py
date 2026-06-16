#!/usr/bin/env python3
"""Universal Bezout operator for the order-7 H-coboundary target.

Let H=<gamma> have order n=30 and let T act by `(T f)(s)=f(gamma*s)`.
The additive Hilbert-90 target is:

    G = (1-T)Y

on each H-coset.  This is equivalent to `e_H G=0`, where
`e_H=(1/n)sum_i T^i`.

This toy records the fixed group-algebra certificate:

    (1-T) U = 1 - e_H,
    U = (1/n) sum_{i=0}^{n-1} (n-1-i) T^i.

Therefore, once the p24 arithmetic proof gives the H-coset trace identities
`e_H G=0`, the potential is deterministic: `Y=U G`.  No sampling is involved.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
GEN = 2
H_STEP = 7
H_ORDER = 30
Q = 1009


def log_table() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("generator is not primitive")
    return logs


def cosets_by_log_residue(logs: dict[int, int]) -> list[list[int]]:
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % H_STEP == residue],
            key=logs.__getitem__,
        )
        for residue in range(H_STEP)
    ]


def shift(row: list[int], gamma: int) -> list[int]:
    out = [0] * RIGHT
    for value in range(1, RIGHT):
        out[value] = row[gamma * value % RIGHT]
    return out


def add(left: list[int], right: list[int]) -> list[int]:
    return [(a + b) % Q for a, b in zip(left, right)]


def sub(left: list[int], right: list[int]) -> list[int]:
    return [(a - b) % Q for a, b in zip(left, right)]


def scale(coeff: int, row: list[int]) -> list[int]:
    return [(coeff * value) % Q for value in row]


def apply_power(row: list[int], gamma: int, power: int) -> list[int]:
    out = row[:]
    for _ in range(power):
        out = shift(out, gamma)
    return out


def h_average(row: list[int], gamma: int) -> list[int]:
    inv_n = pow(H_ORDER, -1, Q)
    total = [0] * RIGHT
    for power in range(H_ORDER):
        total = add(total, apply_power(row, gamma, power))
    return scale(inv_n, total)


def bezout_u(row: list[int], gamma: int) -> list[int]:
    inv_n = pow(H_ORDER, -1, Q)
    total = [0] * RIGHT
    for power in range(H_ORDER):
        coeff = (H_ORDER - 1 - power) * inv_n % Q
        total = add(total, scale(coeff, apply_power(row, gamma, power)))
    return total


def coboundary(row: list[int], gamma: int) -> list[int]:
    return sub(row, shift(row, gamma))


def relative_trace_zero(row: list[int], cosets: list[list[int]]) -> bool:
    return all(sum(row[value] for value in coset) % Q == 0 for coset in cosets)


def random_row(rng: random.Random) -> list[int]:
    return [0] + [rng.randrange(Q) for _value in range(1, RIGHT)]


def force_trace_zero(row: list[int], cosets: list[list[int]]) -> list[int]:
    out = row[:]
    for coset in cosets:
        out[coset[0]] = (out[coset[0]] - sum(out[value] for value in coset)) % Q
    return out


def equal_nonzero(left: list[int], right: list[int]) -> bool:
    return all((left[value] - right[value]) % Q == 0 for value in range(1, RIGHT))


def main() -> None:
    logs = log_table()
    gamma = pow(GEN, H_STEP, RIGHT)
    cosets = cosets_by_log_residue(logs)
    rng = random.Random(20260606)

    random_control = random_row(rng)
    trace_zero = force_trace_zero(random_row(rng), cosets)

    average_random = h_average(random_control, gamma)
    residual_random = sub(random_control, average_random)
    bezout_random = coboundary(bezout_u(random_control, gamma), gamma)

    average_zero = h_average(trace_zero, gamma)
    bezout_potential = bezout_u(trace_zero, gamma)
    reconstructed = coboundary(bezout_potential, gamma)
    potential_average = h_average(bezout_potential, gamma)

    p_mod = P24 % RIGHT
    p_log = logs[p_mod]

    print("Trace-GCD fixed-frequency order-7 H-Bezout operator toy")
    print(f"field_q={Q}")
    print(f"right={RIGHT}")
    print(f"primitive_root={GEN}")
    print(f"p24_p_mod_211={p_mod}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"h_generator=2^{H_STEP}_mod_211={gamma}")
    print(f"h_order={H_ORDER}")
    print(f"h_coset_count={len(cosets)}")
    print(f"h_coset_size={len(cosets[0])}")
    print(f"h_order_invertible_mod_q={int(H_ORDER % Q != 0)}")
    print(f"bezout_identity_random_control={int(equal_nonzero(bezout_random, residual_random))}")
    print(f"random_control_h_average_nonzero={int(any(average_random[value] for value in range(1, RIGHT)))}")
    print(f"trace_zero_input_h_average_zero={int(not any(average_zero[value] for value in range(1, RIGHT)))}")
    print(f"trace_zero_input_relative_trace_zero={int(relative_trace_zero(trace_zero, cosets))}")
    print(f"canonical_potential_reconstructs_trace_zero_input={int(equal_nonzero(reconstructed, trace_zero))}")
    print(f"canonical_potential_has_zero_h_average={int(not any(potential_average[value] for value in range(1, RIGHT)))}")
    print("interpretation")
    print("  universal_operator_satisfies_one_minus_T_times_U_equals_one_minus_eH=1")
    print("  h_trace_zero_gives_deterministic_potential_Y_equals_U_G=1")
    print("  p24_remaining_arithmetic_theorem_is_eH_G_equals_zero=1")
    print("  no_sampling_needed_once_h_coset_sums_vanish=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order7_h_bezout_operator_toy")

    if (p_mod, p_log, gamma, len(cosets), len(cosets[0])) != (114, 198, 128, 7, 30):
        raise SystemExit(1)
    if not equal_nonzero(bezout_random, residual_random):
        raise SystemExit(1)
    if not any(average_random[value] for value in range(1, RIGHT)):
        raise SystemExit(1)
    if any(average_zero[value] for value in range(1, RIGHT)):
        raise SystemExit(1)
    if not relative_trace_zero(trace_zero, cosets):
        raise SystemExit(1)
    if not equal_nonzero(reconstructed, trace_zero):
        raise SystemExit(1)
    if any(potential_average[value] for value in range(1, RIGHT)):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

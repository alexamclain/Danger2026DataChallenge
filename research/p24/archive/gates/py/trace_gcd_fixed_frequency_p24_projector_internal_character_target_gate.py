#!/usr/bin/env python3
"""Combine right-axis projectors with the internal C/E character target.

The current p24 target has two equivalent-looking front doors:

* right-axis form: six nontrivial rho/quotient projectors vanish;
* internal-trace form: after B/C trace, the trivial C/E component vanishes.

This gate puts them in one finite model.  A raw packet has coordinates

    quotient C_7  x  internal C_179  x  B/C C_31.

In the toy model we use C_7 x C_5 x C_3.  The quotient projector commutes
with the internal traces, so for each nontrivial quotient index m the real
arithmetic target is:

    Tr_{C/E}(Tr_{B/C}(Pi_m(packet))) = 0.

Random quotient-projected packets do not satisfy this.  Packets supported in
nontrivial C-character components do.  Packets with trivial C-character
support do not.  Thus the missing theorem is precisely a statement that the
weighted CM/Lang packet has no trivial C component after B/C trace in each of
the six quotient projector channels.
"""

from __future__ import annotations

import random

import sympy as sp


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
N = 3107441
RHO_EXPONENT = 780
ORDER7 = 7
P24_C_DEGREE = 179
P24_B_OVER_C_DEGREE = 31

FIELD_Q = 211  # 210 is divisible by 7 and 5.
TOY_QUOTIENT_DEGREE = 7
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3
SEED = 20260606
TRIALS = 24


RawPacket = list[list[list[int]]]
QuotC = list[list[int]]


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


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def zero_packet() -> RawPacket:
    return [
        [[0 for _b in range(TOY_B_OVER_C_DEGREE)] for _c in range(TOY_C_DEGREE)]
        for _q in range(TOY_QUOTIENT_DEGREE)
    ]


def random_packet(rng: random.Random) -> RawPacket:
    return [
        [
            [rng.randrange(FIELD_Q) for _b in range(TOY_B_OVER_C_DEGREE)]
            for _c in range(TOY_C_DEGREE)
        ]
        for _q in range(TOY_QUOTIENT_DEGREE)
    ]


def character_packet(quotient_index: int, c_index: int, omega7: int, omega_c: int) -> RawPacket:
    packet = zero_packet()
    for q_index in range(TOY_QUOTIENT_DEGREE):
        q_value = pow(omega7, quotient_index * q_index, FIELD_Q)
        for c_pos in range(TOY_C_DEGREE):
            c_value = pow(omega_c, c_index * c_pos, FIELD_Q)
            for b_pos in range(TOY_B_OVER_C_DEGREE):
                packet[q_index][c_pos][b_pos] = q_value * c_value % FIELD_Q
    return packet


def quotient_projector(packet: RawPacket, omega7: int, quotient_index: int) -> RawPacket:
    inv7 = pow(TOY_QUOTIENT_DEGREE, -1, FIELD_Q)
    projected = zero_packet()
    for target_q in range(TOY_QUOTIENT_DEGREE):
        for source_q in range(TOY_QUOTIENT_DEGREE):
            weight = pow(
                omega7,
                (-quotient_index * (source_q - target_q)) % TOY_QUOTIENT_DEGREE,
                FIELD_Q,
            )
            for c_pos in range(TOY_C_DEGREE):
                for b_pos in range(TOY_B_OVER_C_DEGREE):
                    projected[target_q][c_pos][b_pos] = (
                        projected[target_q][c_pos][b_pos]
                        + inv7 * weight * packet[source_q][c_pos][b_pos]
                    ) % FIELD_Q
    return projected


def trace_b_over_c(packet: RawPacket) -> QuotC:
    return [
        [
            sum(packet[q_index][c_pos][b_pos] for b_pos in range(TOY_B_OVER_C_DEGREE))
            % FIELD_Q
            for c_pos in range(TOY_C_DEGREE)
        ]
        for q_index in range(TOY_QUOTIENT_DEGREE)
    ]


def trace_c_over_e(quot_c: QuotC) -> list[int]:
    return [sum(row) % FIELD_Q for row in quot_c]


def full_internal_trace(packet: RawPacket) -> list[int]:
    return trace_c_over_e(trace_b_over_c(packet))


def c_character_projection(quot_c: QuotC, omega_c: int, character_index: int) -> list[int]:
    out: list[int] = []
    for q_index in range(TOY_QUOTIENT_DEGREE):
        total = 0
        for c_pos, value in enumerate(quot_c[q_index]):
            total = (
                total
                + value * pow(omega_c, (-character_index * c_pos) % TOY_C_DEGREE, FIELD_Q)
            ) % FIELD_Q
        out.append(total)
    return out


def nonzero(values: list[int]) -> bool:
    return any(value % FIELD_Q for value in values)


def packets_equal(left: RawPacket, right: RawPacket) -> bool:
    return left == right


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_shift = logs[rho_right] % ORDER7
    rho_mod_n = pow(P24, RHO_EXPONENT, N)
    rho_order_mod_n = int(sp.n_order(rho_mod_n, N))
    internal_generator = pow(P24, RHO_EXPONENT * ORDER7, N)
    internal_order = int(sp.n_order(internal_generator, N))
    b_over_c_generator = pow(internal_generator, P24_C_DEGREE, N)
    b_over_c_order = int(sp.n_order(b_over_c_generator, N))
    c_over_e_generator = pow(internal_generator, P24_B_OVER_C_DEGREE, N)
    c_over_e_order = int(sp.n_order(c_over_e_generator, N))

    root = primitive_root(FIELD_Q)
    omega7 = pow(root, (FIELD_Q - 1) // TOY_QUOTIENT_DEGREE, FIELD_Q)
    omega_c = pow(root, (FIELD_Q - 1) // TOY_C_DEGREE, FIELD_Q)
    rng = random.Random(SEED)

    projector_idempotent_failures = 0
    projector_trace_commutation_failures = 0
    random_projected_final_trace_nonzero = 0
    forced_nontrivial_c_final_trace_zero = 0
    forced_nontrivial_c_b_trace_nonzero = 0
    forced_trivial_c_final_trace_nonzero = 0
    forced_trivial_c_detected_by_c_projection = 0
    checks = 0

    for quotient_index in range(1, TOY_QUOTIENT_DEGREE):
        for _trial in range(TRIALS):
            packet = random_packet(rng)
            projected = quotient_projector(packet, omega7, quotient_index)
            projected_again = quotient_projector(projected, omega7, quotient_index)
            projector_idempotent_failures += int(not packets_equal(projected, projected_again))
            random_projected_final_trace_nonzero += int(nonzero(full_internal_trace(projected)))

            # Projecting before or after B/C trace is the same for the
            # quotient coordinate.  Lift the B/C trace back with one B slot to
            # reuse the same projector routine.
            b_trace = trace_b_over_c(packet)
            lifted = zero_packet()
            for q_pos in range(TOY_QUOTIENT_DEGREE):
                for c_pos in range(TOY_C_DEGREE):
                    lifted[q_pos][c_pos][0] = b_trace[q_pos][c_pos]
            left = trace_b_over_c(quotient_projector(packet, omega7, quotient_index))
            right = trace_b_over_c(quotient_projector(lifted, omega7, quotient_index))
            projector_trace_commutation_failures += int(left != right)

        nontrivial_c_packet = character_packet(quotient_index, 1, omega7, omega_c)
        nontrivial_projected = quotient_projector(nontrivial_c_packet, omega7, quotient_index)
        nontrivial_b = trace_b_over_c(nontrivial_projected)
        forced_nontrivial_c_final_trace_zero += int(
            not nonzero(full_internal_trace(nontrivial_projected))
        )
        forced_nontrivial_c_b_trace_nonzero += int(any(nonzero(row) for row in nontrivial_b))

        trivial_c_packet = character_packet(quotient_index, 0, omega7, omega_c)
        trivial_projected = quotient_projector(trivial_c_packet, omega7, quotient_index)
        trivial_b = trace_b_over_c(trivial_projected)
        forced_trivial_c_final_trace_nonzero += int(nonzero(full_internal_trace(trivial_projected)))
        forced_trivial_c_detected_by_c_projection += int(
            nonzero(c_character_projection(trivial_b, omega_c, 0))
        )
        checks += 1

    print("Trace-GCD fixed-frequency p24 projector/internal-character target gate")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho_right}")
    print(f"rho_log_mod_order7_quotient={rho_shift}")
    print(f"n={N}")
    print(f"rho_mod_n={rho_mod_n}")
    print(f"rho_order_mod_n={rho_order_mod_n}")
    print(f"internal_generator=p^(780*7)_mod_n={internal_generator}")
    print(f"internal_order={internal_order}")
    print(f"b_over_c_order={b_over_c_order}")
    print(f"c_over_e_order={c_over_e_order}")
    print(f"toy_q={FIELD_Q}")
    print(f"toy_quotient_degree={TOY_QUOTIENT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"projector_idempotent_failures={projector_idempotent_failures}")
    print(f"projector_commutes_with_B_over_C_trace_failures={projector_trace_commutation_failures}")
    print(
        "random_projected_packets_final_internal_trace_nonzero="
        f"{random_projected_final_trace_nonzero}/{TRIALS * 6}"
    )
    print(
        "forced_nontrivial_C_character_final_trace_zero="
        f"{forced_nontrivial_c_final_trace_zero}/{checks}"
    )
    print(
        "forced_nontrivial_C_character_B_trace_nonzero="
        f"{forced_nontrivial_c_b_trace_nonzero}/{checks}"
    )
    print(
        "forced_trivial_C_character_final_trace_nonzero="
        f"{forced_trivial_c_final_trace_nonzero}/{checks}"
    )
    print(
        "forced_trivial_C_character_detected_by_projection="
        f"{forced_trivial_c_detected_by_c_projection}/{checks}"
    )
    print("interpretation")
    print("  quotient_projectors_commute_with_internal_B_over_C_trace=1")
    print("  quotient_projector_alone_does_not_force_final_internal_trace_zero=1")
    print("  nontrivial_C_character_support_would_force_final_trace_zero=1")
    print("  p24_missing_theorem_is_no_trivial_C_component_in_each_projector_channel=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_projector_internal_character_target_gate")

    if (rho_shift, rho_order_mod_n, internal_order) != (6, 38843, 5549):
        raise SystemExit(1)
    if (b_over_c_order, c_over_e_order) != (31, 179):
        raise SystemExit(1)
    if projector_idempotent_failures or projector_trace_commutation_failures:
        raise SystemExit(1)
    if random_projected_final_trace_nonzero < TRIALS * 6 - 2:
        raise SystemExit(1)
    if forced_nontrivial_c_final_trace_zero != checks:
        raise SystemExit(1)
    if forced_nontrivial_c_b_trace_nonzero != checks:
        raise SystemExit(1)
    if forced_trivial_c_final_trace_nonzero != checks:
        raise SystemExit(1)
    if forced_trivial_c_detected_by_c_projection != checks:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

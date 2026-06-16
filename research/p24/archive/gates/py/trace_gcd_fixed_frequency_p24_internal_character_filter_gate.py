#!/usr/bin/env python3
"""Internal C/E character filter for the p24 Gaussian trace target.

The Gaussian-functional gate identifies the remaining scalar theorem as

    Tr_{C/E}(Tr_{B/C}(R_obstruction)) = 0.

This gate rewrites that target one layer more sharply.  After the B/C trace,
the C/E trace is exactly the projection to the trivial C-character.  Thus the
missing arithmetic theorem may be stated as:

    the B/C-traced obstruction has no trivial C/E character component.

It also records a useful negative fact: the order-7 quotient twist from the
raw p^780 action cannot force this internal trace zero.  Seven raw steps are
the internal generator, so an order-7 scalar twist disappears before the
degree-5549 trace is even tested.
"""

from __future__ import annotations

import random

import sympy as sp


P24 = 10**24 + 7
N = 3107441
RHO_EXPONENT = 780
ORDER7 = 7
P24_C_DEGREE = 179
P24_B_OVER_C_DEGREE = 31
P24_INTERNAL_DEGREE = P24_C_DEGREE * P24_B_OVER_C_DEGREE

FIELD_Q = 71
TOY_QUOTIENT_DEGREE = 7
TOY_C_DEGREE = 5
TOY_B_OVER_C_DEGREE = 3
TOY_INTERNAL_DEGREE = TOY_C_DEGREE * TOY_B_OVER_C_DEGREE
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


def scalar_mul(scalar: int, vector: Vector) -> Vector:
    return [(scalar * value) % FIELD_Q for value in vector]


def is_zero(vector: Vector) -> bool:
    return all(value % FIELD_Q == 0 for value in vector)


def quotient_character_vector(epsilon: int) -> Vector:
    inv_epsilon = pow(epsilon, -1, FIELD_Q)
    coeff = 1
    out: Vector = []
    for _index in range(TOY_QUOTIENT_DEGREE):
        out.append(coeff)
        coeff = coeff * inv_epsilon % FIELD_Q
    return out


def tensor_packet(quotient: Vector, internal_seed: Vector) -> Vector:
    out: Vector = []
    for internal_value in internal_seed:
        for quotient_value in quotient:
            out.append(quotient_value * internal_value % FIELD_Q)
    return out


def random_internal_seed(rng: random.Random) -> Vector:
    while True:
        seed = [rng.randrange(FIELD_Q) for _index in range(TOY_INTERNAL_DEGREE)]
        if any(seed):
            return seed


def internal_shift(seed: Vector, power: int = 1) -> Vector:
    shift = power % TOY_INTERNAL_DEGREE
    if shift == 0:
        return seed[:]
    return seed[-shift:] + seed[:-shift]


def raw_seven_steps(packet: Vector) -> Vector:
    """On the tensor model, seven quotient steps are one internal shift."""
    quotient_size = TOY_QUOTIENT_DEGREE
    out = [0] * len(packet)
    for internal_index in range(TOY_INTERNAL_DEGREE):
        source_internal = (internal_index - 1) % TOY_INTERNAL_DEGREE
        for quotient_index in range(quotient_size):
            out[internal_index * quotient_size + quotient_index] = (
                packet[source_internal * quotient_size + quotient_index]
            )
    return out


def internal_trace_tensor(packet: Vector) -> Vector:
    out = [0] * TOY_QUOTIENT_DEGREE
    for internal_index in range(TOY_INTERNAL_DEGREE):
        for quotient_index in range(TOY_QUOTIENT_DEGREE):
            out[quotient_index] = (
                out[quotient_index]
                + packet[internal_index * TOY_QUOTIENT_DEGREE + quotient_index]
            ) % FIELD_Q
    return out


def trace_b_over_c_seed(seed: Vector) -> Vector:
    bucket_sums = [0] * TOY_C_DEGREE
    for c_index in range(TOY_C_DEGREE):
        for b_index in range(TOY_B_OVER_C_DEGREE):
            bucket_sums[c_index] = (
                bucket_sums[c_index] + seed[c_index + TOY_C_DEGREE * b_index]
            ) % FIELD_Q
    return bucket_sums


def trace_c_over_e_seed(bucket_sums: Vector) -> int:
    return sum(bucket_sums) % FIELD_Q


def c_character_projection(bucket_sums: Vector, omega: int, character_index: int) -> int:
    total = 0
    for c_index, value in enumerate(bucket_sums):
        total = (total + value * pow(omega, (-character_index * c_index) % TOY_C_DEGREE, FIELD_Q)) % FIELD_Q
    return total


def force_zero_trivial_c_component(seed: Vector) -> Vector:
    adjusted = seed[:]
    total = trace_c_over_e_seed(trace_b_over_c_seed(adjusted))
    adjusted[0] = (adjusted[0] - total) % FIELD_Q
    return adjusted


def nontrivial_c_character_seed(omega: int, character_index: int, scale: int) -> Vector:
    seed = [0] * TOY_INTERNAL_DEGREE
    for c_index in range(TOY_C_DEGREE):
        seed[c_index] = scale * pow(omega, character_index * c_index, FIELD_Q) % FIELD_Q
    return seed


def main() -> None:
    rho_mod_n = pow(P24, RHO_EXPONENT, N)
    rho_order_mod_n = int(sp.n_order(rho_mod_n, N))
    internal_generator = pow(P24, RHO_EXPONENT * ORDER7, N)
    internal_order = int(sp.n_order(internal_generator, N))
    b_over_c_generator = pow(internal_generator, P24_C_DEGREE, N)
    b_over_c_order = int(sp.n_order(b_over_c_generator, N))
    c_over_e_generator = pow(internal_generator, P24_B_OVER_C_DEGREE, N)
    c_over_e_order = int(sp.n_order(c_over_e_generator, N))

    root = primitive_root(FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // TOY_QUOTIENT_DEGREE, FIELD_Q)
    omega_c = pow(root, (FIELD_Q - 1) // TOY_C_DEGREE, FIELD_Q)
    rng = random.Random(SEED)

    raw_twist_survives_seven_steps_failures = 0
    random_internal_trace_nonzero = 0
    forced_internal_trace_zero = 0
    forced_b_trace_nonzero = 0
    nontrivial_c_trace_zero = 0
    nontrivial_c_b_trace_nonzero = 0
    trivial_projection_mismatches = 0
    nontrivial_projection_support_hits = 0
    trials = 0

    for k in range(1, TOY_QUOTIENT_DEGREE):
        epsilon = pow(zeta7, k, FIELD_Q)
        quotient = quotient_character_vector(epsilon)
        for _trial in range(6):
            seed = random_internal_seed(rng)
            packet = tensor_packet(quotient, seed)
            shifted = raw_seven_steps(packet)
            expected = tensor_packet(quotient, internal_shift(seed))
            raw_twist_survives_seven_steps_failures += int(shifted != expected)
            random_internal_trace_nonzero += int(not is_zero(internal_trace_tensor(packet)))

            forced = force_zero_trivial_c_component(seed)
            forced_bucket = trace_b_over_c_seed(forced)
            forced_packet = tensor_packet(quotient, forced)
            forced_internal_trace_zero += int(is_zero(internal_trace_tensor(forced_packet)))
            forced_b_trace_nonzero += int(any(forced_bucket))
            trivial_projection_mismatches += int(
                c_character_projection(forced_bucket, omega_c, 0)
                != trace_c_over_e_seed(forced_bucket)
            )

            char_index = 1 + (_trial % (TOY_C_DEGREE - 1))
            c_seed = nontrivial_c_character_seed(omega_c, char_index, 1 + _trial)
            c_bucket = trace_b_over_c_seed(c_seed)
            c_packet = tensor_packet(quotient, c_seed)
            nontrivial_c_trace_zero += int(is_zero(internal_trace_tensor(c_packet)))
            nontrivial_c_b_trace_nonzero += int(any(c_bucket))
            nontrivial_projection_support_hits += int(
                c_character_projection(c_bucket, omega_c, char_index) != 0
                and c_character_projection(c_bucket, omega_c, 0) == 0
            )
            trials += 1

    print("Trace-GCD fixed-frequency p24 internal character filter gate")
    print(f"p24={P24}")
    print(f"n={N}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_n={rho_mod_n}")
    print(f"rho_order_mod_n={rho_order_mod_n}")
    print(f"internal_generator=p^(780*7)_mod_n={internal_generator}")
    print(f"internal_order={internal_order}")
    print(f"b_over_c_generator=internal^179_mod_n={b_over_c_generator}")
    print(f"b_over_c_order={b_over_c_order}")
    print(f"c_over_e_generator=internal^31_mod_n={c_over_e_generator}")
    print(f"c_over_e_order={c_over_e_order}")
    print(f"field_q={FIELD_Q}")
    print(f"zeta7={zeta7}")
    print(f"omega_c={omega_c}")
    print(f"toy_quotient_degree={TOY_QUOTIENT_DEGREE}")
    print(f"toy_C_degree={TOY_C_DEGREE}")
    print(f"toy_B_over_C_degree={TOY_B_OVER_C_DEGREE}")
    print(f"raw_twist_survives_seven_steps_failures={raw_twist_survives_seven_steps_failures}")
    print(f"random_order7_packets_internal_trace_nonzero={random_internal_trace_nonzero}/{trials}")
    print(f"forced_zero_trivial_c_component_internal_trace_zero={forced_internal_trace_zero}/{trials}")
    print(f"forced_zero_trivial_c_component_b_trace_nonzero={forced_b_trace_nonzero}/{trials}")
    print(f"nontrivial_c_character_packets_internal_trace_zero={nontrivial_c_trace_zero}/{trials}")
    print(f"nontrivial_c_character_b_trace_nonzero={nontrivial_c_b_trace_nonzero}/{trials}")
    print(f"trivial_c_projection_mismatches={trivial_projection_mismatches}")
    print(f"nontrivial_c_projection_support_hits={nontrivial_projection_support_hits}/{trials}")
    print("interpretation")
    print("  order7_quotient_twist_dies_after_internal_generator=1")
    print("  random_order7_covariant_packets_do_not_have_internal_trace_zero=1")
    print("  nested_internal_trace_zero_is_zero_trivial_C_character_component=1")
    print("  nontrivial_C_character_support_is_sufficient_and_not_B_over_C_zero=1")
    print("  remaining_theorem_is_no_trivial_C_character_in_B_over_C_obstruction=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_internal_character_filter_gate")

    if rho_order_mod_n != ORDER7 * P24_INTERNAL_DEGREE:
        raise SystemExit(1)
    if internal_order != P24_INTERNAL_DEGREE:
        raise SystemExit(1)
    if b_over_c_order != P24_B_OVER_C_DEGREE:
        raise SystemExit(1)
    if c_over_e_order != P24_C_DEGREE:
        raise SystemExit(1)
    if raw_twist_survives_seven_steps_failures != 0:
        raise SystemExit(1)
    if random_internal_trace_nonzero == 0:
        raise SystemExit(1)
    if forced_internal_trace_zero != trials:
        raise SystemExit(1)
    if forced_b_trace_nonzero != trials:
        raise SystemExit(1)
    if nontrivial_c_trace_zero != trials:
        raise SystemExit(1)
    if nontrivial_c_b_trace_nonzero != trials:
        raise SystemExit(1)
    if trivial_projection_mismatches != 0:
        raise SystemExit(1)
    if nontrivial_projection_support_hits != trials:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

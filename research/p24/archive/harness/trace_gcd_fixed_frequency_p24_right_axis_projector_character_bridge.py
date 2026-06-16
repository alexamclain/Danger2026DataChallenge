#!/usr/bin/env python3
"""Bridge anchor rho-projectors to H-quotient character equations.

For the p24 right-axis reduction, rho=p^780 shifts the seven H-cosets by

    s = log_2(rho) mod 7 = 6.

Under the covariance relation rho^j(Y_0)=Y_{j*s}, the anchor projector

    Pi_m(Y_0) = (1/7) sum_j omega^(-m*j) rho^j(Y_0)

is exactly one seventh of the quotient-character projection

    sum_c omega^(-k*c) Y_c

with k = m*s^{-1}.  Since s=6 is its own inverse modulo 7, the six nontrivial
anchor projector vanishings are the same six nontrivial H-coset character
equations, just relabeled as 1<->6, 2<->5, 3<->4.
"""

from __future__ import annotations

import random

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
FIELD_Q = 43
FIELD_DEGREE = 7
SEED = 20260606
TRIALS = 32


FpE = tuple[int, ...]
Profile = list[FpE]


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


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    return tuple(rng.randrange(field.q) for _index in range(field.degree))


def random_profile(rng: random.Random, field: ExtensionField) -> Profile:
    return [random_element(rng, field) for _index in range(ORDER7)]


def add_all(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def quotient_character_projection(
    profile: Profile,
    field: ExtensionField,
    omega7: int,
    character_index: int,
) -> FpE:
    return add_all(
        [
            field.scalar_mul(
                pow(omega7, (-character_index * coset) % ORDER7, field.q),
                value,
            )
            for coset, value in enumerate(profile)
        ],
        field,
    )


def anchor_projector_from_covariant_profile(
    profile: Profile,
    field: ExtensionField,
    omega7: int,
    shift: int,
    projector_index: int,
) -> FpE:
    inv7 = pow(ORDER7, -1, field.q)
    orbit = [profile[(step * shift) % ORDER7] for step in range(ORDER7)]
    total = add_all(
        [
            field.scalar_mul(
                pow(omega7, (-projector_index * step) % ORDER7, field.q),
                value,
            )
            for step, value in enumerate(orbit)
        ],
        field,
    )
    return field.scalar_mul(inv7, total)


def nontrivial_quotient_zero(profile: Profile, field: ExtensionField, omega7: int) -> bool:
    return all(
        quotient_character_projection(profile, field, omega7, index) == field.zero
        for index in range(1, ORDER7)
    )


def nontrivial_anchor_zero(
    profile: Profile,
    field: ExtensionField,
    omega7: int,
    shift: int,
) -> bool:
    return all(
        anchor_projector_from_covariant_profile(profile, field, omega7, shift, index)
        == field.zero
        for index in range(1, ORDER7)
    )


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_right]
    shift = rho_log % ORDER7
    shift_inverse = pow(shift, -1, ORDER7)

    field = ExtensionField(
        FIELD_Q,
        FIELD_DEGREE,
        find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED),
    )
    omega7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    rng = random.Random(SEED)

    scale = field.embed(ORDER7)
    index_map = [(projector_index * shift_inverse) % ORDER7 for projector_index in range(ORDER7)]
    bridge_failures = 0
    zero_equivalence_failures = 0
    random_nonzero_anchor_projectors = 0
    random_nonzero_quotient_projections = 0

    for _trial in range(TRIALS):
        profile = random_profile(rng, field)
        for projector_index in range(ORDER7):
            anchor = anchor_projector_from_covariant_profile(
                profile,
                field,
                omega7,
                shift,
                projector_index,
            )
            quotient = quotient_character_projection(
                profile,
                field,
                omega7,
                index_map[projector_index],
            )
            bridge_failures += int(field.mul(scale, anchor) != quotient)
        zero_equivalence_failures += int(
            nontrivial_anchor_zero(profile, field, omega7, shift)
            != nontrivial_quotient_zero(profile, field, omega7)
        )
        random_nonzero_anchor_projectors += int(
            not nontrivial_anchor_zero(profile, field, omega7, shift)
        )
        random_nonzero_quotient_projections += int(
            not nontrivial_quotient_zero(profile, field, omega7)
        )

    print("Trace-GCD fixed-frequency p24 right-axis projector-character bridge")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_log_mod_order7_quotient={shift}")
    print(f"rho_shift_inverse_mod7={shift_inverse}")
    print(f"anchor_projector_to_quotient_character_index_map={index_map}")
    print(f"bridge_identity_failures={bridge_failures}")
    print(f"nontrivial_anchor_zero_iff_nontrivial_quotient_zero_failures={zero_equivalence_failures}")
    print(f"random_nonzero_anchor_projectors={random_nonzero_anchor_projectors}/{TRIALS}")
    print(f"random_nonzero_quotient_projections={random_nonzero_quotient_projections}/{TRIALS}")
    print("interpretation")
    print("  anchor_projectors_are_relabelled_H_quotient_characters_under_covariance=1")
    print("  p24_shift6_pairs_projector_indices_1_6_2_5_3_4=1")
    print("  proving_six_anchor_projectors_zero_is_same_as_1092_nontrivial_payload=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_projector_character_bridge")

    if shift != 6 or shift_inverse != 6:
        raise SystemExit(1)
    if index_map != [0, 6, 5, 4, 3, 2, 1]:
        raise SystemExit(1)
    if bridge_failures or zero_equivalence_failures:
        raise SystemExit(1)
    if random_nonzero_anchor_projectors != TRIALS:
        raise SystemExit(1)
    if random_nonzero_quotient_projections != TRIALS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

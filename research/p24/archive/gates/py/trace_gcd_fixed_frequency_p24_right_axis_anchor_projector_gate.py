#!/usr/bin/env python3
"""Rho-eigenprojector form of the p24 right-axis anchor target.

After the seven-coset covariance gate, the finite theorem needs one anchor
H-coset sum Y_0 to be fixed by rho=p^780.  Since rho has order 7 on the
right quotient and the coefficient field contains mu_7, this is equivalent to
six explicit projector vanishings

    Pi_k(Y_0) = (1/7) sum_{j=0}^6 omega^(-k*j) rho^j(Y_0),  k=1,...,6.

This gate keeps that dictionary small.  The abstract projector algebra is
tested in an order-7 Frobenius quotient model.  The pure H-period control is
tested separately in a split prime field containing both mu_211 and mu_7,
where the rho action on the anchor orbit is just the induced permutation of
the seven H-cosets.
"""

from __future__ import annotations

import random

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
H_STEP = 7
ORDER7 = 7
RHO_EXPONENT = 780
PROJECTOR_MODEL_Q = 43
PROJECTOR_MODEL_DEGREE = 7
PERIOD_CONTROL_Q = 8863
SEED = 20260606
TRIALS = 24


FpE = tuple[int, ...]


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


def h_coset(coset_index: int, logs: dict[int, int]) -> list[int]:
    return [
        value
        for value in range(1, RIGHT)
        if logs[value] % H_STEP == coset_index
    ]


def add_all(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def rho_orbit(value: FpE, field: ExtensionField) -> list[FpE]:
    orbit: list[FpE] = []
    current = value
    for _step in range(ORDER7):
        orbit.append(current)
        current = frobenius(current, field)
    if current != value:
        raise RuntimeError("projector model Frobenius orbit did not close")
    return orbit


def projector_from_orbit(
    orbit: list[FpE],
    field: ExtensionField,
    omega7: int,
    character_index: int,
) -> FpE:
    total = field.zero
    inv7 = pow(ORDER7, -1, field.q)
    for step, value in enumerate(orbit):
        weight = pow(omega7, (-character_index * step) % ORDER7, field.q)
        total = field.add(total, field.scalar_mul(weight, value))
    return field.scalar_mul(inv7, total)


def all_projectors(value: FpE, field: ExtensionField, omega7: int) -> list[FpE]:
    orbit = rho_orbit(value, field)
    return [
        projector_from_orbit(orbit, field, omega7, index)
        for index in range(ORDER7)
    ]


def nontrivial_projectors_zero(value: FpE, field: ExtensionField, omega7: int) -> bool:
    return all(projector == field.zero for projector in all_projectors(value, field, omega7)[1:])


def is_rho_fixed(value: FpE, field: ExtensionField) -> bool:
    return frobenius(value, field) == value


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    return tuple(rng.randrange(field.q) for _index in range(field.degree))


def random_nonfixed_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = random_element(rng, field)
        if not is_rho_fixed(value, field):
            return value


def force_rho_fixed(value: FpE, field: ExtensionField) -> FpE:
    orbit = rho_orbit(value, field)
    return field.scalar_mul(pow(ORDER7, -1, field.q), add_all(orbit, field))


def projector_sum(projectors: list[FpE], field: ExtensionField) -> FpE:
    return add_all(projectors, field)


def projector_idempotent_failures(value: FpE, field: ExtensionField, omega7: int) -> int:
    failures = 0
    projectors = all_projectors(value, field, omega7)
    failures += int(projector_sum(projectors, field) != value)
    for index, component in enumerate(projectors):
        projected_again = all_projectors(component, field, omega7)
        for second_index, second_component in enumerate(projected_again):
            expected = component if second_index == index else field.zero
            failures += int(second_component != expected)
        eigen_expected = field.scalar_mul(pow(omega7, index, field.q), component)
        failures += int(frobenius(component, field) != eigen_expected)
    return failures


def split_period_projector(orbit: list[int], q: int, omega7: int, character_index: int) -> int:
    inv7 = pow(ORDER7, -1, q)
    total = 0
    for step, value in enumerate(orbit):
        weight = pow(omega7, (-character_index * step) % ORDER7, q)
        total = (total + weight * value) % q
    return inv7 * total % q


def pure_h_period_control(
    logs: dict[int, int],
    rho_shift: int,
) -> tuple[int, int, int, int]:
    root = primitive_root(PERIOD_CONTROL_Q)
    zeta211 = pow(root, (PERIOD_CONTROL_Q - 1) // RIGHT, PERIOD_CONTROL_Q)
    omega7 = pow(root, (PERIOD_CONTROL_Q - 1) // ORDER7, PERIOD_CONTROL_Q)
    periods = [
        sum(pow(zeta211, residue, PERIOD_CONTROL_Q) for residue in h_coset(coset, logs))
        % PERIOD_CONTROL_Q
        for coset in range(ORDER7)
    ]
    orbit = [periods[(step * rho_shift) % ORDER7] for step in range(ORDER7)]
    projectors = [
        split_period_projector(orbit, PERIOD_CONTROL_Q, omega7, index)
        for index in range(ORDER7)
    ]
    nontrivial_nonzero = sum(int(component != 0) for component in projectors[1:])
    anchor_fixed = int(orbit[1] == orbit[0])
    equal_cosets = int(len(set(periods)) == 1)
    return anchor_fixed, nontrivial_nonzero, equal_cosets, omega7


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    p_log = logs[P24 % RIGHT]
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_right]
    rho_shift = rho_log % ORDER7

    field = ExtensionField(
        PROJECTOR_MODEL_Q,
        PROJECTOR_MODEL_DEGREE,
        find_irreducible_modulus(PROJECTOR_MODEL_Q, PROJECTOR_MODEL_DEGREE, SEED),
    )
    omega7 = pow(
        primitive_root(PROJECTOR_MODEL_Q),
        (PROJECTOR_MODEL_Q - 1) // ORDER7,
        PROJECTOR_MODEL_Q,
    )
    rng = random.Random(SEED)

    equivalence_failures = 0
    random_fixed_count = 0
    forced_fixed_count = 0
    forced_nontrivial_zero_count = 0
    idempotent_failures = 0

    for _trial in range(TRIALS):
        value = random_nonfixed_element(rng, field)
        forced = force_rho_fixed(value, field)
        equivalence_failures += int(
            is_rho_fixed(value, field)
            != nontrivial_projectors_zero(value, field, omega7)
        )
        equivalence_failures += int(
            is_rho_fixed(forced, field)
            != nontrivial_projectors_zero(forced, field, omega7)
        )
        random_fixed_count += int(is_rho_fixed(value, field))
        forced_fixed_count += int(is_rho_fixed(forced, field))
        forced_nontrivial_zero_count += int(
            nontrivial_projectors_zero(forced, field, omega7)
        )
        idempotent_failures += projector_idempotent_failures(value, field, omega7)

    (
        pure_anchor_fixed,
        pure_nontrivial_nonzero,
        pure_equal_cosets,
        split_omega7,
    ) = pure_h_period_control(logs, rho_shift)

    print("Trace-GCD fixed-frequency p24 right-axis anchor projector gate")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"p24_mod_211={P24 % RIGHT}")
    print(f"p24_log_base2_mod_211={p_log}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_log_mod_order7_quotient={rho_shift}")
    print(f"projector_model_q={PROJECTOR_MODEL_Q}")
    print(f"projector_model_degree={PROJECTOR_MODEL_DEGREE}")
    print(f"projector_model_omega7={omega7}")
    print(f"period_control_field_q={PERIOD_CONTROL_Q}")
    print(f"period_control_omega7={split_omega7}")
    print(f"projector_idempotent_failures={idempotent_failures}")
    print(f"anchor_fixed_iff_nontrivial_projectors_zero_failures={equivalence_failures}")
    print(f"random_anchor_fixed_count={random_fixed_count}/{TRIALS}")
    print(f"forced_anchor_fixed_count={forced_fixed_count}/{TRIALS}")
    print(f"forced_anchor_nontrivial_projectors_zero={forced_nontrivial_zero_count}/{TRIALS}")
    print(f"pure_H_anchor_fixed={pure_anchor_fixed}")
    print(f"pure_H_anchor_equal_cosets={pure_equal_cosets}")
    print(f"pure_H_anchor_nontrivial_projectors_nonzero={pure_nontrivial_nonzero}/6")
    print("interpretation")
    print("  anchor_fixedness_is_six_rho_eigenprojector_vanishings=1")
    print("  pure_H_periods_show_the_missing_theorem_is_real_cancellation=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_anchor_projector_gate")


if __name__ == "__main__":
    main()

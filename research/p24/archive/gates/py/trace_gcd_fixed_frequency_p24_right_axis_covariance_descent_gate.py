#!/usr/bin/env python3
"""Seven-coset covariance-plus-descent gate for the p24 right-axis target.

The current p24 obstruction has been reduced to the order-7 spectrum of the
internally traced G_chi right profile.  Let Y_c be the seven H-coset sums on
F_211^*, indexed by c=log_2(r) mod 7.  The p24 arithmetic gives:

    rho = p^780 fixes F_p(mu_157),
    rho shifts c by 6 mod 7 on the right 211 quotient,
    rho^7 = p^5460 fixes the whole right 211 axis.

This gate isolates the finite implication now worth proving arithmetically:

    Y_{c+6} = rho(Y_c)   and   rho(Y_0) = Y_0
    ------------------------------------------------------
                  all seven H-coset sums are equal.

Equivalently, the six nontrivial order-7 character projections vanish.  The
negative controls record that covariance alone and descent alone both leave
the order-7 spectrum generically nonzero.
"""

from __future__ import annotations

import random

from k_character_tensor_rank_scan import ExtensionField, find_irreducible_modulus


P24 = 10**24 + 7
LEFT = 157
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
FIELD_Q = 43
FIELD_DEGREE = 7
RHO_EXPONENT = 780
INTERNAL_EXPONENT = 5460
SEED = 20260606
TRIALS = 48


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


def frobenius(value: FpE, field: ExtensionField) -> FpE:
    return field.pow(value, field.q)


def is_fixed(value: FpE, field: ExtensionField) -> bool:
    return frobenius(value, field) == value


def random_element(rng: random.Random, field: ExtensionField) -> FpE:
    return tuple(rng.randrange(field.q) for _index in range(field.degree))


def random_nonfixed_element(rng: random.Random, field: ExtensionField) -> FpE:
    while True:
        value = random_element(rng, field)
        if not is_fixed(value, field):
            return value


def random_base_element(rng: random.Random, field: ExtensionField) -> FpE:
    return field.embed(rng.randrange(field.q))


def add_all(values: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def scalar_mul(scalar: int, value: FpE, field: ExtensionField) -> FpE:
    return field.scalar_mul(scalar, value)


def projection(profile: Profile, zeta7: int, index: int, field: ExtensionField) -> FpE:
    terms: list[FpE] = []
    for coset, value in enumerate(profile):
        weight = pow(zeta7, (-index * coset) % ORDER7, field.q)
        terms.append(scalar_mul(weight, value, field))
    return add_all(terms, field)


def projections_all_zero(profile: Profile, zeta7: int, field: ExtensionField) -> bool:
    return all(
        projection(profile, zeta7, index, field) == field.zero
        for index in range(1, ORDER7)
    )


def coset_sums_equal(profile: Profile) -> bool:
    return len(set(profile)) == 1


def profile_descended(profile: Profile, field: ExtensionField) -> bool:
    return all(is_fixed(value, field) for value in profile)


def covariant_profile(seed: FpE, shift: int, field: ExtensionField) -> Profile:
    profile = [field.zero] * ORDER7
    coset = 0
    value = seed
    for _step in range(ORDER7):
        profile[coset] = value
        coset = (coset + shift) % ORDER7
        value = frobenius(value, field)
    if coset != 0 or value != seed:
        raise RuntimeError("rho orbit did not close")
    return profile


def random_descended_profile(rng: random.Random, field: ExtensionField) -> Profile:
    return [random_base_element(rng, field) for _index in range(ORDER7)]


def random_profile(rng: random.Random, field: ExtensionField) -> Profile:
    return [random_element(rng, field) for _index in range(ORDER7)]


def covariance_failures(profile: Profile, shift: int, field: ExtensionField) -> int:
    failures = 0
    for coset, value in enumerate(profile):
        failures += int(profile[(coset + shift) % ORDER7] != frobenius(value, field))
    return failures


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    p_log = logs[P24 % RIGHT]
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_right]
    internal_right = pow(P24, INTERNAL_EXPONENT, RIGHT)
    internal_log = logs[internal_right]
    shift = rho_log % ORDER7
    rho_fixes_left = pow(P24, RHO_EXPONENT, LEFT) == 1

    zeta7 = pow(primitive_root(FIELD_Q), (FIELD_Q - 1) // ORDER7, FIELD_Q)
    field = ExtensionField(
        FIELD_Q,
        FIELD_DEGREE,
        find_irreducible_modulus(FIELD_Q, FIELD_DEGREE, SEED),
    )
    rng = random.Random(SEED)

    covariance_alone_leaks = 0
    covariance_alone_equal = 0
    covariance_alone_descended = 0
    covariance_alone_failures = 0
    descent_alone_leaks = 0
    descent_alone_equal = 0
    descent_alone_covariant = 0
    descent_alone_descended = 0
    covariance_plus_descent_zero = 0
    covariance_plus_descent_equal = 0
    covariance_plus_descent_failures = 0
    covariance_plus_descent_descended = 0
    covariant_zero_iff_anchor_descends_failures = 0
    projection_equal_equivalence_failures = 0

    for _trial in range(TRIALS):
        nonfixed_seed = random_nonfixed_element(rng, field)
        covariant = covariant_profile(nonfixed_seed, shift, field)
        covariance_alone_leaks += int(not projections_all_zero(covariant, zeta7, field))
        covariance_alone_equal += int(coset_sums_equal(covariant))
        covariance_alone_descended += int(profile_descended(covariant, field))
        covariance_alone_failures += covariance_failures(covariant, shift, field)
        covariant_zero_iff_anchor_descends_failures += int(
            projections_all_zero(covariant, zeta7, field)
            != is_fixed(covariant[0], field)
        )

        descended = random_descended_profile(rng, field)
        descent_alone_leaks += int(not projections_all_zero(descended, zeta7, field))
        descent_alone_equal += int(coset_sums_equal(descended))
        descent_alone_covariant += int(covariance_failures(descended, shift, field) == 0)
        descent_alone_descended += int(profile_descended(descended, field))

        base_seed = random_base_element(rng, field)
        descended_covariant = covariant_profile(base_seed, shift, field)
        covariance_plus_descent_zero += int(
            projections_all_zero(descended_covariant, zeta7, field)
        )
        covariance_plus_descent_equal += int(coset_sums_equal(descended_covariant))
        covariance_plus_descent_failures += covariance_failures(
            descended_covariant,
            shift,
            field,
        )
        covariance_plus_descent_descended += int(
            profile_descended(descended_covariant, field)
        )
        covariant_zero_iff_anchor_descends_failures += int(
            projections_all_zero(descended_covariant, zeta7, field)
            != is_fixed(descended_covariant[0], field)
        )

        arbitrary = random_profile(rng, field)
        projection_equal_equivalence_failures += int(
            projections_all_zero(arbitrary, zeta7, field) != coset_sums_equal(arbitrary)
        )

    print("Trace-GCD fixed-frequency p24 right-axis covariance descent gate")
    print(f"p24={P24}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"field_q={FIELD_Q}")
    print(f"field_degree={FIELD_DEGREE}")
    print(f"zeta7={zeta7}")
    print(f"p24_mod_157={P24 % LEFT}")
    print(f"p24_mod_211={P24 % RIGHT}")
    print(f"p24_log_base2_mod_211={p_log}")
    print(f"p24_log_mod_order7_quotient={p_log % ORDER7}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_fixes_left157={int(rho_fixes_left)}")
    print(f"rho_mod_211={rho_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_log_mod_order7_quotient={shift}")
    print(f"internal_exponent={INTERNAL_EXPONENT}")
    print(f"internal_mod_211={internal_right}")
    print(f"internal_log_base2_mod_211={internal_log}")
    print(f"internal_log_mod_order7_quotient={internal_log % ORDER7}")
    print(f"trials={TRIALS}")
    print(f"covariance_alone_order7_leak={covariance_alone_leaks}/{TRIALS}")
    print(f"covariance_alone_equal_H_coset_sums={covariance_alone_equal}/{TRIALS}")
    print(f"covariance_alone_descended={covariance_alone_descended}/{TRIALS}")
    print(f"covariance_alone_failures={covariance_alone_failures}")
    print(f"descent_alone_order7_leak={descent_alone_leaks}/{TRIALS}")
    print(f"descent_alone_equal_H_coset_sums={descent_alone_equal}/{TRIALS}")
    print(f"descent_alone_covariant={descent_alone_covariant}/{TRIALS}")
    print(f"descent_alone_descended={descent_alone_descended}/{TRIALS}")
    print(f"covariance_plus_descent_projection_zero={covariance_plus_descent_zero}/{TRIALS}")
    print(f"covariance_plus_descent_equal_H_coset_sums={covariance_plus_descent_equal}/{TRIALS}")
    print(f"covariance_plus_descent_failures={covariance_plus_descent_failures}")
    print(f"covariance_plus_descent_descended={covariance_plus_descent_descended}/{TRIALS}")
    print(
        "covariant_projection_zero_iff_anchor_descends_failures="
        f"{covariant_zero_iff_anchor_descends_failures}"
    )
    print(f"projection_zero_iff_equal_H_coset_sums_failures={projection_equal_equivalence_failures}")
    print("interpretation")
    print("  p780_fixes_left157=1")
    print("  p780_shifts_right_order7_quotient_by_6=1")
    print("  p5460_internal_trace_fixes_right_211_axis=1")
    print("  covariance_alone_gives_conjugate_coset_sums_not_equality=1")
    print("  descent_alone_does_not_force_coset_equality=1")
    print("  under_covariance_one_anchor_descent_is_equivalent_to_H_coset_equality=1")
    print("  right_axis_covariance_plus_descent_forces_H_coset_sums_equal=1")
    print("  remaining_arithmetic_is_covariance_and_descent_for_traced_G_chi_profile=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_covariance_descent_gate")

    if p_log % ORDER7 != 2:
        raise SystemExit(1)
    if shift != 6:
        raise SystemExit(1)
    if not rho_fixes_left:
        raise SystemExit(1)
    if internal_log != 0:
        raise SystemExit(1)
    if covariance_alone_leaks != TRIALS or covariance_alone_equal != 0:
        raise SystemExit(1)
    if covariance_alone_descended != 0 or covariance_alone_failures:
        raise SystemExit(1)
    if descent_alone_leaks != TRIALS or descent_alone_equal != 0:
        raise SystemExit(1)
    if descent_alone_covariant != 0 or descent_alone_descended != TRIALS:
        raise SystemExit(1)
    if covariance_plus_descent_zero != TRIALS:
        raise SystemExit(1)
    if covariance_plus_descent_equal != TRIALS:
        raise SystemExit(1)
    if covariance_plus_descent_failures or covariance_plus_descent_descended != TRIALS:
        raise SystemExit(1)
    if covariant_zero_iff_anchor_descends_failures:
        raise SystemExit(1)
    if projection_equal_equivalence_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Auxiliary-prime invariance probe for the McCarthy q-power projection.

The powered McCarthy route currently works in the auxiliary value field

    F_20574061,  20574061 = 1 + 2029*2028*5.

There the target quotient satisfies

    R(138)^2029 in mu_39.

If q-power projection were a theorem-stable Gauss/Jacobi normalization, one
would expect the same behavior after recomputing the same McCarthy quotient in
other auxiliary prime fields containing the same required roots of unity.

This probe recomputes only the target twist q=138 for three primes
`ell = 1 mod 2029*2028*5`.  The result is negative: the next auxiliary primes
leave extra root components after `x -> x^2029`.  This does not refute
McCarthy's exceptional delta theorem.  It does make the post-hoc q-power
projection look specific to the minimal auxiliary residue field, unless a
theorem supplies an invariant quotient-level cancellation or a natural
mod-`mu_2029` interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    BASE_FIELD_Q,
    BASE_PRIMITIVE_ROOT,
    CHARACTER_ORDER,
    ORDER_507_STEP,
    TARGET_Q_EXP,
    X_VALUE,
    factor_distinct,
    is_primitive_root,
)


REQUIRED_ROOT_STEP = BASE_FIELD_Q * CHARACTER_ORDER * 5
PROBE_MULTIPLIERS = (1, 4, 7)
MU39_ORDER = 39


@dataclass(frozen=True)
class AuxiliaryPrimeTargetProfile:
    multiplier: int
    value_field: int
    primitive_root: int
    lower_1f0_value: int
    lhs_target_value: int
    main_target_value: int
    transformed_difference_value: int
    quotient_target_value: int
    quotient_target_order: int
    q_power_value: int
    q_power_order: int
    q_power_in_mu39: bool
    q_power_in_mu2028: bool
    q_power_mu39_exponent: int | None
    quotient_additive_exponent: int | None
    quotient_mu5_exponent: int | None
    extra_component_after_q_power: bool


@dataclass(frozen=True)
class AuxiliaryPrimeInvarianceProfile:
    required_root_step: int
    probe_multipliers: tuple[int, ...]
    target_q_exp: int
    prime_profiles: tuple[AuxiliaryPrimeTargetProfile, ...]
    minimal_prime_projection_ok: bool
    other_primes_projection_ok: tuple[bool, ...]
    q_power_projection_aux_prime_invariant: bool
    posthoc_projection_is_representation_specific: bool


def factor_distinct_with_exp(value: int) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            exponent = 0
            while value % divisor == 0:
                value //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append((value, 1))
    return tuple(factors)


def primitive_root_for(modulus: int) -> int:
    candidate = 2
    while True:
        if is_primitive_root(candidate, modulus):
            return candidate
        candidate += 1


def multiplicative_order_mod(value: int, modulus: int) -> int:
    if value % modulus == 0:
        raise AssertionError("zero has no multiplicative order")
    order = modulus - 1
    for prime, exponent in factor_distinct_with_exp(modulus - 1):
        for _ in range(exponent):
            if order % prime == 0 and pow(value, order // prime, modulus) == 1:
                order //= prime
            else:
                break
    return order


def discrete_log_small(
    root: int,
    value: int,
    order: int,
    modulus: int,
) -> int | None:
    current = 1
    for exponent in range(order):
        if current == value:
            return exponent
        current = current * root % modulus
    return None


class AuxiliaryMcCarthyContext:
    def __init__(self, value_field: int) -> None:
        if (value_field - 1) % REQUIRED_ROOT_STEP != 0:
            raise AssertionError("auxiliary field does not contain required roots")
        self.value_field = value_field
        self.primitive_root = primitive_root_for(value_field)
        self.zeta = pow(
            self.primitive_root,
            (value_field - 1) // CHARACTER_ORDER,
            value_field,
        )
        self.additive_root = pow(
            self.primitive_root,
            (value_field - 1) // BASE_FIELD_Q,
            value_field,
        )
        self.logs, self.antilogs = self._log_tables()
        self.gauss = self._gauss_sums()
        self.inv_gauss = [self.inverse(value) for value in self.gauss]
        self.inv_character_order = self.inverse(CHARACTER_ORDER)

    def inverse(self, value: int) -> int:
        return pow(value % self.value_field, self.value_field - 2, self.value_field)

    def _log_tables(self) -> tuple[list[int | None], list[int]]:
        logs: list[int | None] = [None] * BASE_FIELD_Q
        antilogs: list[int] = []
        value = 1
        for exponent in range(CHARACTER_ORDER):
            logs[value] = exponent
            antilogs.append(value)
            value = value * BASE_PRIMITIVE_ROOT % BASE_FIELD_Q
        if value != 1:
            raise AssertionError("base primitive root did not cycle")
        return logs, antilogs

    def _gauss_sums(self) -> list[int]:
        additive_values = [
            pow(self.additive_root, value, self.value_field)
            for value in range(BASE_FIELD_Q)
        ]
        sums: list[int] = []
        for exponent in range(CHARACTER_ORDER):
            ratio = pow(self.zeta, exponent, self.value_field)
            character_value = 1
            total = 0
            for field_value in self.antilogs:
                total = (
                    total
                    + character_value * additive_values[field_value]
                ) % self.value_field
                character_value = character_value * ratio % self.value_field
            sums.append(total)
        if sums[0] != self.value_field - 1:
            raise AssertionError("trivial Gauss sum should be -1")
        if any(value == 0 for value in sums):
            raise AssertionError("Gauss sum vanished in auxiliary field")
        return sums

    def character_value(self, exponent: int, field_value: int) -> int:
        if field_value % BASE_FIELD_Q == 0:
            return 0
        log_value = self.logs[field_value % BASE_FIELD_Q]
        if log_value is None:
            raise AssertionError("missing log")
        return pow(
            self.zeta,
            (exponent % CHARACTER_ORDER) * log_value,
            self.value_field,
        )

    def hypergeo_star(
        self,
        top: tuple[int, ...],
        bottom: tuple[int, ...],
        x_value: int,
    ) -> int:
        n_value = len(bottom)
        if len(top) != n_value + 1:
            raise AssertionError("McCarthy star needs len(top)=len(bottom)+1")
        character_arg = ((-1) ** (n_value + 1) * (x_value % BASE_FIELD_Q)) % BASE_FIELD_Q
        total = 0
        for chi_exp in range(CHARACTER_ORDER):
            term = 1
            for top_exp in top:
                term = (
                    term
                    * self.gauss[(top_exp + chi_exp) % CHARACTER_ORDER]
                    % self.value_field
                    * self.inv_gauss[top_exp % CHARACTER_ORDER]
                    % self.value_field
                )
            for bottom_exp in bottom:
                term = (
                    term
                    * self.gauss[-(bottom_exp + chi_exp) % CHARACTER_ORDER]
                    % self.value_field
                    * self.inv_gauss[-bottom_exp % CHARACTER_ORDER]
                    % self.value_field
                )
            term = (
                term
                * self.gauss[-chi_exp % CHARACTER_ORDER]
                % self.value_field
                * self.character_value(chi_exp, character_arg)
                % self.value_field
            )
            total = (total + term) % self.value_field
        return total * self.inv_character_order % self.value_field


def target_profile_for_multiplier(multiplier: int) -> AuxiliaryPrimeTargetProfile:
    value_field = REQUIRED_ROOT_STEP * multiplier + 1
    if factor_distinct(value_field) == set():
        raise AssertionError("unreachable primality sanity branch")
    ctx = AuxiliaryMcCarthyContext(value_field)
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    a1_exp = 0
    a2_exp = ORDER_507_STEP * TARGET_Q_EXP
    lower_1f0 = ctx.hypergeo_star((a0_exp,), (), X_VALUE)
    inner_2f1 = tuple(
        ctx.hypergeo_star(
            (a0_exp, (-psi_exp) % CHARACTER_ORDER),
            ((a0_exp + psi_exp) % CHARACTER_ORDER,),
            (-X_VALUE) % BASE_FIELD_Q,
        )
        for psi_exp in range(CHARACTER_ORDER)
    )
    lhs = ctx.hypergeo_star(
        (a0_exp, a1_exp, a2_exp),
        (
            (a0_exp - a1_exp) % CHARACTER_ORDER,
            (a0_exp - a2_exp) % CHARACTER_ORDER,
        ),
        X_VALUE,
    )
    denominator = (
        ctx.gauss[a1_exp]
        * ctx.gauss[a2_exp]
        % value_field
        * ctx.gauss[(-a0_exp + a1_exp) % CHARACTER_ORDER]
        % value_field
        * ctx.gauss[(-a0_exp + a2_exp) % CHARACTER_ORDER]
        % value_field
    )
    prefactor = (
        ctx.gauss[(-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER]
        * ctx.inverse(denominator)
        % value_field
    )
    main_sum = 0
    for psi_exp in range(CHARACTER_ORDER):
        term = (
            ctx.gauss[(a1_exp + psi_exp) % CHARACTER_ORDER]
            * ctx.gauss[(a2_exp + psi_exp) % CHARACTER_ORDER]
            % value_field
            * ctx.gauss[-psi_exp % CHARACTER_ORDER]
            % value_field
            * ctx.gauss[(-a0_exp - psi_exp) % CHARACTER_ORDER]
            % value_field
            * inner_2f1[psi_exp]
            % value_field
        )
        main_sum = (main_sum + term) % value_field
    main_term = prefactor * main_sum % value_field * ctx.inv_character_order % value_field
    quotient = lhs * ctx.inverse(main_term) % value_field
    q_power = pow(quotient, BASE_FIELD_Q, value_field)
    zeta39 = pow(ctx.primitive_root, (value_field - 1) // MU39_ORDER, value_field)
    additive_root = pow(ctx.primitive_root, (value_field - 1) // BASE_FIELD_Q, value_field)
    mu5_root = pow(ctx.primitive_root, (value_field - 1) // 5, value_field)
    additive_power_exponent = discrete_log_small(
        additive_root,
        pow(quotient, MU39_ORDER, value_field),
        BASE_FIELD_Q,
        value_field,
    )
    additive_exponent = (
        None
        if additive_power_exponent is None
        else additive_power_exponent * pow(MU39_ORDER, -1, BASE_FIELD_Q) % BASE_FIELD_Q
    )
    mu5_exponent = discrete_log_small(
        mu5_root,
        pow(quotient, BASE_FIELD_Q * CHARACTER_ORDER, value_field),
        5,
        value_field,
    )
    q_power_in_mu39 = pow(q_power, MU39_ORDER, value_field) == 1
    q_power_in_mu2028 = pow(q_power, CHARACTER_ORDER, value_field) == 1

    return AuxiliaryPrimeTargetProfile(
        multiplier=multiplier,
        value_field=value_field,
        primitive_root=ctx.primitive_root,
        lower_1f0_value=lower_1f0,
        lhs_target_value=lhs,
        main_target_value=main_term,
        transformed_difference_value=(lhs - main_term) % value_field,
        quotient_target_value=quotient,
        quotient_target_order=multiplicative_order_mod(quotient, value_field),
        q_power_value=q_power,
        q_power_order=multiplicative_order_mod(q_power, value_field),
        q_power_in_mu39=q_power_in_mu39,
        q_power_in_mu2028=q_power_in_mu2028,
        q_power_mu39_exponent=discrete_log_small(
            zeta39,
            q_power,
            MU39_ORDER,
            value_field,
        ),
        quotient_additive_exponent=additive_exponent,
        quotient_mu5_exponent=mu5_exponent,
        extra_component_after_q_power=not q_power_in_mu39,
    )


def mccarthy_aux_prime_invariance_profile() -> AuxiliaryPrimeInvarianceProfile:
    prime_profiles = tuple(
        target_profile_for_multiplier(multiplier)
        for multiplier in PROBE_MULTIPLIERS
    )
    minimal = prime_profiles[0]
    other_projection_ok = tuple(profile.q_power_in_mu39 for profile in prime_profiles[1:])
    invariant = all(profile.q_power_in_mu39 for profile in prime_profiles)
    return AuxiliaryPrimeInvarianceProfile(
        required_root_step=REQUIRED_ROOT_STEP,
        probe_multipliers=PROBE_MULTIPLIERS,
        target_q_exp=TARGET_Q_EXP,
        prime_profiles=prime_profiles,
        minimal_prime_projection_ok=(
            minimal.multiplier == 1
            and minimal.value_field == 20574061
            and minimal.q_power_order == 39
            and minimal.q_power_mu39_exponent == 5
            and minimal.quotient_additive_exponent == 1475
        ),
        other_primes_projection_ok=other_projection_ok,
        q_power_projection_aux_prime_invariant=invariant,
        posthoc_projection_is_representation_specific=(
            prime_profiles[0].q_power_in_mu39
            and not any(profile.q_power_in_mu39 for profile in prime_profiles[1:])
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy auxiliary-prime invariance probe")
    profile = mccarthy_aux_prime_invariance_profile()
    row_ok = (
        profile.required_root_step == 20574060
        and profile.probe_multipliers == (1, 4, 7)
        and profile.target_q_exp == 138
        and profile.prime_profiles[0].value_field == 20574061
        and profile.prime_profiles[0].primitive_root == 2
        and profile.prime_profiles[0].transformed_difference_value == 2028
        and profile.prime_profiles[0].quotient_target_order == 79131
        and profile.prime_profiles[0].q_power_order == 39
        and profile.prime_profiles[0].q_power_mu39_exponent == 5
        and profile.prime_profiles[0].quotient_additive_exponent == 1475
        and profile.prime_profiles[0].quotient_mu5_exponent == 0
        and profile.prime_profiles[1].value_field == 82296241
        and profile.prime_profiles[1].primitive_root == 38
        and profile.prime_profiles[1].transformed_difference_value == 2028
        and profile.prime_profiles[1].quotient_target_order == 10287030
        and profile.prime_profiles[1].q_power_order == 5070
        and profile.prime_profiles[1].q_power_mu39_exponent is None
        and profile.prime_profiles[1].quotient_additive_exponent is None
        and profile.prime_profiles[1].quotient_mu5_exponent == 2
        and profile.prime_profiles[2].value_field == 144018421
        and profile.prime_profiles[2].primitive_root == 11
        and profile.prime_profiles[2].transformed_difference_value == 2028
        and profile.prime_profiles[2].quotient_target_order == 48006140
        and profile.prime_profiles[2].q_power_order == 23660
        and profile.prime_profiles[2].q_power_mu39_exponent is None
        and profile.prime_profiles[2].quotient_additive_exponent is None
        and profile.prime_profiles[2].quotient_mu5_exponent is None
        and profile.minimal_prime_projection_ok
        and profile.other_primes_projection_ok == (False, False)
        and not profile.q_power_projection_aux_prime_invariant
        and profile.posthoc_projection_is_representation_specific
    )

    print(f"mccarthy_aux_prime_invariance_profile={profile}")
    print("aux_prime_projection_laws")
    print("  minimal_auxiliary_prime_has_R_138_to_the_2029_in_mu39=1")
    print("  next_two_auxiliary_primes_leave_extra_components_after_2029_power=1")
    print("  transformed_difference_value_2028_is_stable_at_q_138=1")
    print("interpretation")
    print("  mccarthy_exceptional_delta_is_still_the_theorem_hook=1")
    print("  posthoc_q_power_projection_is_not_auxiliary_prime_invariant=1")
    print("  need_theorem_level_cancellation_or_mod_mu2029_interpretation=1")
    print(f"square_axis_mccarthy_aux_prime_invariance_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

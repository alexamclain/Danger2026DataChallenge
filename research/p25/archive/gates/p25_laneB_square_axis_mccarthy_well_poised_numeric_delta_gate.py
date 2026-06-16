#!/usr/bin/env python3
"""Numeric McCarthy well-poised delta check over F_2029.

The support contract gate checked only the exponent geometry of McCarthy's
exceptional term.  This gate instantiates Theorem 1.7 from McCarthy's
"Transformations of Well-Poised Hypergeometric Functions over Finite Fields"
for n=2 over F_2029 and verifies the transformed-difference support directly.

We vary A_2 through the order-507 character subgroup by setting

    A_2(q_exp) = omega^(4*q_exp)

inside the full character group of order 2028.  With A_1 trivial and
A_0 = omega^(4*138), the theorem's exceptional character delta

    delta(bar(A_0) * A_1 * A_2)

fires exactly at q_exp=138.  For x=2 the lower 1F0 factor is nonzero.  The
checked result is:

    support_qexp(LHS - main_sum) = {138},

with the theorem identity `LHS - main_sum = exceptional_term` holding for all
507 q_exp values.
"""

from __future__ import annotations

from dataclasses import dataclass


BASE_FIELD_Q = 2029
CHARACTER_ORDER = BASE_FIELD_Q - 1
VALUE_FIELD = 20574061
VALUE_FIELD_MULTIPLIER = 5
ORDER_507_STEP = 4
TARGET_Q_EXP = 138
X_VALUE = 2
BASE_PRIMITIVE_ROOT = 2
VALUE_PRIMITIVE_ROOT = 2


@dataclass(frozen=True)
class McCarthyNumericDeltaProfile:
    base_field_q: int
    character_order: int
    value_field: int
    value_field_multiplier: int
    a0_exponent: int
    a1_exponent: int
    x_value: int
    lower_1f0_value: int
    delta_support: tuple[int, ...]
    transformed_difference_support: tuple[int, ...]
    exceptional_support: tuple[int, ...]
    theorem_mismatch_count: int
    transformed_difference_equals_exceptional: bool
    support_matches_target: bool


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.add(value)
    return factors


def is_primitive_root(candidate: int, modulus: int) -> bool:
    return all(
        pow(candidate, (modulus - 1) // factor, modulus) != 1
        for factor in factor_distinct(modulus - 1)
    )


class McCarthyContext:
    def __init__(self) -> None:
        if VALUE_FIELD != VALUE_FIELD_MULTIPLIER * BASE_FIELD_Q * CHARACTER_ORDER + 1:
            raise AssertionError("value field does not contain the required roots")
        if not is_primitive_root(BASE_PRIMITIVE_ROOT, BASE_FIELD_Q):
            raise AssertionError("bad primitive root for base field")
        if not is_primitive_root(VALUE_PRIMITIVE_ROOT, VALUE_FIELD):
            raise AssertionError("bad primitive root for value field")

        self.zeta = pow(
            VALUE_PRIMITIVE_ROOT,
            (VALUE_FIELD - 1) // CHARACTER_ORDER,
            VALUE_FIELD,
        )
        self.additive_root = pow(
            VALUE_PRIMITIVE_ROOT,
            (VALUE_FIELD - 1) // BASE_FIELD_Q,
            VALUE_FIELD,
        )
        self.logs, self.antilogs = self._log_tables()
        self.gauss = self._gauss_sums()
        self.inv_gauss = [self.inverse(value) for value in self.gauss]
        self.inv_character_order = self.inverse(CHARACTER_ORDER)

    @staticmethod
    def inverse(value: int) -> int:
        return pow(value % VALUE_FIELD, VALUE_FIELD - 2, VALUE_FIELD)

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
            pow(self.additive_root, value, VALUE_FIELD) for value in range(BASE_FIELD_Q)
        ]
        sums: list[int] = []
        for exponent in range(CHARACTER_ORDER):
            ratio = pow(self.zeta, exponent, VALUE_FIELD)
            character_value = 1
            total = 0
            for field_value in self.antilogs:
                total = (total + character_value * additive_values[field_value]) % VALUE_FIELD
                character_value = character_value * ratio % VALUE_FIELD
            sums.append(total)
        if sums[0] != VALUE_FIELD - 1:
            raise AssertionError("trivial Gauss sum should be -1")
        if any(value == 0 for value in sums):
            raise AssertionError("Gauss sum vanished in the auxiliary value field")
        return sums

    def character_value(self, exponent: int, field_value: int) -> int:
        if field_value % BASE_FIELD_Q == 0:
            return 0
        log_value = self.logs[field_value % BASE_FIELD_Q]
        if log_value is None:
            raise AssertionError("missing log")
        return pow(self.zeta, (exponent % CHARACTER_ORDER) * log_value, VALUE_FIELD)

    def hypergeo_star(self, top: tuple[int, ...], bottom: tuple[int, ...], x_value: int) -> int:
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
                    % VALUE_FIELD
                    * self.inv_gauss[top_exp % CHARACTER_ORDER]
                    % VALUE_FIELD
                )
            for bottom_exp in bottom:
                term = (
                    term
                    * self.gauss[-(bottom_exp + chi_exp) % CHARACTER_ORDER]
                    % VALUE_FIELD
                    * self.inv_gauss[-bottom_exp % CHARACTER_ORDER]
                    % VALUE_FIELD
                )
            term = (
                term
                * self.gauss[-chi_exp % CHARACTER_ORDER]
                % VALUE_FIELD
                * self.character_value(chi_exp, character_arg)
                % VALUE_FIELD
            )
            total = (total + term) % VALUE_FIELD
        return total * self.inv_character_order % VALUE_FIELD


def mccarthy_numeric_delta_profile() -> McCarthyNumericDeltaProfile:
    ctx = McCarthyContext()
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    a1_exp = 0
    lower_1f0 = ctx.hypergeo_star((a0_exp,), (), X_VALUE)
    inner_2f1 = tuple(
        ctx.hypergeo_star(
            (a0_exp, (-psi_exp) % CHARACTER_ORDER),
            ((a0_exp + psi_exp) % CHARACTER_ORDER,),
            (-X_VALUE) % BASE_FIELD_Q,
        )
        for psi_exp in range(CHARACTER_ORDER)
    )

    delta_support: list[int] = []
    transformed_support: list[int] = []
    exceptional_support: list[int] = []
    mismatch_count = 0

    for q_exp in range(507):
        a2_exp = ORDER_507_STEP * q_exp
        lhs = ctx.hypergeo_star(
            (a0_exp, a1_exp, a2_exp),
            ((a0_exp - a1_exp) % CHARACTER_ORDER, (a0_exp - a2_exp) % CHARACTER_ORDER),
            X_VALUE,
        )
        denominator = (
            ctx.gauss[a1_exp]
            * ctx.gauss[a2_exp]
            % VALUE_FIELD
            * ctx.gauss[(-a0_exp + a1_exp) % CHARACTER_ORDER]
            % VALUE_FIELD
            * ctx.gauss[(-a0_exp + a2_exp) % CHARACTER_ORDER]
            % VALUE_FIELD
        )
        prefactor = (
            ctx.gauss[(-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER]
            * ctx.inverse(denominator)
            % VALUE_FIELD
        )
        main_sum = 0
        for psi_exp in range(CHARACTER_ORDER):
            term = (
                ctx.gauss[(a1_exp + psi_exp) % CHARACTER_ORDER]
                * ctx.gauss[(a2_exp + psi_exp) % CHARACTER_ORDER]
                % VALUE_FIELD
                * ctx.gauss[-psi_exp % CHARACTER_ORDER]
                % VALUE_FIELD
                * ctx.gauss[(-a0_exp - psi_exp) % CHARACTER_ORDER]
                % VALUE_FIELD
                * inner_2f1[psi_exp]
                % VALUE_FIELD
            )
            main_sum = (main_sum + term) % VALUE_FIELD
        main_term = prefactor * main_sum % VALUE_FIELD * ctx.inv_character_order % VALUE_FIELD

        delta_active = (-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER == 0
        if delta_active:
            delta_support.append(q_exp)
        exceptional = (
            BASE_FIELD_Q
            * CHARACTER_ORDER
            % VALUE_FIELD
            * ctx.character_value((a2_exp + a1_exp) % CHARACTER_ORDER, -1)
            % VALUE_FIELD
            * int(delta_active)
            % VALUE_FIELD
            * ctx.inverse(denominator)
            % VALUE_FIELD
            * lower_1f0
            % VALUE_FIELD
        )
        transformed_difference = (lhs - main_term) % VALUE_FIELD
        if transformed_difference:
            transformed_support.append(q_exp)
        if exceptional:
            exceptional_support.append(q_exp)
        if transformed_difference != exceptional:
            mismatch_count += 1

    return McCarthyNumericDeltaProfile(
        base_field_q=BASE_FIELD_Q,
        character_order=CHARACTER_ORDER,
        value_field=VALUE_FIELD,
        value_field_multiplier=VALUE_FIELD_MULTIPLIER,
        a0_exponent=a0_exp,
        a1_exponent=a1_exp,
        x_value=X_VALUE,
        lower_1f0_value=lower_1f0,
        delta_support=tuple(delta_support),
        transformed_difference_support=tuple(transformed_support),
        exceptional_support=tuple(exceptional_support),
        theorem_mismatch_count=mismatch_count,
        transformed_difference_equals_exceptional=mismatch_count == 0,
        support_matches_target=tuple(transformed_support) == (TARGET_Q_EXP,),
    )


def main() -> int:
    print("p25 Lane B McCarthy well-poised numeric delta gate")
    profile = mccarthy_numeric_delta_profile()
    row_ok = (
        profile.base_field_q == 2029
        and profile.character_order == 2028
        and profile.value_field == 20574061
        and profile.value_field_multiplier == 5
        and profile.a0_exponent == 552
        and profile.a1_exponent == 0
        and profile.x_value == 2
        and profile.lower_1f0_value == 1
        and profile.delta_support == (138,)
        and profile.transformed_difference_support == (138,)
        and profile.exceptional_support == (138,)
        and profile.theorem_mismatch_count == 0
        and profile.transformed_difference_equals_exceptional
        and profile.support_matches_target
    )

    print(f"mccarthy_numeric_delta_profile={profile}")
    print("numeric_delta_laws")
    print("  theorem_1_7_checked_for_all_507_order_507_twists=1")
    print("  transformed_difference_support_is_exactly_q_exp_138=1")
    print("  exceptional_term_support_is_exactly_q_exp_138=1")
    print("  lower_1F0_factor_at_x_2_is_nonzero=1")
    print("interpretation")
    print("  mccarthy_well_poised_exceptional_term_is_a_numeric_point_delta_producer=1")
    print("  next_step_is_mapping_this_point_delta_into_the_p25_raw_Y_or_bridge_payload=1")
    print(f"square_axis_mccarthy_well_poised_numeric_delta_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

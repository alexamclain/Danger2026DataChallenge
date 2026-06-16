#!/usr/bin/env python3
"""McCarthy quotient power-descent gate for the p25 square axis.

The unit-quotient gate found that

    R(q) = LHS(q) / main_sum(q)

satisfies `R(q)-1` supported exactly at q=138, but `R(138)` has order
39*2029 in the auxiliary value field.  This gate checks the obvious descent:
raise the quotient to the additive-root order 2029.

Because R(q)=1 away from q=138, every power preserves singleton support unless
the exceptional value becomes 1.  The useful fact is:

    R(138)^2029 = zeta_39^5.

Thus `R(q)^2029` is a character-valued sparse quotient with target order 39.
The direct additive-root obstruction can be killed by power descent.  The
remaining debt is arithmetic/certificate cost: justify the 2029th power before
raw lift, and avoid arbitrary full-order scalar normalization of
`R(q)^2029 - 1`.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_mccarthy_normalization_density_gate import (
    mccarthy_vectors,
    support,
)
from p25_laneB_square_axis_mccarthy_unit_quotient_gate import multiplicative_order
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    TARGET_Q_EXP,
    VALUE_FIELD,
    VALUE_PRIMITIVE_ROOT,
)


ADDITIVE_ROOT_ORDER = 2029
CHARACTER_DESCENT_ORDER = 39
FULL_TARGET_ORDER = ADDITIVE_ROOT_ORDER * CHARACTER_DESCENT_ORDER


@dataclass(frozen=True)
class McCarthyPowerDescentProfile:
    target_q_exp: int
    outer_s_image: tuple[int, ...]
    quotient_target_order: int
    additive_power_support: tuple[int, ...]
    additive_power_target_value: int
    additive_power_target_order: int
    additive_power_zeta39_exponent: int
    additive_power_minus_one_value: int
    additive_power_minus_one_order: int
    character_power_support: tuple[int, ...]
    character_power_target_value: int
    character_power_target_order: int
    full_power_support: tuple[int, ...]
    full_power_target_value: int
    power_descent_preserves_singleton: bool
    power_descent_character_valued: bool
    minus_one_scalar_still_full_order: bool
    live_powered_quotient_route: bool


def zeta39_exponent(value: int) -> int:
    zeta_39 = pow(VALUE_PRIMITIVE_ROOT, (VALUE_FIELD - 1) // CHARACTER_DESCENT_ORDER, VALUE_FIELD)
    current = 1
    for exponent in range(CHARACTER_DESCENT_ORDER):
        if current == value:
            return exponent
        current = current * zeta_39 % VALUE_FIELD
    raise AssertionError("value is not in mu_39")


def powered_minus_one_support(quotient: list[int], power: int) -> tuple[int, ...]:
    return support([(pow(value, power, VALUE_FIELD) - 1) % VALUE_FIELD for value in quotient])


def mccarthy_power_descent_profile() -> McCarthyPowerDescentProfile:
    ctx, _lower_1f0, lhs_vector, main_vector, _difference_vector, _exceptional_vector = (
        mccarthy_vectors()
    )
    quotient = [
        lhs_value * ctx.inverse(main_value) % VALUE_FIELD
        for lhs_value, main_value in zip(lhs_vector, main_vector)
    ]
    target = quotient[TARGET_Q_EXP]
    additive_power_value = pow(target, ADDITIVE_ROOT_ORDER, VALUE_FIELD)
    additive_power_minus_one = (additive_power_value - 1) % VALUE_FIELD
    character_power_value = pow(target, CHARACTER_DESCENT_ORDER, VALUE_FIELD)
    full_power_value = pow(target, FULL_TARGET_ORDER, VALUE_FIELD)

    return McCarthyPowerDescentProfile(
        target_q_exp=TARGET_Q_EXP,
        outer_s_image=tuple(
            sorted((TARGET_Q_EXP + layer * S_STEP) % QUOTIENT_ORDER for layer in range(3))
        ),
        quotient_target_order=multiplicative_order(target),
        additive_power_support=powered_minus_one_support(quotient, ADDITIVE_ROOT_ORDER),
        additive_power_target_value=additive_power_value,
        additive_power_target_order=multiplicative_order(additive_power_value),
        additive_power_zeta39_exponent=zeta39_exponent(additive_power_value),
        additive_power_minus_one_value=additive_power_minus_one,
        additive_power_minus_one_order=multiplicative_order(additive_power_minus_one),
        character_power_support=powered_minus_one_support(quotient, CHARACTER_DESCENT_ORDER),
        character_power_target_value=character_power_value,
        character_power_target_order=multiplicative_order(character_power_value),
        full_power_support=powered_minus_one_support(quotient, FULL_TARGET_ORDER),
        full_power_target_value=full_power_value,
        power_descent_preserves_singleton=powered_minus_one_support(
            quotient, ADDITIVE_ROOT_ORDER
        )
        == (TARGET_Q_EXP,),
        power_descent_character_valued=multiplicative_order(additive_power_value)
        == CHARACTER_DESCENT_ORDER,
        minus_one_scalar_still_full_order=multiplicative_order(additive_power_minus_one)
        == VALUE_FIELD - 1,
        live_powered_quotient_route=(
            powered_minus_one_support(quotient, ADDITIVE_ROOT_ORDER) == (TARGET_Q_EXP,)
            and multiplicative_order(additive_power_value) == CHARACTER_DESCENT_ORDER
            and zeta39_exponent(additive_power_value) == 5
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy quotient power-descent gate")
    profile = mccarthy_power_descent_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.outer_s_image == (138, 310, 482)
        and profile.quotient_target_order == 79131
        and profile.additive_power_support == (138,)
        and profile.additive_power_target_value == 12801419
        and profile.additive_power_target_order == 39
        and profile.additive_power_zeta39_exponent == 5
        and profile.additive_power_minus_one_value == 12801418
        and profile.additive_power_minus_one_order == 20574060
        and profile.character_power_support == (138,)
        and profile.character_power_target_value == 13544166
        and profile.character_power_target_order == 2029
        and profile.full_power_support == ()
        and profile.full_power_target_value == 1
        and profile.power_descent_preserves_singleton
        and profile.power_descent_character_valued
        and profile.minus_one_scalar_still_full_order
        and profile.live_powered_quotient_route
    )

    print(f"mccarthy_power_descent_profile={profile}")
    print("power_descent_laws")
    print("  R(q)^2029_minus_1_is_supported_exactly_at_q_138=1")
    print("  R(138)^2029_is_zeta_39_to_the_5=1")
    print("  R(q)^39_keeps_the_additive_order_2029_component=1")
    print("  R(q)^(39*2029)_minus_1_is_zero_everywhere=1")
    print("  R(138)^2029_minus_1_still_has_full_auxiliary_field_order=1")
    print("interpretation")
    print("  additive_root_component_can_be_killed_by_power_descent=1")
    print("  powered_quotient_is_sparse_and_character_valued=1")
    print("  remaining_debt_is_power_cost_and_nonarbitrary_coefficient_normalization=1")
    print(f"square_axis_mccarthy_power_descent_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_power_descent_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

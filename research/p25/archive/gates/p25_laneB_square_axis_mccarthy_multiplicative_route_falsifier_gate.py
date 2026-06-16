#!/usr/bin/env python3
"""Falsifier for invalid additive q-power routes in the McCarthy target.

The live endpoint uses the multiplicative quotient

    R(q) = LHS(q) / main_sum(q)

and then applies the q-power projection to the unit:

    R(q)^2029 - 1.

This gate records why two tempting alternatives are not acceptable:

* `(LHS(q) - main_sum(q))^2029`
* `LHS(q)^2029 - main_sum(q)^2029`

Both invalid routes remain singleton-supported in this p25 instance, so a
support-only check would miss the bug.  They fail by landing on the wrong
coefficient and wrong multiplicative order in the auxiliary value field.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_mccarthy_normalization_density_gate import (
    mccarthy_vectors,
    support,
)
from p25_laneB_square_axis_mccarthy_power_descent_gate import ADDITIVE_ROOT_ORDER
from p25_laneB_square_axis_mccarthy_unit_quotient_gate import multiplicative_order
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    TARGET_Q_EXP,
    VALUE_FIELD,
)


@dataclass(frozen=True)
class McCarthyMultiplicativeRouteFalsifierProfile:
    target_q_exp: int
    q_power: int
    valid_multiplicative_support: tuple[int, ...]
    valid_multiplicative_target_value: int
    valid_multiplicative_target_order: int
    valid_multiplicative_minus_one_value: int
    valid_multiplicative_minus_one_order: int
    additive_difference_power_support: tuple[int, ...]
    additive_difference_power_target_value: int
    additive_difference_power_target_order: int
    lhs_power_minus_main_power_support: tuple[int, ...]
    lhs_power_minus_main_power_target_value: int
    lhs_power_minus_main_power_target_order: int
    invalid_difference_matches_valid: bool
    invalid_power_difference_matches_valid: bool
    invalid_routes_singleton_supported: bool
    support_only_check_is_insufficient: bool
    multiplicative_route_required: bool


def mccarthy_multiplicative_route_falsifier_profile() -> McCarthyMultiplicativeRouteFalsifierProfile:
    ctx, _lower_1f0, lhs_vector, main_vector, difference_vector, _exceptional_vector = (
        mccarthy_vectors()
    )
    quotient = [
        lhs_value * ctx.inverse(main_value) % VALUE_FIELD
        for lhs_value, main_value in zip(lhs_vector, main_vector)
    ]
    valid_unit = [pow(value, ADDITIVE_ROOT_ORDER, VALUE_FIELD) for value in quotient]
    valid_minus_one = [(value - 1) % VALUE_FIELD for value in valid_unit]
    additive_difference_power = [
        pow(value, ADDITIVE_ROOT_ORDER, VALUE_FIELD) for value in difference_vector
    ]
    lhs_power_minus_main_power = [
        (
            pow(lhs_value, ADDITIVE_ROOT_ORDER, VALUE_FIELD)
            - pow(main_value, ADDITIVE_ROOT_ORDER, VALUE_FIELD)
        )
        % VALUE_FIELD
        for lhs_value, main_value in zip(lhs_vector, main_vector)
    ]

    invalid_difference_matches_valid = additive_difference_power == valid_minus_one
    invalid_power_difference_matches_valid = lhs_power_minus_main_power == valid_minus_one
    invalid_routes_singleton_supported = (
        support(additive_difference_power) == (TARGET_Q_EXP,)
        and support(lhs_power_minus_main_power) == (TARGET_Q_EXP,)
    )

    return McCarthyMultiplicativeRouteFalsifierProfile(
        target_q_exp=TARGET_Q_EXP,
        q_power=ADDITIVE_ROOT_ORDER,
        valid_multiplicative_support=support(valid_minus_one),
        valid_multiplicative_target_value=valid_unit[TARGET_Q_EXP],
        valid_multiplicative_target_order=multiplicative_order(valid_unit[TARGET_Q_EXP]),
        valid_multiplicative_minus_one_value=valid_minus_one[TARGET_Q_EXP],
        valid_multiplicative_minus_one_order=multiplicative_order(
            valid_minus_one[TARGET_Q_EXP]
        ),
        additive_difference_power_support=support(additive_difference_power),
        additive_difference_power_target_value=additive_difference_power[TARGET_Q_EXP],
        additive_difference_power_target_order=multiplicative_order(
            additive_difference_power[TARGET_Q_EXP]
        ),
        lhs_power_minus_main_power_support=support(lhs_power_minus_main_power),
        lhs_power_minus_main_power_target_value=lhs_power_minus_main_power[TARGET_Q_EXP],
        lhs_power_minus_main_power_target_order=multiplicative_order(
            lhs_power_minus_main_power[TARGET_Q_EXP]
        ),
        invalid_difference_matches_valid=invalid_difference_matches_valid,
        invalid_power_difference_matches_valid=invalid_power_difference_matches_valid,
        invalid_routes_singleton_supported=invalid_routes_singleton_supported,
        support_only_check_is_insufficient=(
            invalid_routes_singleton_supported
            and not invalid_difference_matches_valid
            and not invalid_power_difference_matches_valid
        ),
        multiplicative_route_required=(
            support(valid_minus_one) == (TARGET_Q_EXP,)
            and multiplicative_order(valid_unit[TARGET_Q_EXP]) == 39
            and not invalid_difference_matches_valid
            and not invalid_power_difference_matches_valid
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy multiplicative-route falsifier gate")
    profile = mccarthy_multiplicative_route_falsifier_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.q_power == 2029
        and profile.valid_multiplicative_support == (138,)
        and profile.valid_multiplicative_target_value == 12801419
        and profile.valid_multiplicative_target_order == 39
        and profile.valid_multiplicative_minus_one_value == 12801418
        and profile.valid_multiplicative_minus_one_order == 20574060
        and profile.additive_difference_power_support == (138,)
        and profile.additive_difference_power_target_value == 19995471
        and profile.additive_difference_power_target_order == 507
        and profile.lhs_power_minus_main_power_support == (138,)
        and profile.lhs_power_minus_main_power_target_value == 6688559
        and profile.lhs_power_minus_main_power_target_order == 5143515
        and not profile.invalid_difference_matches_valid
        and not profile.invalid_power_difference_matches_valid
        and profile.invalid_routes_singleton_supported
        and profile.support_only_check_is_insufficient
        and profile.multiplicative_route_required
    )

    print(f"mccarthy_multiplicative_route_falsifier_profile={profile}")
    print("multiplicative_route_laws")
    print("  valid_route_is_R_q_to_the_2029_minus_1=1")
    print("  invalid_LHS_minus_main_to_the_2029_is_singleton_but_wrong_value=1")
    print("  invalid_LHS_to_the_2029_minus_main_to_the_2029_is_singleton_but_wrong_value=1")
    print("  support_only_checks_do_not_separate_valid_from_invalid_routes=1")
    print("interpretation")
    print("  theorem_attempts_must_form_the_multiplicative_quotient_before_q_power=1")
    print("  additive_or_field_frobenius_powering_is_killed_even_when_support_matches=1")
    print(f"square_axis_mccarthy_multiplicative_route_falsifier_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_multiplicative_route_falsifier_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

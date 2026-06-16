#!/usr/bin/env python3
"""McCarthy transformed quotient gate for the p25 square axis.

The density gate showed that McCarthy's LHS and transformed main sum are both
dense, while their difference is the q=138 singleton.  A more unit-shaped
question is whether the quotient

    R(q) = LHS(q) / main_sum(q)

is sparse after subtracting 1.  It is: `R(q)-1` is supported only at q=138.
That is the best possible multiplicative reading of the theorem-level
cancellation.

This gate also checks the coefficient debt.  The exceptional quotient value is
not an ordinary multiplicative-character phase.  Its order in the auxiliary
value field F_20574061 is 79131 = 39 * 2029, so it has a nontrivial additive
root component; `R(138)-1` has full order 20574060.  Thus the direct
"character-valued unit quotient" version is killed.  A live continuation must
either cancel the 2029-component by a further identity or explain how this
auxiliary-field quotient descends to the p25 raw-Y coefficient field.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_mccarthy_normalization_density_gate import (
    mccarthy_vectors,
    support,
)
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    TARGET_Q_EXP,
    VALUE_FIELD,
)


CHARACTER_ROOT_ORDER = 2028
ADDITIVE_ROOT_ORDER = 2029
ORDER_507 = 507


@dataclass(frozen=True)
class McCarthyUnitQuotientProfile:
    target_q_exp: int
    outer_s_image: tuple[int, ...]
    lhs_support_count: int
    main_support_count: int
    main_zero_count: int
    quotient_minus_one_support: tuple[int, ...]
    quotient_target_value: int
    quotient_minus_one_target_value: int
    quotient_target_order: int
    quotient_minus_one_order: int
    quotient_in_507_roots: bool
    quotient_in_character_roots: bool
    quotient_has_additive_component: bool
    quotient_power_39_order: int
    quotient_power_2029_order: int
    quotient_minus_one_full_order: bool
    sparse_unit_quotient_exists: bool
    direct_character_phase_killed: bool
    additive_component_requires_explanation: bool


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


def multiplicative_order(value: int) -> int:
    if value % VALUE_FIELD == 0:
        raise AssertionError("zero has no multiplicative order")
    order = VALUE_FIELD - 1
    for prime, exponent in factor_distinct_with_exp(VALUE_FIELD - 1):
        for _ in range(exponent):
            if order % prime == 0 and pow(value, order // prime, VALUE_FIELD) == 1:
                order //= prime
            else:
                break
    return order


def mccarthy_unit_quotient_profile() -> McCarthyUnitQuotientProfile:
    ctx, _lower_1f0, lhs_vector, main_vector, _difference_vector, _exceptional_vector = (
        mccarthy_vectors()
    )
    if any(value == 0 for value in main_vector):
        raise AssertionError("main sum has zeros; quotient would be singular")
    quotient = [
        lhs_value * ctx.inverse(main_value) % VALUE_FIELD
        for lhs_value, main_value in zip(lhs_vector, main_vector)
    ]
    quotient_minus_one = [(value - 1) % VALUE_FIELD for value in quotient]
    target_value = quotient[TARGET_Q_EXP]
    target_delta = quotient_minus_one[TARGET_Q_EXP]
    target_order = multiplicative_order(target_value)
    target_delta_order = multiplicative_order(target_delta)
    power_39_order = multiplicative_order(pow(target_value, 39, VALUE_FIELD))
    power_2029_order = multiplicative_order(pow(target_value, ADDITIVE_ROOT_ORDER, VALUE_FIELD))

    return McCarthyUnitQuotientProfile(
        target_q_exp=TARGET_Q_EXP,
        outer_s_image=tuple(
            sorted((TARGET_Q_EXP + layer * S_STEP) % QUOTIENT_ORDER for layer in range(3))
        ),
        lhs_support_count=len(support(lhs_vector)),
        main_support_count=len(support(main_vector)),
        main_zero_count=sum(1 for value in main_vector if value == 0),
        quotient_minus_one_support=support(quotient_minus_one),
        quotient_target_value=target_value,
        quotient_minus_one_target_value=target_delta,
        quotient_target_order=target_order,
        quotient_minus_one_order=target_delta_order,
        quotient_in_507_roots=pow(target_value, ORDER_507, VALUE_FIELD) == 1,
        quotient_in_character_roots=pow(target_value, CHARACTER_ROOT_ORDER, VALUE_FIELD) == 1,
        quotient_has_additive_component=pow(target_value, 39, VALUE_FIELD) != 1,
        quotient_power_39_order=power_39_order,
        quotient_power_2029_order=power_2029_order,
        quotient_minus_one_full_order=target_delta_order == VALUE_FIELD - 1,
        sparse_unit_quotient_exists=support(quotient_minus_one) == (TARGET_Q_EXP,),
        direct_character_phase_killed=(
            pow(target_value, ORDER_507, VALUE_FIELD) != 1
            and pow(target_value, CHARACTER_ROOT_ORDER, VALUE_FIELD) != 1
            and pow(target_value, 39, VALUE_FIELD) != 1
        ),
        additive_component_requires_explanation=pow(target_value, 39, VALUE_FIELD) != 1,
    )


def main() -> int:
    print("p25 Lane B McCarthy transformed unit-quotient gate")
    profile = mccarthy_unit_quotient_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.outer_s_image == (138, 310, 482)
        and profile.lhs_support_count == 507
        and profile.main_support_count == 507
        and profile.main_zero_count == 0
        and profile.quotient_minus_one_support == (138,)
        and profile.quotient_target_value == 1790844
        and profile.quotient_minus_one_target_value == 1790843
        and profile.quotient_target_order == 79131
        and profile.quotient_minus_one_order == 20574060
        and not profile.quotient_in_507_roots
        and not profile.quotient_in_character_roots
        and profile.quotient_has_additive_component
        and profile.quotient_power_39_order == 2029
        and profile.quotient_power_2029_order == 39
        and profile.quotient_minus_one_full_order
        and profile.sparse_unit_quotient_exists
        and profile.direct_character_phase_killed
        and profile.additive_component_requires_explanation
    )

    print(f"mccarthy_unit_quotient_profile={profile}")
    print("unit_quotient_laws")
    print("  main_sum_is_nonzero_on_all_507_twists=1")
    print("  LHS_over_main_sum_minus_1_is_supported_exactly_at_q_138=1")
    print("  quotient_exceptional_value_not_in_mu_507_or_mu_2028=1")
    print("  quotient_exceptional_value_has_order_39_times_2029=1")
    print("  quotient_minus_one_has_full_auxiliary_field_order=1")
    print("interpretation")
    print("  theorem_cancellation_has_a_sparse_multiplicative_quotient_form=1")
    print("  direct_character_valued_unit_phase_is_killed=1")
    print("  live_route_must_cancel_or_explain_the_additive_root_component=1")
    print(f"square_axis_mccarthy_unit_quotient_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_unit_quotient_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

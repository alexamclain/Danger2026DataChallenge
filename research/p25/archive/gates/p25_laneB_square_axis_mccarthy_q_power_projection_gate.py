#!/usr/bin/env python3
"""q-power projection law for the powered McCarthy quotient.

The powered route uses the map `x -> x^2029` on the auxiliary value field
F_20574061.  This gate records exactly what that operation is and is not.

It is not a field Frobenius automorphism of F_20574061: the auxiliary field is
prime, and the only field automorphism is the identity.  The q-power map is
instead a multiplicative-group endomorphism.  On the root groups used by the
McCarthy computation it:

* fixes the character roots mu_2028, hence fixes mu_39;
* kills the additive root group mu_2029;
* acts by fourth power on the unused mu_5 component.

For the McCarthy quotient target this is exactly the desired projection:

    R(138) = zeta_39^5 * additive_root^1475
    R(138)^2029 = zeta_39^5.

Thus the power step is a precise multiplicative projection onto the character
component, not a free additive/field-Frobenius operation.  A producer must
justify applying it to a unit quotient, after which the finite payload gates
already close.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_mccarthy_normalization_density_gate import mccarthy_vectors
from p25_laneB_square_axis_mccarthy_unit_quotient_gate import multiplicative_order
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    BASE_FIELD_Q,
    CHARACTER_ORDER,
    TARGET_Q_EXP,
    VALUE_FIELD,
    VALUE_PRIMITIVE_ROOT,
)


MU39_ORDER = 39
MU5_ORDER = 5


@dataclass(frozen=True)
class McCarthyQPowerProjectionProfile:
    value_field: int
    value_field_minus_one: int
    q_power: int
    q_power_kernel_size: int
    q_power_image_size: int
    quotient_target_value: int
    quotient_target_order: int
    zeta2028_q_fixed: bool
    zeta39_q_fixed: bool
    additive_root_q_power: int
    mu5_q_power_matches_fourth_power: bool
    quotient_character_exponent: int
    quotient_additive_exponent: int
    quotient_reconstruction_ok: bool
    quotient_q_power_value: int
    quotient_q_power_order: int
    quotient_q_power_zeta39_exponent: int
    q_power_multiplicative_witness: bool
    q_power_nonadditive_witness: tuple[int, int]
    q_power_is_not_field_automorphism: bool
    q_power_is_character_projection_on_target: bool
    remaining_debt_is_unit_quotient_legitimacy: bool


def discrete_log_small(base: int, value: int, order: int) -> int:
    current = 1
    for exponent in range(order):
        if current == value:
            return exponent
        current = current * base % VALUE_FIELD
    raise AssertionError("small discrete log not found")


def mccarthy_q_power_projection_profile() -> McCarthyQPowerProjectionProfile:
    ctx, _lower_1f0, lhs_vector, main_vector, _difference_vector, _exceptional_vector = (
        mccarthy_vectors()
    )
    target = lhs_vector[TARGET_Q_EXP] * ctx.inverse(main_vector[TARGET_Q_EXP]) % VALUE_FIELD
    value_group_order = VALUE_FIELD - 1
    zeta2028 = pow(VALUE_PRIMITIVE_ROOT, value_group_order // CHARACTER_ORDER, VALUE_FIELD)
    zeta39 = pow(VALUE_PRIMITIVE_ROOT, value_group_order // MU39_ORDER, VALUE_FIELD)
    additive_root = pow(VALUE_PRIMITIVE_ROOT, value_group_order // BASE_FIELD_Q, VALUE_FIELD)
    mu5_root = pow(VALUE_PRIMITIVE_ROOT, value_group_order // MU5_ORDER, VALUE_FIELD)

    character_component = pow(target, BASE_FIELD_Q, VALUE_FIELD)
    additive_component_power = pow(target, MU39_ORDER, VALUE_FIELD)
    character_exponent = discrete_log_small(zeta39, character_component, MU39_ORDER)
    additive_power_exponent = discrete_log_small(
        additive_root,
        additive_component_power,
        BASE_FIELD_Q,
    )
    additive_exponent = additive_power_exponent * pow(MU39_ORDER, -1, BASE_FIELD_Q) % BASE_FIELD_Q
    reconstructed = (
        pow(zeta39, character_exponent, VALUE_FIELD)
        * pow(additive_root, additive_exponent, VALUE_FIELD)
        % VALUE_FIELD
    )
    q_power_value = pow(target, BASE_FIELD_Q, VALUE_FIELD)
    nonadd_left = pow(2 + 3, BASE_FIELD_Q, VALUE_FIELD)
    nonadd_right = (
        pow(2, BASE_FIELD_Q, VALUE_FIELD) + pow(3, BASE_FIELD_Q, VALUE_FIELD)
    ) % VALUE_FIELD

    return McCarthyQPowerProjectionProfile(
        value_field=VALUE_FIELD,
        value_field_minus_one=value_group_order,
        q_power=BASE_FIELD_Q,
        q_power_kernel_size=gcd(BASE_FIELD_Q, value_group_order),
        q_power_image_size=value_group_order // gcd(BASE_FIELD_Q, value_group_order),
        quotient_target_value=target,
        quotient_target_order=multiplicative_order(target),
        zeta2028_q_fixed=pow(zeta2028, BASE_FIELD_Q, VALUE_FIELD) == zeta2028,
        zeta39_q_fixed=pow(zeta39, BASE_FIELD_Q, VALUE_FIELD) == zeta39,
        additive_root_q_power=pow(additive_root, BASE_FIELD_Q, VALUE_FIELD),
        mu5_q_power_matches_fourth_power=(
            pow(mu5_root, BASE_FIELD_Q, VALUE_FIELD) == pow(mu5_root, 4, VALUE_FIELD)
        ),
        quotient_character_exponent=character_exponent,
        quotient_additive_exponent=additive_exponent,
        quotient_reconstruction_ok=reconstructed == target,
        quotient_q_power_value=q_power_value,
        quotient_q_power_order=multiplicative_order(q_power_value),
        quotient_q_power_zeta39_exponent=discrete_log_small(zeta39, q_power_value, MU39_ORDER),
        q_power_multiplicative_witness=(
            pow(2 * 3, BASE_FIELD_Q, VALUE_FIELD)
            == pow(2, BASE_FIELD_Q, VALUE_FIELD)
            * pow(3, BASE_FIELD_Q, VALUE_FIELD)
            % VALUE_FIELD
        ),
        q_power_nonadditive_witness=(nonadd_left, nonadd_right),
        q_power_is_not_field_automorphism=nonadd_left != nonadd_right,
        q_power_is_character_projection_on_target=(
            q_power_value == character_component
            and character_exponent == 5
            and additive_exponent == 1475
            and multiplicative_order(q_power_value) == MU39_ORDER
        ),
        remaining_debt_is_unit_quotient_legitimacy=(
            reconstructed == target
            and nonadd_left != nonadd_right
            and q_power_value == character_component
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy q-power projection gate")
    profile = mccarthy_q_power_projection_profile()
    row_ok = (
        profile.value_field == 20574061
        and profile.value_field_minus_one == 20574060
        and profile.q_power == 2029
        and profile.q_power_kernel_size == 2029
        and profile.q_power_image_size == 10140
        and profile.quotient_target_value == 1790844
        and profile.quotient_target_order == 79131
        and profile.zeta2028_q_fixed
        and profile.zeta39_q_fixed
        and profile.additive_root_q_power == 1
        and profile.mu5_q_power_matches_fourth_power
        and profile.quotient_character_exponent == 5
        and profile.quotient_additive_exponent == 1475
        and profile.quotient_reconstruction_ok
        and profile.quotient_q_power_value == 12801419
        and profile.quotient_q_power_order == 39
        and profile.quotient_q_power_zeta39_exponent == 5
        and profile.q_power_multiplicative_witness
        and profile.q_power_nonadditive_witness == (18369750, 91572)
        and profile.q_power_is_not_field_automorphism
        and profile.q_power_is_character_projection_on_target
        and profile.remaining_debt_is_unit_quotient_legitimacy
    )

    print(f"mccarthy_q_power_projection_profile={profile}")
    print("q_power_projection_laws")
    print("  q_power_fixes_mu_2028_and_mu_39=1")
    print("  q_power_kills_mu_2029_additive_root_component=1")
    print("  R_138_decomposes_as_zeta39_5_times_additive_root_1475=1")
    print("  R_138_to_the_2029_is_zeta39_5=1")
    print("  q_power_is_multiplicative_but_not_additive_on_the_value_field=1")
    print("interpretation")
    print("  power_descent_is_a_precise_multiplicative_projection_not_field_frobenius=1")
    print("  remaining_debt_is_justifying_a_unit_quotient_before_applying_projection=1")
    print(f"square_axis_mccarthy_q_power_projection_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_q_power_projection_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Additive-character gauge check for the powered McCarthy quotient.

The McCarthy numeric gates choose an auxiliary additive character by choosing a
2029th root in F_20574061.  This gate checks that the current powered quotient
target is not an artifact of that additive-character gauge.

For a nonzero multiplier u in F_2029, replacing psi(x) by psi(u*x) changes
Gauss sums by the standard multiplicative factor

    g_u(A) = conjugate(A)(u) * g_1(A).

The gate verifies this transform law over all 2028 character exponents for
representative gauges, then evaluates the McCarthy target quotient for several
gauges.  The result is stable:

    R_u(138) = 1790844
    R_u(138)^2029 = zeta_39^5

and off-target q values in the h=2 row still give ratio 1.  Thus the powered
order-39 target is additive-gauge stable; the remaining theorem debt is not an
artifact of a hidden auxiliary additive-character choice.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_mccarthy_q_power_projection_gate import (
    MU39_ORDER,
    discrete_log_small,
)
from p25_laneB_square_axis_mccarthy_unit_quotient_gate import multiplicative_order
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    BASE_FIELD_Q,
    CHARACTER_ORDER,
    ORDER_507_STEP,
    TARGET_Q_EXP,
    VALUE_FIELD,
    VALUE_PRIMITIVE_ROOT,
    X_VALUE,
    McCarthyContext,
)


GAUGES = (1, 2, 13, BASE_FIELD_Q - 1)
PROBE_Q_EXPS = (129, TARGET_Q_EXP, 147)


@dataclass(frozen=True)
class GaugeRow:
    additive_multiplier: int
    gauss_transform_ok: bool
    ratios_by_q: tuple[tuple[int, int], ...]
    projected_by_q: tuple[tuple[int, int], ...]
    target_ratio: int
    target_order: int
    target_projected_value: int
    target_projected_order: int
    target_projected_zeta39_exponent: int
    off_target_ratios_are_one: bool


@dataclass(frozen=True)
class McCarthyAdditiveGaugeProfile:
    gauges: tuple[int, ...]
    probe_q_exps: tuple[int, ...]
    rows: tuple[GaugeRow, ...]
    target_ratios: tuple[int, ...]
    target_projected_values: tuple[int, ...]
    all_gauss_transforms_ok: bool
    target_ratio_gauge_stable: bool
    target_projection_gauge_stable: bool
    off_target_ratios_stay_one: bool
    additive_gauge_not_obstruction: bool


class GaugeMcCarthyContext(McCarthyContext):
    def __init__(self, additive_multiplier: int) -> None:
        self.additive_multiplier = additive_multiplier % BASE_FIELD_Q
        if self.additive_multiplier == 0:
            raise AssertionError("additive multiplier must be nonzero")
        super().__init__()

    def _gauss_sums(self) -> list[int]:
        additive_values = [
            pow(
                self.additive_root,
                (self.additive_multiplier * value) % BASE_FIELD_Q,
                VALUE_FIELD,
            )
            for value in range(BASE_FIELD_Q)
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
            raise AssertionError("trivial Gauss sum should be -1 in every gauge")
        if any(value == 0 for value in sums):
            raise AssertionError("Gauss sum vanished in gauge")
        return sums


def zeta39_exponent(value: int) -> int:
    zeta39 = pow(VALUE_PRIMITIVE_ROOT, (VALUE_FIELD - 1) // MU39_ORDER, VALUE_FIELD)
    return discrete_log_small(zeta39, value, MU39_ORDER)


def gauss_transform_ok(base: McCarthyContext, gauge: GaugeMcCarthyContext) -> bool:
    log_u = base.logs[gauge.additive_multiplier]
    if log_u is None:
        raise AssertionError("missing log for gauge multiplier")
    return all(
        gauge.gauss[exponent]
        == base.gauss[exponent] * pow(base.zeta, (-exponent * log_u) % CHARACTER_ORDER, VALUE_FIELD)
        % VALUE_FIELD
        for exponent in range(CHARACTER_ORDER)
    )


def inner_2f1_values(ctx: McCarthyContext, a0_exp: int) -> tuple[int, ...]:
    return tuple(
        ctx.hypergeo_star(
            (a0_exp, (-psi_exp) % CHARACTER_ORDER),
            ((a0_exp + psi_exp) % CHARACTER_ORDER,),
            (-X_VALUE) % BASE_FIELD_Q,
        )
        for psi_exp in range(CHARACTER_ORDER)
    )


def ratio_for_q(ctx: McCarthyContext, inner_2f1: tuple[int, ...], q_exp: int) -> int:
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    a1_exp = 0
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
    if main_term == 0:
        raise AssertionError("main term vanished in additive gauge")
    return lhs * ctx.inverse(main_term) % VALUE_FIELD


def gauge_row(base: McCarthyContext, additive_multiplier: int) -> GaugeRow:
    ctx = GaugeMcCarthyContext(additive_multiplier)
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    inner = inner_2f1_values(ctx, a0_exp)
    ratios = tuple((q_exp, ratio_for_q(ctx, inner, q_exp)) for q_exp in PROBE_Q_EXPS)
    projected = tuple((q_exp, pow(value, BASE_FIELD_Q, VALUE_FIELD)) for q_exp, value in ratios)
    target_ratio = dict(ratios)[TARGET_Q_EXP]
    target_projected = pow(target_ratio, BASE_FIELD_Q, VALUE_FIELD)
    return GaugeRow(
        additive_multiplier=additive_multiplier,
        gauss_transform_ok=gauss_transform_ok(base, ctx),
        ratios_by_q=ratios,
        projected_by_q=projected,
        target_ratio=target_ratio,
        target_order=multiplicative_order(target_ratio),
        target_projected_value=target_projected,
        target_projected_order=multiplicative_order(target_projected),
        target_projected_zeta39_exponent=zeta39_exponent(target_projected),
        off_target_ratios_are_one=all(
            value == 1 for q_exp, value in ratios if q_exp != TARGET_Q_EXP
        ),
    )


def mccarthy_additive_gauge_profile() -> McCarthyAdditiveGaugeProfile:
    base = McCarthyContext()
    rows = tuple(gauge_row(base, additive_multiplier) for additive_multiplier in GAUGES)
    target_ratios = tuple(row.target_ratio for row in rows)
    target_projected = tuple(row.target_projected_value for row in rows)
    return McCarthyAdditiveGaugeProfile(
        gauges=GAUGES,
        probe_q_exps=PROBE_Q_EXPS,
        rows=rows,
        target_ratios=target_ratios,
        target_projected_values=target_projected,
        all_gauss_transforms_ok=all(row.gauss_transform_ok for row in rows),
        target_ratio_gauge_stable=len(set(target_ratios)) == 1,
        target_projection_gauge_stable=len(set(target_projected)) == 1,
        off_target_ratios_stay_one=all(row.off_target_ratios_are_one for row in rows),
        additive_gauge_not_obstruction=(
            all(row.gauss_transform_ok for row in rows)
            and len(set(target_ratios)) == 1
            and len(set(target_projected)) == 1
            and all(row.off_target_ratios_are_one for row in rows)
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy additive-gauge gate")
    profile = mccarthy_additive_gauge_profile()
    row_ok = (
        profile.gauges == (1, 2, 13, 2028)
        and profile.probe_q_exps == (129, 138, 147)
        and profile.target_ratios == (1790844, 1790844, 1790844, 1790844)
        and profile.target_projected_values == (12801419, 12801419, 12801419, 12801419)
        and profile.all_gauss_transforms_ok
        and profile.target_ratio_gauge_stable
        and profile.target_projection_gauge_stable
        and profile.off_target_ratios_stay_one
        and profile.additive_gauge_not_obstruction
        and all(row.target_order == 79131 for row in profile.rows)
        and all(row.target_projected_order == 39 for row in profile.rows)
        and all(row.target_projected_zeta39_exponent == 5 for row in profile.rows)
    )

    print(f"mccarthy_additive_gauge_profile={profile}")
    print("additive_gauge_laws")
    print("  gauss_sum_transform_g_u_A_equals_Abar_u_times_g_1_A_checked=1")
    print("  target_ratio_R_138_is_stable_for_representative_additive_gauges=1")
    print("  projected_value_R_138_to_the_2029_is_stable_for_representative_additive_gauges=1")
    print("  off_target_h2_row_ratios_remain_one=1")
    print("interpretation")
    print("  powered_mccarthy_target_is_not_an_artifact_of_additive_character_gauge=1")
    print("  remaining_debt_is_arithmetic_unit_quotient_legitimacy=1")
    print(f"square_axis_mccarthy_additive_gauge_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_additive_gauge_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

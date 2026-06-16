#!/usr/bin/env python3
"""Period-context adapter for the exact KSY normalized-y Siegel payload.

The KSY-y Siegel formula gate instantiates the four-layer divisor footprint.
The raw value-route gate says finite-field values are acceptable only when the
theorem also supplies period-156 theta2 fixedness/telescoping context.

This adapter ties those facts together for the exact formula footprint: the
four-layer KSY payload is fixed by [2]^156, no proper divisor of 156 fixes it,
and the compact factor/telescoping certificates already provide the required
period context.  It still does not prove the arithmetic theorem that produces
the values.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_factor_period_certificate_gate import (
    profile_factor_period_certificate,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate import (
    formula_footprint_from_layers,
    ksy_y_siegel_layers,
    profile_ksy_y_siegel_formula,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate import (
    profile_raw_orientation_value_route,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import (
    SUPPORT_PERIOD,
    theta2_support_resolvent_profile,
)
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    proper_divisors,
    profile_telescoping_certificate,
    pushforward_power,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    centered_source_trace,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    D_SHIFT,
    KERNEL_SHIFT,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class KsyYPeriodContextProfile:
    formula_gate_ok: bool
    raw_value_route_ok: bool
    support_resolvent_ok: bool
    telescoping_certificate_ok: bool
    factor_period_certificate_ok: bool
    formula_support_period: int
    formula_fixed_by_period_156: bool
    proper_period_divisors_fail: bool
    support_denominator_gcd_fp_star: int
    ambient_value_branch_count_fp_star: int
    compact_telescoping_budget: int
    factor_period_budget: int
    value_route_obligation: str
    row_ok: bool


def ring_period(ring: dict[Coord, int], limit: int) -> int:
    current = ring
    for period in range(1, limit + 1):
        current = pushforward_power(current, 1)
        if current == ring:
            return period
    raise AssertionError("period exceeds limit")


def exact_ksy_formula_footprint() -> dict[Coord, int]:
    raw_center = add_coord(BASE_POINT, D_SHIFT)
    centers = centered_source_trace(raw_center, KERNEL_SHIFT, D_SHIFT)
    return formula_footprint_from_layers(ksy_y_siegel_layers(centers))


def profile_ksy_y_period_context() -> KsyYPeriodContextProfile:
    formula = profile_ksy_y_siegel_formula()
    value_route = profile_raw_orientation_value_route()
    support = theta2_support_resolvent_profile()
    telescoping = profile_telescoping_certificate()
    factor_period = profile_factor_period_certificate()
    footprint = exact_ksy_formula_footprint()
    formula_period = ring_period(footprint, support.ambient_doubling_order)
    fixed_156 = pushforward_power(footprint, SUPPORT_PERIOD) == footprint
    proper_fail = all(
        pushforward_power(footprint, period) != footprint
        for period in proper_divisors(SUPPORT_PERIOD)
    )
    row_ok = (
        formula.row_ok
        and value_route.row_ok
        and support.row_ok
        and telescoping.row_ok
        and factor_period.row_ok
        and formula_period == SUPPORT_PERIOD
        and fixed_156
        and proper_fail
        and value_route.support_denominator_gcd_fp_star == 1
        and value_route.ambient_value_branch_count_fp_star == 11
        and telescoping.compact_linear_cell_check_budget == 975
        and factor_period.factor_support_budget == 31
    )
    return KsyYPeriodContextProfile(
        formula_gate_ok=formula.row_ok,
        raw_value_route_ok=value_route.row_ok,
        support_resolvent_ok=support.row_ok,
        telescoping_certificate_ok=telescoping.row_ok,
        factor_period_certificate_ok=factor_period.row_ok,
        formula_support_period=formula_period,
        formula_fixed_by_period_156=fixed_156,
        proper_period_divisors_fail=proper_fail,
        support_denominator_gcd_fp_star=value_route.support_denominator_gcd_fp_star,
        ambient_value_branch_count_fp_star=value_route.ambient_value_branch_count_fp_star,
        compact_telescoping_budget=telescoping.compact_linear_cell_check_budget,
        factor_period_budget=factor_period.factor_support_budget,
        value_route_obligation=(
            "a value theorem for the KSY-y formula must include this period-156 "
            "theta2 fixedness/telescoping context; then the F_p^* root is unique"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y period-context gate")
    profile = profile_ksy_y_period_context()
    print(f"ksy_y_period_context_profile={profile}")
    print("period_context_checks")
    print(f"  formula_support_period={profile.formula_support_period}")
    print(f"  formula_fixed_by_period_156={int(profile.formula_fixed_by_period_156)}")
    print(f"  proper_period_divisors_fail={int(profile.proper_period_divisors_fail)}")
    print(f"  support_denominator_gcd_Fp_star={profile.support_denominator_gcd_fp_star}")
    print(f"  ambient_value_branch_count_Fp_star={profile.ambient_value_branch_count_fp_star}")
    print("compact_witnesses")
    print(f"  compact_telescoping_budget={profile.compact_telescoping_budget}")
    print(f"  factor_period_budget={profile.factor_period_budget}")
    print("interpretation")
    print("  exact_KSY_y_formula_has_the_period_156_context_required_by_value_route=1")
    print("  support_period_root_is_unique_in_Fp_star=1")
    print("  ambient_780_value_only_route_still_has_mu11_ambiguity=1")
    print("  this_is_period_context_not_the_arithmetic_value_theorem=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_period_context_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

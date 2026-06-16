#!/usr/bin/env python3
"""Lucas-binomial shadow gate for the p25 Lane B square-axis residual.

The no-borrow gate identified the six-term seed as the lower-triangular
selector t <= h.  This gate records a positive structural clue: that selector
is exactly Lucas support for the binomial coefficients binom(h,t) in base 3.

Equivalently, the seed support is the Boolean support of

    X * (1 + X(1 + Y) + X^2(1 + Y)^2).

The same check also records the first coefficient obstruction.  The honest
binomial coefficient vector has a single coefficient 2 at X^3 Y, so the
all-one seed cannot be obtained from this naive symmetric-power/binomial
shadow by a global, row/column, or S-layer separable rescaling.  A real
producer may still use the Lucas support, but it must supply a genuinely mixed
coefficient twist.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
    residual_q_values,
    seed_terms,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class FlattenProfile:
    field_modulus: int
    support_preserved: bool
    scalar_flatten_possible: bool
    row_column_flatten_possible: bool
    separable_h_t_s_flatten_possible: bool


def binomial_seed_coefficients() -> dict[int, int]:
    return {
        X_STEP * (h_value + 1) + Y_STEP * t_value: comb(h_value, t_value)
        for h_value in range(3)
        for t_value in range(h_value + 1)
    }


def lower_triangle_support() -> list[tuple[int, int]]:
    return [
        (h_value, t_value)
        for h_value in range(3)
        for t_value in range(3)
        if t_value <= h_value
    ]


def lucas_support() -> list[tuple[int, int]]:
    return [
        (h_value, t_value)
        for h_value in range(3)
        for t_value in range(3)
        if comb(h_value, t_value) % 3 != 0
    ]


def boolean_pascal_support_ok() -> bool:
    support = set(lower_triangle_support())
    for h_value in range(1, 3):
        for t_value in range(3):
            left = (h_value, t_value) in support
            inherited = (h_value - 1, t_value) in support or (
                h_value - 1,
                t_value - 1,
            ) in support
            if left != inherited:
                return False
    return True


def arithmetic_pascal_defects() -> list[tuple[int, int, int, int]]:
    defects: list[tuple[int, int, int, int]] = []
    all_one = [[int(t_value <= h_value) for t_value in range(3)] for h_value in range(3)]
    for h_value in range(1, 3):
        for t_value in range(3):
            inherited = all_one[h_value - 1][t_value]
            if t_value:
                inherited += all_one[h_value - 1][t_value - 1]
            if all_one[h_value][t_value] != inherited:
                defects.append((h_value, t_value, all_one[h_value][t_value], inherited))
    return defects


def translated(points: list[int], shifts: list[int]) -> list[int]:
    return sorted((point + shift) % QUOTIENT_ORDER for shift in shifts for point in points)


def flatten_profile(field_modulus: int) -> FlattenProfile:
    coeffs = binomial_seed_coefficients()
    nonzero_terms = [
        term for term, coefficient in coeffs.items() if coefficient % field_modulus != 0
    ]
    support_preserved = sorted(nonzero_terms) == seed_terms()

    values = [coeffs[term] % field_modulus for term in seed_terms()]
    scalar_flatten_possible = support_preserved and len(set(values)) == 1

    # The row/column and h/t/S-layer separable systems both contain the
    # equations a_0 b_0 = a_1 b_0 = a_1 b_1 = a_2 b_0 = 1 and
    # 2*a_2*b_1 = 1.  Together they force 2 = 1; in characteristic 2 the
    # support is already lost.  Keep this explicit rather than hiding it in a
    # general solver, because it is the mathematical obstruction we want.
    two_equals_one = (2 - 1) % field_modulus == 0
    row_column_flatten_possible = support_preserved and two_equals_one
    separable_h_t_s_flatten_possible = support_preserved and two_equals_one

    return FlattenProfile(
        field_modulus=field_modulus,
        support_preserved=support_preserved,
        scalar_flatten_possible=scalar_flatten_possible,
        row_column_flatten_possible=row_column_flatten_possible,
        separable_h_t_s_flatten_possible=separable_h_t_s_flatten_possible,
    )


def main() -> int:
    print("p25 Lane B square-axis Lucas-binomial shadow gate")
    print(f"quotient_order={QUOTIENT_ORDER}")
    s_terms = [0, S_STEP, 2 * S_STEP]
    coeffs = binomial_seed_coefficients()
    seed = seed_terms()
    binomial_support_terms = sorted(coeffs)
    binomial_coeff_vector = [coeffs[term] for term in seed]
    binomial_residual_support = translated(binomial_support_terms, s_terms)
    target_residual = residual_q_values()
    anomaly_seed_terms = [
        term for term, coefficient in coeffs.items() if coefficient != 1
    ]
    anomaly_residual_terms = translated(anomaly_seed_terms, s_terms)
    pascal_defects = arithmetic_pascal_defects()
    profiles = [flatten_profile(modulus) for modulus in (2, 3, 5, 2029)]
    support_preserving_odd_profiles = [
        profile for profile in profiles if profile.field_modulus != 2
    ]

    row_ok = (
        lower_triangle_support() == lucas_support()
        and boolean_pascal_support_ok()
        and pascal_defects == [(2, 1, 1, 2)]
        and binomial_support_terms == seed
        and binomial_coeff_vector == [1, 1, 1, 1, 2, 1]
        and binomial_residual_support == target_residual
        and anomaly_seed_terms == [X_STEP * 3 + Y_STEP]
        and anomaly_residual_terms == [138, 310, 482]
        and profiles[0].support_preserved is False
        and all(profile.support_preserved for profile in support_preserving_odd_profiles)
        and not any(profile.scalar_flatten_possible for profile in profiles)
        and not any(profile.row_column_flatten_possible for profile in profiles)
        and not any(profile.separable_h_t_s_flatten_possible for profile in profiles)
    )

    print(
        "lucas_binomial_shadow: "
        f"seed_terms={seed} "
        f"binomial_support_terms={binomial_support_terms} "
        f"binomial_coeff_vector={binomial_coeff_vector} "
        f"lucas_support={lucas_support()} "
        f"boolean_pascal_support_ok={int(boolean_pascal_support_ok())} "
        f"arithmetic_pascal_defects={pascal_defects} "
        f"residual_support_count={len(binomial_residual_support)}/18 "
        f"anomaly_seed_terms={anomaly_seed_terms} "
        f"anomaly_residual_terms={anomaly_residual_terms} "
        f"ok={int(row_ok)}"
    )
    print("flatten_profiles")
    for profile in profiles:
        print(
            f"  mod {profile.field_modulus}: "
            f"support_preserved={int(profile.support_preserved)} "
            f"scalar_flatten_possible={int(profile.scalar_flatten_possible)} "
            f"row_column_flatten_possible={int(profile.row_column_flatten_possible)} "
            f"separable_h_t_s_flatten_possible={int(profile.separable_h_t_s_flatten_possible)}"
        )
    print("binomial_shadow_law")
    print("  seed_support = supp X*(1 + X*(1+Y) + X^2*(1+Y)^2)")
    print("  selected(h,t) = 1 iff binom(h,t) is nonzero mod 3")
    print("  coefficient anomaly = X^3*Y, repeated on the S orbit")
    print(f"square_axis_lucas_binomial_shadow_rows={int(row_ok)}/1")
    print("interpretation")
    print("  no_borrow_triangle_is_lucas_binomial_support=1")
    print("  naive_symmetric_power_coefficients_are_not_the_all_one_seed=1")
    print("  row_column_or_S_layer_separable_rescaling_cannot_flatten_the_coefficients=1")
    print("  producer_must_supply_a_genuinely_mixed_coefficient_twist=1")
    print("conclusion=reported_p25_laneB_square_axis_lucas_binomial_shadow_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

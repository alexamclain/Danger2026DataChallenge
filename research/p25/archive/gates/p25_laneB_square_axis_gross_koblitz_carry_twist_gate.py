#!/usr/bin/env python3
"""Gross-Koblitz carry-twist falsifier for the p25 square-axis anomaly.

The Lucas/q-binomial gates leave one tempting Jacobi-side story: maybe a
Gross-Koblitz / Stickelberger carry valuation supplies the missing mixed
coefficient twist.  This gate tests the strict finite version of that story on
the actual 3 by 3 no-borrow digits.

Write the selected seed cells as a fixed-product digit pair

    a = t,  b = h - t mod 3,  a + b = h mod 3.

The no-borrow support is exactly the cells where the base carry of a+b is zero.
A character twist preserving the product replaces

    (a,b) by (a + tau, b - tau) mod 3.

The Gross-Koblitz valuation can change only through the carry of this twisted
digit pair.  The target q-binomial anomaly would require zero carry on every
selected cell except (h,t)=(2,1), positive carry on that one cell, and positive
carry outside the no-borrow support.

The strict carry model cannot do this.  For every cell with h=2, including the
anomaly, all three product-preserving twists have carry zero.  Thus a pure
carry-valuation twist cannot be the missing all-one correction.  A viable
Jacobi producer would need extra unit-phase data, a multi-digit interaction, or
a different identity such as a Barnes-delta resonance.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


DIGIT_BASE = 3
ANOMALY_CELL = (2, 1)


@dataclass(frozen=True)
class CellCarryProfile:
    h_value: int
    t_value: int
    selected: bool
    anomaly: bool
    base_digits: tuple[int, int]
    possible_carries: tuple[int, ...]


@dataclass(frozen=True)
class AffineScanProfile:
    variables: tuple[str, ...]
    candidate_count: int
    exact_target_count: int
    anomaly_positive_count: int
    outside_unit_free_count: int
    support_safe_count: int


def seed_cells() -> list[tuple[int, int]]:
    return [(h_value, t_value) for h_value in range(3) for t_value in range(3)]


def selected(h_value: int, t_value: int) -> bool:
    return t_value <= h_value


def seed_term(h_value: int, t_value: int) -> int:
    return X_STEP * (h_value + 1) + Y_STEP * t_value


def translated_anomaly_terms() -> list[int]:
    return sorted(
        (seed_term(*ANOMALY_CELL) + s_value * S_STEP) % QUOTIENT_ORDER
        for s_value in range(3)
    )


def base_digits(h_value: int, t_value: int) -> tuple[int, int]:
    return t_value, (h_value - t_value) % DIGIT_BASE


def digit_carry(a_value: int, b_value: int) -> int:
    return (a_value + b_value) // DIGIT_BASE


def twisted_carry(h_value: int, t_value: int, tau: int) -> int:
    a_value, b_value = base_digits(h_value, t_value)
    return digit_carry(
        (a_value + tau) % DIGIT_BASE,
        (b_value - tau) % DIGIT_BASE,
    )


def cell_profile(h_value: int, t_value: int) -> CellCarryProfile:
    carries = tuple(
        sorted({twisted_carry(h_value, t_value, tau) for tau in range(DIGIT_BASE)})
    )
    return CellCarryProfile(
        h_value=h_value,
        t_value=t_value,
        selected=selected(h_value, t_value),
        anomaly=(h_value, t_value) == ANOMALY_CELL,
        base_digits=base_digits(h_value, t_value),
        possible_carries=carries,
    )


def strict_target_carry(h_value: int, t_value: int) -> int:
    return int((h_value, t_value) == ANOMALY_CELL or not selected(h_value, t_value))


def affine_tau(coefficients: tuple[int, ...], variables: tuple[int, ...]) -> int:
    return sum(coefficient * variable for coefficient, variable in zip(coefficients, variables)) % DIGIT_BASE


def affine_scan(include_s_layer: bool) -> AffineScanProfile:
    variable_names = ("1", "s", "h", "t") if include_s_layer else ("1", "h", "t")
    candidate_count = DIGIT_BASE ** len(variable_names)
    exact_target_count = 0
    anomaly_positive_count = 0
    outside_unit_free_count = 0
    support_safe_count = 0
    s_values = range(3) if include_s_layer else (0,)

    for coefficients in product(range(DIGIT_BASE), repeat=len(variable_names)):
        exact = True
        anomaly_positive = True
        outside_unit_free = True
        support_safe = True
        for s_value in s_values:
            for h_value, t_value in seed_cells():
                variables = (
                    (1, s_value, h_value, t_value)
                    if include_s_layer
                    else (1, h_value, t_value)
                )
                carry = twisted_carry(
                    h_value,
                    t_value,
                    affine_tau(coefficients, variables),
                )
                target = strict_target_carry(h_value, t_value)
                exact = exact and carry == target
                if (h_value, t_value) == ANOMALY_CELL:
                    anomaly_positive = anomaly_positive and carry > 0
                elif selected(h_value, t_value):
                    support_safe = support_safe and carry == 0
                else:
                    outside_unit_free = outside_unit_free and carry > 0
        exact_target_count += int(exact)
        anomaly_positive_count += int(anomaly_positive)
        outside_unit_free_count += int(outside_unit_free)
        support_safe_count += int(support_safe)

    return AffineScanProfile(
        variables=variable_names,
        candidate_count=candidate_count,
        exact_target_count=exact_target_count,
        anomaly_positive_count=anomaly_positive_count,
        outside_unit_free_count=outside_unit_free_count,
        support_safe_count=support_safe_count,
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz carry-twist gate")
    print(f"digit_base={DIGIT_BASE} quotient_order={QUOTIENT_ORDER}")
    profiles = [cell_profile(h_value, t_value) for h_value, t_value in seed_cells()]
    anomaly_profile = next(
        profile
        for profile in profiles
        if (profile.h_value, profile.t_value) == ANOMALY_CELL
    )
    h2_profiles = [profile for profile in profiles if profile.h_value == 2]
    affine_profiles = (affine_scan(False), affine_scan(True))
    anomaly_terms = translated_anomaly_terms()

    row_ok = (
        anomaly_terms == [138, 310, 482]
        and anomaly_profile.possible_carries == (0,)
        and all(profile.possible_carries == (0,) for profile in h2_profiles)
        and all(profile.exact_target_count == 0 for profile in affine_profiles)
        and all(profile.anomaly_positive_count == 0 for profile in affine_profiles)
        and affine_profiles[0].candidate_count == 27
        and affine_profiles[1].candidate_count == 81
    )

    print(
        "gross_koblitz_carry_twist: "
        f"anomaly_cell={ANOMALY_CELL} "
        f"anomaly_terms={anomaly_terms} "
        f"anomaly_possible_carries={anomaly_profile.possible_carries} "
        f"h2_possible_carries={[profile.possible_carries for profile in h2_profiles]} "
        f"ok={int(row_ok)}"
    )
    print("cell_profiles")
    for profile in profiles:
        print(
            f"  h={profile.h_value} t={profile.t_value}: "
            f"selected={int(profile.selected)} "
            f"anomaly={int(profile.anomaly)} "
            f"base_digits={profile.base_digits} "
            f"possible_carries={profile.possible_carries} "
            f"strict_target={strict_target_carry(profile.h_value, profile.t_value)}"
        )
    print("affine_twist_scans")
    for profile in affine_profiles:
        print(
            f"  variables={profile.variables}: "
            f"candidate_count={profile.candidate_count} "
            f"exact_target_count={profile.exact_target_count} "
            f"anomaly_positive_count={profile.anomaly_positive_count} "
            f"outside_unit_free_count={profile.outside_unit_free_count} "
            f"support_safe_count={profile.support_safe_count}"
        )
    print("carry_twist_law")
    print("  a=t, b=h-t mod 3, tau preserves a+b=h mod 3")
    print("  Gross-Koblitz unit support is modeled by zero carry in a+tau plus b-tau")
    print("  h=2 cells cannot acquire a one-digit carry under any product-preserving tau")
    print(f"square_axis_gross_koblitz_carry_twist_rows={int(row_ok)}/1")
    print("interpretation")
    print("  strict_one_digit_carry_twist_cannot_charge_the_X3Y_anomaly=1")
    print("  affine_h_t_or_S_h_t_twists_do_not_change_that_obstruction=1")
    print("  jacobi_route_now_needs_extra_unit_phase_or_multi_digit_identity=1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_carry_twist_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""q-binomial twist falsifier for the p25 Lane B square-axis residual.

The Lucas-binomial gate found a useful support clue: the no-borrow seed is
Pascal/Lucas support.  The next natural producer guess is a q-binomial or
q-Pascal shadow, replacing the middle coefficient 2 by 1 + q.

This gate checks that family in the tiny h,t <= 2 triangle.  The result is
sharp:

* q = 0 gives the all-one seed, but q = 0 is not a multiplicative character
  or root-of-unity parameter.
* Every nonzero q with correct support misses the target on exactly one seed
  cell, X^3 Y.
* After the outer S orbit, the mismatch is always q*S*X^3Y, i.e. the same
  three quotient classes 138, 310, 482.
* No nonzero q over the checked fields, and no 507th root of unity in F_2029,
  can be flattened by global or h/t/S-separable scaling.

So the Lucas clue is real, but a straightforward q-binomial/Gaussian-binomial
producer is not the missing ray-local object.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
    residual_q_values,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


ROOT_FIELD = 2029
ROOT_ORDER = QUOTIENT_ORDER


@dataclass(frozen=True)
class FieldProfile:
    modulus: int
    unit_count: int
    unit_exact_matches: int
    unit_support_matches: int
    unit_scalar_flatten_matches: int
    unit_separable_flatten_matches: int
    all_one_q_pascal_parameters: tuple[int, ...]
    degenerate_q_zero_exact: bool
    q_minus_one_support_lost: bool


@dataclass(frozen=True)
class RootProfile:
    modulus: int
    order: int
    root_count: int
    support_matches: int
    exact_matches: int
    scalar_flatten_matches: int
    separable_flatten_matches: int
    anomaly_value_count: int
    contains_minus_one: bool


def seed_cells() -> list[tuple[int, int]]:
    return [
        (h_value, t_value)
        for h_value in range(3)
        for t_value in range(h_value + 1)
    ]


def seed_term(h_value: int, t_value: int) -> int:
    return X_STEP * (h_value + 1) + Y_STEP * t_value


def q_binomial_coefficients(q_value: int, modulus: int) -> dict[tuple[int, int], int]:
    return {
        (0, 0): 1 % modulus,
        (1, 0): 1 % modulus,
        (1, 1): 1 % modulus,
        (2, 0): 1 % modulus,
        (2, 1): (1 + q_value) % modulus,
        (2, 2): 1 % modulus,
    }


def support_matches(coefficients: dict[tuple[int, int], int], modulus: int) -> bool:
    return all(coefficients[cell] % modulus for cell in seed_cells())


def exact_all_one(coefficients: dict[tuple[int, int], int], modulus: int) -> bool:
    return all(coefficients[cell] % modulus == 1 % modulus for cell in seed_cells())


def scalar_flatten(coefficients: dict[tuple[int, int], int], modulus: int) -> bool:
    values = [coefficients[cell] % modulus for cell in seed_cells()]
    return all(values) and len(set(values)) == 1


def separable_flatten_possible(
    coefficients: dict[tuple[int, int], int], modulus: int
) -> bool:
    if not support_matches(coefficients, modulus):
        return False
    # The equations for cells (0,0), (1,0), (1,1), (2,0), and (2,2)
    # force every h-scale, t-scale, and S-layer scale to the same global
    # value.  The (2,1) cell can then flatten only if its coefficient is 1.
    return coefficients[(2, 1)] % modulus == 1 % modulus


def all_one_satisfies_q_pascal(q_value: int, modulus: int) -> bool:
    # For the all-one lower triangle, the q-Pascal recurrence already forces
    # 1 = 1 + q at the middle cell (h,t)=(2,1).  Check the recurrence directly
    # so the gate records the actual obstruction rather than only the shortcut.
    target = [[int(t_value <= h_value) % modulus for t_value in range(3)] for h_value in range(3)]
    for h_value in range(1, 3):
        for t_value in range(h_value + 1):
            left = target[h_value][t_value]
            inherited = target[h_value - 1][t_value]
            if t_value:
                inherited += pow(q_value, h_value - t_value, modulus) * target[h_value - 1][t_value - 1]
            if left != inherited % modulus:
                return False
    return True


def mismatch_terms(q_value: int, modulus: int) -> dict[int, int]:
    coeffs = q_binomial_coefficients(q_value, modulus)
    mismatches: dict[int, int] = {}
    for h_value, t_value in seed_cells():
        delta = (coeffs[(h_value, t_value)] - 1) % modulus
        if delta:
            mismatches[seed_term(h_value, t_value)] = delta
    return mismatches


def translated_anomaly_terms() -> list[int]:
    anomaly = X_STEP * 3 + Y_STEP
    return sorted((anomaly + shift) % QUOTIENT_ORDER for shift in (0, S_STEP, 2 * S_STEP))


def field_profile(modulus: int) -> FieldProfile:
    unit_qs = list(range(1, modulus))
    exact_count = 0
    support_count = 0
    scalar_count = 0
    separable_count = 0
    for q_value in unit_qs:
        coeffs = q_binomial_coefficients(q_value, modulus)
        exact_count += int(exact_all_one(coeffs, modulus))
        support_count += int(support_matches(coeffs, modulus))
        scalar_count += int(scalar_flatten(coeffs, modulus))
        separable_count += int(separable_flatten_possible(coeffs, modulus))
    pascal_qs = tuple(
        q_value
        for q_value in range(modulus)
        if all_one_satisfies_q_pascal(q_value, modulus)
    )
    return FieldProfile(
        modulus=modulus,
        unit_count=len(unit_qs),
        unit_exact_matches=exact_count,
        unit_support_matches=support_count,
        unit_scalar_flatten_matches=scalar_count,
        unit_separable_flatten_matches=separable_count,
        all_one_q_pascal_parameters=pascal_qs,
        degenerate_q_zero_exact=exact_all_one(q_binomial_coefficients(0, modulus), modulus),
        q_minus_one_support_lost=not support_matches(q_binomial_coefficients((-1) % modulus, modulus), modulus),
    )


def root_profile() -> RootProfile:
    root = primitive_root(ROOT_FIELD)
    zeta = pow(root, (ROOT_FIELD - 1) // ROOT_ORDER, ROOT_FIELD)
    roots = tuple(pow(zeta, exponent, ROOT_FIELD) for exponent in range(ROOT_ORDER))
    if len(set(roots)) != ROOT_ORDER:
        raise AssertionError("failed to enumerate the 507th roots of unity")
    exact_count = 0
    support_count = 0
    scalar_count = 0
    separable_count = 0
    anomaly_values: set[int] = set()
    for q_value in roots:
        coeffs = q_binomial_coefficients(q_value, ROOT_FIELD)
        exact_count += int(exact_all_one(coeffs, ROOT_FIELD))
        support_count += int(support_matches(coeffs, ROOT_FIELD))
        scalar_count += int(scalar_flatten(coeffs, ROOT_FIELD))
        separable_count += int(separable_flatten_possible(coeffs, ROOT_FIELD))
        anomaly_values.add(coeffs[(2, 1)])
    return RootProfile(
        modulus=ROOT_FIELD,
        order=ROOT_ORDER,
        root_count=len(roots),
        support_matches=support_count,
        exact_matches=exact_count,
        scalar_flatten_matches=scalar_count,
        separable_flatten_matches=separable_count,
        anomaly_value_count=len(anomaly_values),
        contains_minus_one=(-1 % ROOT_FIELD) in set(roots),
    )


def main() -> int:
    print("p25 Lane B square-axis q-binomial twist falsifier gate")
    print(f"quotient_order={QUOTIENT_ORDER} root_field={ROOT_FIELD}")
    anomaly_terms = translated_anomaly_terms()
    target_residual = residual_q_values()
    field_profiles = [field_profile(modulus) for modulus in (3, 5, ROOT_FIELD)]
    roots = root_profile()
    representative_mismatches = {
        q_value: mismatch_terms(q_value, ROOT_FIELD)
        for q_value in (0, 1, 2, 17)
    }
    row_ok = (
        anomaly_terms == [138, 310, 482]
        and len(target_residual) == 18
        and all(profile.unit_exact_matches == 0 for profile in field_profiles)
        and [profile.unit_support_matches for profile in field_profiles] == [1, 3, 2027]
        and all(profile.unit_scalar_flatten_matches == 0 for profile in field_profiles)
        and all(profile.unit_separable_flatten_matches == 0 for profile in field_profiles)
        and all(profile.all_one_q_pascal_parameters == (0,) for profile in field_profiles)
        and all(profile.degenerate_q_zero_exact for profile in field_profiles)
        and all(profile.q_minus_one_support_lost for profile in field_profiles)
        and roots.root_count == ROOT_ORDER
        and roots.support_matches == ROOT_ORDER
        and roots.exact_matches == 0
        and roots.scalar_flatten_matches == 0
        and roots.separable_flatten_matches == 0
        and roots.anomaly_value_count == ROOT_ORDER
        and not roots.contains_minus_one
        and representative_mismatches[0] == {}
        and representative_mismatches[1] == {138: 1}
        and representative_mismatches[2] == {138: 2}
        and representative_mismatches[17] == {138: 17}
    )
    print(
        "q_binomial_twist: "
        f"target_residual_count={len(target_residual)}/18 "
        f"anomaly_terms={anomaly_terms} "
        f"representative_seed_mismatches={representative_mismatches} "
        f"ok={int(row_ok)}"
    )
    print("field_profiles")
    for profile in field_profiles:
        print(
            f"  mod {profile.modulus}: "
            f"unit_count={profile.unit_count} "
            f"unit_exact_matches={profile.unit_exact_matches} "
            f"unit_support_matches={profile.unit_support_matches} "
            f"unit_scalar_flatten_matches={profile.unit_scalar_flatten_matches} "
            f"unit_separable_flatten_matches={profile.unit_separable_flatten_matches} "
            f"all_one_q_pascal_parameters={list(profile.all_one_q_pascal_parameters)} "
            f"q_zero_exact={int(profile.degenerate_q_zero_exact)} "
            f"q_minus_one_support_lost={int(profile.q_minus_one_support_lost)}"
        )
    print(
        "root_profile "
        f"mod={roots.modulus} order={roots.order} "
        f"root_count={roots.root_count} "
        f"support_matches={roots.support_matches} "
        f"exact_matches={roots.exact_matches} "
        f"scalar_flatten_matches={roots.scalar_flatten_matches} "
        f"separable_flatten_matches={roots.separable_flatten_matches} "
        f"anomaly_value_count={roots.anomaly_value_count} "
        f"contains_minus_one={int(roots.contains_minus_one)}"
    )
    print("q_binomial_law")
    print("  [2 choose 1]_q = 1 + q")
    print("  all-one seed forces q = 0 in the q-Pascal middle cell")
    print("  nonzero q-binomial residual = target + q*S*X^3Y")
    print(f"square_axis_q_binomial_twist_falsifier_rows={int(row_ok)}/1")
    print("interpretation")
    print("  lucas_support_survives_for_odd_order_q_roots=1")
    print("  no_unit_q_binomial_or_q_pascal_shadow_gives_the_all_one_payload=1")
    print("  q_binomial_mismatch_is_exactly_the_coefficient_twist_orbit=1")
    print("  producer_needs_more_than_a_straight_gaussian_binomial_parameter=1")
    print("conclusion=reported_p25_laneB_square_axis_q_binomial_twist_falsifier_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Coefficient-anomaly orbit balance gate for p25 Lane B.

The q-binomial falsifier reduced the coefficient problem to one orbit:

    q * S * X^3 Y,  with S = 1 + D + D^2.

This gate records two producer-facing facts about that orbit.

First, it is not detectable by coarse Fourier support tests: the three-point
orbit has the same two S-factor Fourier zeros as the full residual, rectangle,
and borrow corner.

Second, it is not a degree-zero S-orbit correction.  Subtracting it has total
degree -3q, nonzero for every unit q in the working odd fields.  If we try to
balance it using one more S-orbit, then an orbit inside the target distorts a
correct coefficient, while an orbit outside the target creates forbidden
support.  Thus a modular-unit/ray producer cannot repair the q-binomial
coefficient by a lone visible anomaly subtraction or by a two-S-orbit patch.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    MODULUS,
    S_STEP,
    X_STEP,
    Y_STEP,
    borrow_seed_terms,
    dft_zeros,
    rectangle_seed_terms,
    residual_q_values,
    seed_terms,
    translate,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class BalanceProfile:
    balancing_seed_term: int
    inside_target: bool
    creates_forbidden_support: bool
    distorts_target_coefficient: bool
    exact_target_after_balance: bool


def anomaly_seed_term() -> int:
    return X_STEP * 3 + Y_STEP


def anomaly_orbit() -> list[int]:
    return translate([anomaly_seed_term()], [0, S_STEP, 2 * S_STEP])


def weighted_residual_from_seed(seed_coeffs: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for term, coeff in seed_coeffs.items():
        for point in translate([term], [0, S_STEP, 2 * S_STEP]):
            out[point] = out.get(point, 0) + coeff
    return dict(sorted(out.items()))


def target_vector() -> dict[int, int]:
    return {point: 1 for point in residual_q_values()}


def q_binomial_vector(q_value: int) -> dict[int, int]:
    coeffs = {term: 1 for term in seed_terms()}
    coeffs[anomaly_seed_term()] = 1 + q_value
    return weighted_residual_from_seed(coeffs)


def exact_visible_correction(q_value: int) -> dict[int, int]:
    target = target_vector()
    q_vector = q_binomial_vector(q_value)
    keys = sorted(set(target) | set(q_vector))
    return {
        key: target.get(key, 0) - q_vector.get(key, 0)
        for key in keys
        if target.get(key, 0) != q_vector.get(key, 0)
    }


def vector_degree(vector: dict[int, int]) -> int:
    return sum(vector.values())


def apply_correction(
    vector: dict[int, int], correction: dict[int, int]
) -> dict[int, int]:
    out = dict(vector)
    for key, value in correction.items():
        out[key] = out.get(key, 0) + value
        if out[key] == 0:
            del out[key]
    return dict(sorted(out.items()))


def balance_profiles() -> list[BalanceProfile]:
    target = target_vector()
    q_vector = q_binomial_vector(1)
    profiles: list[BalanceProfile] = []
    anomaly = anomaly_seed_term()
    for balancing in rectangle_seed_terms():
        if balancing == anomaly:
            continue
        correction = weighted_residual_from_seed({anomaly: -1, balancing: 1})
        repaired = apply_correction(q_vector, correction)
        balancing_orbit = translate([balancing], [0, S_STEP, 2 * S_STEP])
        inside_target = balancing in seed_terms()
        creates_forbidden = any(point not in target for point in balancing_orbit)
        distorts_target = any(
            point in target and repaired.get(point, 0) != target[point]
            for point in balancing_orbit
        )
        profiles.append(
            BalanceProfile(
                balancing_seed_term=balancing,
                inside_target=inside_target,
                creates_forbidden_support=creates_forbidden,
                distorts_target_coefficient=distorts_target,
                exact_target_after_balance=repaired == target,
            )
        )
    return profiles


def main() -> int:
    print("p25 Lane B square-axis anomaly-orbit balance gate")
    print(f"quotient_order={QUOTIENT_ORDER} modulus={MODULUS}")
    anomaly = anomaly_seed_term()
    orbit = anomaly_orbit()
    target = target_vector()
    q_vector = q_binomial_vector(1)
    correction = exact_visible_correction(1)
    correction_support = sorted(correction)
    correction_values = sorted(set(correction.values()))
    profiles = balance_profiles()
    anomaly_zero_profile = dft_zeros(orbit, "anomaly_orbit")
    residual_zero_profile = dft_zeros(residual_q_values(), "residual")
    borrow_zero_profile = dft_zeros(translate(borrow_seed_terms(), [0, S_STEP, 2 * S_STEP]), "borrow")
    rectangle_zero_profile = dft_zeros(translate(rectangle_seed_terms(), [0, S_STEP, 2 * S_STEP]), "rectangle")

    inside_target_failures = sum(
        int(profile.inside_target and profile.distorts_target_coefficient)
        for profile in profiles
    )
    outside_target_failures = sum(
        int((not profile.inside_target) and profile.creates_forbidden_support)
        for profile in profiles
    )
    exact_balanced_repairs = sum(
        int(profile.exact_target_after_balance) for profile in profiles
    )
    row_ok = (
        anomaly == 138
        and orbit == [138, 310, 482]
        and q_vector[138] == q_vector[310] == q_vector[482] == 2
        and all(target[point] == 1 for point in orbit)
        and correction == {138: -1, 310: -1, 482: -1}
        and correction_support == orbit
        and correction_values == [-1]
        and vector_degree(correction) == -3
        and vector_degree(correction) % MODULUS != 0
        and anomaly_zero_profile.zeros == residual_zero_profile.zeros == borrow_zero_profile.zeros == rectangle_zero_profile.zeros == (169, 338)
        and anomaly_zero_profile.zero_count == 2
        and len(profiles) == 8
        and inside_target_failures == 5
        and outside_target_failures == 3
        and exact_balanced_repairs == 0
    )
    print(
        "anomaly_orbit_balance: "
        f"anomaly_seed_term={anomaly} "
        f"anomaly_orbit={orbit} "
        f"q_binomial_coefficients_on_orbit={[q_vector[point] for point in orbit]} "
        f"target_coefficients_on_orbit={[target[point] for point in orbit]} "
        f"exact_visible_correction={correction} "
        f"correction_degree={vector_degree(correction)} "
        f"correction_degree_mod_{MODULUS}={vector_degree(correction) % MODULUS} "
        f"fourier_zeros={list(anomaly_zero_profile.zeros)} "
        f"balance_profiles={len(profiles)} "
        f"inside_target_failures={inside_target_failures}/5 "
        f"outside_target_failures={outside_target_failures}/3 "
        f"exact_balanced_repairs={exact_balanced_repairs} "
        f"ok={int(row_ok)}"
    )
    print("balance_profiles")
    for profile in profiles:
        print(
            f"  balancing_seed_term={profile.balancing_seed_term} "
            f"inside_target={int(profile.inside_target)} "
            f"creates_forbidden_support={int(profile.creates_forbidden_support)} "
            f"distorts_target_coefficient={int(profile.distorts_target_coefficient)} "
            f"exact_target_after_balance={int(profile.exact_target_after_balance)}"
        )
    print("fourier_zero_profiles")
    for profile in (
        anomaly_zero_profile,
        residual_zero_profile,
        rectangle_zero_profile,
        borrow_zero_profile,
    ):
        print(
            f"  {profile.name}: point_count={profile.point_count} "
            f"zero_count={profile.zero_count} zeros={list(profile.zeros)}"
        )
    print("interpretation")
    print("  coefficient_anomaly_orbit_is_fourier_dense_like_the_residual=1")
    print("  exact_visible_anomaly_correction_is_not_degree_zero=1")
    print("  degree_zero_two_S_orbit_balancing_breaks_the_quotient_target=1")
    print("  modular_unit_candidate_must_supply_scalar_nonlocal_or_hidden_balance=1")
    print("conclusion=reported_p25_laneB_square_axis_anomaly_orbit_balance_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

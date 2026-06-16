#!/usr/bin/env python3
"""Theorem-side normalization scan for the McCarthy auxiliary-prime failure.

The auxiliary-prime probe showed that the post-hoc projection

    R(138) -> R(138)^2029

lands in `mu_39` only in the minimal auxiliary field.  This scan asks whether
the failure is repaired by a simple theorem-side normalization using the actual
target-twist McCarthy factors: denominator, prefactor, main sum, LHS/main
terms, and the visible Gauss sums `g(a0)`, `g(-a0)`, `g(0)`.

It is intentionally narrow.  It does not search arbitrary filters.  It kills
the easy explanation that a missing denominator/prefactor/Gauss factor makes
the q-power projection auxiliary-prime invariant.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe import (
    AuxiliaryMcCarthyContext,
    REQUIRED_ROOT_STEP,
    multiplicative_order_mod,
)
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import (
    BASE_FIELD_Q,
    CHARACTER_ORDER,
    ORDER_507_STEP,
    TARGET_Q_EXP,
    X_VALUE,
)


PROBE_MULTIPLIERS = (1, 4, 7)
SINGLE_FACTOR_NAMES = (
    "denominator",
    "prefactor",
    "main_sum",
    "main_term",
    "lhs",
    "g_a0",
    "g_minus_a0",
    "g_a0_g_minus_a0",
)
SINGLE_FACTOR_EXPONENTS = (-2, -1, 1, 2)
GAUSS_MONOMIAL_NAMES = ("g_a0", "g_minus_a0", "g0")
GAUSS_MONOMIAL_EXPONENTS = (-2, -1, 0, 1, 2)
THEOREM_MONOMIAL_NAMES = ("denominator", "prefactor", "g_a0", "g_minus_a0")
THEOREM_MONOMIAL_EXPONENTS = (-1, 0, 1)


@dataclass(frozen=True)
class FactorOrderProfile:
    name: str
    order: int
    q_power_order: int


@dataclass(frozen=True)
class McCarthyTargetFactorProfile:
    multiplier: int
    value_field: int
    primitive_root: int
    transformed_difference_value: int
    quotient_q_power_order: int
    quotient_q_power_in_mu39: bool
    factor_orders: tuple[FactorOrderProfile, ...]


@dataclass(frozen=True)
class McCarthyTheoremFactorNormalizationProfile:
    target_q_exp: int
    probe_multipliers: tuple[int, ...]
    raw_quotient_mu39_hits: tuple[bool, ...]
    target_factor_profiles: tuple[McCarthyTargetFactorProfile, ...]
    single_factors_scanned: int
    single_factor_all_mu39_count: int
    single_factor_any_mu39_count: int
    gauss_monomials_scanned: int
    gauss_monomial_all_mu39_count: int
    theorem_monomials_scanned: int
    theorem_monomial_all_mu39_count: int
    easy_theorem_factor_normalization_found: bool
    posthoc_projection_still_suspect: bool


def target_values(multiplier: int) -> tuple[int, AuxiliaryMcCarthyContext, dict[str, int]]:
    value_field = REQUIRED_ROOT_STEP * multiplier + 1
    ctx = AuxiliaryMcCarthyContext(value_field)
    a0_exp = ORDER_507_STEP * TARGET_Q_EXP
    a1_exp = 0
    a2_exp = a0_exp

    lower_1f0 = ctx.hypergeo_star((a0_exp,), (), X_VALUE)
    if lower_1f0 != 1:
        raise AssertionError("unexpected lower 1F0 value")
    inner_2f1 = tuple(
        ctx.hypergeo_star(
            (a0_exp, (-psi_exp) % CHARACTER_ORDER),
            ((a0_exp + psi_exp) % CHARACTER_ORDER,),
            (-X_VALUE) % BASE_FIELD_Q,
        )
        for psi_exp in range(CHARACTER_ORDER)
    )
    lhs = ctx.hypergeo_star(
        (a0_exp, a1_exp, a2_exp),
        (
            (a0_exp - a1_exp) % CHARACTER_ORDER,
            (a0_exp - a2_exp) % CHARACTER_ORDER,
        ),
        X_VALUE,
    )
    denominator = (
        ctx.gauss[a1_exp]
        * ctx.gauss[a2_exp]
        % value_field
        * ctx.gauss[(-a0_exp + a1_exp) % CHARACTER_ORDER]
        % value_field
        * ctx.gauss[(-a0_exp + a2_exp) % CHARACTER_ORDER]
        % value_field
    )
    prefactor = (
        ctx.gauss[(-a0_exp + a1_exp + a2_exp) % CHARACTER_ORDER]
        * ctx.inverse(denominator)
        % value_field
    )
    main_sum = 0
    for psi_exp in range(CHARACTER_ORDER):
        term = (
            ctx.gauss[(a1_exp + psi_exp) % CHARACTER_ORDER]
            * ctx.gauss[(a2_exp + psi_exp) % CHARACTER_ORDER]
            % value_field
            * ctx.gauss[-psi_exp % CHARACTER_ORDER]
            % value_field
            * ctx.gauss[(-a0_exp - psi_exp) % CHARACTER_ORDER]
            % value_field
            * inner_2f1[psi_exp]
            % value_field
        )
        main_sum = (main_sum + term) % value_field
    main_term = prefactor * main_sum % value_field * ctx.inv_character_order % value_field
    quotient = lhs * ctx.inverse(main_term) % value_field

    values = {
        "quotient": quotient,
        "denominator": denominator,
        "prefactor": prefactor,
        "main_sum": main_sum,
        "main_term": main_term,
        "lhs": lhs,
        "g_a0": ctx.gauss[a0_exp],
        "g_minus_a0": ctx.gauss[-a0_exp % CHARACTER_ORDER],
        "g0": ctx.gauss[0],
        "g_a0_g_minus_a0": (
            ctx.gauss[a0_exp] * ctx.gauss[-a0_exp % CHARACTER_ORDER] % value_field
        ),
        "transformed_difference": (lhs - main_term) % value_field,
    }
    return value_field, ctx, values


def q_power_in_mu39(value: int, value_field: int) -> bool:
    q_power = pow(value, BASE_FIELD_Q, value_field)
    return pow(q_power, 39, value_field) == 1


def normalized_q_power_orders(
    target_data: tuple[tuple[int, AuxiliaryMcCarthyContext, dict[str, int]], ...],
    factor_exponents: tuple[tuple[str, int], ...],
) -> tuple[bool, ...]:
    hits: list[bool] = []
    for value_field, _ctx, values in target_data:
        candidate = values["quotient"]
        for factor_name, exponent in factor_exponents:
            candidate = (
                candidate
                * pow(values[factor_name], exponent % (value_field - 1), value_field)
                % value_field
            )
        hits.append(q_power_in_mu39(candidate, value_field))
    return tuple(hits)


def mccarthy_theorem_factor_normalization_profile() -> McCarthyTheoremFactorNormalizationProfile:
    target_data = tuple(target_values(multiplier) for multiplier in PROBE_MULTIPLIERS)
    raw_hits = tuple(
        q_power_in_mu39(values["quotient"], value_field)
        for value_field, _ctx, values in target_data
    )

    factor_profiles: list[McCarthyTargetFactorProfile] = []
    for multiplier, (value_field, ctx, values) in zip(PROBE_MULTIPLIERS, target_data):
        factor_orders = tuple(
            FactorOrderProfile(
                name=name,
                order=multiplicative_order_mod(values[name], value_field),
                q_power_order=multiplicative_order_mod(
                    pow(values[name], BASE_FIELD_Q, value_field),
                    value_field,
                ),
            )
            for name in SINGLE_FACTOR_NAMES
        )
        factor_profiles.append(
            McCarthyTargetFactorProfile(
                multiplier=multiplier,
                value_field=value_field,
                primitive_root=ctx.primitive_root,
                transformed_difference_value=values["transformed_difference"],
                quotient_q_power_order=multiplicative_order_mod(
                    pow(values["quotient"], BASE_FIELD_Q, value_field),
                    value_field,
                ),
                quotient_q_power_in_mu39=raw_hits[len(factor_profiles)],
                factor_orders=factor_orders,
            )
        )

    single_all = 0
    single_any = 0
    single_scanned = 0
    for factor_name in SINGLE_FACTOR_NAMES:
        for exponent in SINGLE_FACTOR_EXPONENTS:
            hits = normalized_q_power_orders(target_data, ((factor_name, exponent),))
            single_scanned += 1
            single_all += int(all(hits))
            single_any += int(any(hits))

    gauss_all = 0
    gauss_scanned = 0
    for exponents in product(GAUSS_MONOMIAL_EXPONENTS, repeat=len(GAUSS_MONOMIAL_NAMES)):
        if all(exponent == 0 for exponent in exponents):
            continue
        factor_exponents = tuple(zip(GAUSS_MONOMIAL_NAMES, exponents))
        gauss_scanned += 1
        gauss_all += int(all(normalized_q_power_orders(target_data, factor_exponents)))

    theorem_all = 0
    theorem_scanned = 0
    for exponents in product(
        THEOREM_MONOMIAL_EXPONENTS,
        repeat=len(THEOREM_MONOMIAL_NAMES),
    ):
        if all(exponent == 0 for exponent in exponents):
            continue
        factor_exponents = tuple(zip(THEOREM_MONOMIAL_NAMES, exponents))
        theorem_scanned += 1
        theorem_all += int(all(normalized_q_power_orders(target_data, factor_exponents)))

    easy_found = single_all + gauss_all + theorem_all > 0
    return McCarthyTheoremFactorNormalizationProfile(
        target_q_exp=TARGET_Q_EXP,
        probe_multipliers=PROBE_MULTIPLIERS,
        raw_quotient_mu39_hits=raw_hits,
        target_factor_profiles=tuple(factor_profiles),
        single_factors_scanned=single_scanned,
        single_factor_all_mu39_count=single_all,
        single_factor_any_mu39_count=single_any,
        gauss_monomials_scanned=gauss_scanned,
        gauss_monomial_all_mu39_count=gauss_all,
        theorem_monomials_scanned=theorem_scanned,
        theorem_monomial_all_mu39_count=theorem_all,
        easy_theorem_factor_normalization_found=easy_found,
        posthoc_projection_still_suspect=not easy_found and raw_hits == (True, False, False),
    )


def main() -> int:
    print("p25 Lane B McCarthy theorem-factor normalization scan")
    profile = mccarthy_theorem_factor_normalization_profile()
    row_ok = (
        profile.target_q_exp == 138
        and profile.probe_multipliers == (1, 4, 7)
        and profile.raw_quotient_mu39_hits == (True, False, False)
        and profile.target_factor_profiles[0].value_field == 20574061
        and profile.target_factor_profiles[0].quotient_q_power_order == 39
        and profile.target_factor_profiles[1].value_field == 82296241
        and profile.target_factor_profiles[1].quotient_q_power_order == 5070
        and profile.target_factor_profiles[2].value_field == 144018421
        and profile.target_factor_profiles[2].quotient_q_power_order == 23660
        and all(
            factor_profile.transformed_difference_value == 2028
            for factor_profile in profile.target_factor_profiles
        )
        and profile.single_factors_scanned == 32
        and profile.single_factor_all_mu39_count == 0
        and profile.single_factor_any_mu39_count == 0
        and profile.gauss_monomials_scanned == 124
        and profile.gauss_monomial_all_mu39_count == 0
        and profile.theorem_monomials_scanned == 80
        and profile.theorem_monomial_all_mu39_count == 0
        and not profile.easy_theorem_factor_normalization_found
        and profile.posthoc_projection_still_suspect
    )

    print(f"mccarthy_theorem_factor_normalization_profile={profile}")
    print("theorem_factor_normalization_laws")
    print("  raw_R_to_the_2029_is_mu39_only_at_the_minimal_auxiliary_prime=1")
    print("  no_single_denominator_prefactor_or_visible_gauss_factor_repairs_all_primes=1")
    print("  no_small_visible_gauss_monomial_repairs_all_primes=1")
    print("  no_small_denominator_prefactor_gauss_monomial_repairs_all_primes=1")
    print("interpretation")
    print("  missing_easy_theorem_side_factor_is_not_the_auxiliary_prime_failure=1")
    print("  need_nontrivial_quotient_cancellation_or_direct_endpoint_identity=1")
    print(f"square_axis_mccarthy_theorem_factor_normalization_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Gauss-normalization boundary for the p24 idempotent covariance route.

Formal Frobenius covariance of the additive right resolvent is not enough.
For a centered right profile G_s in L and a nontrivial quotient character chi,

    U_chi = sum_v chi(v) H_v
          = tau(chi) * P_chi,

where

    H_v = sum_s zeta_211^(v*s) G_s,
    P_chi = sum_s chi(s)^(-1) G_s.

The automorphism zeta_211 -> zeta_211^rho gives

    sigma_rho(U_chi) = chi(rho^(-1)) U_chi,
    sigma_rho(tau)  = chi(rho^(-1)) tau,
    sigma_rho(P_chi)= P_chi.

Thus the nontrivial eigenvalue can live entirely in the Gauss factor.  The
desired p24 theorem must be a Gauss-normalized, L-valued idempotent covariance
identity, not merely the formal additive-resolvent covariance.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780
FIELD_Q = 8863  # 8863 - 1 = 42 * 211, so F_q contains mu_211 and mu_7.


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def log_table_mod_211() -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(RIGHT - 1):
        logs[value] = exponent
        value = value * RIGHT_GEN % RIGHT
    if len(logs) != RIGHT - 1:
        raise RuntimeError("2 is not primitive modulo 211")
    return logs


def roots() -> tuple[int, int, int]:
    root = primitive_root(FIELD_Q)
    return (
        root,
        pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q),
        pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q),
    )


def character(
    value: int,
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    exponent = (k * p_log_inv * logs[value]) % ORDER7
    return pow(zeta7, exponent, FIELD_Q)


def right_dft(profile: list[int], zeta211: int) -> list[int]:
    return [
        sum(
            profile[s] * pow(zeta211, (v * s) % RIGHT, FIELD_Q)
            for s in range(1, RIGHT)
        )
        % FIELD_Q
        for v in range(RIGHT)
    ]


def additive_resolvent(
    periods: list[int],
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    return sum(
        character(v, k, logs, zeta7, p_log_inv) * periods[v]
        for v in range(1, RIGHT)
    ) % FIELD_Q


def multiplicative_projection(
    profile: list[int],
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    return sum(
        pow(character(s, k, logs, zeta7, p_log_inv), -1, FIELD_Q) * profile[s]
        for s in range(1, RIGHT)
    ) % FIELD_Q


def gauss_sum(
    k: int,
    logs: dict[int, int],
    zeta211: int,
    zeta7: int,
    p_log_inv: int,
    exponent_multiplier: int = 1,
) -> int:
    return sum(
        character(v, k, logs, zeta7, p_log_inv)
        * pow(zeta211, (exponent_multiplier * v) % RIGHT, FIELD_Q)
        for v in range(1, RIGHT)
    ) % FIELD_Q


def sigma_on_periods(periods: list[int], multiplier: int) -> list[int]:
    # sigma(zeta^v)=zeta^(multiplier*v), so H_v maps to H_{multiplier*v}.
    return [periods[(multiplier * v) % RIGHT] for v in range(RIGHT)]


def quotient_index(value: int, logs: dict[int, int], p_log_inv: int) -> int:
    return (p_log_inv * logs[value]) % ORDER7


def force_ordinary_centering(profile: list[int]) -> list[int]:
    adjusted = profile[:]
    adjusted[1] = (adjusted[1] - sum(adjusted[1:])) % FIELD_Q
    return adjusted


def main() -> None:
    logs = log_table_mod_211()
    root, zeta211, zeta7 = roots()
    p_log = logs[P24 % RIGHT]
    p_log_inv = pow(p_log % ORDER7, -1, ORDER7)
    rho = pow(P24, RHO_EXPONENT, RIGHT)
    rho_inv = pow(rho, -1, RIGHT)
    rho_raw_log_shift = logs[rho] % ORDER7
    rho_quotient_shift = quotient_index(rho, logs, p_log_inv)
    rng = random.Random(20260606)

    additive_eigen_mismatches = 0
    gauss_eigen_mismatches = 0
    normalized_fixed_mismatches = 0
    bridge_mismatches = 0
    normalized_nonzero = 0
    centered_normalized_nonzero = 0
    trials = 16

    for _ in range(trials):
        profile = [0] + [rng.randrange(FIELD_Q) for _s in range(1, RIGHT)]
        periods = right_dft(profile, zeta211)
        sigma_periods = sigma_on_periods(periods, rho)
        centered = force_ordinary_centering(profile)
        centered_periods = right_dft(centered, zeta211)
        for k in range(1, ORDER7):
            eigenvalue = character(rho_inv, k, logs, zeta7, p_log_inv)
            additive = additive_resolvent(periods, k, logs, zeta7, p_log_inv)
            additive_sigma = additive_resolvent(
                sigma_periods,
                k,
                logs,
                zeta7,
                p_log_inv,
            )
            tau = gauss_sum(k, logs, zeta211, zeta7, p_log_inv)
            tau_sigma = gauss_sum(k, logs, zeta211, zeta7, p_log_inv, rho)
            projection = multiplicative_projection(profile, k, logs, zeta7, p_log_inv)
            centered_projection = multiplicative_projection(
                centered,
                k,
                logs,
                zeta7,
                p_log_inv,
            )

            additive_eigen_mismatches += int(
                additive_sigma != eigenvalue * additive % FIELD_Q
            )
            gauss_eigen_mismatches += int(
                tau_sigma != eigenvalue * tau % FIELD_Q
            )
            bridge_mismatches += int(additive != tau * projection % FIELD_Q)
            normalized_fixed_mismatches += int(
                additive_sigma * pow(tau_sigma, -1, FIELD_Q) % FIELD_Q
                != projection
            )
            normalized_nonzero += int(projection != 0)
            centered_normalized_nonzero += int(centered_projection != 0)

    print("Trace-GCD fixed-frequency p24 Gauss-normalization boundary")
    print(f"p24={P24}")
    print(f"right={RIGHT}")
    print(f"field_q={FIELD_Q}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho}")
    print(f"rho_log_base_2={logs[rho]}")
    print(f"rho_h_raw_log_shift={rho_raw_log_shift}")
    print(f"rho_h_orbit_position_shift={rho_quotient_shift}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p_log_inv_mod_7={p_log_inv}")
    print(f"random_trials={trials}")
    print(f"additive_resolvent_eigen_mismatches={additive_eigen_mismatches}")
    print(f"gauss_sum_eigen_mismatches={gauss_eigen_mismatches}")
    print(f"additive_equals_gauss_times_projection_mismatches={bridge_mismatches}")
    print(f"normalized_projection_fixed_mismatches={normalized_fixed_mismatches}")
    print(f"random_normalized_projection_nonzero={normalized_nonzero}/{trials * 6}")
    print(
        "ordinary_centered_normalized_projection_nonzero="
        f"{centered_normalized_nonzero}/{trials * 6}"
    )
    print("interpretation")
    print("  formal_additive_frobenius_covariance_is_gauss_eigenvalue=1")
    print("  gauss_normalized_L_projection_can_remain_nonzero=1")
    print("  ordinary_centering_does_not_kill_nontrivial_order7_projection=1")
    print("  p24_idempotent_covariance_must_be_gauss_normalized_extra_identity=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_gauss_normalization_boundary")

    if rho_raw_log_shift == 0 or rho_quotient_shift == 0:
        raise SystemExit(1)
    if additive_eigen_mismatches or gauss_eigen_mismatches or bridge_mismatches:
        raise SystemExit(1)
    if normalized_fixed_mismatches:
        raise SystemExit(1)
    if normalized_nonzero != trials * 6:
        raise SystemExit(1)
    if centered_normalized_nonzero != trials * 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

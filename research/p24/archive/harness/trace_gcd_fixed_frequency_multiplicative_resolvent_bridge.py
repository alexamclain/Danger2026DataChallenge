#!/usr/bin/env python3
"""Multiplicative-resolvent bridge for the order-7 fixed-frequency target.

The H-coset theorem can be read in three equivalent finite ways:

* the seven H-coset sums of the centered right profile vanish;
* the six nontrivial order-7 multiplicative-character projections vanish;
* the left additive 157-resolvent is orthogonal to six right multiplicative
  order-7 resolvents.

This script checks that dictionary over a small splitting field for the actual
right prime 211.  It also records a tempting but false Frobenius shortcut:
the orbit-augmentation value is a Frobenius eigenvector, but the nontrivial
eigenvalue sits in the Gauss-sum factor.  After dividing by that factor, the
L-valued projection can be nonzero.
"""

from __future__ import annotations

import random


P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
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
    zeta211 = pow(root, (FIELD_Q - 1) // RIGHT, FIELD_Q)
    zeta7 = pow(root, (FIELD_Q - 1) // ORDER7, FIELD_Q)
    return root, zeta211, zeta7


def character(
    value: int,
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    exponent = (k * p_log_inv * logs[value]) % ORDER7
    return pow(zeta7, exponent, FIELD_Q)


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


def right_dft(profile: list[int], zeta211: int) -> list[int]:
    return [
        sum(
            profile[s] * pow(zeta211, (v * s) % RIGHT, FIELD_Q)
            for s in range(1, RIGHT)
        )
        % FIELD_Q
        for v in range(RIGHT)
    ]


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


def right_multiplicative_resolvent_pairing(
    periods: list[int],
    k: int,
    logs: dict[int, int],
    zeta7: int,
    p_log_inv: int,
) -> int:
    # If B_v is the right additive resolvent and <A,B_v>=periods[v], then
    # this is <A, sum_v chi_k(v) B_v>.
    return sum(
        character(v, k, logs, zeta7, p_log_inv) * periods[v]
        for v in range(1, RIGHT)
    ) % FIELD_Q


def quotient_index(value: int, logs: dict[int, int], p_log_inv: int) -> int:
    return (p_log_inv * logs[value]) % ORDER7


def force_h_coset_sums_zero(
    profile: list[int],
    logs: dict[int, int],
    p_log_inv: int,
) -> list[int]:
    adjusted = profile[:]
    for residue in range(ORDER7):
        members = [
            s
            for s in range(1, RIGHT)
            if quotient_index(s, logs, p_log_inv) == residue
        ]
        total = sum(adjusted[s] for s in members) % FIELD_Q
        adjusted[members[0]] = (adjusted[members[0]] - total) % FIELD_Q
    return adjusted


def force_ordinary_centering(profile: list[int]) -> list[int]:
    adjusted = profile[:]
    adjusted[1] = (adjusted[1] - sum(adjusted[1:])) % FIELD_Q
    return adjusted


def p156_gauss_eigen_check(
    logs: dict[int, int],
    zeta211: int,
    zeta7: int,
    p_log_inv: int,
) -> tuple[int, int, int, int]:
    p156 = pow(P24, 156, RIGHT)
    mismatches = 0
    nonzero_examples = 0
    for k in range(1, ORDER7):
        tau = gauss_sum(k, logs, zeta211, zeta7, p_log_inv)
        tau_twisted = gauss_sum(
            k,
            logs,
            zeta211,
            zeta7,
            p_log_inv,
            exponent_multiplier=p156,
        )
        eigenvalue = character(pow(p156, -1, RIGHT), k, logs, zeta7, p_log_inv)
        mismatches += int(tau_twisted != eigenvalue * tau % FIELD_Q)
        nonzero_examples += int(tau != 0 and eigenvalue != 1)
    return p156, logs[p156] % ORDER7, mismatches, nonzero_examples


def main() -> None:
    logs = log_table_mod_211()
    root, zeta211, zeta7 = roots()
    p_log = logs[P24 % RIGHT]
    p_log_inv = pow(p_log % ORDER7, -1, ORDER7)
    rng = random.Random(20260606)

    bridge_mismatches = 0
    random_nonzero_projections = 0
    centered_nonzero_projections = 0
    forced_zero_projections = 0
    for _trial in range(16):
        profile = [0] + [rng.randrange(FIELD_Q) for _ in range(1, RIGHT)]
        periods = right_dft(profile, zeta211)
        for k in range(1, ORDER7):
            tau = gauss_sum(k, logs, zeta211, zeta7, p_log_inv)
            projection = multiplicative_projection(profile, k, logs, zeta7, p_log_inv)
            pairing = right_multiplicative_resolvent_pairing(
                periods,
                k,
                logs,
                zeta7,
                p_log_inv,
            )
            bridge_mismatches += int(pairing != tau * projection % FIELD_Q)
            random_nonzero_projections += int(projection != 0)

        centered = force_ordinary_centering(profile)
        forced = force_h_coset_sums_zero(profile, logs, p_log_inv)
        for k in range(1, ORDER7):
            centered_nonzero_projections += int(
                multiplicative_projection(centered, k, logs, zeta7, p_log_inv) != 0
            )
            forced_zero_projections += int(
                multiplicative_projection(forced, k, logs, zeta7, p_log_inv) == 0
            )

    p156, p156_quotient_shift, gauss_mismatches, gauss_nonzero_examples = (
        p156_gauss_eigen_check(logs, zeta211, zeta7, p_log_inv)
    )
    sample_projection = 17
    sample_k = 1
    sample_tau = gauss_sum(sample_k, logs, zeta211, zeta7, p_log_inv)
    sample_aug = sample_tau * sample_projection % FIELD_Q
    sample_eigenvalue = character(pow(p156, -1, RIGHT), sample_k, logs, zeta7, p_log_inv)
    sample_aug_twisted = sample_eigenvalue * sample_aug % FIELD_Q

    print("Trace-GCD fixed-frequency multiplicative-resolvent bridge")
    print(f"field_q={FIELD_Q}")
    print(f"field_primitive_root={root}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"p24_log_base_2_mod_211={p_log}")
    print(f"p_log_mod_7={p_log % ORDER7}")
    print(f"p_log_inverse_mod_7={p_log_inv}")
    print(f"bridge_pairing_equals_gauss_times_projection_mismatches={bridge_mismatches}")
    print(f"random_nonzero_multiplicative_projections={random_nonzero_projections}/96")
    print(f"ordinary_centering_nonzero_multiplicative_projections={centered_nonzero_projections}/96")
    print(f"forced_h_coset_zero_projection_zeroes={forced_zero_projections}/96")
    print(f"p24_p156_mod_211={p156}")
    print(f"p24_p156_h_quotient_shift={p156_quotient_shift}")
    print(f"p156_gauss_eigenvalue_mismatches={gauss_mismatches}")
    print(f"p156_nontrivial_gauss_eigen_examples={gauss_nonzero_examples}/6")
    print(f"sample_l_projection_nonzero={int(sample_projection != 0)}")
    print(f"sample_augmentation_nonzero={int(sample_aug != 0)}")
    print(f"sample_augmentation_twisted_nonzero={int(sample_aug_twisted != 0)}")
    print(f"sample_eigenvalue_nontrivial={int(sample_eigenvalue != 1)}")
    print("interpretation")
    print("  h_coboundary_equals_multiplicative_resolvent_orthogonality=1")
    print("  ordinary_centering_does_not_kill_multiplicative_resolvents=1")
    print("  p156_frobenius_eigenvalue_is_carried_by_gauss_sum=1")
    print("  divided_L_projection_can_be_nonzero_after_frobenius_covariance=1")
    print("  frobenius_covariance_alone_does_not_prove_h_coboundary=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_multiplicative_resolvent_bridge")

    if (p_log, p_log % ORDER7, p_log_inv) != (198, 2, 4):
        raise SystemExit(1)
    if bridge_mismatches or random_nonzero_projections != 96:
        raise SystemExit(1)
    if centered_nonzero_projections != 96 or forced_zero_projections != 96:
        raise SystemExit(1)
    if (p156, p156_quotient_shift, gauss_mismatches) != (82, 4, 0):
        raise SystemExit(1)
    if gauss_nonzero_examples != 6:
        raise SystemExit(1)
    if sample_projection == 0 or sample_aug == 0 or sample_aug_twisted == 0:
        raise SystemExit(1)
    if sample_eigenvalue == 1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

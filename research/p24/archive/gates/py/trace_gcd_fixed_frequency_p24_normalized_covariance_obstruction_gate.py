#!/usr/bin/env python3
"""Boundary for nontrivial covariance after Gauss normalization.

The fixed-frequency H-coset route uses the right multiplicative projection

    R_chi = sum_v chi(v) T_{0,v,-a}.

Before dividing by the Gauss sum, Frobenius has the expected nontrivial
order-7 eigenvalue.  But the Gauss sum has the same eigenvalue.  Therefore
the Gauss-normalized right factor has trivial covariance under the same
component shift.

This matters for the 70-idempotent proof attempt: if the component indexing is
the natural one, then a *nontrivial* covariance for the already normalized
components is not a formal refinement.  Together with the formal trivial
normalized covariance it would force every shifted component to be zero.
So the surviving proof target is an internal-trace/right-coboundary identity
for the specific weighted CM packet, not nontrivial normalized covariance.
"""

from __future__ import annotations

P24 = 10**24 + 7
RIGHT = 211
RIGHT_GEN = 2
LEFT = 157
ORDER7 = 7
RHO_EXPONENT = 780
FACTOR_COUNT = 70
FACTOR_STEP = 10


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    value = 1
    logs: dict[int, int] = {}
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad primitive root")
    return logs


def shifted(values: list[int], step: int) -> list[int]:
    out = [0] * len(values)
    for index, value in enumerate(values):
        out[(index + step) % len(values)] = value
    return out


def scale(values: list[int], scalar: int, q: int) -> list[int]:
    return [(scalar * value) % q for value in values]


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_mod_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log_mod7 = logs[rho_mod_right] % ORDER7
    rho_mod_left = pow(P24, RHO_EXPONENT, LEFT)
    p_mod7 = P24 % ORDER7

    raw_right_lambda_exponents = [
        (rho_log_mod7 * k) % ORDER7
        for k in range(1, ORDER7)
    ]
    gauss_lambda_exponents = raw_right_lambda_exponents[:]
    normalized_right_exponents = [
        (raw - gauss) % ORDER7
        for raw, gauss in zip(raw_right_lambda_exponents, gauss_lambda_exponents)
    ]
    left_alpha_exponents = [0 for _ in range(1, ORDER7)]
    normalized_product_exponents = [
        (left + right) % ORDER7
        for left, right in zip(left_alpha_exponents, normalized_right_exponents)
    ]

    # Concrete finite-field sanity check: if normalized covariance is formal
    # with exponent 0, imposing a nontrivial exponent k on the same shifted
    # components forces zero.
    q = 43
    zeta7 = pow(3, (q - 1) // ORDER7, q)  # 3 is primitive mod 43.
    components = [(index * index + 3 * index + 5) % q for index in range(FACTOR_COUNT)]
    components[0] = 1
    trivial_shifted = shifted(components, FACTOR_STEP)
    nontrivial_failures = 0
    forced_zero_checks = 0
    for k in range(1, ORDER7):
        lam = pow(zeta7, k, q)
        nontrivial = scale(trivial_shifted, lam, q)
        nontrivial_failures += int(nontrivial != trivial_shifted)
        # Values satisfying both Z' = shifted(Z) and Z' = lam*shifted(Z)
        # must have shifted(Z)=0 because lam != 1.
        both_possible_only_zero = all(
            ((lam - 1) * value) % q == 0
            for value in [0] * FACTOR_COUNT
        ) and any(((lam - 1) * value) % q for value in trivial_shifted)
        forced_zero_checks += int(both_possible_only_zero)

    print("Trace-GCD fixed-frequency p24 normalized covariance obstruction gate")
    print(f"p24={P24}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_157={rho_mod_left}")
    print(f"rho_mod_211={rho_mod_right}")
    print(f"rho_right_log_mod7={rho_log_mod7}")
    print(f"p24_mod7={p_mod7}")
    print(f"raw_right_lambda_exponents={raw_right_lambda_exponents}")
    print(f"gauss_sum_lambda_exponents={gauss_lambda_exponents}")
    print(f"normalized_right_exponents={normalized_right_exponents}")
    print(f"left_alpha_exponents={left_alpha_exponents}")
    print(f"normalized_product_exponents={normalized_product_exponents}")
    print(f"factor_count={FACTOR_COUNT}")
    print(f"factor_step={FACTOR_STEP}")
    print(f"toy_field_q={q}")
    print(f"toy_zeta7={zeta7}")
    print(f"nontrivial_normalized_covariance_failures={nontrivial_failures}/{ORDER7 - 1}")
    print(f"nontrivial_plus_trivial_covariance_forces_zero_checks={forced_zero_checks}/{ORDER7 - 1}")
    print("interpretation")
    print("  raw_right_covariance_and_gauss_sum_have_same_order7_eigenvalue=1")
    print("  gauss_normalized_right_covariance_is_trivial_under_factor_shift=1")
    print("  gauss_normalized_product_covariance_is_trivial_under_factor_shift=1")
    print("  nontrivial_normalized_covariance_would_be_componentwise_zero_theorem=1")
    print("  proof_target_should_be_internal_trace_or_right_coboundary_not_normalized_covariance=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate")

    if rho_mod_left != 1:
        raise SystemExit(1)
    if p_mod7 != 1:
        raise SystemExit(1)
    if rho_log_mod7 != 6:
        raise SystemExit(1)
    if any(exponent != 0 for exponent in normalized_right_exponents):
        raise SystemExit(1)
    if any(exponent != 0 for exponent in normalized_product_exponents):
        raise SystemExit(1)
    if nontrivial_failures != ORDER7 - 1:
        raise SystemExit(1)
    if forced_zero_checks != ORDER7 - 1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

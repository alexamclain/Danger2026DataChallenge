#!/usr/bin/env python3
"""p24 twist bookkeeping for the product-coboundary target.

The product-coboundary gate leaves a symbolic matching twist:

    sigma(A) = alpha*A
    B = sigma(V) - (epsilon/alpha)*V.

For the fixed-frequency p24 packet terms under sigma=Frob_p^780, the left
157-frequency is fixed.  In the raw quotient convention chi_k(2)=zeta_7^k,
p^780 has right quotient shift 6 mod 7.  Therefore

    lambda_chi = chi(p^780) = zeta_7^(6k)
    epsilon_chi = lambda_chi^(-1) = zeta_7^k,

and alpha=1 for the left factor.  This script records that exact convention,
plus the normalized convention used by some earlier bridge toys where p itself
has quotient index 1.
"""

from __future__ import annotations


P24 = 10**24 + 7
LEFT = 157
RIGHT = 211
RIGHT_GEN = 2
ORDER7 = 7
RHO_EXPONENT = 780


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("generator is not primitive")
    return logs


def scale_exponents(shift: int) -> list[int]:
    return [(shift * k) % ORDER7 for k in range(1, ORDER7)]


def inverse_exponents(exponents: list[int]) -> list[int]:
    return [(-exponent) % ORDER7 for exponent in exponents]


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    p_mod_right = P24 % RIGHT
    p_log = logs[p_mod_right]
    p_log_mod7 = p_log % ORDER7
    p_log_inv_mod7 = pow(p_log_mod7, -1, ORDER7)
    rho_mod_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_mod_right]
    rho_raw_shift = rho_log % ORDER7
    rho_normalized_shift = (p_log_inv_mod7 * rho_log) % ORDER7
    rho_mod_left = pow(P24, RHO_EXPONENT, LEFT)

    raw_lambda = scale_exponents(rho_raw_shift)
    raw_epsilon = inverse_exponents(raw_lambda)
    normalized_lambda = scale_exponents(rho_normalized_shift)
    normalized_epsilon = inverse_exponents(normalized_lambda)
    left_alpha = [0 for _ in range(1, ORDER7)]

    print("Trace-GCD fixed-frequency p24 matching twist bookkeeping gate")
    print(f"p24={P24}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"p24_mod_157={P24 % LEFT}")
    print(f"p24_rho_mod_157={rho_mod_left}")
    print(f"p24_mod_211={p_mod_right}")
    print(f"p24_log_base2_mod_211={p_log}")
    print(f"p24_log_base2_mod7={p_log_mod7}")
    print(f"p24_log_inverse_mod7={p_log_inv_mod7}")
    print(f"rho_mod_211={rho_mod_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_raw_h_quotient_shift={rho_raw_shift}")
    print(f"rho_normalized_h_quotient_shift={rho_normalized_shift}")
    print(f"left_alpha_exponents={left_alpha}")
    print(f"raw_lambda_exponents={raw_lambda}")
    print(f"raw_epsilon_exponents={raw_epsilon}")
    print(f"normalized_lambda_exponents={normalized_lambda}")
    print(f"normalized_epsilon_exponents={normalized_epsilon}")
    print("interpretation")
    print("  p780_fixes_left_157_frequency=1")
    print("  left_covariance_alpha_is_trivial=1")
    print("  raw_lambda_chi_exponent_is_6k=1")
    print("  raw_matching_epsilon_exponent_is_k=1")
    print("  normalized_convention_has_p_index_1_and_rho_shift_3=1")
    print("  matching_right_resolvent_twist_is_now_explicit=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_matching_twist_bookkeeping_gate")

    if rho_mod_left != 1:
        raise SystemExit(1)
    if p_log_mod7 != 2 or p_log_inv_mod7 != 4:
        raise SystemExit(1)
    if rho_raw_shift != 6 or rho_normalized_shift != 3:
        raise SystemExit(1)
    if left_alpha != [0, 0, 0, 0, 0, 0]:
        raise SystemExit(1)
    if raw_epsilon != [1, 2, 3, 4, 5, 6]:
        raise SystemExit(1)
    if normalized_epsilon != [4, 1, 5, 2, 6, 3]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

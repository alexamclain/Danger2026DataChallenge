#!/usr/bin/env python3
"""Principal-conjugate dominance for the p24 Hermitian packet.

For the preferred Hermitian scalar, the fiber P_0(a) contains the principal
singular modulus j_0 with coefficient 1.  Every other term in that fiber has
reduced-form denominator a >= 2, hence size at most exp(pi*sqrt(|Delta|)/2)
up to the standard 2079 error.

This proves characteristic-zero nonvanishing of every Hermitian packet by a
very large margin.  It still does not prove p-adic unit status at the selected
split prime over p.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
TRACE = -1178414874616
H_CLASS = 205880396014
M_QUOTIENT = 66254
N_RELATIVE = 3107441
J_ERROR = 2079.0


def logsumexp(a: float, b: float) -> float:
    hi = max(a, b)
    lo = min(a, b)
    return hi + math.log1p(math.exp(lo - hi))


def log_exp_minus_const(x: float, c: float) -> float:
    logc = math.log(c)
    if x <= logc:
        return float("-inf")
    if x - logc > 50:
        return x + math.log1p(-math.exp(logc - x))
    return math.log(math.exp(x) - c)


def log_exp_minus_exp(x: float, y: float) -> float:
    if x <= y:
        return float("-inf")
    if x - y > 50:
        return x + math.log1p(-math.exp(y - x))
    return y + math.log(math.exp(x - y) - 1)


def main() -> None:
    delta = TRACE * TRACE - 4 * P24
    if delta >= 0:
        raise AssertionError("expected negative CM discriminant")
    if H_CLASS != M_QUOTIENT * N_RELATIVE:
        raise AssertionError("bad h=m*n")

    log_p = math.log(P24)
    s = math.sqrt(abs(delta))
    principal_log = math.pi * s
    principal_lower = log_exp_minus_const(principal_log, J_ERROR)
    one_other_upper = logsumexp(principal_log / 2, math.log(J_ERROR))
    fiber_other_sum_upper = math.log(N_RELATIVE - 1) + one_other_upper
    p0_margin = principal_lower - fiber_other_sum_upper
    p0_lower = log_exp_minus_exp(principal_lower, fiber_other_sum_upper)
    hermitian_lower = 2 * p0_lower

    # Crude upper bound used to show height is still much too large.
    pu_upper = math.log(N_RELATIVE) + logsumexp(principal_log, math.log(J_ERROR))
    hermitian_upper = math.log(M_QUOTIENT) + 2 * pu_upper

    print("p24 Hermitian principal-dominance audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"delta={delta}")
    print(f"m={M_QUOTIENT}")
    print(f"n={N_RELATIVE}")
    print(f"log_p={log_p:.6f}")
    print()
    print("dominance_bounds")
    print(f"  log_principal_lower={principal_lower:.6e}")
    print(f"  log_one_other_upper={one_other_upper:.6e}")
    print(f"  log_fiber_other_sum_upper={fiber_other_sum_upper:.6e}")
    print(f"  p0_dominance_margin={p0_margin:.6e}")
    print(f"  log_abs_P0_lower={p0_lower:.6e}")
    print(f"  log_Hermitian_embedding_lower={hermitian_lower:.6e}")
    print(f"  lower_over_log_p={hermitian_lower / log_p:.6e}")
    print()
    print("height_context")
    print(f"  log_Hermitian_embedding_upper={hermitian_upper:.6e}")
    print(f"  upper_over_log_p={hermitian_upper / log_p:.6e}")
    print()
    print("interpretation")
    print("  P0_fiber_contains_unique_principal_singular_modulus=1")
    print("  principal_term_dominates_other_terms_in_P0_by_enormous_margin=1")
    print("  every_complex_Hermitian_packet_is_nonzero=1")
    print("  dominance_is_archimedean_not_padic=1")
    print("  selected_prime_punit_status_still_unproved=1")
    print(
        "conclusion=Hermitian_packet_has_strong_complex_nonzero_but_no_"
        "height_lift_to_mod_p_certificate"
    )


if __name__ == "__main__":
    main()

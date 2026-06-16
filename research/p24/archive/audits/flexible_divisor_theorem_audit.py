#!/usr/bin/env python3
"""Audit flexible prescribed-divisor theorems against the strict DANGER target.

Shparlinski-Sutherland prove fast/probabilistic results for finding curves
whose order has some divisor m in [M,2M], with M <= p^(1/2-epsilon), and a
deterministic GRH result for a fixed m=o(sqrt(p)/(log p)^4).

DANGER3 is stricter:

    m = 2^k, where 2^k > sqrt(p) + 1 + 2*p^(1/4).

So the required divisor is not flexible and necessarily sits just above
sqrt(p).  This script records the numeric gap for p24 and the asymptotic
reason this theorem family does not solve the verifier target.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7


def main() -> None:
    p = P24
    sqrt_p = math.isqrt(p)
    bound = sqrt_p + 1 + math.isqrt(4 * sqrt_p)
    k = bound.bit_length()
    m = 1 << k
    logp = math.log(p)

    finite_epsilon_for_m_over_2 = math.log(sqrt_p / (m // 2)) / logp
    finite_epsilon_for_m = math.log(sqrt_p / m) / logp

    print("p24 flexible-divisor theorem audit")
    print(f"p={p}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"danger_bound={bound}")
    print(f"danger_k={k}")
    print(f"danger_m=2^k={m}")
    print(f"danger_m_over_sqrt={m / sqrt_p:.12f}")
    print(f"danger_m_minus_sqrt={m - sqrt_p}")
    print(f"sqrt_over_log4={math.sqrt(p) / (logp**4):.6f}")
    print(f"danger_m_over_sqrt_over_log4={m / (math.sqrt(p) / (logp**4)):.6e}")
    print(f"epsilon_if_using_M_2^(k-1)={finite_epsilon_for_m_over_2:.6e}")
    print(f"epsilon_if_using_M_2^k={finite_epsilon_for_m:.6e}")
    print("strict_target=exact_power_of_two_not_arbitrary_divisor")
    print("conclusion=flexible_divisor_theorems_do_not_meet_DANGER3_target")


if __name__ == "__main__":
    main()

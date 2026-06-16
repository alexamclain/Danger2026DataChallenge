#!/usr/bin/env python3
"""Numerically audit the Shparlinski-Sutherland range for p24.

Their deterministic GRH construction applies to subgroup divisibility

    m = o(p^(1/2) / (log p)^4)

with running time roughly m*p^(1/2+o(1)).  The DANGER3 single-point target
needs m = 2^k with k=40 for p=10^24+7, which is essentially sqrt(p), far
outside the proven range and with no useful running-time saving.
"""

from __future__ import annotations

from math import isqrt, log

P24 = 10**24 + 7


def main() -> None:
    p = P24
    q = isqrt(p)
    danger_bound = q + 1 + isqrt(4 * q)
    k = danger_bound.bit_length()
    m = 1 << k
    ss_threshold = p**0.5 / (log(p) ** 4)

    print("p24 prescribed-subgroup range audit")
    print(f"p={p}")
    print(f"sqrt_floor={q}")
    print(f"danger_bound={danger_bound}")
    print(f"k={k}")
    print(f"m=2^k={m}")
    print(f"sqrt_over_log4={ss_threshold:.6f}")
    print(f"m_over_sqrt_over_log4={m / ss_threshold:.6e}")
    print(f"heuristic_runtime_m_sqrtp={m * q:.6e}")
    print("conclusion=known_prescribed_subgroup_theorem_is_far_out_of_range")


if __name__ == "__main__":
    main()

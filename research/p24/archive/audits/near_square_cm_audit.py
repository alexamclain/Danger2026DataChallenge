#!/usr/bin/env python3
"""Audit the tempting near-square CM construction for p = 10^24 + 7.

The prime is

    p = 10^24 + 7 = (10^12)^2 + 7.

This represents p by the CM field of fundamental discriminant -7.  The
corresponding CM traces are t = +/- 2*10^12.  They are extremely cheap to
construct, but the DANGER3 verifier needs v2(#E) or v2(#E_twist) at least 40.
"""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7
N = 10**12
DANGER_K = 40
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def main() -> None:
    print("p24 near-square small-CM audit")
    print(f"p={P24}")
    print(f"p_minus_n_squared={P24 - N * N}")
    print(f"fundamental_CM_D=-7")
    print(f"danger_k={DANGER_K}")
    print(f"danger_target_traces={TARGET_TRACES}")
    print()

    for trace in (2 * N, -2 * N):
        order = P24 + 1 - trace
        twist_order = P24 + 1 + trace
        print(f"cm_trace={trace}")
        print(f"  trace_mod_2^40={trace % (1 << DANGER_K)}")
        print(f"  min_abs_distance_to_target={min(abs(trace - t) for t in TARGET_TRACES)}")
        print(f"  v2_order={v2(order)}")
        print(f"  v2_twist_order={v2(twist_order)}")
        print(f"  partial_factor_order={sp.factorint(order, limit=1_000_000)}")
        print()

    print("conclusion=near_square_CM_is_a_fast_known_trace_but_not_a_DANGER3_depth_40_trace")


if __name__ == "__main__":
    main()

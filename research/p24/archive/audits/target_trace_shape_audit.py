#!/usr/bin/env python3
"""Audit the elementary shape of the p24 DANGER target traces.

For p = n^2 + 7 with n = 10^12, the DANGER congruence is

    t == p + 1 == n^2 + 8  (mod 2^40)

on the curve side, and the x-only verifier also allows the opposite sign
branch.  This script records the six Hasse representatives and compares them
with the obvious low-height traces 0, +/-n, +/-2n coming from small-CM-looking
near-square formulas.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
N = 10**12
K = 40
M = 1 << K


def v2(x: int) -> int:
    return (x & -x).bit_length() - 1


def hasse_representatives(residue: int) -> list[int]:
    bound = math.isqrt(4 * P24)
    out = []
    first = -bound + ((residue + bound) % M)
    t = first
    while t <= bound:
        out.append(t)
        t += M
    return out


def main() -> None:
    r = (P24 + 1) % M
    quotient = (P24 + 1) // M
    signed = sorted(set(hasse_representatives(r)) | set(hasse_representatives(-r)))
    low_height = [0, N, -N, 2 * N, -2 * N]

    print("p24 target trace shape audit")
    print(f"p={P24}")
    print(f"n={N}")
    print(f"p_minus_n_squared={P24 - N * N}")
    print(f"k={K}")
    print(f"modulus_2^k={M}")
    print(f"quotient_floor((p+1)/2^k)={quotient}")
    print(f"curve_side_residue=(p+1)_mod_2^k={r}")
    print(f"curve_side_residue_decomposition=8 + 2^24 * {(r - 8) // (1 << 24)}")
    print(f"opposite_xonly_residue={(-r) % M}")
    print(f"v2(curve_side_residue)={v2(r)}")
    print("curve_side_trace_progression:")
    for offset in range(3):
        t = r - offset * M
        order_odd = (P24 + 1 - t) // M
        print(f"  t=r-{offset}*2^k={t} order_div_2^k={order_odd}")
    print()
    print("signed_hasse_representatives:")
    for t in signed:
        print(
            f"  t={t} residue={t % M} "
            f"v2(p+1-t)={v2(P24 + 1 - t)} v2(p+1+t)={v2(P24 + 1 + t)}"
        )
    print()
    print("obvious_low_height_near_square_traces:")
    for t in low_height:
        nearest = min(signed, key=lambda u: abs(u - t))
        print(
            f"  t={t} residue={t % M} "
            f"v2(p+1-t)={v2(P24 + 1 - t)} v2(p+1+t)={v2(P24 + 1 + t)} "
            f"nearest_target={nearest} distance={abs(nearest - t)}"
        )
    print("conclusion=target_traces_are_only_the_2^40_residue_representatives_not_low_height_CM_traces")


if __name__ == "__main__":
    main()

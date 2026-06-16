#!/usr/bin/env python3
"""X0-to-X1 orientation-cover tradeoff for p24.

`X0(2^d)` records a rational cyclic 2^d subgroup.  The DANGER verifier needs
an x-only point of order 2^d, i.e. an orientation/generator up to sign.  The
cover from oriented x-only data to an X0 subgroup has degree

    phi(2^d) / 2 = 2^(d-2)      for d >= 2.

This script quantifies the tradeoff.  The X0 trace-residue condition gives
only a constant-factor gain for p == 7 mod 16; paying the orientation cover
cost grows like 2^d and cancels the hoped-for asymptotic improvement.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
K = 40


def gamma0_power2(depth: int) -> int:
    return 3 * (1 << (depth - 1))


def orientation_cover_degree(depth: int) -> int:
    if depth < 2:
        return 1
    return 1 << (depth - 2)


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 X0-to-X1 orientation degree tradeoff audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"sqrt_floor={sqrt_p}")
    print(
        "depth gamma0/sqrt orientation_cover residual_2^(k-d) "
        "free_x0_cover_residual/sqrt oriented_index/sqrt oriented_index_times_residual/sqrt"
    )

    for depth in range(4, K + 1, 4):
        gamma0 = gamma0_power2(depth)
        cover = orientation_cover_degree(depth)
        residual = 1 << max(0, K - depth)
        cover_residual = cover * residual
        full_oriented = gamma0 * cover
        total_oriented_proxy = full_oriented * residual
        print(
            f"{depth:2d} {gamma0 / sqrt_p:12.6e} {cover:17d} {residual:17d} "
            f"{cover_residual / sqrt_p:28.6f} {full_oriented / sqrt_p:20.6e} "
            f"{total_oriented_proxy / sqrt_p:35.6e}"
        )

    print("conclusion=X0_orientation_cover_cost_grows_like_the_missing_X1_level")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit singular Montgomery torus degeneration shortcuts for p24.

The only genuine rational power-map shortcuts for Montgomery doubling occur in
the singular limits A = +/-2.  These collapse to multiplicative/norm-one tori,
where 2-power depth is controlled by v2(p-1) or v2(p+1).

The DANGER3 verifier rejects A^2 = 4, but this audit also checks that p24 has
too little 2-power in either torus even before that rejection.
"""

from __future__ import annotations

P24 = 10**24 + 7
DANGER_K = 40


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def main() -> None:
    print("p24 singular Montgomery torus degeneration audit")
    print(f"p={P24}")
    print(f"danger_k={DANGER_K}")
    print(f"v2(p-1)={v2(P24 - 1)}")
    print(f"v2(p+1)={v2(P24 + 1)}")
    print(f"v2(p^2-1)={v2(P24 * P24 - 1)}")
    print(f"max_split_torus_2power=2^{v2(P24 - 1)}")
    print(f"max_nonsplit_torus_2power=2^{v2(P24 + 1)}")
    print("verifier_rejects_A_equals_plus_minus_2=True")
    print("conclusion=singular_power_map_shortcut_has_only_2^3_depth_and_is_rejected")


if __name__ == "__main__":
    main()

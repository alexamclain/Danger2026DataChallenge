#!/usr/bin/env python3
"""Convert the near-square CM certificate curve to Montgomery form.

This checks whether the fast D=-7 elliptic certificate fails DANGER3 merely
because it is in the wrong model.  It does not: the curve has Montgomery
models over F_p, but their curve and twist orders both have v2 = 3, and since
they are split Montgomery curves their rational 2-primary exponent is at most
2^(3-1) = 4.
"""

from __future__ import annotations

import random

import near_square_ecpp_certificate as cert

P24 = cert.P24


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    v = pow(a, (p - 1) // 2, p)
    return -1 if v == p - 1 else 1


def main() -> None:
    E = cert.curve_from_j(P24, cert.J)
    trace, order = cert.detect_order(E)
    twist_order = P24 + 1 + trace
    rng = random.Random(456)

    two_torsion = None
    four_torsion = None
    for _ in range(100):
        P = cert.find_point(E, rng)
        T2 = cert.mul(E, order // 4, P)
        if T2 is not None and T2[1] == 0:
            two_torsion = T2
        T4 = cert.mul(E, order // 8, P)
        if T4 is not None and cert.mul(E, 2, T4) is not None:
            four_torsion = T4
        if two_torsion and four_torsion:
            break

    if two_torsion is None:
        raise RuntimeError("failed to find rational 2-torsion")

    alpha = two_torsion[0]
    d = (3 * alpha * alpha + E.a) % P24
    if legendre(d, P24) != 1:
        raise RuntimeError("2-torsion root does not give Montgomery model over F_p")

    s0 = pow(d, (P24 + 1) // 4, P24)
    As = []
    for s in (s0, (-s0) % P24):
        As.append((3 * alpha * cert.inv(s, P24)) % P24)

    print("p24 near-square CM Montgomery bridge audit")
    print(f"p={P24}")
    print(f"trace={trace}")
    print(f"order={order}")
    print(f"twist_order={twist_order}")
    print(f"v2_order={cert.v2(order)}")
    print(f"v2_twist_order={cert.v2(twist_order)}")
    print(f"two_torsion_x={alpha}")
    if four_torsion is not None:
        print(f"four_torsion_x={four_torsion[0]}")
    for A in As:
        split = legendre(A * A - 4, P24)
        max_curve_2_exponent = cert.v2(order) - 1 if split == 1 else cert.v2(order)
        max_twist_2_exponent = cert.v2(twist_order) - 1 if split == 1 else cert.v2(twist_order)
        print(f"montgomery_A={A}")
        print(f"  split_legendre_A2_minus_4={split}")
        print(f"  max_curve_2power_exponent={max_curve_2_exponent}")
        print(f"  max_twist_2power_exponent={max_twist_2_exponent}")
    print("danger_k=40")
    print("conclusion=near_square_CM_has_Montgomery_models_but_max_xonly_2power_is_4")


if __name__ == "__main__":
    main()

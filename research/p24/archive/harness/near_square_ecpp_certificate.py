#!/usr/bin/env python3
"""Construct a fast non-DANGER elliptic certificate from the near-square CM curve.

Because

    p = 10^24 + 7 = (10^12)^2 + 7,

the class-number-one CM field of discriminant -7 gives curves with
trace +/- 2*10^12 and j = -15^3 = -3375.  This produces an ordinary elliptic
certificate with a large prime factor of the group order in polylogarithmic
work once the CM trace is recognized.

This is intentionally not a DANGER3 x-only certificate: the group orders have
only v2 = 3, so no point on this curve or its twist can have order 2^40.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import sympy as sp

P24 = 10**24 + 7
N0 = 10**12
J = -3375
OUT = Path(__file__).with_name("near_square_ecpp_certificate.json")


Point = Optional[tuple[int, int]]


@dataclass(frozen=True)
class Curve:
    p: int
    a: int
    b: int


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def sqrt_mod_p3(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    return pow(a, (p + 1) // 4, p)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def curve_from_j(p: int, j: int) -> Curve:
    # For j not 0 or 1728, E: y^2 = x^3 + 3k*x + 2k has j-invariant j,
    # where k = j/(1728-j).
    k = (j % p) * inv(1728 - j, p) % p
    return Curve(p=p, a=3 * k % p, b=2 * k % p)


def j_invariant(E: Curve) -> int:
    p = E.p
    num = 1728 * 4 * pow(E.a, 3, p)
    den = (4 * pow(E.a, 3, p) + 27 * pow(E.b, 2, p)) % p
    return num * inv(den, p) % p


def add(E: Curve, P: Point, Q: Point) -> Point:
    p = E.p
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        if y1 == 0:
            return None
        lam = (3 * x1 * x1 + E.a) * inv(2 * y1, p) % p
    else:
        lam = (y2 - y1) * inv(x2 - x1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return x3, y3


def mul(E: Curve, n: int, P: Point) -> Point:
    R: Point = None
    Q = P
    while n:
        if n & 1:
            R = add(E, R, Q)
        Q = add(E, Q, Q)
        n >>= 1
    return R


def rhs(E: Curve, x: int) -> int:
    return (pow(x, 3, E.p) + E.a * x + E.b) % E.p


def find_point(E: Curve, rng: random.Random) -> Point:
    while True:
        x = rng.randrange(0, E.p)
        y = sqrt_mod_p3(rhs(E, x), E.p)
        if y is not None:
            return x, y


def detect_order(E: Curve) -> tuple[int, int]:
    candidates = [(2 * N0, P24 + 1 - 2 * N0), (-2 * N0, P24 + 1 + 2 * N0)]
    rng = random.Random(20260603)
    witnesses = [find_point(E, rng) for _ in range(4)]
    for trace, order in candidates:
        if all(mul(E, order, P) is None for P in witnesses):
            return trace, order
    raise RuntimeError("could not determine CM trace sign")


def build_certificate() -> dict:
    E = curve_from_j(P24, J)
    if j_invariant(E) != J % P24:
        raise AssertionError("bad j-invariant")

    trace, order = detect_order(E)
    factors = {int(q): int(e) for q, e in sp.factorint(order).items()}
    q = max(factors)
    if not sp.isprime(q):
        raise AssertionError("largest factor is not prime")
    if q <= math.isqrt(P24):
        raise AssertionError("largest factor does not exceed sqrt(p)")

    rng = random.Random(20260604)
    while True:
        P = find_point(E, rng)
        if mul(E, order, P) is not None:
            raise AssertionError("detected order does not annihilate point")
        Q = mul(E, order // q, P)
        if Q is not None:
            if mul(E, q, Q) is not None:
                raise AssertionError("q-subgroup point does not have q-torsion")
            break

    return {
        "kind": "near_square_cm_non_danger_ecpp_certificate",
        "p": str(P24),
        "cm_discriminant": -7,
        "j": J,
        "curve": {"model": "short_weierstrass", "a": str(E.a), "b": str(E.b)},
        "trace": str(trace),
        "order": str(order),
        "order_factorization": {str(k): v for k, v in sorted(factors.items())},
        "large_prime_factor": str(q),
        "large_prime_is_prime": bool(sp.isprime(q)),
        "large_prime_minus_1_factorization": {
            str(k): int(v) for k, v in sorted(sp.factorint(q - 1).items())
        },
        "large_prime_gt_sqrt_p": q > math.isqrt(P24),
        "v2_order": v2(order),
        "danger_k": 40,
        "point": {"x": str(P[0]), "y": str(P[1])},
        "q_torsion_point": {"x": str(Q[0]), "y": str(Q[1])},
    }


def verify_certificate(cert: dict) -> None:
    E = Curve(
        p=int(cert["p"]),
        a=int(cert["curve"]["a"]),
        b=int(cert["curve"]["b"]),
    )
    order = int(cert["order"])
    q = int(cert["large_prime_factor"])
    P = (int(cert["point"]["x"]), int(cert["point"]["y"]))
    Q = (int(cert["q_torsion_point"]["x"]), int(cert["q_torsion_point"]["y"]))

    if rhs(E, P[0]) != P[1] * P[1] % E.p:
        raise AssertionError("point is not on curve")
    if rhs(E, Q[0]) != Q[1] * Q[1] % E.p:
        raise AssertionError("q-torsion point is not on curve")
    if mul(E, order, P) is not None:
        raise AssertionError("[order]P != O")
    if mul(E, order // q, P) != Q:
        raise AssertionError("[order/q]P != Q")
    if mul(E, q, Q) is not None:
        raise AssertionError("[q]Q != O")
    if Q is None:
        raise AssertionError("Q is infinity")
    if not sp.isprime(q):
        raise AssertionError("q is not prime")
    if q <= math.isqrt(E.p):
        raise AssertionError("q <= sqrt(p)")


def main() -> None:
    cert = build_certificate()
    verify_certificate(cert)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    verify_certificate(json.loads(OUT.read_text()))

    print(f"wrote {OUT}")
    print(f"p={P24}")
    print(f"j={J}")
    print(f"trace={cert['trace']}")
    print(f"order={cert['order']}")
    print(f"order_factorization={cert['order_factorization']}")
    print(f"large_prime_factor={cert['large_prime_factor']}")
    print(f"large_prime_gt_sqrt_p={cert['large_prime_gt_sqrt_p']}")
    print(f"v2_order={cert['v2_order']}")
    print("verification=PASS")
    print("danger3_bridge=NO_v2_order_is_only_3")


if __name__ == "__main__":
    main()

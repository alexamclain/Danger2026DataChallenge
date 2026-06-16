#!/usr/bin/env python3
"""Audit the level-shifted X0 idea for DANGER3 p24.

Potential loophole:

    X0(2^k) by itself only gives an invariant cyclic subgroup and misses the
    orientation needed for a rational point of order 2^k.  But X0(2^(k+1))
    with Frobenius eigenvalue lambda == 1 mod 2^k would make 2P rational for
    a generator P of the invariant subgroup, yielding a rational point of
    order 2^k.

This is true as a level-shift statement, but it does not give an asymptotic
speedup: the X0(2^(k+1)) modular curve has index about 3*2^k, and selecting
lambda == 1 mod 2^k is exactly the missing orientation information in another
form.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def gamma0_index_power2(a: int) -> int:
    # [SL2(Z):Gamma0(2^a)] = 2^a * (1 + 1/2)
    return 3 * (1 << (a - 1))


def danger_trace_representatives(modulus: int) -> list[int]:
    bound = math.isqrt(4 * P24)
    residue = (P24 + 1) % modulus
    out = []
    first = -bound + ((residue + bound) % modulus)
    t = first
    while t <= bound:
        out.append(t)
        t += modulus
    return out


def eigen_roots_for_trace_residue(a: int, residue: int) -> list[int]:
    # For the specific residue t=p+1, use the factorization
    # (lambda-1)(lambda-p)=0 mod 2^a.
    modulus = 1 << a
    if residue % modulus != (P24 + 1) % modulus:
        raise ValueError("only implemented for t == p+1 mod 2^a")
    half = 1 << (a - 1)
    return sorted({1 % modulus, (1 + half) % modulus, P24 % half, (P24 % half + half) % modulus})


def main() -> None:
    k = verifier_k(P24)
    q = math.isqrt(P24)
    print("p24 level-shifted X0 audit")
    print(f"p={P24}")
    print(f"sqrt_floor={q}")
    print(f"danger_k={k}")
    print(f"2^k={1 << k}")
    print()

    for a in (k, k + 1):
        modulus = 1 << a
        residue = (P24 + 1) % modulus
        reps = danger_trace_representatives(modulus)
        print(f"level_a={a}")
        print(f"  modulus=2^{a}={modulus}")
        print(f"  gamma0_index={gamma0_index_power2(a)}")
        print(f"  gamma0_index_over_sqrt_p={gamma0_index_power2(a) / q:.6f}")
        print(f"  trace_residue_p_plus_1={residue}")
        print(f"  hasse_representatives={reps}")
        for t in reps:
            print(f"    t={t} v2(p+1-t)={v2(P24 + 1 - t)}")
        for lam in eigen_roots_for_trace_residue(a, residue):
            mu = P24 * pow(lam, -1, modulus) % modulus
            rational_after_doubling = v2(lam - 1) >= k or v2(mu - 1) >= k
            rational_at_level = v2(lam - 1) >= a or v2(mu - 1) >= a
            print(
                f"    lambda={lam} mu={mu} "
                f"v2(lambda-1)={min(v2(lam - 1), a)} "
                f"v2(mu-1)={min(v2(mu - 1), a)} "
                f"rational_order_2^k_after_doubling={rational_after_doubling} "
                f"x1_at_level_2^a={rational_at_level}"
            )
        print()

    print(
        "conclusion=level_shift_X0_can_encode_rational_2^k_but_at_index_Theta(2^k),"
        "_so_it_is_not_an_asymptotic_speedup_sampler"
    )


if __name__ == "__main__":
    main()

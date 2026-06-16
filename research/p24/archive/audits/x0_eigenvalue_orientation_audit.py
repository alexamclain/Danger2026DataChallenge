#!/usr/bin/env python3
"""Exact p24 X0(2^a) Frobenius eigenvalue orientation audit.

The X0 trace condition for a cyclic subgroup of order 2^a is

    t == lambda + p/lambda  (mod 2^a), lambda odd.

For the DANGER curve-side trace residue t == p+1, this factors as

    (lambda - 1) * (lambda - p) == 0 (mod 2^a).

Since v2(p-1)=1, this has four roots modulo 2^a for a>=2.  Two are the
true X1 orientations (one eigenvalue is 1 mod 2^a); the other two split the
2-adic vanishing as (a-1)+1 and do not by themselves mark a rational point of
order 2^a.
"""

from __future__ import annotations

P24 = 10**24 + 7


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def roots_for_danger_residue(a: int) -> list[int]:
    modulus = 1 << a
    half = 1 << (a - 1)
    return sorted({1 % modulus, (1 + half) % modulus, P24 % half, (P24 % half + half) % modulus})


def signed(x: int, modulus: int) -> int:
    return x if x < modulus // 2 else x - modulus


def main() -> None:
    print("p24 X0(2^a) eigenvalue orientation audit")
    print(f"p={P24}")
    print(f"v2(p-1)={v2(P24 - 1)}")
    print(f"v2(p+1)={v2(P24 + 1)}")
    print()

    for a in (8, 16, 24, 32, 40):
        modulus = 1 << a
        target = (P24 + 1) % modulus
        print(f"a={a} target_trace_residue={target}")
        for lam in roots_for_danger_residue(a):
            mu = P24 * pow(lam, -1, modulus) % modulus
            ok = (lam + mu - target) % modulus == 0
            fixed_lam = min(v2(lam - 1), a)
            fixed_mu = min(v2(mu - 1), a)
            x1_orientation = fixed_lam >= a or fixed_mu >= a
            print(
                f"  lambda={lam} signed={signed(lam, modulus)} "
                f"mu={mu} signed_mu={signed(mu, modulus)} ok={ok} "
                f"v2(lambda-1)={fixed_lam} v2(mu-1)={fixed_mu} "
                f"x1_orientation={x1_orientation}"
            )
        print()

    print("conclusion=X0_has_four_orientations_but_only_two_are_true_X1_at_level_2^a")


if __name__ == "__main__":
    main()

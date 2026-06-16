#!/usr/bin/env python3
"""Consolidate the p24 CM/ray-orientation obstruction.

The strict DANGER condition can be phrased as a 2-adic Frobenius orientation:
one eigenvalue is 1 modulo 2^k on the relevant cyclic 2-primary direction.
This script puts the relevant CM/ray facts in one place:

* the target CM fields have D_K == 1 mod 8, so 2 splits;
* the target order has conductor 2 and ring-class multiplier 1;
* X0 has four eigenvalue roots for the DANGER trace residue, but only two are
  true X1 orientations;
* shifting to X0(2^(k+1)) has index Theta(2^k), about 3.3*sqrt(p).
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(n).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def target_cm_data(t: int) -> tuple[int, int, int]:
    delta_abs = 4 * P24 - t * t
    sf = squarefree_part(delta_abs)
    D_K = fundamental_discriminant_for_negative_squarefree(sf)
    conductor_sq = delta_abs // abs(D_K)
    conductor = math.isqrt(conductor_sq)
    if conductor * conductor != conductor_sq:
        raise AssertionError("bad conductor")
    return delta_abs, D_K, conductor


def ring_class_multiplier_for_conductor_two(D_K: int) -> str:
    # h(4D_K)/h(D_K) = 2 * (1 - kronecker(D_K,2)/2), up to the unit index.
    # These huge fields have only +/-1 units; D_K == 1 mod 8 gives chi(2)=1.
    chi2 = sp.kronecker_symbol(D_K, 2)
    num = 2 * (2 - chi2)
    den = 2
    g = math.gcd(num, den)
    return f"{num // g}/{den // g}"


def roots_for_danger_residue(a: int) -> list[int]:
    modulus = 1 << a
    half = 1 << (a - 1)
    return sorted({1 % modulus, (1 + half) % modulus, P24 % half, (P24 % half + half) % modulus})


def gamma0_index_power2(a: int) -> int:
    return 3 * (1 << (a - 1))


def main() -> None:
    q = math.isqrt(P24)
    k = verifier_k(P24)
    print("p24 ray/orientation audit")
    print(f"p={P24}")
    print(f"sqrt_floor={q}")
    print(f"k={k}")
    print(f"2^k={1 << k}")
    print()

    for t in TRACES:
        delta_abs, D_K, conductor = target_cm_data(t)
        print(f"trace={t}")
        print(f"  abs_delta={delta_abs}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  D_K_mod_8={D_K % 8}")
        print(f"  two_splits={D_K % 8 == 1}")
        print(f"  conductor_Zpi_in_OK={conductor}")
        print(f"  v2_conductor={v2(conductor)}")
        print(f"  ring_class_multiplier_h_4D_over_h_D={ring_class_multiplier_for_conductor_two(D_K)}")
        print()

    modulus = 1 << k
    target = (P24 + 1) % modulus
    print(f"curve_side_target_trace_residue_mod_2^k={target}")
    print("x0_eigenvalue_roots_at_level_k:")
    for lam in roots_for_danger_residue(k):
        mu = P24 * pow(lam, -1, modulus) % modulus
        fixed_lam = min(v2(lam - 1), k)
        fixed_mu = min(v2(mu - 1), k)
        print(
            f"  lambda={lam} mu={mu} "
            f"v2(lambda-1)={fixed_lam} v2(mu-1)={fixed_mu} "
            f"x1_orientation={fixed_lam >= k or fixed_mu >= k}"
        )
    print()

    for a in (k, k + 1):
        idx = gamma0_index_power2(a)
        print(
            f"Gamma0(2^{a})_index={idx} "
            f"index_over_sqrt_p={idx / q:.6f}"
        )
    print(
        "conclusion=ray_orientation_is_the_X0_to_X1_gap_and_level_shift_is_theta_2^k"
    )


if __name__ == "__main__":
    main()

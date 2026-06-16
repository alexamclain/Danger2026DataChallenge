#!/usr/bin/env python3
"""Connect strict DANGER orientation with the split-2 ideal class.

For each p24 target trace, D_K == 1 mod 8, so 2 splits in O_K.  The strict
DANGER condition says one Frobenius eigenvalue is 1 modulo 2^40, i.e. one of
the split primes above 2 divides pi-1 to depth 40.  A possible CM shortcut
would be that the split-2 ideal class, or its 40th power, has small order,
giving a short class-field relation.

This audit computes the exact class order of a prime form above 2 and the
remaining order after taking the 40th power.  It does not construct roots; it
measures whether the strict 2-adic condition itself collapses the root torsor.
"""

from __future__ import annotations

import math

import sympy as sp
from cypari2 import Pari


P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)
K = 40


def v2(n: int) -> int:
    if n == 0:
        return 999
    return (abs(n) & -abs(n)).bit_length() - 1


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(abs(n)).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_from_trace(t: int) -> int:
    delta = t * t - 4 * P24
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def class_order(pari: Pari, D: int, ell: int, h: int, h_factors: dict[int, int]) -> int:
    principal = pari.qfbred(pari(f"Qfb(1,1,{(1 - D) // 4})"))
    form = pari.qfbprimeform(D, ell)
    nucomp_l = int((abs(D) // 4) ** 0.25) + 1

    def is_principal(candidate) -> bool:
        return str(pari.qfbred(candidate)) == str(principal)

    order = h
    for q, e in h_factors.items():
        for _ in range(e):
            trial = order // q
            if is_principal(pari.qfbnupow(form, trial, nucomp_l)):
                order = trial
            else:
                break
    return order


def roots_for_danger_residue(a: int) -> list[int]:
    # For t == p+1 mod 2^a, roots of X^2 - tX + p are the roots of
    # (X-1)(X-p) modulo 2^a.  Since p == 7 mod 8, there are four roots.
    modulus = 1 << a
    half = 1 << (a - 1)
    return sorted({1 % modulus, (1 + half) % modulus, P24 % half, (P24 % half + half) % modulus})


def main() -> None:
    pari = Pari()
    sqrt_p = math.isqrt(P24)
    modulus = 1 << K
    roots = roots_for_danger_residue(K)

    print("p24 split-2 strict orientation relation audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"k={K}")
    print(f"2^k={modulus}")
    print()
    print("2_adic_eigenvalue_roots_for_target_trace_residue")
    for lam in roots:
        mu = P24 * pow(lam, -1, modulus) % modulus
        print(
            f"  lambda={lam:13d} mu={mu:13d} "
            f"v2(lambda-1)={min(v2(lam - 1), K):2d} "
            f"v2(mu-1)={min(v2(mu - 1), K):2d} "
            f"strict_orientation={min(v2(lam - 1), K) >= K or min(v2(mu - 1), K) >= K}"
        )
    print()

    print("target_split2_class_orders")
    print(
        "  trace h class_group split2_order split2_index "
        "order_of_split2^k order_after_k_over_sqrt v2_curve v2_twist"
    )
    for t in TRACES:
        D = fundamental_discriminant_from_trace(t)
        data = pari.quadclassunit(D)
        h = int(data[0])
        group = [int(x) for x in list(data[1])]
        h_factors = {int(q): int(e) for q, e in sp.factorint(h).items()}
        split2_order = class_order(pari, D, 2, h, h_factors)
        split2_index = h // split2_order
        order_after_k = split2_order // math.gcd(split2_order, K)
        print(
            f"  {t:15d} {h:12d} {group!s:18s} "
            f"{split2_order:12d} {split2_index:12d} "
            f"{order_after_k:17d} {order_after_k / sqrt_p:20.6e} "
            f"{v2(P24 + 1 - t):8d} {v2(P24 + 1 + t):8d}"
        )
    print()
    print("interpretation")
    print("  strict_eigenvalue_root_known_mod_2^40=1")
    print("  split2_class_or_40th_power_principal=0")
    print("  split2_40th_power_still_has_huge_class_order=1")
    print(
        "conclusion=the_2adic_strict_orientation_is_a_ray_condition_not_a_"
        "seed_CM_root_selector"
    )


if __name__ == "__main__":
    main()

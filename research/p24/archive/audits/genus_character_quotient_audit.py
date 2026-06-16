#!/usr/bin/env python3
"""Audit genus-character quotients for the p24 target CM orders.

The target traces have order discriminant Delta = t^2 - 4p = 4*D_K, where
D_K is a large odd fundamental discriminant and the conductor is 2.  Since
D_K == 1 mod 8 in all three cases, 2 splits in the maximal order and the
conductor-2 ring class multiplier is 1.  Thus the class group of Z[pi] has
the same size as the maximal class group for this audit.

Genus characters only see the class group modulo squares.  For an odd
fundamental discriminant with r prime-discriminant factors, that quotient has
size 2^(r-1).  The p24 target fields have r = 2, 4, and 2, so full genus
information reveals only 1, 3, and 1 bits respectively.
"""

from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)
EULER_PRODUCT_PRIME_BOUND = 200_000


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(n).items():
        if exp & 1:
            out *= prime
    return out


def fundamental_discriminant_for_negative_squarefree(sf: int) -> int:
    d = -sf
    return d if d % 4 == 1 else 4 * d


def prime_discriminant_factors(D: int) -> list[int]:
    """Return the odd prime discriminants for an odd fundamental D."""
    if D % 2 == 0 or D % 4 != 1:
        raise ValueError(f"expected odd fundamental discriminant, got {D}")

    factors: list[int] = []
    for prime in sorted(sp.factorint(abs(D))):
        factors.append(prime if prime % 4 == 1 else -prime)

    product = math.prod(factors)
    if product != D:
        raise AssertionError((D, factors, product))
    return factors


def genus_count_for_odd_fundamental(D: int) -> int:
    return 1 << max(0, len(prime_discriminant_factors(D)) - 1)


def ring_class_multiplier(D_K: int, conductor: int) -> Fraction:
    multiplier = Fraction(conductor, 1)
    for ell in sp.factorint(conductor):
        chi = sp.kronecker_symbol(D_K, ell)
        multiplier *= Fraction(ell - chi, ell)
    return multiplier


def euler_product_l1(D: int, prime_bound: int) -> float:
    product = 1.0
    for ell in sp.primerange(2, prime_bound + 1):
        chi = sp.kronecker_symbol(D, ell)
        if chi:
            product *= 1.0 / (1.0 - chi / ell)
    return product


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 genus-character quotient audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"euler_product_prime_bound={EULER_PRODUCT_PRIME_BOUND}")
    print()

    for trace in TRACES:
        abs_delta = 4 * P24 - trace * trace
        sf = squarefree_part(abs_delta)
        D_K = fundamental_discriminant_for_negative_squarefree(sf)
        conductor_sq = abs_delta // abs(D_K)
        conductor = math.isqrt(conductor_sq)
        if conductor * conductor != conductor_sq:
            raise AssertionError((trace, abs_delta, D_K, conductor_sq))

        order_discriminant = conductor * conductor * D_K
        prime_discriminants = prime_discriminant_factors(D_K)
        max_genus_count = genus_count_for_odd_fundamental(D_K)
        multiplier = ring_class_multiplier(D_K, conductor)
        order_genus_count_upper_bound = max_genus_count * multiplier.numerator

        L_est = euler_product_l1(D_K, EULER_PRODUCT_PRIME_BOUND)
        h_max_est = math.sqrt(abs(D_K)) * L_est / math.pi
        h_order_est = h_max_est * float(multiplier)
        residual_classes_est = h_order_est / order_genus_count_upper_bound

        print(f"trace={trace}")
        print(f"  target_order_discriminant={order_discriminant}")
        print(f"  maximal_fundamental_D_K={D_K}")
        print(f"  factor_abs_D_K={sp.factorint(abs(D_K))}")
        print(f"  prime_discriminant_factors={prime_discriminants}")
        print(f"  conductor_in_Zpi={conductor}")
        print(f"  kronecker_DK_2={sp.kronecker_symbol(D_K, 2)}")
        print(f"  ring_class_multiplier={multiplier}")
        print(f"  conductor_kernel_trivial={multiplier == 1}")
        print(f"  genus_character_count={max_genus_count}")
        print(f"  genus_bits={math.log2(max_genus_count):.0f}")
        print(f"  h_order_est={h_order_est:.6e}")
        print(f"  residual_classes_per_genus_est={residual_classes_est:.6e}")
        print(f"  residual_entropy_bits_est={math.log2(residual_classes_est):.3f}")
        print()

    print(
        "conclusion=full_genus_information_saves_only_constant_bits_and_leaves_"
        "about_2^36_to_2^37_hidden_classes"
    )


if __name__ == "__main__":
    main()

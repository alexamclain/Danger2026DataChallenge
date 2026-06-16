#!/usr/bin/env python3
"""Quantify ramified-factor/genus shortcuts for the p24 target fields.

For the target traces, the fundamental discriminants factor into only a few
prime discriminants.  Ramified ideals and genus characters are natural things
to try: they give canonical order-2 actions or quotients of the CM class set.

This audit is deliberately a model rather than a search.  It records the best
case if we could impose any chosen ramified-prime quotient at only linear
modular degree in that prime, then asks how many hidden CM classes remain.
Since the number of prime-discriminant factors is bounded here, even the
optimistic model saves only constant bits; imposing the huge cofactor costs far
more than sqrt(p) while still saving just one bit.
"""

from __future__ import annotations

import itertools
import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)
H_EST = {
    1020608380936: 2.786879e11,
    -78903246840: 8.329662e11,
    -1178414874616: 2.060276e11,
}


def prime_discriminant_factors(D: int) -> list[int]:
    factors: list[int] = []
    for q in sorted(sp.factorint(abs(D))):
        factors.append(q if q % 4 == 1 else -q)
    product = math.prod(factors)
    if product != D:
        raise AssertionError((D, factors, product))
    return factors


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 ramified-factor/genus tradeoff audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print()

    for t in TRACES:
        D = t * t - 4 * P24
        if D % 4 != 0:
            raise AssertionError(D)
        D_K = D // 4
        factors = prime_discriminant_factors(D_K)
        h = H_EST[t]
        print(f"trace={t}")
        print(f"  fundamental_D_K={D_K}")
        print(f"  prime_discriminants={factors}")
        print(f"  h_est={h:.6e}")
        print("  optimistic_ramified_quotients")
        print("    imposed_count max_abs_prime optimistic_degree residual_classes residual/sqrt")

        rows: list[tuple[float, int, int, int, float, float]] = []
        for r in range(len(factors) + 1):
            for subset in itertools.combinations(factors, r):
                max_abs_prime = max((abs(x) for x in subset), default=0)
                optimistic_degree = sum(abs(x) + 1 for x in subset)
                # Genus characters have one global product relation, so all
                # but one prime-discriminant quotient can be independent.
                independent_bits = min(r, max(0, len(factors) - 1))
                residual = h / (1 << independent_bits)
                score = max(optimistic_degree, residual)
                rows.append(
                    (
                        score,
                        r,
                        max_abs_prime,
                        optimistic_degree,
                        residual,
                        residual / sqrt_p,
                    )
                )

        for _, r, max_abs_prime, degree, residual, residual_ratio in sorted(rows)[:8]:
            print(
                f"    {r:13d} {max_abs_prime:13d} {degree:17d} "
                f"{residual:16.6e} {residual_ratio:13.6e}"
            )
        print()

    print(
        "conclusion=ramified_prime_conditions_are_only_genus_quotients; "
        "for_p24_they_save_constant_bits_and_do_not_create_a_subsqrt_selector"
    )


if __name__ == "__main__":
    main()

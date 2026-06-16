#!/usr/bin/env python3
"""Audit small split-prime CM cycle shortcuts for the p24 target fields.

Ramified-prime self-loops and the split prime above 2 were already checked.
Another tempting class-group shortcut is a small split prime ell whose ideal
has modest order m in the target class group.  Then target CM roots lie on
cycles of ell-isogenies of length m, and one might hope to solve the small
cycle equations instead of computing a full class polynomial.

The norm lower bound is severe.  If an ell-ideal power is principal and
non-scalar, its generator has norm ell^m and

    4 ell^m = x^2 + |D| y^2,  y != 0,

so ell^m >= |D|/4.  A chain representation of the cycle has only m local
ell-isogeny steps, but the composite correspondence degree is ell^m; keeping
only the chain variables leaves about h(D)/m cycles to choose from.
"""

from __future__ import annotations

import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)
H_EST = {
    1020608380936: 2.786879e11,
    -78903246840: 8.329662e11,
    -1178414874616: 2.060276e11,
}


def squarefree_part(n: int) -> int:
    out = 1
    for q, exp in sp.factorint(abs(n)).items():
        if exp & 1:
            out *= int(q)
    return out


def fundamental_discriminant_from_trace(trace: int) -> int:
    delta = trace * trace - 4 * P24
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def min_relation_power(abs_D: int, ell: int) -> int:
    return math.ceil(math.log((abs_D + 3) // 4, ell))


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 small split-prime cycle barrier")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print("split_prime_bound=200")
    print()

    for trace in TRACES:
        D = fundamental_discriminant_from_trace(trace)
        h_est = H_EST[trace]
        rows: list[tuple[float, int, int, int, float, float]] = []
        for ell in sp.primerange(2, 201):
            if abs(D) % ell == 0:
                continue
            if sp.kronecker_symbol(D, ell) != 1:
                continue
            m = min_relation_power(abs(D), ell)
            relation_norm = ell**m
            cycle_count_est = h_est / m
            rows.append(
                (
                    relation_norm / sqrt_p,
                    ell,
                    m,
                    relation_norm,
                    relation_norm / sqrt_p,
                    cycle_count_est,
                )
            )

        print(f"trace={trace}")
        print(f"  fundamental_D={D}")
        print(f"  h_est={h_est:.6e}")
        print("  best_split_prime_cycles_by_composite_norm")
        print("    ell min_m ell^m/sqrt_p h_est/min_m")
        for _score, ell, m, _norm, norm_ratio, cycle_count in sorted(rows)[:10]:
            print(f"    {ell:3d} {m:5d} {norm_ratio:14.6e} {cycle_count:14.6e}")
        print()

    print(
        "conclusion=small_split_prime_cycles_either_have_composite_degree_far_above_"
        "sqrt_p_or_leave_sqrt_scale_many_cycles_without_a_seed_root"
    )


if __name__ == "__main__":
    main()

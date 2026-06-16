#!/usr/bin/env python3
"""Exact class-group structure audit for the p24 target CM fields.

The earlier CM notes used class-number estimates and genus data.  With PARI
available through cypari2, this script records exact class numbers and class
group decompositions.  This is aimed at the remaining odd-class-field tower
loophole: if a target class group were very smooth, perhaps one could build a
small-degree tower of class invariants and select a CM root without enumerating
all h roots.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Row:
    trace: int
    D_K: int
    h: int
    group: list[int]
    h_factorization: dict[int, int]
    largest_prime_factor: int


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(abs(n)).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_from_trace(trace: int) -> int:
    delta = trace * trace - 4 * P24
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def main() -> None:
    pari = Pari()
    sqrt_p = math.isqrt(P24)
    print("p24 exact target CM class-group structure audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print("backend=PARI/GP via cypari2")
    print()

    rows: list[Row] = []
    for trace in TRACES:
        D_K = fundamental_discriminant_from_trace(trace)
        data = pari.quadclassunit(D_K)
        h = int(data[0])
        group = [int(x) for x in list(data[1])]
        fac = {int(q): int(e) for q, e in sp.factorint(h).items()}
        largest_prime_factor = max(fac)
        rows.append(Row(trace, D_K, h, group, fac, largest_prime_factor))

    for row in rows:
        odd_part = row.h
        while odd_part % 2 == 0:
            odd_part //= 2
        print(f"trace={row.trace}")
        print(f"  fundamental_D_K={row.D_K}")
        print(f"  class_number={row.h}")
        print(f"  class_group_invariants={row.group}")
        print(f"  factor_class_number={row.h_factorization}")
        print(f"  odd_part={odd_part}")
        print(f"  largest_prime_factor={row.largest_prime_factor}")
        print(f"  largest_prime_factor_over_sqrt={row.largest_prime_factor / sqrt_p:.6e}")
        print(f"  largest_prime_factor_over_p_quarter={row.largest_prime_factor / (P24 ** 0.25):.6e}")
        if row.largest_prime_factor < sqrt_p:
            print("  largest_prime_factor_subsqrt=1")
        else:
            print("  largest_prime_factor_subsqrt=0")
        print()

    print(
        "conclusion=exact_class_groups_do_not_give_a_root_but_the_"
        "third_target_has_a_smoothish_odd_component_worth_separating_from_"
        "the_large_class_polynomial_obstruction"
    )


if __name__ == "__main__":
    main()

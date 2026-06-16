#!/usr/bin/env python3
"""Audit split-prime cycle quotients across all strict p24 CM targets.

Most of the recent work focused on the smooth third target

    h = 2 * 157 * 211 * 3107441.

The other strict traces have less smooth class numbers, but their largest
prime factors are still below sqrt(p).  This script checks whether they have
small-norm split-prime cycles with very small quotient degrees, which might be
better theorem targets even if the class group is not fully smooth.
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Target:
    trace: int
    D_K: int
    class_number: int
    group: tuple[int, ...]


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


def exact_targets() -> list[Target]:
    pari = Pari()
    targets: list[Target] = []
    for trace in TRACES:
        D_K = fundamental_discriminant_from_trace(trace)
        data = pari.quadclassunit(D_K)
        targets.append(
            Target(
                trace=trace,
                D_K=D_K,
                class_number=int(data[0]),
                group=tuple(int(x) for x in list(data[1])),
            )
        )
    return targets


def split_cycle_rows(target: Target, prime_bound: int) -> list[tuple[int, int, int]]:
    pari = Pari()
    factors = {int(q): int(e) for q, e in sp.factorint(target.class_number).items()}
    principal = pari.qfbred(pari(f"Qfb(1,1,{(1 - target.D_K) // 4})"))
    principal_text = str(principal)
    nucomp_l = int((abs(target.D_K) // 4) ** 0.25) + 1

    def is_principal(form) -> bool:
        return str(pari.qfbred(form)) == principal_text

    def form_order(form) -> int:
        order = target.class_number
        for q, e in factors.items():
            for _ in range(e):
                candidate = order // q
                if is_principal(pari.qfbnupow(form, candidate, nucomp_l)):
                    order = candidate
                else:
                    break
        return order

    rows: list[tuple[int, int, int]] = []
    for ell in sp.primerange(2, prime_bound + 1):
        if sp.kronecker_symbol(target.D_K, ell) != 1:
            continue
        order = form_order(pari.qfbprimeform(target.D_K, int(ell)))
        rows.append((int(ell), order, target.class_number // order))
    return rows


def x0_degree(ell: int) -> int:
    return ell + 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=5000)
    ap.add_argument("--show", type=int, default=12)
    args = ap.parse_args()

    sqrt_p = math.isqrt(P24)
    targets = exact_targets()
    print("p24 all-target split-cycle audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"prime_bound={args.prime_bound}")
    print()

    for target in targets:
        started = time.time()
        rows = split_cycle_rows(target, args.prime_bound)
        print(f"trace={target.trace}")
        print(f"  D_K={target.D_K}")
        print(f"  class_number={target.class_number}")
        print(f"  class_group={target.group}")
        print(f"  factor_class_number={sp.factorint(target.class_number)}")
        print(f"  split_primes_checked={len(rows)}")
        print(f"  elapsed_seconds={time.time() - started:.3f}")

        by_index = sorted(rows, key=lambda row: (row[2], row[0]))
        print("  smallest_cycle_counts")
        print("    ell order cycle_count seeded_walk_over_sqrt order_over_sqrt factors_order factors_count")
        for ell, order, index in by_index[: args.show]:
            print(
                f"    {ell:6d} {order:15d} {index:12d} "
                f"{x0_degree(ell) * order / sqrt_p:22.6e} "
                f"{order / sqrt_p:14.6e} {sp.factorint(order)} {sp.factorint(index)}"
            )

        by_seeded = sorted(rows, key=lambda row: x0_degree(row[0]) * row[1])
        print("  best_seeded_walk_proxy")
        print("    ell order cycle_count seeded_walk seeded_walk_over_sqrt")
        for ell, order, index in by_seeded[: args.show]:
            seeded = x0_degree(ell) * order
            print(
                f"    {ell:6d} {order:15d} {index:12d} "
                f"{seeded:18d} {seeded / sqrt_p:20.6e}"
            )
        print()

    print("interpretation")
    print("  small_cycle_count_does_not_construct_the_embedded_quotient_polynomial=1")
    print("  seeded_walk_proxy_assumes_a_target_cm_root_is_already_known=1")
    print("  audit_identifies_additional_formal_targets_for_the_period_selector=1")
    print("conclusion=reported_all_strict_trace_split_cycle_candidates")


if __name__ == "__main__":
    main()

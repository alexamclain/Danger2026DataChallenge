#!/usr/bin/env python3
"""Audit split-prime cycle quotients for the p24 smooth CM target.

The third strict p24 target has a cyclic class group.  A split prime ell whose
ideal class has order n partitions the CM roots into h/n horizontal ell-isogeny
cycles of length n.  Symmetric functions of whole cycles are embedded quotient
invariants in principle.

This script records the best observed small-norm cycle splits.  It does not
build the cycles modulo p; doing so would already require embedded CM vertices.
"""

from __future__ import annotations

import argparse
import math
import time

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014


def class_order_probe(prime_bound: int) -> list[tuple[int, int, int]]:
    pari = Pari()
    factors = {int(q): int(e) for q, e in sp.factorint(CLASS_NUMBER).items()}
    principal = pari.qfbred(pari(f"Qfb(1,1,{(1 - D_K) // 4})"))
    principal_text = str(principal)
    nucomp_l = int((abs(D_K) // 4) ** 0.25) + 1

    def is_principal(form) -> bool:
        return str(pari.qfbred(form)) == principal_text

    def form_order(form) -> int:
        order = CLASS_NUMBER
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
        if sp.kronecker_symbol(D_K, ell) != 1:
            continue
        order = form_order(pari.qfbprimeform(D_K, int(ell)))
        rows.append((int(ell), order, CLASS_NUMBER // order))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=250_000)
    args = ap.parse_args()

    started = time.time()
    rows = class_order_probe(args.prime_bound)
    sqrt_p = math.isqrt(P24)

    print("p24 split-prime cycle selector audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print(f"sqrt_floor_p={sqrt_p}")
    print(f"prime_bound={args.prime_bound}")
    print(f"split_primes_checked={len(rows)}")
    print(f"elapsed_seconds={time.time() - started:.3f}")
    print()

    best_by_max_degree: list[tuple[int, int, int, int]] = []
    best_by_seeded_walk: list[tuple[int, int, int, int]] = []
    for ell, order, index in rows:
        best_by_max_degree.append((max(order, index), ell, order, index))
        best_by_seeded_walk.append(((ell + 1) * order, ell, order, index))
    best_by_max_degree.sort()
    best_by_seeded_walk.sort()

    print("best_cycle_splits_by_largest_formal_degree")
    print("  ell class_order cycle_count max_degree max_over_sqrt seeded_walk_over_sqrt factor_order factor_count")
    for max_degree, ell, order, index in best_by_max_degree[:20]:
        seeded_walk = (ell + 1) * order
        print(
            f"  {ell:8d} {order:12d} {index:11d} {max_degree:10d} "
            f"{max_degree / sqrt_p:13.6e} {seeded_walk / sqrt_p:21.6e} "
            f"{sp.factorint(order)} {sp.factorint(index)}"
        )
    print()

    print("best_splits_by_seeded_walk_proxy")
    print("  ell class_order cycle_count seeded_walk_proxy seeded_walk_over_sqrt max_degree_over_sqrt")
    for seeded_walk, ell, order, index in best_by_seeded_walk[:12]:
        print(
            f"  {ell:8d} {order:12d} {index:11d} {seeded_walk:18d} "
            f"{seeded_walk / sqrt_p:21.6e} {max(order, index) / sqrt_p:20.6e}"
        )
    print()

    print("distinguished_observed_splits")
    for ell, order, index in rows:
        if ell in {2, 23, 677, 2897, 7349, 14057}:
            print(
                f"  ell={ell} order={order} index={index} "
                f"largest_formal_degree={max(order,index)}"
            )
    print()

    print("interpretation")
    print("  split_prime_cycles_give_embedded_quotients_after_vertices_exist=1")
    print("  best_seen_formal_cycle_split_is_ell_7349_index_422=1")
    print("  smaller_edge_degree_tradeoff_ell_677_index_314=1")
    print("  cheapest_seeded_walk_proxy_is_ell_2_but_sqrt_scale=1")
    print("  x0_ell_edge_relation_degrees_are_678_and_7350=1")
    print("  locating_one_target_cycle_without_a_seed_is_still_missing=1")
    print(
        "conclusion=split_prime_cycle_quotients_are_a_sharper_candidate_"
        "theorem_target_but_not_yet_a_root_selector"
    )


if __name__ == "__main__":
    main()

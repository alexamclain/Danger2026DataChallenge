#!/usr/bin/env python3
"""Probe small split-prime class actions for the smooth-ish p24 target field.

The exact class group audit shows that the target trace

    t = -1178414874616

has cyclic class group of order

    h = 2 * 157 * 211 * 3107441.

This script asks whether small split primes represent useful class group
generators or large subgroups.  This does not construct a CM root; it only
tests whether an explicit odd class-field tower could plausibly use low-degree
modular equations for its class actions.
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=50_000)
    args = ap.parse_args()

    pari = Pari()
    factors = {int(q): int(e) for q, e in sp.factorint(CLASS_NUMBER).items()}
    principal = pari.qfbred(pari(f"Qfb(1,1,{(1 - D_K) // 4})"))
    nucomp_L = int((abs(D_K) // 4) ** 0.25) + 1

    def is_principal(form) -> bool:
        return str(pari.qfbred(form)) == str(principal)

    def form_order(form) -> int:
        order = CLASS_NUMBER
        for q, e in factors.items():
            for _ in range(e):
                candidate = order // q
                if is_principal(pari.qfbnupow(form, candidate, nucomp_L)):
                    order = candidate
                else:
                    break
        return order

    started = time.time()
    best_by_index: dict[int, tuple[int, int]] = {}
    best_by_order: dict[int, tuple[int, int]] = {}
    split_count = 0
    for ell in sp.primerange(2, args.prime_bound + 1):
        if sp.kronecker_symbol(D_K, ell) != 1:
            continue
        split_count += 1
        form = pari.qfbprimeform(D_K, int(ell))
        order = form_order(form)
        index = CLASS_NUMBER // order
        best_by_index.setdefault(index, (int(ell), order))
        best_by_order.setdefault(order, (int(ell), index))

    print("p24 smooth class-tower small-prime action probe")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"factor_class_number={factors}")
    print(f"prime_bound={args.prime_bound}")
    print(f"split_primes_checked={split_count}")
    print(f"elapsed_seconds={time.time() - started:.3f}")
    print()

    print("smallest_split_prime_by_generated_subgroup_index")
    print("  index ell order factor_order")
    for index in sorted(best_by_index)[:20]:
        ell, order = best_by_index[index]
        print(f"  {index:8d} {ell:6d} {order:12d} {sp.factorint(order)}")
    print()

    print("smallest_observed_orders")
    print("  order ell index factor_order")
    for order in sorted(best_by_order)[:20]:
        ell, index = best_by_order[order]
        print(f"  {order:12d} {ell:6d} {index:8d} {sp.factorint(order)}")
    print(
        "conclusion=small_split_primes_generate_large_class_subgroups_but_"
        "still_need_an_explicit_class_field_root_selector"
    )


if __name__ == "__main__":
    main()

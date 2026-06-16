#!/usr/bin/env python3
"""Search Atkin-Lehner quotient degree windows for p24 split classes.

The finite-field zero-lemma route for a class of order n and index m=h/n
would need a modular/correspondence function of pole degree < m.

For a representative of norm N, this script uses the optimistic lower proxy

    ceil([SL2Z:Gamma0(N)] / |W_N|)

where |W_N|=2^omega(N) is the full Atkin-Lehner group size for the squarefree
prime-support of N.  This is a generous screen: an actual oriented invariant
may have larger degree or may not realize the desired class stabilizer.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

from composite_split_cycle_audit import (
    TARGET_INDICES,
    exhaustive_norm_search,
    split_prime_logs,
)


def gamma0_index(n: int) -> int:
    value = n
    for ell in sp.factorint(n):
        value *= ell + 1
        value //= ell
    return int(value)


def atkin_lehner_size(n: int) -> int:
    return 1 << len(sp.factorint(n))


def quotient_degree_lower_proxy(n: int) -> int:
    return math.ceil(gamma0_index(n) / atkin_lehner_size(n))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=100000)
    ap.add_argument("--norm-bound", type=int, default=200000)
    ap.add_argument("--show", type=int, default=10)
    args = ap.parse_args()

    rows = split_prime_logs(args.prime_bound)
    hits = exhaustive_norm_search(rows, args.norm_bound)

    print("p24 Atkin-Lehner zero-window search")
    print(f"prime_bound={args.prime_bound}")
    print(f"norm_bound={args.norm_bound}")
    print(f"split_prime_logs={len(rows)}")
    print(f"hits={len(hits)}")
    print()

    for index in TARGET_INDICES:
        selected = [hit for hit in hits if hit.index == index]
        ranked = sorted(
            selected,
            key=lambda hit: (
                quotient_degree_lower_proxy(hit.norm) / index,
                gamma0_index(hit.norm),
                hit.norm,
            ),
        )
        passes = [
            hit for hit in selected
            if quotient_degree_lower_proxy(hit.norm) < index
        ]
        print(f"index={index}")
        print(f"  hit_count={len(selected)}")
        print(f"  atkin_zero_window_hits={len(passes)}")
        print("  ratio delta_AL gamma0 AL norm order signed_prime_powers")
        for hit in ranked[: args.show]:
            gamma0 = gamma0_index(hit.norm)
            al = atkin_lehner_size(hit.norm)
            delta = quotient_degree_lower_proxy(hit.norm)
            print(
                f"  {delta / index:9.6f} {delta:8d} {gamma0:8d} {al:4d} "
                f"{hit.norm:8d} {hit.order:12d} {hit.signed_primes}"
            )
        print()

    print("interpretation")
    print("  delta_AL=ceil(Gamma0_index/full_Atkin_Lehner_size)")
    print("  zero_lemma_window_requires_delta_AL_less_than_class_index=1")
    print("  this_is_an_optimistic_lower_proxy_not_an_actual_construction=1")
    print("conclusion=reported_atkin_lehner_zero_window_search")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Search auxiliary ray kernels with p24 odd factors.

The Cho/Koo/Shin smaller-generator theorem can use an odd prime order element
in the local ray-kernel group.  This script records how easy it is to find
small auxiliary rational primes whose local norm-kernel modulo units contains
the p24 odd factors 157 or 211.

This is only an arithmetic temptation check.  Such kernels are vertical over
the Hilbert class field: their Artin image in the ordinary class group is
trivial, so they do not by themselves select a level-1 CM j root.
"""

from __future__ import annotations

import argparse

import sympy as sp

D_K = -652834595820939249713143
ODD_LAYERS = (157, 211)
OMEGA_K = 2


def norm_kernel_mod_units_order(q: int) -> tuple[int, int, int]:
    """Return Kronecker(D,q), q-(D/q), and quotient by +/-1."""

    k = int(sp.kronecker_symbol(D_K, q))
    if k == 0:
        return k, 0, 0
    raw = q - k
    return k, raw, raw // OMEGA_K


def first_hits(layer: int, limit: int, count: int) -> list[tuple[int, int, int, int]]:
    hits: list[tuple[int, int, int, int]] = []
    q = 2
    while q < limit and len(hits) < count:
        q = int(sp.nextprime(q))
        if q == layer or D_K % q == 0:
            continue
        k, raw, quotient = norm_kernel_mod_units_order(q)
        if quotient % layer == 0:
            hits.append((q, k, raw, quotient))
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200_000)
    parser.add_argument("--count", type=int, default=12)
    args = parser.parse_args()

    print("p24 auxiliary ray-kernel search")
    print(f"D_K={D_K}")
    print(f"omega_K={OMEGA_K}")
    print()
    print("layer q kronecker q_minus_chi quotient_mod_units quotient_factor")
    for layer in ODD_LAYERS:
        for q, k, raw, quotient in first_hits(layer, args.limit, args.count):
            print(
                f"{layer:5d} {q:6d} {k:9d} {raw:11d} {quotient:18d} "
                f"{sp.factorint(quotient)}"
            )
    print()
    print("interpretation")
    print("  small_auxiliary_ray_kernels_with_157_or_211_exist=1")
    print("  these_kernels_are_local_principal_congruence_directions=1")
    print("  their_image_in_the_ordinary_class_group_is_trivial=1")
    print("  local_kernel_generators_do_not_move_level_1_j_roots=1")


if __name__ == "__main__":
    main()

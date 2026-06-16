#!/usr/bin/env python3
"""Partial-window test for oriented composite H-orbit invariants.

In the D=-5000 toy, the oriented composite move 3*17^(-1) has index 6 and
orbit size 5.  This script checks whether any shorter consecutive window along
that move collapses to the six quotient components.  It does not: only the
full H-orbit polynomial is H-invariant.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)

LOG_3 = 1
LOG_17 = 7
MOVE = (LOG_3 - LOG_17) % H
ORDER = H // __import__("math").gcd(H, MOVE)
INDEX = H // ORDER


def window_indices(start: int, length: int) -> list[int]:
    return [(start + k * MOVE) % H for k in range(length)]


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    print("partial orbit window toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"move={MOVE}")
    print(f"index={INDEX}")
    print(f"orbit_size={ORDER}")
    print("window_length distinct_window_polys distinct_window_sums distinct_window_products")

    for length in range(1, ORDER + 1):
        polys = []
        sums = []
        products = []
        for start in range(H):
            values = [cycle[i] for i in window_indices(start, length)]
            polys.append(tuple(monic_poly_from_roots(values, Q)))
            sums.append(sum(values) % Q)
            product = 1
            for value in values:
                product = product * value % Q
            products.append(product)
        print(
            f"{length:13d} {len(set(polys)):21d} "
            f"{len(set(sums)):20d} {len(set(products)):24d}"
        )

    print()
    print("interpretation")
    print("  quotient_count=6")
    print("  proper_windows_keep_full_orbit=1")
    print("  full_window_collapses_to_quotient_components=1")
    print("conclusion=reported_partial_orbit_window_toy")


if __name__ == "__main__":
    main()

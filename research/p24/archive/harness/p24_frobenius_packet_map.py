#!/usr/bin/env python3
"""Frobenius packet map for the third p24 CM target.

For a cyclic group of order N, irreducible factors of T^N-1 over F_p are
grouped by character order d | N.  Characters of exact order d have packet
degree ord_d(p), with phi(d)/ord_d(p) packets.
"""

from __future__ import annotations

import sympy as sp

P = 10**24 + 7
QUOTIENT_M = 66254
SUBGROUP_N = 3107441
CLASS_H = 205880396014


def rows(n: int) -> list[tuple[int, int, int, int]]:
    out: list[tuple[int, int, int, int]] = []
    for d in sorted(sp.divisors(n)):
        if d == 1:
            degree = 1
            packets = 1
            phi = 1
        else:
            degree = int(sp.n_order(P % d, d))
            phi = int(sp.totient(d))
            packets = phi // degree
        out.append((int(d), int(degree), int(packets), int(phi)))
    return out


def print_table(name: str, n: int) -> None:
    data = rows(n)
    print(f"{name}={n}")
    print(f"factors={sp.factorint(n)}")
    print(f"packet_count={sum(packet_count for _d, _deg, packet_count, _phi in data)}")
    print("order degree packets phi")
    for order, degree, packet_count, phi in data:
        print(f"{order:12d} {degree:10d} {packet_count:8d} {phi:12d}")
    print()


def main() -> None:
    print("p24 third-trace Frobenius packet map")
    print(f"p={P}")
    print()
    print_table("quotient_m", QUOTIENT_M)
    print_table("subgroup_n", SUBGROUP_N)
    print_table("class_h", CLASS_H)
    print("interpretation")
    print("  quotient_factored_period_normality_needs_28_packets=1")
    print("  full_class_cycle_normality_needs_10156_packets=1")
    print("  arbitrary_additive_selector_still_needs_full_annihilator_or_min_weight=1")
    print("conclusion=reported_p24_frobenius_packet_map")


if __name__ == "__main__":
    main()

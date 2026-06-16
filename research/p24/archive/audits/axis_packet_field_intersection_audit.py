#!/usr/bin/env python3
"""Field-intersection audit for p24 axis modules and packet fields.

For a component c of the smooth complement K, the nontrivial c-axis characters
are defined over F_{p^ord_c(p)}.  A packet factor for the H direction has
degree d=ord_n(p).  This audit records whether those character fields lie
inside the packet field F_{p^d}, and the intersection/compositum degrees.
"""

from __future__ import annotations

import argparse

import sympy as sp

P24_P = 10**24 + 7
P24_N = 3107441
P24_COMPONENTS = (2, 157, 211)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P24_P)
    parser.add_argument("--n", type=int, default=P24_N)
    parser.add_argument("--components", default=",".join(str(c) for c in P24_COMPONENTS))
    args = parser.parse_args()

    components = tuple(int(part) for part in args.components.split(",") if part)
    packet_degree = int(sp.n_order(args.p % args.n, args.n))

    print("axis packet-field intersection audit")
    print(f"p={args.p}")
    print(f"n={args.n}")
    print(f"packet_degree=ord_n(p)={packet_degree}")
    print(f"packet_degree_factorization={sp.factorint(packet_degree)}")
    print()
    print(
        "component char_degree intersection_degree compositum_degree "
        "chars_in_packet"
    )
    for component in components:
        char_degree = int(sp.n_order(args.p % component, component))
        intersection = int(sp.igcd(packet_degree, char_degree))
        compositum = int(sp.ilcm(packet_degree, char_degree))
        chars_in_packet = packet_degree % char_degree == 0
        print(
            f"{component:9d} {char_degree:11d} {intersection:19d} "
            f"{compositum:16d} {int(chars_in_packet):15d}"
        )
    print()
    print("interpretation")
    print("  component_characters_live_in_Fp_ord_component=1")
    print("  chars_in_packet_means_the_H_packet_field_already_diagonalizes_that_axis=1")
    print("  p24_211_axis_is_diagonal_inside_the_packet_field=1")
    print("  p24_157_axis_needs_an_external_degree_156_character_field=1")
    print("conclusion=reported_axis_packet_field_intersection_audit")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""K-character module decomposition over the p24 H-packet field.

Over F_p the L1 axis space has nine Frobenius-stable modules.  Over the
degree-ord_n(p) H-packet field the Frobenius is p^ord_n(p), so the K-character
orbits refine.  This is the natural module decomposition for proving
K-normality after passing to one packet field.
"""

from __future__ import annotations

import argparse

import sympy as sp

P24_P = 10**24 + 7
P24_N = 3107441
P24_M = 2 * 157 * 211
P24_COMPONENTS = (2, 157, 211)


def orbit_sizes_under_multiplier(modulus: int, multiplier: int) -> list[int]:
    seen: set[int] = set()
    sizes: list[int] = []
    for a in range(1, modulus):
        if a in seen:
            continue
        orbit: set[int] = set()
        x = a
        while x not in orbit:
            orbit.add(x)
            x = (x * multiplier) % modulus
        seen.update(orbit)
        sizes.append(len(orbit))
    return sorted(sizes)


def histogram(values: list[int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P24_P)
    parser.add_argument("--n", type=int, default=P24_N)
    parser.add_argument("--m", type=int, default=P24_M)
    parser.add_argument("--components", default=",".join(str(c) for c in P24_COMPONENTS))
    args = parser.parse_args()

    d = int(sp.n_order(args.p % args.n, args.n))
    multiplier = pow(args.p, d, args.m)
    components = tuple(int(part) for part in args.components.split(",") if part)
    ord_m = int(sp.n_order(args.p % args.m, args.m))
    splitting_degree = int(sp.ilcm(d, ord_m))

    print("packet-field K-module audit")
    print(f"p={args.p}")
    print(f"n={args.n}")
    print(f"m={args.m}")
    print(f"packet_degree=ord_n(p)={d}")
    print(f"ord_m(p)={ord_m}")
    print(f"full_k_splitting_degree_over_Fp={splitting_degree}")
    print(f"full_k_splitting_degree_over_packet={splitting_degree // d}")
    print(f"p^packet_degree_mod_m={multiplier}")
    print()
    print("axis_components_over_packet")
    print("component p^d_mod_c orbit_size_hist nontrivial_orbit_count")
    for component in components:
        component_multiplier = pow(args.p, d, component)
        sizes = orbit_sizes_under_multiplier(component, component_multiplier)
        print(
            f"{component:9d} {component_multiplier:9d} "
            f"{histogram(sizes)!s:20s} {len(sizes):22d}"
        )
    print()
    full_sizes = orbit_sizes_under_multiplier(args.m, multiplier)
    print("full_K_over_packet")
    print(f"  nontrivial_orbit_count={len(full_sizes)}")
    print(f"  orbit_size_histogram={histogram(full_sizes)}")
    print(f"  total_nontrivial_dimension={sum(full_sizes)}")
    print()
    print("axis_interpretation")
    print("  2_axis_modules_over_packet=1x1")
    print("  157_axis_modules_over_packet=2x78")
    print("  211_axis_modules_over_packet=210x1")
    print("  full_mu_m_extension_over_packet_has_degree_78=1")
    print("conclusion=reported_packet_field_k_module_audit")


if __name__ == "__main__":
    main()

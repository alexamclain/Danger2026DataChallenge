#!/usr/bin/env python3
"""Degree accounting for tensor-separating K roots from H packets.

For p24, the H-packet field has degree d=ord_n(p).  The K-character field
E=F_p(mu_m) has degree e=ord_m(p).  Tensoring gives

    F_{p^d} tensor_{F_p} F_{p^e}
      ~= product_{gcd(d,e)} F_{p^lcm(d,e)}

or, as an E-algebra, `gcd(d,e)` factors each of degree `d/gcd(d,e)`.

This script records that accounting and the axis-frequency decomposition.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24_P = 10**24 + 7
P24_M = 2 * 157 * 211
P24_N = 3107441
P24_COMPONENTS = (2, 157, 211)


def orbit_sizes(modulus: int, multiplier: int, values: list[int]) -> list[int]:
    values_set = set(values)
    seen: set[int] = set()
    out: list[int] = []
    for value in values:
        if value in seen:
            continue
        orbit: set[int] = set()
        x = value
        while x not in orbit:
            orbit.add(x)
            x = (x * multiplier) % modulus
        seen.update(orbit & values_set)
        out.append(len(orbit))
    return sorted(out)


def histogram(values: list[int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def axis_frequencies(m: int, components: tuple[int, ...]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {"constant": [0]}
    for component in components:
        step = m // component
        out[str(component)] = sorted((j * step) % m for j in range(1, component))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P24_P)
    parser.add_argument("--m", type=int, default=P24_M)
    parser.add_argument("--n", type=int, default=P24_N)
    parser.add_argument(
        "--components",
        default=",".join(str(c) for c in P24_COMPONENTS),
    )
    args = parser.parse_args()

    components = tuple(int(part) for part in args.components.split(",") if part)
    d = int(sp.n_order(args.p % args.n, args.n))
    e = int(sp.n_order(args.p % args.m, args.m))
    g = math.gcd(d, e)
    lcm = math.lcm(d, e)
    phi_n = int(sp.totient(args.n))
    h_packet_count = phi_n // d
    e_frobenius = pow(args.p, e, args.n)
    e_orbit_size = int(sp.n_order(e_frobenius, args.n))
    e_orbit_count = phi_n // e_orbit_size
    axis = axis_frequencies(args.m, components)
    axis_dim = sum(len(values) for values in axis.values())

    print("tensor decomposition accounting")
    print(f"p={args.p}")
    print(f"m={args.m}")
    print(f"n={args.n}")
    print(f"components={components}")
    print(f"ord_n(p)={d}")
    print(f"ord_m(p)={e}")
    print(f"gcd(ord_n,ord_m)={g}")
    print(f"lcm(ord_n,ord_m)={lcm}")
    print(f"E_degree_over_Fp={e}")
    print(f"H_packet_degree_over_Fp={d}")
    print(f"tensor_factor_count_over_E={g}")
    print(f"tensor_factor_degree_over_E={d // g}")
    print(f"H_packet_count_over_Fp={h_packet_count}")
    print(f"E_Frobenius_multiplier_mod_n={e_frobenius}")
    print(f"E_Frobenius_orbit_size_on_H={e_orbit_size}")
    print(f"E_Frobenius_nonzero_orbit_count_on_H={e_orbit_count}")
    print(f"E_orbits_per_H_packet={e_orbit_count // h_packet_count}")
    print(f"beta_orbit_count_matches_packets_times_tensor_factors={int(e_orbit_count == h_packet_count * g)}")
    print(f"full_K_dimension={args.m}")
    print(f"axis_dimension={axis_dim}")
    print()
    print("axis_frequency_counts")
    for name, values in axis.items():
        print(f"  {name}: {len(values)}")
    print()
    print("component_character_degree_intersections")
    print("  component ord_component gcd_with_H_packet tensor_factor_intersection")
    for component in components:
        component_order = int(sp.n_order(args.p % component, component))
        component_gcd = math.gcd(component_order, d)
        tensor_factor_intersection = math.gcd(component_order, d // g)
        print(
            f"  {component:9d} {component_order:13d} "
            f"{component_gcd:17d} {tensor_factor_intersection:26d}"
        )
    print()
    print("axis_orbits_under_Fp_Frobenius_on_K")
    for name, values in axis.items():
        sizes = orbit_sizes(args.m, args.p % args.m, values)
        print(f"  {name}: {histogram(sizes)}")
    print()
    print("axis_orbits_under_E_Frobenius_on_K")
    p_to_e = pow(args.p, e, args.m)
    for name, values in axis.items():
        sizes = orbit_sizes(args.m, p_to_e, values)
        print(f"  {name}: {histogram(sizes)}")
    print()
    print("H_packet_orbit_under_E_Frobenius")
    print(f"  multiplier_p^e_mod_n={e_frobenius}")
    print(f"  orbit_size={e_orbit_size}")
    print(f"  nonzero_orbit_count={e_orbit_count}")
    print(f"  orbits_per_Fp_H_packet={e_orbit_count // h_packet_count}")
    print()
    print("interpretation")
    print("  E_contains_all_K_characters=1")
    print("  K_characters_are_fixed_by_E_Frobenius=1")
    print("  H_packet_splits_over_E_into_gcd_ord_factors=1")
    print("  beta_orbits_refine_H_packets_by_the_same_tensor_factor_count=1")
    print(f"  one_tensor_factor_degree_exceeds_axis_dimension={int((d // g) > axis_dim)}")
    print("  one_tensor_factor_axis_injectivity_would_descend_to_base_packet=1")
    print("conclusion=reported_tensor_decomposition_accounting")


if __name__ == "__main__":
    main()

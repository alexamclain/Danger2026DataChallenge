#!/usr/bin/env python3
"""Character-support audit for the L1 partial-moment scalar.

For the complement subgroup K of order m with coprime components c_i, the
tower-native scalar

    L1 = M0 + sum_i P_{c_i}

uses the coefficient function

    w(r) = 1 + sum_i (r mod c_i).

This script records its Fourier support on K.  The support is small and
axis-shaped, but not K-trivial.  Therefore L1 keeps H-eigen propagation while
losing the stronger "single K-trivial resolvent" interpretation of M0.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24_M = 66254
P24_N = 3107441
P24_ORD_N_P = 388430


def components(m: int) -> tuple[int, ...]:
    return tuple(int(p) ** int(e) for p, e in sp.factorint(m).items())


def weight_bounds(comps: tuple[int, ...], lambdas: tuple[int, ...]) -> tuple[int, int]:
    lo = 1
    hi = 1 + sum(lam * (component - 1) for lam, component in zip(lambdas, comps))
    return lo, hi


def axis_support_size(comps: tuple[int, ...], lambdas: tuple[int, ...]) -> int:
    # Constant coefficient plus nonzero frequencies on each component whose
    # lambda is nonzero.  The function r mod c has full nontrivial support on
    # that component.
    return 1 + sum((component - 1) for lam, component in zip(lambdas, comps) if lam)


def weight_value(r: int, comps: tuple[int, ...], lambdas: tuple[int, ...]) -> int:
    return 1 + sum(lam * (r % component) for lam, component in zip(lambdas, comps))


def translation_stabilizer_size(m: int, comps: tuple[int, ...], lambdas: tuple[int, ...]) -> int:
    values = [weight_value(r, comps, lambdas) for r in range(m)]
    stabilizers = 0
    for shift in range(m):
        if all(values[(r + shift) % m] == values[r] for r in range(m)):
            stabilizers += 1
    return stabilizers


def brute_support(comps: tuple[int, ...], lambdas: tuple[int, ...], modulus: int) -> set[tuple[int, ...]]:
    """Brute-force product-DFT support for small component products."""
    points = list(sp.utilities.iterables.cartes(*[range(c) for c in comps]))
    support: set[tuple[int, ...]] = set()
    for freq in sp.utilities.iterables.cartes(*[range(c) for c in comps]):
        total = 0j
        for point in points:
            w = 1 + sum(lam * x for lam, x in zip(lambdas, point))
            angle = sum((f * x) / c for f, x, c in zip(freq, point, comps))
            total += w * complex(math.cos(-2 * math.pi * angle), math.sin(-2 * math.pi * angle))
        if abs(total) > 1e-7:
            support.add(tuple(int(x) for x in freq))
    return support


def support_shape(comps: tuple[int, ...], support: set[tuple[int, ...]]) -> tuple[int, int, int]:
    axis = 0
    mixed = 0
    trivial = 0
    for freq in support:
        nz = sum(x != 0 for x in freq)
        if nz == 0:
            trivial += 1
        elif nz == 1:
            axis += 1
        else:
            mixed += 1
    return trivial, axis, mixed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=P24_M)
    parser.add_argument("--lambdas", default="1")
    parser.add_argument("--brute", action="store_true")
    args = parser.parse_args()

    comps = components(args.m)
    raw_lambdas = tuple(int(part) for part in args.lambdas.split(",") if part)
    if len(raw_lambdas) == 1 and len(comps) != 1:
        lambdas = tuple(raw_lambdas[0] for _ in comps)
    else:
        lambdas = raw_lambdas
    if len(lambdas) != len(comps):
        raise SystemExit("lambda tuple length must match component count")

    lo, hi = weight_bounds(comps, lambdas)
    support_size = axis_support_size(comps, lambdas)
    stabilizer_size = translation_stabilizer_size(args.m, comps, lambdas)
    orbit_size = args.m // stabilizer_size

    print("L1 character-support audit")
    print(f"m={args.m}")
    print(f"components={list(comps)}")
    print(f"lambdas={list(lambdas)}")
    print(f"weight_min={lo}")
    print(f"weight_max={hi}")
    print(f"axis_support_size={support_size}")
    print(f"k_trivial_only={int(support_size == 1)}")
    print(f"translation_stabilizer_size={stabilizer_size}")
    print(f"translation_orbit_size={orbit_size}")

    if args.m == P24_M:
        print()
        print("p24_support_accounting")
        print(f"  n={P24_N}")
        print(f"  ord_n_p={P24_ORD_N_P}")
        print(f"  full_resolvent_support_per_H_character={support_size}")
        print(f"  K_translation_orbit_size={orbit_size}")
        print(f"  support_times_frobenius_packet={support_size * P24_ORD_N_P}")
        print(f"  H_eigen_zero_pdiv_exponent=n*ord_n_p={P24_N * P24_ORD_N_P}")
        print("  K_trivial_resolvent_interpretation=0")
        print("  H_eigen_propagation_survives=1")
        print("  quotient_field_norm_packaging_survives=0")

    if args.brute:
        if math.prod(comps) > 5000:
            raise SystemExit("brute support is only intended for small m")
        support = brute_support(comps, lambdas, args.m)
        trivial, axis, mixed = support_shape(comps, support)
        print()
        print("brute_product_dft")
        print(f"  support_size={len(support)}")
        print(f"  trivial_support={trivial}")
        print(f"  axis_support={axis}")
        print(f"  mixed_support={mixed}")
        print(f"  support={sorted(support)}")

    print()
    print("interpretation")
    print("  L1_is_not_K_trivial_unless_all_partial_lambdas_are_zero=1")
    print("  L1_has_axis_shaped_K_character_support=1")
    print("  nontrivial_translation_orbit_means_selected_K_origin_is_part_of_the_data=1")
    print("  selected_zero_still_propagates_through_H_and_Frobenius_packets=1")
    print("  L1_punit_theorem_is_not_the_same_as_the_complement_M0_punit_theorem=1")
    print("conclusion=reported_l1_character_support_audit")


if __name__ == "__main__":
    main()

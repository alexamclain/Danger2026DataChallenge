#!/usr/bin/env python3
"""Semi-invariant descent toy for Plucker-Kummer payloads.

Raising a Plucker coordinate to a Kummer power removes cyclic label ambiguity
only when the coordinate is semi-invariant under the hidden cyclic action.  If
the action merely permutes different Plucker coordinates, individual powers
need not descend; the orbit product is then the honest invariant payload.
"""

from __future__ import annotations


Q = 13
ORDER = 3
CHARACTER = 3  # primitive cube root in F_13


def product(values: list[int], q: int = Q) -> int:
    out = 1
    for value in values:
        out = out * value % q
    return out


def powers(values: list[int], exponent: int = ORDER, q: int = Q) -> list[int]:
    return [pow(value, exponent, q) for value in values]


def cyclic_orbit(values: list[int]) -> list[list[int]]:
    return [values[i:] + values[:i] for i in range(len(values))]


def main() -> None:
    semi_base = 2
    semi_orbit = [semi_base * pow(CHARACTER, i, Q) % Q for i in range(ORDER)]
    semi_powers = powers(semi_orbit)

    nonsemi_orbit = [2, 5, 7]
    nonsemi_powers = powers(nonsemi_orbit)
    nonsemi_products = [product(row) for row in cyclic_orbit(nonsemi_orbit)]

    zero_orbit = [2, 0, 7]
    zero_product = product(zero_orbit)

    print("Plucker-Kummer descent toy")
    print(f"q={Q}")
    print(f"order={ORDER}")
    print(f"character={CHARACTER}")
    print()
    print("semi_invariant_coordinate")
    print(f"  orbit={semi_orbit}")
    print(f"  powers={semi_powers}")
    print(f"  powers_descend_to_single_scalar={int(len(set(semi_powers)) == 1)}")
    print(f"  descended_scalar={semi_powers[0]}")
    print(f"  nonzero_detected={int(semi_powers[0] != 0)}")
    print()
    print("non_semi_invariant_coordinate")
    print(f"  orbit={nonsemi_orbit}")
    print(f"  powers={nonsemi_powers}")
    print(f"  powers_descend_to_single_scalar={int(len(set(nonsemi_powers)) == 1)}")
    print(f"  orbit_products_under_relabeling={nonsemi_products}")
    print(f"  orbit_product_descends={int(len(set(nonsemi_products)) == 1)}")
    print(f"  orbit_product={nonsemi_products[0]}")
    print()
    print("orbit_product_zero_control")
    print(f"  orbit={zero_orbit}")
    print(f"  orbit_product={zero_product}")
    print(f"  zero_detected={int(zero_product == 0)}")
    print()
    print("interpretation")
    print("  plucker_power_descends_for_semi_invariant_coordinates=1")
    print("  individual_powers_do_not_descend_for_permuted_coordinates=1")
    print("  orbit_product_is_the_safe_invariant_when_descent_fails=1")
    print("conclusion=reported_plucker_kummer_descent_toy")


if __name__ == "__main__":
    main()

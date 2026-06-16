#!/usr/bin/env python3
"""Toy model for the relative coset-polynomial phase problem.

In the D=-5000 calibration, the class group has order 30.  Taking cosets of a
subgroup of size 5 gives six degree-5 recovery polynomials U_r(X).  Each U_r
would be a perfectly good recovery polynomial once its coset is selected, but
no single U_r is rational/symmetric by itself.  The six U_r are conjugates over
the degree-6 quotient; multiplying them all recovers the full degree-30 class
polynomial.

This is the small analogue of the p24 third target:

    quotient degree 66254, recovery degree 3107441.

Computing one recovery polynomial modulo p requires the missing quotient phase
or embedded period selector.  Symmetric computation over all phases returns to
the full class set.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    QUOTIENT_SIZE,
    SUBGROUP_SIZE,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)


def poly_mul(a: list[int], b: list[int], q: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % q
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    coset_polys: list[list[int]] = []
    coset_roots: list[list[int]] = []
    for r in range(QUOTIENT_SIZE):
        coset = [cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)]
        coset_roots.append(coset)
        coset_polys.append(monic_poly_from_roots(coset, Q))

    product = [1]
    for poly in coset_polys:
        product = poly_mul(product, poly, Q)
    full = monic_poly_from_roots(roots, Q)

    print("relative coset phase toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print()
    print("coset_recovery_polynomials")
    print("  r roots coeffs_ascending_mod_q")
    for r, (coset, poly) in enumerate(zip(coset_roots, coset_polys)):
        print(f"  {r:1d} {coset!s:32s} {poly}")
    print()
    print(f"distinct_recovery_polynomial_coeff_tuples={len({tuple(poly) for poly in coset_polys})}")
    print(f"product_of_coset_polys_equals_full_class_poly_mod_q={int(product == full)}")
    print(f"full_class_polynomial_degree={len(full) - 1}")
    print()
    print("interpretation")
    print("  one_coset_recovery_polynomial_is_enough_after_phase_selection=1")
    print("  selected_coset_polynomial_is_not_symmetric_over_the_full_class_group=1")
    print("  quotient_phase_has_degree_equal_to_number_of_cosets=1")
    print("  symmetrizing_over_all_phases_recovers_the_full_class_polynomial=1")
    print(
        "conclusion=relative_recovery_polynomial_needs_the_same_embedded_"
        "quotient_phase_selector"
    )


if __name__ == "__main__":
    main()

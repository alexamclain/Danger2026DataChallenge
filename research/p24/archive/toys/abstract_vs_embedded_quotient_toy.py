#!/usr/bin/env python3
"""Toy comparison: abstract class-field quotient vs embedded period quotient.

For the tiny maximal-order case D=-87, PARI can write down the abstract
degree-2 unramified quotient:

    bnrclassfield(bnr, 2, 1) = x^2 + 3.

Over F_103 the same CM roots also have an embedded split-cycle quotient from
the horizontal ell=7 cycles:

    (Y - 29) (Y - 4).

Both quadratic algebras split over F_103, as they should because p splits
completely in the Hilbert class field.  But the abstract roots {10,93} are
not attached to the embedded cycle sums {4,29} until one supplies a relation
between the class-field generator and the CM j coordinate.  There are two
affine pairings in this degree-2 toy; the class-field polynomial alone does
not choose one.
"""

from __future__ import annotations

from cypari2 import Pari

from seedless_cycle_elimination_toy import D, ELL, Q, expected_cycle_sums


def roots_of_x2_plus_3(q: int) -> list[int]:
    return sorted(x for x in range(q) if (x * x + 3) % q == 0)


def affine_map(pair_a: tuple[int, int], pair_y: tuple[int, int], q: int) -> tuple[int, int]:
    a0, a1 = pair_a
    y0, y1 = pair_y
    slope = (y1 - y0) * pow(a1 - a0, -1, q) % q
    intercept = (y0 - slope * a0) % q
    return slope, intercept


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    c = (1 - D) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")
    abstract_poly = pari("bnrclassfield(bnr,2,1)")

    abstract_roots = roots_of_x2_plus_3(Q)
    embedded_roots = expected_cycle_sums()
    pairings = [
        affine_map((abstract_roots[0], abstract_roots[1]), (embedded_roots[0], embedded_roots[1]), Q),
        affine_map((abstract_roots[0], abstract_roots[1]), (embedded_roots[1], embedded_roots[0]), Q),
    ]

    print("abstract vs embedded quotient toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"split_cycle_ell={ELL}")
    print(f"abstract_bnrclassfield_degree_2={abstract_poly}")
    print(f"abstract_quotient_roots_mod_q={abstract_roots}")
    print(f"embedded_cycle_sum_roots_mod_q={embedded_roots}")
    print(f"possible_affine_pairings_alpha_to_Y={pairings}")
    print()
    print("interpretation")
    print("  abstract_quotient_field_splits_mod_q=1")
    print("  embedded_period_quotient_splits_mod_q=1")
    print("  quotient_roots_are_unpaired_without_a_relation_to_j=1")
    print("  degree_two_has_only_two_pairings_but_p24_has_314_or_422_roots=1")
    print(
        "conclusion=bnrclassfield_existence_does_not_select_an_embedded_"
        "CM_cycle_or_recovery_factor_without_an_explicit_relation_to_j"
    )


if __name__ == "__main__":
    main()

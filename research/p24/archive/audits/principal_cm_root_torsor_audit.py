#!/usr/bin/env python3
"""Toy audit for the "principal CM root" selector trap.

For a large target discriminant it is tempting to say: do not compute all
roots, just reduce the principal CM singular modulus j(tau_O) modulo p.  The
problem is that reducing this algebraic number modulo a prime that splits
completely in the class field requires choosing one of the primes above p.
That choice is equivalent to choosing a root of the class polynomial.

This script makes the point in the small D=-5000 calibration already used in
`embedded_decomposition_calibration.py`.  The class group has 30 elements and
H_D splits over q=1259.  The horizontal 3-isogeny graph is a 30-cycle.  Any
chosen root can be declared the principal class after choosing an isomorphism
from the abstract class group to the embedded root torsor; Frobenius is trivial
and fixes every root, so it does not pick a distinguished one.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    rotations = len(cycle)
    orientations = 2
    possible_labelings = rotations * orientations

    print("principal CM root torsor audit")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_norm={ELL}")
    print(f"split_roots_over_Fq={len(roots)}")
    print(f"horizontal_cycle_length={len(cycle)}")
    print(f"frobenius_action_on_roots=identity")
    print(f"frobenius_fixed_roots={len(roots)}")
    print(f"possible_principal_root_choices={rotations}")
    print(f"possible_cycle_labelings_with_orientation={possible_labelings}")
    print()
    print("example")
    print(f"  first_cycle_root={cycle[0]}")
    print(f"  second_cycle_root={cycle[1]}")
    print("  Either can be labeled as the principal class after rotating the")
    print("  abstract class-group coordinate.  The finite-field root set and")
    print("  Frobenius identity action do not distinguish the labels.")
    print()
    print("p24_analogy")
    print("  p24_target_h=205880396014")
    print("  principal_norm_representation_says_splitting=1")
    print("  roots_fixed_by_frobenius=all_target_roots")
    print("  principal_root_selector_from_splitting_data=0")
    print(
        "conclusion=principal_CM_root_reduction_requires_the_same_class_field_"
        "embedding_choice_as_selecting_a_root"
    )


if __name__ == "__main__":
    main()

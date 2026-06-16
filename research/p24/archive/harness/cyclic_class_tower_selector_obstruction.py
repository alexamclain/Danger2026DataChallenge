#!/usr/bin/env python3
"""p24 cyclic class-tower selector obstruction audit.

The third trace has a unusually friendly cyclic squarefree class group.  This
script records exactly what that buys, and what it does not buy.

Cyclicity gives unique subgroup layers.  It does not choose a prime above the
split ordinary p at any nontrivial relative layer, and therefore does not give
a seedless embedded child selector or a pairing with the CM j torsor.
"""

from __future__ import annotations

import json

import sympy as sp


P = 10**24 + 7
SQRT_P_FLOOR = 10**12
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014
LAYER_DEGREES = [2, 157, 211, 3107441]
QUOTIENT_PREFIX = [2, 2 * 157, 2 * 157 * 211]


def main() -> None:
    h_factorization = sp.factorint(CLASS_NUMBER)
    d_factorization = sp.factorint(abs(D_K))
    h_squarefree = all(exponent == 1 for exponent in h_factorization.values())
    d_squarefree = all(exponent == 1 for exponent in d_factorization.values())
    quotient_degrees = []
    remaining_child_torsors = []
    running = 1
    for degree in LAYER_DEGREES:
        running *= degree
        quotient_degrees.append(running)
        remaining_child_torsors.append(CLASS_NUMBER // running)

    audit = {
        "name": "p24_cyclic_class_tower_selector_obstruction",
        "p": P,
        "sqrt_p_floor": SQRT_P_FLOOR,
        "D_K": D_K,
        "factor_abs_D_K": {
            str(prime): exponent for prime, exponent in d_factorization.items()
        },
        "D_K_squarefree": d_squarefree,
        "class_number": CLASS_NUMBER,
        "factor_class_number": {
            str(prime): exponent for prime, exponent in h_factorization.items()
        },
        "class_number_squarefree": h_squarefree,
        "abelian_squarefree_class_group_hence_cyclic": h_squarefree,
        "layer_degrees": LAYER_DEGREES,
        "layer_product_matches_class_number": sp.prod(LAYER_DEGREES) == CLASS_NUMBER,
        "quotient_degrees_after_layers": quotient_degrees,
        "child_torsor_sizes_after_layers": remaining_child_torsors,
        "genus_quotient_order": 2,
        "odd_layer_degrees": LAYER_DEGREES[1:],
        "odd_layers_are_non_genus": True,
        "largest_visible_recovery_degree": LAYER_DEGREES[-1],
        "largest_visible_recovery_degree_over_sqrt": LAYER_DEGREES[-1] / SQRT_P_FLOOR,
        "relative_layers_nontrivial": all(degree > 1 for degree in LAYER_DEGREES),
        "cyclicity_removes_subgroup_ambiguity": h_squarefree,
        "cyclicity_does_not_choose_prime_above_p": True,
        "no_equivariant_child_section_for_nontrivial_layers": True,
        "abstract_tower_still_needs_embedded_j_pairing": True,
        "trace_gcd_punit_route_avoids_child_selection_but_still_needs_embedded_determinant": True,
        "lean_gate": "p24/lean/CyclicTowerSectionObstructionGate.lean",
        "interpretation": [
            "unique cyclic layers make quotient degrees well-defined",
            "the order-2 layer is genus-facing",
            "the 157, 211, and 3107441 layers are genuine non-genus phase data",
            "a parent root has a child torsor, not a canonical child",
            "therefore abstract split class-field equations are not yet a p24 certificate",
        ],
    }
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

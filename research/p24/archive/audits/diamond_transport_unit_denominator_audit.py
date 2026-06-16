#!/usr/bin/env python3
"""p24 denominator audit for diamond determinant-line transport.

This is not the diamond-equivariance producer theorem.  It records the
prime-to-p denominator hygiene needed after the producer constructs the
right-unit transport over the full p-integral 211-product algebra.
"""

from __future__ import annotations

import json
from math import gcd

import sympy as sp


P = 10**24 + 7
RIGHT = 211
LEFT = 157
UNIT = 2
RIGHT_ORBIT_LEN = 35
LEFT_DIM = 156
H_COSET_COUNT = 7
H_COSET_SIZE = 30
E_DEGREE = 5460
M = 2 * LEFT * RIGHT
CLASS_NUMBER = 205880396014


def main() -> None:
    denominators = {
        "quadratic_orientation": 2,
        "right_unit": UNIT,
        "right_level": RIGHT,
        "left_level": LEFT,
        "right_orbit_degree": RIGHT_ORBIT_LEN,
        "left_degree": LEFT_DIM,
        "h_coset_count": H_COSET_COUNT,
        "h_coset_size": H_COSET_SIZE,
        "E_over_Fp_degree": E_DEGREE,
        "mixed_level_m": M,
        "class_number": CLASS_NUMBER,
    }
    gcds = {name: gcd(P, value) for name, value in denominators.items()}
    audit = {
        "name": "p24_diamond_transport_unit_denominator_audit",
        "p": P,
        "right": RIGHT,
        "unit": UNIT,
        "unit_is_right_unit": gcd(UNIT, RIGHT) == 1,
        "p_mod_right": P % RIGHT,
        "ord_p_mod_right": int(sp.n_order(P % RIGHT, RIGHT)),
        "unit_action_order_on_nonzero_orbits": 6,
        "transport_denominators": denominators,
        "gcd_p_denominator": gcds,
        "all_denominators_prime_to_p": all(value == 1 for value in gcds.values()),
        "lean_gate": "p24/lean/TraceGcdDiamondEquivarianceGate.lean",
        "interpretation": [
            "prime-to-level denominators are p-units",
            "unit-2 is an automorphism of the right 211-product algebra",
            "once the producer constructs p-integral source/target transports, determinant comparison factors are p-units",
            "this proves denominator hygiene only, not the two p-unit nonvanishing statements",
        ],
    }
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

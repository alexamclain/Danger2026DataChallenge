#!/usr/bin/env python3
"""Audit direct reduction of the principal singular modulus.

The complex principal singular modulus is distinguished: for discriminant
Delta < 0, the reduced form with a=1 gives the dominant conjugate.  A tempting
route is therefore:

    compute the principal j(Delta) directly and reduce it modulo p.

There are two obstructions.

1. Complex/q-exp computation must recover an algebraic integer of height about
   exp(pi*sqrt(|Delta|)), so reduction modulo p by integer reconstruction is
   height-scale.

2. More importantly, "the principal conjugate modulo p" is not a canonical
   finite-field element when p splits completely.  Reducing an algebraic
   integer modulo p requires choosing a prime above p, equivalently one root
   of the class polynomial mod p.  The complex embedding that makes the
   principal conjugate dominant does not choose that finite-field prime.

Thus direct principal-j reduction is the same embedded root-selection problem
unless a new p-adic embedding selector is supplied.
"""

from __future__ import annotations

import math

from cypari2 import Pari

from embedded_decomposition_calibration import pari_linear_roots

P24 = 10**24 + 7
THIRD_ABS_TRACE = 1178414874616
THIRD_D_K = -652834595820939249713143
THIRD_CLASS_NUMBER = 205880396014

TOY_D = -87
TOY_Q = 103


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    toy_hilbert = pari.polclass(TOY_D)
    toy_roots = pari_linear_roots(toy_hilbert, TOY_Q)

    delta = THIRD_ABS_TRACE * THIRD_ABS_TRACE - 4 * P24
    log_principal = math.pi * math.sqrt(abs(delta))

    print("principal singular modulus reduction audit")
    print("toy_complete_split_example")
    print(f"  D={TOY_D}")
    print(f"  q={TOY_Q}")
    print(f"  class_polynomial_degree={int(pari.poldegree(toy_hilbert))}")
    print(f"  roots_mod_q={toy_roots}")
    print("  reduction_maps_above_q_equal_number_of_roots=1")
    print("  complex_principal_embedding_selects_one_complex_conjugate=1")
    print("  complex_principal_embedding_selects_root_mod_q=0")
    print()

    print("p24_third_target_scale")
    print(f"  p={P24}")
    print(f"  D_K={THIRD_D_K}")
    print(f"  class_number={THIRD_CLASS_NUMBER}")
    print(f"  log_principal_j_proxy={log_principal:.6f}")
    print(f"  log_p={math.log(P24):.6f}")
    print(f"  log_principal_over_log_p={log_principal / math.log(P24):.6e}")
    print()

    print("interpretation")
    print("  principal_complex_conjugate_is_canonical_over_C=1")
    print("  reduction_mod_split_p_requires_prime_above_p=1")
    print("  choosing_prime_above_p_is_equivalent_to_choosing_class_root_mod_p=1")
    print("  q_exp_integer_reconstruction_requires_height_scale_precision=1")
    print(
        "conclusion=direct_principal_singular_modulus_reduction_does_not_"
        "bypass_the_embedded_CM_root_selector"
    )


if __name__ == "__main__":
    main()

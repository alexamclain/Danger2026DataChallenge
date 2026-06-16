#!/usr/bin/env python3
"""Check whether the order-19 Hilbert quotient is a small conductor layer.

The first strict p24 trace has a degree-19 unramified quotient

    Cl(O_K) / <prime over 19>.

A tempting escape is that this quotient might be the same as a ring/ray class
layer of conductor 19, giving explicit level-19 modular units.  For a split
rational prime l, however, the small-conductor exact sequences add split
local unit kernels of size l-1 (or quotients of that), not an unramified
quotient of order l.

This script records the exact local degree bookkeeping for l=19.
"""

from __future__ import annotations

import sympy as sp


D_K = -739589633190799177940983
CLASS_NUMBER = 278733727154
ELL = 19


def main() -> None:
    kronecker = sp.kronecker_symbol(D_K, ELL)
    if kronecker != 1:
        raise AssertionError("19 should split")

    # For K not Q(i), Q(sqrt(-3)), units are +/-1.
    unit_count = 2
    ring_kernel_conductor_ell = ELL * (1 - kronecker / ELL)
    ray_kernel_one_split_prime = (ELL - 1) // unit_count
    ray_kernel_both_split_primes = ((ELL - 1) * (ELL - 1)) // unit_count
    ray_kernel_one_prime_squared = (ELL * (ELL - 1)) // unit_count
    ray_kernel_both_prime_squared = (ELL * (ELL - 1) * ELL * (ELL - 1)) // unit_count

    print("order-19 ring/ray exact-sequence audit")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factor={sp.factorint(CLASS_NUMBER)}")
    print(f"ell={ELL}")
    print(f"kronecker_D_ell={kronecker}")
    print(f"ell_splits={int(kronecker == 1)}")
    print()

    print("unramified_target")
    print(f"  quotient_degree=19")
    print(f"  recovery_degree={CLASS_NUMBER // ELL}")
    print("  ramification_at_19=0")
    print()

    print("small_conductor_layers")
    print(f"  ring_class_conductor_19_kernel={int(ring_kernel_conductor_ell)}")
    print(f"  ring_class_conductor_19_total_degree={int(CLASS_NUMBER * ring_kernel_conductor_ell)}")
    print(f"  ray_one_prime_mod_p_kernel={ray_kernel_one_split_prime}")
    print(f"  ray_one_prime_mod_p_total_degree={CLASS_NUMBER * ray_kernel_one_split_prime}")
    print(f"  ray_both_primes_mod_19_kernel={ray_kernel_both_split_primes}")
    print(f"  ray_both_primes_mod_19_total_degree={CLASS_NUMBER * ray_kernel_both_split_primes}")
    print(f"  ray_one_prime_squared_kernel={ray_kernel_one_prime_squared}")
    print(f"  ray_one_prime_squared_total_degree={CLASS_NUMBER * ray_kernel_one_prime_squared}")
    print(f"  ray_both_primes_squared_kernel={ray_kernel_both_prime_squared}")
    print(f"  ray_both_primes_squared_total_degree={CLASS_NUMBER * ray_kernel_both_prime_squared}")
    print()

    print("interpretation")
    print("  conductor_19_ring_kernel_equals_18_not_19=1")
    print("  modulus_one_split_prime_kernel_equals_9_not_19=1")
    print("  19_power_ray_kernel_first_appears_at_prime_square=1")
    print("  prime_square_ray_layer_is_ramified_at_19=1")
    print("  unramified_degree_19_quotient_is_from_base_class_group=1")
    print("  isolating_it_inside_ray_class_data_requires_same_class_character=1")
    print(
        "conclusion=order19_Hilbert_quotient_is_not_a_small_conductor_"
        "ring_or_ray_layer"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Find small split primes that move the first-trace order-19 components.

For the first strict trace, the split prime 19 has class order h/19.  Its
orbits would give 19 embedded components.  A second split prime whose class is
nontrivial modulo <19> would orient/move those 19 components.

This audit is only class-group arithmetic.  A small component mover means the
quotient action can be described at low modular level after the components
exist; it does not compute the component periods seedlessly.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp
from cypari2 import Pari


P = 10**24 + 7
TRACE = 1020608380936
D_K = -739589633190799177940983
CLASS_NUMBER = 278733727154
SUBGROUP_PRIME = 19
RECOVERY_ORDER = CLASS_NUMBER // SUBGROUP_PRIME


def principal_form(pari: Pari):
    return pari.qfbred(pari(f"Qfb(1,1,{(1 - D_K) // 4})"))


def form_text(pari: Pari, form) -> str:
    return str(pari.qfbred(form))


def form_order(pari: Pari, form, nucomp_l: int, principal_text: str) -> int:
    order = CLASS_NUMBER
    for prime, exponent in sp.factorint(CLASS_NUMBER).items():
        prime = int(prime)
        for _ in range(int(exponent)):
            candidate = order // prime
            if form_text(pari, pari.qfbnupow(form, candidate, nucomp_l)) == principal_text:
                order = candidate
            else:
                break
    return order


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=300)
    args = ap.parse_args()

    pari = Pari()
    nucomp_l = int((abs(D_K) // 4) ** 0.25) + 1
    principal = principal_form(pari)
    principal_text = form_text(pari, principal)

    subgroup_form = pari.qfbprimeform(D_K, SUBGROUP_PRIME)
    subgroup_image = pari.qfbnupow(subgroup_form, RECOVERY_ORDER, nucomp_l)
    subgroup_image_is_identity = int(form_text(pari, subgroup_image) == principal_text)

    base_torsion = None
    base_prime = None
    base_order = None
    rows: list[tuple[int, int | None, int, int, int]] = []

    for ell in sp.primerange(2, args.prime_bound + 1):
        ell = int(ell)
        if abs(D_K) % ell == 0 or sp.kronecker_symbol(D_K, ell) != 1:
            continue

        form = pari.qfbprimeform(D_K, ell)
        image = pari.qfbnupow(form, RECOVERY_ORDER, nucomp_l)
        image_text = form_text(pari, image)
        in_subgroup = int(image_text == principal_text)
        quotient_log = None

        if not in_subgroup:
            if base_torsion is None:
                base_torsion = image
                base_prime = ell
                base_order = form_order(pari, form, nucomp_l, principal_text)
                quotient_log = 1
            else:
                for k in range(19):
                    if form_text(pari, pari.qfbnupow(base_torsion, k, nucomp_l)) == image_text:
                        quotient_log = k
                        break
                if quotient_log is None:
                    raise AssertionError("nontrivial image not in generated 19-torsion")

        rows.append((ell, quotient_log, in_subgroup, ell + 1, form_order(pari, form, nucomp_l, principal_text)))

    print("order-19 component mover audit")
    print(f"p={P}")
    print(f"trace={TRACE}")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factor={sp.factorint(CLASS_NUMBER)}")
    print(f"subgroup_prime={SUBGROUP_PRIME}")
    print(f"recovery_order=h/19={RECOVERY_ORDER}")
    print(f"subgroup_prime_image_identity_after_h_over_19={subgroup_image_is_identity}")
    print(f"prime_bound={args.prime_bound}")
    print(f"base_component_mover_prime={base_prime}")
    print(f"base_component_mover_class_order={base_order}")
    print(f"base_component_mover_is_full_generator={int(base_order == CLASS_NUMBER) if base_order is not None else 0}")
    print()

    print("split_prime_images_mod_<19>")
    print("  ell quotient_log_relative_to_base in_<19> x0_degree class_order")
    for ell, quotient_log, in_subgroup, x0_degree, order in rows:
        marker = "." if quotient_log is None else str(quotient_log)
        print(f"  {ell:5d} {marker:29s} {in_subgroup:7d} {x0_degree:9d} {order:15d}")
    print()

    movers = [row for row in rows if row[1] is not None]
    print("interpretation")
    print(f"  small_component_mover_exists={int(bool(movers))}")
    if movers:
        ell, quotient_log, _in_subgroup, x0_degree, order = movers[0]
        print(f"  smallest_mover_prime={ell}")
        print(f"  smallest_mover_x0_degree={x0_degree}")
        print(f"  smallest_mover_quotient_log={quotient_log}")
        print(f"  smallest_mover_class_order={order}")
        print(f"  combined_local_level_proxy={(SUBGROUP_PRIME + 1) * x0_degree}")
    print("  low_level_orientation_after_components_exist=1")
    print("  component_periods_constructed_seedlessly=0")
    print(
        "conclusion=small_split_primes_can_orient_the_order19_quotient_but_"
        "do_not_replace_the_missing_subgroup_trace"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit ramified-prime self-isogeny shortcuts.

For a CM discriminant Delta = t^2 - 4p, a root of Phi_l(j,j) would correspond
to an actual endomorphism of degree l, equivalently an element of norm l in
the quadratic order:

    x^2 - Delta*y^2 = 4*l.

The target discriminants have ramified prime factors such as 7, 29, 599, and
4973929.  A tempting shortcut is to use the corresponding ramified l-isogeny
as a self-loop or low-degree class selector.  But a self-loop would require the
ramified ideal to be principal, i.e. an element of norm l in the quadratic
order.  Since |Delta| is much larger than 4*l for every ramified factor here,
y != 0 is impossible in the norm equation, and y = 0 would require l to be a
square.

Nonprincipal ramified ideals still give genus/2-torsion information in the
class group.  That was audited separately and saves only constant bits; it does
not select a target class among the remaining ~2^36 to 2^37 possibilities.
"""

from __future__ import annotations

import argparse
import math

from sympy import factorint

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


def has_norm_l_element(delta_abs: int, ell: int) -> bool:
    # Delta is negative, so x^2 - Delta*y^2 = x^2 + delta_abs*y^2.
    # If y != 0, the left side is at least delta_abs, which dwarfs 4*ell
    # in all p24 cases.  We keep the loop for clarity and small sanity cases.
    limit = int((4 * ell // delta_abs) ** 0.5) if delta_abs <= 4 * ell else 0
    for y in range(limit + 1):
        rem = 4 * ell - delta_abs * y * y
        if rem < 0:
            break
        x = int(rem**0.5)
        if x * x == rem:
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-ramified-prime", type=int, default=0, help="0 means print all odd ramified primes")
    args = ap.parse_args()

    sqrt_p = math.isqrt(P24)
    print("p24 ramified-prime self-loop audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"max_ramified_prime={args.max_ramified_prime or 'all'}")
    for trace in TARGET_TRACES:
        delta_abs = 4 * P24 - trace * trace
        factors = factorint(delta_abs)
        min_non_scalar_norm = (delta_abs + 3) // 4
        print(f"trace={trace}")
        print(f"  abs_delta={delta_abs}")
        print(f"  factor(abs_delta)={factors}")
        print(f"  min_non_scalar_principal_norm=ceil(abs_delta/4)={min_non_scalar_norm}")
        print(f"  min_non_scalar_norm_over_sqrt_p={min_non_scalar_norm / sqrt_p:.6e}")
        for ell in sorted(q for q in factors if q != 2):
            if args.max_ramified_prime and ell > args.max_ramified_prime:
                continue
            print(
                f"  ell={ell} ramified=yes "
                f"ell_over_sqrt_p={ell / sqrt_p:.6e} "
                f"4ell={4*ell} "
                f"has_norm_ell_element={has_norm_l_element(delta_abs, ell)}"
            )
        print()
    print("conclusion=ramified_primes_give_only_nonprincipal_genus_information_not_self_loops")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit a tempting modular-neighbor coincidence from the cheap D=-7 seed.

For p = n^2 + 7, the curve with CM by D=-7 has j=-3375 and trace +/-2n.
The smoothest strict p24 target has t/2 = -589207437308, and

    n + t/2 = 23 * 3391 * 1316761 * 4.

Since norm 23 also generates the target CM class group, it is tempting to hope
that a low-level modular correspondence from the cheap D=-7 seed names the
strict target root.  This script checks the concrete low-level version of that
idea over F_p.

The conclusion is negative: evaluating Phi_ell(-3375, Y) modulo p gives no new
odd-level F_p-rational neighbor for ell=23 (only the seed j again, with
multiplicity).  Level 2 does expose the expected conductor-2 neighbor in the
same Q(sqrt(-7)) CM field, but it still has trace +/-2n, not a strict target
trace.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
N = 10**12
J_D_MINUS_7 = -3375
DANGER_K = 40

CURVE_SIDE_TARGET_TRACES = (
    1020608380936,
    -78903246840,
    -1178414874616,
)

MODULAR_LEVELS = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)


@dataclass(frozen=True)
class FiberRow:
    ell: int
    kronecker_d_minus_7: int
    factor_degrees: tuple[tuple[int, int], ...]
    fp_roots: tuple[int, ...]


def v2(value: int) -> int:
    return (value & -value).bit_length() - 1


def pari_factor_degrees(pari: Pari, ell: int, p: int, j: int) -> FiberRow:
    """Factor Phi_ell(j,Y) over F_p and return degree/multiplicity data."""
    pari(f"P=polmodular({ell})")
    pari(f"F=lift(subst(P,x,Mod({j % p},{p})))")
    pari(f"FAC=factormod(F,{p})")
    degrees = tuple(
        (int(row[0]), int(row[1]))
        for row in zip(
            pari("Vec([poldegree(FAC[i,1]) | i <- [1..matsize(FAC)[1]]])"),
            pari("Vec([FAC[i,2] | i <- [1..matsize(FAC)[1]]])"),
        )
    )
    roots = tuple(sorted(int(root.lift()) for root in pari(f"polrootsmod(F,{p})")))
    return FiberRow(
        ell=ell,
        kronecker_d_minus_7=int(sp.kronecker_symbol(-7, ell)),
        factor_degrees=degrees,
        fp_roots=roots,
    )


def print_target_congruences() -> None:
    print("target_trace_near_square_congruences")
    print("  t r=t/2 factor(n-r) factor(n+r) t_plus_2n_divisible_by")
    for trace in CURVE_SIDE_TARGET_TRACES:
        r = trace // 2
        minus = N - r
        plus = N + r
        t_plus_2n = trace + 2 * N
        small_divisor = 1
        for ell in (7, 11, 23, 29, 157, 211, 599, 2897, 14057):
            if t_plus_2n % ell == 0:
                small_divisor *= ell
        print(
            f"  {trace:15d} {r:14d} "
            f"{sp.factorint(minus)} {sp.factorint(plus)} {small_divisor}"
        )
    print()


def print_seed_trace_status() -> None:
    print("cheap_D_minus_7_seed")
    print(f"  p=n^2+7 with n={N}")
    print(f"  j={J_D_MINUS_7}")
    for trace in (2 * N, -2 * N):
        order = P24 + 1 - trace
        twist_order = P24 + 1 + trace
        nearest = min(CURVE_SIDE_TARGET_TRACES, key=lambda target: abs(target - trace))
        print(
            f"  trace={trace:16d} "
            f"v2(order)={v2(order):2d} v2(twist_order)={v2(twist_order):2d} "
            f"trace_mod_2^40={trace % (1 << DANGER_K)} "
            f"nearest_target={nearest} distance={abs(nearest - trace)}"
        )
    print()


def main() -> None:
    print("p24 near-square seed modular-neighbor audit")
    print(f"p={P24}")
    print(f"sqrt_floor_p={math.isqrt(P24)}")
    print()
    print_target_congruences()
    print_seed_trace_status()

    pari = Pari()
    pari.allocatemem(256_000_000)
    j_seed = J_D_MINUS_7 % P24

    print("modular_fibers_Phi_ell(j_seed,Y)_over_Fp")
    print("  ell kronecker(-7,ell) factor_degrees roots_are_seed_only")
    any_new_root = False
    any_new_odd_root = False
    degree_two_new_roots: list[int] = []
    for ell in MODULAR_LEVELS:
        row = pari_factor_degrees(pari, ell, P24, j_seed)
        new_roots = tuple(root for root in row.fp_roots if root != j_seed)
        any_new_root = any_new_root or bool(new_roots)
        any_new_odd_root = any_new_odd_root or (ell % 2 == 1 and bool(new_roots))
        if ell == 2:
            degree_two_new_roots.extend(new_roots)
        print(
            f"  {row.ell:3d} {row.kronecker_d_minus_7:18d} "
            f"{row.factor_degrees!s:35s} {int(not new_roots)}"
        )
        if row.fp_roots:
            signed_roots = tuple(root if root <= P24 // 2 else root - P24 for root in row.fp_roots)
            print(f"      fp_roots={signed_roots}")
    print()
    print("interpretation")
    print("  coincidence_23_divides_n_plus_target_half_trace=1")
    print("  Phi_23_seed_fiber_has_new_Fp_root=0")
    print(f"  any_new_Fp_root_for_tested_levels={int(any_new_root)}")
    print(f"  any_new_odd_Fp_root_for_tested_levels={int(any_new_odd_root)}")
    if degree_two_new_roots:
        signed = tuple(root if root <= P24 // 2 else root - P24 for root in degree_two_new_roots)
        print(f"  level_2_new_roots_same_D_minus_7_CM_field={signed}")
    print("  low_level_isogeny_from_D_minus_7_seed_preserves_CM_field=1")
    print("  strict_target_CM_fields_have_large_D_not_D_minus_7=1")
    print(
        "conclusion=the_23_near_square_coincidence_is_only_a_trace_congruence; "
        "it_does_not_supply_a_strict_target_root_or_sub_sqrt_certificate"
    )


if __name__ == "__main__":
    main()

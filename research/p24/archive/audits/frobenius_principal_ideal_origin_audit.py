#!/usr/bin/env python3
"""Audit the Frobenius-principal-ideal origin trap.

For a fixed target trace t, Frobenius satisfies

    pi^2 - t*pi + p = 0

in the CM order of discriminant Delta=t^2-4p.  Since pi is an actual element
of the order, the prime above p is principal.  This can sound like it should
select the principal class/root.

It does not.  Principal Frobenius means the rational prime p splits completely
in the ring class field, so every target CM root lies in F_p and Frobenius
acts trivially on all of them.  It fixes the whole torsor, not a point in it.

This script records that arithmetic for the strict p24 traces and links it to
the D=-5000 toy where Frobenius fixes all roots over the splitting field.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import sympy as sp

P24 = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Row:
    trace: int
    delta: int
    conductor: int
    fundamental_D: int
    norm_pi: int
    trace_pi: int


def squarefree_part(n: int) -> int:
    out = 1
    for prime, exp in sp.factorint(abs(n)).items():
        if exp & 1:
            out *= int(prime)
    return out


def fundamental_discriminant(delta: int) -> int:
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def row(trace: int) -> Row:
    delta = trace * trace - 4 * P24
    D = fundamental_discriminant(delta)
    conductor_sq = delta // D
    conductor = math.isqrt(conductor_sq)
    if conductor * conductor != conductor_sq:
        raise AssertionError((trace, delta, D))
    return Row(trace, delta, conductor, D, P24, trace)


def main() -> None:
    print("p24 Frobenius principal-ideal origin audit")
    print(f"p={P24}")
    print("strict_trace_rows")
    for r in (row(t) for t in TRACES):
        print(f"trace={r.trace}")
        print(f"  Delta=t^2-4p={r.delta}")
        print(f"  fundamental_D={r.fundamental_D}")
        print(f"  conductor={r.conductor}")
        print(f"  pi_trace={r.trace_pi}")
        print(f"  pi_norm={r.norm_pi}")
        print("  ideal_(pi)_is_principal=1")
        print("  Artin_symbol_at_chosen_prime_above_p_in_ring_class_field=identity")
        print()

    print("torsor_consequence")
    print("  p_splits_completely_in_the_target_ring_class_field=1")
    print("  all_CM_roots_are_Fp_rational=1")
    print("  Frobenius_action_on_root_torsor=identity")
    print("  identity_action_selects_origin=0")
    print()
    print("toy_reference")
    print("  p24/principal_cm_root_torsor_audit.py")
    print("  D=-5000, q=1259: Frobenius fixes all 30 roots, and any root")
    print("  can be labeled principal after rotating the abstract class coordinate.")
    print()
    print(
        "conclusion=the_principal_Frobenius_ideal_proves_splitting_but_does_"
        "not_select_an_embedded_CM_root"
    )


if __name__ == "__main__":
    main()

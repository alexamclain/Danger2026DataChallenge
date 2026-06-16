#!/usr/bin/env python3
"""Cheap abstract class-field quotient probe for the p24 smooth CM target.

The third strict p24 trace has cyclic maximal-order class group

    h = 205880396014 = 2 * 157 * 211 * 3107441.

This script asks PARI only for class-field *quotient degrees* by default.  That
is the cheap part of the embedded-tower lead: abstract unramified quotients of
the Hilbert class field exist for every divisor of h.  Materializing high-degree
defining equations is intentionally opt-in, because it is not the missing
certificate primitive and can turn into a large CPU/stack job.
"""

from __future__ import annotations

import argparse
import math
import time

import sympy as sp
from cypari2 import Pari

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_NUMBER = 205880396014

DEFAULT_REQUESTS = (
    2,
    157,
    211,
    314,
    422,
    66254,
    3107441,
    487868237,
    655670051,
    CLASS_NUMBER,
)


def init_pari(stack_mb: int) -> Pari:
    pari = Pari()
    pari.allocatemem(stack_mb * 1024 * 1024)
    # D_K == 1 mod 4, so O_K = Z[(1 + sqrt(D_K))/2] and the defining
    # polynomial y^2 - y + (1-D_K)/4 has discriminant D_K.
    c = (1 - D_K) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")
    return pari


def polynomial_degree(pari: Pari, poly) -> int:
    return int(pari.poldegree(poly))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-mb", type=int, default=256)
    ap.add_argument(
        "--materialize",
        type=int,
        nargs="*",
        default=[2],
        help=(
            "Opt-in bnrclassfield(bnr,n,1) requests.  Keep this to tiny n "
            "unless you explicitly want a large PARI job."
        ),
    )
    args = ap.parse_args()

    started = time.time()
    pari = init_pari(args.stack_mb)
    factors = {int(q): int(e) for q, e in sp.factorint(CLASS_NUMBER).items()}

    print("p24 abstract class-field quotient probe")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={factors}")
    print(f"sqrt_floor_p={math.isqrt(P24)}")
    print(f"bnf_cyc={[int(x) for x in list(pari('bnf.cyc'))]}")
    print(f"bnr_cyc={[int(x) for x in list(pari('bnr.cyc'))]}")
    print()

    print("abstract_quotient_requests")
    print("  request_n expected_gcd quotient_degree_or_classno")
    for n in DEFAULT_REQUESTS:
        expected = math.gcd(n, CLASS_NUMBER)
        got = int(pari(f"bnrclassno(bnr,{n})"))
        print(f"  {n:15d} {expected:12d} {got:27d}")
    print()

    if args.materialize:
        print("materialized_defining_equations")
        for n in args.materialize:
            before = time.time()
            poly = pari(f"bnrclassfield(bnr,{n},1)")
            elapsed = time.time() - before
            degree = polynomial_degree(pari, poly)
            text = str(poly)
            if len(text) > 120:
                text = text[:117] + "..."
            print(
                f"  request_n={n} degree={degree} elapsed_seconds={elapsed:.3f} "
                f"polynomial_prefix={text}"
            )
        print()

    print("interpretation")
    print("  abstract_unramified_quotients_exist_for_all_divisors=1")
    print("  degree_2_layer_is_the_genus_layer=1")
    print("  quotient_field_defining_equation_is_not_an_embedded_j_selector=1")
    print("  relation_between_quotient_generator_and_j_is_still_required=1")
    print(
        "conclusion=class_field_tower_is_abstractly_available_but_the_missing_"
        "primitive_is_an_embedded_invariant_or_finite_field_identity"
    )
    print(f"elapsed_seconds_total={time.time() - started:.3f}")


if __name__ == "__main__":
    main()

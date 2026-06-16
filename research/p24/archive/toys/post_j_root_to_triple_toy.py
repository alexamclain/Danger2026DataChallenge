#!/usr/bin/env python3
"""Toy: conductor-2 CM j-root -> Montgomery A -> DANGER x0.

The p24 decomposed-CM route ultimately needs to output one embedded CM
`j`-root on the strict branch.  This script checks the remaining finite tail
in the small `p=103, |t|=8` conductor-2 analogue:

    conductor-2 j root
      -> Montgomery A with that j and target trace
      -> x0 by odd-part projection
      -> literal verifier pass.

For p24 a certificate may simply provide `A` and `x0`; the verifier only has
to check `j(A)=j`, the branch/trace conditions if desired, and the DANGER3
doubling replay.
"""

from __future__ import annotations

import argparse
from math import gcd

from cypari2 import Pari

from fixed_trace_cm_root_toy import FROBENIUS_D, P, TRACE, pari_linear_roots
from fixed_trace_montgomery_verifier_toy import (
    legendre,
    montgomery_j_from_A,
    montgomery_trace,
    pp_verify,
)
from post_cm_root_projection_toy import find_projected_x


def montgomery_A_for_j(p: int, j: int) -> list[int]:
    out: list[int] = []
    for A in range(p):
        if gcd(A * A - 4, p) != 1:
            continue
        if montgomery_j_from_A(A, p) == j % p:
            out.append(A)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P)
    parser.add_argument("--trace", type=int, default=TRACE)
    parser.add_argument("--D", type=int, default=FROBENIUS_D)
    parser.add_argument("--trials", type=int, default=200)
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    roots = sorted(pari_linear_roots(pari.polclass(args.D), args.p))

    print("post-j-root to DANGER triple toy")
    print(f"p={args.p}")
    print(f"D={args.D}")
    print(f"target_abs_trace={abs(args.trace)}")
    print(f"j_roots={roots}")
    print(
        "columns: j A_count strict_A_count found trace split side seed_x odd x0 verify"
    )

    total_strict = 0
    total_found = 0
    for j in roots:
        A_values = montgomery_A_for_j(args.p, j)
        strict_rows: list[tuple[int, int, int, tuple[str, int, int, int] | None]] = []
        for A in A_values:
            trace = montgomery_trace(A, args.p)
            if trace is None or abs(trace) != abs(args.trace):
                continue
            split = legendre(A * A - 4, args.p)
            result = find_projected_x(args.p, A, trace, args.trials)
            strict_rows.append((A, trace, split, result))
        total_strict += len(strict_rows)
        if not strict_rows:
            print(
                f"j={j} A_count={len(A_values)} strict_A_count=0 "
                "found=0 trace=NA split=NA side=NA seed_x=NA odd=NA x0=NA verify=0"
            )
            continue
        for A, trace, split, result in strict_rows:
            if result is None:
                print(
                    f"j={j} A_count={len(A_values)} strict_A_count={len(strict_rows)} "
                    f"found=0 trace={trace} split={split} side=NA "
                    "seed_x=NA odd=NA x0=NA verify=0"
                )
                continue
            side, seed_x, odd, x0 = result
            total_found += 1
            print(
                f"j={j} A_count={len(A_values)} strict_A_count={len(strict_rows)} "
                f"found=1 trace={trace} split={split} side={side} "
                f"seed_x={seed_x} odd={odd} x0={x0} verify={int(pp_verify(args.p, A, x0))}"
            )

    print()
    print(f"root_count={len(roots)}")
    print(f"total_strict_A={total_strict}")
    print(f"total_found_triples={total_found}")
    print("conclusion=conductor2_j_roots_lift_to_montgomery_triples_in_toy")


if __name__ == "__main__":
    main()

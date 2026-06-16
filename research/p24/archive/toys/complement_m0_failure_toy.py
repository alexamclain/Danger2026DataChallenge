#!/usr/bin/env python3
"""Pinned counterexample to universal complement M0 nonvanishing.

The wider complement-moment scan found that the K-trivial complement trace
resolvent can vanish even when the exact relative content vector is nonzero.
This file pins the smallest observed failure:

    D=-899, q=281, h=14, m=2, n=7.

Here `M0 = J_0 + J_1` vanishes at a primitive 7th-root packet, while
`M1 = J_1` is nonzero.  Thus the single complement trace scalar is not a
universal theorem, but the two-moment projection still certifies content in
this row.
"""

from __future__ import annotations

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_decomposition_calibration import pari_linear_roots
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import section_fiber_polynomials

D = -899
Q = 281
M = 2
N = 7


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, Q)
    ell, cycle = find_full_cycle_prime(roots, D, Q)
    fibers = section_fiber_polynomials(cycle, Q, M, "complement")
    factors = packet_factors(N, Q)

    print("complement M0 failure toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"h={len(roots)}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"generator_ell={ell}")
    print(f"cycle={cycle}")
    print(f"fibers={[str(f.as_expr()) for f in fibers]}")
    for factor in factors:
        residues = [fiber.rem(factor) for fiber in fibers]
        m0 = sum(residues, sp.Poly(0, factor.gens[0], modulus=Q)).rem(factor)
        m1 = residues[1].rem(factor)
        print()
        print(f"factor={factor.as_expr()}")
        print(f"factor_degree={factor.degree()}")
        print(f"residues={[str(r.as_expr()) for r in residues]}")
        print(f"coord_zero_count={sum(r.is_zero for r in residues)}")
        print(f"content_zero={int(all(r.is_zero for r in residues))}")
        print(f"M0={m0.as_expr()}")
        print(f"M0_zero={int(m0.is_zero)}")
        print(f"M1={m1.as_expr()}")
        print(f"M1_zero={int(m1.is_zero)}")
    print()
    print("interpretation")
    print("  complement_M0_universal_nonvanishing_false=1")
    print("  exact_content_vector_nonzero=1")
    print("  moment_pair_M0_M1_certifies_this_row=1")
    print("conclusion=reported_complement_m0_failure_toy")


if __name__ == "__main__":
    main()

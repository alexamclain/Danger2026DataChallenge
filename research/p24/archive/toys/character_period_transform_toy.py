#!/usr/bin/env python3
"""Toy class-character transform for CM period/cycle sums.

This script makes the Gaussian-period analogy precise in a small CM example.
For D=-5000 the class group is cyclic of order 30 and the norm-3 ideal gives a
full class cycle.  We take the subgroup of size 3, so the quotient has size 10.

Over q=3851 the Hilbert class polynomial splits and q == 1 mod 10, so the
quotient-character Fourier transform is available inside F_q:

    y_r = sum_{k=0}^{2} j_{r + 10k}
    T_s = sum_{r=0}^{9} zeta^(sr) y_r

If the twisted traces T_s were available by a theorem, the period sums y_r and
their degree-10 quotient polynomial would follow by an inverse DFT without
enumerating the subgroup.  In this toy, however, T_s are computed by summing
the embedded vertices, so it is a calibration of the missing primitive.
"""

from __future__ import annotations

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)

Q = 3851
SUBGROUP_SIZE = 3
QUOTIENT_SIZE = H // SUBGROUP_SIZE


def primitive_root_of_order(q: int, order: int) -> int:
    generator = sp.primitive_root(q)
    root = pow(generator, (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("not an order divisor")
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            raise AssertionError("not primitive")
    return int(root)


def dft(values: list[int], zeta: int, q: int) -> list[int]:
    m = len(values)
    out: list[int] = []
    for s in range(m):
        total = 0
        for r, value in enumerate(values):
            total = (total + pow(zeta, s * r, q) * value) % q
        out.append(total)
    return out


def inverse_dft(transformed: list[int], zeta: int, q: int) -> list[int]:
    m = len(transformed)
    inv_m = pow(m, -1, q)
    out: list[int] = []
    for r in range(m):
        total = 0
        for s, value in enumerate(transformed):
            total = (total + pow(zeta, -s * r, q) * value) % q
        out.append(total * inv_m % q)
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    zeta = primitive_root_of_order(Q, QUOTIENT_SIZE)
    period_sums = [
        sum(cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)) % Q
        for r in range(QUOTIENT_SIZE)
    ]
    twisted_traces = dft(period_sums, zeta, Q)
    recovered = inverse_dft(twisted_traces, zeta, Q)
    quotient_poly = monic_poly_from_roots(period_sums, Q)

    print("CM class-character period transform toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"q_mod_quotient_size={Q % QUOTIENT_SIZE}")
    print(f"zeta_order_{QUOTIENT_SIZE}={zeta}")
    print()
    print(f"period_sums={period_sums}")
    print(f"twisted_traces={twisted_traces}")
    print(f"inverse_dft_recovers_period_sums={int(recovered == period_sums)}")
    print(f"period_polynomial_degree={len(quotient_poly) - 1}")
    print(f"period_polynomial_coeffs_ascending_mod_q={quotient_poly}")
    print()
    print("interpretation")
    print("  quotient_periods_are_inverse_dft_of_character_twisted_traces=1")
    print("  dft_step_is_cheap_once_twisted_traces_are_known=1")
    print("  this_toy_computed_twisted_traces_by_enumerating_vertices=1")
    print(
        "conclusion=the_missing_theorem_can_be_rephrased_as_sublinear_"
        "computation_of_class_character_twisted_traces"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Relative class-character traces for an embedded period tower.

This is the Fourier-side companion to ``tower_phase_refinement_toy.py``.  It
uses the same complete CM torsor

    D = -5000, h = 30 = 2 * 3 * 5 over F_1259

and the same quotient tower

    G >= K=<g^2> >= H=<g^6>.

The point is theorem bookkeeping.  Once the embedded j-cycle is known, the
degree-3 child polynomials above the two top roots can be recovered from
relative character traces on K/H.  Conversely, those traces are just the
discrete Fourier transform of the child period vector.  Thus a p24 tower
construction is equivalent to computing these relative, non-genus class
character periods without first enumerating the full CM torsor.
"""

from __future__ import annotations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)

RECOVERY_SIZE = 5
FINE_QUOTIENT = H // RECOVERY_SIZE
TOP_QUOTIENT = 2
RELATIVE_DEGREE = FINE_QUOTIENT // TOP_QUOTIENT


Fq2 = tuple[int, int]


def f2_add(x: Fq2, y: Fq2, q: int = Q) -> Fq2:
    return ((x[0] + y[0]) % q, (x[1] + y[1]) % q)


def f2_mul(x: Fq2, y: Fq2, q: int = Q) -> Fq2:
    """Multiply in F_q[w]/(w^2+w+1).  This is F_{q^2} for q=2 mod 3."""
    a, b = x
    c, d = y
    return ((a * c - b * d) % q, (a * d + b * c - b * d) % q)


def f2_pow(x: Fq2, n: int, q: int = Q) -> Fq2:
    out = (1, 0)
    base = x
    while n:
        if n & 1:
            out = f2_mul(out, base, q)
        base = f2_mul(base, base, q)
        n >>= 1
    return out


def f2_scalar_mul(c: int, x: Fq2, q: int = Q) -> Fq2:
    return (c * x[0] % q, c * x[1] % q)


def f2_from_base(x: int, q: int = Q) -> Fq2:
    return (x % q, 0)


def inverse_dft(traces: list[Fq2], zeta: Fq2, q: int = Q) -> list[Fq2]:
    degree = len(traces)
    inv_degree = pow(degree, -1, q)
    out: list[Fq2] = []
    for r in range(degree):
        value = (0, 0)
        for s, trace in enumerate(traces):
            coeff = f2_pow(zeta, (-s * r) % degree, q)
            value = f2_add(value, f2_mul(coeff, trace, q), q)
        out.append(f2_scalar_mul(inv_degree, value, q))
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    fine_periods = [
        sum(cycle[(r + FINE_QUOTIENT * k) % H] for k in range(RECOVERY_SIZE)) % Q
        for r in range(FINE_QUOTIENT)
    ]
    top_periods = [
        sum(cycle[(r + TOP_QUOTIENT * k) % H] for k in range(H // TOP_QUOTIENT)) % Q
        for r in range(TOP_QUOTIENT)
    ]

    zeta = (0, 1)  # primitive cube root in F_q[w]/(w^2+w+1)
    if f2_pow(zeta, RELATIVE_DEGREE) != (1, 0) or zeta == (1, 0):
        raise AssertionError("bad relative root of unity")

    relative_rows: list[tuple[int, list[int], list[Fq2], list[Fq2], list[int]]] = []
    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        traces = []
        for s in range(RELATIVE_DEGREE):
            value = (0, 0)
            for a, child in enumerate(children):
                coeff = f2_pow(zeta, s * a, Q)
                value = f2_add(value, f2_scalar_mul(child, coeff, Q), Q)
            traces.append(value)
        recovered = inverse_dft(traces, zeta, Q)
        if any(x[1] != 0 for x in recovered):
            raise AssertionError("relative inverse DFT did not descend to F_q")
        recovered_base = [x[0] for x in recovered]
        child_poly = monic_poly_from_roots(children, Q)
        recovered_poly = monic_poly_from_roots(recovered_base, Q)
        relative_rows.append((parent, children, traces, recovered, child_poly))
        if recovered_poly != child_poly:
            raise AssertionError("relative Fourier inversion failed")

    print("relative tower character toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"chain=G>=<g^{TOP_QUOTIENT}>=K>=<g^{FINE_QUOTIENT}>=H")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print(f"recovery_subgroup_size={RECOVERY_SIZE}")
    print(f"relative_root_field=F_{Q}^2")
    print(f"primitive_relative_root_pair={zeta}")
    print()
    print(f"top_periods={top_periods}")
    print(f"fine_periods={fine_periods}")
    print()
    for parent, children, traces, recovered, child_poly in relative_rows:
        print(f"parent={parent} top_value={top_periods[parent]}")
        print(f"  child_periods={children}")
        print(f"  relative_character_traces_pairs={traces}")
        print(f"  inverse_dft_recovered_pairs={recovered}")
        print(f"  child_polynomial_coeffs_ascending={child_poly}")
    print()
    print("interpretation")
    print("  relative_child_polynomial_is_equivalent_to_relative_character_traces=1")
    print("  abstract_tower_degrees_do_not_supply_these_traces=1")
    print("  p24_157_and_211_steps_need_non_genus_relative_traces=1")
    print(
        "conclusion=embedded_class_field_tower_phase_is_relative_"
        "class_character_period_computation"
    )


if __name__ == "__main__":
    main()

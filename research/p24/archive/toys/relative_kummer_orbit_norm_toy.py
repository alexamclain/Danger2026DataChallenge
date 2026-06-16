#!/usr/bin/env python3
"""Toy audit for norm-compressing relative Kummer constants.

The relative Kummer normal form replaces a prime-degree child polynomial by
primitive Kummer powers K_s = T_s^r.  Frobenius groups these K_s into orbits.
Could one keep only an orbit norm instead of the whole orbit?

In the D=-5000 degree-3 toy, K_1 lives in F_{q^2}; its orbit is {K_1,K_2}
and its norm is K_1*K_2 in F_q.  This script fixes the true parent trace T0
and the true norm of K_1, then enumerates every K in F_{q^2} with that norm.
For each K it tries cube roots as possible T_1 values and keeps the choices
whose inverse DFT descends to F_q child periods.

If many child polynomials survive, then orbit norm is only a p-unit/nonzero
certificate candidate; it is not enough to reconstruct the selected child
polynomial.
"""

from __future__ import annotations

from collections import defaultdict

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
from relative_kummer_reconstruction_toy import (
    f2_frob,
    f2_equal_base,
    inverse_dft_degree3,
)
from relative_tower_character_toy import (
    FINE_QUOTIENT,
    RECOVERY_SIZE,
    RELATIVE_DEGREE,
    TOP_QUOTIENT,
    f2_add,
    f2_mul,
    f2_pow,
    f2_scalar_mul,
)


Fq2 = tuple[int, int]


def f2_trace(x: Fq2, q: int = Q) -> int:
    y = f2_add(x, f2_frob(x, q), q)
    return f2_equal_base(y)


def f2_norm(x: Fq2, q: int = Q) -> int:
    y = f2_mul(x, f2_frob(x, q), q)
    return f2_equal_base(y)


def cube_map(q: int = Q) -> dict[Fq2, list[Fq2]]:
    out: dict[Fq2, list[Fq2]] = defaultdict(list)
    for a in range(q):
        for b in range(q):
            x = (a, b)
            out[f2_pow(x, RELATIVE_DEGREE, q)].append(x)
    return dict(out)


def descending_polynomials_from_kummer(
    t0: int,
    kummer: Fq2,
    cubes: dict[Fq2, list[Fq2]],
    zeta: Fq2,
    q: int = Q,
) -> set[tuple[int, ...]]:
    polys: set[tuple[int, ...]] = set()
    for t1 in cubes.get(kummer, []):
        children = inverse_dft_degree3(t0, t1, zeta, q)
        if all(child[1] == 0 for child in children):
            base_children = [f2_equal_base(child) for child in children]
            polys.add(tuple(monic_poly_from_roots(base_children, q)))
    return polys


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
    zeta = (0, 1)
    cubes = cube_map(Q)

    print("relative Kummer orbit-norm toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"relative_degree={RELATIVE_DEGREE}")
    print()

    for parent in range(TOP_QUOTIENT):
        children = [
            fine_periods[parent + TOP_QUOTIENT * a]
            for a in range(RELATIVE_DEGREE)
        ]
        true_poly = tuple(monic_poly_from_roots(children, Q))
        t0 = sum(children) % Q
        t1 = (0, 0)
        for a, child in enumerate(children):
            t1 = f2_add(t1, f2_scalar_mul(child, f2_pow(zeta, a, Q), Q), Q)
        kummer = f2_pow(t1, RELATIVE_DEGREE, Q)
        norm = f2_norm(kummer, Q)
        trace = f2_trace(kummer, Q)

        norm_candidates: list[Fq2] = []
        trace_norm_candidates: list[Fq2] = []
        norm_polys: set[tuple[int, ...]] = set()
        trace_norm_polys: set[tuple[int, ...]] = set()
        for a in range(Q):
            for b in range(Q):
                candidate = (a, b)
                if f2_norm(candidate, Q) != norm:
                    continue
                norm_candidates.append(candidate)
                polys = descending_polynomials_from_kummer(t0, candidate, cubes, zeta, Q)
                norm_polys.update(polys)
                if f2_trace(candidate, Q) == trace:
                    trace_norm_candidates.append(candidate)
                    trace_norm_polys.update(polys)

        print(f"parent={parent}")
        print(f"  true_child_polynomial={true_poly}")
        print(f"  true_K={kummer}")
        print(f"  true_K_trace={trace}")
        print(f"  true_K_norm={norm}")
        print(f"  norm_candidate_count={len(norm_candidates)}")
        print(f"  norm_descending_polynomial_count={len(norm_polys)}")
        print(f"  norm_true_polynomial_survives={int(true_poly in norm_polys)}")
        print(f"  trace_norm_candidate_count={len(trace_norm_candidates)}")
        print(f"  trace_norm_descending_polynomial_count={len(trace_norm_polys)}")
        print(f"  trace_norm_true_polynomial_survives={int(true_poly in trace_norm_polys)}")
    print()
    print("interpretation")
    print("  orbit_norm_alone_leaves_many_candidate_Kummer_constants=1")
    print("  orbit_norm_alone_does_not_reconstruct_child_polynomial=1")
    print("  trace_plus_norm_identifies_the_Frobenius_pair_in_degree_2=1")
    print("conclusion=relative_Kummer_orbit_norm_is_punit_payload_not_selected_chain_payload")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check whether packet interpolant divisors have small Heegner support.

The phase-aware Borcherds route would be more credible if the tautological
rational interpolant for a packet scalar had numerator/denominator support on
CM/Heegner reductions or cuspidal data.  This script performs a small
falsification test:

1. build a packet scalar function on a small embedded CM cycle;
2. compute a minimal rational interpolant in the selected j coordinate;
3. extract its numerator roots over F_q;
4. compare those roots with a bounded union of reductions of Hilbert class
   polynomial roots for small fundamental discriminants.

Generic roots do not disprove a high-degree phase-aware Borcherds product, but
they rule out the easy "this scalar is already a simple Heegner-supported
divisor in j" explanation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle
from embedded_selector_identity_toy import candidate_from_basis, matrix_for_degree, nullspace_mod
from packet_scalar_divisor_shape_toy import (
    packet_values,
    rational_degree,
)
from packetized_relative_content_scan import packet_factors


@dataclass(frozen=True)
class HeegnerRootHit:
    root: int
    discriminants: tuple[int, ...]


def is_squarefree(n: int) -> bool:
    n = abs(n)
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1 if d == 2 else 2
    return True


def is_fundamental_discriminant(D: int) -> bool:
    if D >= 0:
        return False
    if D % 4 == 1:
        return is_squarefree(D)
    if D % 4 == 0:
        d = D // 4
        return d % 4 in (2, 3) and is_squarefree(d)
    return False


def fixed_cycle(D: int, q: int, ell: int | None) -> tuple[int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), q)
    if ell is None:
        raise ValueError("this scan expects an explicit split-prime ell")
    graph = isogeny_neighbors(roots, ell, q)
    return ell, walk_cycle(graph)


def interpolant_roots(pairs: list[tuple[int, int]], q: int) -> tuple[int, list[int], list[int]]:
    degree = rational_degree(pairs, q)
    matrix = matrix_for_degree(pairs, degree, q)
    basis, _ = nullspace_mod(matrix, q)
    candidate = candidate_from_basis(basis, degree, pairs, q)
    if candidate is None:
        raise RuntimeError("rational interpolant disappeared")
    numerator, denominator = candidate
    num_roots: list[int] = []
    den_roots: list[int] = []
    for x in range(q):
        num = 0
        den = 0
        for coeff in reversed(numerator):
            num = (num * x + coeff) % q
        for coeff in reversed(denominator):
            den = (den * x + coeff) % q
        if num == 0 and den != 0:
            num_roots.append(x)
        if den == 0:
            den_roots.append(x)
    return degree, num_roots, den_roots


def heegner_roots(q: int, max_abs_D: int, max_h: int) -> dict[int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: dict[int, list[int]] = {}
    for D in range(-3, -max_abs_D - 1, -1):
        if not is_fundamental_discriminant(D) or q % abs(D) == 0:
            continue
        h = int(pari.quadclassunit(D)[0])
        if h > max_h:
            continue
        try:
            roots = pari_linear_roots(pari.polclass(D), q)
        except ValueError:
            continue
        if roots:
            out[D] = roots
    return out


def root_hits(roots: list[int], heegner: dict[int, list[int]]) -> list[HeegnerRootHit]:
    by_root: dict[int, list[int]] = {root: [] for root in roots}
    wanted = set(roots)
    for D, d_roots in heegner.items():
        for root in d_roots:
            if root in wanted:
                by_root[root].append(D)
    return [HeegnerRootHit(root, tuple(ds)) for root, ds in sorted(by_root.items())]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--D", type=int, default=-2239)
    parser.add_argument("--q", type=int, default=2243)
    parser.add_argument("--ell", type=int, default=2)
    parser.add_argument("--m", type=int, default=7)
    parser.add_argument("--factor-index", type=int, default=0)
    parser.add_argument("--scalar", choices=("hermitian", "ordinary"), default="hermitian")
    parser.add_argument("--max-heegner-abs-D", type=int, default=5000)
    parser.add_argument("--max-heegner-h", type=int, default=40)
    args = parser.parse_args()

    _ell, cycle = fixed_cycle(args.D, args.q, args.ell)
    n = len(cycle) // args.m
    factors = packet_factors(n, args.q)
    factor = factors[args.factor_index]
    pairs = packet_values(cycle, args.q, args.m, factor, args.scalar)
    degree, num_roots, den_roots = interpolant_roots(pairs, args.q)
    cm_roots = {x for x, _ in pairs}
    heegner = heegner_roots(args.q, args.max_heegner_abs_D, args.max_heegner_h)
    hits = root_hits(num_roots, heegner)

    print("phase divisor Heegner-support scan")
    print(f"D={args.D}")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"h={len(cycle)}")
    print(f"m={args.m}")
    print(f"n={n}")
    print(f"scalar={args.scalar}")
    print(f"factor_index={args.factor_index}")
    print(f"factor_degree={factor.degree()}")
    print(f"rational_degree={degree}")
    print(f"numerator_roots={num_roots}")
    print(f"denominator_roots={den_roots}")
    print(f"numerator_roots_in_target_cm={sorted(set(num_roots) & cm_roots)}")
    print(f"heegner_discriminants_tested={len(heegner)}")
    print(f"heegner_roots_total={sum(len(v) for v in heegner.values())}")
    print("numerator_root_heegner_hits")
    for hit in hits:
        print(f"  root={hit.root} discriminants={hit.discriminants}")
    print()
    print("interpretation")
    print("  numerator_roots_outside_target_cm=" + str(int(not set(num_roots) <= cm_roots)))
    print("  numerator_roots_with_small_heegner_support=" + str(sum(bool(hit.discriminants) for hit in hits)))
    print("  tested_simple_heegner_supported_divisor_route=" + str(int(True)))
    print("conclusion=reported_phase_divisor_heegner_support_scan")


if __name__ == "__main__":
    main()

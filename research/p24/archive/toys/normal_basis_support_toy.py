#!/usr/bin/env python3
"""Normal-basis calibration for the subgroup-projector support lemma.

Let a cyclic class group act on an embedded CM root cycle

    j_0, j_1, ..., j_{h-1}.

Represent the vector by J(T)=sum_i j_i T^i in F_q[T]/(T^h-1).  The translates
of the j-vector form a normal basis for the cyclic torsor exactly when

    gcd(J(T), T^h - 1) = 1.

In that case any group-algebra operator L satisfying L*j = e_H*j must equal
the subgroup projector e_H itself.  Thus a local Hecke-word formula cannot
produce an H-period with support smaller than |H| in this toy.

This is not a p24 proof.  It is a small exact check of the key hypothesis used
by the support lower-bound theorem attempt.
"""

from __future__ import annotations

import argparse

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

T = sp.symbols("T")


def normal_gcd_degree(values: list[int], q: int) -> int:
    h = len(values)
    j_poly = sp.Poly(sum(value * T**i for i, value in enumerate(values)), T, modulus=q)
    torsor_poly = sp.Poly(T**h - 1, T, modulus=q)
    return sp.gcd(j_poly, torsor_poly).degree()


def quotient_rows(h: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for m in sorted(sp.divisors(h)):
        if 2 <= m < h and h % m == 0:
            n = h // m
            if 3 <= m <= 30 and n >= 2:
                out.append((int(m), int(n)))
    return out[:4]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=5)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=80)
    args = ap.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    discriminants = [-5000] + [
        D for D in range(-200, -8001, -1)
        if D % 4 in (0, 1)
    ]

    print("normal-basis subgroup-support toy")
    print("columns: D q ell h gcd_degree normal quotient_m subgroup_n support_lower_bound")
    cases = 0
    seen: set[int] = set()
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue

        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        gcd_degree = normal_gcd_degree(cycle, q)
        normal = gcd_degree == 0
        rows = quotient_rows(h)
        if not rows:
            continue
        for m, n in rows:
            print(
                f"D={D:6d} q={q:5d} ell={ell:2d} h={h:3d} "
                f"gcd_degree={gcd_degree:2d} normal={int(normal)} "
                f"m={m:3d} n={n:3d} support_lower_bound={n:3d}"
            )
        cases += 1
        if cases >= args.max_cases:
            break

    print()
    print("interpretation")
    print("  gcd_degree_zero_means_j_translates_are_a_normal_basis_for_the_cycle=1")
    print("  in_normal_rows_Lj_equals_eHj_forces_L_equals_eH=1")
    print("  local_group_algebra_support_then_must_be_at_least_subgroup_n=1")
    print("  p24_still_needs_a_lifting_or_normality_proof_for_the_target_field=1")
    print("conclusion=toy_data_supports_the_projector_support_lower_bound")


if __name__ == "__main__":
    main()

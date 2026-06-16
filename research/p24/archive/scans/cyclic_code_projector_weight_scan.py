#!/usr/bin/env python3
"""Small CM scan for cyclic-code sparse projector accidents.

This broadens `cyclic_code_projector_weight_toy.py` from the calibrated
D=-5000 row to a few small CM cycles.  For each cyclic embedded CM cycle it
artificially inserts one low-degree packet into the annihilator and asks
whether the coset

    e_H + Ann(j)

contains a representative of Hamming weight below the subgroup-projector
support `|H|`.

The scan is intentionally small.  It is looking for a structural accident,
not trying to enumerate large class sets.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_factor

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime

T = sp.symbols("T")


@dataclass(frozen=True)
class ScanRow:
    D: int
    q: int
    ell: int
    h: int
    quotient_size: int
    subgroup_size: int
    natural_gcd_degree: int
    artificial_factor_degree: int
    projector_weight: int
    best_coset_weight: int
    reduced_weight: bool


def poly_from_values(values: list[int], q: int) -> sp.Poly:
    return sp.Poly(sum(value * T**i for i, value in enumerate(values)), T, modulus=q)


def coeff_vector(poly: sp.Poly, length: int, q: int) -> list[int]:
    out = [0] * length
    for (power,), value in poly.as_dict().items():
        out[power % length] = (out[power % length] + int(value)) % q
    return out


def low_degree_factor(h: int, q: int, max_degree: int) -> sp.Poly | None:
    coeffs = [1] + [0] * (h - 1) + [-1]
    _unit, factors = gf_factor(coeffs, q, ZZ)
    candidates: list[list[int]] = []
    for factor_coeffs, multiplicity in factors:
        degree = len(factor_coeffs) - 1
        if multiplicity == 1 and 1 < degree <= max_degree:
            candidates.append([int(c) % q for c in factor_coeffs])
    if not candidates and max_degree >= 1:
        for factor_coeffs, multiplicity in factors:
            degree = len(factor_coeffs) - 1
            if multiplicity == 1 and degree == 1:
                candidates.append([int(c) % q for c in factor_coeffs])
    if not candidates:
        return None
    # Prefer the largest allowed degree, then lexicographic determinism.
    chosen = sorted(candidates, key=lambda c: (-(len(c) - 1), c))[0]
    return sp.Poly.from_list(chosen, gens=T, modulus=q)


def projector_vector(h: int, quotient_size: int) -> list[int]:
    subgroup_size = h // quotient_size
    out = [0] * h
    for k in range(subgroup_size):
        out[k * quotient_size] = 1
    return out


def weight(values: list[int], q: int) -> int:
    return sum(1 for value in values if value % q)


def cyclic_shift(values: list[int], shift: int) -> list[int]:
    h = len(values)
    out = [0] * h
    for i, value in enumerate(values):
        out[(i + shift) % h] = value
    return out


def min_weight_degree1(base: list[int], generator: list[int], q: int) -> int:
    best = len(base) + 1
    for a in range(q):
        candidate = [(x + a * y) % q for x, y in zip(base, generator)]
        best = min(best, weight(candidate, q))
    return best


def min_weight_degree2(base: list[int], generator: list[int], q: int) -> int:
    basis0 = generator
    basis1 = cyclic_shift(generator, 1)
    best = len(base) + 1
    for a in range(q):
        a_part = [(x + a * y) % q for x, y in zip(base, basis0)]
        for b in range(q):
            candidate = [(x + b * y) % q for x, y in zip(a_part, basis1)]
            current = weight(candidate, q)
            if current < best:
                best = current
                if best == 0:
                    return best
    return best


def quotient_sizes(h: int, max_quotients: int) -> list[int]:
    out = [
        int(d)
        for d in sp.divisors(h)
        if 2 <= d <= min(30, h // 2) and h % d == 0
    ]
    # Prefer nontrivial middle quotients but keep deterministic order.
    return sorted(out, key=lambda d: (abs(d - h // d), d))[:max_quotients]


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    max_degree: int,
    max_quotients: int,
    max_q_for_degree2: int,
) -> list[ScanRow]:
    h = len(cycle)
    torsion = sp.Poly(T**h - 1, T, modulus=q)
    j_poly = poly_from_values(cycle, q)
    natural_gcd = sp.gcd(j_poly, torsion)
    factor = low_degree_factor(h, q, max_degree)
    if factor is None:
        return []
    quotient, remainder = torsion.div(factor)
    if not remainder.is_zero:
        raise AssertionError((D, q, h, factor))
    generator = coeff_vector(quotient, h, q)
    rows: list[ScanRow] = []
    for quotient_size in quotient_sizes(h, max_quotients):
        subgroup_size = h // quotient_size
        projector = projector_vector(h, quotient_size)
        projector_weight = weight(projector, q)
        if factor.degree() == 1:
            best_weight = min_weight_degree1(projector, generator, q)
        elif factor.degree() == 2 and q <= max_q_for_degree2:
            best_weight = min_weight_degree2(projector, generator, q)
        else:
            continue
        rows.append(
            ScanRow(
                D=D,
                q=q,
                ell=ell,
                h=h,
                quotient_size=quotient_size,
                subgroup_size=subgroup_size,
                natural_gcd_degree=natural_gcd.degree(),
                artificial_factor_degree=factor.degree(),
                projector_weight=projector_weight,
                best_coset_weight=best_weight,
                reduced_weight=best_weight < projector_weight,
            )
        )
    return rows


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_degree: int,
    max_quotients: int,
    max_q_for_degree2: int,
) -> list[ScanRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]

    rows: list[ScanRow] = []
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
        if not (min_h <= h <= max_h):
            continue
        split = find_splitting_prime(pari, hilbert, h)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        case_rows = audit_case(
            D,
            q,
            ell,
            cycle,
            max_degree=max_degree,
            max_quotients=max_quotients,
            max_q_for_degree2=max_q_for_degree2,
        )
        if not case_rows:
            continue
        rows.extend(case_rows)
        cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=5)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=80)
    ap.add_argument("--max-abs-D", type=int, default=8000)
    ap.add_argument("--max-degree", type=int, default=2)
    ap.add_argument("--max-quotients", type=int, default=3)
    ap.add_argument("--max-q-for-degree2", type=int, default=1500)
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_degree=args.max_degree,
        max_quotients=args.max_quotients,
        max_q_for_degree2=args.max_q_for_degree2,
    )

    print("cyclic-code projector weight scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"max_degree={args.max_degree}")
    print(f"max_quotients={args.max_quotients}")
    print(f"max_q_for_degree2={args.max_q_for_degree2}")
    print()
    print(
        "D q ell h quotient subgroup natural_gcd artificial_degree "
        "projector_weight best_coset_weight reduced"
    )
    for row in rows:
        print(
            f"{row.D:7d} {row.q:5d} {row.ell:3d} {row.h:3d} "
            f"{row.quotient_size:8d} {row.subgroup_size:8d} "
            f"{row.natural_gcd_degree:11d} {row.artificial_factor_degree:17d} "
            f"{row.projector_weight:16d} {row.best_coset_weight:17d} "
            f"{int(row.reduced_weight)}"
        )

    reduced = sum(1 for row in rows if row.reduced_weight)
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  reduced_weight_rows={reduced}")
    print()
    print("interpretation")
    print("  artificial_low_degree_packet_kernel_tests_annihilator_coset_escape=1")
    print("  reduced_weight_row_would_suggest_sparse_projector_accident=1")
    print("  no_reduced_rows_supports_projector_barrier_in_small_CM_cycles=1")
    print("conclusion=reported_cyclic_code_projector_weight_scan")


if __name__ == "__main__":
    main()

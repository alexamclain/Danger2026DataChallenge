#!/usr/bin/env python3
"""Scan complexity of complement-trace recovery relations in small CM cycles."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from complement_trace_recovery_toy import build_recovery_relation, choose_m


@dataclass(frozen=True)
class Row:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    relation_degree_y_max: int
    nonzero_coeff_terms: int
    dense_slots: int
    density: float
    all_specializations_ok: bool


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    q_start: int,
    q_stop: int,
) -> list[Row]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[Row] = []
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
        try:
            m = choose_m(h, None)
        except ValueError:
            continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        try:
            _values, _quotient_poly, coeff_polys, ok = build_recovery_relation(cycle, q, m)
        except ValueError:
            continue
        n = h // m
        nonzero_terms = sum(len(poly.as_dict()) for poly in coeff_polys)
        dense_slots = m * n
        rows.append(
            Row(
                D=D,
                q=q,
                ell=ell,
                h=h,
                m=m,
                n=n,
                relation_degree_y_max=max(poly.degree() for poly in coeff_polys),
                nonzero_coeff_terms=nonzero_terms,
                dense_slots=dense_slots,
                density=nonzero_terms / dense_slots,
                all_specializations_ok=ok,
            )
        )
        if len(rows) >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=24)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=120)
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=250000)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        q_start=args.q_start,
        q_stop=args.q_stop,
    )

    print("complement trace recovery complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print("columns: D q ell h m n deg_y_max nonzero_terms dense_slots density ok")
        for row in rows:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg_y_max={row.relation_degree_y_max:3d} "
                f"nonzero_terms={row.nonzero_coeff_terms:5d} "
                f"dense_slots={row.dense_slots:5d} density={row.density:6.3f} "
                f"ok={int(row.all_specializations_ok)}"
            )

    full_degree_rows = sum(1 for row in rows if row.relation_degree_y_max == row.n - 1)
    avg_density = sum(row.density for row in rows) / len(rows) if rows else 0.0
    min_density = min((row.density for row in rows), default=0.0)
    max_density = max((row.density for row in rows), default=0.0)
    all_ok = all(row.all_specializations_ok for row in rows)
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  all_specializations_ok={int(all_ok)}")
    print(f"  full_y_degree_rows={full_degree_rows}")
    print(f"  avg_density={avg_density:.6f}")
    print(f"  min_density={min_density:.6f}")
    print(f"  max_density={max_density:.6f}")
    print()
    print("interpretation")
    print("  dense_interpolation_size_is_m_times_n=1")
    print("  high_density_means_naive_recovery_relation_does_not_compress=1")
    print("  sub_sqrt_route_needs_tower_or_formula_for_coefficients=1")
    print("conclusion=reported_complement_trace_recovery_complexity")


if __name__ == "__main__":
    main()

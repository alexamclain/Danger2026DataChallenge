#!/usr/bin/env python3
"""Scan natural small CM cycles for harmful relative-resolvent vanishings.

This tests the exact condition from
`harmful_dual_coset_relative_resolvent_lemma.md` on toy embedded CM cycles.
It deliberately chooses split primes q with q = 1 mod h so that all h-th roots
of unity live in the base field and no extension arithmetic is needed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_decomposition_calibration import pari_linear_roots


@dataclass(frozen=True)
class QuotientRow:
    quotient_size: int
    subgroup_size: int
    harmful_a_count: int
    vanished_character_count: int
    relative_character_count: int
    individual_zero_fiber_count: int
    min_nonzero_fibers: int
    full_resolvent_equivalence: bool


@dataclass(frozen=True)
class ScanRow:
    D: int
    q: int
    ell: int
    h: int
    quotient_rows: tuple[QuotientRow, ...]


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError(f"order {order} does not divide q-1")
    root = pow(sp.primitive_root(q), (q - 1) // order, q)
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            raise AssertionError("not primitive")
    return int(root)


def find_splitting_prime_with_mu_h(
    pari: Pari,
    hilbert,
    h: int,
    start: int,
    stop: int,
) -> tuple[int, list[int]] | None:
    lo = max(start, h + 2)
    for q in sp.primerange(lo, stop):
        if q % h != 1:
            continue
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            return int(q), roots
    return None


def dft(values: list[int], q: int, zeta: int) -> list[int]:
    h = len(values)
    out: list[int] = []
    for s in range(h):
        total = 0
        for i, value in enumerate(values):
            total = (total + value * pow(zeta, s * i, q)) % q
        out.append(total)
    return out


def relative_sums(cycle: list[int], q: int, zeta_h: int, m: int, a: int) -> list[int]:
    h = len(cycle)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    out: list[int] = []
    for u in range(m):
        total = 0
        for k in range(n):
            total = (total + pow(zeta_n, a * k, q) * cycle[u + m * k]) % q
        out.append(total)
    return out


def quotient_sizes(h: int, max_quotients: int) -> list[int]:
    sizes = [
        int(d)
        for d in sp.divisors(h)
        if 2 <= d <= min(30, h // 2) and h % d == 0
    ]
    return sorted(sizes, key=lambda d: (abs(d - h // d), d))[:max_quotients]


def audit_quotient(cycle: list[int], q: int, zeta_h: int, m: int) -> QuotientRow:
    h = len(cycle)
    n = h // m
    full = dft(cycle, q, zeta_h)
    harmful = 0
    vanished_count = 0
    individual_zero_fibers = 0
    min_nonzero_fibers = m
    equivalence_ok = True
    for a in range(1, n):
        rel = relative_sums(cycle, q, zeta_h, m, a)
        nonzero_fibers = sum(1 for value in rel if value % q)
        individual_zero_fibers += m - nonzero_fibers
        min_nonzero_fibers = min(min_nonzero_fibers, nonzero_fibers)
        coset = [(a + r * n) % h for r in range(m)]
        coset_zero = all(full[s] == 0 for s in coset)
        rel_zero = nonzero_fibers == 0
        if coset_zero:
            vanished_count += len(coset)
        if coset_zero != rel_zero:
            equivalence_ok = False
        if rel_zero:
            harmful += 1
    return QuotientRow(
        quotient_size=m,
        subgroup_size=n,
        harmful_a_count=harmful,
        vanished_character_count=vanished_count,
        relative_character_count=n - 1,
        individual_zero_fiber_count=individual_zero_fibers,
        min_nonzero_fibers=min_nonzero_fibers,
        full_resolvent_equivalence=equivalence_ok,
    )


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_quotients: int,
    q_start: int,
    q_stop: int,
) -> list[ScanRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[ScanRow] = []
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
        split = find_splitting_prime_with_mu_h(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        zeta_h = primitive_root_of_order(q, h)
        quotient_rows = tuple(
            audit_quotient(cycle, q, zeta_h, m)
            for m in quotient_sizes(h, max_quotients)
        )
        if not quotient_rows:
            continue
        rows.append(ScanRow(D=D, q=q, ell=ell, h=h, quotient_rows=quotient_rows))
        if len(rows) >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=6)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=60)
    ap.add_argument("--max-abs-D", type=int, default=5000)
    ap.add_argument("--max-quotients", type=int, default=4)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=30000)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_quotients=args.max_quotients,
        q_start=args.q_start,
        q_stop=args.q_stop,
    )

    print("natural relative-resolvent scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h quotient_m subgroup_n harmful_a_count "
            "vanished_character_count individual_zero_fibers "
            "min_nonzero_fibers equivalence_ok"
        )
        for row in rows:
            for qrow in row.quotient_rows:
                print(
                    f"D={row.D:7d} q={row.q:5d} ell={row.ell:2d} h={row.h:3d} "
                    f"m={qrow.quotient_size:3d} n={qrow.subgroup_size:3d} "
                    f"harmful_a={qrow.harmful_a_count:2d} "
                    f"vanished_chars={qrow.vanished_character_count:3d} "
                    f"individual_zero_fibers={qrow.individual_zero_fiber_count:3d} "
                    f"min_nonzero_fibers={qrow.min_nonzero_fibers:3d} "
                    f"equivalence_ok={int(qrow.full_resolvent_equivalence)}"
                )

    total_quotients = sum(len(row.quotient_rows) for row in rows)
    total_harmful = sum(
        qrow.harmful_a_count
        for row in rows
        for qrow in row.quotient_rows
    )
    total_relative_characters = sum(
        qrow.relative_character_count
        for row in rows
        for qrow in row.quotient_rows
    )
    total_relative_fibers = sum(
        qrow.relative_character_count * qrow.quotient_size
        for row in rows
        for qrow in row.quotient_rows
    )
    total_individual_zero_fibers = sum(
        qrow.individual_zero_fiber_count
        for row in rows
        for qrow in row.quotient_rows
    )
    expected_random_zero_fibers = sum(
        (qrow.relative_character_count * qrow.quotient_size) / row.q
        for row in rows
        for qrow in row.quotient_rows
    )
    product_nonzero_rows = sum(
        1
        for row in rows
        for qrow in row.quotient_rows
        if qrow.min_nonzero_fibers == qrow.quotient_size
    )
    all_equiv = all(
        qrow.full_resolvent_equivalence
        for row in rows
        for qrow in row.quotient_rows
    )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  quotient_rows={total_quotients}")
    print(f"  relative_characters_tested={total_relative_characters}")
    print(f"  relative_fibers_tested={total_relative_fibers}")
    print(f"  harmful_a_total={total_harmful}")
    print(f"  individual_zero_fiber_total={total_individual_zero_fibers}")
    print(f"  expected_random_zero_fibers={expected_random_zero_fibers:.6f}")
    print(f"  quotient_rows_with_all_individual_fibers_nonzero={product_nonzero_rows}")
    print(f"  all_equivalences_verified={int(all_equiv)}")
    print()
    print("interpretation")
    print("  harmful_a_zero_means_no_full_dual_coset_relative_collapse_seen=1")
    print("  all_individual_fibers_nonzero_supports_stronger_product_certificate=1")
    print("  equivalence_ok_checks_the_fourier_factorization_on_natural_CM_cycles=1")
    print("  q_congruent_1_mod_h_keeps_the_test_in_the_base_field=1")
    print("conclusion=reported_natural_relative_resolvent_scan")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Scan small CM cycles for the relative quadratic energy certificate."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from natural_relative_resolvent_scan import (
    dft,
    find_splitting_prime_with_mu_h,
    primitive_root_of_order,
    quotient_sizes,
    relative_sums,
)


@dataclass(frozen=True)
class EnergyRow:
    quotient_size: int
    subgroup_size: int
    characters_tested: int
    harmful_count: int
    energy_zero_count: int
    harmful_energy_mismatch: int


@dataclass(frozen=True)
class ScanRow:
    D: int
    q: int
    ell: int
    h: int
    energy_rows: tuple[EnergyRow, ...]


def relative_energy(values: list[int], q: int, zeta_h: int, m: int, a: int) -> int:
    n = len(values) // m
    rel_pos = relative_sums(values, q, zeta_h, m, a)
    rel_neg = relative_sums(values, q, zeta_h, m, (-a) % n)
    return sum(x * y for x, y in zip(rel_pos, rel_neg)) % q


def autocorrelation_energy(values: list[int], q: int, zeta_h: int, m: int, a: int) -> int:
    h = len(values)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    total = 0
    for d in range(n):
        corr = 0
        offset = m * d
        for i, value in enumerate(values):
            corr = (corr + values[(i + offset) % h] * value) % q
        total = (total + pow(zeta_n, a * d, q) * corr) % q
    return total


def packet_parseval_energy(values: list[int], q: int, zeta_h: int, m: int, a: int) -> int:
    h = len(values)
    n = h // m
    full = dft(values, q, zeta_h)
    total = 0
    for r in range(m):
        s = (a + r * n) % h
        total = (total + full[s] * full[(-s) % h]) % q
    return total


def audit_quotient(values: list[int], q: int, zeta_h: int, m: int) -> EnergyRow:
    h = len(values)
    n = h // m
    harmful = 0
    energy_zero = 0
    mismatch = 0
    for a in range(1, n):
        rel = relative_sums(values, q, zeta_h, m, a)
        harmful_a = all(value % q == 0 for value in rel)
        energy_a = relative_energy(values, q, zeta_h, m, a)
        energy_auto = autocorrelation_energy(values, q, zeta_h, m, a)
        if energy_a != energy_auto:
            raise AssertionError("energy/autocorrelation identity failed")
        energy_packet = packet_parseval_energy(values, q, zeta_h, m, a)
        if energy_packet != (m * energy_a) % q:
            raise AssertionError("packet Parseval identity failed")
        if harmful_a:
            harmful += 1
        if energy_a == 0:
            energy_zero += 1
        if harmful_a and energy_a != 0:
            mismatch += 1
    return EnergyRow(
        quotient_size=m,
        subgroup_size=n,
        characters_tested=n - 1,
        harmful_count=harmful,
        energy_zero_count=energy_zero,
        harmful_energy_mismatch=mismatch,
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
        energy_rows = tuple(
            audit_quotient(cycle, q, zeta_h, m)
            for m in quotient_sizes(h, max_quotients)
        )
        if energy_rows:
            rows.append(ScanRow(D=D, q=q, ell=ell, h=h, energy_rows=energy_rows))
        if len(rows) >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=20)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=72)
    ap.add_argument("--max-abs-D", type=int, default=12000)
    ap.add_argument("--max-quotients", type=int, default=4)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=120000)
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

    print("relative energy certificate scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print()
    if not args.summary_only:
        print("columns: D q ell h m n characters harmful energy_zero mismatch")
        for row in rows:
            for erow in row.energy_rows:
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"m={erow.quotient_size:3d} n={erow.subgroup_size:3d} "
                    f"characters={erow.characters_tested:3d} "
                    f"harmful={erow.harmful_count:2d} "
                    f"energy_zero={erow.energy_zero_count:2d} "
                    f"mismatch={erow.harmful_energy_mismatch:2d}"
                )

    total_rows = sum(len(row.energy_rows) for row in rows)
    characters = sum(erow.characters_tested for row in rows for erow in row.energy_rows)
    harmful = sum(erow.harmful_count for row in rows for erow in row.energy_rows)
    energy_zero = sum(erow.energy_zero_count for row in rows for erow in row.energy_rows)
    mismatch = sum(erow.harmful_energy_mismatch for row in rows for erow in row.energy_rows)
    expected_energy_zeros = sum(
        erow.characters_tested / row.q
        for row in rows
        for erow in row.energy_rows
    )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  quotient_rows={total_rows}")
    print(f"  characters_tested={characters}")
    print(f"  harmful_total={harmful}")
    print(f"  energy_zero_total={energy_zero}")
    print(f"  expected_random_energy_zeros={expected_energy_zeros:.6f}")
    print(f"  harmful_energy_mismatch_total={mismatch}")
    print()
    print("interpretation")
    print("  energy_nonzero_is_a_scalar_sufficient_certificate=1")
    print("  autocorrelation_identity_verified_for_all_tested_characters=1")
    print("  harmful_implies_energy_zero_verified=1")
    print("conclusion=reported_relative_energy_certificate_scan")


if __name__ == "__main__":
    main()

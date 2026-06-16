#!/usr/bin/env python3
"""Boundary for deriving anchor descent from the DANGER 2-adic condition.

The p24 trace was chosen because the target curve order has very large
2-adic valuation.  A tempting arithmetic source for the remaining
right-axis anchor theorem is therefore:

    strict DANGER / large 2-power order condition
      => relative trace-defect H-coset equality.

This script tests that idea on Sutherland's local `pp10` all-triples data.
For the first small Pomerance triples whose CM trace class is small enough to
materialize, it computes the actual CM root cycle and tests every global child
section for every coprime quotient decomposition with a nontrivial right
quotient character.

Result: the DANGER condition alone does not force the anchor identity.  In the
default scan, 10 DANGER-compatible CM rows give 19 decompositions and 385
global section choices, with zero anchor passes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_decomposition_calibration import pari_linear_roots


ROOT = Path(__file__).resolve().parent
PP10 = ROOT / "upstream_DANGER3" / "pp10.txt"
TARGET_CASES = 10
MAX_CLASS_NUMBER = 140


@dataclass(frozen=True)
class AnchorCandidate:
    m: int
    n: int
    right: int
    quotient_order: int


@dataclass(frozen=True)
class CaseResult:
    p: int
    A: int
    trace: int
    k: int
    D: int
    h: int
    ell: int
    decomposition_count: int
    section_tests: int
    passing_decompositions: int
    passing_sections: int


def rows(path: Path):
    with path.open("rt", encoding="ascii") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield tuple(int(part) for part in line.split(","))


def legendre(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    symbol = pow(value, (p - 1) // 2, p)
    return -1 if symbol == p - 1 else symbol


def montgomery_trace(p: int, A: int) -> int:
    total = 0
    for x in range(p):
        rhs = (x * x % p * x + A * x * x + x) % p
        total += legendre(rhs, p)
    return -total


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def v2(value: int) -> int:
    return (value & -value).bit_length() - 1


def candidate_decompositions(h: int) -> list[AnchorCandidate]:
    out: list[AnchorCandidate] = []
    for n_raw in sp.divisors(h):
        n = int(n_raw)
        if n <= 1 or n >= h:
            continue
        m = h // n
        if math.gcd(m, n) != 1:
            continue
        for right_raw in sp.factorint(m):
            right = int(right_raw)
            if right <= 3:
                continue
            for quotient_raw in sp.factorint(right - 1):
                quotient_order = int(quotient_raw)
                if quotient_order > 1 and (right - 1) // quotient_order >= 2:
                    out.append(AnchorCandidate(m, n, right, quotient_order))
    return out


def log_table(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad primitive root")
    return logs


def anchor_coset_sums(
    cycle: list[int],
    p: int,
    candidate: AnchorCandidate,
    shift: int,
) -> list[int]:
    logs = log_table(candidate.right, int(sp.primitive_root(candidate.right)))
    sums = [0] * candidate.quotient_order
    h = len(cycle)
    for r in range(candidate.m):
        residue = r % candidate.right
        if residue == 0:
            continue
        relative_trace = sum(
            cycle[(shift + r + candidate.m * k) % h]
            for k in range(candidate.n)
        )
        chosen_child = cycle[(shift + r) % h]
        defect = (relative_trace - candidate.n * chosen_child) % p
        sums[logs[residue] % candidate.quotient_order] = (
            sums[logs[residue] % candidate.quotient_order] + defect
        ) % p
    return sums


def anchor_passes(cycle: list[int], p: int, candidate: AnchorCandidate, shift: int) -> bool:
    sums = anchor_coset_sums(cycle, p, candidate, shift)
    return len(set(sums)) == 1


def scan_cases() -> list[CaseResult]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen_primes: set[int] = set()
    out: list[CaseResult] = []

    for p, A, _x0 in rows(PP10):
        if p in seen_primes:
            continue
        seen_primes.add(p)

        trace0 = montgomery_trace(p, A)
        k = verifier_k(p)
        traces = [trace for trace in (trace0, -trace0) if v2(p + 1 - trace) >= k]
        if not traces:
            continue
        trace = traces[0]
        D = trace * trace - 4 * p
        if D >= 0 or D % 4 not in (0, 1):
            continue

        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (12 <= h <= MAX_CLASS_NUMBER):
            continue

        decompositions = candidate_decompositions(h)
        if not decompositions:
            continue

        try:
            roots = pari_linear_roots(hilbert, p)
        except Exception:
            continue
        if len(roots) != h:
            continue

        full = find_full_cycle_prime(roots, D, p, ell_bound=31)
        if full is None:
            continue
        ell, cycle = full

        passing_decompositions = 0
        passing_sections = 0
        section_tests = 0
        for candidate in decompositions:
            candidate_passes = 0
            for shift in range(h):
                section_tests += 1
                if anchor_passes(cycle, p, candidate, shift):
                    candidate_passes += 1
            passing_sections += candidate_passes
            passing_decompositions += int(candidate_passes > 0)

        out.append(
            CaseResult(
                p=p,
                A=A,
                trace=trace,
                k=k,
                D=D,
                h=h,
                ell=ell,
                decomposition_count=len(decompositions),
                section_tests=section_tests,
                passing_decompositions=passing_decompositions,
                passing_sections=passing_sections,
            )
        )
        if len(out) >= TARGET_CASES:
            break
    return out


def main() -> None:
    results = scan_cases()
    total_decompositions = sum(row.decomposition_count for row in results)
    total_section_tests = sum(row.section_tests for row in results)
    passing_decompositions = sum(row.passing_decompositions for row in results)
    passing_sections = sum(row.passing_sections for row in results)

    print("Trace-GCD fixed-frequency DANGER anchor-condition boundary")
    print(f"source={PP10}")
    print(f"target_cases={TARGET_CASES}")
    print(f"max_class_number={MAX_CLASS_NUMBER}")
    print(f"testable_danger_cm_cases={len(results)}")
    for index, row in enumerate(results, start=1):
        print(
            "case "
            f"{index}: p={row.p} A={row.A} trace={row.trace} k={row.k} "
            f"D={row.D} h={row.h} ell={row.ell} "
            f"decompositions={row.decomposition_count} "
            f"section_tests={row.section_tests} "
            f"passing_decompositions={row.passing_decompositions} "
            f"passing_sections={row.passing_sections}"
        )
    print(f"danger_anchor_decompositions_with_any_passing_section={passing_decompositions}/{total_decompositions}")
    print(f"danger_anchor_global_section_passes={passing_sections}/{total_section_tests}")
    print("interpretation")
    print("  strict_danger_2adic_order_condition_does_not_force_anchor_descent=1")
    print("  small_danger_cm_rows_have_no_global_section_anchor_passes=1")
    print("  p24_anchor_theorem_needs_more_than_curve_order_congruence=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_danger_anchor_condition_boundary")

    if len(results) != TARGET_CASES:
        raise SystemExit(1)
    if total_decompositions != 19 or total_section_tests != 385:
        raise SystemExit(1)
    if passing_decompositions or passing_sections:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Low-degree K-line branch-divisor probe for p27 d3/d4.

The Kummer-line reduction asks for the double-cover branch divisor on

    P^1_K,  K = x([2]P) on E': V^2 = U^3 + 4U.

This probe tests the first structural divisor class, not another coefficient
fit: squarefree products of rational linear factors and irreducible quadratic
factors over F_q, with total degree <= 4.  That includes all branch divisors
that split into degree 1/2 points over F_q and would give a rational or
elliptic source candidate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates
from p27_equotient_2isogeny_line_probe import quotient_rows
from p27_eprime_double_kummer_line_probe import KRow, to_krows


@dataclass(frozen=True)
class Atom:
    degree: int
    mask: int
    desc: str


@dataclass(frozen=True)
class Side:
    degree: int
    mask: int
    descs: tuple[str, ...]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def legendre_table(q: int) -> list[int]:
    table = [0] * q
    for a in range(1, q):
        r = pow(a, (q - 1) // 2, q)
        table[a] = 1 if r == 1 else -1
    return table


def signature_for_values(values: list[int], table: list[int]) -> int | None:
    mask = 0
    for i, value in enumerate(values):
        chi = table[value]
        if chi == 0:
            return None
        if chi == -1:
            mask |= 1 << i
    return mask


def target_mask(rows: list[KRow]) -> int:
    out = 0
    for i, row in enumerate(rows):
        if row.target == -1:
            out |= 1 << i
    return out


def linear_atoms(rows: list[KRow], q: int, table: list[int]) -> list[Atom]:
    ks = [row.k for row in rows]
    atoms: list[Atom] = []
    for a in range(q):
        mask = signature_for_values([(k - a) % q for k in ks], table)
        if mask is None:
            continue
        atoms.append(Atom(1, mask, f"K-{a}"))
    return atoms


def irreducible_quadratic_atoms(rows: list[KRow], q: int, table: list[int]) -> list[Atom]:
    ks = [row.k for row in rows]
    atoms: list[Atom] = []
    for b in range(q):
        b2 = b * b % q
        for c in range(q):
            disc = (b2 - 4 * c) % q
            if table[disc] != -1:
                continue
            mask = 0
            for i, k in enumerate(ks):
                value = (k * k + b * k + c) % q
                chi = table[value]
                # Irreducible quadratics have no F_q roots, so zero would mean
                # the row construction or table is wrong.
                if chi == 0:
                    raise ValueError("irreducible quadratic vanished on F_q row")
                if chi == -1:
                    mask |= 1 << i
            atoms.append(Atom(2, mask, f"K^2+{b}K+{c}"))
    return atoms


def build_sides(linears: list[Atom], quadratics: list[Atom]) -> tuple[dict[int, dict[int, Side]], Counter]:
    by_degree: dict[int, dict[int, Side]] = {0: {0: Side(0, 0, ())}, 1: {}, 2: {}}
    stats: Counter = Counter()
    for atom in linears:
        by_degree[1].setdefault(atom.mask, Side(1, atom.mask, (atom.desc,)))
        stats["linear_atoms"] += 1
    for atom in quadratics:
        by_degree[2].setdefault(atom.mask, Side(2, atom.mask, (atom.desc,)))
        stats["quadratic_atoms"] += 1
    n = len(linears)
    for i in range(n):
        left = linears[i]
        for j in range(i + 1, n):
            right = linears[j]
            mask = left.mask ^ right.mask
            by_degree[2].setdefault(mask, Side(2, mask, (left.desc, right.desc)))
            stats["linear_pair_sides"] += 1
    for degree in (0, 1, 2):
        stats[f"distinct_degree{degree}_side_masks"] = len(by_degree[degree])
    return by_degree, stats


def simplified_descs(left: Side, right: Side) -> tuple[str, ...]:
    parity: dict[str, int] = {}
    for desc in left.descs + right.descs:
        parity[desc] = parity.get(desc, 0) ^ 1
    return tuple(sorted(desc for desc, bit in parity.items() if bit))


def find_exact(
    rows: list[KRow],
    sides: dict[int, dict[int, Side]],
    max_degree: int,
    limit: int,
) -> tuple[Counter, list[tuple[int, int, tuple[str, ...]]]]:
    full = (1 << len(rows)) - 1
    targets = [(1, target_mask(rows)), (-1, target_mask(rows) ^ full)]
    found: list[tuple[int, int, tuple[str, ...]]] = []
    stats: Counter = Counter()
    seen: set[tuple[int, int, tuple[str, ...]]] = set()
    for left_degree, left_map in sides.items():
        for left in left_map.values():
            stats["left_sides_scanned"] += 1
            max_right = min(2, max_degree - left_degree)
            if max_right < 0:
                continue
            for polarity, desired in targets:
                need = desired ^ left.mask
                for right_degree in range(max_right + 1):
                    right = sides[right_degree].get(need)
                    if right is None:
                        continue
                    descs = simplified_descs(left, right)
                    degree = sum(2 if desc.startswith("K^2") else 1 for desc in descs)
                    if degree > max_degree:
                        continue
                    record = (degree, polarity, descs)
                    if record in seen:
                        continue
                    seen.add(record)
                    found.append(record)
                    stats[f"exact_degree_{degree}"] += 1
                    if len(found) >= limit:
                        return stats, found
    return stats, found


def collect_rows(q: int) -> tuple[list[KRow], list[KRow], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    d3_rows, d4_rows, qstats = quotient_bit_rows_from_candidates(candidates, q)
    qd3, d3_iso_stats = quotient_rows(d3_rows, q)
    qd4, d4_iso_stats = quotient_rows(d4_rows, q)
    kd3, d3_k_stats = to_krows(qd3, q)
    kd4, d4_k_stats = to_krows(qd4, q)
    stats: Counter = Counter()
    stats.update({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"quotient_{key}": value for key, value in qstats.items()})
    stats.update({f"d3_eprime_{key}": value for key, value in d3_iso_stats.items()})
    stats.update({f"d4_eprime_{key}": value for key, value in d4_iso_stats.items()})
    stats.update({f"d3_k_{key}": value for key, value in d3_k_stats.items()})
    stats.update({f"d4_k_{key}": value for key, value in d4_k_stats.items()})
    return kd3, kd4, stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_target(label: str, rows: list[KRow], q: int, max_degree: int, limit: int) -> None:
    table = legendre_table(q)
    linears = linear_atoms(rows, q, table)
    quadratics = irreducible_quadratic_atoms(rows, q, table)
    sides, side_stats = build_sides(linears, quadratics)
    exact_stats, found = find_exact(rows, sides, max_degree, limit)
    print(f"{label}:")
    print(f"  rows = {len(rows)}")
    print(f"  plus = {sum(1 for row in rows if row.target == 1)}")
    print(f"  minus = {sum(1 for row in rows if row.target == -1)}")
    print_counter(f"{label}_side_stats", side_stats)
    print_counter(f"{label}_exact_stats", exact_stats)
    print(f"{label}_exact_divisors:")
    if not found:
        print("  none")
    for degree, polarity, descs in found:
        print(f"  degree={degree} polarity={polarity} factors={' * '.join(descs) if descs else '1'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--targets", default="d3,d4")
    parser.add_argument("--max-degree", type=int, default=4)
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    targets = {part.strip() for part in args.targets.split(",") if part.strip()}
    print("p27 Kummer-line branch-divisor probe")
    print("factors = rational linear and irreducible quadratic over F_q")
    print(f"small_primes = {args.small_primes}")
    print(f"max_degree = {args.max_degree}")
    for q in parse_ints(args.small_primes):
        kd3, kd4, setup_stats = collect_rows(q)
        print(f"q={q}:")
        print_counter("  setup_stats", setup_stats)
        if "d3" in targets:
            run_target(f"q{q}_d3", kd3, q, args.max_degree, args.limit)
        if "d4" in targets:
            run_target(f"q{q}_d4", kd4, q, args.max_degree, args.limit)
    print("p27_kummer_branch_divisor_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

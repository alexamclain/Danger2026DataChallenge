#!/usr/bin/env python3
"""Guard-field signature audit for p27 K/S finite-field probes.

p = 10^27+103 is 7 mod 16, so v2(p+1)=3.  Several small fields used for quick
screens are only 7 mod 8, and q=15 mod 16 has v2(q+1)>=4.  This probe checks
whether the K/S artifacts that looked tempting, especially d4 constants and
K -> 4/K closures, correlate with that extra 2-adic layer.

The purpose is methodological: choose promotion fields that match the p27
2-adic sign regime before treating finite-field exactness as structure.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from p27_k_belyi_involution_probe import collect_rows, k_transforms, transform_stats


P27 = 10**27 + 103


@dataclass(frozen=True)
class FieldRow:
    q: int
    q_mod16: int
    v2_q_plus_1: int
    d3_rows: int
    d3_plus: int
    d3_minus: int
    d4_rows: int
    d4_plus: int
    d4_minus: int
    d3_k4_present: int
    d3_k4_same: int
    d3_k4_opposite: int
    d3_k4_missing: int
    d4_k4_present: int
    d4_k4_same: int
    d4_k4_opposite: int
    d4_k4_missing: int


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def default_primes(min_q: int, max_q: int) -> list[int]:
    return [q for q in range(min_q, max_q + 1) if q % 8 == 7 and is_prime(q)]


def target_counts(values: list[int]) -> tuple[int, int]:
    return sum(1 for value in values if value == 1), sum(1 for value in values if value == -1)


def get_transform(stats: Counter, name: str, key: str) -> int:
    return int(stats.get(f"{name}_{key}", 0))


def analyze_field(q: int) -> FieldRow:
    kd3, kd4, _sd3, _sd4, _setup = collect_rows(q)
    d3_values = [row.target for row in kd3]
    d4_values = [row.target for row in kd4]
    d3_plus, d3_minus = target_counts(d3_values)
    d4_plus, d4_minus = target_counts(d4_values)
    d3_t = transform_stats({row.k: row.target for row in kd3}, q, k_transforms())
    d4_t = transform_stats({row.k: row.target for row in kd4}, q, k_transforms())
    return FieldRow(
        q=q,
        q_mod16=q % 16,
        v2_q_plus_1=v2(q + 1),
        d3_rows=len(kd3),
        d3_plus=d3_plus,
        d3_minus=d3_minus,
        d4_rows=len(kd4),
        d4_plus=d4_plus,
        d4_minus=d4_minus,
        d3_k4_present=get_transform(d3_t, "4/K", "present"),
        d3_k4_same=get_transform(d3_t, "4/K", "same"),
        d3_k4_opposite=get_transform(d3_t, "4/K", "opposite"),
        d3_k4_missing=get_transform(d3_t, "4/K", "missing"),
        d4_k4_present=get_transform(d4_t, "4/K", "present"),
        d4_k4_same=get_transform(d4_t, "4/K", "same"),
        d4_k4_opposite=get_transform(d4_t, "4/K", "opposite"),
        d4_k4_missing=get_transform(d4_t, "4/K", "missing"),
    )


def row_flags(row: FieldRow) -> list[str]:
    flags: list[str] = []
    if row.d4_rows and (row.d4_plus == 0 or row.d4_minus == 0):
        flags.append("d4_constant")
    if row.d3_rows and row.d3_k4_present == row.d3_rows:
        if row.d3_k4_same == row.d3_rows:
            flags.append("d3_4K_full_same")
        elif row.d3_k4_opposite == row.d3_rows:
            flags.append("d3_4K_full_opposite")
        else:
            flags.append("d3_4K_full_mixed")
    elif row.d3_rows and row.d3_k4_present == 0:
        flags.append("d3_4K_absent")
    else:
        flags.append("d3_4K_partial")
    if row.d4_rows and row.d4_k4_present == row.d4_rows:
        if row.d4_k4_same == row.d4_rows:
            flags.append("d4_4K_full_same")
        elif row.d4_k4_opposite == row.d4_rows:
            flags.append("d4_4K_full_opposite")
        else:
            flags.append("d4_4K_full_mixed")
    elif row.d4_rows and row.d4_k4_present == 0:
        flags.append("d4_4K_absent")
    else:
        flags.append("d4_4K_partial")
    return flags


def print_row(row: FieldRow) -> None:
    print(
        "field "
        f"q={row.q} q_mod16={row.q_mod16} v2_q_plus_1={row.v2_q_plus_1} "
        f"d3={row.d3_plus}/{row.d3_rows} d4={row.d4_plus}/{row.d4_rows} "
        f"d3_4K=present:{row.d3_k4_present} same:{row.d3_k4_same} "
        f"opp:{row.d3_k4_opposite} miss:{row.d3_k4_missing} "
        f"d4_4K=present:{row.d4_k4_present} same:{row.d4_k4_same} "
        f"opp:{row.d4_k4_opposite} miss:{row.d4_k4_missing} "
        f"flags={','.join(row_flags(row))}"
    )


def print_summary(rows: list[FieldRow]) -> None:
    for mod16 in [7, 15]:
        group = [row for row in rows if row.q_mod16 == mod16]
        stats: Counter = Counter()
        for row in group:
            stats["fields"] += 1
            for flag in row_flags(row):
                stats[flag] += 1
            stats["d4_nonconstant"] += int(row.d4_plus > 0 and row.d4_minus > 0)
            stats["total_d3_rows"] += row.d3_rows
            stats["total_d4_rows"] += row.d4_rows
        print(f"summary q_mod16={mod16}:")
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-q", type=int, default=607)
    parser.add_argument("--max-q", type=int, default=5000)
    parser.add_argument("--primes", default="")
    args = parser.parse_args()

    primes = parse_ints(args.primes) if args.primes.strip() else default_primes(args.min_q, args.max_q)
    print("p27 guard-field signature probe")
    print(f"p27_mod16 = {P27 % 16}")
    print(f"p27_v2_p_plus_1 = {v2(P27 + 1)}")
    print(f"fields = {len(primes)}")
    rows = [analyze_field(q) for q in primes]
    for row in rows:
        print_row(row)
    print_summary(rows)
    print("p27_guard_field_signature_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

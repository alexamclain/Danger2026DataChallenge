#!/usr/bin/env python3
"""U-line divisor screen for the H90-soluble Dplus U6 row bit.

The H90-solubility boundary says Ktrace square/zero gives a uniform row-bit
t-fiber.  Since the row bit is also invariant under w -> -w, the next cheap
question is whether the soluble-side sign descends to the even elliptic
coordinate

    a = t - 1/t
    u = 4/a^2

on E: v^2 = u^3 - u.  If it descends to u and is a small polynomial divisor
chi(P(u)), that would be a concrete sourceable handle.  If it is mixed over u
or has no low-degree divisor, the lane stays in non-visible Prym/theta territory.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path

from p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe import (
    chi,
    h90_values,
    inv,
    parse_fields,
    row_signs_for_t,
    sign_name,
)


@dataclass(frozen=True)
class Hit:
    degree: int
    polarity: int
    coeffs: tuple[int, ...]


def normalize_signs(values: list[int]) -> int | None:
    signs = {value for value in values if value in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def u_from_t(t: int, q: int) -> int | None:
    a = (t - inv(t, q)) % q
    if a == 0:
        return None
    return 4 * inv(a * a, q) % q


def collect_u_rows(q: int, materialization_filters: bool) -> tuple[list[tuple[int, int]], Counter[str]]:
    stats: Counter[str] = Counter()
    by_u: defaultdict[int, list[int]] = defaultdict(list)
    for t in range(1, q):
        signs = row_signs_for_t(t, q, materialization_filters)
        target = normalize_signs(signs)
        if target is None:
            stats["empty_t"] += 1
            continue
        if target == 0:
            stats["mixed_t_skipped"] += 1
            continue
        _B, _C, _Fspin, Ktrace = h90_values(t, q)
        if chi(Ktrace, q) == -1:
            stats["h90_insoluble_uniform_unexpected"] += 1
            continue
        u = u_from_t(t, q)
        if u is None:
            stats["u_undefined"] += 1
            continue
        by_u[u].append(target)
        stats["soluble_uniform_t"] += 1
        stats[f"soluble_uniform_t_{sign_name(target)}"] += 1

    rows: list[tuple[int, int]] = []
    for u, targets in sorted(by_u.items()):
        stats["u_groups"] += 1
        stats[f"u_group_size_{len(targets)}"] += 1
        sign = normalize_signs(targets)
        if sign in (-1, 1):
            rows.append((u, sign))
            stats[f"u_uniform_{sign_name(sign)}"] += 1
        elif sign == 0:
            stats["u_mixed"] += 1
            stats["u_mixed_rows"] += len(targets)
        else:
            stats["u_empty"] += 1

    stats["u_rows"] = len(rows)
    stats["u_rows_plus"] = sum(1 for _u, target in rows if target == 1)
    stats["u_rows_minus"] = sum(1 for _u, target in rows if target == -1)
    stats["both_signs_present"] = int(stats["u_rows_plus"] > 0 and stats["u_rows_minus"] > 0)
    return rows, stats


def residue_table(q: int) -> bytearray:
    table = bytearray(q)
    for x in range(1, q):
        table[x * x % q] = 1
    return table


def match_value(value: int, target: int, polarity: int, residues: bytearray, q: int) -> bool:
    value %= q
    if value == 0:
        return False
    sign = 1 if residues[value] else -1
    return sign == polarity * target


def scan_degree1(rows: list[tuple[int, int]], q: int, residues: bytearray) -> list[Hit]:
    hits: list[Hit] = []
    for c in range(q):
        for polarity in (1, -1):
            if all(match_value(u + c, target, polarity, residues, q) for u, target in rows):
                hits.append(Hit(1, polarity, (c,)))
    return hits


def scan_degree2(rows: list[tuple[int, int]], q: int, residues: bytearray) -> list[Hit]:
    hits: list[Hit] = []
    for b in range(q):
        for c in range(q):
            for polarity in (1, -1):
                ok = True
                for u, target in rows:
                    if not match_value(u * u + b * u + c, target, polarity, residues, q):
                        ok = False
                        break
                if ok:
                    hits.append(Hit(2, polarity, (b, c)))
    return hits


def score_best_linear(rows: list[tuple[int, int]], q: int, residues: bytearray) -> Counter[str]:
    stats: Counter[str] = Counter()
    for c in range(q):
        for polarity in (1, -1):
            matches = 0
            zeros = 0
            for u, target in rows:
                value = (u + c) % q
                if value == 0:
                    zeros += 1
                    continue
                sign = 1 if residues[value] else -1
                matches += int(sign == polarity * target)
            if matches > stats["best_matches"]:
                stats["best_matches"] = matches
                stats["best_zeros"] = zeros
                stats["best_polarity"] = polarity
                stats["best_c"] = c
    stats["best_total"] = len(rows)
    if rows:
        stats["best_x1000000"] = stats["best_matches"] * 1_000_000 // len(rows)
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(label: str, hits: list[Hit], keep: int) -> None:
    print(f"{label}:")
    if not hits:
        print("  none")
        return
    for hit in hits[:keep]:
        coeffs = ",".join(str(c) for c in hit.coeffs)
        print(f"  degree={hit.degree} polarity={hit.polarity} coeffs={coeffs}")


def fixture_packet(fields: list[int]) -> dict[str, object]:
    targets = []
    for q in fields:
        rows, stats = collect_u_rows(q, materialization_filters=True)
        targets.append(
            {
                "field": q,
                "coordinate": "u",
                "family": "dplus_h90_soluble_rowbit_u",
                "row_count": len(rows),
                "plus_count": stats["u_rows_plus"],
                "minus_count": stats["u_rows_minus"],
                "u_mixed_groups": stats["u_mixed"],
                "materialization_filters": True,
                "rows": [{"u": u, "sign": target} for u, target in rows],
            }
        )
    return {
        "name": "p27_dplus_rowbit_u_divisor_targets",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "Exact finite-field target rows for testing whether the "
            "H90-soluble Dplus U6 row bit is chi(P(u)) for a monic cubic, "
            "quartic, or other named low-degree divisor on E: v^2=u^3-u."
        ),
        "known_results": {
            "u_descent": "zero mixed u groups in tested fields",
            "degree_1_exact": 0,
            "degree_2_exact": 0,
            "next_gpu_tests": [
                "monic cubic exact support in q1847 and q2087",
                "monic quartic exact support in q1847 and q2087",
            ],
        },
        "polynomial_family": {
            "degree_3": "u^3 + a*u^2 + b*u + c",
            "degree_4": "u^4 + a*u^3 + b*u^2 + c*u + d",
            "accept": "chi(P(u)) = polarity * sign for every listed row, with no zero evaluations",
        },
        "targets": targets,
    }


def run_field(q: int, degree: int, materialization_filters: bool, top: int) -> Counter[str]:
    rows, stats = collect_u_rows(q, materialization_filters)
    print_counter(f"q{q}", stats)
    if stats["u_mixed"]:
        print(f"q{q}_screen:")
        print("  skipped = u_mixed")
        return stats
    if not stats["both_signs_present"]:
        print(f"q{q}_screen:")
        print("  skipped = one_sign_only")
        return stats

    residues = residue_table(q)
    best_linear = score_best_linear(rows, q, residues)
    print_counter(f"q{q}_linear_best", best_linear)

    degree1_hits = scan_degree1(rows, q, residues)
    stats["degree1_exact"] = len(degree1_hits)
    print_hits(f"q{q}_degree1_hits", degree1_hits, top)

    degree2_hits: list[Hit] = []
    if degree >= 2:
        degree2_hits = scan_degree2(rows, q, residues)
        stats["degree2_exact"] = len(degree2_hits)
        print_hits(f"q{q}_degree2_hits", degree2_hits, top)

    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="263,607,1607,1847,2087")
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--include-bare", action="store_true")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    print("p27 trace/norm Dplus U6 row-bit H90 u-divisor probe")
    print("question = does the H90-soluble row bit descend to a low-degree u divisor?")
    print(f"fields = {','.join(str(q) for q in fields)}")
    print(f"degree = {args.degree}")

    aggregate: Counter[str] = Counter()
    for materialization_filters in ([True, False] if args.include_bare else [True]):
        print(f"materialization_filters = {int(materialization_filters)}")
        for q in fields:
            stats = run_field(q, args.degree, materialization_filters, args.top)
            for key in ("u_mixed", "degree1_exact", "degree2_exact", "both_signs_present"):
                aggregate[key] += stats[key]

    print_counter("aggregate", aggregate)
    if args.json_out:
        packet = fixture_packet(fields)
        Path(args.json_out).write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
        print(f"json_out = {args.json_out}")
    print("verdict:")
    print("  u_mixed kills descent to the even elliptic coordinate")
    print("  exact low-degree hits promote a divisor/source candidate")
    print("  no exact hits keeps the row bit in non-visible Prym/theta territory")
    print("p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

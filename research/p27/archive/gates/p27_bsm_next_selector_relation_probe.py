#!/usr/bin/env python3
"""Next-selector relation screen on the legal-B-restricted BSM surface.

The first BSM relation probe showed that the staged surface

    m^2*(B^2+s^2-4) = 4*s^2*(s^2-4)

captures canonical d3-plus rows but does not add a low-degree target relation
beyond the inherited surface equation.  A sqrt-beating BSM route would need
the same staged object to control more than one selected half-gate.  This
probe therefore asks whether d4-plus, after d3-plus, satisfies an additional
low-degree relation in the same coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Optional

from p27_b_source_descent_probe import source_b_plus
from p27_bsm_surface_incidence_probe import parse_ints, strict_single
from p27_bsm_legal_restricted_relation_probe import (
    PAIR_SYSTEMS,
    TRIPLE_SYSTEMS,
    empty_stats,
    transformed_points,
)
from p27_conic_pair_invariant_relation_probe import System, relation_stats_for_system
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, sqrt_table
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits, normalize


def legal_b_selector_data(p: int) -> tuple[dict[str, set[tuple[int, int] | tuple[int, int, int]]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    by_ax_d3: defaultdict[tuple[int, int], list[Optional[int]]] = defaultdict(list)
    by_ax_d4: defaultdict[tuple[int, int], list[Optional[int]]] = defaultdict(list)
    by_ax_b: defaultdict[tuple[int, int], list[Optional[int]]] = defaultdict(list)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in candidates:
        key = (int(cand["A"]) % p, int(cand["x5"]) % p)
        bits = candidate_bits(cand, p)
        by_ax_d3[key].append(bits.d3)
        by_ax_d4[key].append(bits.d4)
        by_ax_b[key].append(source_b_plus(int(cand["X"]) % p, p))

    legal_b: set[int] = set()
    legal_bax: set[tuple[int, int, int]] = set()
    d3plus_bax: set[tuple[int, int, int]] = set()
    d4plus_bax: set[tuple[int, int, int]] = set()
    d4minus_bax: set[tuple[int, int, int]] = set()

    for (A, x), d3_values in by_ax_d3.items():
        B = strict_single(by_ax_b[(A, x)])
        d3 = normalize(d3_values)
        d4 = normalize(by_ax_d4[(A, x)])
        if B is None:
            stats["mixed_or_missing_B"] += 1
            continue
        legal_b.add(B)
        bax = (B, A, x)
        legal_bax.add(bax)
        if d3 == 1:
            d3plus_bax.add(bax)
            if d4 == 1:
                d4plus_bax.add(bax)
            elif d4 == -1:
                d4minus_bax.add(bax)
            elif d4 == 0:
                stats["mixed_d4_after_d3_ax"] += 1
            else:
                stats["missing_d4_after_d3_ax"] += 1
        elif d3 == 0:
            stats["mixed_d3_ax"] += 1
        elif d3 is None:
            stats["missing_d3_ax"] += 1

    stats["legal_B"] = len(legal_b)
    stats["legal_bax"] = len(legal_bax)
    stats["d3plus_bax"] = len(d3plus_bax)
    stats["d4plus_bax"] = len(d4plus_bax)
    stats["d4minus_bax"] = len(d4minus_bax)
    return {
        "legal_b": {(B, 0) for B in legal_b},
        "legal_bax": legal_bax,
        "d3plus_bax": d3plus_bax,
        "d4plus_bax": d4plus_bax,
        "d4minus_bax": d4minus_bax,
    }, stats


def bsm_selector_rows(p: int) -> tuple[list[dict[str, int]], dict[str, list[dict[str, int]]], Counter]:
    roots = sqrt_table(p)
    invs = inv_table(p)
    data, data_stats = legal_b_selector_data(p)
    legal_b = {B for B, _ in data["legal_b"]}  # type: ignore[misc]
    targets = {
        "d3plus": data["d3plus_bax"],
        "d4plus_after_d3": data["d4plus_bax"],
        "d4minus_after_d3": data["d4minus_bax"],
    }
    stats: Counter = Counter({f"data_{key}": value for key, value in data_stats.items()})
    inv16 = invs[16 % p]

    legal_rows: list[dict[str, int]] = []
    target_rows: dict[str, list[dict[str, int]]] = {key: [] for key in targets}
    per_b_target: dict[str, Counter] = {key: Counter() for key in targets}
    per_b_surface: Counter = Counter()

    for B in sorted(legal_b):
        B2 = B * B % p
        for s in range(p):
            s2 = s * s % p
            den = (B2 + s2 - 4) % p
            rhs = 4 * s2 % p * ((s2 - 4) % p) % p
            if den == 0:
                if rhs == 0:
                    stats["degenerate_all_m_pairs"] += 1
                else:
                    stats["inconsistent_den0_pairs"] += 1
                continue
            m2 = rhs * invs[den] % p
            for m in roots[m2]:
                if m == 0:
                    stats["skip_m0"] += 1
                    continue
                row = {"B": B, "s": s, "m": m}
                legal_rows.append(row)
                per_b_surface[B] += 1
                A = (B2 - 2) % p
                x = m * m % p * inv16 % p
                bax = (B, A, x)
                for label, target in targets.items():
                    if bax in target:
                        target_rows[label].append(row)
                        per_b_target[label][B] += 1

    stats["legal_surface_rows"] = len(legal_rows)
    for label, rows in target_rows.items():
        stats[f"{label}_rows"] = len(rows)
        stats[f"{label}_B"] = len(per_b_target[label])
        for value, count in Counter(per_b_target[label].values()).items():
            stats[f"{label}_rows_per_B_{value}"] = count
    for value, count in Counter(per_b_surface.values()).items():
        stats[f"surface_rows_per_B_{value}"] = count
    return legal_rows, target_rows, stats


def safe_relation_stats(points: list[tuple[int, ...]], p: int, degrees: list[int]) -> Counter:
    if not points:
        return empty_stats(degrees)
    return relation_stats_for_system(points, p, degrees)


def compare_targets(
    label: str,
    p: int,
    legal_rows: list[dict[str, int]],
    target_rows: dict[str, list[dict[str, int]]],
    system: System,
    degrees: list[int],
) -> None:
    legal_points = transformed_points(legal_rows, system)
    legal_stats = safe_relation_stats(legal_points, p, degrees)
    target_stats = {
        name: safe_relation_stats(transformed_points(rows, system), p, degrees)
        for name, rows in target_rows.items()
    }
    print(f"{label}_{system.name}:")
    print(f"  legal_rows = {len(legal_points)}")
    print(f"  legal_unique = {len(set(legal_points))}")
    for name, rows in target_rows.items():
        points = transformed_points(rows, system)
        print(f"  {name}_rows = {len(points)}")
        print(f"  {name}_unique = {len(set(points))}")
    for degree in degrees:
        prefix = f"deg{degree}"
        legal_extra = legal_stats[f"{prefix}_extra_nullity"]
        d3_extra = target_stats["d3plus"][f"{prefix}_extra_nullity"]
        d4p_extra = target_stats["d4plus_after_d3"][f"{prefix}_extra_nullity"]
        d4m_extra = target_stats["d4minus_after_d3"][f"{prefix}_extra_nullity"]
        print(
            "  "
            f"{prefix}: legal_extra={legal_extra} "
            f"d3_extra={d3_extra} d3_minus_legal={d3_extra - legal_extra} "
            f"d4plus_extra={d4p_extra} d4plus_minus_d3={d4p_extra - d3_extra} "
            f"d4minus_extra={d4m_extra} d4minus_minus_d3={d4m_extra - d3_extra}"
        )


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="2,4,6,8,10,12")
    parser.add_argument("--triple-degrees", default="2,4")
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees)
    triple_degrees = parse_ints(args.triple_degrees)
    print("p27 BSM next-selector relation probe")
    print("legal surface = BSM surface with B in legal B-domain")
    print("targets = d3plus, d4plus_after_d3, d4minus_after_d3")
    print(f"pair_degrees = {pair_degrees}")
    print(f"triple_degrees = {triple_degrees}")
    for p in parse_ints(args.small_primes):
        legal_rows, target_rows, stats = bsm_selector_rows(p)
        print_counter(f"q{p}_base", stats)
        for system in PAIR_SYSTEMS:
            compare_targets(f"q{p}", p, legal_rows, target_rows, system, pair_degrees)
        for system in TRIPLE_SYSTEMS:
            compare_targets(f"q{p}", p, legal_rows, target_rows, system, triple_degrees)
    print("p27_bsm_next_selector_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

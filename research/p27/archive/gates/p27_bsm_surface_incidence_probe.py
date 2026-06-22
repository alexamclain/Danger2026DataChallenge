#!/usr/bin/env python3
"""Incidence of the staged (B,s,m) conic-pullback surface.

The B-enhanced pullback found the stable equation

    m^2*(B^2+s^2-4) = 4*s^2*(s^2-4).

This probe treats that equation as a source surface and asks how often it hits
the actual legal label-2 / compactD / d3-plus rows.  A below-sqrt source would
need better than constant/q incidence after accounting for source size.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Optional

from p27_b_source_descent_probe import source_b_plus
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, legal_sets, sqrt_table
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits, normalize


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def strict_single(values: list[Optional[int]]) -> Optional[int]:
    vals = {value for value in values if value is not None}
    if len(vals) != 1:
        return None
    return vals.pop()


def legal_b_data(p: int) -> tuple[dict[str, set[tuple[int, int] | tuple[int, int, int]]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(p)
    by_ax_bits: defaultdict[tuple[int, int], list[Optional[int]]] = defaultdict(list)
    by_ax_b: defaultdict[tuple[int, int], list[Optional[int]]] = defaultdict(list)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in candidates:
        key = (int(cand["A"]) % p, int(cand["x5"]) % p)
        bits = candidate_bits(cand, p)
        by_ax_bits[key].append(bits.d3)
        by_ax_b[key].append(source_b_plus(int(cand["X"]) % p, p))

    legal_ax: set[tuple[int, int]] = set()
    d3plus_ax: set[tuple[int, int]] = set()
    d3minus_ax: set[tuple[int, int]] = set()
    legal_bax: set[tuple[int, int, int]] = set()
    d3plus_bax: set[tuple[int, int, int]] = set()
    d3minus_bax: set[tuple[int, int, int]] = set()
    legal_b: set[int] = set()
    d3plus_b: set[int] = set()

    for (A, x), bits in by_ax_bits.items():
        B = strict_single(by_ax_b[(A, x)])
        d3 = normalize(bits)
        legal_ax.add((A, x))
        if B is None:
            stats["mixed_or_missing_B"] += 1
            continue
        legal_b.add(B)
        legal_bax.add((B, A, x))
        if d3 == 1:
            d3plus_ax.add((A, x))
            d3plus_b.add(B)
            d3plus_bax.add((B, A, x))
        elif d3 == -1:
            d3minus_ax.add((A, x))
            d3minus_bax.add((B, A, x))
        elif d3 == 0:
            stats["mixed_d3_ax"] += 1
        else:
            stats["missing_d3_ax"] += 1

    stats["legal_ax"] = len(legal_ax)
    stats["d3plus_ax"] = len(d3plus_ax)
    stats["d3minus_ax"] = len(d3minus_ax)
    stats["legal_b"] = len(legal_b)
    stats["d3plus_b"] = len(d3plus_b)

    data: dict[str, set[tuple[int, int] | tuple[int, int, int]]] = {
        "legal_ax": legal_ax,
        "d3plus_ax": d3plus_ax,
        "d3minus_ax": d3minus_ax,
        "legal_bax": legal_bax,
        "d3plus_bax": d3plus_bax,
        "d3minus_bax": d3minus_bax,
        "legal_b": {(B, 0) for B in legal_b},
        "d3plus_b": {(B, 0) for B in d3plus_b},
    }
    return data, stats


def surface_incidence(p: int) -> Counter:
    roots = sqrt_table(p)
    invs = inv_table(p)
    data, data_stats = legal_b_data(p)
    stats: Counter = Counter({f"data_{key}": value for key, value in data_stats.items()})
    inv16 = invs[16 % p]
    legal_ax = data["legal_ax"]
    d3plus_ax = data["d3plus_ax"]
    d3minus_ax = data["d3minus_ax"]
    legal_bax = data["legal_bax"]
    d3plus_bax = data["d3plus_bax"]
    d3minus_bax = data["d3minus_bax"]
    legal_b = {B for B, _ in data["legal_b"]}  # type: ignore[misc]
    d3plus_b = {B for B, _ in data["d3plus_b"]}  # type: ignore[misc]

    unique_ax: set[tuple[int, int]] = set()
    unique_bax: set[tuple[int, int, int]] = set()
    unique_legal_ax: set[tuple[int, int]] = set()
    unique_d3plus_ax: set[tuple[int, int]] = set()
    unique_legal_bax: set[tuple[int, int, int]] = set()
    unique_d3plus_bax: set[tuple[int, int, int]] = set()

    for B in range(p):
        B2 = B * B % p
        if B in (0, 2 % p, (-2) % p):
            stats["skip_degenerate_B"] += 1
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
            m_roots = roots[m2]
            if not m_roots:
                stats["surface_no_m_root_pairs"] += 1
                continue
            for m in m_roots:
                if m == 0:
                    stats["skip_m0"] += 1
                    continue
                A = (B2 - 2) % p
                x = m * m % p * inv16 % p
                ax = (A, x)
                bax = (B, A, x)
                unique_ax.add(ax)
                unique_bax.add(bax)
                stats["surface_points"] += 1
                if ax in legal_ax:
                    stats["surface_legal_ax_points_unsigned_B"] += 1
                    unique_legal_ax.add(ax)
                if ax in d3plus_ax:
                    stats["surface_d3plus_ax_points_unsigned_B"] += 1
                    unique_d3plus_ax.add(ax)
                if ax in d3minus_ax:
                    stats["surface_d3minus_ax_points_unsigned_B"] += 1
                if bax in legal_bax:
                    stats["surface_legal_bax_points"] += 1
                    unique_legal_bax.add(bax)
                if bax in d3plus_bax:
                    stats["surface_d3plus_bax_points"] += 1
                    unique_d3plus_bax.add(bax)
                if bax in d3minus_bax:
                    stats["surface_d3minus_bax_points"] += 1
                if B in legal_b:
                    stats["surface_points_with_legal_B"] += 1
                if B in d3plus_b:
                    stats["surface_points_with_d3plus_B"] += 1

    stats["surface_unique_ax"] = len(unique_ax)
    stats["surface_unique_bax"] = len(unique_bax)
    stats["surface_unique_legal_ax"] = len(unique_legal_ax)
    stats["surface_unique_d3plus_ax"] = len(unique_d3plus_ax)
    stats["surface_unique_legal_bax"] = len(unique_legal_bax)
    stats["surface_unique_d3plus_bax"] = len(unique_d3plus_bax)
    return stats


def print_counter(prefix: str, p: int, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    surface = stats["surface_points"]
    q2 = p * p
    if surface:
        print(f"  surface_points_per_q2 = {surface / q2:.9f}")
        print(f"  d3plus_bax_rate_on_surface = {stats['surface_d3plus_bax_points'] / surface:.9f}")
        print(f"  d3plus_bax_rate_times_q = {stats['surface_d3plus_bax_points'] * p / surface:.9f}")
        print(f"  legal_bax_rate_on_surface = {stats['surface_legal_bax_points'] / surface:.9f}")
        print(f"  legal_B_rate_on_surface = {stats['surface_points_with_legal_B'] / surface:.9f}")
        print(f"  d3plus_B_rate_on_surface = {stats['surface_points_with_d3plus_B'] / surface:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 BSM surface incidence probe")
    print("surface = m^2*(B^2+s^2-4)=4*s^2*(s^2-4)")
    print("target = legal/d3-plus label-2 compactD rows")
    for p in parse_ints(args.small_primes):
        print_counter(f"q{p}", p, surface_incidence(p))
    print("p27_bsm_surface_incidence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

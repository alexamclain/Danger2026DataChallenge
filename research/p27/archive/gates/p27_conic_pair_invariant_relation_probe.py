#!/usr/bin/env python3
"""Invariant-coordinate relation screen for p27 conic-pair preimages.

The raw `(R,L)` screen found no low-degree plane relation for legal d3-plus
preimages.  This probe repeats the test after quotient-friendly coordinate
changes that remember the visible involutions:

    R -> 1/R,  L -> a^2/L,  a = R - 1/R.

It reports only "extra" nullity beyond finite interpolation forced by the
number of unique transformed points.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import product

from p27_conic_pair_lowdegree_relation_probe import sampler_preimages_for_targets
from p27_conic_pair_sampler_legal_incidence_probe import inv_table, legal_sets


@dataclass(frozen=True)
class System:
    name: str
    coordinates: tuple[str, ...]
    max_degree_default: int
    note: str = ""


PAIR_SYSTEMS = [
    System("A_x", ("A", "x"), 12, "target coordinates"),
    System("c_r", ("c", "r"), 14, "signed conic coordinates"),
    System("r_d", ("r", "d"), 14, "half-sum/half-difference conic coordinates"),
    System("s_m", ("s", "m"), 14, "R+1/R with L+a^2/L"),
    System("s_n", ("s", "n"), 14, "R+1/R with L-a^2/L"),
    System("a2_m", ("a2", "m"), 14, "(R-1/R)^2 with L+a^2/L"),
    System("a2_n", ("a2", "n"), 14, "(R-1/R)^2 with L-a^2/L"),
    System("s_w", ("s", "w"), 14, "R+1/R with (L+a)(L-a)"),
    System("a2_w", ("a2", "w"), 14, "(R-1/R)^2 with (L+a)(L-a)"),
    System("s_lsym", ("s", "lsym"), 14, "R+1/R with L+1/L"),
    System("s_lanti", ("s", "lanti"), 14, "R+1/R with L-1/L"),
    System("m_n", ("m", "n"), 14, "L+a^2/L with L-a^2/L"),
]

TRIPLE_SYSTEMS = [
    System("s_m_w", ("s", "m", "w"), 7, "small triple screen; tautologies possible"),
    System("s_n_w", ("s", "n", "w"), 7, "small triple screen; tautologies possible"),
    System("s_r_c", ("s", "r", "c"), 7, "small triple screen; tautologies possible"),
]


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def monomials_total_degree(dim: int, max_degree: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []

    def rec(remaining_dim: int, remaining_degree: int, prefix: tuple[int, ...]) -> None:
        if remaining_dim == 1:
            out.append(prefix + (remaining_degree,))
            return
        for value in range(remaining_degree + 1):
            rec(remaining_dim - 1, remaining_degree - value, prefix + (value,))

    for total in range(max_degree + 1):
        rec(dim, total, ())
    return out


def invariant_values(point: tuple[int, int], p: int, invs: list[int]) -> dict[str, int] | None:
    R, L = point
    if R == 0 or L == 0:
        return None
    invR = invs[R]
    invL = invs[L]
    inv2 = invs[2]
    inv4 = invs[4]
    a = (R - invR) % p
    s = (R + invR) % p
    a2 = a * a % p
    a2_over_l = a2 * invL % p
    m = (L + a2_over_l) % p
    n = (L - a2_over_l) % p
    r = (-m * inv4) % p
    d = n * inv2 % p
    if r == 0:
        return None
    c = s * d % p * invs[(2 * r) % p] % p
    A = (2 - c * c) % p
    x = r * r % p
    w = (L * L - a2) % p
    return {
        "R": R,
        "L": L,
        "A": A,
        "x": x,
        "c": c,
        "r": r,
        "d": d,
        "s": s,
        "a": a,
        "a2": a2,
        "m": m,
        "n": n,
        "w": w,
        "lsym": (L + invL) % p,
        "lanti": (L - invL) % p,
    }


def transform_points(
    points: list[tuple[int, int]], system: System, p: int, invs: list[int]
) -> tuple[list[tuple[int, ...]], Counter]:
    out: list[tuple[int, ...]] = []
    stats: Counter = Counter()
    for point in points:
        values = invariant_values(point, p, invs)
        if values is None:
            stats["degenerate"] += 1
            continue
        out.append(tuple(values[name] for name in system.coordinates))
    stats["rows"] = len(out)
    stats["unique"] = len(set(out))
    return out, stats


def row_for_point(
    point: tuple[int, ...], monomials: list[tuple[int, ...]], p: int
) -> list[int]:
    max_powers = [max(mono[i] for mono in monomials) for i in range(len(point))]
    powers: list[list[int]] = []
    for coord, max_power in zip(point, max_powers):
        coord_powers = [1] * (max_power + 1)
        for i in range(1, max_power + 1):
            coord_powers[i] = coord_powers[i - 1] * coord % p
        powers.append(coord_powers)
    return [
        product_value(monomial, powers, p)
        for monomial in monomials
    ]


def product_value(monomial: tuple[int, ...], powers: list[list[int]], p: int) -> int:
    value = 1
    for axis, exponent in enumerate(monomial):
        value = value * powers[axis][exponent] % p
    return value


def echelon_basis(rows: list[list[int]], p: int) -> tuple[dict[int, list[int]], list[int]]:
    basis: dict[int, list[int]] = {}
    pivots: list[int] = []
    for raw in rows:
        row = raw[:]
        while True:
            pivot = next((i for i, value in enumerate(row) if value % p), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(row[pivot] % p, p - 2, p)
                row = [value * inv % p for value in row]
                basis[pivot] = row
                pivots.append(pivot)
                break
            coeff = row[pivot] % p
            brow = basis[pivot]
            row = [(value - coeff * bvalue) % p for value, bvalue in zip(row, brow)]
    pivots.sort()
    return basis, pivots


def null_vector_from_basis(
    basis: dict[int, list[int]], pivots: list[int], ncols: int, p: int
) -> list[int] | None:
    free_cols = [col for col in range(ncols) if col not in basis]
    if not free_cols:
        return None
    free = free_cols[0]
    vec = [0] * ncols
    vec[free] = 1
    for pivot in reversed(pivots):
        row = basis[pivot]
        acc = 0
        for col in range(pivot + 1, ncols):
            acc = (acc + row[col] * vec[col]) % p
        vec[pivot] = (-acc) % p
    return vec


def evaluate_relation(
    point: tuple[int, ...], monomials: list[tuple[int, ...]], coeffs: list[int], p: int
) -> int:
    row = row_for_point(point, monomials, p)
    return sum(c * v for c, v in zip(coeffs, row)) % p


def relation_stats_for_system(
    transformed: list[tuple[int, ...]], p: int, degrees: list[int]
) -> Counter:
    stats: Counter = Counter()
    unique_points = sorted(set(transformed))
    for degree in degrees:
        monomials = monomials_total_degree(len(unique_points[0]), degree) if unique_points else []
        rows = [row_for_point(point, monomials, p) for point in unique_points]
        basis, pivots = echelon_basis(rows, p)
        rank = len(pivots)
        nullity = len(monomials) - rank
        forced = max(0, len(monomials) - len(unique_points))
        extra = max(0, nullity - forced)
        prefix = f"deg{degree}"
        stats[f"{prefix}_monomials"] = len(monomials)
        stats[f"{prefix}_rank"] = rank
        stats[f"{prefix}_nullity"] = nullity
        stats[f"{prefix}_forced_nullity"] = forced
        stats[f"{prefix}_extra_nullity"] = extra
        if extra:
            coeffs = null_vector_from_basis(basis, pivots, len(monomials), p)
            if coeffs is not None:
                bad = sum(
                    1
                    for point in unique_points
                    if evaluate_relation(point, monomials, coeffs, p) != 0
                )
                stats[f"{prefix}_relation_self_mismatches"] = bad
                stats[f"{prefix}_relation_terms"] = sum(1 for c in coeffs if c % p)
    return stats


def degrees_for(system: System, requested: list[int] | None) -> list[int]:
    if requested is not None:
        return requested
    return list(range(2, system.max_degree_default + 1, 2))


def screen_field(
    p: int,
    systems: list[System],
    pair_degrees: list[int] | None,
    triple_degrees: list[int] | None,
) -> list[tuple[str, Counter]]:
    invs = inv_table(p)
    legal_stats, _, d3_plus, d3_minus = legal_sets(p)
    plus_points, plus_stats = sampler_preimages_for_targets(p, d3_plus)
    minus_points, minus_stats = sampler_preimages_for_targets(p, d3_minus)
    base = Counter({f"legal_{key}": value for key, value in legal_stats.items()})
    base.update({f"plus_{key}": value for key, value in plus_stats.items()})
    base.update({f"minus_{key}": value for key, value in minus_stats.items()})
    base["minus_unique_preimages"] = len(set(minus_points))

    rows: list[tuple[str, Counter]] = []
    for system in systems:
        transformed, transform_stats = transform_points(plus_points, system, p, invs)
        stats = Counter(base)
        stats.update({f"transform_{key}": value for key, value in transform_stats.items()})
        requested = triple_degrees if len(system.coordinates) == 3 else pair_degrees
        stats.update(relation_stats_for_system(transformed, p, degrees_for(system, requested)))
        rows.append((system.name, stats))
    return rows


def print_system(prefix: str, system_name: str, stats: Counter, degrees: list[int]) -> None:
    print(f"{prefix} {system_name}:")
    print(f"  rows = {stats['transform_rows']}")
    print(f"  unique = {stats['transform_unique']}")
    print(f"  degenerate = {stats['transform_degenerate']}")
    print(f"  legal_unique_d3_plus_A_x = {stats['legal_unique_d3_plus_A_x']}")
    print(f"  plus_target_preimages = {stats['plus_target_preimages']}")
    print(f"  minus_target_preimages = {stats['minus_target_preimages']}")
    for degree in degrees:
        prefix_key = f"deg{degree}"
        print(
            "  "
            f"{prefix_key}: monomials={stats[f'{prefix_key}_monomials']} "
            f"rank={stats[f'{prefix_key}_rank']} "
            f"nullity={stats[f'{prefix_key}_nullity']} "
            f"forced={stats[f'{prefix_key}_forced_nullity']} "
            f"extra={stats[f'{prefix_key}_extra_nullity']}"
        )
        if stats[f"{prefix_key}_extra_nullity"]:
            print(
                "  "
                f"{prefix_key}_relation_terms={stats[f'{prefix_key}_relation_terms']} "
                f"self_mismatches={stats[f'{prefix_key}_relation_self_mismatches']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--pair-degrees", default="")
    parser.add_argument("--triple-degrees", default="")
    parser.add_argument("--include-triples", action="store_true")
    args = parser.parse_args()

    pair_degrees = parse_ints(args.pair_degrees) if args.pair_degrees else None
    triple_degrees = parse_ints(args.triple_degrees) if args.triple_degrees else None
    systems = PAIR_SYSTEMS + (TRIPLE_SYSTEMS if args.include_triples else [])

    print("p27 conic-pair invariant relation probe")
    print("points = sampler preimages of legal d3-plus classes")
    print("nullity_extra = nullity beyond finite interpolation forced by unique count")
    for p in parse_ints(args.small_primes):
        for system_name, stats in screen_field(p, systems, pair_degrees, triple_degrees):
            system = next(system for system in systems if system.name == system_name)
            requested = triple_degrees if len(system.coordinates) == 3 else pair_degrees
            print_system(f"q{p}", system_name, stats, degrees_for(system, requested))
    print("p27_conic_pair_invariant_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

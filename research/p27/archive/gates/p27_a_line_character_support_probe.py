#!/usr/bin/env python3
"""Low-degree A-line character support screen for the p27 selected tower.

The A-level prefix probe shows that selected gates descend to whole A-fibers.
This probe asks whether those A-level bits are visible low-genus characters:

    d_j(A) = chi(f_j(A))

for low-degree branch support on P1_A.  It is a falsifier/prototype screen,
not a coefficient fit over p27.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from math import comb

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints, prefix_alive
from p27_a_projection_prefix_profile_probe import auto_primes
from p27_b_line_branch_support_probe import (
    exact_linear_factor_search,
    irreducible_quadratic_pair_search,
    irreducible_quadratic_plus_linear_search,
)
from p27_legal_conic_tower_depth_probe import selected_gate_bits


def target_rows(ax_points: set[tuple[int, int]], p: int, gate: int, depth: int) -> tuple[list[tuple[int, int]], Counter]:
    """Return A rows for d_gate on the selected prefix before that gate.

    Row bit convention follows the B-line branch probes:
      0 = target +1
      1 = target -1
    """

    gate_index = gate - 3
    bits_by_ax = {
        (A, x): selected_gate_bits(A, x, p, depth)
        for A, x in sorted(ax_points)
    }
    groups: defaultdict[int, Counter] = defaultdict(Counter)
    stats: Counter = Counter()
    for (A, _x), bits in bits_by_ax.items():
        if gate_index < 0 or gate_index >= len(bits):
            continue
        if not prefix_alive(bits, gate_index):
            continue
        bit = bits[gate_index]
        if bit not in (-1, 1):
            stats["bad_bit_rows"] += 1
            continue
        groups[A][int(bit)] += 1
        groups[A]["rows"] += 1

    rows: list[tuple[int, int]] = []
    for A, counter in sorted(groups.items()):
        if counter[1] and counter[-1]:
            stats["mixed_A_groups"] += 1
            stats["mixed_A_rows"] += counter["rows"]
            continue
        if counter[1]:
            rows.append((A, 0))
            stats["plus_A"] += 1
        elif counter[-1]:
            rows.append((A, 1))
            stats["minus_A"] += 1
    stats["gate_d"] = gate
    stats["groups"] = len(groups)
    stats["rows"] = len(rows)
    stats["domain_points"] = len(ax_points)
    stats["domain_A"] = len({A for A, _x in ax_points})
    return rows, stats


def split_family_size(q: int, rows: int, max_weight: int) -> int:
    candidates = max(0, q - rows)
    return sum(comb(candidates, weight) for weight in range(1, max_weight + 1))


def rough_expected_exact(family_size: int, rows: int) -> float:
    if rows <= 0:
        return 0.0
    return 2.0 * family_size / (2.0**rows)


def verdict(lam: float) -> str:
    if lam >= 10:
        return "interpolation_likely"
    if lam >= 0.25:
        return "local_fit_not_decisive"
    if lam >= 0.01:
        return "exact_fit_interesting_needs_guard"
    return "exact_fit_decisive_if_stable"


def add_significance(stats: Counter, q: int, rows: int, max_weight: int) -> None:
    split_size = split_family_size(q, rows, max_weight)
    lam = rough_expected_exact(split_size, rows)
    stats["split_family_size"] = split_size
    stats["split_expected_exact_x1e12"] = int(lam * 1_000_000_000_000)
    # Families for irreducible quadratic + <=2 linears and two irreducible quadratics
    # are only rough calibrations; they keep exact hits in tiny domains from being
    # mistaken for stable structure.
    irreducible_quads = q * (q - 1) // 2
    quad_plus_size = irreducible_quads * (1 + max(0, q - rows) + comb(max(0, q - rows), 2))
    quad_pair_size = irreducible_quads * (irreducible_quads + 1) // 2
    stats["quad_plus_expected_exact_x1e12"] = int(rough_expected_exact(quad_plus_size, rows) * 1_000_000_000_000)
    stats["quad_pair_expected_exact_x1e12"] = int(rough_expected_exact(quad_pair_size, rows) * 1_000_000_000_000)
    stats["split_verdict_code"] = {
        "interpolation_likely": 3,
        "local_fit_not_decisive": 2,
        "exact_fit_interesting_needs_guard": 1,
        "exact_fit_decisive_if_stable": 0,
    }[verdict(lam)]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def parse_gate_set(raw: str) -> set[int]:
    return {int(part) for part in raw.split(",") if part.strip()}


def run_field(
    q: int,
    depth: int,
    min_rows: int,
    max_weight: int,
    quadratic_gates: set[int],
) -> None:
    ax_points, base_stats = collect_field_ax(q)
    base_stats["sqrt_q_floor"] = math.isqrt(q)
    print_counter(f"q{q}_base", base_stats)

    for gate in range(3, depth + 3):
        rows, row_stats = target_rows(ax_points, q, gate, depth)
        add_significance(row_stats, q, len(rows), max_weight)
        print_counter(f"q{q}_d{gate}_target_stats", row_stats)
        if len(rows) < min_rows:
            print(f"q{q}_d{gate}_split_support_result: skipped_rows_lt_{min_rows}")
            continue
        if row_stats["plus_A"] == 0 or row_stats["minus_A"] == 0:
            print(f"q{q}_d{gate}_split_support_result: skipped_one_sided")
            continue

        split_stats, split_solution = exact_linear_factor_search(q, rows, max_weight)
        print_counter(f"q{q}_d{gate}_split_support_stats", split_stats)
        if split_solution is None:
            print(f"q{q}_d{gate}_split_support_result: none_weight_le_{max_weight}")
        else:
            weight, factors, polarity = split_solution
            print(
                f"q{q}_d{gate}_split_support_result: "
                f"weight={weight} polarity={polarity} factors={','.join(str(f) for f in factors)} "
                f"significance={verdict(row_stats['split_expected_exact_x1e12'] / 1_000_000_000_000)}"
            )

        if gate not in quadratic_gates:
            continue
        quad_stats, quad_solution = irreducible_quadratic_plus_linear_search(q, rows, 2)
        print_counter(f"q{q}_d{gate}_quad_plus_linear_stats", quad_stats)
        if quad_solution is None:
            print(f"q{q}_d{gate}_quad_plus_linear_result: none_quad_plus_le_2_linear")
        else:
            u, v, factors, polarity = quad_solution
            print(
                f"q{q}_d{gate}_quad_plus_linear_result: "
                f"quadratic=A^2+{u}A+{v} polarity={polarity} "
                f"linear_factors={','.join(str(f) for f in factors) if factors else 'none'}"
            )

        pair_stats, pair_solution = irreducible_quadratic_pair_search(q, rows)
        print_counter(f"q{q}_d{gate}_two_quadratic_stats", pair_stats)
        if pair_solution is None:
            print(f"q{q}_d{gate}_two_quadratic_result: none_two_irreducible_quadratics")
        else:
            q0, q1, polarity = pair_solution
            q1_label = "single" if q1 == (-1, -1) else f"A^2+{q1[0]}A+{q1[1]}"
            print(
                f"q{q}_d{gate}_two_quadratic_result: "
                f"polarity={polarity} quadratic0=A^2+{q0[0]}A+{q0[1]} quadratic1={q1_label}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--auto-start", type=int, default=0)
    parser.add_argument("--auto-count", type=int, default=0)
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=40)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--quadratic-gates", default="")
    args = parser.parse_args()

    primes = parse_ints(args.small_primes)
    if args.auto_count:
        primes.extend(auto_primes(args.auto_start, args.auto_count))
    quadratic_gates = parse_gate_set(args.quadratic_gates)

    print("p27 A-line character support probe")
    print("screen = d_j(A) as chi(low-degree branch support on P1_A)")
    print(f"depth = {args.depth}")
    print(f"min_rows = {args.min_rows}")
    print(f"max_split_weight = {args.max_weight}")
    print(f"quadratic_gates = {','.join(str(g) for g in sorted(quadratic_gates)) or 'none'}")
    for q in dict.fromkeys(primes):
        run_field(q, args.depth, args.min_rows, args.max_weight, quadratic_gates)
    print("p27_a_line_character_support_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

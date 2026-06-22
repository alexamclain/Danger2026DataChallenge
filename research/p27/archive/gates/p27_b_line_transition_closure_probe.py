#!/usr/bin/env python3
"""Check whether the second B-line fiber is just the generic halving transition.

The first reduced B fixture gives four values of u=x6+1/x6 over each legal B.
The second fixture gives eight values of v=x7+1/x7 over each legal B with
f3(B)=+1.  A possible moonshot opening would be that the second fiber is a
proper special subcover of the generic transition from u to v.

For Montgomery halving,

    x6 = (x7^2 - 1)^2 / (4*x7*(x7^2 + A*x7 + 1)).

Writing u=x6+1/x6 and v=x7+1/x7 gives the quotient transition

    (v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A) + 16*(v + A)^2 = 0.

This probe compares the actual parent (B,u,v) edges against all roots of that
generic transition over the guard fields.  Equality is negative for a hidden
second-fiber source, but useful: it says f4/f3 must be attacked as a Kummer
class on the legal B domain, not as a smaller v-fiber bucket.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from p27_b_line_second_reduced_fiber_probe import collect_second_fibers
from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import normalize


DEFAULT_FIRST = Path("research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json")
DEFAULT_SECOND = Path("research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json")


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def transition_value(A: int, u: int, v: int, p: int) -> int:
    n = (v * v - 4) % p
    d = (v + A) % p
    return (n * n - 4 * u * n * d + 16 * d * d) % p


def transition_roots(A: int, u: int, p: int) -> set[int]:
    roots = set()
    for v in range(p):
        if (v + A) % p == 0:
            continue
        if transition_value(A, u, v, p) == 0:
            roots.add(v)
    return roots


def load_field(packet: dict[str, Any], q: int) -> dict[str, Any]:
    for fixture in packet["fixtures"]:
        if int(fixture["field"]) == q:
            return fixture
    raise KeyError(f"field {q} not present in fixture")


def sign_to_int(label: str) -> int:
    if label == "plus":
        return 1
    if label == "minus":
        return -1
    return 0


def collect_actual_edges(q: int) -> tuple[dict[tuple[int, int], set[int]], dict[int, set[int]], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    edges: defaultdict[tuple[int, int], set[int]] = defaultdict(set)
    by_b: defaultdict[int, set[int]] = defaultdict(set)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})

    for cand in dedupe_candidates(candidates):
        stats["deduped_candidates"] += 1
        A = int(cand["A"]) % q
        x5 = int(cand["x5"]) % q
        B = source_b_plus(int(cand["X"]) % q, q)
        if B is None:
            stats["b_degenerate"] += 1
            continue

        d2, x6s = halve_all(A, x5, q)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        d3 = normalize(legendre(x6, q) for x6 in x6s)
        if d3 != 1:
            stats[f"d3_not_plus_{d3}"] += 1
            continue

        for x6 in x6s:
            if legendre(x6, q) != 1:
                stats["x6_not_square_despite_d3_plus"] += 1
                continue
            u = (x6 + inv(x6, q)) % q
            d_next, x7s = halve_all(A, x6, q)
            if d_next != 1:
                stats["next_halving_not_square"] += 1
                continue
            for x7 in x7s:
                v = (x7 + inv(x7, q)) % q
                edges[(B, u)].add(v)
                by_b[B].add(v)

    stats["actual_parent_pairs"] = len(edges)
    stats["actual_B"] = len(by_b)
    stats["actual_edges"] = sum(len(values) for values in edges.values())
    return dict(edges), dict(by_b), stats


def run_field(q: int, first: dict[str, Any], second: dict[str, Any]) -> None:
    first_field = load_field(first, q)
    second_field = load_field(second, q)
    actual_edges, actual_by_b, edge_stats = collect_actual_edges(q)
    second_groups, second_signs, _setup = collect_second_fibers(q)

    first_plus_rows = [
        row for row in first_field["rows"] if str(row["sign"]) == "plus"
    ]
    second_by_b = {
        int(row["B"]): {int(value) % q for value in row["v_roots"]}
        for row in second_field["rows"]
    }
    second_sign_by_b = {
        int(row["B"]): sign_to_int(str(row["sign"]))
        for row in second_field["rows"]
    }

    stats = Counter(edge_stats)
    stats["first_plus_B"] = len(first_plus_rows)
    stats["second_fixture_B"] = len(second_by_b)
    stats["second_collect_B"] = len(second_groups)

    generic_by_b: defaultdict[int, set[int]] = defaultdict(set)
    generic_edges: dict[tuple[int, int], set[int]] = {}
    sample_mismatches: list[str] = []

    for row in first_plus_rows:
        B = int(row["B"]) % q
        A = (B * B - 2) % q
        fixture_vs = second_by_b.get(B, set())
        for raw_u in row["u_roots"]:
            u = int(raw_u) % q
            roots = transition_roots(A, u, q)
            actual = actual_edges.get((B, u), set())
            generic_edges[(B, u)] = roots
            generic_by_b[B].update(roots)

            stats[f"generic_roots_per_u_{len(roots)}"] += 1
            stats[f"actual_roots_per_u_{len(actual)}"] += 1
            if roots == actual:
                stats["parent_edge_equal"] += 1
            else:
                stats["parent_edge_mismatch"] += 1
                stats["parent_edge_missing_roots"] += len(roots - actual)
                stats["parent_edge_extra_roots"] += len(actual - roots)
                if len(sample_mismatches) < 8:
                    sample_mismatches.append(
                        f"B={B} u={u} generic={sorted(roots)} actual={sorted(actual)}"
                    )

            if any(v not in fixture_vs for v in roots):
                stats["generic_roots_outside_second_fixture_parent"] += 1

    for B, roots in sorted(generic_by_b.items()):
        fixture_roots = second_by_b.get(B, set())
        actual_roots = actual_by_b.get(B, set())
        stats[f"generic_v_roots_per_B_{len(roots)}"] += 1
        stats[f"fixture_v_roots_per_B_{len(fixture_roots)}"] += 1
        if roots == fixture_roots:
            stats["B_union_equals_second_fixture"] += 1
        else:
            stats["B_union_mismatch_second_fixture"] += 1
            stats["B_union_missing_fixture_roots"] += len(fixture_roots - roots)
            stats["B_union_extra_fixture_roots"] += len(roots - fixture_roots)
        if roots == actual_roots:
            stats["B_union_equals_actual"] += 1
        else:
            stats["B_union_mismatch_actual"] += 1

        sign = second_sign_by_b.get(B, 0)
        value_signs = {legendre((v + 2) % q, q) for v in roots}
        stats[f"generic_vplus2_sign_classes_{len(value_signs)}"] += 1
        if sign and value_signs == {sign}:
            stats["generic_vplus2_matches_f4"] += 1
        elif roots:
            stats["generic_vplus2_mismatch_f4"] += 1

    # Verify the explicit relation on independently collected second roots.
    for B, roots in sorted(second_groups.items()):
        A = (B * B - 2) % q
        for x7 in set(roots):
            v = (x7 + inv(x7, q)) % q
            # The parent u is not available from second_groups, so this exact
            # check is done on generic_edges above.  Keep this loop only to
            # verify fixture signs against the independent collector.
            if B in second_signs and legendre((v + 2) % q, q) == second_signs[B]:
                stats["second_collect_vplus2_sign_ok"] += 1
            else:
                stats["second_collect_vplus2_sign_bad"] += 1

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    if sample_mismatches:
        print("  parent_edge_mismatch_samples:")
        for sample in sample_mismatches:
            print(f"    {sample}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--second-fixture", type=Path, default=DEFAULT_SECOND)
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    second = json.loads(args.second_fixture.read_text())

    print("p27 B-line transition closure probe")
    print("question = is f4 over f3-plus exactly the generic u-to-v halving transition?")
    print("transition = (v^2-4)^2 - 4*u*(v^2-4)*(v+A) + 16*(v+A)^2")
    print(f"first_fixture = {args.first_fixture}")
    print(f"second_fixture = {args.second_fixture}")
    for q in parse_ints(args.small_primes):
        run_field(q, first, second)
    print("p27_b_line_transition_closure_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

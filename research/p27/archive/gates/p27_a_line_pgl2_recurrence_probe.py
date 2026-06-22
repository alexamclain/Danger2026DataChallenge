#!/usr/bin/env python3
"""PGL2 recurrence screen for the p27 A-line selected Kummer sequence.

The affine A-line recurrence screen killed A -> m*A+b.  This probe tests the
full degree-one rational family

    phi(A) = (a*A + b) / (c*A + d)
    d_{j+1}(A) = polarity * d_j(phi(A))

on selected prefix domains.  A full-coverage PGL2 map is determined by the
images of any three distinct later-domain A values, so the search is finite
and structural rather than a broad coefficient fit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import permutations

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import target_rows


@dataclass(frozen=True)
class PGL2Map:
    a: int
    b: int
    c: int
    d: int


@dataclass(frozen=True)
class PGL2Hit:
    phi: PGL2Map
    polarity: int
    covered: int
    matches: int


def row_map(rows: list[tuple[int, int]]) -> dict[int, int]:
    """Convert target rows to sign map.  Row bit: 0 => +1, 1 => -1."""

    return {A: (1 if bit == 0 else -1) for A, bit in rows}


def inv_mod(x: int, q: int) -> int | None:
    x %= q
    if x == 0:
        return None
    return pow(x, q - 2, q)


def normalize_map(values: list[int], q: int) -> PGL2Map | None:
    values = [value % q for value in values]
    if all(value == 0 for value in values):
        return None
    for value in values:
        inv = inv_mod(value, q)
        if inv is not None:
            return PGL2Map(*(component * inv % q for component in values))
    return None


def nullspace_vector_mod(rows: list[list[int]], q: int) -> list[int] | None:
    """Return one nonzero vector in the right nullspace of a 3x4 matrix."""

    mat = [[value % q for value in row] for row in rows]
    pivots: list[int] = []
    r = 0
    for c in range(4):
        pivot = None
        for rr in range(r, 3):
            if mat[rr][c] % q:
                pivot = rr
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        inv = pow(mat[r][c], q - 2, q)
        mat[r] = [(value * inv) % q for value in mat[r]]
        for rr in range(3):
            if rr == r:
                continue
            factor = mat[rr][c] % q
            if factor:
                mat[rr] = [(mat[rr][cc] - factor * mat[r][cc]) % q for cc in range(4)]
        pivots.append(c)
        r += 1
        if r == 3:
            break

    free_cols = [c for c in range(4) if c not in pivots]
    if not free_cols:
        return None
    free = free_cols[-1]
    sol = [0, 0, 0, 0]
    sol[free] = 1
    for row_idx in range(len(pivots) - 1, -1, -1):
        pivot_col = pivots[row_idx]
        total = sum(mat[row_idx][c] * sol[c] for c in free_cols) % q
        sol[pivot_col] = (-total) % q
    return sol


def pgl2_from_three(xs: tuple[int, int, int], ys: tuple[int, int, int], q: int) -> PGL2Map | None:
    equations = []
    for x, y in zip(xs, ys):
        equations.append([x, 1, (-y * x) % q, -y])
    sol = nullspace_vector_mod(equations, q)
    if sol is None:
        return None
    phi = normalize_map(sol, q)
    if phi is None:
        return None
    det = (phi.a * phi.d - phi.b * phi.c) % q
    if det == 0:
        return None
    for x, y in zip(xs, ys):
        if eval_pgl2(phi, x, q) != y % q:
            return None
    return phi


def eval_pgl2(phi: PGL2Map, x: int, q: int) -> int | None:
    den = (phi.c * x + phi.d) % q
    inv = inv_mod(den, q)
    if inv is None:
        return None
    return ((phi.a * x + phi.b) * inv) % q


def score_pgl2(
    q: int,
    prev: dict[int, int],
    nxt: dict[int, int],
    phi: PGL2Map,
    polarity: int,
) -> tuple[int, int, int]:
    covered = 0
    matches = 0
    poles = 0
    for A, target in nxt.items():
        image = eval_pgl2(phi, A, q)
        if image is None:
            poles += 1
            continue
        source = prev.get(image)
        if source is None:
            continue
        covered += 1
        if target == polarity * source:
            matches += 1
    return covered, matches, poles


def transition_name(prev_gate: int, next_gate: int) -> str:
    return f"d{prev_gate}_to_d{next_gate}"


def find_pgl2_recurrences(
    q: int,
    prev_rows: list[tuple[int, int]],
    next_rows: list[tuple[int, int]],
    keep_best: int,
) -> tuple[Counter, list[PGL2Hit], list[PGL2Hit]]:
    prev = row_map(prev_rows)
    nxt = row_map(next_rows)
    stats: Counter = Counter()
    stats["prev_rows"] = len(prev)
    stats["next_rows"] = len(nxt)
    if len(prev) < 3 or len(nxt) < 3:
        return stats, [], []

    xs = tuple(sorted(nxt)[:3])
    prev_values = tuple(sorted(prev))
    seen: set[PGL2Map] = set()
    exact: list[PGL2Hit] = []
    best: list[PGL2Hit] = []

    for ys in permutations(prev_values, 3):
        phi = pgl2_from_three(xs, ys, q)
        if phi is None or phi in seen:
            continue
        seen.add(phi)
        stats["pgl2_maps_tested"] += 1
        for polarity in (1, -1):
            covered, matches, poles = score_pgl2(q, prev, nxt, phi, polarity)
            stats["candidate_poles"] += poles
            hit = PGL2Hit(phi=phi, polarity=polarity, covered=covered, matches=matches)
            if covered == len(nxt) and matches == len(nxt):
                exact.append(hit)
            best.append(hit)

    best.sort(key=lambda hit: (hit.matches, hit.covered), reverse=True)
    stats["exact_pgl2_recurrences"] = len(exact)
    if best:
        stats["best_covered"] = best[0].covered
        stats["best_matches"] = best[0].matches
        stats["best_match_x1000000"] = (best[0].matches * 1_000_000) // len(nxt)
        stats["best_coverage_x1000000"] = (best[0].covered * 1_000_000) // len(nxt)
    stats["distinct_pgl2_maps"] = len(seen)
    return stats, exact[:keep_best], best[:keep_best]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(prefix: str, hits: list[PGL2Hit]) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
    for hit in hits:
        phi = hit.phi
        print(
            "  "
            f"phi=({phi.a}*A+{phi.b})/({phi.c}*A+{phi.d}) "
            f"polarity={hit.polarity} covered={hit.covered} matches={hit.matches}"
        )


def run_field(q: int, depth: int, min_rows: int, keep_best: int) -> None:
    ax_points, base_stats = collect_field_ax(q)
    print_counter(f"q{q}_base", base_stats)
    rows_by_gate: dict[int, list[tuple[int, int]]] = {}
    for gate in range(3, depth + 3):
        rows, stats = target_rows(ax_points, q, gate, depth)
        rows_by_gate[gate] = rows
        print_counter(f"q{q}_d{gate}_target", stats)

    for prev_gate in range(3, depth + 2):
        next_gate = prev_gate + 1
        label = transition_name(prev_gate, next_gate)
        prev_rows = rows_by_gate[prev_gate]
        next_rows = rows_by_gate[next_gate]
        if len(prev_rows) < min_rows or len(next_rows) < min_rows:
            print(f"q{q}_{label}_pgl2_result: skipped_rows_lt_{min_rows}")
            continue
        stats, exact, best = find_pgl2_recurrences(q, prev_rows, next_rows, keep_best)
        print_counter(f"q{q}_{label}_pgl2_stats", stats)
        print_hits(f"q{q}_{label}_exact_pgl2", exact)
        print_hits(f"q{q}_{label}_best_pgl2", best)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--depth", type=int, default=8)
    parser.add_argument("--min-rows", type=int, default=20)
    parser.add_argument("--keep-best", type=int, default=5)
    args = parser.parse_args()

    print("p27 A-line PGL2 recurrence probe")
    print("screen = d_{j+1}(A) = +/- d_j((a*A+b)/(c*A+d))")
    print(f"depth = {args.depth}")
    print(f"min_rows = {args.min_rows}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.depth, args.min_rows, args.keep_best)
    print("p27_a_line_pgl2_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Low-bidegree abstract-to-embedded quotient pairing scan.

The selected p24 tower would be much easier if abstract unramified quotient
coordinates carried enough phase information to pair with embedded quotient
periods.  Earlier toys ruled out affine/Mobius set maps.  This scan tests a
slightly broader version: a low-bidegree relation F(X,Y)=0 whose zeros on the
cartesian product of abstract roots X and embedded roots Y form a perfect
matching.

For a quotient of size n, arbitrary interpolation becomes cheap once the
monomial support exceeds n.  The interesting question is whether actual CM
rows admit a separating relation with support <= n, unlike random sets.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass

from cypari2 import Pari

from embedded_decomposition_calibration import (
    isogeny_neighbors,
    pari_linear_roots,
)


@dataclass(frozen=True)
class Case:
    D: int
    q: int
    ell: int
    quotient_size: int


CASES = (
    Case(D=-2239, q=2243, ell=5, quotient_size=5),
    Case(D=-2239, q=2243, ell=2, quotient_size=7),
    Case(D=-711, q=727, ell=2, quotient_size=5),
)


def rref_mod_q(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    m = len(rows)
    n = len(rows[0]) if rows else 0
    pivots: list[int] = []
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(m):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % q for j in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return rows, pivots


def nullspace_basis_mod_q(matrix: list[list[int]], q: int) -> list[list[int]]:
    if not matrix:
        return []
    rows, pivots = rref_mod_q(matrix, q)
    n = len(matrix[0])
    free_cols = [c for c in range(n) if c not in pivots]
    basis: list[list[int]] = []
    for free in free_cols:
        vec = [0] * n
        vec[free] = 1
        for row_index, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-rows[row_index][free]) % q
        basis.append(vec)
    return basis


def dot(row: list[int], vec: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(row, vec)) % q


def combine(coeffs: list[int], basis: list[list[int]], q: int) -> list[int]:
    out = [0] * len(basis[0])
    for coeff, vec in zip(coeffs, basis):
        if coeff:
            out = [(x + coeff * y) % q for x, y in zip(out, vec)]
    return out


def monomial_row(x: int, y: int, dx: int, dy: int, q: int) -> list[int]:
    row: list[int] = []
    xpows = [1]
    ypows = [1]
    for _ in range(dx):
        xpows.append(xpows[-1] * x % q)
    for _ in range(dy):
        ypows.append(ypows[-1] * y % q)
    for i in range(dx + 1):
        for j in range(dy + 1):
            row.append(xpows[i] * ypows[j] % q)
    return row


def separates_matching(
    xs: list[int],
    ys: list[int],
    perm: tuple[int, ...],
    q: int,
    dx: int,
    dy: int,
    rng: random.Random,
    random_combos: int,
) -> bool:
    matched_rows = [
        monomial_row(x, ys[perm[i]], dx, dy, q)
        for i, x in enumerate(xs)
    ]
    basis = nullspace_basis_mod_q(matched_rows, q)
    if not basis:
        return False

    candidates = basis[:]
    for _ in range(random_combos):
        coeffs = [rng.randrange(q) for _ in basis]
        if any(coeffs):
            candidates.append(combine(coeffs, basis, q))

    for vec in candidates:
        if all(value % q == 0 for value in vec):
            continue
        ok = True
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                if j == perm[i]:
                    continue
                if dot(monomial_row(x, y, dx, dy, q), vec, q) == 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return True
    return False


def count_separating_matchings(
    xs: list[int],
    ys: list[int],
    q: int,
    dx: int,
    dy: int,
    rng: random.Random,
    max_perms: int,
    random_combos: int,
) -> tuple[int, int]:
    n = len(xs)
    all_perms = itertools.permutations(range(n))
    checked = 0
    found = 0
    for perm in all_perms:
        if checked >= max_perms:
            break
        checked += 1
        if separates_matching(xs, ys, perm, q, dx, dy, rng, random_combos):
            found += 1
    return found, checked


def components(graph: dict[int, list[int]]) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for root in sorted(graph):
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        comp: list[int] = []
        while stack:
            current = stack.pop()
            comp.append(current)
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        out.append(sorted(comp))
    return sorted(out, key=lambda row: row[0])


def walk_cycle(graph: dict[int, list[int]]) -> list[int]:
    start = min(graph)
    for first in graph[start]:
        prev = start
        current = first
        cycle = [start]
        while current != start:
            cycle.append(current)
            candidates = [nxt for nxt in graph[current] if nxt != prev]
            if not candidates:
                break
            prev, current = current, candidates[0]
            if len(cycle) > len(graph):
                break
        if len(cycle) == len(graph) and current == start:
            return cycle
    raise ValueError("expected one cycle")


def embedded_periods(roots: list[int], ell: int, q: int, quotient_size: int) -> list[int]:
    graph = isogeny_neighbors(roots, ell, q)
    comps = components(graph)
    if len(comps) == quotient_size:
        return sorted(sum(comp) % q for comp in comps)

    cycle = walk_cycle(graph)
    h = len(cycle)
    if h % quotient_size:
        raise ValueError("quotient size does not divide class number")
    subgroup_size = h // quotient_size
    return sorted(
        sum(cycle[(r + quotient_size * k) % h] for k in range(subgroup_size)) % q
        for r in range(quotient_size)
    )


def y_roots_for_D(D: int, q: int) -> list[int]:
    if D % 4 != 1:
        return []
    c = (1 - D) // 4
    return [a for a in range(q) if (a * a - a + c) % q == 0]


def abstract_root_sets(pari: Pari, D: int, q: int, quotient_size: int) -> list[tuple[int | None, list[int]]]:
    if D % 4 != 1:
        raise ValueError("this scan expects D == 1 mod 4")
    c = (1 - D) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")
    poly = pari(f"bnrclassfield(bnr,{quotient_size},1)")
    try:
        return [(None, sorted(pari_linear_roots(poly, q)))]
    except ValueError:
        out: list[tuple[int | None, list[int]]] = []
        for y0 in y_roots_for_D(D, q):
            specialized = pari(f"subst({poly},y,{y0})")
            try:
                roots = sorted(pari_linear_roots(specialized, q))
            except ValueError:
                continue
            if len(roots) == quotient_size:
                out.append((y0, roots))
        return out


def random_set(size: int, q: int, rng: random.Random) -> list[int]:
    return sorted(rng.sample(range(q), size))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degrees", nargs="*", default=["1,1", "2,1", "1,2", "2,2"])
    parser.add_argument("--max-perms", type=int, default=6000)
    parser.add_argument("--random-controls", type=int, default=5)
    parser.add_argument("--random-combos", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260607)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    degree_pairs = [tuple(int(x) for x in item.split(",")) for item in args.degrees]
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    print("abstract embedded pairing low-bidegree scan")
    print(f"degree_pairs={degree_pairs}")
    print(f"max_perms={args.max_perms}")
    print(f"random_controls={args.random_controls}")
    print(f"random_combos={args.random_combos}")
    print()
    print("columns: D q ell n orient dx dy support actual_found/checked random_controls_with_found")

    total_actual_low = 0
    total_random_low = 0
    rows = 0
    low_support_rows = 0

    for case in CASES:
        hilbert = pari.polclass(case.D)
        cm_roots = pari_linear_roots(hilbert, case.q)
        abstract_sets = abstract_root_sets(pari, case.D, case.q, case.quotient_size)
        ep = embedded_periods(cm_roots, case.ell, case.q, case.quotient_size)
        if len(ep) != case.quotient_size or not abstract_sets:
            print(
                f"D={case.D} q={case.q} ell={case.ell} n={case.quotient_size} "
                "root_count_mismatch=1"
            )
            continue
        for orient, ar in abstract_sets:
            for dx, dy in degree_pairs:
                rows += 1
                support = (dx + 1) * (dy + 1)
                actual_found, checked = count_separating_matchings(
                    ar,
                    ep,
                    case.q,
                    dx,
                    dy,
                    rng,
                    args.max_perms,
                    args.random_combos,
                )
                random_hits = 0
                for _ in range(args.random_controls):
                    xs = random_set(case.quotient_size, case.q, rng)
                    ys = random_set(case.quotient_size, case.q, rng)
                    found, _checked = count_separating_matchings(
                        xs,
                        ys,
                        case.q,
                        dx,
                        dy,
                        rng,
                        args.max_perms,
                        args.random_combos,
                    )
                    random_hits += int(found > 0)
                if support <= case.quotient_size:
                    low_support_rows += 1
                    total_actual_low += int(actual_found > 0)
                    total_random_low += random_hits
                orient_text = "base" if orient is None else str(orient)
                print(
                    f"D={case.D:6d} q={case.q:5d} ell={case.ell:2d} "
                    f"n={case.quotient_size:2d} orient={orient_text:>4s} "
                    f"dx={dx:2d} dy={dy:2d} support={support:2d} "
                    f"actual={actual_found:4d}/{checked:<4d} "
                    f"random_controls_with_found={random_hits}/{args.random_controls}"
                )

    print()
    print("summary")
    print(f"  rows={rows}")
    print(f"  low_support_rows={low_support_rows}")
    print(f"  actual_low_support_rows_with_pairing={total_actual_low}")
    print(f"  random_low_support_control_hits={total_random_low}")
    print()
    print("interpretation")
    print("  support_gt_quotient_size_is_generic_interpolation_not_structure=1")
    print("  support_le_quotient_size_pairing_would_be_non_generic_phase_evidence=1")
    print("  abstract_quotient_coordinate_did_not_show_low_support_pairing_if_actual_low_support_rows_with_pairing_is_zero=1")
    print("conclusion=reported_abstract_embedded_pairing_low_bidegree_scan")

    if rows == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

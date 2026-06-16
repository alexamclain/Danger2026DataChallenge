#!/usr/bin/env python3
"""Audit whether abstract class-field roots expose a cheap tower fiber map.

The selected-chain theorem needs relative fibers, not just two unpaired
abstract quotient polynomials.  This script tests a prerequisite for the
abstract-to-embedded Kummer-pairing idea:

    degree-(a*r) abstract roots -> degree-a abstract parent roots

via a low-degree rational map over the splitting field, with every parent
having exactly r preimages.

If this fails in small rows, then an abstract Kummer-pairing scan is missing
its own fiber grouping data.  If it succeeds, the fibers become candidates for
computing abstract Kummer orbit/minpoly data to compare with embedded child
periods.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from itertools import product

from cypari2 import Pari

from embedded_decomposition_calibration import pari_linear_roots


@dataclass(frozen=True)
class Case:
    D: int
    q: int
    parent_degree: int
    child_degree: int


CASES = [
    Case(D=-671, q=1571, parent_degree=5, child_degree=3),
    Case(D=-815, q=2111, parent_degree=5, child_degree=3),
]


def eval_poly(coeffs: list[int], x: int, q: int) -> int:
    out = 0
    power = 1
    for coeff in coeffs:
        out = (out + coeff * power) % q
        power = power * x % q
    return out


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


def normalize(vec: list[int], q: int) -> tuple[int, ...] | None:
    for value in vec:
        if value % q:
            inv = pow(value % q, -1, q)
            return tuple((v * inv) % q for v in vec)
    return None


def combine(coeffs: list[int], basis: list[list[int]], q: int) -> list[int]:
    out = [0] * len(basis[0])
    for coeff, vec in zip(coeffs, basis):
        if coeff:
            out = [(x + coeff * y) % q for x, y in zip(out, vec)]
    return out


def relation_row(x: int, y: int, degree: int, q: int) -> list[int]:
    row: list[int] = []
    power = 1
    for _ in range(degree + 1):
        row.append(power)
        power = power * x % q
    power = 1
    for _ in range(degree + 1):
        row.append((-y * power) % q)
        power = power * x % q
    return row


def rational_fiber_maps(
    source: list[int],
    target: list[int],
    q: int,
    degree: int,
    fiber_size: int,
    max_found: int,
    random_combos: int,
    rng: random.Random,
) -> set[tuple[int, ...]]:
    """Find low-degree P/Q maps from source onto target with balanced fibers."""

    target_set = set(target)
    fixed_source = source[: 2 * degree + 1]
    found: set[tuple[int, ...]] = set()
    for image_tuple in product(target, repeat=len(fixed_source)):
        matrix = [
            relation_row(x, y, degree, q)
            for x, y in zip(fixed_source, image_tuple)
        ]
        basis = nullspace_basis_mod_q(matrix, q)
        if not basis:
            continue

        candidates: list[list[int]] = []
        candidates.extend(basis)
        for _ in range(random_combos):
            coeffs = [rng.randrange(q) for _ in basis]
            if any(coeffs):
                candidates.append(combine(coeffs, basis, q))

        for vec in candidates:
            key = normalize(vec, q)
            if key is None or key in found:
                continue
            p_coeffs = list(key[: degree + 1])
            q_coeffs = list(key[degree + 1 :])
            counts = {value: 0 for value in target}
            ok = True
            for x in source:
                den = eval_poly(q_coeffs, x, q)
                if den == 0:
                    ok = False
                    break
                y = eval_poly(p_coeffs, x, q) * pow(den, -1, q) % q
                if y not in target_set:
                    ok = False
                    break
                counts[y] += 1
            if ok and all(counts[value] == fiber_size for value in target):
                found.add(key)
                if len(found) >= max_found:
                    return found
    return found


def lagrange_basis_values(
    anchors: list[int],
    points: list[int],
    q: int,
) -> list[list[int]]:
    """basis_values[i][j] = L_j(points[i]) for the anchor Lagrange basis."""

    basis_values: list[list[int]] = []
    denominators: list[int] = []
    for j, xj in enumerate(anchors):
        denom = 1
        for m, xm in enumerate(anchors):
            if m != j:
                denom = denom * (xj - xm) % q
        denominators.append(pow(denom, -1, q))
    for x in points:
        row: list[int] = []
        for j, xj in enumerate(anchors):
            num = 1
            for m, xm in enumerate(anchors):
                if m != j:
                    num = num * (x - xm) % q
            row.append(num * denominators[j] % q)
        basis_values.append(row)
    return basis_values


def polynomial_fiber_maps(
    source: list[int],
    target: list[int],
    q: int,
    degree: int,
    fiber_size: int,
    max_found: int,
    max_tuples: int,
) -> tuple[set[tuple[int, ...]], int, bool]:
    """Find degree-bounded polynomial maps with balanced target fibers.

    Returns maps, the tuple count that would be scanned, and whether the scan
    was skipped by the tuple budget.
    """

    anchor_count = degree + 1
    tuple_count = len(target) ** anchor_count
    if anchor_count > len(source) or tuple_count > max_tuples:
        return set(), tuple_count, True

    target_set = set(target)
    anchors = source[:anchor_count]
    basis_values = lagrange_basis_values(anchors, source, q)
    found: set[tuple[int, ...]] = set()
    for images in product(target, repeat=anchor_count):
        counts = {value: 0 for value in target}
        values: list[int] = []
        ok = True
        for basis_row in basis_values:
            value = sum(y * b for y, b in zip(images, basis_row)) % q
            if value not in target_set:
                ok = False
                break
            counts[value] += 1
            values.append(value)
        if ok and all(counts[value] == fiber_size for value in target):
            found.add(tuple(values))
            if len(found) >= max_found:
                return found, tuple_count, False
    return found, tuple_count, False


def y_roots_for_D(D: int, q: int) -> list[int]:
    if D % 4 != 1:
        return []
    c = (1 - D) // 4
    return [a for a in range(q) if (a * a - a + c) % q == 0]


def abstract_root_sets(
    pari: Pari,
    D: int,
    q: int,
    parent_degree: int,
    fine_degree: int,
) -> list[tuple[int, list[int], list[int]]]:
    if D % 4 != 1:
        raise ValueError("this audit currently expects a fundamental D == 1 mod 4")
    c = (1 - D) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")

    parent_poly = pari(f"lift(bnrclassfield(bnr,{parent_degree},1))")
    fine_poly = pari(f"lift(bnrclassfield(bnr,{fine_degree},1))")
    root_sets: list[tuple[int, list[int], list[int]]] = []
    for y0 in y_roots_for_D(D, q):
        parent_specialized = pari(f"subst({parent_poly},y,{y0})")
        fine_specialized = pari(f"subst({fine_poly},y,{y0})")
        parent_roots = sorted(pari_linear_roots(parent_specialized, q))
        fine_roots = sorted(pari_linear_roots(fine_specialized, q))
        if len(parent_roots) == parent_degree and len(fine_roots) == fine_degree:
            root_sets.append((y0, parent_roots, fine_roots))
    return root_sets


def random_set(size: int, q: int, rng: random.Random) -> list[int]:
    return sorted(rng.sample(range(q), size))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degrees", nargs="*", default=["1", "2"])
    parser.add_argument("--polynomial-degrees", nargs="*", default=[])
    parser.add_argument("--max-found", type=int, default=3)
    parser.add_argument("--max-polynomial-tuples", type=int, default=500000)
    parser.add_argument("--random-controls", type=int, default=20)
    parser.add_argument("--random-combos", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)

    print("abstract tower fiber map scan")
    print("columns: D q a(parent) r(child) ar_orientation degree maps_found random_controls_with_map")
    for case in CASES:
        fine_degree = case.parent_degree * case.child_degree
        try:
            root_sets = abstract_root_sets(
                pari,
                case.D,
                case.q,
                case.parent_degree,
                fine_degree,
            )
        except Exception as exc:
            print(f"D={case.D} q={case.q} error={exc}")
            continue

        print(f"case D={case.D} q={case.q}")
        for y0, parent_roots, fine_roots in root_sets:
            print(f"  orientation_y={y0} parent_roots={parent_roots}")
            print(f"  fine_orientation_y={y0} fine_roots={fine_roots}")
            for degree_text in args.degrees:
                degree = int(degree_text)
                maps = rational_fiber_maps(
                    fine_roots,
                    parent_roots,
                    case.q,
                    degree,
                    case.child_degree,
                    args.max_found,
                    args.random_combos,
                    rng,
                )
                random_hits = 0
                for _ in range(args.random_controls):
                    source = random_set(fine_degree, case.q, rng)
                    target = random_set(case.parent_degree, case.q, rng)
                    controls = rational_fiber_maps(
                        source,
                        target,
                        case.q,
                        degree,
                        case.child_degree,
                        1,
                        args.random_combos,
                        rng,
                    )
                    random_hits += int(bool(controls))
                print(
                    f"D={case.D} q={case.q} a={case.parent_degree} "
                    f"r={case.child_degree} ar_y={y0} degree={degree} "
                    f"maps_found={len(maps)} "
                    f"random_controls_with_map={random_hits}/{args.random_controls}"
                )
                for index, key in enumerate(sorted(maps)[: args.max_found]):
                    print(f"  map_{index}_coeffs={list(key)}")
            for degree_text in args.polynomial_degrees:
                degree = int(degree_text)
                poly_maps, tuple_count, skipped = polynomial_fiber_maps(
                    fine_roots,
                    parent_roots,
                    case.q,
                    degree,
                    case.child_degree,
                    args.max_found,
                    args.max_polynomial_tuples,
                )
                print(
                    f"D={case.D} q={case.q} a={case.parent_degree} "
                    f"r={case.child_degree} ar_y={y0} "
                    f"polynomial_degree={degree} "
                    f"polynomial_maps_found={len(poly_maps)} "
                    f"anchor_tuple_count={tuple_count} skipped={int(skipped)}"
                )
                for index, values in enumerate(sorted(poly_maps)[: args.max_found]):
                    print(f"  polynomial_map_{index}_values={list(values)}")
    print()
    print("interpretation")
    print("  balanced_low_degree_map_would_supply_abstract_relative_fibers=1")
    print("  no_map_means_abstract_roots_are_unpaired_even_before_embedding=1")
    print("  random_control_hits_mean_the_map_degree_is_generic_not_explanatory=1")
    print("  polynomial_map_values_are_reported_as_fine_root_images=1")
    print("conclusion=reported_abstract_tower_fiber_map_scan")


if __name__ == "__main__":
    main()

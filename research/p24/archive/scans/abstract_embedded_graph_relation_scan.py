#!/usr/bin/env python3
"""Low-bidegree pairing relation scan for abstract vs embedded quotient roots.

The embedded tower route needs more than an abstract quotient polynomial: it
needs a relation pairing abstract class-field roots with embedded period
roots.  This script tests whether very low-bidegree equations

    S(A,Y) = 0

can distinguish such a pairing in the D=-2239 degree-5 toy.  It also runs a
random-control set with the same sizes.  The control is important: once
`(deg_A+1)*(deg_Y+1)` exceeds the number of matched pairs, graph equations may
exist by generic interpolation and therefore do not explain the CM pairing.
"""

from __future__ import annotations

import argparse
import random
from itertools import permutations

from cypari2 import Pari

from abstract_embedded_pairing_non_genus_toy import components
from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots

D = -2239
Q = 2243
ELL = 5
QUOTIENT_SIZE = 5


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


def monomials(a: int, y: int, deg_a: int, deg_y: int, q: int) -> list[int]:
    out: list[int] = []
    a_pows = [1]
    y_pows = [1]
    for _ in range(deg_a):
        a_pows.append(a_pows[-1] * a % q)
    for _ in range(deg_y):
        y_pows.append(y_pows[-1] * y % q)
    for i in range(deg_a + 1):
        for j in range(deg_y + 1):
            out.append(a_pows[i] * y_pows[j] % q)
    return out


def dot(left: list[int], right: list[int], q: int) -> int:
    return sum(x * y for x, y in zip(left, right)) % q


def combine(coeffs: list[int], basis: list[list[int]], q: int) -> list[int]:
    out = [0] * len(basis[0])
    for c, vec in zip(coeffs, basis):
        if c:
            out = [(x + c * y) % q for x, y in zip(out, vec)]
    return out


def relation_for_matching(
    abstract_roots: list[int],
    embedded_roots: list[int],
    perm: tuple[int, ...],
    deg_a: int,
    deg_y: int,
    q: int,
    random_trials: int,
    rng: random.Random,
) -> tuple[bool, int]:
    matched = [
        monomials(a, embedded_roots[perm[i]], deg_a, deg_y, q)
        for i, a in enumerate(abstract_roots)
    ]
    basis = nullspace_basis_mod_q(matched, q)
    if not basis:
        return False, 0
    cross = [
        monomials(a, y, deg_a, deg_y, q)
        for i, a in enumerate(abstract_roots)
        for j, y in enumerate(embedded_roots)
        if j != perm[i]
    ]

    candidates: list[list[int]] = []
    candidates.extend(basis)
    if len(basis) == 1:
        candidates.append(basis[0])
    elif len(basis) <= 3 and q <= 5000:
        # Try a deterministic small grid before random sampling.
        for coeffs in permutations(range(1, min(q, 8)), len(basis)):
            candidates.append(combine(list(coeffs), basis, q))
            if len(candidates) >= random_trials:
                break
    for _ in range(random_trials):
        coeffs = [rng.randrange(q) for _ in basis]
        if any(coeffs):
            candidates.append(combine(coeffs, basis, q))

    for coeff in candidates:
        if any(coeff) and all(dot(coeff, row, q) != 0 for row in cross):
            return True, len(basis)
    return False, len(basis)


def count_graph_relations(
    abstract_roots: list[int],
    embedded_roots: list[int],
    deg_a: int,
    deg_y: int,
    q: int,
    random_trials: int,
    rng: random.Random,
) -> tuple[int, int]:
    successes = 0
    max_nullity = 0
    for perm in permutations(range(len(embedded_roots))):
        ok, nullity = relation_for_matching(
            abstract_roots,
            embedded_roots,
            perm,
            deg_a,
            deg_y,
            q,
            random_trials,
            rng,
        )
        max_nullity = max(max_nullity, nullity)
        successes += int(ok)
    return successes, max_nullity


def actual_root_sets() -> tuple[list[int], list[int], str]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    c = (1 - D) // 4
    pari(f"bnf=bnfinit(y^2-y+{c})")
    pari("bnr=bnrinit(bnf,1)")
    abstract_poly = pari(f"bnrclassfield(bnr,{QUOTIENT_SIZE},1)")
    abstract_roots = sorted(pari_linear_roots(abstract_poly, Q))
    cm_roots = pari_linear_roots(hilbert, Q)
    graph = isogeny_neighbors(cm_roots, ELL, Q)
    comps = components(graph)
    embedded_roots = sorted(sum(comp) % Q for comp in comps)
    return abstract_roots, embedded_roots, str(abstract_poly)


def random_root_set(size: int, q: int, rng: random.Random) -> list[int]:
    return sorted(rng.sample(range(q), size))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degrees", nargs="*", default=["1,1", "1,2", "2,1", "2,2"])
    parser.add_argument("--random-controls", type=int, default=20)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    abstract_roots, embedded_roots, abstract_poly = actual_root_sets()
    degree_pairs = [tuple(map(int, item.split(","))) for item in args.degrees]

    print("abstract embedded graph relation scan")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell={ELL}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"abstract_polynomial={abstract_poly}")
    print(f"abstract_roots={abstract_roots}")
    print(f"embedded_period_sums={embedded_roots}")
    print(f"random_controls={args.random_controls}")
    print(f"random_trials_per_matching={args.random_trials}")
    print()
    print("columns: degA degY variables actual_success_matchings actual_max_nullity random_success_controls random_success_matchings_total")

    for deg_a, deg_y in degree_pairs:
        actual_successes, actual_nullity = count_graph_relations(
            abstract_roots,
            embedded_roots,
            deg_a,
            deg_y,
            Q,
            args.random_trials,
            rng,
        )
        random_success_controls = 0
        random_success_matchings = 0
        for _ in range(args.random_controls):
            source = random_root_set(QUOTIENT_SIZE, Q, rng)
            target = random_root_set(QUOTIENT_SIZE, Q, rng)
            successes, _ = count_graph_relations(
                source,
                target,
                deg_a,
                deg_y,
                Q,
                args.random_trials,
                rng,
            )
            if successes:
                random_success_controls += 1
                random_success_matchings += successes
        variables = (deg_a + 1) * (deg_y + 1)
        print(
            f"degA={deg_a} degY={deg_y} variables={variables} "
            f"actual_success_matchings={actual_successes} "
            f"actual_max_nullity={actual_nullity} "
            f"random_success_controls={random_success_controls}/{args.random_controls} "
            f"random_success_matchings_total={random_success_matchings}"
        )

    print()
    print("interpretation")
    print("  bidegree_success_below_or_at_point_count_is_potentially_meaningful=1")
    print("  bidegree_success_above_point_count_may_be_generic_interpolation=1")
    print("  random_control_success_means_the_relation_does_not_explain_cm_pairing=1")
    print("conclusion=reported_abstract_embedded_graph_relation_scan")


if __name__ == "__main__":
    main()

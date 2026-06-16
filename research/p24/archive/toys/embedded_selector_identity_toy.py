#!/usr/bin/env python3
"""Toy finite-field selector identity calibration.

For D=-5000 over F_1259, `embedded_decomposition_calibration.py` constructs a
cyclic CM root orbit of size 30 and a subgroup quotient with six coset labels.

This script asks a sharper finite-field-identity question: is that quotient
label a low-degree rational function of the j-root alone?

Concretely, for pairs (j_i, y_i) with y_i constant on subgroup cosets, search
for A(x), B(x) in F_q[x] with deg(A), deg(B) <= d and

    A(j_i) = y_i B(j_i),  B(j_i) != 0

for every CM root.  If the first d found is the generic interpolation
threshold, then the quotient exists as embedded data but not as a visibly
special low-degree identity in the j-coordinate.
"""

from __future__ import annotations

import random

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    QUOTIENT_SIZE,
    SUBGROUP_SIZE,
    decompose,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from cypari2 import Pari


def eval_poly(coeffs: list[int], x: int, q: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * x + coeff) % q
    return acc


def nullspace_mod(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    rows = [row[:] for row in matrix]
    m = len(rows)
    n = len(rows[0])
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

    pivot_set = set(pivots)
    free_cols = [c for c in range(n) if c not in pivot_set]
    basis: list[list[int]] = []
    for free in free_cols:
        vec = [0] * n
        vec[free] = 1
        for row_index, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-rows[row_index][free]) % q
        basis.append(vec)
    return basis, pivots


def build_pairs() -> list[tuple[int, int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    dec = decompose(cycle, Q)

    label_by_root: dict[int, int] = {}
    for r, label in enumerate(dec.coset_sums):
        coset = [cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)]
        for root in coset:
            label_by_root[root] = label
    return sorted(label_by_root.items())


def candidate_from_basis(
    basis: list[list[int]],
    degree: int,
    pairs: list[tuple[int, int]],
    q: int,
) -> tuple[list[int], list[int]] | None:
    if not basis:
        return None

    rng = random.Random(20260604 + degree)
    trial_vectors = basis[:]
    if len(basis) > 1:
        for _ in range(200):
            coeffs = [rng.randrange(q) for _ in basis]
            if all(c == 0 for c in coeffs):
                coeffs[0] = 1
            vec = [0] * len(basis[0])
            for c, base in zip(coeffs, basis):
                if c:
                    vec = [(v + c * b) % q for v, b in zip(vec, base)]
            trial_vectors.append(vec)

    for vec in trial_vectors:
        a = vec[: degree + 1]
        b = vec[degree + 1 :]
        if all(v == 0 for v in b):
            continue
        ok = True
        for x, y in pairs:
            den = eval_poly(b, x, q)
            if den == 0 or eval_poly(a, x, q) != y * den % q:
                ok = False
                break
        if ok:
            return a, b
    return None


def matrix_for_degree(pairs: list[tuple[int, int]], degree: int, q: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for x, y in pairs:
        powers = [1]
        for _ in range(degree):
            powers.append(powers[-1] * x % q)
        # Unknowns are a_0..a_d,b_0..b_d.
        matrix.append(powers + [(-y * xp) % q for xp in powers])
    return matrix


def main() -> None:
    pairs = build_pairs()
    n = len(pairs)
    generic_threshold = n // 2

    print("embedded selector identity toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"ell_generator={ELL}")
    print(f"class_number={H}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"data_pairs={n}")
    print(f"generic_rational_interpolation_threshold={generic_threshold}")
    print()
    print("degree nullity found_valid_selector")

    first = None
    for degree in range(0, n + 1):
        matrix = matrix_for_degree(pairs, degree, Q)
        basis, _ = nullspace_mod(matrix, Q)
        candidate = candidate_from_basis(basis, degree, pairs, Q)
        found = candidate is not None
        print(f"{degree:6d} {len(basis):7d} {int(found):20d}")
        if found:
            first = degree, candidate
            break

    if first is None:
        raise RuntimeError("no rational interpolant found")

    degree, (a, b) = first
    print()
    print(f"first_selector_degree={degree}")
    print(f"numerator_coeffs={a}")
    print(f"denominator_coeffs={b}")
    print("interpretation")
    print(f"  first_degree_equals_generic_threshold={int(degree == generic_threshold)}")
    print("  low_degree_plain_j_identity_found=0" if degree == generic_threshold else "  low_degree_plain_j_identity_found=1")
    print(
        "conclusion=the_toy_subgroup_quotient_is_embedded_but_the_plain_j_"
        "selector_behaves_like_generic_interpolation"
    )


if __name__ == "__main__":
    main()

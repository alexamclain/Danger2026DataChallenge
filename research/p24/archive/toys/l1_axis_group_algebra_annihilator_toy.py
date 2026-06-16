#!/usr/bin/env python3
"""Group-algebra annihilator toy for L1 axis injectivity.

The p24 L1 axis space is a small sum of cyclotomic factors in F_p[C_m]:

    orders 1, 2, 157, 211.

For a fixed H-packet vector beta, the axis evaluation map is group-algebra
action restricted to this subspace.  In a split toy group algebra, the Fourier
coordinates make the criterion transparent:

    rank(T|W_axis) = number of axis characters where beta_hat is nonzero.

Thus axis injectivity is equivalent to the annihilator of beta having zero
intersection with the axis cyclotomic factors.
"""

from __future__ import annotations

import argparse
import random

from lang_trace_gcd_plucker_spectral_toy import primitive_root_of_order


def axis_exponents(m: int, components: list[int]) -> list[int]:
    exponents = {0}
    for component in components:
        step = m // component
        for a in range(1, component):
            exponents.add((a * step) % m)
    return sorted(exponents)


def axis_basis(m: int, components: list[int]) -> list[list[int]]:
    basis = [[1 for _ in range(m)]]
    for component in components:
        for t in range(1, component):
            basis.append([1 if r % component == t else 0 for r in range(m)])
    return basis


def dft(vector: list[int], root: int, q: int) -> list[int]:
    m = len(vector)
    out: list[int] = []
    for exponent in range(m):
        total = 0
        for r, value in enumerate(vector):
            total = (total + value * pow(root, exponent * r, q)) % q
        out.append(total)
    return out


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, q)
        mat[rank] = [value * inv % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=181)
    parser.add_argument("--m", type=int, default=30)
    parser.add_argument("--components", default="2,3,5")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--kill-axis-exponent", type=int)
    args = parser.parse_args()

    components = [int(part) for part in args.components.split(",") if part]
    root = primitive_root_of_order(args.q, args.m)
    basis = axis_basis(args.m, components)
    exponents = axis_exponents(args.m, components)
    rng = random.Random(args.seed)
    beta_hat = [rng.randrange(1, args.q) for _ in range(args.m)]
    if args.kill_axis_exponent is not None:
        beta_hat[args.kill_axis_exponent % args.m] = 0

    transformed_rows = []
    for vector in basis:
        vector_hat = dft(vector, root, args.q)
        transformed_rows.append([
            vector_hat[exponent] * beta_hat[exponent] % args.q
            for exponent in range(args.m)
        ])

    axis_rank = rank_mod_q([dft(vector, root, args.q) for vector in basis], args.q)
    eval_rank = rank_mod_q(transformed_rows, args.q)
    nonzero_axis_exponents = [
        exponent for exponent in exponents if beta_hat[exponent] % args.q
    ]
    killed_axis_exponents = [
        exponent for exponent in exponents if beta_hat[exponent] % args.q == 0
    ]

    print("L1 axis group-algebra annihilator toy")
    print(f"q={args.q}")
    print(f"m={args.m}")
    print(f"components={components}")
    print(f"root={root}")
    print(f"axis_dim={len(basis)}")
    print(f"axis_exponents={exponents}")
    print(f"axis_rank={axis_rank}")
    print(f"eval_rank={eval_rank}")
    print(f"nonzero_axis_exponent_count={len(nonzero_axis_exponents)}")
    print(f"killed_axis_exponents={killed_axis_exponents}")
    print(f"rank_matches_nonzero_axis_exponents={int(eval_rank == len(nonzero_axis_exponents))}")
    print(f"axis_injective={int(eval_rank == len(basis))}")
    print("interpretation")
    print("  axis_injectivity_equiv_no_axis_character_in_annihilator=1")
    print("  p24_arithmetic_target_is_axis_cyclotomic_components_nonzero=1")
    print("conclusion=reported_l1_axis_group_algebra_annihilator_toy")


if __name__ == "__main__":
    main()

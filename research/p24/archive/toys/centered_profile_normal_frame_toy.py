#!/usr/bin/env python3
"""Toy for the centered-profile normal-frame proof route.

A tempting proof of the centered-profile theorem is:

    one profile value is normal in L/F_p.

That is too weak.  The profile span must contain the whole Frobenius orbit of
that normal value.  Equivalently, the profile span must be Frobenius-stable
enough to close the orbit.

This toy uses a cyclic-shift model for Frobenius on F_q^d.  The vector e_0 has
a full cyclic orbit, so it is "normal" in this model.  The one-dimensional
span of e_0 contains a normal coordinate but is not full; its Frobenius
closure is full.
"""

from __future__ import annotations

import argparse


def rank_mod(matrix: list[list[int]], q: int) -> int:
    mat = [
        [value % q for value in row]
        for row in matrix
        if any(value % q for value in row)
    ]
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
        mat[rank] = [(inv * value) % q for value in mat[rank]]
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


def shift(vec: list[int], amount: int) -> list[int]:
    n = len(vec)
    amount %= n
    return vec[-amount:] + vec[:-amount] if amount else list(vec)


def orbit(vec: list[int]) -> list[list[int]]:
    return [shift(vec, i) for i in range(len(vec))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--degree", type=int, default=8)
    args = parser.parse_args()

    normal_value = [1] + [0] * (args.degree - 1)
    normal_orbit = orbit(normal_value)
    profile_span_generators = [normal_value]
    frobenius_closure_generators = normal_orbit
    one_step_defect = (
        rank_mod(profile_span_generators + [shift(normal_value, 1)], args.q)
        - rank_mod(profile_span_generators, args.q)
    )

    print("Centered-profile normal-frame toy")
    print(f"q={args.q}")
    print(f"degree={args.degree}")
    print(f"normal_orbit_rank={rank_mod(normal_orbit, args.q)}/{args.degree}")
    print(
        "profile_rank_with_one_normal_coordinate="
        f"{rank_mod(profile_span_generators, args.q)}/{args.degree}"
    )
    print(f"profile_one_step_stability_defect={one_step_defect}")
    print(
        "frobenius_closure_rank="
        f"{rank_mod(frobenius_closure_generators, args.q)}/{args.degree}"
    )
    print(
        "normal_coordinate_alone_implies_full_span="
        f"{int(rank_mod(profile_span_generators, args.q) == args.degree)}"
    )
    print(
        "contained_normal_orbit_implies_full_span="
        f"{int(rank_mod(frobenius_closure_generators, args.q) == args.degree)}"
    )
    print(
        "interpretation="
        "normal_coordinate_needs_frobenius_stability_or_orbit_containment"
    )
    print("conclusion=reported_centered_profile_normal_frame_toy")


if __name__ == "__main__":
    main()

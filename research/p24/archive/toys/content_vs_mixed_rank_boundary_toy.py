#!/usr/bin/env python3
"""Toy boundary between packet content and mixed-rank normality.

Surviving relative-content scans support a theorem of the form:

    a right-frequency packet is not identically zero.

The p24 mixed certificate needs much more:

    the centered right profile values span L = F_{p^156}.

This toy constructs a rank-one profile whose right Fourier components are all
nonzero.  It demonstrates that exact packet content/nonzero right Fourier
components do not imply the mixed Moore-rank theorem.
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


def dft(values: list[int], root: int, q: int) -> list[int]:
    n = len(values)
    out: list[int] = []
    for freq in range(n):
        total = 0
        for pos, value in enumerate(values):
            total += value * pow(root, freq * pos, q)
        out.append(total % q)
    return out


def find_primitive_root_of_order(n: int, q: int) -> int:
    for value in range(2, q):
        if pow(value, n, q) != 1:
            continue
        if all(pow(value, d, q) != 1 for d in range(1, n)):
            return value
    raise ValueError("no primitive root of requested order")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=13)
    parser.add_argument("--right", type=int, default=6)
    parser.add_argument("--left-dim", type=int, default=5)
    args = parser.parse_args()

    if (args.q - 1) % args.right != 0:
        raise ValueError("toy requires right | q-1 for a base-field DFT")
    root = find_primitive_root_of_order(args.right, args.q)

    # Choose a scalar right profile whose nonzero Fourier components are all
    # nonzero.  For q=13,right=6, [0,1,2,3,4,5] works after centering.
    scalars = list(range(args.right))
    mean = sum(scalars) * pow(args.right, -1, args.q)
    centered_scalars = [(value - mean) % args.q for value in scalars]
    spectrum = dft(centered_scalars, root, args.q)

    direction = [1] + [0] * (args.left_dim - 1)
    profile = [
        [(scalar * coord) % args.q for coord in direction]
        for scalar in centered_scalars
    ]
    profile_rank = rank_mod(profile, args.q)
    nonzero_frequency_count = sum(1 for value in spectrum[1:] if value % args.q)

    print("Content vs mixed-rank boundary toy")
    print(f"q={args.q}")
    print(f"right={args.right}")
    print(f"left_dim={args.left_dim}")
    print(f"root={root}")
    print(f"centered_scalars={centered_scalars}")
    print(f"nonzero_right_frequency_count={nonzero_frequency_count}/{args.right - 1}")
    print(f"profile_span_rank={profile_rank}/{args.left_dim}")
    print(f"all_nonzero_right_frequencies={int(nonzero_frequency_count == args.right - 1)}")
    print(f"mixed_full_rank={int(profile_rank == args.left_dim)}")
    print(
        "interpretation="
        "nonzero_packet_content_does_not_imply_centered_profile_spans_L"
    )
    print("conclusion=reported_content_vs_mixed_rank_boundary_toy")


if __name__ == "__main__":
    main()

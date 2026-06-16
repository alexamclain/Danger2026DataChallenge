#!/usr/bin/env python3
"""Greedy exact odd trace-residue selector audit for p24.

This is an idealized lattice calculation, not a curve sampler.  It asks how
quickly exact odd trace residues would isolate the six x-only DANGER target
traces after imposing the two 2-adic branches

    t == +/- (p+1) mod 2^d.

The point is to separate arithmetic information content from construction
cost: exact residues can isolate the target traces, but imposing them
constructively requires growing odd modular information.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24 = 10**24 + 7
TARGET_TRACES = tuple(
    sorted({1020608380936, -78903246840, -1178414874616, -1020608380936, 78903246840, 1178414874616})
)


def lattice_traces(d: int) -> list[int]:
    bound = math.isqrt(4 * P24)
    modulus = 1 << d
    residues = {(P24 + 1) % modulus, (-(P24 + 1)) % modulus}
    out: set[int] = set()
    for residue in residues:
        first = -bound + ((residue + bound) % modulus)
        t = first
        while t <= bound:
            out.add(t)
            t += modulus
    return sorted(out)


def target_residues(ell: int) -> set[int]:
    return {t % ell for t in TARGET_TRACES}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, default=28)
    ap.add_argument("--max-ell", type=int, default=200)
    args = ap.parse_args()

    primes = [ell for ell in sp.primerange(3, args.max_ell + 1)]
    survivors = lattice_traces(args.d)
    target_set = set(TARGET_TRACES)
    selected: list[int] = []
    product = 1

    print("p24 greedy exact trace-residue selector audit")
    print(f"p={P24}")
    print(f"d={args.d}")
    print(f"max_ell={args.max_ell}")
    print(f"initial_lattice_count={len(survivors)}")
    print(f"target_traces={TARGET_TRACES}")
    print(f"targets_in_lattice={target_set.issubset(survivors)}")
    print()

    step = 0
    while set(survivors) != target_set:
        best: tuple[int, int, list[int]] | None = None
        for ell in primes:
            if ell in selected:
                continue
            residues = target_residues(ell)
            kept = [t for t in survivors if t % ell in residues]
            row = (len(kept), ell, kept)
            if best is None or row[0] < best[0]:
                best = row

        if best is None or best[0] == len(survivors):
            print("no_further_progress=1")
            break

        kept_count, ell, kept = best
        selected.append(ell)
        product *= ell
        survivors = kept
        step += 1

        print(
            f"step={step} ell={ell} target_residue_count={len(target_residues(ell))} "
            f"survivors={kept_count} product={product}"
        )
        if kept_count <= 20:
            print("  survivor_traces=" + ",".join(str(t) for t in survivors))

    print()
    print(f"selected_ells={selected}")
    print(f"selected_product={product}")
    print(f"final_survivor_count={len(survivors)}")
    print(f"isolated_exact_xonly_targets={set(survivors) == target_set}")
    print("conclusion=exact_residues_are_information_rich_but_only_as_free_oracle_filters")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Measure whether tiny trace-residue filters stack with the nonsplit X1(16) filter.

This is a small-prime calibration helper.  It samples the local X1(16) stream,
classifies each accepted sample by the exact y-level split/nonsplit character,
brute-force counts the Montgomery curve trace, and reports target-residue
survival rates for all/split/nonsplit subclasses.

The purpose is not to build a production filter.  It tests whether a hypothetical
cheap exact trace-residue predicate would still have rejection power after the
active p23 nonsplit filter.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from dataclasses import dataclass

import x16_trace_residue_calibration as cal
import x16_trace_feature_scan as feature_scan


@dataclass(frozen=True)
class Sample:
    cls: str
    trace: int


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def split_class_from_y(y: int, p: int) -> str:
    y %= p
    y2 = y * y % p
    g = (y2 - 2) * (y2 - 4 * y + 2)
    chi = legendre(g, p)
    if chi == 1:
        return "split"
    if chi == -1:
        return "nonsplit"
    return "degenerate"


def summarize_group(name: str, samples: list[Sample], ells: list[int]) -> None:
    traces = [sample.trace for sample in samples]
    print(f"group={name} samples={len(traces)}")
    if not traces:
        return

    for ell in ells:
        residues = {t % ell for t in cal.P23_TRACES}
        counts = Counter(t % ell for t in traces)
        accepted = sum(counts[r] for r in residues)
        rate = accepted / len(traces)
        ideal = len(residues) / ell
        print(
            f"  ell={ell:2d} target_residues={sorted(residues)} "
            f"accepted={accepted:4d}/{len(traces):4d} rate={rate:.4f} "
            f"ideal={ideal:.4f} counts={dict(sorted(counts.items()))}"
        )

    active = [True] * len(traces)
    ideal_product = 1.0
    for ell in ells:
        residues = {t % ell for t in cal.P23_TRACES}
        ideal_product *= len(residues) / ell
        for i, trace in enumerate(traces):
            active[i] = active[i] and (trace % ell in residues)
        survivors = sum(active)
        print(
            f"  cumulative_through_ell={ell:2d} survivors={survivors:4d}/{len(traces):4d} "
            f"rate={survivors / len(traces):.4f} ideal_independent={ideal_product:.4f}"
        )


def run_prime(p: int, samples: int, seed: int, ells: list[int]) -> None:
    rng = random.Random(seed)
    pairs = feature_scan.x16_samples_with_y(p, rng, samples)
    rows: list[Sample] = []
    class_counts: Counter[str] = Counter()

    for y, A in pairs:
        cls = split_class_from_y(y, p)
        trace = cal.trace_for_montgomery_A(p, A)
        rows.append(Sample(cls, trace))
        class_counts[cls] += 1

    print(f"calibration_prime={p}")
    print(f"samples={len(rows)} seed={seed}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in sorted(class_counts)))
    print()

    summarize_group("all", rows, ells)
    print()
    for cls in ("split", "nonsplit"):
        summarize_group(cls, [row for row in rows if row.cls == cls], ells)
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=240)
    parser.add_argument("--starts", type=int, nargs="+", default=[100_000, 200_000, 400_000])
    parser.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11])
    parser.add_argument("--seed", type=int, default=20260607)
    args = parser.parse_args()

    modulus = 8
    for ell in args.ells:
        modulus *= ell

    print("X1(16) nonsplit trace-residue stack probe")
    print(f"p23_mod_modulus={cal.P23 % modulus} modulus={modulus}")
    print(f"ells={args.ells}")
    print()

    for start in args.starts:
        p = cal.find_calibration_prime(start, modulus, cal.P23 % modulus)
        run_prime(p, args.samples, args.seed, args.ells)


if __name__ == "__main__":
    main()

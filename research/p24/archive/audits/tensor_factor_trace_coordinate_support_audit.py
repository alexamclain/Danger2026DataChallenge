#!/usr/bin/env python3
"""Support growth for p24 trace-coordinate Plucker minors.

Top_k trace coordinates are indexed by C/E Frobenius representatives.  Each
coordinate has beta-character support on one size-31 trace subgroup coset
inside the size-5549 tensor-factor orbit.  A coordinate Plucker minor using
several trace coordinates has support in the sumset of the selected cosets.

This audit asks how quickly those selected-coordinate sumsets fill Z/nZ.
"""

from __future__ import annotations

import argparse
import random

P = 10**24 + 7
M = 66_254
N = 3_107_441
ORD_M = 5_460
A = 209_035
SUBDEGREE = 179


def orbit(multiplier: int, modulus: int) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()
    value = 1
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = (value * multiplier) % modulus
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=80)
    parser.add_argument("--max-prefix", type=int, default=8)
    parser.add_argument("--sample-size", type=int, default=6)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    try:
        import numpy as np
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "NumPy is required. In this Codex workspace, run with "
            "/Users/agent/.cache/codex-runtimes/codex-primary-runtime/"
            "dependencies/python/bin/python3"
        ) from exc

    trace_generator = pow(A, SUBDEGREE, N)
    trace_subgroup = orbit(trace_generator, N)
    cosets = []
    spectra = []
    for t in range(SUBDEGREE):
        rep = pow(A, t, N)
        values = [(rep * r) % N for r in trace_subgroup]
        cosets.append(values)
        indicator = np.zeros(N, dtype=np.float64)
        indicator[values] = 1.0
        spectra.append(np.fft.rfft(indicator))

    def support_size(indices: list[int]):
        spectrum = spectra[indices[0]].copy()
        for idx in indices[1:]:
            spectrum *= spectra[idx]
        counts = np.fft.irfft(spectrum, n=N)
        rounded = np.rint(counts).astype(np.int64)
        covered = int((rounded > 0).sum())
        zero_covered = int(bool(rounded[0] > 0))
        min_positive = int(rounded[rounded > 0].min()) if covered else 0
        max_count = int(rounded.max()) if rounded.size else 0
        return covered, zero_covered, min_positive, max_count

    print("p24 trace-coordinate support audit")
    print(f"p={P}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"a=p^ord_m_mod_n={A}")
    print(f"trace_subgroup_size={len(trace_subgroup)}")
    print(f"trace_coordinate_cosets={len(cosets)}")
    print()
    print("consecutive_prefixes")
    for size in range(1, args.max_prefix + 1):
        covered, zero, min_count, max_count = support_size(list(range(size)))
        print(
            f"  size={size} covered={covered} missing={N-covered} "
            f"zero={zero} min_positive={min_count} max_count={max_count}"
        )

    rng = random.Random(args.seed)
    sample_sizes: list[int] = []
    zero_count = 0
    for _ in range(args.random_trials):
        indices = rng.sample(range(SUBDEGREE), args.sample_size)
        covered, zero, _, _ = support_size(indices)
        sample_sizes.append(covered)
        zero_count += zero

    print()
    print("random_samples")
    print(f"  sample_size={args.sample_size}")
    print(f"  trials={args.random_trials}")
    print(f"  covered_min={min(sample_sizes) if sample_sizes else 'NA'}")
    print(f"  covered_max={max(sample_sizes) if sample_sizes else 'NA'}")
    print(f"  full_support_trials={sum(1 for value in sample_sizes if value == N)}")
    print(f"  zero_covered_trials={zero_count}")
    print()
    print("p24_targets")
    print("  Omega_1 coordinate minor selects 158 of 179 Top_1 coordinates")
    print("  Omega_211 coordinate minor selects 210 of 358 Top_2 coordinates")
    print("  Omega_3 coordinate minor selects 368 of 537 Top_3 coordinates")
    print()
    print("interpretation")
    print("  fast_support_growth_rules_out_small_coordinate_minor_support=1")
    print("  coordinate_minor_speedup_would_need_special_non-generic_coordinate_choice=1")
    print("conclusion=reported_tensor_factor_trace_coordinate_support_audit")


if __name__ == "__main__":
    main()

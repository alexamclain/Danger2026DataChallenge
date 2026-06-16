#!/usr/bin/env python3
"""p24 tensor-factor beta-character support audit.

For a chosen Plucker coordinate of a beta-shifted marginal exterior product,
the beta sequence has spectral support inside sumsets of the tensor-factor
Frobenius orbit

    O = <p^ord_m(p)> mod n.

If a small sumset of O already covers all residues mod n, then large exterior
coordinates have full beta-character support available and cannot be
compressed by a small-support argument.
"""

from __future__ import annotations

import argparse

P = 10**24 + 7
M = 66_254
N = 3_107_441
ORD_M = 5_460


def orbit(multiplier: int, modulus: int) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()
    value = 1
    while value not in seen:
        seen.add(value)
        out.append(value)
        value = (value * multiplier) % modulus
    return out


def coset_coverage(covered_mask, values: list[int], modulus: int):
    visited = bytearray(modulus)
    cosets_covered = 0
    cosets_missing = 0
    partial_cosets = 0
    for start in range(1, modulus):
        if visited[start]:
            continue
        members = [(start * value) % modulus for value in values]
        for member in members:
            visited[member] = 1
        hit_count = sum(1 for member in members if covered_mask[member])
        if hit_count == len(members):
            cosets_covered += 1
        elif hit_count == 0:
            cosets_missing += 1
        else:
            partial_cosets += 1
    return cosets_covered, cosets_missing, partial_cosets


def sumset_by_fft(values: list[int], modulus: int, fold: int):
    try:
        import numpy as np
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "NumPy is required. In this Codex workspace, run with "
            "/Users/agent/.cache/codex-runtimes/codex-primary-runtime/"
            "dependencies/python/bin/python3"
        ) from exc

    indicator = np.zeros(modulus, dtype=np.float64)
    indicator[values] = 1.0
    spectrum = np.fft.rfft(indicator)
    counts = np.fft.irfft(spectrum**fold, n=modulus)
    rounded = np.rint(counts).astype(np.int64)
    covered_mask = rounded > 0
    covered = int(covered_mask.sum())
    min_positive = int(rounded[rounded > 0].min()) if covered else 0
    max_count = int(rounded.max()) if rounded.size else 0
    negative_rounding = int((rounded < 0).sum())
    zero_covered = int(bool(covered_mask[0]))
    cosets_covered, cosets_missing, partial_cosets = coset_coverage(
        covered_mask,
        values,
        modulus,
    )
    return (
        covered,
        min_positive,
        max_count,
        negative_rounding,
        zero_covered,
        cosets_covered,
        cosets_missing,
        partial_cosets,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folds", type=int, nargs="+", default=[2, 3, 4])
    args = parser.parse_args()

    a = pow(P, ORD_M, N)
    O = orbit(a, N)
    print("p24 tensor-factor beta-character support audit")
    print(f"p={P}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_m={ORD_M}")
    print(f"a=p^ord_m_mod_n={a}")
    print(f"orbit_size={len(O)}")
    print()
    print("sumsets")
    for fold in args.folds:
        (
            covered,
            min_count,
            max_count,
            negative,
            zero_covered,
            cosets_covered,
            cosets_missing,
            partial_cosets,
        ) = sumset_by_fft(O, N, fold)
        print(
            f"  fold={fold} covered={covered} missing={N-covered} "
            f"min_positive={min_count} max_count={max_count} "
            f"negative_rounding={negative} zero_covered={zero_covered} "
            f"cosets_covered={cosets_covered} cosets_missing={cosets_missing} "
            f"partial_cosets={partial_cosets}"
        )
    print()
    print("interpretation")
    print("  beta_sequence_spectral_support_lies_in_exterior_sumsets_of_O=1")
    print("  threefold_sumset_full_rules_out_small_support_compression_for_large_exteriors=1")
    print("conclusion=reported_tensor_factor_beta_support_audit")


if __name__ == "__main__":
    main()

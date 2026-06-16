#!/usr/bin/env python3
"""Additive support audit for exterior-power packet characters.

For a packet factor of `Phi_n`, the eigencharacters of multiplication by `X`
are a Frobenius orbit

    H = <q> in (Z/nZ)^*.

In the exterior-power view of the coefficient-minor route, beta-shifted
Pluecker coordinates can involve sums of packet exponents.  If even `H+H`
covers all residues modulo `n`, then the exterior representation already has
full cyclic character support available.  That rules out a character-support
or low-recurrence compression explanation for the sliding-window product.

For p24, `n=3107441` and `|H|=388430`; the exact circular convolution is small
enough with NumPy from the bundled workspace runtime.
"""

from __future__ import annotations

import argparse
import math


P24 = 10**24 + 7
N24 = 3_107_441
ORD_N24_P24 = 388_430


def orbit(generator: int, modulus: int) -> list[int]:
    values: list[int] = []
    x = 1
    seen: set[int] = set()
    while x not in seen:
        seen.add(x)
        values.append(x)
        x = (x * generator) % modulus
    return values


def exact_sumset_by_fft(values: list[int], modulus: int) -> tuple[int, int, int, int]:
    try:
        import numpy as np
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "NumPy is required; use the bundled workspace Python from "
            "codex_app.load_workspace_dependencies"
        ) from exc

    indicator = np.zeros(modulus, dtype=np.float64)
    indicator[values] = 1.0
    spectrum = np.fft.rfft(indicator)
    counts = np.fft.irfft(spectrum * spectrum, n=modulus)
    rounded = np.rint(counts).astype(np.int64)
    negative_rounding = int((rounded < 0).sum())
    covered = int((rounded > 0).sum())
    min_positive = int(rounded[rounded > 0].min()) if covered else 0
    max_count = int(rounded.max()) if rounded.size else 0
    return covered, min_positive, max_count, negative_rounding


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=N24)
    parser.add_argument("--q", type=int, default=P24 % N24)
    parser.add_argument("--expected-order", type=int, default=ORD_N24_P24)
    args = parser.parse_args()

    H = orbit(args.q % args.n, args.n)
    index = (args.n - 1) // len(H) if args.n > 1 else 0
    covered, min_count, max_count, negative = exact_sumset_by_fft(H, args.n)

    print("exterior character-support sumset audit")
    print(f"n={args.n}")
    print(f"q_mod_n={args.q % args.n}")
    print(f"orbit_size={len(H)}")
    print(f"expected_order={args.expected_order}")
    print(f"order_matches_expected={int(len(H) == args.expected_order)}")
    print(f"multiplicative_index={(args.n - 1) // len(H)}")
    print()
    print("two_sumset")
    print(f"  covered_residues={covered}")
    print(f"  modulus={args.n}")
    print(f"  full_coverage={int(covered == args.n)}")
    print(f"  min_ordered_pair_count={min_count}")
    print(f"  max_ordered_pair_count={max_count}")
    print(f"  negative_rounding_count={negative}")
    print(f"  density={covered / args.n:.12f}")
    print()
    print("interpretation")
    print("  H_plus_H_full_means_exterior_characters_can_have_full_beta_support=1")
    print("  full_support_rules_out_small_character_support_compression=1")
    print("conclusion=reported_exterior_character_support_audit")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Toy verifier for the harmful-dual-coset relative-resolvent lemma.

The toy works over a prime field with all h-th roots of unity present, so the
Fourier equivalence can be checked exactly without extension arithmetic.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError(f"order {order} does not divide q-1={q - 1}")
    root = pow(sp.primitive_root(q), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("root has wrong order")
    for prime in sp.factorint(order):
        if pow(root, order // prime, q) == 1:
            raise AssertionError("root is not primitive")
    return int(root)


def dft(values: list[int], q: int, zeta: int) -> list[int]:
    h = len(values)
    out: list[int] = []
    for s in range(h):
        total = 0
        for i, value in enumerate(values):
            total = (total + value * pow(zeta, s * i, q)) % q
        out.append(total)
    return out


def inverse_dft(spectrum: list[int], q: int, zeta: int) -> list[int]:
    h = len(spectrum)
    inv_h = pow(h, -1, q)
    out: list[int] = []
    for i in range(h):
        total = 0
        for s, value in enumerate(spectrum):
            total = (total + value * pow(zeta, (-s * i) % h, q)) % q
        out.append((inv_h * total) % q)
    return out


def relative_sums(values: list[int], q: int, zeta_h: int, m: int, a: int) -> list[int]:
    h = len(values)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    out: list[int] = []
    for u in range(m):
        total = 0
        for k in range(n):
            total = (total + pow(zeta_n, a * k, q) * values[u + m * k]) % q
        out.append(total)
    return out


def coset_indices(h: int, m: int, a: int) -> list[int]:
    n = h // m
    return [int((a + r * n) % h) for r in range(m)]


def inverse_indicator_support(q: int, h: int, m: int, a: int, zeta: int) -> list[int]:
    indicator = [0] * h
    for s in coset_indices(h, m, a):
        indicator[s] = 1
    word = inverse_dft(indicator, q, zeta)
    return [i for i, value in enumerate(word) if value % q]


def projector(h: int, m: int) -> list[int]:
    n = h // m
    out = [0] * h
    for k in range(n):
        out[m * k] = 1
    return out


def weight(values: list[int], q: int) -> int:
    return sum(1 for value in values if value % q)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=31)
    ap.add_argument("--h", type=int, default=30)
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--a", type=int, default=1)
    args = ap.parse_args()

    q = args.q
    h = args.h
    m = args.m
    if h % m:
        raise ValueError("m must divide h")
    n = h // m
    if args.a % n == 0:
        raise ValueError("choose a non-quotient coset, i.e. a not 0 mod n")

    zeta = primitive_root_of_order(q, h)
    coset = coset_indices(h, m, args.a)

    spectrum = [(7 + 3 * s + s * s) % q for s in range(h)]
    for s in coset:
        spectrum[s] = 0
    values = inverse_dft(spectrum, q, zeta)
    recovered_spectrum = dft(values, q, zeta)
    if recovered_spectrum != spectrum:
        raise AssertionError("DFT inversion failed")

    rel = relative_sums(values, q, zeta, m, args.a)
    other_a = 2 if n > 2 and args.a % n != 2 else 1
    other_rel = relative_sums(values, q, zeta, m, other_a)
    support = inverse_indicator_support(q, h, m, args.a, zeta)

    e_h = projector(h, m)
    one_character_word = inverse_dft([1 if s in coset else 0 for s in range(h)], q, zeta)
    best = h + 1
    for scalar in range(q):
        candidate = [(x + scalar * y) % q for x, y in zip(e_h, one_character_word)]
        best = min(best, weight(candidate, q))

    print("harmful dual-coset relative toy")
    print(f"q={q}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"a={args.a % n}")
    print(f"primitive_h_root={zeta}")
    print(f"dual_coset={coset}")
    print(f"forced_coset_resolvents_zero={all(recovered_spectrum[s] == 0 for s in coset)}")
    print(f"relative_sums={rel}")
    print(f"relative_sums_zero={all(value == 0 for value in rel)}")
    print(f"other_a={other_a}")
    print(f"other_relative_sums_zero={all(value == 0 for value in other_rel)}")
    print(f"inverse_indicator_support={support}")
    print(f"expected_H_support={[m * k for k in range(n)]}")
    print(f"gcd_a_n={math.gcd(args.a, n)}")
    print(f"projector_weight={weight(e_h, q)}")
    print(f"best_weight_after_one_character_coset={best}")
    print()
    print("interpretation")
    print("  full_dual_coset_vanishing_equals_fiberwise_relative_vanishing=1")
    print("  inverse_coset_word_is_supported_on_H=1")
    print("  one_imprimitive_character_cancels_gcd_a_n_projector_positions=1")
    print("conclusion=reported_harmful_dual_coset_relative_toy")


if __name__ == "__main__":
    main()

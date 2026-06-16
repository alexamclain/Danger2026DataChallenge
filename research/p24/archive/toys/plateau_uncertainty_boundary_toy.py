#!/usr/bin/env python3
"""Toy boundary for plateau/uncertainty shortcuts.

If a right-window determinant vanishes, some nonzero dual word is constant on
a long interval.  Subtracting that constant gives a sparse word.  Prime cyclic
uncertainty only says

    support_time + support_frequency >= right + 1.

This toy builds sparse zero-sum words whose nonzero Fourier support is full,
so the uncertainty bound does not contradict a long plateau.
"""

from __future__ import annotations

import argparse
import itertools
import random

import sympy as sp


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1")
    generator = int(sp.primitive_root(q))
    root = pow(generator, (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise AssertionError("bad root")
    for prime in sp.factorint(order):
        if pow(root, order // int(prime), q) == 1:
            raise AssertionError("root is not primitive")
    return root


def dft(word: list[int], root: int, q: int) -> list[int]:
    n = len(word)
    out: list[int] = []
    for frequency in range(n):
        total = 0
        for t, value in enumerate(word):
            total = (total + value * pow(root, (-frequency * t) % n, q)) % q
        out.append(total)
    return out


def find_example(
    length: int,
    plateau: int,
    q: int,
    trials: int,
    seed: int,
) -> tuple[list[int], list[int]]:
    rng = random.Random(seed)
    complement = list(range(plateau, length))
    support_size = len(complement)
    root = primitive_root_of_order(q, length)
    for _ in range(trials):
        values = [rng.randrange(1, q) for _ in range(support_size - 1)]
        values.append((-sum(values)) % q)
        if values[-1] == 0:
            continue
        rng.shuffle(values)
        sparse = [0 for _ in range(length)]
        for index, value in zip(complement, values):
            sparse[index] = value
        spectrum = dft(sparse, root, q)
        if spectrum[0] == 0 and all(spectrum[f] != 0 for f in range(1, length)):
            word = [(7 + value) % q for value in sparse]
            return word, spectrum
    raise RuntimeError("no example found; increase trials")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=13)
    parser.add_argument("--plateau", type=int, default=8)
    parser.add_argument("--q", type=int, default=53)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    word, spectrum = find_example(
        args.length,
        args.plateau,
        args.q,
        args.trials,
        args.seed,
    )
    constant = word[0]
    sparse = [(value - constant) % args.q for value in word]
    time_support = sum(1 for value in sparse if value)
    freq_support = sum(1 for value in spectrum if value)
    plateau_ok = all(word[t] == constant for t in range(args.plateau))

    print("Plateau uncertainty boundary toy")
    print(f"q={args.q}")
    print(f"length={args.length}")
    print(f"plateau={args.plateau}")
    print(f"time_support_after_subtracting_constant={time_support}")
    print(f"frequency_support_after_subtracting_constant={freq_support}")
    print(f"uncertainty_sum={time_support + freq_support}")
    print(f"uncertainty_threshold={args.length + 1}")
    print(f"plateau_constant={constant}")
    print(f"plateau_ok={int(plateau_ok)}")
    print(f"zero_frequency_absent={int(spectrum[0] == 0)}")
    print(
        "nonzero_frequency_support_full="
        f"{int(all(spectrum[f] != 0 for f in range(1, args.length)))}"
    )
    print(f"word={word}")
    print()
    print("interpretation")
    print("  long_plateau_can_coexist_with_full_nonzero_fourier_support=1")
    print("  prime_cyclic_uncertainty_alone_does_not_prove_pi_c_right=1")
    print("conclusion=reported_plateau_uncertainty_boundary_toy")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Counterexample to an over-broad cyclic-code support theorem.

Single packet vanishings did not lower projector support in the earlier toys,
and the actual small CM failures also kept the projector minimum.  But a
purely group-theoretic theorem is false: a structured multi-packet
annihilator can make the coset e_H + Ann contain a word below |H|.

This script gives the smallest example I found.
"""

from __future__ import annotations

import itertools

import sympy as sp

T = sp.symbols("T")


def coeff_vector(poly: sp.Poly, h: int, q: int) -> list[int]:
    out = [0] * h
    for (power,), coeff in poly.as_dict().items():
        out[power % h] = (out[power % h] + int(coeff)) % q
    return out


def shift(values: list[int], amount: int) -> list[int]:
    h = len(values)
    out = [0] * h
    for i, value in enumerate(values):
        out[(i + amount) % h] = value
    return out


def weight(values: list[int], q: int) -> int:
    return sum(1 for value in values if value % q)


def projector(h: int, quotient_size: int) -> list[int]:
    subgroup_size = h // quotient_size
    out = [0] * h
    for k in range(subgroup_size):
        out[(quotient_size * k) % h] = 1
    return out


def dft(values: list[int], q: int, zeta: int) -> list[int]:
    h = len(values)
    out = []
    for s in range(h):
        total = 0
        for i, value in enumerate(values):
            total = (total + value * pow(zeta, s * i, q)) % q
        out.append(total)
    return out


def main() -> None:
    h = 6
    q = 7
    quotient_size = 2
    subgroup_size = h // quotient_size
    quotient_characters = {0, subgroup_size}

    zeta = pow(sp.primitive_root(q), (q - 1) // h, q)
    vanished_characters = (1, 4)

    torsion = sp.Poly(T**h - 1, T, modulus=q)
    vanished_factor = sp.Poly(1, T, modulus=q)
    for s in vanished_characters:
        vanished_factor *= sp.Poly(T - pow(zeta, s, q), T, modulus=q)
    annihilator_generator, remainder = torsion.div(vanished_factor)
    if not remainder.is_zero:
        raise AssertionError(vanished_factor)

    e_h = projector(h, quotient_size)
    generator = coeff_vector(annihilator_generator, h, q)
    basis = [generator, shift(generator, 1)]

    best_weight = h + 1
    best_coeffs: tuple[int, int] | None = None
    best_word: list[int] | None = None
    for a, b in itertools.product(range(q), repeat=2):
        candidate = [
            (x + a * y + b * z) % q
            for x, y, z in zip(e_h, basis[0], basis[1])
        ]
        current = weight(candidate, q)
        if current < best_weight:
            best_weight = current
            best_coeffs = (a, b)
            best_word = candidate

    if best_word is None or best_coeffs is None:
        raise AssertionError("no best word")

    print("cyclic-code min-weight counterexample")
    print(f"q={q}")
    print(f"h={h}")
    print(f"quotient_size={quotient_size}")
    print(f"subgroup_size={subgroup_size}")
    print(f"primitive_h_root={zeta}")
    print(f"quotient_characters={sorted(quotient_characters)}")
    print(f"vanished_nonquotient_characters={list(vanished_characters)}")
    print(f"vanished_factor={vanished_factor.as_expr()}")
    print(f"annihilator_generator={annihilator_generator.as_expr()}")
    print(f"projector={e_h}")
    print(f"projector_weight={weight(e_h, q)}")
    print(f"best_coeffs={list(best_coeffs)}")
    print(f"best_word={best_word}")
    print(f"best_weight={best_weight}")
    print(f"projector_spectrum={dft(e_h, q, zeta)}")
    print(f"best_word_spectrum={dft(best_word, q, zeta)}")
    print()
    print("interpretation")
    print("  quotient_characters_do_not_vanish=1")
    print("  vanished_characters_are_proper_nonquotient_subset=1")
    print("  affine_code_coset_has_weight_below_projector=1")
    print("  pure_group_theoretic_min_weight_theorem_is_false=1")
    print("conclusion=p24_min_weight_theorem_needs_arithmetic_CM_annihilator_input")


if __name__ == "__main__":
    main()

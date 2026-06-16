#!/usr/bin/env python3
"""Toy counterexamples for too-weak reduced-normality lemmas.

The p24 support theorem needs the cyclic translate matrix of the reduced CM
root vector to be invertible.  This script shows that several nearby facts are
strictly weaker:

* the polynomial with these entries as roots can be split and squarefree;
* the entries can be distinct, so the vector separates the split algebra;
* the acting group can have order prime to the characteristic.

Those hypotheses still do not force all Fourier/class-character components to
be nonzero.
"""

from __future__ import annotations

import itertools

import sympy as sp


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError((q, order))
    root = pow(sp.primitive_root(q), (q - 1) // order, q)
    if pow(root, order, q) != 1:
        raise ValueError((q, order, root))
    for ell in sp.factorint(order):
        if pow(root, order // ell, q) == 1:
            raise ValueError((q, order, root, ell))
    return int(root)


def dft(values: tuple[int, ...], q: int) -> list[int]:
    h = len(values)
    zeta = primitive_root_of_order(q, h)
    out: list[int] = []
    for s in range(h):
        total = 0
        for i, value in enumerate(values):
            total = (total + value * pow(zeta, s * i, q)) % q
        out.append(total)
    return out


def polynomial_coefficients(values: tuple[int, ...], q: int) -> list[int]:
    x = sp.symbols("x")
    poly = sp.Poly(1, x, modulus=q)
    for value in values:
        poly *= sp.Poly(x - value, x, modulus=q)
    return [int(c) % q for c in poly.all_coeffs()]


def find_example(q: int, h: int) -> tuple[int, ...]:
    zeta = primitive_root_of_order(q, h)
    for values in itertools.permutations(range(q), h):
        if len(set(values)) != h:
            continue
        if sum(values[i] * pow(zeta, i, q) for i in range(h)) % q == 0:
            return tuple(int(v) for v in values)
    raise RuntimeError((q, h))


def main() -> None:
    q = 11
    h = 5
    values = find_example(q, h)
    spectrum = dft(values, q)
    coeffs = polynomial_coefficients(values, q)
    zero_characters = [i for i, value in enumerate(spectrum) if value == 0]

    print("reduced-normality false-lemmas toy")
    print(f"q={q}")
    print(f"h={h}")
    print(f"gcd(h,q)={sp.gcd(h, q)}")
    print(f"primitive_h_root={primitive_root_of_order(q, h)}")
    print(f"distinct_values={list(values)}")
    print(f"split_squarefree_polynomial_coeffs={coeffs}")
    print(f"dft_spectrum={spectrum}")
    print(f"zero_character_indices={zero_characters}")
    print()
    print("interpretation")
    print("  split_squarefree_roots_do_not_imply_reduced_normality=1")
    print("  primitive_element_for_the_split_etale_algebra_is_not_enough=1")
    print("  a_p24_proof_must_control_the_normal_determinant_at_the_chosen_prime=1")
    print("conclusion=reported_false_lemma_counterexample")


if __name__ == "__main__":
    main()

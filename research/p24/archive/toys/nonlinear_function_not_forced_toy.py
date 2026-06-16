#!/usr/bin/env python3
"""Tiny Fourier toy: linear packet collapse does not force nonlinear collapse.

This is the finite-algebra warning behind the ell=677 Atkin/gonality
boundary.  Relative-content collapse says a character component of the
`j`-vector is zero.  It does not imply that the same character component of an
arbitrary nonlinear function of `j` is zero.
"""

from __future__ import annotations


def character_sum(values: list[int], zeta: int, q: int) -> int:
    total = 0
    power = 1
    for value in values:
        total = (total + power * value) % q
        power = power * zeta % q
    return total


def main() -> None:
    q = 7
    zeta = 2  # primitive third root in F_7
    values = [5, 1, 0]
    squares = [value * value % q for value in values]

    print("nonlinear function not forced by linear content toy")
    print(f"q={q}")
    print(f"n={len(values)}")
    print(f"zeta={zeta}")
    print(f"values={values}")
    print(f"squares={squares}")
    print(f"linear_character_sum={character_sum(values, zeta, q)}")
    print(f"square_character_sum={character_sum(squares, zeta, q)}")
    print()
    print("interpretation")
    print("  linear_content_character_component_zero=1")
    print("  nonlinear_same_character_component_zero=0")
    print("  arbitrary_low_degree_modular_functions_are_not_forced_by_content_collapse=1")


if __name__ == "__main__":
    main()

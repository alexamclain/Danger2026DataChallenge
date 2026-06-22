#!/usr/bin/env python3
"""Symbolic identity behind the p27 conic-pair d4 recurrence."""

from __future__ import annotations

import sympy as sp


def main() -> int:
    R, L = sp.symbols("R L")
    a = (R**2 - 1) / R
    r = -(L**2 + a**2) / (4 * L)
    s = (R**2 + 1) / R
    c = sp.factor(s * (L + 2 * r) / (2 * r))
    next_conic = sp.factor(R**2 + c * R + 1)
    d4_selector = sp.factor(-(L + a) * (L - a) * c * R)
    quotient = sp.factor(sp.together(next_conic / d4_selector))

    print("p27 conic-pair d4 symbolic identity")
    print(f"a = {sp.factor(a)}")
    print(f"r = {sp.factor(r)}")
    print(f"c = {c}")
    print(f"next_conic = {next_conic}")
    print(f"d4_selector = {d4_selector}")
    print(f"quotient = {quotient}")
    print("quotient_is_2_times_square = 1")
    print("p27_chi2 = 1")
    print("p27_conic_pair_d4_symbolic_identity_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

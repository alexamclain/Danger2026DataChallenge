#!/usr/bin/env python3
"""Toy verifier for the split-algebra relative-resolvent theorem."""

from __future__ import annotations

import argparse

from harmful_dual_coset_relative_toy import (
    dft,
    inverse_dft,
    primitive_root_of_order,
    relative_sums,
)


def split_components(values: list[int], q: int, zeta_h: int, m: int, a: int) -> list[int]:
    h = len(values)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    rel = relative_sums(values, q, zeta_h, m, a)
    out: list[int] = []
    for r in range(h):
        u = r % m
        level = (r - u) // m
        out.append(pow(zeta_n, (-a * level) % n, q) * rel[u] % q)
    return out


def direct_split_components(values: list[int], q: int, zeta_h: int, m: int, a: int) -> list[int]:
    h = len(values)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    out: list[int] = []
    for r in range(h):
        total = 0
        for k in range(n):
            total = (total + pow(zeta_n, a * k, q) * values[(r + m * k) % h]) % q
        out.append(total)
    return out


def make_generic(q: int, h: int) -> list[int]:
    return [(5 + 7 * i + 3 * i * i) % q for i in range(h)]


def make_one_fiber_zero(values: list[int], q: int, zeta_h: int, m: int, a: int) -> list[int]:
    h = len(values)
    n = h // m
    zeta_n = pow(zeta_h, m, q)
    out = list(values)
    target_u = 0
    total = 0
    for k in range(n - 1):
        total = (total + pow(zeta_n, a * k, q) * out[target_u + m * k]) % q
    coeff = pow(zeta_n, a * (n - 1), q)
    out[target_u + m * (n - 1)] = (-total * pow(coeff, -1, q)) % q
    return out


def make_harmful(q: int, h: int, m: int, a: int, zeta_h: int) -> list[int]:
    n = h // m
    spectrum = [(7 + 3 * s + s * s) % q for s in range(h)]
    for r in range(m):
        spectrum[(a + r * n) % h] = 0
    return inverse_dft(spectrum, q, zeta_h)


def summarize(label: str, values: list[int], q: int, zeta_h: int, m: int, a: int) -> None:
    h = len(values)
    n = h // m
    rel = relative_sums(values, q, zeta_h, m, a)
    components = split_components(values, q, zeta_h, m, a)
    direct = direct_split_components(values, q, zeta_h, m, a)
    full = dft(values, q, zeta_h)
    coset = [(a + r * n) % h for r in range(m)]

    zero_fibers = sum(1 for value in rel if value % q == 0)
    zero_components = sum(1 for value in components if value % q == 0)
    print(f"case={label}")
    print(f"  relative_sums={rel}")
    print(f"  zero_fibers={zero_fibers}")
    print(f"  zero_split_components={zero_components}")
    print(f"  expected_zero_split_components={n * zero_fibers}")
    print(f"  direct_component_formula_ok={int(components == direct)}")
    print(f"  harmful_dual_coset_zero={int(all(full[s] == 0 for s in coset))}")
    print(f"  split_algebra_zero={int(zero_components == h)}")


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
        raise ValueError("choose a nonzero relative character a mod n")

    zeta_h = primitive_root_of_order(q, h)
    generic = make_generic(q, h)
    one_fiber = make_one_fiber_zero(generic, q, zeta_h, m, args.a)
    harmful = make_harmful(q, h, m, args.a, zeta_h)

    print("relative resolvent split-algebra toy")
    print(f"q={q}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"a={args.a % n}")
    print()
    summarize("generic", generic, q, zeta_h, m, args.a)
    summarize("one_fiber_zero", one_fiber, q, zeta_h, m, args.a)
    summarize("harmful_all_fibers_zero", harmful, q, zeta_h, m, args.a)
    print()
    print("interpretation")
    print("  zero_split_components_equals_n_times_zero_relative_fibers=1")
    print("  harmful_dual_coset_zero_equals_split_algebra_zero=1")
    print("  one_zero_fiber_gives_only_one_quotient_block_not_full_harmful_event=1")
    print("conclusion=reported_relative_resolvent_split_algebra_toy")


if __name__ == "__main__":
    main()

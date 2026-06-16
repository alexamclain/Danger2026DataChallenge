#!/usr/bin/env python3
"""Show that relative products are not dual-coset group-determinant factors."""

from __future__ import annotations

import argparse

import sympy as sp

from harmful_dual_coset_relative_toy import dft, primitive_root_of_order, relative_sums


def product(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def determinant_dft(order: int, q: int, root: int) -> int:
    matrix = sp.Matrix([[pow(root, r * u, q) for u in range(order)] for r in range(order)])
    return int(matrix.det()) % q


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
    zeta_h = primitive_root_of_order(q, h)
    zeta_m = pow(zeta_h, n, q)

    values = [(5 + 7 * i + 3 * i * i) % q for i in range(h)]
    full = dft(values, q, zeta_h)
    rel = relative_sums(values, q, zeta_h, m, args.a)
    coset = [(args.a + r * n) % h for r in range(m)]

    product_full = product([full[s] for s in coset], q)
    product_relative = product(rel, q)
    det = determinant_dft(m, q, zeta_m)

    print("relative product noninvariance toy")
    print(f"q={q}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"a={args.a}")
    print(f"dual_coset={coset}")
    print(f"det_dft={det}")
    print(f"product_full_resolvents={product_full}")
    print(f"product_relative_fibers={product_relative}")
    print(f"naive_unit_relation_holds={int(product_full == det * product_relative % q)}")
    print(f"full_vector_zero={int(all(full[s] == 0 for s in coset))}")
    print(f"relative_vector_zero={int(all(value == 0 for value in rel))}")
    print(f"full_coset_all_nonzero={int(all(full[s] % q for s in coset))}")
    print(f"relative_fibers_all_nonzero={int(all(value % q for value in rel))}")
    print()
    print("interpretation")
    print("  fourier_transform_preserves_zero_vector_not_coordinate_products=1")
    print("  relative_product_and_group_determinant_product_are_distinct=1")
    print("conclusion=reported_relative_product_noninvariance_toy")


if __name__ == "__main__":
    main()

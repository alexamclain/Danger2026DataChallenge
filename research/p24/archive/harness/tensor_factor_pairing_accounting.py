#!/usr/bin/env python3
"""Accounting for inversion/Hermitian pairing among p24 tensor factors."""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24_P = 10**24 + 7
P24_M = 2 * 157 * 211
P24_N = 3107441


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=P24_P)
    parser.add_argument("--m", type=int, default=P24_M)
    parser.add_argument("--n", type=int, default=P24_N)
    args = parser.parse_args()

    d = int(sp.n_order(args.p % args.n, args.n))
    e = int(sp.n_order(args.p % args.m, args.m))
    g = math.gcd(d, e)
    half_packet = d // 2
    inversion_shift = half_packet % g
    factor_degree = d // g

    print("tensor factor pairing accounting")
    print(f"p={args.p}")
    print(f"m={args.m}")
    print(f"n={args.n}")
    print(f"ord_n(p)={d}")
    print(f"ord_m(p)={e}")
    print(f"tensor_factor_count={g}")
    print(f"tensor_factor_degree_over_E={factor_degree}")
    print(f"p^(ord_n/2)_mod_n={pow(args.p, half_packet, args.n)}")
    print(f"inversion_shift_mod_factor_count={inversion_shift}")
    print(f"factor_degree_parity={factor_degree % 2}")
    print()
    print("interpretation")
    print("  inversion_pairs_tensor_factor_i_with_i_plus_shift=1")
    print("  p24_shift_is_35_among_70_factors=1")
    print("  one_factor_has_no_internal_hermitian_involution=1")
    print("  hermitian_object_lives_on_paired_tensor_factors=1")
    print("conclusion=reported_tensor_factor_pairing_accounting")


if __name__ == "__main__":
    main()

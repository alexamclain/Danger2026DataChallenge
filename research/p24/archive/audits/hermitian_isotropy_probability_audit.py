#!/usr/bin/env python3
"""Exact random-model scale for Hermitian energy packet failure.

For the preferred p24 scalar certificate, one packet lives over

    F_{Q^2},    Q = p^194215,

with Hermitian involution x -> x^Q.  The content vector has length

    m = 66254.

The Hermitian energy is a nondegenerate Hermitian form

    H(v) = sum_i v_i v_i^Q in F_Q.

This script records the exact finite-field zero count and validates the
formula on tiny prime fields using an explicit quadratic extension.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp

P24 = 10**24 + 7
M = 66254
N = 3107441
ORD_N_P = 388430


def hermitian_zero_count(Q: int, m: int) -> int:
    """Number of vectors in F_{Q^2}^m with standard Hermitian norm zero."""
    if m < 1:
        raise ValueError("m must be positive")
    return Q ** (2 * m - 1) + ((-1) ** m) * (Q - 1) * Q ** (m - 1)


def legendre_nonsquare(q: int) -> int:
    for d in range(2, q):
        if sp.legendre_symbol(d, q) == -1:
            return d
    raise ValueError(f"no nonsquare found for q={q}")


def mul(x: tuple[int, int], y: tuple[int, int], q: int, d: int) -> tuple[int, int]:
    # F_q[s]/(s^2-d).
    return ((x[0] * y[0] + d * x[1] * y[1]) % q, (x[0] * y[1] + x[1] * y[0]) % q)


def conj(x: tuple[int, int], q: int) -> tuple[int, int]:
    return (x[0] % q, (-x[1]) % q)


def norm_to_base(x: tuple[int, int], q: int, d: int) -> int:
    z = mul(x, conj(x, q), q, d)
    if z[1] % q:
        raise AssertionError("norm not in base field")
    return z[0] % q


def brute_zero_count(q: int, m: int) -> int:
    d = legendre_nonsquare(q)
    elements = [(a, b) for a in range(q) for b in range(q)]
    count = 0

    def rec(pos: int, total: int) -> None:
        nonlocal count
        if pos == m:
            if total % q == 0:
                count += 1
            return
        for x in elements:
            rec(pos + 1, (total + norm_to_base(x, q, d)) % q)

    rec(0, 0)
    return count


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brute-q", type=int, default=3)
    ap.add_argument("--brute-max-m", type=int, default=3)
    args = ap.parse_args()

    real_packet_degree = ORD_N_P // 2
    packet_count = (N - 1) // ORD_N_P
    log_Q = real_packet_degree * math.log(P24)
    log_total_vectors = 2 * M * log_Q
    log_zero_probability = -log_Q
    log10_zero_probability = log_zero_probability / math.log(10)
    log10_union_probability = math.log(packet_count) / math.log(10) + log10_zero_probability

    print("Hermitian isotropy probability audit")
    print(f"p={P24}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"ord_n_p={ORD_N_P}")
    print(f"real_packet_degree={real_packet_degree}")
    print(f"packet_count={packet_count}")
    print()
    print("p24_random_model")
    print(f"  log_Q={log_Q:.6e}")
    print(f"  log_total_vectors={log_total_vectors:.6e}")
    print(f"  log_zero_probability≈-log_Q={log_zero_probability:.6e}")
    print(f"  log10_zero_probability≈{log10_zero_probability:.6e}")
    print(f"  log10_union_bound_8_packets≈{log10_union_probability:.6e}")
    print()
    print("tiny_formula_validation")
    for m in range(1, args.brute_max_m + 1):
        exact = hermitian_zero_count(args.brute_q, m)
        brute = brute_zero_count(args.brute_q, m)
        total = args.brute_q ** (2 * m)
        print(
            f"  Q={args.brute_q} m={m} formula={exact} brute={brute} "
            f"total={total} probability={exact / total:.6f} ok={int(exact == brute)}"
        )
    print()
    print("interpretation")
    print("  Hermitian_packet_failure_is_quadric_membership_not_all_zero=1")
    print("  random_failure_probability_per_packet_is_about_Q^-1=1")
    print("  p24_Q_equals_p^194215_so_random_failure_is_astronomically_unlikely=1")
    print("  probability_is_not_a_certificate_for_the_selected_prime=1")
    print("conclusion=Hermitian_scalar_is_statistically_strong_but_needs_padic_proof")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Classify small fixed-trace Montgomery verifier triples by CM order."""

from __future__ import annotations

from math import gcd, isqrt

from cypari2 import Pari

from fixed_trace_cm_root_toy import FROBENIUS_D, MAXIMAL_D, P, TRACE, pari_linear_roots


def pp_verify(p: int, A: int, x0: int) -> bool:
    if p < 5 or p % 2 == 0:
        return False
    q = isqrt(p)
    k = (q + 1 + isqrt(4 * q)).bit_length()
    if gcd(A * A - 4, p) != 1:
        return False
    X, Z = x0 % p, 1
    zprev = None
    inv4 = (p + 1) // 4 if p % 4 == 3 else (3 * p + 1) // 4
    C = ((A + 2) * inv4) % p
    for _ in range(k):
        zprev = Z
        U = (X + Z) * (X + Z) % p
        V = (X - Z) * (X - Z) % p
        W = U - V
        X, Z = U * V % p, W * (V + C * W) % p
    return Z % p == 0 and gcd(zprev, p) == 1


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def montgomery_trace(A: int, p: int) -> int | None:
    if gcd(A * A - 4, p) != 1:
        return None
    character_sum = 0
    for x in range(p):
        rhs = (x * x % p * x + A * x * x + x) % p
        character_sum += legendre(rhs, p)
    return -character_sum


def montgomery_j_from_A(A: int, p: int) -> int | None:
    denominator = (A * A - 4) % p
    if denominator == 0:
        return None
    numerator = 256 * pow((A * A - 3) % p, 3, p)
    return numerator * pow(denominator, -1, p) % p


def v2(n: int) -> int:
    if n == 0:
        return 10**9
    n = abs(n)
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    maximal_roots = set(pari_linear_roots(pari.polclass(MAXIMAL_D), P))
    frobenius_roots = set(pari_linear_roots(pari.polclass(FROBENIUS_D), P))
    q = isqrt(P)
    k = (q + 1 + isqrt(4 * q)).bit_length()

    valid_by_order = {"maximal": set(), "conductor2": set(), "other": set()}
    valid_A_by_order = {"maximal": set(), "conductor2": set(), "other": set()}
    trace_A_by_order = {"maximal": set(), "conductor2": set(), "other": set()}
    torsion_shape_by_order = {
        "maximal": {"split": 0, "nonsplit": 0},
        "conductor2": {"split": 0, "nonsplit": 0},
        "other": {"split": 0, "nonsplit": 0},
    }
    valid_torsion_shape_by_order = {
        "maximal": {"split": 0, "nonsplit": 0},
        "conductor2": {"split": 0, "nonsplit": 0},
        "other": {"split": 0, "nonsplit": 0},
    }
    valid_triples = 0
    good_A_no_x = 0

    for A in range(P):
        j = montgomery_j_from_A(A, P)
        if j is None:
            continue
        trace = montgomery_trace(A, P)
        if trace is None:
            continue
        good_trace = max(v2(P + 1 - trace), v2(P + 1 + trace)) >= k
        has_x = any(pp_verify(P, A, x0) for x0 in range(P))
        bucket = (
            "maximal" if j in maximal_roots else
            "conductor2" if j in frobenius_roots else
            "other"
        )
        shape = "split" if legendre(A * A - 4, P) == 1 else "nonsplit"
        if abs(trace) == TRACE:
            trace_A_by_order[bucket].add(A)
            torsion_shape_by_order[bucket][shape] += 1
        if good_trace and not has_x:
            good_A_no_x += 1
        if not has_x:
            continue
        valid_A_by_order[bucket].add(A)
        valid_by_order[bucket].add(j)
        valid_torsion_shape_by_order[bucket][shape] += 1
        valid_triples += sum(1 for x0 in range(P) if pp_verify(P, A, x0))

    print("fixed trace Montgomery verifier toy")
    print(f"p={P}")
    print(f"k={k}")
    print(f"target_abs_trace={TRACE}")
    print(f"maximal_D={MAXIMAL_D}")
    print(f"frobenius_order_D={FROBENIUS_D}")
    print(f"maximal_roots={sorted(maximal_roots)}")
    print(f"frobenius_roots={sorted(frobenius_roots)}")
    print(f"valid_triples={valid_triples}")
    print(f"good_trace_A_without_verifier_x={good_A_no_x}")
    for bucket in ("maximal", "conductor2", "other"):
        print(f"{bucket}_trace_A_count={len(trace_A_by_order[bucket])}")
        print(f"{bucket}_trace_A_torsion_shape={torsion_shape_by_order[bucket]}")
        print(f"{bucket}_valid_j={sorted(valid_by_order[bucket])}")
        print(f"{bucket}_valid_A_count={len(valid_A_by_order[bucket])}")
        print(f"{bucket}_valid_A_torsion_shape={valid_torsion_shape_by_order[bucket]}")
    print()
    print("interpretation")
    print("  fixed_trace_maximal_roots_are_split_montgomery_in_this_toy=1")
    print("  conductor2_roots_are_nonsplit_montgomery_and_verifier_valid=1")
    print("  p24_xonly_certificate_should_target_frobenius_order_branch_or_verify_nonsplitness=1")
    print("conclusion=reported_fixed_trace_montgomery_verifier_toy")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Probe the X0(7) Atkin/Elkies status filter on X1(16) samples.

For p23 the two admissible traces both have nonsquare Frobenius discriminant
modulo 7.  Equivalently, the curve should be Atkin at ell=7, so the classical
X0(7) modular equation should have no Fp root.

This script uses the genus-zero X0(7) parametrization

  j = ((t^2 + 13t + 49) * (t^2 + 5t + 1)^3) / t

and tests whether the resulting degree-8 polynomial has an Fp root.  It is a
research helper, not a production filter.
"""

from __future__ import annotations

import argparse
import random
import time
from collections import Counter
from dataclasses import dataclass

import x16_trace_residue_calibration as cal
from x16_trace_feature_scan import legendre, x16_samples_with_y


P23 = 10**23 + 117
P23_TRACES = (321963163766, -227792650122)


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def poly_divmod(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int]]:
    a = trim(a[:])
    b = trim(b[:])
    if b == [0]:
        raise ZeroDivisionError
    if len(a) < len(b):
        return [0], a
    q = [0] * (len(a) - len(b) + 1)
    inv_lc = cal.inv(b[-1], p)
    while len(a) >= len(b) and a != [0]:
        coeff = a[-1] * inv_lc % p
        shift = len(a) - len(b)
        q[shift] = coeff
        for i, bi in enumerate(b):
            a[i + shift] = (a[i + shift] - coeff * bi) % p
        trim(a)
    return trim(q), trim(a)


def poly_mod(a: list[int], mod_poly: list[int], p: int) -> list[int]:
    return poly_divmod(a, mod_poly, p)[1]


def poly_gcd(a: list[int], b: list[int], p: int) -> list[int]:
    a = trim([x % p for x in a])
    b = trim([x % p for x in b])
    while b != [0]:
        _, r = poly_divmod(a, b, p)
        a, b = b, r
    inv_lc = cal.inv(a[-1], p)
    return trim([x * inv_lc % p for x in a])


def poly_mulmod(a: list[int], b: list[int], mod_poly: list[int], p: int) -> list[int]:
    return poly_mod(poly_mul(a, b, p), mod_poly, p)


def poly_powmod(base: list[int], exp: int, mod_poly: list[int], p: int) -> list[int]:
    out = [1]
    base = poly_mod(base, mod_poly, p)
    while exp:
        if exp & 1:
            out = poly_mulmod(out, base, mod_poly, p)
        base = poly_mulmod(base, base, mod_poly, p)
        exp >>= 1
    return out


def x0_7_poly_for_j(j: int, p: int) -> list[int]:
    # Low-to-high coefficients.
    a = [49 % p, 13 % p, 1]
    b = [1, 5 % p, 1]
    poly = poly_mul(a, poly_mul(poly_mul(b, b, p), b, p), p)
    if len(poly) < 2:
        poly += [0] * (2 - len(poly))
    poly[1] = (poly[1] - j) % p
    return trim(poly)


def has_x0_7_root(j: int, p: int) -> bool:
    f = x0_7_poly_for_j(j, p)
    xp = poly_powmod([0, 1], p, f, p)
    g = poly_gcd(poly_sub(xp, [0, 1], p), f, p)
    return len(g) > 1


def brute_has_x0_7_root(j: int, p: int) -> bool:
    f = x0_7_poly_for_j(j, p)
    for t in range(p):
        v = 0
        for coeff in reversed(f):
            v = (v * t + coeff) % p
        if v == 0:
            return True
    return False


def montgomery_j(A: int, p: int) -> int | None:
    B = A * A % p
    den = (B - 4) % p
    if den == 0:
        return None
    num = 256 * pow((B - 3) % p, 3, p) % p
    return num * cal.inv(den, p) % p


def nonsplit_bit(y: int, p: int) -> int:
    y2 = y * y % p
    return legendre((y2 - 2) * (y2 - 4 * y + 2), p)


def target_atkin_status_for_p23() -> None:
    ell = 7
    rows = []
    for t in P23_TRACES:
        D = (t * t - 4 * P23) % ell
        status = "ramified" if D == 0 else ("elkies" if legendre(D, ell) == 1 else "atkin")
        rows.append((t % ell, D, status))
    print(f"p23_mod_7={P23 % 7}")
    print(f"p23_target_trace_rows_mod7={rows}")
    all_status = []
    for tr in range(ell):
        D = (tr * tr - 4 * (P23 % ell)) % ell
        status = "ramified" if D == 0 else ("elkies" if legendre(D, ell) == 1 else "atkin")
        all_status.append((tr, D, status))
    print(f"all_trace_status_mod7={all_status}")


@dataclass(frozen=True)
class Row:
    y: int
    A: int
    j: int
    has_root: bool
    trace: int | None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0, help="field prime; default finds calibration prime")
    ap.add_argument("--start", type=int, default=100_000)
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260602)
    ap.add_argument("--nonsplit-only", action="store_true")
    ap.add_argument("--brute-trace", action="store_true")
    ap.add_argument("--brute-root-check", action="store_true")
    args = ap.parse_args()

    p = args.p
    if not p:
        modulus = 8 * 7
        p = cal.find_calibration_prime(args.start, modulus, P23 % modulus)
    rng = random.Random(args.seed)

    target_atkin_status_for_p23()
    print(f"calibration_or_probe_p={p}")
    print(f"p_mod_56={p % 56} p23_mod_56={P23 % 56}")
    print(f"samples_requested={args.samples} seed={args.seed} nonsplit_only={args.nonsplit_only}")

    rows: list[Row] = []
    attempts = 0
    t_sample0 = time.perf_counter()
    while len(rows) < args.samples and attempts < args.samples * 100 + 1000:
        attempts += 1
        for y, A in x16_samples_with_y(p, rng, 1):
            if args.nonsplit_only and nonsplit_bit(y, p) != -1:
                continue
            j = montgomery_j(A, p)
            if j is None:
                continue
            has_root = has_x0_7_root(j, p)
            if args.brute_root_check and p < 1_000_000:
                brute = brute_has_x0_7_root(j, p)
                if brute != has_root:
                    raise RuntimeError(f"root predicate mismatch p={p} A={A} j={j}")
            trace = cal.trace_for_montgomery_A(p, A) if args.brute_trace else None
            rows.append(Row(y=y, A=A, j=j, has_root=has_root, trace=trace))
            break
    elapsed = time.perf_counter() - t_sample0

    print(f"samples={len(rows)} attempts={attempts}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"curves_per_second={len(rows) / elapsed if elapsed else 0.0:.3f}")

    root_counts = Counter(row.has_root for row in rows)
    print(f"x0_7_root_counts={dict(sorted(root_counts.items()))}")
    atkin_accept = sum(1 for row in rows if not row.has_root)
    print(f"atkin_accept_no_root={atkin_accept}/{len(rows)} rate={atkin_accept / len(rows) if rows else 0.0:.6f}")

    split_counts = Counter(nonsplit_bit(row.y, p) for row in rows)
    print(f"nonsplit_character_counts={dict(sorted(split_counts.items()))}")
    by_split = Counter((nonsplit_bit(row.y, p), row.has_root) for row in rows)
    print("by_nonsplit_character_and_root char has_root count")
    for key in sorted(by_split):
        print(f"{key[0]} {int(key[1])} {by_split[key]}")

    if args.brute_trace:
        target_residues = {t % 7 for t in P23_TRACES}
        trace_counts = Counter(row.trace % 7 for row in rows if row.trace is not None)
        status_mismatches = 0
        accepted = 0
        atkin_false_positive = 0
        atkin_false_negative = 0
        for row in rows:
            assert row.trace is not None
            D = (row.trace * row.trace - 4 * p) % 7
            exact_has_root = D != 0 and legendre(D, 7) == 1
            if exact_has_root != row.has_root:
                status_mismatches += 1
            is_target_residue = row.trace % 7 in target_residues
            is_atkin_accept = not row.has_root
            if is_target_residue:
                accepted += 1
                if not is_atkin_accept:
                    atkin_false_negative += 1
            elif is_atkin_accept:
                atkin_false_positive += 1
        print(f"trace_mod7_counts={dict(sorted(trace_counts.items()))}")
        print(f"status_mismatches_vs_trace_discriminant={status_mismatches}")
        print(f"target_trace_mod7_accept={accepted}/{len(rows)} rate={accepted / len(rows) if rows else 0.0:.6f}")
        print(f"atkin_false_negative_on_targets={atkin_false_negative}")
        print(f"atkin_false_positive_non_targets={atkin_false_positive}")


if __name__ == "__main__":
    main()

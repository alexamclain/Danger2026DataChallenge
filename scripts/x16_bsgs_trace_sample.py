#!/usr/bin/env python3
"""Sample X1(16) rows and compute exact traces by Hasse-interval BSGS.

The fast FFT trace helper is excellent up to medium calibration primes, but it
stores full length-p arrays.  The first larger p23 residue-matched controls are
around p=260M, where full-array FFT enumeration is too memory-heavy.  This
helper switches to sampled calibration: sample accepted X1(16) y-values and
point-count each Montgomery curve individually.

For E_A: y^2 = x^3 + A*x^2 + x, Hasse says

    #E(Fp) = p + 1 - t,  |t| <= 2*sqrt(p).

For a random point P, (p+1)P = tP.  Since the trace interval is short for the
larger controls, a baby-step/giant-step search recovers t.  A second independent
point is used as a verification check; if it disagrees, the curve is retried.
This is a calibration tool only and does not touch p23 production workers.
"""

from __future__ import annotations

import argparse
import math
import random
import time
from collections import Counter
from functools import reduce
from typing import Optional

from x16_hazard_calibration import compute_k, odd_parts
from x16_trace_residue_calibration import P23, P23_TRACES, sqrt_mod, trace_for_montgomery_A

Point = Optional[tuple[int, int]]


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def target_traces(p: int) -> set[int]:
    k = compute_k(p)
    twok = 1 << k
    return {p + 1 - twok * m for m in odd_parts(p, k)}


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def ec_neg(P: Point, p: int) -> Point:
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)


def ec_add(P: Point, Q: Point, A: int, p: int) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return None
        if y1 == 0:
            return None
        lam = (3 * x1 * x1 + 2 * A * x1 + 1) * inv(2 * y1, p) % p
    else:
        lam = (y2 - y1) * inv(x2 - x1, p) % p
    x3 = (lam * lam - A - x1 - x2) % p
    y3 = (-y1 - lam * (x3 - x1)) % p
    return (x3, y3)


def ec_mul(n: int, P: Point, A: int, p: int) -> Point:
    if n < 0:
        return ec_mul(-n, ec_neg(P, p), A, p)
    R: Point = None
    Q = P
    while n:
        if n & 1:
            R = ec_add(R, Q, A, p)
        Q = ec_add(Q, Q, A, p)
        n >>= 1
    return R


def point_key(P: Point) -> tuple[int, int]:
    return (-1, -1) if P is None else P


def random_point(A: int, p: int, rng: random.Random) -> Point:
    while True:
        x = rng.randrange(p)
        rhs = (x * x % p * x + A * x % p * x + x) % p
        y = sqrt_mod(rhs, p)
        if y is not None:
            if y and rng.randrange(2):
                y = (-y) % p
            return (x, y)


def trace_from_point(P: Point, A: int, p: int, bound: int) -> int | None:
    """Recover t from (p+1)P=tP, or return None on ambiguity/failure."""
    if P is None:
        return None
    width = 2 * bound + 1
    m = math.isqrt(width) + 1

    babies: dict[tuple[int, int], int | None] = {}
    R: Point = None
    for j in range(m):
        key = point_key(R)
        if key in babies:
            # P has order below m, making the interval log ambiguous.
            return None
        babies[key] = j
        R = ec_add(R, P, A, p)

    qP = ec_mul(p + 1, P, A, p)
    bP = ec_mul(bound, P, A, p)
    target = ec_add(qP, bP, A, p)
    giant = ec_mul(m, P, A, p)
    neg_giant = ec_neg(giant, p)

    cur = target
    max_i = (width + m - 1) // m
    found: list[int] = []
    for i in range(max_i + 1):
        j = babies.get(point_key(cur))
        if j is not None:
            n = i * m + j
            if n < width:
                found.append(-bound + n)
                if len(found) > 1:
                    return None
        cur = ec_add(cur, neg_giant, A, p)

    return found[0] if len(found) == 1 else None


def trace_bsgs(A: int, p: int, rng: random.Random, checks: int) -> tuple[int, int]:
    bound = 2 * math.isqrt(p) + 2
    attempts = 0
    while attempts < 40:
        attempts += 1
        P = random_point(A, p, rng)
        t = trace_from_point(P, A, p, bound)
        if t is None:
            continue
        ok = True
        n = p + 1 - t
        for _ in range(checks):
            Q = random_point(A, p, rng)
            if ec_mul(n, Q, A, p) is not None:
                ok = False
                break
        if ok:
            return t, attempts
    raise RuntimeError(f"failed to recover trace for A={A} after {attempts} attempts")


def x16_A_from_y(y: int, p: int) -> int | None:
    ym1 = (y - 1) % p
    if ym1 == 0:
        return None
    y2 = y * y % p
    y3 = y2 * y % p
    y4 = y2 * y2 % p
    y5 = y4 * y % p
    y6 = y3 * y3 % p
    y7 = y6 * y % p
    y8 = y4 * y4 % p
    num = (
        y8
        - 8 * y7
        + 24 * y6
        - 32 * y5
        + 8 * y4
        + 32 * y3
        - 48 * y2
        + 32 * y
        - 8
    ) % p
    den = 4 * pow(ym1, 4, p) % p
    if den == 0:
        return None
    A = num * inv(den, p) % p
    if A <= 2 or A >= p - 2:
        return None
    return A


def fiber_root_count(y: int, p: int) -> int:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return 0
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    chi = legendre(disc, p)
    if chi < 0:
        return 0
    return 1 if chi == 0 else 2


def fmt_rate(hits: int, total: int) -> str:
    return f"{hits}/{total}:{(hits / total if total else 0.0):.6f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--samples", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260602)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--max-threshold", type=int, default=12)
    ap.add_argument("--class-filter", choices=["all", "nonsplit", "split"], default="nonsplit")
    ap.add_argument("--verify-random-points", type=int, default=2)
    ap.add_argument("--validate-brute", type=int, default=0)
    args = ap.parse_args()

    p = args.p
    rng = random.Random(args.seed)
    residues = {ell: {t % ell for t in P23_TRACES} for ell in args.ells}
    p_targets = target_traces(p)
    p_residues = {ell: {t % ell for t in p_targets} for ell in args.ells}

    t0 = time.perf_counter()
    rows = 0
    attempts_y = 0
    bsgs_attempts = 0
    class_counts: Counter[str] = Counter()
    class_cumulative: Counter[tuple[str, int]] = Counter()
    bucket_counts: Counter[tuple[str, int]] = Counter()
    bucket_cumulative: Counter[tuple[str, int, int]] = Counter()
    v2_hist: Counter[int] = Counter()
    validation_mismatches = 0

    while rows < args.samples:
        attempts_y += 1
        y = rng.randrange(1, p)
        A = x16_A_from_y(y, p)
        if A is None:
            continue
        mult = fiber_root_count(y, p)
        if mult == 0:
            continue
        chi_disc = legendre(A * A - 4, p)
        cls = "split" if chi_disc == 1 else "nonsplit"
        if args.class_filter != "all" and cls != args.class_filter:
            continue

        trace, attempts = trace_bsgs(A, p, rng, args.verify_random_points)
        bsgs_attempts += attempts
        if args.validate_brute and rows < args.validate_brute:
            brute = trace_for_montgomery_A(p, A)
            if brute != trace:
                validation_mismatches += 1
                print(f"validation_mismatch row={rows} A={A} bsgs={trace} brute={brute}")

        e2 = v2(p + 1 - trace)
        v2_hist[e2] += 1
        rows += 1
        labels = ["all", cls]
        for label in labels:
            class_counts[label] += 1
            cumulative_ok = True
            for ell in args.ells:
                cumulative_ok = cumulative_ok and (trace % ell in residues[ell])
                if cumulative_ok:
                    class_cumulative[(label, ell)] += 1
            for threshold in range(4, args.max_threshold + 1):
                if e2 < threshold:
                    continue
                bucket_counts[(label, threshold)] += 1
                cumulative_ok = True
                for ell in args.ells:
                    cumulative_ok = cumulative_ok and (trace % ell in residues[ell])
                    if cumulative_ok:
                        bucket_cumulative[(label, threshold, ell)] += 1

    elapsed = time.perf_counter() - t0
    modulus = 8 * reduce(lambda a, b: a * b, args.ells, 1)

    print("X1(16) sampled BSGS trace-residue calibration")
    print(f"p={p}")
    print(f"p_mod_modulus={p % modulus}")
    print(f"p23_mod_modulus={P23 % modulus}")
    print(f"ells={args.ells}")
    print("p23_target_residues=" + ",".join(f"ell{ell}:{sorted(residues[ell])}" for ell in args.ells))
    print("calibration_p_target_residues=" + ",".join(f"ell{ell}:{sorted(p_residues[ell])}" for ell in args.ells))
    print("residue_sets_match_p23=" + ",".join(
        f"ell{ell}:{int(p_residues[ell] == residues[ell])}" for ell in args.ells
    ))
    print(f"class_filter={args.class_filter}")
    print(f"samples={rows}")
    print(f"attempted_y={attempts_y}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"samples_per_second={rows / elapsed if elapsed else 0.0:.3f}")
    print(f"mean_bsgs_attempts={bsgs_attempts / rows if rows else 0.0:.3f}")
    if args.validate_brute:
        print(f"validate_brute_checked={min(rows, args.validate_brute)} mismatches={validation_mismatches}")
    print("v2_hist=" + ",".join(f"{k}:{v2_hist[k]}" for k in sorted(v2_hist)))
    print()

    for label in ("all", "nonsplit", "split"):
        total = class_counts[label]
        if not total:
            continue
        print(f"group={label} total={total}")
        print("  cumulative_by_ell")
        ideal_product = 1.0
        for ell in args.ells:
            ideal_product *= len(residues[ell]) / ell
            print(
                f"    through={ell:2d} accepted={fmt_rate(class_cumulative[(label, ell)], total)} "
                f"ideal_independent={ideal_product:.6f}"
            )
        print("  conditioned_on_v2")
        for threshold in range(4, args.max_threshold + 1):
            btotal = bucket_counts[(label, threshold)]
            if not btotal:
                continue
            print(f"    v2_ge={threshold} total={fmt_rate(btotal, total)}")
            ideal_product = 1.0
            for ell in args.ells:
                ideal_product *= len(residues[ell]) / ell
                print(
                    f"      through={ell:2d} accepted={fmt_rate(bucket_cumulative[(label, threshold, ell)], btotal)} "
                    f"ideal_independent={ideal_product:.6f}"
                )
        print()


if __name__ == "__main__":
    main()

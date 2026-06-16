#!/usr/bin/env python3
"""Fast exact X1(16) trace/v2 enumeration for calibration primes.

For Montgomery curves

    E_A: y^2 = x^3 + A*x^2 + x,

the trace is the character sum

    t(A) = - sum_x chi(x^3 + A*x^2 + x).

For x != 0,

    x^3 + A*x^2 + x = x^2 * (A + x + 1/x),

so after grouping by c = x + 1/x,

    t(A) = - sum_c chi(c^2 - 4) * chi(A + c).

This is one cyclic convolution over F_p.  The helper uses an FFT to compute
all t(A), then exactly enumerates the accepted X1(16) y-stream with quadratic
fiber multiplicity.  It is a calibration tool only; it is not a p23 production
kernel.
"""

from __future__ import annotations

import argparse
import math
import random
import sys
import time
from collections import Counter

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover - environment hint
    raise SystemExit(
        "x16_fast_trace_enumeration.py requires NumPy. In this Codex workspace, "
        "run it with /Users/agent/.cache/codex-runtimes/codex-primary-runtime/"
        "dependencies/python/bin/python3"
    ) from exc

from x16_hazard_calibration import compute_k, odd_parts, trace_mass
from x16_trace_residue_calibration import P23, find_calibration_prime, trace_for_montgomery_A


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


def legendre_table(p: int) -> np.ndarray:
    chi = np.zeros(p, dtype=np.int16)
    exp = (p - 1) // 2
    for a in range(1, p):
        r = pow(a, exp, p)
        chi[a] = 1 if r == 1 else -1
    return chi


def inverse_table(p: int) -> np.ndarray:
    inv = np.zeros(p, dtype=np.int64)
    inv[1] = 1
    for a in range(2, p):
        inv[a] = (p - (p // a) * int(inv[p % a]) % p) % p
    return inv


def next_pow2(n: int) -> int:
    return 1 << (n - 1).bit_length()


def all_montgomery_traces_fft(p: int, chi: np.ndarray) -> tuple[np.ndarray, float]:
    c = np.arange(p, dtype=np.int64)
    f = chi[(c * c - 4) % p].astype(np.float64)
    g = chi.astype(np.float64)

    # r[d] = f[-d], so conv(r,g)[A] = sum_c f[c] g[A+c].
    r = np.empty(p, dtype=np.float64)
    r[0] = f[0]
    r[1:] = f[:0:-1]

    nfft = next_pow2(2 * p - 1)
    conv = np.fft.irfft(np.fft.rfft(r, nfft) * np.fft.rfft(g, nfft), nfft)[: 2 * p - 1]
    folded = conv[:p].copy()
    folded[: p - 1] += conv[p:]
    rounded = np.rint(folded)
    max_error = float(np.max(np.abs(folded - rounded)))
    traces = (-rounded).astype(np.int64)
    return traces, max_error


def x16_A_from_y_fast(y: int, p: int, inv: np.ndarray) -> int | None:
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
    A = num * int(inv[den]) % p
    if A <= 2 or A >= p - 2:
        return None
    return A


def fiber_root_count_fast(y: int, p: int, chi: np.ndarray) -> int:
    y2 = y * y % p
    y3 = y2 * y % p
    qa = (y2 - 2 * y) % p
    if qa == 0:
        return 0
    qb = (2 * y2 - y3) % p
    qc = (1 - y) % p
    disc = (qb * qb - 4 * qa * qc) % p
    leg = int(chi[disc])
    if leg < 0:
        return 0
    return 1 if leg == 0 else 2


def validate_traces(p: int, traces: np.ndarray, count: int, seed: int) -> None:
    rng = random.Random(seed)
    mismatches = 0
    checked = 0
    for _ in range(count):
        A = rng.randrange(3, p - 2)
        fast = int(traces[A])
        brute = trace_for_montgomery_A(p, A)
        checked += 1
        if fast != brute:
            mismatches += 1
            print(f"trace_validation_mismatch A={A} fast={fast} brute={brute}")
    print(f"trace_validation checked={checked} mismatches={mismatches}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0)
    ap.add_argument("--start", type=int, default=100_000)
    ap.add_argument("--modulus", type=int, default=120)
    ap.add_argument("--max-threshold", type=int, default=16)
    ap.add_argument("--validate-brute", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20260602)
    args = ap.parse_args()

    p = args.p or find_calibration_prime(args.start, args.modulus, P23 % args.modulus)
    k = compute_k(p)
    targets = target_traces(p)
    tm = trace_mass(p, k)
    heuristic = 16.0 * tm

    print("X1(16) fast exact trace/v2 enumeration")
    print(f"p={p}")
    print(f"k={k}")
    print(f"sqrt_p={math.isqrt(p)}")
    print(f"mod120={p % 120}")
    print(f"target_trace_count={len(targets)}")
    print(f"target_traces={sorted(targets)}")
    print(f"trace_mass={tm:.9e}")
    print(f"heuristic_16x_trace_mass={heuristic:.9e}")
    print(f"python={sys.executable}")

    t0 = time.perf_counter()
    chi = legendre_table(p)
    t_chi = time.perf_counter()
    inv = inverse_table(p)
    t_inv = time.perf_counter()
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    t_fft = time.perf_counter()
    if args.validate_brute:
        validate_traces(p, traces, args.validate_brute, args.seed)

    rows = 0
    accepted_y = 0
    degenerate_roots = 0
    unique_As: set[int] = set()
    class_counts: Counter[str] = Counter()
    class_hits: Counter[str] = Counter()
    class_v2_hist: Counter[str] = Counter()
    class_v2_ge: Counter[str] = Counter()
    target_trace_hist: Counter[int] = Counter()

    for y in range(1, p):
        A = x16_A_from_y_fast(y, p, inv)
        if A is None:
            continue
        mult = fiber_root_count_fast(y, p, chi)
        if mult == 0:
            continue
        accepted_y += 1
        if mult == 1:
            degenerate_roots += 1
        unique_As.add(A)
        trace = int(traces[A])
        cls = "split" if int(chi[(A * A - 4) % p]) == 1 else "nonsplit"
        e2 = v2(p + 1 - trace)
        rows += mult
        class_counts[cls] += mult
        class_v2_hist[f"{cls}:v2={e2}"] += mult
        for threshold in range(1, args.max_threshold + 1):
            if e2 >= threshold:
                class_v2_ge[f"{cls}:ge{threshold}"] += mult
        if trace in targets:
            class_hits[cls] += mult
            target_trace_hist[trace] += mult

    elapsed = time.perf_counter() - t0
    all_hits = sum(class_hits.values())
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"legendre_seconds={t_chi - t0:.6f}")
    print(f"inverse_seconds={t_inv - t_chi:.6f}")
    print(f"fft_trace_seconds={t_fft - t_inv:.6f}")
    print(f"fft_max_rounding_error={fft_error:.3e}")
    print(f"accepted_y={accepted_y}")
    print(f"candidate_rows_with_root_multiplicity={rows}")
    print(f"unique_A={len(unique_As)}")
    print(f"degenerate_root_y={degenerate_roots}")
    print("split_class_counts=" + ",".join(f"{key}:{class_counts[key]}" for key in sorted(class_counts)))
    print()
    for cls in ["all", "nonsplit", "split"]:
        total = rows if cls == "all" else class_counts[cls]
        hits = all_hits if cls == "all" else class_hits[cls]
        rate = hits / total if total else 0.0
        L = rate / heuristic if heuristic else 0.0
        print(f"{cls}_x16 hits={hits}/{total} rate={rate:.9f} L_trace={L:.3f}")
    print("target_trace_hist=" + ",".join(f"{tr}:{target_trace_hist[tr]}" for tr in sorted(target_trace_hist)))
    print("class_v2_hist=" + ",".join(f"{k}:{class_v2_hist[k]}" for k in sorted(class_v2_hist)))
    print("threshold_rates")
    for threshold in range(1, args.max_threshold + 1):
        pieces = []
        for cls in ["nonsplit", "split"]:
            total = class_counts[cls]
            hits = class_v2_ge[f"{cls}:ge{threshold}"]
            rate = hits / total if total else 0.0
            pieces.append(f"{cls}:ge{threshold}={hits}/{total}:{rate:.6f}")
        print(" ".join(pieces))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact small-prime joint v2 and odd trace-residue stack for X1(16).

This enumerates the accepted X1(16) candidate stream over a small prime,
with multiplicity matching the sampler's quadratic fiber roots.  It records:

  * split/nonsplit class,
  * v2(#E(Fp)),
  * whether the trace lies in the p23 target residues modulo small odd primes.

The purpose is to test whether hypothetical cheap exact odd trace-residue
filters remain independent after conditioning on nonsplit and high 2-adic
curve order.
"""

from __future__ import annotations

import argparse
import time
from collections import Counter
from functools import reduce

from x16_exact_trace_enumeration import fiber_root_count, legendre, target_traces, x16_A_from_y
from x16_trace_residue_calibration import P23, P23_TRACES, trace_for_montgomery_A


def v2(n: int) -> int:
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out


def fmt_rate(hits: int, total: int) -> str:
    return f"{hits}/{total}:{(hits / total if total else 0.0):.6f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11])
    ap.add_argument("--max-threshold", type=int, default=12)
    args = ap.parse_args()

    p = args.p
    ells = args.ells
    residues = {ell: {t % ell for t in P23_TRACES} for ell in ells}
    p_targets = target_traces(p)
    p_residues = {ell: {t % ell for t in p_targets} for ell in ells}

    trace_cache: dict[int, int] = {}
    rows = 0
    unique_As: set[int] = set()
    class_counts: Counter[str] = Counter()
    bucket_counts: Counter[tuple[str, int]] = Counter()
    bucket_cumulative: Counter[tuple[str, int, int]] = Counter()
    bucket_marginal: Counter[tuple[str, int, int]] = Counter()
    class_cumulative: Counter[tuple[str, int]] = Counter()
    class_marginal: Counter[tuple[str, int]] = Counter()

    start = time.perf_counter()
    for y in range(1, p):
        A = x16_A_from_y(y, p)
        if A is None:
            continue
        mult = fiber_root_count(y, p)
        if mult == 0:
            continue

        unique_As.add(A)
        if A not in trace_cache:
            trace_cache[A] = trace_for_montgomery_A(p, A)
        trace = trace_cache[A]
        cls = "split" if legendre(A * A - 4, p) == 1 else "nonsplit"
        e2 = v2(p + 1 - trace)

        rows += mult
        class_counts["all"] += mult
        class_counts[cls] += mult
        for label in ("all", cls):
            cumulative_ok = True
            for ell in ells:
                marginal_ok = trace % ell in residues[ell]
                if marginal_ok:
                    class_marginal[(label, ell)] += mult
                cumulative_ok = cumulative_ok and marginal_ok
                if cumulative_ok:
                    class_cumulative[(label, ell)] += mult

            for threshold in range(4, args.max_threshold + 1):
                if e2 < threshold:
                    continue
                bucket_counts[(label, threshold)] += mult
                cumulative_ok = True
                for ell in ells:
                    marginal_ok = trace % ell in residues[ell]
                    if marginal_ok:
                        bucket_marginal[(label, threshold, ell)] += mult
                    cumulative_ok = cumulative_ok and marginal_ok
                    if cumulative_ok:
                        bucket_cumulative[(label, threshold, ell)] += mult

    elapsed = time.perf_counter() - start

    print("X1(16) exact v2 plus trace-residue stack")
    print(f"p={p}")
    modulus = 8 * reduce(lambda a, b: a * b, ells, 1)
    print(f"modulus={modulus}")
    print(f"p_mod_modulus={p % modulus}")
    print(f"p23_mod_modulus={P23 % modulus}")
    print(f"ells={ells}")
    print("target_residues=" + ",".join(f"ell{ell}:{sorted(residues[ell])}" for ell in ells))
    print("calibration_p_target_residues=" + ",".join(f"ell{ell}:{sorted(p_residues[ell])}" for ell in ells))
    print("residue_sets_match_p23=" + ",".join(
        f"ell{ell}:{int(p_residues[ell] == residues[ell])}" for ell in ells
    ))
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"rows={rows}")
    print(f"unique_A={len(unique_As)}")
    print(f"trace_cache_size={len(trace_cache)}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in ("nonsplit", "split")))
    print()

    for label in ("all", "nonsplit", "split"):
        total = class_counts[label]
        print(f"group={label} total={total}")
        print("  marginal_by_ell")
        for ell in ells:
            ideal = len(residues[ell]) / ell
            print(f"    ell={ell:2d} accepted={fmt_rate(class_marginal[(label, ell)], total)} ideal={ideal:.6f}")
        print("  cumulative_by_ell")
        ideal_product = 1.0
        for ell in ells:
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
            for ell in ells:
                ideal_product *= len(residues[ell]) / ell
                print(
                    f"      through={ell:2d} accepted={fmt_rate(bucket_cumulative[(label, threshold, ell)], btotal)} "
                    f"ideal_independent={ideal_product:.6f}"
                )
        print()


if __name__ == "__main__":
    main()

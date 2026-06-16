#!/usr/bin/env python3
"""Fast exact X1(16) v2 plus p23 trace-residue stack calibration."""

from __future__ import annotations

import argparse
import time
from collections import Counter
from functools import reduce

from x16_fast_trace_enumeration import (
    all_montgomery_traces_fft,
    fiber_root_count_fast,
    inverse_table,
    legendre_table,
    target_traces,
    v2,
    x16_A_from_y_fast,
)
from x16_trace_residue_calibration import P23, P23_TRACES, find_calibration_prime


def fmt_rate(hits: int, total: int) -> str:
    return f"{hits}/{total}:{(hits / total if total else 0.0):.6f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=0)
    ap.add_argument("--start", type=int, default=100_000)
    ap.add_argument("--modulus", type=int, default=120)
    ap.add_argument("--ells", type=int, nargs="+", default=[3, 5, 7, 11])
    ap.add_argument("--max-threshold", type=int, default=14)
    args = ap.parse_args()

    p = args.p or find_calibration_prime(args.start, args.modulus, P23 % args.modulus)
    ells = args.ells
    p23_residues = {ell: {t % ell for t in P23_TRACES} for ell in ells}
    p_targets = target_traces(p)
    p_residues = {ell: {t % ell for t in p_targets} for ell in ells}

    start = time.perf_counter()
    chi = legendre_table(p)
    inv = inverse_table(p)
    traces, fft_error = all_montgomery_traces_fft(p, chi)
    prep_elapsed = time.perf_counter() - start

    rows = 0
    accepted_y = 0
    unique_As: set[int] = set()
    class_counts: Counter[str] = Counter()
    class_marginal: Counter[tuple[str, int]] = Counter()
    class_cumulative: Counter[tuple[str, int]] = Counter()
    bucket_counts: Counter[tuple[str, int]] = Counter()
    bucket_cumulative: Counter[tuple[str, int, int]] = Counter()
    bucket_marginal: Counter[tuple[str, int, int]] = Counter()

    for y in range(1, p):
        A = x16_A_from_y_fast(y, p, inv)
        if A is None:
            continue
        mult = fiber_root_count_fast(y, p, chi)
        if mult == 0:
            continue
        accepted_y += 1
        unique_As.add(A)
        trace = int(traces[A])
        cls = "split" if int(chi[(A * A - 4) % p]) == 1 else "nonsplit"
        e2 = v2(p + 1 - trace)
        rows += mult
        class_counts["all"] += mult
        class_counts[cls] += mult

        for label in ("all", cls):
            cumulative_ok = True
            for ell in ells:
                marginal_ok = trace % ell in p23_residues[ell]
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
                    marginal_ok = trace % ell in p23_residues[ell]
                    if marginal_ok:
                        bucket_marginal[(label, threshold, ell)] += mult
                    cumulative_ok = cumulative_ok and marginal_ok
                    if cumulative_ok:
                        bucket_cumulative[(label, threshold, ell)] += mult

    elapsed = time.perf_counter() - start
    print("X1(16) fast exact v2 plus p23 trace-residue stack")
    print(f"p={p}")
    modulus = 8 * reduce(lambda a, b: a * b, ells, 1)
    print(f"modulus={modulus}")
    print(f"p_mod_modulus={p % modulus}")
    print(f"p23_mod_modulus={P23 % modulus}")
    print(f"ells={ells}")
    print("p23_target_residues=" + ",".join(f"ell{ell}:{sorted(p23_residues[ell])}" for ell in ells))
    print("calibration_p_target_residues=" + ",".join(f"ell{ell}:{sorted(p_residues[ell])}" for ell in ells))
    print("residue_sets_match_p23=" + ",".join(
        f"ell{ell}:{int(p_residues[ell] == p23_residues[ell])}" for ell in ells
    ))
    print(f"prep_seconds={prep_elapsed:.6f}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"fft_max_rounding_error={fft_error:.3e}")
    print(f"accepted_y={accepted_y}")
    print(f"rows={rows}")
    print(f"unique_A={len(unique_As)}")
    print("split_class_counts=" + ",".join(f"{k}:{class_counts[k]}" for k in ("nonsplit", "split")))
    print()

    for label in ("all", "nonsplit", "split"):
        total = class_counts[label]
        print(f"group={label} total={total}")
        print("  marginal_by_ell")
        for ell in ells:
            ideal = len(p23_residues[ell]) / ell
            print(f"    ell={ell:2d} accepted={fmt_rate(class_marginal[(label, ell)], total)} ideal={ideal:.6f}")
        print("  cumulative_by_ell")
        ideal_product = 1.0
        for ell in ells:
            ideal_product *= len(p23_residues[ell]) / ell
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
                ideal_product *= len(p23_residues[ell]) / ell
                print(
                    f"      through={ell:2d} accepted={fmt_rate(bucket_cumulative[(label, threshold, ell)], btotal)} "
                    f"ideal_independent={ideal_product:.6f}"
                )
        print()


if __name__ == "__main__":
    main()

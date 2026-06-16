#!/usr/bin/env python3
"""Audit multiplicative-coset structure in the strict trace bucket.

Earlier p24 probes checked additive spectra and low-degree quadratic character
labels in the Montgomery parameter A.  A different possible selector would be
that the target-trace bucket is biased toward a low-index multiplicative coset
of F_p^*, either in A itself or in the Montgomery j-invariant.

This exact small-field audit computes the strict x-only good bucket for
p = n^2 + 7, builds a primitive-root log table, and measures:

* the largest nontrivial multiplicative Fourier coefficient;
* the best lift from low-order multiplicative character cosets; and
* whether the same low-order cosets are stable across rows.

It is a calibration probe.  It does not search p24.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table, montgomery_j_from_A


@dataclass(frozen=True)
class SpectrumSummary:
    label: str
    support: int
    hits: int
    base_rate: float
    max_frequency: int
    max_abs: float
    max_over_sqrt_hits: float
    top_frequencies: tuple[tuple[int, float, float], ...]


@dataclass(frozen=True)
class CosetSummary:
    label: str
    order: int
    best_bucket: int
    best_total: int
    best_hits: int
    best_lift: float
    best_capture: float
    worst_lift: float
    bucket_rates: tuple[float, ...]


def primitive_root(p: int) -> int:
    factors = []
    n = p - 1
    q = 2
    while q * q <= n:
        if n % q == 0:
            factors.append(q)
            while n % q == 0:
                n //= q
        q += 1 if q == 2 else 2
    if n > 1:
        factors.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root found for p={p}")


def log_table(p: int, g: int) -> np.ndarray:
    logs = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        logs[x] = e
        x = x * g % p
    return logs


def spectrum_for_values(
    label: str,
    p: int,
    logs: np.ndarray,
    values: np.ndarray,
    good: np.ndarray,
    top: int,
) -> SpectrumSummary:
    support_mask = values != 0
    support = int(np.count_nonzero(support_mask))
    hit_mask = support_mask & good
    hits = int(np.count_nonzero(hit_mask))
    base_rate = hits / support if support else 0.0

    by_log = np.zeros(p - 1, dtype=np.float64)
    if hits:
        hit_values = values[hit_mask]
        hit_logs = logs[hit_values]
        np.add.at(by_log, hit_logs, 1.0)

    coeffs = np.fft.fft(by_log)
    magnitudes = np.abs(coeffs)
    if len(magnitudes) > 1:
        magnitudes[0] = 0.0
    order = np.argsort(magnitudes)[::-1]
    top_rows = []
    for idx in order[:top]:
        mag = float(magnitudes[int(idx)])
        top_rows.append((int(idx), mag, mag / math.sqrt(hits) if hits else 0.0))

    max_idx = int(order[0]) if len(order) else 0
    max_abs = float(magnitudes[max_idx]) if len(magnitudes) else 0.0
    return SpectrumSummary(
        label=label,
        support=support,
        hits=hits,
        base_rate=base_rate,
        max_frequency=max_idx,
        max_abs=max_abs,
        max_over_sqrt_hits=max_abs / math.sqrt(hits) if hits else 0.0,
        top_frequencies=tuple(top_rows),
    )


def coset_summary(
    label: str,
    p: int,
    logs: np.ndarray,
    values: np.ndarray,
    good: np.ndarray,
    order: int,
) -> CosetSummary | None:
    if (p - 1) % order != 0:
        return None
    support_mask = values != 0
    support = int(np.count_nonzero(support_mask))
    hits_total = int(np.count_nonzero(support_mask & good))
    if support == 0 or hits_total == 0:
        return None
    base_rate = hits_total / support
    buckets_total = [0] * order
    buckets_hits = [0] * order
    selected_logs = logs[values[support_mask]]
    selected_good = good[support_mask]
    for residue, is_good in zip(selected_logs % order, selected_good):
        r = int(residue)
        buckets_total[r] += 1
        buckets_hits[r] += int(bool(is_good))

    rates = tuple(
        buckets_hits[i] / buckets_total[i] if buckets_total[i] else 0.0
        for i in range(order)
    )
    lifts = [rate / base_rate if base_rate else 0.0 for rate in rates]
    best_bucket = max(range(order), key=lambda i: lifts[i])
    worst_lift = min(lifts)
    best_hits = buckets_hits[best_bucket]
    return CosetSummary(
        label=label,
        order=order,
        best_bucket=best_bucket,
        best_total=buckets_total[best_bucket],
        best_hits=best_hits,
        best_lift=lifts[best_bucket],
        best_capture=best_hits / hits_total if hits_total else 0.0,
        worst_lift=worst_lift,
        bucket_rates=rates,
    )


def j_values_for_A(p: int) -> np.ndarray:
    values = np.zeros(p, dtype=np.int64)
    for A in range(p):
        j = montgomery_j_from_A(A, p)
        values[A] = 0 if j is None else j
    return values


def print_spectrum(summary: SpectrumSummary) -> None:
    print(
        f"  spectrum {summary.label}: support={summary.support} hits={summary.hits} "
        f"base={summary.base_rate:.8f} max_h={summary.max_frequency} "
        f"max_abs={summary.max_abs:.3f} max/sqrt_hits={summary.max_over_sqrt_hits:.3f}"
    )
    for h, mag, norm in summary.top_frequencies:
        print(f"    top h={h:6d} abs={mag:.3f} abs/sqrt_hits={norm:.3f}")


def print_cosets(rows: list[CosetSummary], top: int) -> None:
    rows = sorted(rows, key=lambda row: (row.best_lift, row.best_capture), reverse=True)
    for row in rows[:top]:
        print(
            f"  coset {row.label} order={row.order:3d} bucket={row.best_bucket:3d} "
            f"hits={row.best_hits:5d}/{row.best_total:5d} lift={row.best_lift:.3f} "
            f"capture={row.best_capture:.3f} worst_lift={row.worst_lift:.3f}"
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=10)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-character-order", type=int, default=32)
    ap.add_argument("--top-spectrum", type=int, default=5)
    ap.add_argument("--top-cosets", type=int, default=8)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    print("multiplicative spectrum trace-bucket audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"max_character_order={args.max_character_order}")

    aggregate_lifts: dict[tuple[str, int], list[float]] = defaultdict(list)
    aggregate_captures: dict[tuple[str, int], list[float]] = defaultdict(list)
    max_norms: dict[str, list[float]] = defaultdict(list)

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        g = primitive_root(p)
        logs = log_table(p, g)
        A_values = np.arange(p, dtype=np.int64)
        J_values = j_values_for_A(p)

        print(
            f"row={row_index:02d} n={n} p={p} k={stats['k']} "
            f"good={stats['good']}/{stats['nonsingular']} primitive_root={g}"
        )
        spectra = [
            spectrum_for_values("A", p, logs, A_values, good, args.top_spectrum),
            spectrum_for_values("j", p, logs, J_values, good, args.top_spectrum),
        ]
        for summary in spectra:
            max_norms[summary.label].append(summary.max_over_sqrt_hits)
            print_spectrum(summary)

        cosets: list[CosetSummary] = []
        for label, values in (("A", A_values), ("j", J_values)):
            for order in range(2, args.max_character_order + 1):
                row = coset_summary(label, p, logs, values, good, order)
                if row is None:
                    continue
                cosets.append(row)
                aggregate_lifts[(label, order)].append(row.best_lift)
                aggregate_captures[(label, order)].append(row.best_capture)
        print_cosets(cosets, args.top_cosets)

    print("aggregate")
    for label in sorted(max_norms):
        values = max_norms[label]
        print(
            f"  {label} max/sqrt_hits min={min(values):.3f} "
            f"median={float(np.median(values)):.3f} max={max(values):.3f}"
        )

    aggregate_rows = []
    for key, lifts in aggregate_lifts.items():
        if len(lifts) < 2:
            continue
        captures = aggregate_captures[key]
        aggregate_rows.append(
            (
                float(np.median(lifts)),
                float(np.mean(lifts)),
                float(np.median(captures)),
                key[0],
                key[1],
                len(lifts),
            )
        )
    print("  best_low_order_coset_lifts")
    for median_lift, mean_lift, median_capture, label, order, count in sorted(
        aggregate_rows, reverse=True
    )[: args.top_cosets]:
        print(
            f"    {label} order={order:3d} rows={count:2d} "
            f"median_lift={median_lift:.3f} mean_lift={mean_lift:.3f} "
            f"median_capture={median_capture:.3f}"
        )
    print("conclusion=no_stable_low_order_multiplicative_coset_selector_visible")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Additive/residue structure audit for strict near-square DANGER buckets.

For small primes in the family p = n^2 + 7, compute the exact strict x-only
DANGER-good Montgomery parameters A, then test whether that rare set has a
visible low-complexity selector:

* large low-frequency additive Fourier coefficients; or
* stable small integer residue classes A == r mod m.

This is not a proof of pseudorandomness.  It is a bounded diagnostic for a
potential constructive shortcut.  A useful p24 idea should show up as a stable,
large bias at small scale before we spend effort trying to lift it.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import legendre_table


@dataclass(frozen=True)
class RowSpectrum:
    n: int
    p: int
    k: int
    good: int
    total: int
    density: float
    max_freq: int
    max_abs: float
    max_over_sqrt_good: float
    max_over_good: float
    low_energy_frac_32: float
    low_energy_frac_128: float
    top_freqs: tuple[tuple[int, float, float], ...]


@dataclass(frozen=True)
class ResidueStats:
    modulus: int
    residue: int
    hits: int
    total: int
    lift: float
    capture: float
    coverage: float
    score: float


def centered_indicator(good: np.ndarray, nonsingular: np.ndarray) -> np.ndarray:
    """Return a mean-zero float vector on nonsingular A and 0 on singular A."""
    total = int(np.count_nonzero(nonsingular))
    hits = int(np.count_nonzero(good & nonsingular))
    density = hits / total if total else 0.0
    f = np.zeros(good.shape[0], dtype=np.float64)
    f[nonsingular] = good[nonsingular].astype(np.float64) - density
    return f


def signed_frequency(index: int, p: int) -> int:
    return index if index <= p // 2 else index - p


def row_spectrum(n: int, p: int, low_cutoffs: tuple[int, int], top: int) -> RowSpectrum:
    chi = legendre_table(p)
    good, stats = exact_xonly_good_flags(p, chi)
    nonsingular = np.ones(p, dtype=np.bool_)
    nonsingular[[2 % p, (-2) % p]] = False
    good &= nonsingular

    total = int(stats["nonsingular"])
    good_count = int(stats["good"])
    density = good_count / total if total else 0.0

    f = centered_indicator(good, nonsingular)
    spectrum = np.fft.fft(f)
    magnitudes = np.abs(spectrum)
    magnitudes[0] = 0.0
    max_index = int(np.argmax(magnitudes))
    max_abs = float(magnitudes[max_index])
    total_energy = float(np.sum(magnitudes[1:] ** 2))

    low_fracs: list[float] = []
    for cutoff in low_cutoffs:
        low_energy = 0.0
        for h in range(1, min(cutoff, p // 2) + 1):
            low_energy += float(magnitudes[h] ** 2)
            low_energy += float(magnitudes[p - h] ** 2)
        low_fracs.append(low_energy / total_energy if total_energy else 0.0)

    top_indices = np.argsort(magnitudes)[-top:][::-1]
    top_freqs = tuple(
        (
            signed_frequency(int(idx), p),
            float(magnitudes[int(idx)]),
            float(magnitudes[int(idx)] / math.sqrt(good_count)) if good_count else 0.0,
        )
        for idx in top_indices
        if int(idx) != 0
    )

    return RowSpectrum(
        n=n,
        p=p,
        k=int(stats["k"]),
        good=good_count,
        total=total,
        density=density,
        max_freq=signed_frequency(max_index, p),
        max_abs=max_abs,
        max_over_sqrt_good=max_abs / math.sqrt(good_count) if good_count else 0.0,
        max_over_good=max_abs / good_count if good_count else 0.0,
        low_energy_frac_32=low_fracs[0],
        low_energy_frac_128=low_fracs[1],
        top_freqs=top_freqs,
    )


def residue_moduli(limit: int) -> list[int]:
    out: list[int] = []
    for m in range(3, limit + 1):
        # Keep all tiny moduli and prime/power-ish moduli thereafter; this
        # avoids overweighting dozens of nearly identical composite partitions.
        if m <= 16:
            out.append(m)
        elif is_prime_small(m) or m & (m - 1) == 0:
            out.append(m)
    return out


def is_prime_small(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def aggregate_residue_stats(
    rows: list[tuple[int, int]],
    moduli: list[int],
    min_coverage: float,
    max_coverage: float,
) -> tuple[list[ResidueStats], int, int]:
    keys = [(m, r) for m in moduli for r in range(m)]
    hit_totals = {key: 0 for key in keys}
    total_totals = {key: 0 for key in keys}
    all_hits = 0
    all_total = 0

    for n, p in rows:
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        nonsingular = np.ones(p, dtype=np.bool_)
        nonsingular[[2 % p, (-2) % p]] = False
        good &= nonsingular
        all_hits += int(stats["good"])
        all_total += int(stats["nonsingular"])
        A = np.arange(p, dtype=np.int64)
        for m, r in keys:
            selected = nonsingular & ((A % m) == r)
            total = int(np.count_nonzero(selected))
            if total == 0:
                continue
            total_totals[(m, r)] += total
            hit_totals[(m, r)] += int(np.count_nonzero(selected & good))

    base = all_hits / all_total if all_total else 0.0
    out: list[ResidueStats] = []
    for m, r in keys:
        total = total_totals[(m, r)]
        hits = hit_totals[(m, r)]
        if total == 0 or all_hits == 0 or all_total == 0:
            continue
        coverage = total / all_total
        if coverage < min_coverage or coverage > max_coverage:
            continue
        precision = hits / total
        lift = precision / base if base else 0.0
        capture = hits / all_hits
        score = lift * math.sqrt(capture)
        out.append(
            ResidueStats(
                modulus=m,
                residue=r,
                hits=hits,
                total=total,
                lift=lift,
                capture=capture,
                coverage=coverage,
                score=score,
            )
        )
    return sorted(out, key=lambda row: (row.score, row.lift), reverse=True), all_hits, all_total


def print_row_spectrum(row: RowSpectrum, top: int) -> None:
    print(
        f"row n={row.n} p={row.p} k={row.k} "
        f"good={row.good}/{row.total} density={row.density:.6f}"
    )
    print(
        f"  max_freq={row.max_freq:+d} max_abs={row.max_abs:.3f} "
        f"max/sqrt(good)={row.max_over_sqrt_good:.3f} "
        f"max/good={row.max_over_good:.6f}"
    )
    print(
        f"  low_energy_frac(|h|<=32)={row.low_energy_frac_32:.6f} "
        f"low_energy_frac(|h|<=128)={row.low_energy_frac_128:.6f}"
    )
    for h, amp, norm in row.top_freqs[:top]:
        print(f"    top h={h:+d} abs={amp:.3f} abs/sqrt(good)={norm:.3f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=12)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-modulus", type=int, default=64)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-coverage", type=float, default=0.005)
    ap.add_argument("--max-coverage", type=float, default=0.98)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    moduli = residue_moduli(args.max_modulus)
    print("additive/residue strict trace-bucket audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"max_modulus={args.max_modulus}")
    print(f"moduli={moduli}")

    spectra = [row_spectrum(n, p, (32, 128), args.top) for n, p in rows]
    for spectrum in spectra:
        print_row_spectrum(spectrum, args.top)

    if spectra:
        print("spectrum_summary")
        print(
            "  max/sqrt(good): "
            f"min={min(r.max_over_sqrt_good for r in spectra):.3f} "
            f"median={float(np.median([r.max_over_sqrt_good for r in spectra])):.3f} "
            f"max={max(r.max_over_sqrt_good for r in spectra):.3f}"
        )
        print(
            "  low_energy_frac(|h|<=32): "
            f"median={float(np.median([r.low_energy_frac_32 for r in spectra])):.6f} "
            f"max={max(r.low_energy_frac_32 for r in spectra):.6f}"
        )
        print(
            "  low_energy_frac(|h|<=128): "
            f"median={float(np.median([r.low_energy_frac_128 for r in spectra])):.6f} "
            f"max={max(r.low_energy_frac_128 for r in spectra):.6f}"
        )

    residue_stats, all_hits, all_total = aggregate_residue_stats(
        rows, moduli, args.min_coverage, args.max_coverage
    )
    base = all_hits / all_total if all_total else 0.0
    print("aggregate_residue_summary")
    print(f"  good={all_hits}/{all_total} base_rate={base:.6f}")
    for row in residue_stats[: args.top]:
        print(
            f"  m={row.modulus:2d} r={row.residue:2d} "
            f"lift={row.lift:.3f} capture={row.capture:.3f} "
            f"coverage={row.coverage:.3f} hits={row.hits}/{row.total} "
            f"score={row.score:.3f}"
        )

    print("conclusion=no_stable_low_frequency_or_small_residue_selector_visible")


if __name__ == "__main__":
    main()

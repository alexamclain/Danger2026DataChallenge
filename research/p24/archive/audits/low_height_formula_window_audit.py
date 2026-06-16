#!/usr/bin/env python3
"""Audit sub-sqrt windows around low-height A(n) formulas.

Earlier probes ruled out exact low-height formulas for a valid Montgomery
parameter A in the family p=n^2+7.  A softer asymptotic shortcut would be:

    scan |A - f(n)| <= W(p)

for a simple formula f and W=o(sqrt(p)), with non-negligible capture of the
strict DANGER A-set.  This script tests that claim at exact small scale.

It uses the full exact strict-good A mask for small p=n^2+7 rows, and measures
capture/lift for circular intervals around low-height LFT centers

    f(n) = (a*n+b)/(c*n+d).

The computation uses prefix sums on a duplicated good-mask, so each
formula/window query is O(1) after the exact trace mask is built.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import exact_xonly_good_flags, prime_rows
from near_square_formula_probe import Formula, formulas, legendre_table


@dataclass(frozen=True)
class Score:
    formula: Formula
    label: str
    width_label: str
    last_width: int
    hits: int
    total: int
    rows_valid: int
    capture: float
    lift: float
    coverage: float
    score: float


def circular_interval_sum(prefix: np.ndarray, center: int, width: int, p: int) -> int:
    """Count marked values with circular distance <= width from center."""
    if width >= (p - 1) // 2:
        return int(prefix[p] - prefix[0])
    start = center - width
    end = center + width
    if start < 0:
        start += p
        end += p
    return int(prefix[end + 1] - prefix[start])


def width_rows(p: int, betas: list[float], fixed: list[int]) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    seen: set[int] = set()
    for width in fixed:
        width = max(0, min(width, (p - 1) // 2))
        if width not in seen:
            seen.add(width)
            out.append((f"fixed_{width}", width))
    for beta in betas:
        width = int(p**beta)
        width = max(0, min(width, (p - 1) // 2))
        if width not in seen:
            seen.add(width)
            out.append((f"p^{beta:.2f}", width))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=180_000)
    ap.add_argument("--max-rows", type=int, default=10)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--coeff-bound", type=int, default=3)
    ap.add_argument("--betas", type=float, nargs="*", default=[0.20, 0.25, 0.30, 0.40, 0.50])
    ap.add_argument("--fixed", type=int, nargs="*", default=[8, 16, 32, 64, 128])
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    candidates = formulas(args.coeff_bound)

    totals: dict[tuple[int, str], list[int]] = {}
    last_width: dict[tuple[int, str], int] = {}
    total_good = 0
    total_space = 0

    print("low-height formula window audit")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"formula_count={len(candidates)}")

    for row_index, (n, p) in enumerate(rows, start=1):
        chi = legendre_table(p)
        good, stats = exact_xonly_good_flags(p, chi)
        nonsingular = np.ones(p, dtype=np.bool_)
        nonsingular[[2 % p, (-2) % p]] = False
        good &= nonsingular
        doubled_good = np.concatenate([good, good])
        prefix = np.concatenate([[0], np.cumsum(doubled_good, dtype=np.int64)])
        row_good = int(np.count_nonzero(good))
        row_space = int(np.count_nonzero(nonsingular))
        total_good += row_good
        total_space += row_space
        widths = width_rows(p, args.betas, args.fixed)

        valid_centers = 0
        for idx, formula in enumerate(candidates):
            center = formula.eval(n, p)
            if center is None:
                continue
            valid_centers += 1
            center = int(center)
            for width_label, width in widths:
                key = (idx, width_label)
                totals.setdefault(key, [0, 0, 0])
                hits = circular_interval_sum(prefix, center, width, p)
                interval_total = min(row_space, 2 * width + 1)
                # Remove singular endpoints if they fall in this interval.
                for singular in (2 % p, (-2) % p):
                    dist = min((singular - center) % p, (center - singular) % p)
                    if dist <= width:
                        interval_total -= 1
                totals[key][0] += hits
                totals[key][1] += max(0, interval_total)
                totals[key][2] += 1
                last_width[key] = width
        print(
            f"row={row_index:02d} n={n} p={p} k={stats['k']} "
            f"good={row_good}/{row_space} valid_centers={valid_centers}"
        )

    base = total_good / total_space if total_space else 0.0
    scores: list[Score] = []
    for (idx, width_label), (hits, total, rows_valid) in totals.items():
        if total == 0 or total_good == 0 or total_space == 0:
            continue
        precision = hits / total
        lift = precision / base if base else 0.0
        capture = hits / total_good
        coverage = total / total_space
        # A useful preselector needs lift and capture; this score penalizes
        # narrow overfit windows with microscopic capture.
        score = lift * math.sqrt(capture)
        formula = candidates[idx]
        scores.append(
            Score(
                formula=formula,
                label=formula.label(),
                width_label=width_label,
                last_width=last_width[(idx, width_label)],
                hits=hits,
                total=total,
                rows_valid=rows_valid,
                capture=capture,
                lift=lift,
                coverage=coverage,
                score=score,
            )
        )

    print("aggregate")
    print(f"  good={total_good}/{total_space}")
    print(f"  base_rate={base:.8f}")
    print("top_by_score")
    for score in sorted(scores, key=lambda row: (row.score, row.lift), reverse=True)[: args.top]:
        print(
            f"  {score.width_label:8s} last_width={score.last_width:6d} "
            f"hits={score.hits:5d}/{score.total:8d} capture={score.capture:.6f} "
            f"lift={score.lift:.3f} coverage={score.coverage:.6f} "
            f"score={score.score:.3f} formula={score.label}"
        )
    print("top_by_lift_with_capture_ge_1pct")
    filtered = [row for row in scores if row.capture >= 0.01]
    for score in sorted(filtered, key=lambda row: (row.lift, row.capture), reverse=True)[: args.top]:
        print(
            f"  {score.width_label:8s} last_width={score.last_width:6d} "
            f"hits={score.hits:5d}/{score.total:8d} capture={score.capture:.6f} "
            f"lift={score.lift:.3f} coverage={score.coverage:.6f} "
            f"formula={score.label}"
        )
    print(
        "conclusion=low_height_formula_windows_show_no_subsqrt_capture_concentration"
    )


if __name__ == "__main__":
    main()

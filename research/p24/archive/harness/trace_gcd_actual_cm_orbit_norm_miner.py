#!/usr/bin/env python3
"""Bounded actual-CM miner for trace-GCD right-orbit Fitting norms.

The pinned norm-triangle audit proves that the scalar, block-cycle, and
split-norm packages agree for one small CM row.  This script asks the next
theorem-finding question on a bounded stream of actual rows:

    are the positive-size right-orbit Fitting norms nonzero, and which
    structural tags separate failures from clean rows?

It deliberately scans small Hilbert class rows only.  It is a falsifier and
pattern miner for the p24 theorem surface, not a production search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from lang_trace_gcd_block_cycle_norm_audit import (
    MatrixRow,
    audit_matrix_row,
    class_representatives,
    frobenius_orbits,
    product_mod,
    records_by_omitted,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any


@dataclass(frozen=True)
class OrbitSummary:
    row_index: int
    D: int
    q: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    q_mod_right: int
    right_order: int
    right_is_prime: bool
    n_is_prime: bool
    omitted: int
    block_size: int
    orbit_rep: int
    orbit_len: int
    zero_dets: int
    orbit_norm: int
    det_mismatches: int

    @property
    def orbit_nonzero(self) -> bool:
        return self.orbit_norm != 0 and self.zero_dets == 0 and self.det_mismatches == 0


def iter_matrix_rows(args: argparse.Namespace):
    pari = Pari()
    pari.allocatemem(args.pari_stack_mb * 1024 * 1024)
    seen: set[int] = set()
    cases = 0
    yielded = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
        ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        if not splits:
            continue

        case_had_cycle = False
        for q, roots in splits:
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left is not None and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (
                                args.only_right is not None and right != args.only_right
                            ):
                                continue
                            if args.require_prime_right and not sp.isprime(right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_matrix_row(
                                    D,
                                    q,
                                    ell,
                                    cycle,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args,
                                )
                                if row is None:
                                    continue
                                if not row_has_positive_block(row, args.min_block_size):
                                    continue
                                yield row
                                yielded += 1
                                if yielded >= args.max_rows:
                                    return
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                return


def row_has_positive_block(row: MatrixRow, min_block_size: int) -> bool:
    for _omitted, records in records_by_omitted(row.records).items():
        reps, det_mismatches = class_representatives(records, row.right)
        if reps and len(reps[0].matrix) >= min_block_size:
            return True
        if det_mismatches and reps and len(reps[0].matrix) >= min_block_size:
            return True
    return False


def summarize_row(row_index: int, row: MatrixRow, min_block_size: int) -> list[OrbitSummary]:
    out: list[OrbitSummary] = []
    orbits = frobenius_orbits(row.right, row.q % row.right)
    right_order = int(sp.n_order(row.q % row.right, row.right))
    for omitted, records in records_by_omitted(row.records).items():
        reps, det_mismatches = class_representatives(records, row.right)
        if not reps:
            continue
        block_size = len(reps[0].matrix)
        if block_size < min_block_size:
            continue
        for orbit in orbits:
            dets = [int(reps[index].determinant) for index in orbit]
            out.append(
                OrbitSummary(
                    row_index=row_index,
                    D=row.D,
                    q=row.q,
                    h=row.h,
                    m=row.m,
                    n=row.n,
                    factor_degree=row.factor_degree,
                    extension_degree=row.extension_degree,
                    left=row.left,
                    right=row.right,
                    q_mod_right=row.q % row.right,
                    right_order=right_order,
                    right_is_prime=bool(sp.isprime(row.right)),
                    n_is_prime=bool(sp.isprime(row.n)),
                    omitted=omitted,
                    block_size=block_size,
                    orbit_rep=orbit[0],
                    orbit_len=len(orbit),
                    zero_dets=sum(1 for det in dets if det == 0),
                    orbit_norm=product_mod(dets, row.q),
                    det_mismatches=det_mismatches,
                )
            )
    return out


def tag_counter(rows: list[OrbitSummary], key) -> Counter[tuple[str, bool]]:
    counter: Counter[tuple[str, bool]] = Counter()
    for row in rows:
        counter[(str(key(row)), row.orbit_nonzero)] += 1
    return counter


def print_tag_summary(name: str, counter: Counter[tuple[str, bool]]) -> None:
    print(f"by_{name}")
    keys = sorted({key for key, _ok in counter})
    for key in keys:
        ok = counter[(key, True)]
        bad = counter[(key, False)]
        print(f"  {key}: nonzero={ok} zero_or_bad={bad}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("pinned", "scan"), default="pinned")
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=240)
    parser.add_argument("--max-abs-D", type=int, default=40000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=120)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=120000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=8)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--min-block-size", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--require-prime-right", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--pari-stack-mb", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    if args.profile == "pinned":
        args.max_rows = min(args.max_rows, 1)
        args.max_cases = max(args.max_cases, 24)
        args.max_h = max(args.max_h, 500)
        args.max_abs_D = max(args.max_abs_D, 80000)
        args.q_start = 13463
        args.q_stop = 13464
        args.max_splitting_primes = max(args.max_splitting_primes, 2)
        args.max_m = max(args.max_m, 120)
        args.max_n = max(args.max_n, 220)
        args.max_factor_degree = max(args.max_factor_degree, 8)
        args.max_extension_degree = max(args.max_extension_degree, 8)
        args.only_D = -13319
        args.only_q = 13463
        args.only_m = 28
        args.only_left = 4
        args.only_right = 7

    rows = list(iter_matrix_rows(args))
    summaries: list[OrbitSummary] = []
    for row_index, row in enumerate(rows):
        summaries.extend(summarize_row(row_index, row, args.min_block_size))

    print("trace-GCD actual-CM orbit-norm miner")
    print(f"profile={args.profile}")
    print(f"matrix_rows={len(rows)}")
    print(f"orbit_rows={len(summaries)}")
    print(f"min_block_size={args.min_block_size}")
    print(
        "columns: row D q h m n factor_deg ext_deg pair right qmod ord "
        "n_prime right_prime omitted block orbit len zero_dets norm nonzero"
    )
    for row in summaries:
        print(
            f"row={row.row_index} D={row.D} q={row.q} h={row.h} "
            f"m={row.m} n={row.n} factor_deg={row.factor_degree} "
            f"ext_deg={row.extension_degree} pair=({row.left},{row.right}) "
            f"right={row.right} qmod={row.q_mod_right} ord={row.right_order} "
            f"n_prime={int(row.n_is_prime)} right_prime={int(row.right_is_prime)} "
            f"omitted={row.omitted} block={row.block_size} "
            f"orbit={row.orbit_rep} len={row.orbit_len} "
            f"zero_dets={row.zero_dets} norm={row.orbit_norm} "
            f"nonzero={int(row.orbit_nonzero)}"
        )

    zero_or_bad = [row for row in summaries if not row.orbit_nonzero]
    print()
    print("totals")
    print(f"  nonzero_orbits={len(summaries) - len(zero_or_bad)}")
    print(f"  zero_or_bad_orbits={len(zero_or_bad)}")
    print(f"  determinant_mismatch_orbits={sum(1 for row in summaries if row.det_mismatches)}")
    print(f"  local_zero_det_orbits={sum(1 for row in summaries if row.zero_dets)}")
    print(f"  zero_norm_orbits={sum(1 for row in summaries if row.orbit_norm == 0)}")
    print_tag_summary("right_prime", tag_counter(summaries, lambda row: row.right_is_prime))
    print_tag_summary("n_prime", tag_counter(summaries, lambda row: row.n_is_prime))
    print_tag_summary("block_size", tag_counter(summaries, lambda row: row.block_size))
    print_tag_summary("right_order", tag_counter(summaries, lambda row: row.right_order))
    print("interpretation")
    print("  zero_or_bad_orbits=0 supports but does not prove the p24 Fitting p-unit theorem")
    print("  any zero_or_bad row falsifies the naive all-actual-CM universal version")
    print("  useful theorem hypotheses should explain the clean rows by structural tags")
    print("conclusion=reported_trace_gcd_actual_cm_orbit_norm_miner")


if __name__ == "__main__":
    main()

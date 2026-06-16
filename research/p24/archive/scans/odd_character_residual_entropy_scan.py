#!/usr/bin/env python3
"""Residual odd-character scan for strict near-square DANGER buckets.

The existing p24 scans cover low-degree quadratic character gates and dyadic
integer residues of A and j.  This tiny exact audit asks a narrower follow-up:

    after conditioning on the known Legendre sign chi(q(A,n)), does an odd
    low-order multiplicative coset of the same low-degree q add predictive
    entropy reduction for the strict x-only trace-v2/order bucket?

For the p24-shaped branch n == 0 mod 8, every p = n^2 + 7 has p == 7 mod 64,
so Fp has no quartic/octic characters.  The only multiplicative labels beyond
Legendre inside Fp are odd-order cosets.  This script tests those labels on
very small primes with a direct integer trace convolution; no FFT or NumPy is
used.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from dataclasses import dataclass


EXPR_NAMES = (
    "A",
    "A+2",
    "A-2",
    "A^2-4",
    "A^2-3",
    "A+n",
    "A-n",
    "A^2+n",
    "A^2-n",
    "A^2+nA+1",
    "A^2-nA+1",
)


@dataclass(frozen=True)
class RowData:
    n: int
    p: int
    k: int
    chi: list[int]
    logs: list[int]
    good: list[bool]
    nonsingular: list[bool]
    values: dict[str, list[int]]
    odd_orders: tuple[int, ...]


@dataclass(frozen=True)
class ResidualSummary:
    expr: str
    order: int
    rows: int
    support: int
    residual_bits: float
    median_best_lift: float
    max_best_lift: float


@dataclass(frozen=True)
class HoldoutRecord:
    expr: str
    order: int
    holdout_p: int
    train_rows: int
    sign: int
    residue: int
    train_lift: float
    train_capture: float
    holdout_lift: float
    holdout_hits: int
    holdout_total: int


def is_prime_trial(n: int) -> bool:
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


def prime_rows(
    min_p: int,
    max_p: int,
    max_rows: int,
    n_modulus: int,
    n_residue: int,
) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    start_n = max(2, math.isqrt(max(0, min_p - 7)))
    if start_n * start_n + 7 < min_p:
        start_n += 1
    first = start_n + ((n_residue - start_n) % n_modulus)
    for n in range(first, math.isqrt(max_p - 7) + 1, n_modulus):
        p = n * n + 7
        if p >= min_p and is_prime_trial(p):
            rows.append((n, p))
            if len(rows) >= max_rows:
                break
    return rows


def v2(n: int) -> int:
    if n == 0:
        return 999
    n = abs(n)
    return (n & -n).bit_length() - 1


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def binary_entropy(rate: float) -> float:
    if rate <= 0.0 or rate >= 1.0:
        return 0.0
    return -rate * math.log2(rate) - (1.0 - rate) * math.log2(1.0 - rate)


def legendre_table(p: int) -> list[int]:
    chi = [0] * p
    exp = (p - 1) // 2
    for a in range(1, p):
        r = pow(a, exp, p)
        chi[a] = 1 if r == 1 else -1
    return chi


def all_montgomery_traces_direct(p: int, chi: list[int]) -> list[int]:
    kernel = [chi[(c * c - 4) % p] for c in range(p)]
    traces: list[int] = []
    for A in range(p):
        total = 0
        for c, weight in enumerate(kernel):
            total += weight * chi[(A + c) % p]
        traces.append(-total)
    return traces


def strict_xonly_good_flags(p: int, chi: list[int]) -> tuple[list[bool], list[bool], int]:
    traces = all_montgomery_traces_direct(p, chi)
    k = verifier_k(p)
    good = [False] * p
    nonsingular = [True] * p

    for A, trace in enumerate(traces):
        disc = (A * A - 4) % p
        if disc == 0:
            nonsingular[A] = False
            continue
        curve_v = v2(p + 1 - trace)
        twist_v = v2(p + 1 + trace)
        if chi[disc] == 1:
            curve_exp = max(0, curve_v - 1)
            twist_exp = max(0, twist_v - 1)
        else:
            curve_exp = curve_v
            twist_exp = twist_v
        good[A] = max(curve_exp, twist_exp) >= k

    return good, nonsingular, k


def primitive_root(p: int) -> int:
    n = p - 1
    factors: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root for p={p}")


def log_table(p: int, g: int) -> list[int]:
    logs = [-1] * p
    x = 1
    for e in range(p - 1):
        logs[x] = e
        x = x * g % p
    return logs


def expr_value(name: str, A: int, n: int, p: int) -> int:
    A2 = A * A % p
    if name == "A":
        return A % p
    if name == "A+2":
        return (A + 2) % p
    if name == "A-2":
        return (A - 2) % p
    if name == "A^2-4":
        return (A2 - 4) % p
    if name == "A^2-3":
        return (A2 - 3) % p
    if name == "A+n":
        return (A + n) % p
    if name == "A-n":
        return (A - n) % p
    if name == "A^2+n":
        return (A2 + n) % p
    if name == "A^2-n":
        return (A2 - n) % p
    if name == "A^2+nA+1":
        return (A2 + n * A + 1) % p
    if name == "A^2-nA+1":
        return (A2 - n * A + 1) % p
    raise ValueError(name)


def build_row(n: int, p: int, max_order: int) -> RowData:
    chi = legendre_table(p)
    good, nonsingular, k = strict_xonly_good_flags(p, chi)
    g = primitive_root(p)
    logs = log_table(p, g)
    values = {
        name: [expr_value(name, A, n, p) for A in range(p)]
        for name in EXPR_NAMES
    }
    odd_orders = tuple(m for m in range(3, max_order + 1, 2) if (p - 1) % m == 0)
    return RowData(
        n=n,
        p=p,
        k=k,
        chi=chi,
        logs=logs,
        good=good,
        nonsingular=nonsingular,
        values=values,
        odd_orders=odd_orders,
    )


def sign_counts(row: RowData, expr: str) -> dict[int, list[int]]:
    counts = {-1: [0, 0], 1: [0, 0]}
    for A, value in enumerate(row.values[expr]):
        if not row.nonsingular[A] or value == 0:
            continue
        sign = row.chi[value]
        if sign == 0:
            continue
        counts[sign][0] += 1
        counts[sign][1] += int(row.good[A])
    return counts


def coset_counts(row: RowData, expr: str, order: int) -> dict[tuple[int, int], list[int]]:
    counts: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    for A, value in enumerate(row.values[expr]):
        if not row.nonsingular[A] or value == 0:
            continue
        sign = row.chi[value]
        if sign == 0:
            continue
        residue = row.logs[value] % order
        counts[(sign, residue)][0] += 1
        counts[(sign, residue)][1] += int(row.good[A])
    return counts


def residual_summaries(rows: list[RowData], max_order: int) -> list[ResidualSummary]:
    accum: dict[tuple[str, int], dict[str, object]] = defaultdict(
        lambda: {"support": 0, "sign_mass": 0.0, "coset_mass": 0.0, "best_lifts": [], "rows": 0}
    )
    for row in rows:
        for expr in EXPR_NAMES:
            signs = sign_counts(row, expr)
            support = sum(total for total, _hits in signs.values())
            if support == 0:
                continue
            sign_mass = sum(
                total * binary_entropy(hits / total)
                for total, hits in signs.values()
                if total
            )
            sign_rates = {
                sign: hits / total if total else 0.0
                for sign, (total, hits) in signs.items()
            }
            for order in row.odd_orders:
                if order > max_order:
                    continue
                buckets = coset_counts(row, expr, order)
                coset_mass = sum(
                    total * binary_entropy(hits / total)
                    for total, hits in buckets.values()
                    if total
                )
                best_lift = 0.0
                for (sign, _residue), (total, hits) in buckets.items():
                    base = sign_rates[sign]
                    if total and base:
                        best_lift = max(best_lift, (hits / total) / base)

                slot = accum[(expr, order)]
                slot["support"] = int(slot["support"]) + support
                slot["sign_mass"] = float(slot["sign_mass"]) + sign_mass
                slot["coset_mass"] = float(slot["coset_mass"]) + coset_mass
                slot["rows"] = int(slot["rows"]) + 1
                slot["best_lifts"].append(best_lift)

    out: list[ResidualSummary] = []
    for (expr, order), slot in accum.items():
        support = int(slot["support"])
        if not support:
            continue
        lifts = sorted(float(x) for x in list(slot["best_lifts"]))
        mid = len(lifts) // 2
        median = lifts[mid] if len(lifts) % 2 else 0.5 * (lifts[mid - 1] + lifts[mid])
        residual_bits = (float(slot["sign_mass"]) - float(slot["coset_mass"])) / support
        out.append(
            ResidualSummary(
                expr=expr,
                order=order,
                rows=int(slot["rows"]),
                support=support,
                residual_bits=residual_bits,
                median_best_lift=median,
                max_best_lift=max(lifts),
            )
        )
    return sorted(out, key=lambda row: (row.residual_bits, row.median_best_lift), reverse=True)


def merge_counts(rows: list[RowData], expr: str, order: int) -> tuple[dict[int, list[int]], dict[tuple[int, int], list[int]], int]:
    signs = {-1: [0, 0], 1: [0, 0]}
    buckets: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    used_rows = 0
    for row in rows:
        if order not in row.odd_orders:
            continue
        used_rows += 1
        row_signs = sign_counts(row, expr)
        for sign, (total, hits) in row_signs.items():
            signs[sign][0] += total
            signs[sign][1] += hits
        for key, (total, hits) in coset_counts(row, expr, order).items():
            buckets[key][0] += total
            buckets[key][1] += hits
    return signs, buckets, used_rows


def leave_one_out(
    rows: list[RowData],
    max_order: int,
    min_train_rows: int,
    min_train_total: int,
) -> list[HoldoutRecord]:
    records: list[HoldoutRecord] = []
    for holdout_index, holdout in enumerate(rows):
        train = [row for idx, row in enumerate(rows) if idx != holdout_index]
        for expr in EXPR_NAMES:
            for order in holdout.odd_orders:
                if order > max_order:
                    continue
                train_signs, train_buckets, used_rows = merge_counts(train, expr, order)
                if used_rows < min_train_rows:
                    continue
                best: tuple[float, float, int, int, int, int] | None = None
                for (sign, residue), (total, hits) in train_buckets.items():
                    sign_total, sign_hits = train_signs[sign]
                    if total < min_train_total or not sign_total or not sign_hits:
                        continue
                    precision = hits / total
                    base = sign_hits / sign_total
                    lift = precision / base if base else 0.0
                    capture = hits / sign_hits
                    score = lift * math.sqrt(capture)
                    candidate = (score, lift, sign, residue, total, hits)
                    if best is None or candidate > best:
                        best = candidate
                if best is None:
                    continue

                _score, train_lift, sign, residue, _train_total, train_hits = best
                holdout_signs = sign_counts(holdout, expr)
                holdout_buckets = coset_counts(holdout, expr, order)
                holdout_total, holdout_hits = holdout_buckets.get((sign, residue), [0, 0])
                sign_total, sign_hits = holdout_signs[sign]
                if not holdout_total or not sign_total or not sign_hits:
                    holdout_lift = 0.0
                else:
                    holdout_lift = (holdout_hits / holdout_total) / (sign_hits / sign_total)
                records.append(
                    HoldoutRecord(
                        expr=expr,
                        order=order,
                        holdout_p=holdout.p,
                        train_rows=used_rows,
                        sign=sign,
                        residue=residue,
                        train_lift=train_lift,
                        train_capture=train_hits / train_signs[sign][1],
                        holdout_lift=holdout_lift,
                        holdout_hits=holdout_hits,
                        holdout_total=holdout_total,
                    )
                )
    return sorted(records, key=lambda row: (row.train_lift, row.holdout_lift), reverse=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=50)
    ap.add_argument("--max-p", type=int, default=3_000)
    ap.add_argument("--max-rows", type=int, default=5)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    ap.add_argument("--max-order", type=int, default=15)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--min-train-rows", type=int, default=2)
    ap.add_argument("--min-train-total", type=int, default=20)
    args = ap.parse_args()

    rows_np = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    rows = [build_row(n, p, args.max_order) for n, p in rows_np]

    print("odd-character residual entropy scan")
    print("family=p=n^2+7")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"rows={len(rows)}")
    print(f"n_modulus={args.n_modulus}")
    print(f"n_residue={args.n_residue}")
    print(f"max_order={args.max_order}")
    print("expressions=" + ",".join(EXPR_NAMES))
    print()

    for row in rows:
        total = sum(row.nonsingular)
        hits = sum(1 for A in range(row.p) if row.nonsingular[A] and row.good[A])
        print(
            f"row n={row.n:3d} p={row.p:5d} k={row.k} "
            f"good={hits:4d}/{total:4d} density={hits / total:.6f} "
            f"odd_orders={list(row.odd_orders)}"
        )
    print()

    summaries = residual_summaries(rows, args.max_order)
    print("top_residual_entropy_after_legendre")
    for row in summaries[: args.top]:
        print(
            f"  expr={row.expr:11s} order={row.order:2d} rows={row.rows:2d} "
            f"support={row.support:5d} residual_bits={row.residual_bits:.6f} "
            f"median_best_lift={row.median_best_lift:.3f} max_best_lift={row.max_best_lift:.3f}"
        )
    print()

    holdouts = leave_one_out(rows, args.max_order, args.min_train_rows, args.min_train_total)
    print("leave_one_out_top_train_lifts")
    for row in holdouts[: args.top]:
        print(
            f"  holdout_p={row.holdout_p:5d} expr={row.expr:11s} order={row.order:2d} "
            f"sign={row.sign:+d} residue={row.residue:2d} train_rows={row.train_rows} "
            f"train_lift={row.train_lift:.3f} train_capture={row.train_capture:.3f} "
            f"holdout_lift={row.holdout_lift:.3f} holdout_hits={row.holdout_hits}/{row.holdout_total}"
        )
    if holdouts:
        holdout_lifts = sorted(row.holdout_lift for row in holdouts)
        median_holdout = holdout_lifts[len(holdout_lifts) // 2]
        positive = sum(1 for row in holdouts if row.holdout_lift > 1.0)
        print(
            f"leave_one_out_summary evaluations={len(holdouts)} "
            f"median_holdout_lift={median_holdout:.3f} "
            f"positive_holdout_lifts={positive}/{len(holdouts)} "
            f"best_holdout_lift={max(holdout_lifts):.3f}"
        )
    else:
        print("leave_one_out_summary evaluations=0")

    best_bits = summaries[0].residual_bits if summaries else 0.0
    best_holdout = max((row.holdout_lift for row in holdouts), default=0.0)
    if best_bits < 0.05 and best_holdout < 2.0:
        print("conclusion=no_nonconstant_odd_character_residual_entropy_reduction_seen")
    else:
        print("conclusion=odd_character_residual_lead_needs_larger_holdout")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""P27 halving u+2 x-square gate probe.

For a successful Montgomery halving step, the two half x-coordinates satisfy
    x' + 1/x' = u.
This probe verifies on the p27 compactD stream that the next x-square gate can
be tested as chi(u+2), before taking sqrt(u^2-4) to materialize x'.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_label2_alpha_branch_recurrence_probe import (
    P,
    halve_all,
    inv,
    legendre,
    sample_rows,
    sqrt_mod,
)


def halve_u_records(a: int, x: int, p: int = P) -> tuple[int, list[dict[str, object]]]:
    d = (x * x + a * x + 1) % p
    sd = sqrt_mod(d, p)
    if sd is None:
        return legendre(d, p), []

    inv2 = (p + 1) // 2
    records: list[dict[str, object]] = []
    for sign, rd in [(1, sd), (-1, (-sd) % p)]:
        u = (2 * x + 2 * rd) % p
        w = (u * u - 4) % p
        sw = sqrt_mod(w, p)
        xs: list[int] = []
        if sw is not None:
            for cand in [((u + sw) * inv2) % p, ((u - sw) * inv2) % p]:
                if cand and cand not in xs:
                    xs.append(cand)
        records.append(
            {
                "sign": sign,
                "u": u,
                "w_chi": legendre(w, p),
                "u_plus_2_chi": legendre(u + 2, p),
                "u_minus_2_chi": legendre(u - 2, p),
                "xs": xs,
            }
        )
    return 1, records


def check_step(a: int, x: int, p: int = P) -> dict[str, object]:
    d_chi, records = halve_u_records(a, x, p)
    out: dict[str, object] = {
        "d_chi": d_chi,
        "records": records,
        "good_records": 0,
        "x_count": 0,
        "product_mismatch": 0,
        "uplus_mismatch": 0,
        "uminus_mismatch": 0,
        "uplus_uminus_mismatch": 0,
        "next_d_mismatch": 0,
        "next_d_plus": 0,
        "next_d_minus": 0,
        "next_d_zero": 0,
        "prefilter_class": 0,
    }
    if d_chi != 1:
        return out

    good = [rec for rec in records if int(rec["w_chi"]) == 1]
    out["good_records"] = len(good)
    for rec in good:
        xs = rec["xs"]
        assert isinstance(xs, list)
        out["x_count"] = int(out["x_count"]) + len(xs)
        up = int(rec["u_plus_2_chi"])
        um = int(rec["u_minus_2_chi"])
        if up != um:
            out["uplus_uminus_mismatch"] = int(out["uplus_uminus_mismatch"]) + 1
        if xs:
            out["prefilter_class"] = up
        if len(xs) == 2 and xs[0] * xs[1] % p != 1:
            out["product_mismatch"] = int(out["product_mismatch"]) + 1
        for xp in xs:
            x_chi = legendre(xp, p)
            if x_chi != up:
                out["uplus_mismatch"] = int(out["uplus_mismatch"]) + 1
            if x_chi != um:
                out["uminus_mismatch"] = int(out["uminus_mismatch"]) + 1
            next_d = legendre(xp * xp + a * xp + 1, p)
            if next_d != x_chi:
                out["next_d_mismatch"] = int(out["next_d_mismatch"]) + 1
            if next_d == 1:
                out["next_d_plus"] = int(out["next_d_plus"]) + 1
            elif next_d == -1:
                out["next_d_minus"] = int(out["next_d_minus"]) + 1
            else:
                out["next_d_zero"] = int(out["next_d_zero"]) + 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=1000000)
    args = parser.parse_args()

    rows, sample_stats = sample_rows(args.target, args.seed, args.max_draws)
    totals: Counter = Counter()
    d3_prefilter: Counter = Counter()
    d4_prefilter: Counter = Counter()

    for row in rows:
        for key in ["root0", "root1"]:
            cand = row[key]
            assert isinstance(cand, dict)
            a = int(cand["A"])
            x5 = int(cand["x5"])
            d2 = check_step(a, x5)
            totals["d2_roots"] += 1
            for name in [
                "good_records",
                "x_count",
                "product_mismatch",
                "uplus_mismatch",
                "uminus_mismatch",
                "uplus_uminus_mismatch",
                "next_d_mismatch",
                "next_d_plus",
                "next_d_minus",
                "next_d_zero",
            ]:
                totals[f"d2_{name}"] += int(d2[name])
            d3_prefilter[int(d2["prefilter_class"])] += 1

            _, x6s = halve_all(a, x5)
            for x6 in x6s:
                if legendre(x6 * x6 + a * x6 + 1) != 1:
                    continue
                d3 = check_step(a, x6)
                totals["d3plus_x6"] += 1
                for name in [
                    "good_records",
                    "x_count",
                    "product_mismatch",
                    "uplus_mismatch",
                    "uminus_mismatch",
                    "uplus_uminus_mismatch",
                    "next_d_mismatch",
                    "next_d_plus",
                    "next_d_minus",
                    "next_d_zero",
                ]:
                    totals[f"d3_{name}"] += int(d3[name])
                d4_prefilter[int(d3["prefilter_class"])] += 1

    print("p27 halving u+2 x-square gate probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"sampled_pairs = {len(rows)}")
    for key in sorted(sample_stats):
        print(f"sample_stat {key} = {sample_stats[key]}")
    print("d2_to_d3_gate:")
    for key in sorted(k for k in totals if k.startswith("d2_")):
        print(f"  {key[3:]} = {totals[key]}")
    print("  prefilter_class_counts:")
    for cls in [-1, 0, 1]:
        print(f"    chi_u_plus_2={cls} count={d3_prefilter[cls]}")
    d2_roots = totals["d2_roots"]
    print(
        "  reject_before_sqrt_w_share = "
        f"{(d3_prefilter[-1] / d2_roots) if d2_roots else 0.0:.9f}"
    )
    print("d3_to_d4_gate:")
    for key in sorted(k for k in totals if k.startswith("d3_")):
        print(f"  {key[3:]} = {totals[key]}")
    print("  prefilter_class_counts:")
    for cls in [-1, 0, 1]:
        print(f"    chi_u_plus_2={cls} count={d4_prefilter[cls]}")
    d3_roots = totals["d3plus_x6"]
    print(
        "  reject_before_sqrt_w_share = "
        f"{(d4_prefilter[-1] / d3_roots) if d3_roots else 0.0:.9f}"
    )
    print("p27_halving_usquare_gate_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

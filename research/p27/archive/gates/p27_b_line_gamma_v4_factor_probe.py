#!/usr/bin/env python3
"""Probe the V4 factorization of the p27 B-line gamma transition.

For the handoff quartic in Y=v+2,

    A = B^2 - 2
    H^2 = u + 2
    F_A(u,v)=0
    Y = v + 2,

the polynomial P(Y)=0 has square discriminant and split cubic resolvent.  In
fact, after adjoining

    R^2 = H^2 - 4
    S^2 = B^2 + H^2 - 4,

the four Y roots are

    (H + R)(H + S), (H + R)(H - S),
    (H - R)(H + S), (H - R)(H - S).

This probe verifies the identity on the frozen guard-field handoff and records
whether the induced characters give a source handle.  The expected outcome is
subtle: gamma decomposes as a product of two sheet-dependent half-norm phases,
but the product is the canonical f4 bit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any, Optional

from p27_b_line_gamma_h90_quotient_probe import sqrt_mod_square
from p27_label2_alpha_branch_recurrence_probe import legendre


DEFAULT_HANDOFF = Path("research/p27/archive/fixtures/p27_b_line_gamma_class_handoff_20260622.json")


def sign_to_int(label: str) -> int:
    if label == "plus":
        return 1
    if label == "minus":
        return -1
    if label == "zero":
        return 0
    raise ValueError(f"bad sign label {label!r}")


def signed_roots(root: Optional[int], q: int) -> list[int]:
    if root is None:
        return []
    return sorted({root % q, (-root) % q})


def sqrt_roots(value: int, q: int) -> list[int]:
    return signed_roots(sqrt_mod_square(value, q), q)


def product_roots(H: int, R: int, S: int, q: int) -> set[int]:
    roots = set()
    for rsign in (1, -1):
        for ssign in (1, -1):
            roots.add((H + rsign * R) * (H + ssign * S) % q)
    return roots


def chi(value: int, q: int) -> int:
    return legendre(value % q, q)


def row_checks(row: dict[str, Any], q: int) -> tuple[Counter, list[dict[str, int]]]:
    stats: Counter = Counter()
    records: list[dict[str, int]] = []
    B = int(row["B"]) % q
    H2 = int(row["H2"]) % q
    target_y = {(int(v) + 2) % q for v in row["generic_v_roots"]}
    target_sign = sign_to_int(str(row["f4"]))

    H_roots = [int(value) % q for value in row["H_roots"]]
    if len(H_roots) != 2:
        stats["bad_H_root_count"] += 1
        return stats, records

    R_roots = sqrt_roots(H2 - 4, q)
    S_roots = sqrt_roots(B * B + H2 - 4, q)
    stats[f"R_roots_{len(R_roots)}"] += 1
    stats[f"S_roots_{len(S_roots)}"] += 1
    if len(R_roots) != 2:
        stats["bad_R_root_count"] += 1
        return stats, records
    if len(S_roots) != 2:
        stats["bad_S_root_count"] += 1
        return stats, records

    # For a fixed H sheet, the root set is independent of the chosen signs of
    # R and S.  Character factors alpha/beta are sign-independent in R/S but
    # flip together under H -> -H.
    for H in H_roots:
        R = R_roots[0]
        S = S_roots[0]
        roots = product_roots(H, R, S, q)
        if roots != target_y:
            stats["v4_roots_mismatch"] += 1

        alpha_values = {chi(H + rsign * R, q) for rsign in (1, -1)}
        beta_values = {chi(H + ssign * S, q) for ssign in (1, -1)}
        product_values = {
            chi((H + rsign * R) * (H + ssign * S), q)
            for rsign in (1, -1)
            for ssign in (1, -1)
        }
        if len(alpha_values) != 1:
            stats["alpha_R_sign_not_invariant"] += 1
        if len(beta_values) != 1:
            stats["beta_S_sign_not_invariant"] += 1
        if product_values != {target_sign}:
            stats["alpha_beta_product_not_f4"] += 1

        alpha = next(iter(alpha_values)) if len(alpha_values) == 1 else 0
        beta = next(iter(beta_values)) if len(beta_values) == 1 else 0
        stats[f"alpha_{alpha}"] += 1
        stats[f"beta_{beta}"] += 1
        stats[f"product_{alpha * beta}"] += 1
        records.append(
            {
                "B": B,
                "u": int(row["u"]) % q,
                "H": H,
                "alpha": alpha,
                "beta": beta,
                "product": alpha * beta,
                "f4": target_sign,
            }
        )

    if len(records) == 2:
        a0, a1 = records[0]["alpha"], records[1]["alpha"]
        b0, b1 = records[0]["beta"], records[1]["beta"]
        p0, p1 = records[0]["product"], records[1]["product"]
        if a0 + a1:
            stats["alpha_not_flipped_by_H"] += 1
        if b0 + b1:
            stats["beta_not_flipped_by_H"] += 1
        if p0 != p1:
            stats["product_not_H_invariant"] += 1

    if chi(4 - B * B, q) != 1:
        stats["four_minus_B2_not_square"] += 1
    return stats, records


def summarize_variation(records: list[dict[str, int]]) -> Counter:
    stats: Counter = Counter()
    by_B: dict[int, list[dict[str, int]]] = defaultdict(list)
    by_Bu: dict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    for record in records:
        by_B[record["B"]].append(record)
        by_Bu[(record["B"], record["u"])].append(record)

    for B, items in by_B.items():
        products = {item["product"] for item in items}
        alphas = {item["alpha"] for item in items}
        betas = {item["beta"] for item in items}
        if len(products) == 1:
            stats["B_product_constant"] += 1
        else:
            stats["B_product_mixed"] += 1
        if len(alphas) == 1:
            stats["B_alpha_constant"] += 1
        else:
            stats["B_alpha_mixed"] += 1
        if len(betas) == 1:
            stats["B_beta_constant"] += 1
        else:
            stats["B_beta_mixed"] += 1

    for _key, items in by_Bu.items():
        if len(items) != 2:
            stats["Bu_bad_H_sheet_count"] += 1
            continue
        if items[0]["product"] == items[1]["product"]:
            stats["Bu_product_H_invariant"] += 1
        else:
            stats["Bu_product_H_mixed"] += 1
        if items[0]["alpha"] == -items[1]["alpha"]:
            stats["Bu_alpha_flips"] += 1
        else:
            stats["Bu_alpha_not_flipped"] += 1
        if items[0]["beta"] == -items[1]["beta"]:
            stats["Bu_beta_flips"] += 1
        else:
            stats["Bu_beta_not_flipped"] += 1
    return stats


def run_field(fixture: dict[str, Any]) -> None:
    q = int(fixture["field"])
    stats: Counter = Counter()
    records: list[dict[str, int]] = []
    for row in fixture["rows"]:
        row_stats, row_records = row_checks(row, q)
        stats.update(row_stats)
        records.extend(row_records)
    stats.update(summarize_variation(records))
    stats["records"] = len(records)
    stats["handoff_rows"] = int(fixture["row_count"])
    for key in (
        "bad_H_root_count",
        "bad_R_root_count",
        "bad_S_root_count",
        "v4_roots_mismatch",
        "alpha_R_sign_not_invariant",
        "beta_S_sign_not_invariant",
        "alpha_beta_product_not_f4",
        "alpha_not_flipped_by_H",
        "beta_not_flipped_by_H",
        "product_not_H_invariant",
        "four_minus_B2_not_square",
        "Bu_bad_H_sheet_count",
        "Bu_product_H_mixed",
        "Bu_alpha_not_flipped",
        "Bu_beta_not_flipped",
    ):
        stats.setdefault(key, 0)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF)
    args = parser.parse_args()

    packet = json.loads(args.handoff.read_text())
    print("p27 B-line gamma V4 factor probe")
    print("question = does gamma decompose into lower half-norm phases?")
    print("identity = v+2 in {(H +/- R)(H +/- S)}")
    print("R2 = H^2 - 4")
    print("S2 = B^2 + H^2 - 4")
    print(f"handoff = {args.handoff}")
    for fixture in packet["fixtures"]:
        run_field(fixture)
    print("p27_b_line_gamma_v4_factor_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

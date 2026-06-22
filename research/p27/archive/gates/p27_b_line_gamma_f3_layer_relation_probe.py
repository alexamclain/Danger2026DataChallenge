#!/usr/bin/env python3
"""Relation screen for gamma over the explicit f3/H90 layer.

The gamma H90 quotient collapses to the first reduced layer:

    H^2 = u + 2,  where H = h + 1/h.

This probe asks whether the remaining f4 class becomes visible after making
that layer explicit.  It doubles each materialized pair by H -> +/-H (and
tau -> tau, tau^-1) and then checks all rows and f4 sign subcovers for
low-degree relations in quotient-friendly coordinates.

The target is a concrete source/correspondence clue.  A negative means that
gamma still needs actual divisor/Kummer-class extraction over the normalized
f3/H90 layer.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import json

from p27_b_line_gamma_h90_quotient_probe import DEFAULT_FIRST, build_rows, inv
from p27_conic_pair_invariant_relation_probe import relation_stats_for_system
from p27_kline_reverse_z_relation_probe import parse_ints


def h_layer_rows(q: int, first: dict) -> tuple[list[dict[str, int]], Counter]:
    base_rows, base_stats = build_rows(q, first)
    rows: list[dict[str, int]] = []
    stats: Counter = Counter(base_stats)
    for row in base_rows:
        tau_inv = inv(row["tau"], q)
        if tau_inv is None:
            stats["tau_inverse_missing"] += 1
            continue
        for H, tau, sheet in (
            (row["h_sym"], row["tau"], 1),
            ((-row["h_sym"]) % q, tau_inv, -1),
        ):
            rows.append(
                {
                    "B": row["B"],
                    "A": row["A"],
                    "u": row["u"],
                    "H": H,
                    "H2": H * H % q,
                    "tau": tau,
                    "tau2": tau * tau % q,
                    "tau_sym": row["tau_sym"],
                    "v_sum": row["v_sum"],
                    "v_prod": row["v_prod"],
                    "gamma_norm": row["gamma_norm"],
                    "sheet": sheet,
                    "f4": row["f4"],
                }
            )
    stats["h_layer_rows"] = len(rows)
    stats["h_layer_f4_plus"] = sum(1 for row in rows if row["f4"] == 1)
    stats["h_layer_f4_minus"] = sum(1 for row in rows if row["f4"] == -1)
    return rows, stats


def systems(rows: list[dict[str, int]]) -> dict[str, list[tuple[int, ...]]]:
    out: dict[str, list[tuple[int, ...]]] = {
        "B_H": [],
        "B_tau": [],
        "B_H2": [],
        "B_tau_sym": [],
        "B_u_H": [],
        "B_H_tau": [],
        "B_H_plus": [],
        "B_H_minus": [],
        "B_tau_plus": [],
        "B_tau_minus": [],
        "B_u_H_plus": [],
        "B_u_H_minus": [],
    }
    for row in rows:
        B = row["B"]
        u = row["u"]
        H = row["H"]
        tau = row["tau"]
        sign = row["f4"]
        out["B_H"].append((B, H))
        out["B_tau"].append((B, tau))
        out["B_H2"].append((B, row["H2"]))
        out["B_tau_sym"].append((B, row["tau_sym"]))
        out["B_u_H"].append((B, u, H))
        out["B_H_tau"].append((B, H, tau))
        if sign == 1:
            out["B_H_plus"].append((B, H))
            out["B_tau_plus"].append((B, tau))
            out["B_u_H_plus"].append((B, u, H))
        elif sign == -1:
            out["B_H_minus"].append((B, H))
            out["B_tau_minus"].append((B, tau))
            out["B_u_H_minus"].append((B, u, H))
    return out


def relation_lines(label: str, points: list[tuple[int, ...]], q: int, degrees: list[int]) -> list[str]:
    unique = sorted(set(points))
    stats = relation_stats_for_system(unique, q, degrees)
    out = [f"  relation_{label}:", f"    rows = {len(points)}", f"    unique = {len(unique)}"]
    for degree in degrees:
        prefix = f"deg{degree}"
        out.append(
            "    "
            f"{prefix}: monomials={stats[f'{prefix}_monomials']} "
            f"rank={stats[f'{prefix}_rank']} "
            f"nullity={stats[f'{prefix}_nullity']} "
            f"forced={stats[f'{prefix}_forced_nullity']} "
            f"extra={stats[f'{prefix}_extra_nullity']}"
        )
    return out


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def run_field(q: int, first: dict, pair_degrees: list[int], triple_degrees: list[int]) -> None:
    rows, stats = h_layer_rows(q, first)
    # Make the tautological layer identities explicit.
    stats["H2_minus_uplus2_fail"] = sum(
        1 for row in rows if (row["H2"] - (row["u"] + 2)) % q
    )
    stats["tau_sym_formula_fail"] = 0
    for row in rows:
        denom = (row["u"] - 2) % q
        if denom == 0:
            stats["tau_sym_formula_denominator_zero"] += 1
            continue
        expected = 2 * (row["u"] + 6) * pow(denom, q - 2, q) % q
        if (row["tau_sym"] - expected) % q:
            stats["tau_sym_formula_fail"] += 1

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")

    by_name = systems(rows)
    for name in (
        "B_H",
        "B_tau",
        "B_H2",
        "B_tau_sym",
        "B_H_plus",
        "B_H_minus",
        "B_tau_plus",
        "B_tau_minus",
    ):
        for line in relation_lines(name, by_name[name], q, pair_degrees):
            print(line)
    for name in ("B_u_H", "B_H_tau", "B_u_H_plus", "B_u_H_minus"):
        for line in relation_lines(name, by_name[name], q, triple_degrees):
            print(line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--pair-degrees", default="2,4,6,8,10,12,14,16,18,20")
    parser.add_argument("--triple-degrees", default="2,4,6,8,10")
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    pair_degrees = parse_degrees(args.pair_degrees)
    triple_degrees = parse_degrees(args.triple_degrees)

    print("p27 B-line gamma over f3/H90 layer relation probe")
    print("question = does gamma become low-degree/sourceable after adjoining H^2=u+2?")
    print(f"first_fixture = {args.first_fixture}")
    print(f"pair_degrees = {args.pair_degrees}")
    print(f"triple_degrees = {args.triple_degrees}")
    for q in parse_ints(args.small_primes):
        run_field(q, first, pair_degrees, triple_degrees)
    print("p27_b_line_gamma_f3_layer_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Low-degree relation screen for the reduced p27 B-line d3 fiber.

The reduced fixture freezes, for each legal B, four values of u=x+1/x with
f3(B)=chi(u+2).  This probe asks whether the all-cover or either sign subcover
has an extra low-degree plane relation in natural B-line coordinates.

It reports only extra nullity beyond interpolation forced by point count.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from p27_conic_pair_invariant_relation_probe import relation_stats_for_system


DEFAULT_FIXTURE = Path("research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json")


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def maybe_div(num: int, den: int, p: int) -> int | None:
    iden = inv(den, p)
    if iden is None:
        return None
    return num % p * iden % p


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def systems_for_field(fixture: dict[str, Any]) -> dict[str, list[tuple[int, int]]]:
    q = int(fixture["field"])
    systems: dict[str, list[tuple[int, int]]] = {
        "B_u": [],
        "B_u2": [],
        "B_uplus2": [],
        "A_u": [],
        "lambda_u": [],
        "mu_u": [],
        "B_u_plus": [],
        "B_u_minus": [],
    }
    for row in fixture["rows"]:
        B = int(row["B"])
        A = (B * B - 2) % q
        lam = maybe_div(B, B + 2, q)
        mu = maybe_div(B - 2, B + 2, q)
        sign = str(row["sign"])
        for u_raw in row["u_roots"]:
            u = int(u_raw) % q
            systems["B_u"].append((B, u))
            systems["B_u2"].append((B, u * u % q))
            systems["B_uplus2"].append((B, (u + 2) % q))
            systems["A_u"].append((A, u))
            if lam is not None:
                systems["lambda_u"].append((lam, u))
            if mu is not None:
                systems["mu_u"].append((mu, u))
            if sign == "plus":
                systems["B_u_plus"].append((B, u))
            elif sign == "minus":
                systems["B_u_minus"].append((B, u))
    return systems


def print_system_stats(label: str, points: list[tuple[int, int]], q: int, degrees: list[int]) -> None:
    unique_points = sorted(set(points))
    stats: Counter = relation_stats_for_system(unique_points, q, degrees)
    print(f"{label}:")
    print(f"  rows = {len(points)}")
    print(f"  unique = {len(unique_points)}")
    for degree in degrees:
        prefix = f"deg{degree}"
        print(
            "  "
            f"{prefix}: monomials={stats[f'{prefix}_monomials']} "
            f"rank={stats[f'{prefix}_rank']} "
            f"nullity={stats[f'{prefix}_nullity']} "
            f"forced={stats[f'{prefix}_forced_nullity']} "
            f"extra={stats[f'{prefix}_extra_nullity']}"
        )
        if stats[f"{prefix}_extra_nullity"]:
            print(
                "  "
                f"{prefix}_relation_terms={stats[f'{prefix}_relation_terms']} "
                f"self_mismatches={stats[f'{prefix}_relation_self_mismatches']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--degrees", default="2,4,6,8,10,12,14,16,18,20")
    parser.add_argument(
        "--systems",
        default="B_u,B_u2,B_uplus2,A_u,lambda_u,mu_u,B_u_plus,B_u_minus",
    )
    args = parser.parse_args()

    degrees = parse_ints(args.degrees)
    requested_systems = [part.strip() for part in args.systems.split(",") if part.strip()]
    packet = load_fixture(args.fixture)

    print("p27 B-line reduced-fiber relation probe")
    print("question = does the 4-u d3 cover have a low-degree plane relation?")
    print(f"fixture = {args.fixture}")
    print(f"degrees = {degrees}")
    print(f"systems = {requested_systems}")

    for fixture in packet["fixtures"]:
        q = int(fixture["field"])
        print(f"q={q}:")
        systems = systems_for_field(fixture)
        for name in requested_systems:
            print_system_stats(f"q{q}_{name}", systems[name], q, degrees)

    print("p27_b_line_reduced_fiber_relation_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

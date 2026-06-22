#!/usr/bin/env python3
"""Bridge the frozen B-line and K/Sroot Kummer fixture packets.

The B and K-line bridge was already checked for d3/d4 from reconstructed
finite-field rows.  This probe checks the actual JSON fixtures used as CAS
handoffs, including the conditional tail rows and the signed Sroot sheets.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any


DEFAULT_B_PACKET = Path("research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json")
DEFAULT_KS_PACKET = Path("research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json")


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def sqrt_table(p: int) -> list[list[int]]:
    roots: list[list[int]] = [[] for _ in range(p)]
    for x in range(p):
        roots[x * x % p].append(x)
    return roots


def b_to_k_square(B: int, p: int) -> int | None:
    B %= p
    if B == 0 or (B + 2) % p == 0:
        return None
    num = pow((B - 2) % p, 4, p)
    den = 8 * B % p * ((B + 2) % p) ** 2 % p
    return num * inv(den, p) % p


def load_packet(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def fixture_by_field(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(fixture["field"]): fixture for fixture in packet["fixtures"]}


def family_map(fixture: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {family["name"]: family for family in fixture["families"]}


def row_signs(rows: list[dict[str, Any]], key: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for row in rows:
        value = int(row[key])
        sign = str(row["sign"])
        if value in out and out[value] != sign:
            raise ValueError(f"mixed sign for {key}={value}: {out[value]} vs {sign}")
        out[value] = sign
    return out


def sroot_by_k(rows: list[dict[str, Any]]) -> dict[int, list[tuple[int, str]]]:
    out: defaultdict[int, list[tuple[int, str]]] = defaultdict(list)
    for row in rows:
        out[int(row["K"])].append((int(row["Sroot"]), str(row["sign"])))
    return dict(out)


def compare_gate(
    q: int,
    gate: int,
    b_family: dict[str, Any],
    k_family: dict[str, Any],
    s_family: dict[str, Any],
) -> Counter:
    stats: Counter = Counter()
    roots = sqrt_table(q)
    b_rows = row_signs(b_family["rows"], "B")
    k_rows = row_signs(k_family["rows"], "K")
    s_by_k = sroot_by_k(s_family["rows"])

    stats["B_rows"] = len(b_rows)
    stats["K_rows"] = len(k_rows)
    stats["Sroot_rows"] = sum(len(values) for values in s_by_k.values())

    for B, b_sign in sorted(b_rows.items()):
        stats["B_checked"] += 1
        K2 = b_to_k_square(B, q)
        if K2 is None:
            stats["B_degenerate"] += 1
            continue
        k_roots = roots[K2]
        stats[f"K_roots_{len(k_roots)}"] += 1
        present = [K for K in k_roots if K in k_rows]
        stats[f"K_present_{len(present)}"] += 1
        if len(present) != 1:
            continue
        K = present[0]
        k_sign = k_rows[K]
        if k_sign == b_sign:
            stats["B_to_K_sign_match"] += 1
        else:
            stats["B_to_K_sign_mismatch"] += 1

        s_rows = s_by_k.get(K, [])
        stats[f"Sroot_present_{len(s_rows)}"] += 1
        s_signs = {sign for _s, sign in s_rows}
        if len(s_signs) == 1 and next(iter(s_signs)) == b_sign:
            stats["B_to_Sroot_sheet_signs_match"] += 1
        elif s_rows:
            stats["B_to_Sroot_sheet_signs_mismatch"] += 1

        for Sroot, _sign in s_rows:
            if Sroot * Sroot % q != K:
                stats["Sroot_square_mismatch"] += 1
            else:
                stats["Sroot_square_match"] += 1

    stats[f"gate{gate}_rows"] = stats["B_rows"]
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--b-packet", type=Path, default=DEFAULT_B_PACKET)
    parser.add_argument("--ks-packet", type=Path, default=DEFAULT_KS_PACKET)
    args = parser.parse_args()

    b_packet = load_packet(args.b_packet)
    ks_packet = load_packet(args.ks_packet)
    b_fields = fixture_by_field(b_packet)
    ks_fields = fixture_by_field(ks_packet)
    fields = sorted(set(b_fields) & set(ks_fields))
    max_gate = min(int(b_packet["max_gate"]), int(ks_packet["max_gate"]))

    print("p27 B/K/Sroot fixture bridge probe")
    print("relation = K^2 - (B-2)^4/(8*B*(B+2)^2), Sroot^2=K")
    print(f"fields = {fields}")
    print(f"max_gate = {max_gate}")

    for q in fields:
        b_families = family_map(b_fields[q])
        ks_families = family_map(ks_fields[q])
        print(f"q={q}:")
        for gate in range(3, max_gate + 1):
            b_name = f"f{gate}_conditional"
            k_name = f"f{gate}_conditional_on_K"
            s_name = f"f{gate}_conditional_on_Sroot"
            stats = compare_gate(
                q,
                gate,
                b_families[b_name],
                ks_families[k_name],
                ks_families[s_name],
            )
            print_counter(f"  gate{gate}_bridge", stats)

    print("p27_b_ksroot_fixture_bridge_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Emit finite-field fixtures for the p27 K/Sroot Kummer sequence.

The K/Sroot lane has clean prefix descent but no source-density advantage:
Sroot separates the two K sheets while exactly doubling the K rows.  This
packet freezes the conditional guard-field rows for

    f3(K), f4(K), ... and f3(Sroot), f4(Sroot), ...

so the remaining CAS/expert task is normalized branch-class extraction, not
another bucket or coefficient scan.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from typing import Any, Optional

from p27_extension_prefix_count_probe import GF, find_irreducible
from p27_sroot_prefix_profile_probe import Bit, collect_groups, strict_normalize


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def sign_label(sign: int) -> str:
    return "plus" if sign == 1 else "minus"


def counter_json(stats: Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(stats.items(), key=lambda item: str(item[0]))}


def bit_for_group(values: list[tuple[Bit, ...]], index: int) -> Optional[int]:
    return strict_normalize(bits[index] for bits in values)


def legal_payload(coord: str, keys: list[int], F: GF) -> dict[str, Any]:
    rows: list[dict[str, int]] = []
    if coord == "Sroot":
        rows = [{"Sroot": int(s), "K": int(F.sqr(s))} for s in keys]
    else:
        rows = [{"K": int(k)} for k in keys]
    return {
        "name": f"legal_{coord}",
        "coordinate": coord,
        "meaning": f"legal selected-source {coord} values",
        "row_count": len(rows),
        "rows": rows,
    }


def conditional_payloads(
    coord: str,
    groups: defaultdict[int, list[tuple[Bit, ...]]],
    F: GF,
    max_gate: int,
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    active = set(groups)
    for index, gate in enumerate(range(3, max_gate + 1)):
        rows: list[dict[str, Any]] = []
        next_active: set[int] = set()
        stats: Counter = Counter()
        for key in sorted(active):
            bit = bit_for_group(groups[key], index)
            if bit in (-1, 1):
                if coord == "Sroot":
                    row: dict[str, Any] = {"Sroot": int(key), "K": int(F.sqr(key))}
                else:
                    row = {"K": int(key)}
                row["sign"] = sign_label(bit)
                rows.append(row)
                stats[sign_label(bit)] += 1
                if bit == 1:
                    next_active.add(key)
            elif bit == 0:
                row = {"Sroot" if coord == "Sroot" else "K": int(key), "sign": "mixed"}
                if coord == "Sroot":
                    row["K"] = int(F.sqr(key))
                rows.append(row)
                stats["mixed"] += 1
            else:
                row = {"Sroot" if coord == "Sroot" else "K": int(key), "sign": "missing"}
                if coord == "Sroot":
                    row["K"] = int(F.sqr(key))
                rows.append(row)
                stats["missing"] += 1

        payloads.append(
            {
                "name": f"f{gate}_conditional_on_{coord}",
                "gate": f"d{gate}",
                "coordinate": coord,
                "domain": f"legal {coord}" if gate == 3 else f"{coord} all-plus prefix through d{gate - 1}",
                "meaning": f"selected gate d{gate} character on the active {coord} domain",
                "row_count": len(rows),
                "plus_count": stats["plus"],
                "minus_count": stats["minus"],
                "mixed_count": stats["mixed"],
                "missing_count": stats["missing"],
                "rows": rows,
            }
        )
        active = next_active
    return payloads


def sheet_stats(sroot_keys: list[int], F: GF) -> dict[str, Any]:
    by_k: defaultdict[int, list[int]] = defaultdict(list)
    for s in sroot_keys:
        by_k[F.sqr(s)].append(s)
    hist = Counter(len(values) for values in by_k.values())
    return {
        "K_from_Sroot": len(by_k),
        "Sroot": len(sroot_keys),
        "Sroot_per_K_histogram": {str(key): int(value) for key, value in sorted(hist.items())},
    }


def field_payload(q: int, max_gate: int) -> dict[str, Any]:
    F = GF(q=q, n=1, modulus=find_irreducible(q, 1))
    groups, stats = collect_groups(F, max_gate)
    k_keys = sorted(groups["K"])
    s_keys = sorted(groups["Sroot"])
    return {
        "field": q,
        "base": {
            "legal_K": len(k_keys),
            "legal_Sroot": len(s_keys),
            "sheet_stats": sheet_stats(s_keys, F),
            "K_group_size_histogram": {
                key.removeprefix("K_group_size_"): value
                for key, value in sorted(stats.items())
                if str(key).startswith("K_group_size_")
            },
            "Sroot_group_size_histogram": {
                key.removeprefix("Sroot_group_size_"): value
                for key, value in sorted(stats.items())
                if str(key).startswith("Sroot_group_size_")
            },
        },
        "families": [
            legal_payload("K", k_keys, F),
            *conditional_payloads("K", groups["K"], F, max_gate),
            legal_payload("Sroot", s_keys, F),
            *conditional_payloads("Sroot", groups["Sroot"], F, max_gate),
        ],
        "source_stats": counter_json(stats),
    }


def packet_json(fields: list[int], max_gate: int) -> dict[str, Any]:
    return {
        "name": "p27_ksroot_kummer_fixture_packet",
        "date": "2026-06-22",
        "target_prime": "1000000000000000000000000103",
        "purpose": (
            "Compact guard-field fixtures for extracting and comparing the "
            "K/Sroot branch classes after K/Sroot bucket, prefix-density, "
            "quartic, and visible branch-divisor shortcuts were killed."
        ),
        "field_signature": {
            "q_mod_16": 7,
            "chi_minus_one": -1,
            "chi_two": 1,
        },
        "coordinates": {
            "K": "x([2]P) on E': V^2 = U^3 + 4U",
            "Sroot": "(U^2 - 4)/(2V)",
            "relation": "Sroot^2 = K",
        },
        "fields": fields,
        "max_gate": max_gate,
        "fixtures": [field_payload(q, max_gate) for q in fields],
        "cas_tasks": [
            {
                "priority": 10,
                "name": "Recover normalized Sroot branch class for f3",
                "compute": [
                    "branch divisor degree and support field degrees over P1_Sroot",
                    "normalization genus and component count",
                    "Sroot -> -Sroot decomposition and descent to K",
                    "whether the class preserves the rational K-square stratum",
                ],
                "promote_if": "stable low-genus/sourceable Sroot class that survives K quotient checks",
                "kill_if": "class only appears after forgetting K-square rationality or is high/generic",
            },
            {
                "priority": 20,
                "name": "Compare f4/f3 after f3 is named",
                "compute": [
                    "pullback/translate/coboundary/iterate relation between conditional classes",
                    "whether signed Sroot is essential or the relation descends to K",
                    "first falsifier showing f4 is a fresh independent half-cover",
                ],
                "promote_if": "one K/Sroot class or correspondence controls multiple selected gates",
                "kill_if": "successive classes are unrelated fresh Kummer covers",
            },
        ],
        "do_not_run": [
            "K/Sroot bucket production without a named class",
            "Sroot prefix-density GPU tests",
            "visible degree <=4 branch divisor restarts",
            "K-line even or reciprocal quartic subfamilies already killed",
        ],
        "acceptance": {
            "promote": "low-genus/sourceable/recurrent K/Sroot class preserving K-square rationality",
            "kill": "generic high-genus f3 plus fresh f4 half-cover or class that only works after forgetting K",
        },
        "sentinel": "p27_ksroot_kummer_fixture_packet_rows=1/1",
    }


def print_text(packet: dict[str, Any]) -> None:
    print("p27 K/Sroot Kummer fixture packet")
    print()
    print("Purpose:")
    print("  Freeze guard-field rows for conditional K and signed-Sroot classes")
    print("  so branch-class extraction can preserve the K-square stratum.")
    print()
    print("Guard fields:")
    for fixture in packet["fixtures"]:
        base = fixture["base"]
        print(
            f"  q={fixture['field']}: legal_K={base['legal_K']} "
            f"legal_Sroot={base['legal_Sroot']} "
            f"Sroot_per_K={base['sheet_stats']['Sroot_per_K_histogram']}"
        )
        for family in fixture["families"]:
            if not family["name"].startswith("f"):
                continue
            print(
                "    "
                f"{family['name']}: rows={family['row_count']} "
                f"plus={family['plus_count']} minus={family['minus_count']} "
                f"mixed={family['mixed_count']} missing={family['missing_count']}"
            )
    print()
    print("CAS task:")
    print("  1. Recover f3 over P1_Sroot and check descent/parity under Sroot -> -Sroot.")
    print("  2. Preserve the rational K-square stratum; do not accept a source that only")
    print("     appears after forgetting K.")
    print("  3. Compare f4/f3 only after f3 is named.")
    print("  4. Promote only a low-genus/sourceable/recurrent class controlling multiple gates.")
    print()
    print("Fixture JSON:")
    print("  research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json")
    print()
    print(packet["sentinel"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--max-gate", type=int, default=6)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    packet = packet_json(parse_ints(args.small_primes), args.max_gate)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print_text(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

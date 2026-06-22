#!/usr/bin/env python3
"""Verify a GPU-reported B-line monic quartic hit.

The GPU screen searches for quartics

    chi(B^4 + aB^3 + bB^2 + cB + d) = polarity * target_sign(B)

on frozen finite-field target rows.  This verifier reads the JSON target
packet and checks a proposed coefficient tuple exactly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_PACKET = (
    "research/p27/archive/fixtures/"
    "p27_b_line_quartic_targets_20260622.json"
)


def legendre(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def parse_coeffs(raw: str) -> tuple[int, int, int, int]:
    parts = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--coeffs must have four comma-separated integers")
    return tuple(parts)  # type: ignore[return-value]


def load_packet(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def target_entry(packet: dict[str, Any], field: int, family: str) -> dict[str, Any]:
    for target in packet["targets"]:
        if target["field"] == field and target["family"] == family:
            return target
    raise KeyError(f"target not found: field={field} family={family}")


def quartic_value(b_value: int, coeffs: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = coeffs
    B = b_value % p
    return (pow(B, 4, p) + a * pow(B, 3, p) + b * B * B + c * B + d) % p


def verify(
    target: dict[str, Any],
    coeffs: tuple[int, int, int, int],
    polarity: int,
) -> dict[str, int]:
    p = int(target["field"])
    stats = {
        "rows": 0,
        "matches": 0,
        "mismatches": 0,
        "zeros": 0,
        "plus_rows": 0,
        "minus_rows": 0,
    }
    for row in target["rows"]:
        stats["rows"] += 1
        target_sign = int(row["sign"])
        if target_sign == 1:
            stats["plus_rows"] += 1
        elif target_sign == -1:
            stats["minus_rows"] += 1
        chi = legendre(quartic_value(int(row["B"]), coeffs, p), p)
        desired = polarity * target_sign
        if chi == 0:
            stats["zeros"] += 1
            stats["mismatches"] += 1
        elif chi == desired:
            stats["matches"] += 1
        else:
            stats["mismatches"] += 1
    return stats


def print_targets(packet: dict[str, Any]) -> None:
    print("available_targets:")
    for target in packet["targets"]:
        print(
            "  "
            f"field={target['field']} family={target['family']} "
            f"rows={target['row_count']} plus={target['plus_count']} "
            f"minus={target['minus_count']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=DEFAULT_PACKET)
    parser.add_argument("--field", type=int)
    parser.add_argument("--family")
    parser.add_argument("--coeffs", type=parse_coeffs)
    parser.add_argument("--polarity", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--list-targets", action="store_true")
    args = parser.parse_args()

    packet = load_packet(args.packet)
    print("p27 B-line quartic verifier")
    print(f"packet = {args.packet}")
    if args.list_targets or args.coeffs is None:
        print_targets(packet)
    if args.coeffs is not None:
        if args.field is None or args.family is None:
            raise SystemExit("--field and --family are required with --coeffs")
        target = target_entry(packet, args.field, args.family)
        stats = verify(target, args.coeffs, args.polarity)
        print(
            "verify_result: "
            f"field={args.field} family={args.family} "
            f"coeffs={','.join(str(c % args.field) for c in args.coeffs)} "
            f"polarity={args.polarity}"
        )
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
        print(f"  pass = {int(stats['mismatches'] == 0 and stats['zeros'] == 0)}")
    print("p27_b_line_quartic_verify_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

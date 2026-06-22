#!/usr/bin/env python3
"""Export frozen B/K/lambda quartic target rows for the fast C chunk oracle."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import p27_b_line_quartic_verify as b_verify
import p27_dplus_rowbit_u_lowgenus_verify as u_verify
import p27_kline_quartic_verify as k_verify
import p27_lambda_lowgenus_verify as lambda_verify


COORDS = {
    "B": (b_verify.DEFAULT_PACKET, b_verify.load_packet, b_verify.target_entry, "B"),
    "K": (k_verify.DEFAULT_PACKET, k_verify.load_packet, k_verify.target_entry, "K"),
    "lambda": (
        lambda_verify.DEFAULT_PACKET,
        lambda_verify.load_packet,
        lambda_verify.target_entry,
        "lambda",
    ),
    "u": (u_verify.DEFAULT_PACKET, u_verify.load_packet, u_verify.target_entry, "u"),
}


def export_rows(target: dict[str, Any], coordinate_name: str) -> str:
    q = int(target["field"])
    rows = target["rows"]
    out = [
        "# p27 quartic target rows",
        f"# coordinate {coordinate_name}",
        f"# field {q}",
        f"# family {target['family']}",
        f"# rows {len(rows)}",
        f"{q} {len(rows)}",
    ]
    key = coordinate_name
    for row in rows:
        out.append(f"{int(row[key]) % q} {int(row['sign'])}")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coordinate", choices=sorted(COORDS), required=True)
    parser.add_argument("--packet")
    parser.add_argument("--field", type=int, required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    default_packet, loader, target_lookup, row_key = COORDS[args.coordinate]
    packet = loader(args.packet or default_packet)
    target = target_lookup(packet, args.field, args.family)
    text = export_rows(target, row_key)
    if args.out:
        Path(args.out).write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

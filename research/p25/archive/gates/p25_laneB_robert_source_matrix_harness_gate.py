#!/usr/bin/env python3
"""Source-matrix intake harness for Robert/Siegel-style p25 bridge candidates.

The bridge candidate harness accepts a raw vector indexed by the primitive
source exponent e in C_12675.  A Robert elliptic-unit or mixed Siegel-unit
probe is more likely to emit a rectangular table indexed by the local source
logs

    (right_log mod 75, c_log mod 169).

This small wrapper converts that source matrix to the raw exponent order and
then reuses the producer-facing bridge candidate profile.  It is an intake
artifact for the next arithmetic producer attempt, not a producer itself.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


def crt_source_to_raw(right_log: int, c_log: int) -> int:
    """Return e with e = right_log mod 75 and e = c_log mod 169."""

    inverse_75 = pow(RIGHT_ORDER, -1, C_ORDER)
    lift = ((c_log - right_log) * inverse_75) % C_ORDER
    return (right_log + RIGHT_ORDER * lift) % RAW_ORDER


def source_matrix_from_raw(raw: list[int]) -> list[int]:
    matrix = [0] * RAW_ORDER
    for e_value, value in enumerate(raw):
        right_log = e_value % RIGHT_ORDER
        c_log = e_value % C_ORDER
        matrix[right_log * C_ORDER + c_log] = value
    return matrix


def raw_from_source_matrix(matrix: list[int]) -> list[int]:
    raw = [0] * RAW_ORDER
    for right_log in range(RIGHT_ORDER):
        for c_log in range(C_ORDER):
            raw[crt_source_to_raw(right_log, c_log)] = matrix[right_log * C_ORDER + c_log]
    return raw


def parse_source_matrix(path: Path) -> list[int]:
    values = [int(token) for token in re.findall(r"-?\d+", path.read_text())]
    if len(values) != RAW_ORDER:
        raise ValueError(f"{path} contains {len(values)} integers, expected {RAW_ORDER}")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a p25 square-axis bridge candidate in C_75 x C_169 source-matrix order."
    )
    parser.add_argument(
        "--source-matrix",
        type=Path,
        help="optional row-major C_75 x C_169 integer table to check",
    )
    args = parser.parse_args()

    print("p25 Lane B Robert/source-matrix bridge intake harness")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} raw_order={RAW_ORDER} "
        "source_order=row_major_right_then_c"
    )
    target = target_raw_bridge()

    if args.source_matrix is not None:
        raw = raw_from_source_matrix(parse_source_matrix(args.source_matrix))
        profile = profile_candidate(str(args.source_matrix), raw, target)
        print("mode=source_matrix_candidate")
        print(f"candidate_profile={profile}")
        print("candidate_contract")
        print("  pass requires the converted raw vector to satisfy the bridge producer contract")
        print(f"robert_source_matrix_harness_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_source_matrix_harness_candidate")
        return 0 if profile.ok else 1

    target_matrix = source_matrix_from_raw(target)
    roundtrip_raw = raw_from_source_matrix(target_matrix)
    profile = profile_candidate("target_source_matrix_roundtrip", roundtrip_raw, target)
    active_entries = [
        (right_log, c_log, target_matrix[right_log * C_ORDER + c_log])
        for right_log in range(RIGHT_ORDER)
        for c_log in range(C_ORDER)
        if target_matrix[right_log * C_ORDER + c_log]
    ]
    right_support = sorted({right_log for right_log, _c_log, _value in active_entries})
    c_support = sorted({c_log for _right_log, c_log, _value in active_entries})
    row_ok = (
        roundtrip_raw == target
        and profile.ok
        and len(active_entries) == 150
        and len(right_support) == RIGHT_ORDER
        and len(c_support) == 6
    )

    print(
        "source_matrix_roundtrip: "
        f"active_entries={len(active_entries)}/150 "
        f"right_support={len(right_support)}/{RIGHT_ORDER} "
        f"c_support={len(c_support)}/6 "
        f"profile_ok={int(profile.ok)} "
        f"ok={int(row_ok)}"
    )
    print("active_c_values")
    print(f"  {c_support}")
    print("intake_law")
    print("  source_matrix[right,c] is converted by CRT to raw exponent e")
    print("  e = right mod 75 and e = c mod 169")
    print("  Robert/Siegel finite tables can be checked without hand raw-order conversion")
    print(f"robert_source_matrix_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  source_matrix_roundtrip_preserves_the_exact_raw_bridge_contract=1")
    print("  next_robert_or_modular_unit_probe_can_emit_C75_by_C169_table=1")
    print("conclusion=reported_p25_laneB_robert_source_matrix_harness_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

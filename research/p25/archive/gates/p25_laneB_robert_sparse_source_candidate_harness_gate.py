#!/usr/bin/env python3
"""Sparse source-coordinate intake for Robert/Siegel bridge candidates.

The source-matrix harness accepts a full row-major `C_75 x C_169` table.  A
lit-search hit or hand calculation is more likely to emit only the nonzero
divisor terms

    right_log  c_log  coefficient

in the same source coordinates.  This wrapper coalesces such triples, converts
them by CRT into raw `C_12675` order, and reuses the bridge candidate harness.
It is an intake/falsifier artifact, not a producer.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_robert_source_matrix_harness_gate import crt_source_to_raw
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    profile_candidate,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


SparseEntry = tuple[int, int, int]


@dataclass(frozen=True)
class SparseSourceProfile:
    name: str
    input_terms: int
    active_source_terms: int
    duplicate_source_terms: int
    raw_support: int
    bridge_profile: CandidateProfile
    ok: bool


def parse_sparse_source(path: Path) -> tuple[SparseEntry, ...]:
    entries: list[SparseEntry] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        clean = line.split("#", 1)[0]
        for char in ",()[]":
            clean = clean.replace(char, " ")
        if not clean.strip():
            continue
        parts = clean.split()
        if len(parts) != 3:
            raise ValueError(
                f"{path}:{line_number} expected three integers: right c coeff"
            )
        entries.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return tuple(entries)


def target_sparse_entries() -> tuple[SparseEntry, ...]:
    return tuple(
        (right_log, c_log, coefficient)
        for (right_log, c_log), coefficient in raw_source_mask().items()
    )


def sparse_source_to_raw(entries: tuple[SparseEntry, ...]) -> tuple[list[int], int, int]:
    source_terms: dict[tuple[int, int], int] = {}
    duplicate_terms = 0
    for right_log, c_log, coefficient in entries:
        coord = (right_log % RIGHT_ORDER, c_log % C_ORDER)
        duplicate_terms += int(coord in source_terms)
        source_terms[coord] = source_terms.get(coord, 0) + coefficient

    raw = [0] * RAW_ORDER
    active_terms = 0
    for (right_log, c_log), coefficient in source_terms.items():
        if coefficient == 0:
            continue
        active_terms += 1
        raw[crt_source_to_raw(right_log, c_log)] = coefficient
    return raw, active_terms, duplicate_terms


def profile_sparse_source(name: str, entries: tuple[SparseEntry, ...]) -> SparseSourceProfile:
    raw, active_terms, duplicate_terms = sparse_source_to_raw(entries)
    bridge_profile = profile_candidate(name, raw, target_raw_bridge())
    raw_support = sum(1 for value in raw if value)
    ok = bridge_profile.ok and active_terms == 150 and raw_support == 150
    return SparseSourceProfile(
        name=name,
        input_terms=len(entries),
        active_source_terms=active_terms,
        duplicate_source_terms=duplicate_terms,
        raw_support=raw_support,
        bridge_profile=bridge_profile,
        ok=ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit sparse C_75 x C_169 source-coordinate triples against the "
            "p25 Robert/Siegel bridge contract."
        )
    )
    parser.add_argument(
        "--sparse-source",
        type=Path,
        help="optional text file of triples: right_log c_log coefficient",
    )
    args = parser.parse_args()

    print("p25 Lane B Robert sparse-source bridge intake harness")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} raw_order={RAW_ORDER} "
        "format='right_log c_log coefficient'"
    )

    if args.sparse_source is not None:
        profile = profile_sparse_source(
            str(args.sparse_source),
            parse_sparse_source(args.sparse_source),
        )
        print("mode=sparse_source_candidate")
        print(f"sparse_source_profile={profile}")
        print("candidate_contract")
        print("  pass requires the coalesced sparse source vector to satisfy the bridge producer contract")
        print("  source coordinates are reduced modulo C_75 x C_169 before CRT conversion")
        print(f"robert_sparse_source_candidate_harness_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_robert_sparse_source_candidate_harness_candidate")
        return 0 if profile.ok else 1

    target_profile = profile_sparse_source(
        "target_sparse_source_roundtrip",
        target_sparse_entries(),
    )
    row_ok = (
        target_profile.ok
        and target_profile.input_terms == 150
        and target_profile.active_source_terms == 150
        and target_profile.duplicate_source_terms == 0
    )
    print(f"target_sparse_source_profile={target_profile}")
    print("intake_law")
    print("  sparse triples are coalesced in C_75 x C_169 source coordinates")
    print("  coalesced triples are converted by CRT to raw exponent order C_12675")
    print("  Robert/Siegel divisor quotients can be tested without full matrix expansion")
    print(f"robert_sparse_source_candidate_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  target_sparse_source_roundtrip_preserves_the_exact_bridge_contract=1")
    print("  next_lit_search_hit_can_emit_only_nonzero_source_triples=1")
    print("conclusion=reported_p25_laneB_robert_sparse_source_candidate_harness_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Sign-level Hilbert-90 corner to sparse-source bridge harness.

The fast sign-candidate harness checks the two-sign finite target.  This
stricter wrapper expands a valid `eps,a` pair through the quotient corner
chain, applies the Hilbert-90 first boundary and inversion boundary, lifts the
resulting signed S-layer bridge through the 25-point raw K trace, and reuses
the Robert sparse-source bridge harness.

This gives a compact path:

    eps,a -> source-row triangle -> quotient bridge -> C_75 x C_169 triples
          -> existing raw bridge contract.

It is still an intake/falsifier artifact, not an arithmetic producer proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p25_laneB_robert_sparse_source_candidate_harness_gate import (
    SparseEntry,
    SparseSourceProfile,
    profile_sparse_source,
    target_sparse_entries,
)
from p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness import (
    CornerSignCandidateProfile,
    profile_sign_candidate,
)
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    boundary,
    inversion_boundary,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER, RIGHT_ORDER
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class CornerSignSparseSourceProfile:
    name: str
    sign_profile: CornerSignCandidateProfile
    chain_q_items: tuple[tuple[int, int], ...]
    first_boundary_q_items: tuple[tuple[int, int], ...]
    bridge_q_items: tuple[tuple[int, int], ...]
    sparse_entries: tuple[SparseEntry, ...]
    sparse_entry_count: int
    sparse_entries_equal_target: bool
    sparse_source_profile: SparseSourceProfile | None
    ok: bool


def quotient_q_from_source(row: int, c_log: int) -> int:
    inverse_3 = pow(3, -1, C_ORDER)
    lift = ((c_log - row) * inverse_3) % C_ORDER
    return (row + 3 * lift) % QUOTIENT_ORDER


def source_entries_from_quotient_bridge(
    quotient_bridge: dict[int, int],
) -> tuple[SparseEntry, ...]:
    entries: list[SparseEntry] = []
    for q_value, coefficient in sorted(quotient_bridge.items()):
        for layer in range(25):
            raw_e = q_value + QUOTIENT_ORDER * layer
            entries.append((raw_e % RIGHT_ORDER, raw_e % C_ORDER, coefficient))
    return tuple(sorted(entries))


def sign_sparse_source_profile(
    name: str,
    eps: int,
    branch: int,
) -> CornerSignSparseSourceProfile:
    sign_profile = profile_sign_candidate(name, eps, branch)
    if not sign_profile.ok or sign_profile.points_by_source_row is None:
        return CornerSignSparseSourceProfile(
            name=name,
            sign_profile=sign_profile,
            chain_q_items=(),
            first_boundary_q_items=(),
            bridge_q_items=(),
            sparse_entries=(),
            sparse_entry_count=0,
            sparse_entries_equal_target=False,
            sparse_source_profile=None,
            ok=False,
        )

    chain: dict[int, int] = {}
    for row, (low, fiber) in enumerate(sign_profile.points_by_source_row):
        c_log = (low + 13 * fiber) % C_ORDER
        chain[quotient_q_from_source(row, c_log)] = branch
    first = boundary(chain, sign_profile.recorded_direction_q)
    bridge = inversion_boundary(first)
    sparse_entries = source_entries_from_quotient_bridge(bridge)
    sparse_profile = profile_sparse_source(name, sparse_entries)
    sparse_equal_target = sparse_entries == target_sparse_entries()
    ok = (
        sign_profile.ok
        and len(chain) == 3
        and sign_profile.recorded_direction_q is not None
        and len(first) == 4
        and len(bridge) == 6
        and len(sparse_entries) == 150
        and sparse_equal_target
        and sparse_profile.ok
    )
    return CornerSignSparseSourceProfile(
        name=name,
        sign_profile=sign_profile,
        chain_q_items=tuple(sorted(chain.items())),
        first_boundary_q_items=tuple(sorted(first.items())),
        bridge_q_items=tuple(sorted(bridge.items())),
        sparse_entries=sparse_entries,
        sparse_entry_count=len(sparse_entries),
        sparse_entries_equal_target=sparse_equal_target,
        sparse_source_profile=sparse_profile,
        ok=ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Expand a two-sign Hilbert-90 corner into sparse source triples."
    )
    parser.add_argument("--eps", type=int, help="primitive D-unit sign, +1 or -1")
    parser.add_argument("--branch", type=int, help="branch coefficient, +1 or -1")
    args = parser.parse_args()

    print("p25 Lane B Hilbert-90 corner sign-to-sparse-source harness")
    print("format='eps branch' with eps,branch in {+1,-1}")

    if args.eps is not None or args.branch is not None:
        if args.eps is None or args.branch is None:
            raise SystemExit("--eps and --branch must be supplied together")
        profile = sign_sparse_source_profile("sign_sparse_source_candidate", args.eps, args.branch)
        print("mode=single_sign_sparse_source_candidate")
        print(f"corner_sign_sparse_source_profile={profile}")
        print("candidate_contract")
        print("  signs expand through quotient boundary and inversion boundary")
        print("  quotient bridge expands through the 25-point K trace to sparse source triples")
        print("  sparse triples must pass the existing Robert sparse-source bridge harness")
        print(f"square_axis_bridge_hilbert90_corner_sign_sparse_source_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_candidate")
        return 0 if profile.ok else 1

    profiles = tuple(
        sign_sparse_source_profile(f"target_eps_{eps}_branch_{branch}", eps, branch)
        for eps in (-1, 1)
        for branch in (-1, 1)
    )
    row_ok = (
        all(profile.ok for profile in profiles)
        and tuple(profile.sparse_entry_count for profile in profiles) == (150, 150, 150, 150)
        and all(profile.sparse_entries_equal_target for profile in profiles)
        and tuple(len(profile.first_boundary_q_items) for profile in profiles) == (4, 4, 4, 4)
        and tuple(len(profile.bridge_q_items) for profile in profiles) == (6, 6, 6, 6)
    )
    print(f"target_sign_sparse_source_profiles={profiles}")
    print("intake_law")
    print("  every valid sign pair expands to the exact target sparse source bridge")
    print("  quotient support ladder is 3 -> 4 -> 6 before K-trace expansion")
    print("  raw sparse source support is 150 and passes the existing bridge contract")
    print(f"square_axis_bridge_hilbert90_corner_sign_sparse_source_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  two-sign theorem hits can be promoted directly to sparse source triples")
    print("  primitive C169 producer debt remains; this is an intake check only")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

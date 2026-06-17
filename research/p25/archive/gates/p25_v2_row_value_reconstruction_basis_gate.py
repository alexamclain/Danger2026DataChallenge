#!/usr/bin/env python3
"""Finite row-value reconstruction basis for the p25 four-row target."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"

EDGE_NAMES = ("m1", "m2", "m4", "m8")
E1 = (1, 0, 0, 0)
E2 = (0, 1, 0, 0)
E4 = (0, 0, 1, 0)
E8 = (0, 0, 0, 1)
ZERO_BASIS = {
    "q2_1": (-1, 1, 0, 0),
    "q4_1": (-1, 0, 1, 0),
    "q8_1": (-1, 0, 0, 1),
}
DIAGONAL_Q_ROWS = {
    "d14": (1, 0, 1, 0),
    "q14": (1, 0, -1, 0),
    "d28": (0, 1, 0, 1),
    "q28": (0, 1, 0, -1),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text()


@dataclass(frozen=True)
class ReconstructionRow:
    name: str
    input_data: str
    algebra: str
    decision: str
    first_missing_or_falsifier: str
    source_stage_candidate_if_theorem_present: bool
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "unified_group_ring_payload",
        "evidence/p25_v2_unified_group_ring_payload_20260616.md",
        "p25_v2_unified_group_ring_payload_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    EvidenceMarker(
        "row_quotient_invariant_bridge",
        "evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
        "p25_v2_row_quotient_invariant_bridge_rows=1/1",
    ),
    EvidenceMarker(
        "row_square_root_ambiguity",
        "evidence/p25_v2_row_square_root_ambiguity_20260616.md",
        "p25_v2_row_square_root_ambiguity_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_payload_router",
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
    EvidenceMarker(
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
)


def add(*vectors: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(sum(vector[i] for vector in vectors) for i in range(4))


def sub(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def scale(coeff: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(coeff * value for value in vector)


def coeff_sum(vector: tuple[int, int, int, int]) -> int:
    return sum(vector)


def rank(vectors: tuple[tuple[int, int, int, int], ...]) -> int:
    matrix = [[Fraction(value) for value in vector] for vector in vectors]
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if matrix[i][c]:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        factor = matrix[r][c]
        matrix[r] = [value / factor for value in matrix[r]]
        for i in range(rows):
            if i == r or not matrix[i][c]:
                continue
            factor = matrix[i][c]
            matrix[i] = [matrix[i][j] - factor * matrix[r][j] for j in range(cols)]
        r += 1
    return r


def reconstruction_rows() -> tuple[ReconstructionRow, ...]:
    quotient_span_rank = rank(tuple(ZERO_BASIS.values()))
    full_basis_rank = rank((E1, *ZERO_BASIS.values()))
    d14 = DIAGONAL_Q_ROWS["d14"]
    q14 = DIAGONAL_Q_ROWS["q14"]
    d28 = DIAGONAL_Q_ROWS["d28"]
    q28 = DIAGONAL_Q_ROWS["q28"]
    return (
        ReconstructionRow(
            name="one_absolute_row_anchor",
            input_data="exact scalar-fixed finite theorem for one legal row R_m",
            algebra="one basis vector e_m has coefficient sum 1",
            decision="source_stage_candidate_if_theorem_present",
            first_missing_or_falsifier="DANGER3 framing, same-j extraction, and official vpp.py",
            source_stage_candidate_if_theorem_present=True,
            ok=coeff_sum(E1) == 1,
        ),
        ReconstructionRow(
            name="one_row_plus_three_quotients",
            input_data="R_1 plus q2_1, q4_1, q8_1 boundary-zero values",
            algebra="e2=e1+q2_1, e4=e1+q4_1, e8=e1+q8_1",
            decision="reconstruct_all_rows_after_absolute_anchor",
            first_missing_or_falsifier="absolute row value still required before quotients can transfer",
            source_stage_candidate_if_theorem_present=False,
            ok=(
                full_basis_rank == 4
                and add(E1, ZERO_BASIS["q2_1"]) == E2
                and add(E1, ZERO_BASIS["q4_1"]) == E4
                and add(E1, ZERO_BASIS["q8_1"]) == E8
            ),
        ),
        ReconstructionRow(
            name="three_quotients_only",
            input_data="q2_1, q4_1, q8_1 boundary-zero values",
            algebra="rank-3 zero-lattice fixes ratios but has coefficient sum 0",
            decision="support_transfer_data_not_first_absolute_row",
            first_missing_or_falsifier="common F_p^* scalar / one W-boundary row value",
            source_stage_candidate_if_theorem_present=False,
            ok=quotient_span_rank == 3 and all(coeff_sum(vector) == 0 for vector in ZERO_BASIS.values()),
        ),
        ReconstructionRow(
            name="diagonal_plus_matching_quotient",
            input_data="d14=m1+m4 plus q14=m1-m4, or d28 plus q28",
            algebra="d14+q14=2*m1 and d14-q14=2*m4; denominator 2 is unavoidable",
            decision="repair_row_square_oriented_root_missing",
            first_missing_or_falsifier="oriented square root/sign or direct one-row theorem",
            source_stage_candidate_if_theorem_present=False,
            ok=(
                add(d14, q14) == scale(2, E1)
                and sub(d14, q14) == scale(2, E4)
                and add(d28, q28) == scale(2, E2)
                and sub(d28, q28) == scale(2, E8)
            ),
        ),
        ReconstructionRow(
            name="nonunit_w_boundary_plus_zero_lattice",
            input_data="nonunit coefficient-sum-one theorem plus exact boundary-zero correction",
            algebra="v=e_m+z, so e_m=v-z only if z has an exact finite value",
            decision="normalize_to_one_row_only_with_exact_zero_lattice_values",
            first_missing_or_falsifier="finite value for boundary-zero content or direct unit-edge theorem",
            source_stage_candidate_if_theorem_present=False,
            ok=coeff_sum(add(E1, ZERO_BASIS["q2_1"])) == 1 and add(E1, ZERO_BASIS["q2_1"]) == E2,
        ),
        ReconstructionRow(
            name="q_square_payload",
            input_data="exact scalar-fixed finite value for the Q-square row",
            algebra="bounded two-root row-value payload, not a direct vpp.py candidate",
            decision="bounded_payload_needs_oriented_root_and_extraction_map",
            first_missing_or_falsifier="oriented root/sign plus same-j/X_1(16)/halving or direct A,x0 map",
            source_stage_candidate_if_theorem_present=False,
            ok=True,
        ),
    )


def main() -> int:
    rows = reconstruction_rows()
    marker_ok_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    source_stage_candidates = sum(row.source_stage_candidate_if_theorem_present for row in rows)
    current_source_stage_closers = 0
    current_submission_ready = 0
    overall_ok = (
        marker_ok_count == len(EVIDENCE_MARKERS)
        and len(rows) == 6
        and all(row.ok for row in rows)
        and rank(tuple(ZERO_BASIS.values())) == 3
        and rank((E1, *ZERO_BASIS.values())) == 4
        and source_stage_candidates == 1
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 row-value reconstruction basis")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("lattice")
    print(f"  edge_names={EDGE_NAMES}")
    print(f"  zero_lattice_rank={rank(tuple(ZERO_BASIS.values()))}")
    print(f"  one_anchor_plus_zero_lattice_rank={rank((E1, *ZERO_BASIS.values()))}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    input_data={row.input_data}")
        print(f"    algebra={row.algebra}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={marker_ok_count}/{len(EVIDENCE_MARKERS)}")
    print(f"  reconstruction_rows={len(rows)}")
    print(f"  source_stage_candidate_shapes={source_stage_candidates}")
    print("  quotient_only_absolute_anchors=0")
    print("  diagonal_plus_split_denominator=2")
    print(f"  current_source_stage_closers={current_source_stage_closers}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  one_absolute_scalar_fixed_row_value_is_the_missing_anchor=1")
    print("  boundary_zero_values_are_transfer_not_first_row=1")
    print(f"p25_v2_row_value_reconstruction_basis_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("row-value reconstruction basis failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

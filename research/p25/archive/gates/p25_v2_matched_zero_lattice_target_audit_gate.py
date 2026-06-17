#!/usr/bin/env python3
"""Audit the exact zero-lattice targets needed by matched-affine packets."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_matched_zero_lattice_target_audit_rows=1/1"


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


@dataclass(frozen=True)
class ZeroTarget:
    name: str
    aggregate_vector: tuple[int, int, int, int]
    target_index: int
    zero_vector: tuple[int, int, int, int]
    source_target: str
    decision: str
    first_missing_or_falsifier: str

    @property
    def coefficient_sum(self) -> int:
        return sum(self.aggregate_vector)


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_candidate_sweep",
        "evidence/p25_v2_zero_lattice_candidate_sweep_20260617.md",
        "p25_v2_zero_lattice_candidate_sweep_rows=1/1",
    ),
    EvidenceMarker(
        "row_quotient_invariant_bridge",
        "evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
        "p25_v2_row_quotient_invariant_bridge_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_closure_packet",
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_burden_audit",
        "evidence/p25_v2_matched_quotient_burden_audit_20260617.md",
        "p25_v2_matched_quotient_burden_audit_rows=1/1",
    ),
)


def unit(index: int) -> tuple[int, int, int, int]:
    return tuple(1 if i == index else 0 for i in range(4))


def scale(c: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(c * value for value in vector)


def sub(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def matched_zero(aggregate: tuple[int, int, int, int], target_index: int) -> tuple[int, int, int, int]:
    return sub(aggregate, scale(sum(aggregate), unit(target_index)))


def zero_coordinates(vector: tuple[int, int, int, int]) -> tuple[int, int, int] | None:
    if sum(vector) != 0:
        return None
    a, b, c = vector[1], vector[2], vector[3]
    return (a, b, c) if (-a - b - c, a, b, c) == vector else None


def rank(vectors: tuple[tuple[int, ...], ...]) -> int:
    matrix = [[Fraction(value) for value in vector] for vector in vectors if any(vector)]
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if matrix[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        pivot_value = matrix[r][c]
        matrix[r] = [value / pivot_value for value in matrix[r]]
        for i in range(rows):
            if i == r or matrix[i][c] == 0:
                continue
            factor = matrix[i][c]
            matrix[i] = [
                matrix[i][j] - factor * matrix[r][j]
                for j in range(cols)
            ]
        r += 1
        if r == rows:
            break
    return r


def targets() -> tuple[ZeroTarget, ...]:
    return (
        ZeroTarget(
            name="unit_sum_inverse_q2_1",
            aggregate_vector=(2, -1, 0, 0),
            target_index=0,
            zero_vector=(1, -1, 0, 0),
            source_target="exact inverse of q2_1, equivalently R1/R2",
            decision="needed_for_unit_sum_matched_packet",
            first_missing_or_falsifier="quotient relation or zero boundary without scalar-fixed finite value",
        ),
        ZeroTarget(
            name="unit_power_q2_1",
            aggregate_vector=(2, 1, 0, 0),
            target_index=0,
            zero_vector=(-1, 1, 0, 0),
            source_target="exact q2_1, equivalently R2/R1",
            decision="needed_for_unit_power_matched_packet",
            first_missing_or_falsifier="quotient relation or zero boundary without scalar-fixed finite value",
        ),
        ZeroTarget(
            name="full_zero_basis_product",
            aggregate_vector=(2, 1, 1, 1),
            target_index=0,
            zero_vector=(-3, 1, 1, 1),
            source_target="exact q2_1*q4_1*q8_1",
            decision="needed_for_full_zero_basis_matched_packet",
            first_missing_or_falsifier="individual quotient vocabulary without exact product value theorem",
        ),
    )


def target_ok(target: ZeroTarget) -> bool:
    z = matched_zero(target.aggregate_vector, target.target_index)
    coeff_sum = target.coefficient_sum
    return (
        z == target.zero_vector
        and zero_coordinates(z) is not None
        and gcd(coeff_sum, PM1) == 1
        and sub(target.aggregate_vector, z) == scale(coeff_sum, unit(target.target_index))
    )


def main() -> int:
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    rows = targets()
    coords = tuple(zero_coordinates(row.zero_vector) for row in rows)
    coordinate_rank = rank(tuple(coord for coord in coords if coord is not None))
    unique_zero_lines = {
        coord if coord >= tuple(-value for value in coord) else tuple(-value for value in coord)
        for coord in coords
        if coord is not None
    }
    scalar_fixed_zero_values_in_hand = 0
    matched_zero_source_theorems_in_hand = 0
    current_matched_source_packets = 0
    current_source_stage_closers = 0
    row_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and len(rows) == 3
        and all(target_ok(row) for row in rows)
        and coords == ((-1, 0, 0), (1, 0, 0), (1, 1, 1))
        and coordinate_rank == 2
        and len(unique_zero_lines) == 2
        and scalar_fixed_zero_values_in_hand == 0
        and matched_zero_source_theorems_in_hand == 0
        and current_matched_source_packets == 0
        and current_source_stage_closers == 0
    )

    print("p25 v2 matched zero-lattice target audit")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("targets")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} ok={int(target_ok(row))}")
        print(f"    aggregate_vector={row.aggregate_vector}")
        print(f"    coefficient_sum={row.coefficient_sum}")
        print(f"    matched_zero_vector={row.zero_vector}")
        print(f"    zero_coordinates={zero_coordinates(row.zero_vector)}")
        print(f"    source_target={row.source_target}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"matched_zero_targets={len(rows)}")
    print(f"zero_coordinate_rank={coordinate_rank}")
    print(f"unique_zero_lines_up_to_sign={len(unique_zero_lines)}")
    print(f"scalar_fixed_zero_values_in_hand={scalar_fixed_zero_values_in_hand}")
    print(f"matched_zero_source_theorems_in_hand={matched_zero_source_theorems_in_hand}")
    print(f"current_matched_source_packets={current_matched_source_packets}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print("interpretation")
    print("  matched_affine_route_needs_specific_zero_values_not_generic_quotient_vocab=1")
    print("  required_zero_targets_span_rank_two_not_full_rank_three=1")
    print("  zero_lattice_targets_are_support_not_first_anchor=1")
    print(MARKER if row_ok else "p25_v2_matched_zero_lattice_target_audit_rows=0/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

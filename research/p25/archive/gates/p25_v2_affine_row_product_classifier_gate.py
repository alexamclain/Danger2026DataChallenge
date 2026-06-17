#!/usr/bin/env python3
"""Classify affine products of the four p25 legal rows."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
ZERO_BASIS = {
    "q2_1": (-1, 1, 0, 0),
    "q4_1": (-1, 0, 1, 0),
    "q8_1": (-1, 0, 0, 1),
}


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
class AffineRow:
    name: str
    vector: tuple[int, int, int, int]
    required_extra: str
    decision: str
    first_falsifier: str
    ok: bool

    @property
    def coeff_sum(self) -> int:
        return sum(self.vector)

    @property
    def scalar_gcd(self) -> int:
        return gcd(self.coeff_sum, PM1)


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "row_value_reconstruction_basis",
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    EvidenceMarker(
        "common_scalar_anchor_filter",
        "evidence/p25_v2_common_scalar_anchor_filter_20260617.md",
        "p25_v2_common_scalar_anchor_filter_rows=1/1",
    ),
    EvidenceMarker(
        "basis_sensitive_anchor_sieve",
        "evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md",
        "p25_v2_basis_sensitive_anchor_sieve_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "drew_kernel_review_packet",
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
)


def sub(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def scale(c: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(c * value for value in vector)


def zero_lattice_coordinates(vector: tuple[int, int, int, int]) -> tuple[int, int, int] | None:
    if sum(vector) != 0:
        return None
    # vector = a*q2_1 + b*q4_1 + c*q8_1 = (-a-b-c, a, b, c)
    a, b, c = vector[1], vector[2], vector[3]
    if (-a - b - c, a, b, c) != vector:
        return None
    return (a, b, c)


def can_reduce_to_row_power(
    vector: tuple[int, int, int, int],
    row_index: int,
) -> tuple[bool, tuple[int, int, int] | None]:
    d = sum(vector)
    residual = sub(vector, scale(d, tuple(1 if i == row_index else 0 for i in range(4))))
    coords = zero_lattice_coordinates(residual)
    return coords is not None, coords


def rows() -> tuple[AffineRow, ...]:
    return (
        AffineRow(
            name="direct_unit_row",
            vector=(1, 0, 0, 0),
            required_extra="arithmetic source theorem and extraction ladder",
            decision="current_kernel_front_door",
            first_falsifier="source legality, boundary-only, or value up to scalar",
            ok=True,
        ),
        AffineRow(
            name="row_labeled_unit_power",
            vector=(75, 0, 0, 0),
            required_extra="row label, exact finite value, source theorem, boundary or period bridge",
            decision="inverse_power_then_current_kernel",
            first_falsifier="rowless power or exact-P 75-atom vocabulary",
            ok=gcd(75, PM1) == 1,
        ),
        AffineRow(
            name="unit_sum_nonedge_without_quotients",
            vector=(2, -1, 0, 0),
            required_extra="exact boundary-zero value for q2_1 before row recovery",
            decision="repair_zero_lattice_value_missing",
            first_falsifier="coefficient sum 1 presented as one legal row",
            ok=can_reduce_to_row_power((2, -1, 0, 0), 0) == (True, (-1, 0, 0)),
        ),
        AffineRow(
            name="unit_sum_nonedge_with_matched_zero_lattice_value",
            vector=(2, -1, 0, 0),
            required_extra="exact matched value for -q2_1; then recover R_1 directly",
            decision="normalize_to_current_kernel_if_matched_quotient_present",
            first_falsifier="aggregate value without the exact matched quotient value",
            ok=can_reduce_to_row_power((2, -1, 0, 0), 0) == (True, (-1, 0, 0)),
        ),
        AffineRow(
            name="unit_power_nonedge_with_matched_zero_lattice_value",
            vector=(2, 1, 0, 0),
            required_extra="exact matched value for q2_1; then recover R_1^3 and invert exponent 3",
            decision="normalize_to_current_kernel_if_matched_quotient_present",
            first_falsifier="aggregate value without the exact matched quotient value",
            ok=can_reduce_to_row_power((2, 1, 0, 0), 0) == (True, (1, 0, 0))
            and gcd(3, PM1) == 1,
        ),
        AffineRow(
            name="zero_lattice_quotient",
            vector=(-1, 1, 0, 0),
            required_extra="one absolute row anchor already known",
            decision="transfer_only_never_first_anchor",
            first_falsifier="quotient value presented as absolute W-boundary row",
            ok=zero_lattice_coordinates((-1, 1, 0, 0)) == (1, 0, 0),
        ),
        AffineRow(
            name="nonunit_pair_sum",
            vector=(1, 1, 0, 0),
            required_extra="oriented square root/sign even if quotient values are known",
            decision="root_debt_repair",
            first_falsifier="two-edge product treated as scalar-fixed row",
            ok=can_reduce_to_row_power((1, 1, 0, 0), 0) == (True, (1, 0, 0))
            and gcd(2, PM1) == 2,
        ),
        AffineRow(
            name="all_four_product",
            vector=(1, 1, 1, 1),
            required_extra="fourth-root/scalar and row selector",
            decision="root_and_selector_repair",
            first_falsifier="all-four product treated as a legal row theorem",
            ok=can_reduce_to_row_power((1, 1, 1, 1), 0) == (True, (1, 1, 1))
            and gcd(4, PM1) == 4,
        ),
    )


def main() -> int:
    affine_rows = rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    direct_current_kernel = sum(
        row.decision in {"current_kernel_front_door", "inverse_power_then_current_kernel"}
        for row in affine_rows
    )
    conditional_normalizers = sum(row.decision.startswith("normalize_to_current_kernel") for row in affine_rows)
    repair_rows = sum(row.decision.endswith("repair") or "repair" in row.decision for row in affine_rows)
    transfer_rows = sum(row.decision.startswith("transfer_only") for row in affine_rows)
    current_matched_zero_lattice_packets = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    overall_ok = (
        P25 % 8 == 5
        and markers_ok == len(EVIDENCE_MARKERS)
        and len(affine_rows) == 8
        and all(row.ok for row in affine_rows)
        and direct_current_kernel == 2
        and conditional_normalizers == 2
        and repair_rows == 3
        and transfer_rows == 1
        and current_matched_zero_lattice_packets == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 affine row-product classifier")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("zero_lattice_basis")
    for name, vector in ZERO_BASIS.items():
        print(f"  {name}={vector}")
    print("rows")
    for row in affine_rows:
        reductions = [can_reduce_to_row_power(row.vector, index) for index in range(4)]
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    vector={row.vector}")
        print(f"    coefficient_sum={row.coeff_sum}")
        print(f"    scalar_gcd={row.scalar_gcd}")
        print(f"    reductions={reductions}")
        print(f"    required_extra={row.required_extra}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  affine_rows={len(affine_rows)}")
    print(f"  direct_current_kernel_rows={direct_current_kernel}")
    print(f"  conditional_zero_lattice_normalizers={conditional_normalizers}")
    print(f"  repair_rows={repair_rows}")
    print(f"  transfer_only_rows={transfer_rows}")
    print(f"  current_matched_zero_lattice_packets={current_matched_zero_lattice_packets}")
    print(f"  current_source_stage_closers={current_source_stage_closers}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  affine_unit_sum_aggregate_needs_exact_matched_zero_lattice_value=1")
    print("  nonunit_coefficient_sum_retains_root_debt=1")
    print("  zero_lattice_value_is_transfer_only=1")
    print(f"p25_v2_affine_row_product_classifier_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("affine row-product classifier failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

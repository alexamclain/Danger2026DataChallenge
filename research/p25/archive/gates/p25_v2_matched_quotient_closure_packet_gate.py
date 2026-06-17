#!/usr/bin/env python3
"""Validate the matched-quotient closure packet for affine row products."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_matched_quotient_closure_packet_rows=1/1"
ROW_NAMES = ("m1", "m2", "m4", "m8")


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
class PacketRow:
    name: str
    vector: tuple[int, int, int, int]
    target_index: int
    supplied_quotient: tuple[int, int, int, int] | None
    decision: str
    first_missing_or_falsifier: str

    @property
    def coeff_sum(self) -> int:
        return sum(self.vector)

    @property
    def target_name(self) -> str:
        return ROW_NAMES[self.target_index]


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "row_value_reconstruction_basis",
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
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
        "affine_row_product_classifier",
        "evidence/p25_v2_affine_row_product_classifier_20260617.md",
        "p25_v2_affine_row_product_classifier_rows=1/1",
    ),
    EvidenceMarker(
        "affine_row_normal_form",
        "evidence/p25_v2_affine_row_normal_form_20260617.md",
        "p25_v2_affine_row_normal_form_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
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


def zero_lattice_coordinates(vector: tuple[int, int, int, int]) -> tuple[int, int, int] | None:
    if sum(vector) != 0:
        return None
    a, b, c = vector[1], vector[2], vector[3]
    if (-a - b - c, a, b, c) != vector:
        return None
    return (a, b, c)


def matched_quotient(
    vector: tuple[int, int, int, int],
    target_index: int,
) -> tuple[int, int, int, int]:
    return sub(vector, scale(sum(vector), unit(target_index)))


def closure_identity_holds(
    vector: tuple[int, int, int, int],
    quotient: tuple[int, int, int, int],
    target_index: int,
) -> bool:
    return sub(vector, quotient) == scale(sum(vector), unit(target_index))


def package_accepts(row: PacketRow) -> bool:
    if row.supplied_quotient is None:
        return False
    return (
        row.supplied_quotient == matched_quotient(row.vector, row.target_index)
        and zero_lattice_coordinates(row.supplied_quotient) is not None
        and row.coeff_sum != 0
        and gcd(row.coeff_sum, PM1) == 1
        and closure_identity_holds(row.vector, row.supplied_quotient, row.target_index)
    )


def packet_rows() -> tuple[PacketRow, ...]:
    return (
        PacketRow(
            name="unit_sum_matched_packet",
            vector=(2, -1, 0, 0),
            target_index=0,
            supplied_quotient=(1, -1, 0, 0),
            decision="normalize_to_current_kernel",
            first_missing_or_falsifier="none if both aggregate value and exact matched quotient value are source theorems",
        ),
        PacketRow(
            name="unit_power_matched_packet",
            vector=(2, 1, 0, 0),
            target_index=0,
            supplied_quotient=(-1, 1, 0, 0),
            decision="normalize_to_current_kernel_after_inverse_exponent",
            first_missing_or_falsifier="none if aggregate, matched quotient, and exponent-3 inverse are valid",
        ),
        PacketRow(
            name="full_zero_basis_matched_packet",
            vector=(2, 1, 1, 1),
            target_index=0,
            supplied_quotient=(-3, 1, 1, 1),
            decision="normalize_to_current_kernel_after_inverse_exponent",
            first_missing_or_falsifier="requires exact zero-lattice value for q2_1+q4_1+q8_1",
        ),
        PacketRow(
            name="aggregate_without_matched_quotient",
            vector=(2, -1, 0, 0),
            target_index=0,
            supplied_quotient=None,
            decision="repair_zero_lattice_value_missing",
            first_missing_or_falsifier="aggregate value alone leaves boundary-zero content unpaid",
        ),
        PacketRow(
            name="wrong_quotient_packet",
            vector=(2, -1, 0, 0),
            target_index=0,
            supplied_quotient=(-1, 1, 0, 0),
            decision="repair_unmatched_zero_lattice_value",
            first_missing_or_falsifier="supplied quotient is not v - s*e_m",
        ),
        PacketRow(
            name="zero_lattice_only_packet",
            vector=(-1, 1, 0, 0),
            target_index=0,
            supplied_quotient=(-1, 1, 0, 0),
            decision="transfer_only_not_first_anchor",
            first_missing_or_falsifier="coefficient sum zero cannot reveal common scalar",
        ),
        PacketRow(
            name="nonunit_pair_matched_packet",
            vector=(1, 1, 0, 0),
            target_index=0,
            supplied_quotient=(-1, 1, 0, 0),
            decision="repair_root_debt_remaining",
            first_missing_or_falsifier="R_m^2 remains after matched quotient; gcd(2,p-1)=2",
        ),
    )


def exhaustive_small_normal_forms_ok() -> bool:
    for vector in product(range(-3, 4), repeat=4):
        for target_index in range(4):
            q = matched_quotient(vector, target_index)
            if zero_lattice_coordinates(q) is None:
                return False
            if not closure_identity_holds(vector, q, target_index):
                return False
    return True


def main() -> int:
    rows = packet_rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    positive_rows = sum(package_accepts(row) for row in rows)
    repair_rows = sum(not package_accepts(row) and row.decision.startswith("repair") for row in rows)
    transfer_rows = sum(row.decision.startswith("transfer") for row in rows)
    current_matched_quotient_source_packets = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and exhaustive_small_normal_forms_ok()
        and len(rows) == 7
        and positive_rows == 3
        and repair_rows == 3
        and transfer_rows == 1
        and current_matched_quotient_source_packets == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 matched-quotient closure packet")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print(f"exhaustive_small_normal_forms_ok={int(exhaustive_small_normal_forms_ok())}")
    print("rows")
    for row in rows:
        q = matched_quotient(row.vector, row.target_index)
        supplied = row.supplied_quotient if row.supplied_quotient is not None else "none"
        inverse = pow(row.coeff_sum, -1, PM1) if row.coeff_sum and gcd(row.coeff_sum, PM1) == 1 else "none"
        print(f"  {row.name}: decision={row.decision} accepted_shape={int(package_accepts(row))}")
        print(f"    vector={row.vector}")
        print(f"    target={row.target_name}")
        print(f"    coefficient_sum={row.coeff_sum}")
        print(f"    scalar_gcd={gcd(row.coeff_sum, PM1)}")
        print(f"    required_matched_quotient={q}")
        print(f"    supplied_quotient={supplied}")
        print(f"    zero_lattice_coordinates={zero_lattice_coordinates(q)}")
        print(f"    inverse_exponent={inverse}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"packet_rows={len(rows)}")
    print(f"positive_matched_quotient_shapes={positive_rows}")
    print(f"repair_rows={repair_rows}")
    print(f"transfer_only_rows={transfer_rows}")
    print(f"current_matched_quotient_source_packets={current_matched_quotient_source_packets}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"{MARKER if row_ok else 'p25_v2_matched_quotient_closure_packet_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

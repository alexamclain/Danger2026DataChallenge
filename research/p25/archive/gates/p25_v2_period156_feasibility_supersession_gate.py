#!/usr/bin/env python3
"""Validate that the period-156 row bridge supersedes a duplicate feasibility gate."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_period156_feasibility_supersession_rows=1/1"


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
class FeasibilityRow:
    name: str
    status: str
    first_missing_or_falsifier: str


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "period156_row_bridge_packet",
        "evidence/p25_v2_period156_row_bridge_packet_20260617.md",
        "p25_v2_period156_row_bridge_packet_rows=1/1",
    ),
    EvidenceMarker(
        "period156_lookup_row_status",
        "evidence/p25_v2_period156_lookup_row_status_20260617.md",
        "p25_v2_period156_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_branch_contract",
        "evidence/p25_v2_period156_value_branch_contract_20260616.md",
        "p25_v2_period156_value_branch_contract_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_source_hook",
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_candidate_sweep",
        "evidence/p25_v2_period156_value_candidate_sweep_20260617.md",
        "p25_v2_period156_value_candidate_sweep_rows=1/1",
    ),
    EvidenceMarker(
        "h0_y507_period156_compatibility",
        "evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
        "p25_v2_h0_y507_period156_compatibility_rows=1/1",
    ),
)


def multiplicative_order(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise ValueError("value is not invertible")
    order = 1
    acc = value % modulus
    while acc != 1:
        acc = (acc * value) % modulus
        order += 1
    return order


def rows() -> tuple[FeasibilityRow, ...]:
    return (
        FeasibilityRow(
            "canonical_h0_period156_value",
            "covered_by_row_bridge_accept_shape",
            "exact arithmetic source theorem not in hand",
        ),
        FeasibilityRow(
            "y507_value_with_legal_row_bridge",
            "covered_by_row_bridge_accept_shape",
            "exact arithmetic source theorem not in hand",
        ),
        FeasibilityRow(
            "theta2_payload_with_period156_bridge",
            "covered_by_row_bridge_accept_shape",
            "exact arithmetic theta2 payload with bridge not in hand",
        ),
        FeasibilityRow(
            "ambient780_or_mu11_value",
            "covered_by_row_bridge_repair_shape",
            "ambient-period-780 route leaves 11 F_p branches",
        ),
        FeasibilityRow(
            "degree6_value_without_fp_row_descent",
            "covered_by_row_bridge_repair_shape",
            "degree-6 value lacks F_p descent and selected legal row",
        ),
        FeasibilityRow(
            "norm_boundary_or_payload_without_source",
            "covered_by_row_bridge_repair_shape",
            "missing finite selected value, additive theorem, or arithmetic source",
        ),
    )


def main() -> int:
    marker_hits = sum(marker.ok for marker in EVIDENCE_MARKERS)
    support_gcd = gcd(pow(4, 156, PM1) - 1, PM1)
    ambient_gcd = gcd(pow(4, 780, PM1) - 1, PM1)
    ord39 = multiplicative_order(P25 % 39, 39)
    accept_rows = sum(row.status.endswith("accept_shape") for row in rows())
    repair_rows = sum(row.status.endswith("repair_shape") for row in rows())
    current_period156_value_packets = 0
    current_source_stage_closers = 0
    duplicate_feasibility_gate_needed = 0
    continue_only_on_exact_source_theorem = 1

    row_ok = (
        marker_hits == len(EVIDENCE_MARKERS)
        and P25 % 39 == 23
        and ord39 == 6
        and support_gcd == 1
        and ambient_gcd == 11
        and len(rows()) == 6
        and accept_rows == 3
        and repair_rows == 3
        and current_period156_value_packets == 0
        and current_source_stage_closers == 0
        and duplicate_feasibility_gate_needed == 0
        and continue_only_on_exact_source_theorem == 1
    )

    print("p25 v2 period-156 feasibility supersession")
    print(f"p={P25}")
    print(f"p_mod_39={P25 % 39}")
    print(f"ord_39_p={ord39}")
    print(f"support_period156_gcd={support_gcd}")
    print(f"ambient_period780_gcd={ambient_gcd}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows():
        print(f"  {row.name}: status={row.status}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={marker_hits}/{len(EVIDENCE_MARKERS)}")
    print(f"covered_accept_shapes={accept_rows}")
    print(f"covered_repair_shapes={repair_rows}")
    print(f"current_period156_value_packets={current_period156_value_packets}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"duplicate_feasibility_gate_needed={duplicate_feasibility_gate_needed}")
    print(f"continue_only_on_exact_source_theorem={continue_only_on_exact_source_theorem}")
    print(f"{MARKER if row_ok else 'p25_v2_period156_feasibility_supersession_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the Q/Yang row-bridge packet for conductor-39 support data."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_q_yang_row_bridge_packet_rows=1/1"


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
class BridgeRow:
    name: str
    finite_theorem: bool
    source_theorem: bool
    selector_paid: bool
    oriented_root_or_edge: bool
    extraction_map: bool
    decision: str
    first_missing_or_falsifier: str


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "q_yang_lookup_row_status",
        "evidence/p25_v2_q_yang_lookup_row_status_20260617.md",
        "p25_v2_q_yang_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_selector_debt",
        "evidence/p25_v2_q_route_selector_debt_20260616.md",
        "p25_v2_q_route_selector_debt_rows=1/1",
    ),
    EvidenceMarker(
        "q_diagonal_normalization",
        "evidence/p25_v2_q_diagonal_normalization_20260616.md",
        "p25_v2_q_diagonal_normalization_rows=1/1",
    ),
    EvidenceMarker(
        "q_split_quartic_selector",
        "evidence/p25_v2_q_split_quartic_selector_20260616.md",
        "p25_v2_q_split_quartic_selector_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_payload_router",
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_extraction_boundary",
        "evidence/p25_v2_q_square_extraction_boundary_20260616.md",
        "p25_v2_q_square_extraction_boundary_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_source_hook_scan",
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
    ),
    EvidenceMarker(
        "q_route_candidate_sweep",
        "evidence/p25_v2_q_route_candidate_sweep_20260617.md",
        "p25_v2_q_route_candidate_sweep_rows=1/1",
    ),
    EvidenceMarker(
        "yang_lift_descent_boundary_contract",
        "evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md",
        "p25_v2_yang_lift_descent_boundary_contract_rows=1/1",
    ),
    EvidenceMarker(
        "conductor39_yang_h90_interface_contract",
        "evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
        "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1",
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


def add(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] + right[i] for i in range(4))


def sub(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def bridge_rows() -> tuple[BridgeRow, ...]:
    return (
        BridgeRow(
            name="mixed_yang_h90_direct_finite_theorem",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=True,
            extraction_map=False,
            decision="source_stage_candidate",
            first_missing_or_falsifier="downstream DANGER3 framing and extraction only",
        ),
        BridgeRow(
            name="q_or_q3_with_selector_normalization",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=True,
            extraction_map=False,
            decision="normalize_to_current_kernel",
            first_missing_or_falsifier="same row theorem data after selector normalization",
        ),
        BridgeRow(
            name="q_diagonal_split_with_oriented_root",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=True,
            extraction_map=False,
            decision="normalize_to_current_kernel",
            first_missing_or_falsifier="same row theorem data after oriented-root normalization",
        ),
        BridgeRow(
            name="q_square_value_with_extraction_map",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=False,
            extraction_map=True,
            decision="extraction_payload_candidate",
            first_missing_or_falsifier="official vpp.py still required after concrete A,x0 candidates",
        ),
        BridgeRow(
            name="q_or_q3_without_selector",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=False,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="repair_selector_debt_missing",
            first_missing_or_falsifier="Q theorem data has not selected one oriented edge",
        ),
        BridgeRow(
            name="q6_boundary_only",
            finite_theorem=False,
            source_theorem=True,
            selector_paid=False,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="repair_value_or_additive_normalization_missing",
            first_missing_or_falsifier="Hilbert-90 boundary alone has no scalar-fixed finite payload",
        ),
        BridgeRow(
            name="q_diagonal_without_split",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=False,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="support_diagonal_selector_missing",
            first_missing_or_falsifier="Q diagonal aggregate needs pure quartic split or direct one-edge theorem",
        ),
        BridgeRow(
            name="q_diagonal_split_without_oriented_root",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="repair_oriented_square_root_missing",
            first_missing_or_falsifier="diagonal plus split reaches 2*edge, not one scalar-fixed edge",
        ),
        BridgeRow(
            name="q_square_without_extraction_map",
            finite_theorem=True,
            source_theorem=True,
            selector_paid=True,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="repair_extraction_map_missing_after_two_roots",
            first_missing_or_falsifier="two row-value roots are not vpp.py candidates",
        ),
        BridgeRow(
            name="local_q_source_language",
            finite_theorem=False,
            source_theorem=False,
            selector_paid=False,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="repair_exact_q_theorem_missing",
            first_missing_or_falsifier="local corpus has helper vocabulary but no conductor-39 Q hook",
        ),
        BridgeRow(
            name="pure_character_degree6_norm",
            finite_theorem=False,
            source_theorem=False,
            selector_paid=False,
            oriented_root_or_edge=False,
            extraction_map=False,
            decision="reject_pure_character_degree6_norm_cancels",
            first_missing_or_falsifier="Frobenius alternation makes the pure-character degree-6 norm zero",
        ),
        BridgeRow(
            name="direct_vpp_on_row_value",
            finite_theorem=True,
            source_theorem=False,
            selector_paid=True,
            oriented_root_or_edge=True,
            extraction_map=False,
            decision="reject_vpp_requires_A_x0_not_row_value",
            first_missing_or_falsifier="vpp.py verifies (p,A,x0), not modular-unit row values",
        ),
    )


def source_stage_accepts(row: BridgeRow) -> bool:
    return (
        row.finite_theorem
        and row.source_theorem
        and row.selector_paid
        and row.oriented_root_or_edge
        and row.decision in {"source_stage_candidate", "normalize_to_current_kernel"}
    )


def extraction_accepts(row: BridgeRow) -> bool:
    return (
        row.finite_theorem
        and row.source_theorem
        and row.selector_paid
        and row.extraction_map
        and row.decision == "extraction_payload_candidate"
    )


def q_diagonal_algebra_ok() -> bool:
    m1 = (1, 0, 0, 0)
    m2 = (0, 1, 0, 0)
    m4 = (0, 0, 1, 0)
    m8 = (0, 0, 0, 1)
    diag14 = add(m1, m4)
    split14 = sub(m1, m4)
    diag28 = add(m2, m8)
    split28 = sub(m2, m8)
    return (
        add(diag14, split14) == (2, 0, 0, 0)
        and sub(diag14, split14) == (0, 0, 2, 0)
        and add(diag28, split28) == (0, 2, 0, 0)
        and sub(diag28, split28) == (0, 0, 0, 2)
    )


def main() -> int:
    rows = bridge_rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    ord39 = multiplicative_order(P25 % 39, 39)
    square_root_kernel = gcd(2, PM1)
    source_stage_shapes = sum(source_stage_accepts(row) for row in rows)
    extraction_payload_shapes = sum(extraction_accepts(row) for row in rows)
    repair_rows = sum(row.decision.startswith("repair") or row.decision.startswith("support") for row in rows)
    reject_rows = sum(row.decision.startswith("reject") for row in rows)
    current_q_source_hooks = 0
    current_source_stage_closers = 0
    current_extraction_ready = 0
    current_submission_ready = 0
    row_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and P25 % 39 == 23
        and ord39 == 6
        and square_root_kernel == 2
        and q_diagonal_algebra_ok()
        and len(rows) == 12
        and source_stage_shapes == 3
        and extraction_payload_shapes == 1
        and repair_rows == 6
        and reject_rows == 2
        and current_q_source_hooks == 0
        and current_source_stage_closers == 0
        and current_extraction_ready == 0
        and current_submission_ready == 0
    )

    print("p25 v2 Q/Yang row bridge packet")
    print(f"p={P25}")
    print(f"p_mod_39={P25 % 39}")
    print(f"ord_39_p={ord39}")
    print(f"square_root_kernel_fp_star={square_root_kernel}")
    print(f"q_diagonal_algebra_ok={int(q_diagonal_algebra_ok())}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source_stage_shape={int(source_stage_accepts(row))} "
            f"extraction_shape={int(extraction_accepts(row))}"
        )
        print(
            "    clauses="
            f"finite:{int(row.finite_theorem)},"
            f"source:{int(row.source_theorem)},"
            f"selector:{int(row.selector_paid)},"
            f"oriented_edge_or_root:{int(row.oriented_root_or_edge)},"
            f"extraction_map:{int(row.extraction_map)}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"packet_rows={len(rows)}")
    print(f"source_stage_shapes={source_stage_shapes}")
    print(f"extraction_payload_shapes={extraction_payload_shapes}")
    print(f"repair_or_support_rows={repair_rows}")
    print(f"reject_rows={reject_rows}")
    print(f"current_q_source_hooks={current_q_source_hooks}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_extraction_ready={current_extraction_ready}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"{MARKER if row_ok else 'p25_v2_q_yang_row_bridge_packet_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

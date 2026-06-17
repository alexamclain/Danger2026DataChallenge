#!/usr/bin/env python3
"""Validate the period-156 value row-bridge packet."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_period156_row_bridge_packet_rows=1/1"


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
    finite_value: bool
    arithmetic_source: bool
    period156_context: bool
    legal_row_bridge: bool
    norm_boundary: bool
    branch_or_additive_normalization: bool
    decision: str
    first_missing_or_falsifier: str


EVIDENCE_MARKERS = (
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
        "h0_y507_period156_compatibility",
        "evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
        "p25_v2_h0_y507_period156_compatibility_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_candidate_sweep",
        "evidence/p25_v2_period156_value_candidate_sweep_20260617.md",
        "p25_v2_period156_value_candidate_sweep_rows=1/1",
    ),
    EvidenceMarker(
        "degree6_value_descent_ambiguity",
        "evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
        "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
    ),
    EvidenceMarker(
        "norm_only_descent_ambiguity",
        "evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
        "p25_v2_norm_only_descent_ambiguity_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
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


def legendre_symbol(value: int, prime: int) -> int:
    result = pow(value % prime, (prime - 1) // 2, prime)
    if result == prime - 1:
        return -1
    return result


def packet_rows() -> tuple[PacketRow, ...]:
    return (
        PacketRow(
            name="canonical_h0_period156_value_packet",
            finite_value=True,
            arithmetic_source=True,
            period156_context=True,
            legal_row_bridge=True,
            norm_boundary=True,
            branch_or_additive_normalization=True,
            decision="source_stage_value_candidate",
            first_missing_or_falsifier="downstream DANGER3 framing and extraction only",
        ),
        PacketRow(
            name="y507_value_with_legal_row_bridge",
            finite_value=True,
            arithmetic_source=True,
            period156_context=True,
            legal_row_bridge=True,
            norm_boundary=True,
            branch_or_additive_normalization=True,
            decision="source_stage_value_candidate",
            first_missing_or_falsifier="downstream DANGER3 framing and extraction only",
        ),
        PacketRow(
            name="theta2_payload_with_period156_bridge",
            finite_value=True,
            arithmetic_source=True,
            period156_context=True,
            legal_row_bridge=True,
            norm_boundary=True,
            branch_or_additive_normalization=True,
            decision="theta2_or_exactp_bridge_candidate",
            first_missing_or_falsifier="must route through theta2/exact-P bridge and extraction",
        ),
        PacketRow(
            name="y507_value_without_legal_row_bridge",
            finite_value=True,
            arithmetic_source=True,
            period156_context=True,
            legal_row_bridge=False,
            norm_boundary=True,
            branch_or_additive_normalization=True,
            decision="repair_legal_row_bridge_missing",
            first_missing_or_falsifier="Y_507 value does not select one legal support-156 row",
        ),
        PacketRow(
            name="canonical_value_without_period156_context",
            finite_value=True,
            arithmetic_source=True,
            period156_context=False,
            legal_row_bridge=True,
            norm_boundary=True,
            branch_or_additive_normalization=False,
            decision="repair_period156_branch_missing",
            first_missing_or_falsifier="value lacks support-period-156 branch/root/telescoping or additive normalization",
        ),
        PacketRow(
            name="ambient780_value_or_mu11_quotient",
            finite_value=True,
            arithmetic_source=True,
            period156_context=False,
            legal_row_bridge=False,
            norm_boundary=False,
            branch_or_additive_normalization=False,
            decision="repair_ambient_mu11_branch",
            first_missing_or_falsifier="ambient-period-780 route leaves 11 F_p branches",
        ),
        PacketRow(
            name="degree6_value_without_fp_row_descent",
            finite_value=True,
            arithmetic_source=True,
            period156_context=False,
            legal_row_bridge=False,
            norm_boundary=False,
            branch_or_additive_normalization=False,
            decision="repair_fp_descent_and_row_selection_missing",
            first_missing_or_falsifier="degree-6 value lacks F_p descent and selected legal row",
        ),
        PacketRow(
            name="norm_or_boundary_only",
            finite_value=False,
            arithmetic_source=True,
            period156_context=True,
            legal_row_bridge=False,
            norm_boundary=True,
            branch_or_additive_normalization=False,
            decision="repair_finite_value_or_divisor_theorem_missing",
            first_missing_or_falsifier="Norm_156(Y_507) boundary does not choose a legal preimage row value",
        ),
        PacketRow(
            name="finite_payload_without_source",
            finite_value=True,
            arithmetic_source=False,
            period156_context=True,
            legal_row_bridge=True,
            norm_boundary=True,
            branch_or_additive_normalization=True,
            decision="repair_arithmetic_source_theorem_missing",
            first_missing_or_falsifier="finite payload is a target, not a source theorem",
        ),
        PacketRow(
            name="direct_fp_order39_or_sqrt_minus39_shortcut",
            finite_value=False,
            arithmetic_source=False,
            period156_context=False,
            legal_row_bridge=False,
            norm_boundary=False,
            branch_or_additive_normalization=False,
            decision="reject_arithmetic_shortcut",
            first_missing_or_falsifier="ord_39(p)=6 and sqrt(-39) is not in F_p",
        ),
    )


def row_is_accepted(row: PacketRow) -> bool:
    return (
        row.finite_value
        and row.arithmetic_source
        and row.period156_context
        and row.legal_row_bridge
        and row.norm_boundary
        and row.branch_or_additive_normalization
        and row.decision in {
            "source_stage_value_candidate",
            "theta2_or_exactp_bridge_candidate",
        }
    )


def main() -> int:
    rows = packet_rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    ord39 = multiplicative_order(P25 % 39, 39)
    support_gcd = gcd(pow(4, 156, PM1) - 1, PM1)
    ambient_gcd = gcd(pow(4, 780, PM1) - 1, PM1)
    sqrt_minus39_in_fp = legendre_symbol(-39, P25) == 1
    accepted_rows = sum(row_is_accepted(row) for row in rows)
    source_stage_value_shapes = sum(
        row.decision == "source_stage_value_candidate" for row in rows
    )
    theta2_bridge_shapes = sum(
        row.decision == "theta2_or_exactp_bridge_candidate" for row in rows
    )
    repair_rows = sum(row.decision.startswith("repair") for row in rows)
    reject_rows = sum(row.decision.startswith("reject") for row in rows)
    current_period156_value_packets = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and P25 % 39 == 23
        and ord39 == 6
        and support_gcd == 1
        and ambient_gcd == 11
        and not sqrt_minus39_in_fp
        and len(rows) == 10
        and accepted_rows == 3
        and source_stage_value_shapes == 2
        and theta2_bridge_shapes == 1
        and repair_rows == 6
        and reject_rows == 1
        and current_period156_value_packets == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 period-156 row bridge packet")
    print(f"p={P25}")
    print(f"p_mod_39={P25 % 39}")
    print(f"ord_39_p={ord39}")
    print(f"support_period156_gcd={support_gcd}")
    print(f"ambient_period780_gcd={ambient_gcd}")
    print(f"sqrt_minus39_in_fp={int(sqrt_minus39_in_fp)}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} accepted_shape={int(row_is_accepted(row))}")
        print(
            "    clauses="
            f"finite_value:{int(row.finite_value)},"
            f"source:{int(row.arithmetic_source)},"
            f"period156:{int(row.period156_context)},"
            f"row_bridge:{int(row.legal_row_bridge)},"
            f"norm_boundary:{int(row.norm_boundary)},"
            f"branch_or_additive:{int(row.branch_or_additive_normalization)}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"packet_rows={len(rows)}")
    print(f"accepted_period156_bridge_shapes={accepted_rows}")
    print(f"source_stage_value_shapes={source_stage_value_shapes}")
    print(f"theta2_bridge_shapes={theta2_bridge_shapes}")
    print(f"repair_rows={repair_rows}")
    print(f"reject_rows={reject_rows}")
    print(f"current_period156_value_packets={current_period156_value_packets}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"{MARKER if row_ok else 'p25_v2_period156_row_bridge_packet_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

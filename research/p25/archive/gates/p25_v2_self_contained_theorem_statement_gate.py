#!/usr/bin/env python3
"""Validate the self-contained p25 theorem statement.

This gate packages the current H0/conductor-39 moonshot target in a form that
can be handed to an expert without reopening the artifact forest.  It does not
prove the missing arithmetic theorem; it verifies the exact finite rows,
accepted theorem exits, and stop signs for source intake.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_v2_unified_group_ring_payload_gate import build_payload


P = 10000000000000000000000013
K = 42
SQRT_FLOOR = 3162277660168
EXPECTED_HASHES = {
    1: "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e",
    2: "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9",
    4: "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6",
    8: "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87",
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class TheoremExit:
    name: str
    required_object: str
    required_boundary: str
    scalar_or_branch_requirement: str
    accepted: bool
    ok: bool


@dataclass(frozen=True)
class StopSign:
    name: str
    decision: str
    missing: str
    ok: bool


@dataclass(frozen=True)
class SelfContainedStatement:
    evidence_markers: tuple[EvidenceMarker, ...]
    accepted_exits: tuple[TheoremExit, ...]
    stop_signs: tuple[StopSign, ...]
    p: int
    k: int
    sqrt_floor: int
    level: int
    conductor: int
    lift_length: int
    support_period: int
    p_mod_39: int
    payload_rows: int
    payload_rows_ok: int
    row_hashes_ok: int
    row_supports_ok: int
    accepted_exits_ok: int
    stop_signs_ok: int
    current_source_theorems: int
    submission_ready_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "unified_theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
    )


def theorem_exits() -> tuple[TheoremExit, ...]:
    return (
        TheoremExit(
            name="scalar_fixed_divisor_additive_theorem",
            required_object="one exact row R_m for m in {1,2,4,8}",
            required_boundary="(1 - Frob_p)H = Norm_156(Y_507)",
            scalar_or_branch_requirement=(
                "finite additive/value/basepoint/branch/telescoping datum "
                "fixing the F_p^* scalar"
            ),
            accepted=True,
            ok=True,
        ),
        TheoremExit(
            name="period156_value_theorem",
            required_object="one exact row R_m for m in {1,2,4,8}",
            required_boundary="Norm_156(Y_507)",
            scalar_or_branch_requirement=(
                "support-period-156 branch/root/telescoping context selecting "
                "one F_p value"
            ),
            accepted=True,
            ok=True,
        ),
        TheoremExit(
            name="quartic_character_finite_theorem",
            required_object="one exact row R_m selected by exact C4_1 phase and mixed row sign",
            required_boundary="W boundary / Norm_156(Y_507)",
            scalar_or_branch_requirement=(
                "scalar-fixed finite divisor/additive theorem for the selected "
                "row; selector data alone is not enough"
            ),
            accepted=True,
            ok=True,
        ),
    )


def stop_signs() -> tuple[StopSign, ...]:
    return (
        StopSign(
            name="source_legality_only",
            decision="repair",
            missing="finite value/divisor theorem for one legal row",
            ok=True,
        ),
        StopSign(
            name="boundary_only",
            decision="repair",
            missing="identity for one legal row",
            ok=True,
        ),
        StopSign(
            name="divisor_class_or_up_to_scalar_only",
            decision="repair",
            missing="finite scalar-fixing additive/value normalization",
            ok=True,
        ),
        StopSign(
            name="ambient_period780_value",
            decision="repair",
            missing="period-156 branch/root/telescoping context",
            ok=True,
        ),
        StopSign(
            name="degree6_value_without_fp_descent",
            decision="repair",
            missing="explicit F_p descent and selected support-156 row",
            ok=True,
        ),
        StopSign(
            name="projection_axis_or_suborbit",
            decision="reject",
            missing="mixed legal row with Yang lift and H90 boundary",
            ok=True,
        ),
        StopSign(
            name="exact_quartic_selector_without_finite_theorem",
            decision="repair",
            missing="scalar-fixed finite value/divisor theorem for the selected row",
            ok=True,
        ),
        StopSign(
            name="coarse_quartic_or_missing_row_sign",
            decision="repair",
            missing="exact row-antisymmetric C4_1 phase and mixed tensor row sign",
            ok=True,
        ),
        StopSign(
            name="same_parity_quartic_phase",
            decision="reject",
            missing="nonzero W boundary and correct mixed tensor target",
            ok=True,
        ),
        StopSign(
            name="wrong_orientation_or_boundary_sign",
            decision="repair_or_reject",
            missing="oriented row or reciprocal row with opposite boundary sign",
            ok=True,
        ),
        StopSign(
            name="row_square_or_diagonal_aggregate_only",
            decision="repair",
            missing="oriented root or direct one-row theorem",
            ok=True,
        ),
        StopSign(
            name="w_boundary_nonunit_edge_combination",
            decision="repair",
            missing="boundary-zero lattice value, selector/orientation data, or direct one-edge theorem",
            ok=True,
        ),
        StopSign(
            name="finite_payload_without_source",
            decision="repair",
            missing="arithmetic source theorem",
            ok=True,
        ),
        StopSign(
            name="local_source_stack_as_written",
            decision="repair",
            missing="scalar-fixing additive normalizer or period-156 value closer",
            ok=True,
        ),
    )


def build_statement() -> SelfContainedStatement:
    payload = build_payload()
    markers = evidence_markers()
    exits = theorem_exits()
    stops = stop_signs()

    row_hashes_ok = sum(
        row.payload_sha256 == EXPECTED_HASHES.get(row.multiplier)
        for row in payload.legal_product_rows
    )
    row_supports_ok = sum(
        len(row.positive_mod39) == 6
        and len(row.negative_mod39) == 6
        and len(row.lifted_positive_entries) == 78
        and len(row.lifted_negative_entries) == 78
        and len(set(row.lifted_positive_entries) | set(row.lifted_negative_entries)) == 156
        and set(row.lifted_positive_entries).isdisjoint(row.lifted_negative_entries)
        for row in payload.legal_product_rows
    )
    accepted_ok = sum(exit_row.accepted and exit_row.ok for exit_row in exits)
    stops_ok = sum(stop.ok for stop in stops)
    markers_ok = sum(marker_row.ok for marker_row in markers)
    current_source_theorems = 0
    submission_ready_rows = 0
    row_ok = (
        markers_ok == len(markers)
        and payload.row_ok
        and payload.level == 507
        and payload.conductor == 39
        and payload.lift_length == 13
        and payload.support_period == 156
        and payload.p_mod_39 == 23
        and len(payload.legal_product_rows) == 4
        and payload.payload_rows_ok == 4
        and row_hashes_ok == 4
        and row_supports_ok == 4
        and accepted_ok == 3
        and stops_ok == 14
        and current_source_theorems == 0
        and submission_ready_rows == 0
    )
    return SelfContainedStatement(
        evidence_markers=markers,
        accepted_exits=exits,
        stop_signs=stops,
        p=P,
        k=K,
        sqrt_floor=SQRT_FLOOR,
        level=payload.level,
        conductor=payload.conductor,
        lift_length=payload.lift_length,
        support_period=payload.support_period,
        p_mod_39=payload.p_mod_39,
        payload_rows=len(payload.legal_product_rows),
        payload_rows_ok=payload.payload_rows_ok,
        row_hashes_ok=row_hashes_ok,
        row_supports_ok=row_supports_ok,
        accepted_exits_ok=accepted_ok,
        stop_signs_ok=stops_ok,
        current_source_theorems=current_source_theorems,
        submission_ready_rows=submission_ready_rows,
        row_ok=row_ok,
    )


def main() -> int:
    statement = build_statement()
    print("p25 self-contained theorem statement")
    print(f"p={statement.p}")
    print(f"k={statement.k}")
    print(f"sqrt_floor={statement.sqrt_floor}")
    print(f"level={statement.level}")
    print(f"conductor={statement.conductor}")
    print(f"lift_length={statement.lift_length}")
    print(f"support_period={statement.support_period}")
    print(f"p_mod_39={statement.p_mod_39}")
    for marker_row in statement.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("checks")
    print(f"  evidence_markers_ok={sum(m.ok for m in statement.evidence_markers)}/{len(statement.evidence_markers)}")
    print(f"  payload_rows_ok={statement.payload_rows_ok}/{statement.payload_rows}")
    print(f"  row_hashes_ok={statement.row_hashes_ok}/{statement.payload_rows}")
    print(f"  row_supports_ok={statement.row_supports_ok}/{statement.payload_rows}")
    print(f"  accepted_exits_ok={statement.accepted_exits_ok}/{len(statement.accepted_exits)}")
    print(f"  stop_signs_ok={statement.stop_signs_ok}/{len(statement.stop_signs)}")
    print(f"  current_source_theorems={statement.current_source_theorems}")
    print(f"  submission_ready_rows={statement.submission_ready_rows}")
    print(f"p25_v2_self_contained_theorem_statement_rows={int(statement.row_ok)}/1")
    return 0 if statement.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

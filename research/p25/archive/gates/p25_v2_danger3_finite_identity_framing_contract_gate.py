#!/usr/bin/env python3
"""DANGER3 finite-identity framing contract for the p25 v2 frontier.

The first-pass theorem ask is now exact, but a theorem hit still has to be
framed as a DANGER3-usable finite identity before extraction. This gate keeps
generic CM or class-field generation from being over-counted as that framing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class FramingRow:
    name: str
    payload: str
    decision: str
    source_stage_closed: bool
    danger3_unblocked: bool
    same_j_bridge_identified: bool
    x16_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class Danger3FiniteIdentityFramingContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[FramingRow, ...]
    evidence_markers_ok: int
    rejected_rows: int
    source_shape_missing_rows: int
    policy_or_framing_missing_rows: int
    danger3_unblocked_rows: int
    same_j_bridge_rows: int
    x16_surface_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    current_danger3_framed_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "post_theorem_extraction_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
    )


def row(
    name: str,
    payload: str,
    decision: str,
    missing: str,
    *,
    source_closed: bool = False,
    danger3: bool = False,
    same_j: bool = False,
    x16: bool = False,
    extraction: bool = False,
    submission: bool = False,
) -> FramingRow:
    return FramingRow(
        name=name,
        payload=payload,
        decision=decision,
        source_stage_closed=source_closed,
        danger3_unblocked=danger3,
        same_j_bridge_identified=same_j,
        x16_surface_reached=x16,
        extraction_ready=extraction,
        submission_ready=submission,
        first_missing_or_falsifier=missing,
        ok=True,
    )


def framing_rows() -> tuple[FramingRow, ...]:
    return (
        row(
            "no_source_no_triple",
            "no arithmetic theorem and no concrete A,x0 triple",
            "reject_no_source_theorem_or_triple",
            "source theorem or concrete vpp-verifiable triple",
        ),
        row(
            "source_theorem_no_finite_identity",
            "source theorem, class-field statement, or unit theorem with no exact p25 finite identity",
            "source_theorem_value_shape_missing_finite_identity",
            "finite-field value/divisor identity specialized to p25",
        ),
        row(
            "generic_cm_class_field_generation",
            "generic CM, ray-class generation, or class-field generation presented as DANGER3 framing",
            "reject_generic_cm_generation_not_framing",
            "explicit non-CM finite-field identity framing or external policy yes",
        ),
        row(
            "finite_identity_policy_unknown",
            "finite p25 value/divisor identity, but no DANGER3/non-CM framing yet",
            "source_theorem_closed_policy_or_framing_missing",
            "DANGER3 finite-identity/non-CM framing",
            source_closed=True,
        ),
        row(
            "finite_identity_explicit_non_cm_no_bridge",
            "finite p25 identity with explicit non-CM finite-field framing",
            "danger3_unblocked_same_j_bridge_missing",
            "same-j X_1(8112) bridge or equivalent cross-level map",
            source_closed=True,
            danger3=True,
        ),
        row(
            "finite_identity_policy_yes_no_bridge",
            "finite p25 identity with an external DANGER3 policy yes",
            "danger3_unblocked_same_j_bridge_missing",
            "same-j X_1(8112) bridge or equivalent cross-level map",
            source_closed=True,
            danger3=True,
        ),
        row(
            "same_j_bridge_no_x16",
            "DANGER3-framed theorem plus same-curve P16/Q507 bridge",
            "same_j_bridge_x16_surface_missing",
            "practical X_1(16) y plus model root or direct A,xP16",
            source_closed=True,
            danger3=True,
            same_j=True,
        ),
        row(
            "x16_surface_no_x0",
            "DANGER3-framed theorem plus practical A,xP16 surface",
            "x16_surface_reached_halving_missing",
            "38-link halving chain or direct concrete x0",
            source_closed=True,
            danger3=True,
            same_j=True,
            x16=True,
        ),
        row(
            "concrete_A_x0_no_vpp",
            "concrete A,x0 obtained from the framed theorem and extraction ladder",
            "extraction_ready_vpp_missing",
            "official src/vpp.py verification",
            source_closed=True,
            danger3=True,
            same_j=True,
            x16=True,
            extraction=True,
        ),
        row(
            "official_vpp_verified_triple",
            "official vpp.py verifies concrete p25 (p,A,x0)",
            "submission_ready",
            "none",
            source_closed=True,
            danger3=True,
            same_j=True,
            x16=True,
            extraction=True,
            submission=True,
        ),
    )


def build_contract() -> Danger3FiniteIdentityFramingContract:
    markers = evidence_markers()
    rows = framing_rows()
    markers_ok = sum(item.ok for item in markers)
    rejected = sum(item.decision.startswith("reject_") for item in rows)
    source_shape_missing = sum(
        item.decision == "source_theorem_value_shape_missing_finite_identity"
        for item in rows
    )
    policy_missing = sum(
        item.decision == "source_theorem_closed_policy_or_framing_missing"
        for item in rows
    )
    danger3 = sum(item.danger3_unblocked for item in rows)
    same_j = sum(item.same_j_bridge_identified for item in rows)
    x16 = sum(item.x16_surface_reached for item in rows)
    extraction = sum(item.extraction_ready for item in rows)
    submission = sum(item.submission_ready for item in rows)
    current_danger3_framed = 0
    current_submission = 0
    expected = (
        "reject_no_source_theorem_or_triple",
        "source_theorem_value_shape_missing_finite_identity",
        "reject_generic_cm_generation_not_framing",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_same_j_bridge_missing",
        "danger3_unblocked_same_j_bridge_missing",
        "same_j_bridge_x16_surface_missing",
        "x16_surface_reached_halving_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_ok == len(markers)
        and len(rows) == 10
        and rejected == 2
        and source_shape_missing == 1
        and policy_missing == 1
        and danger3 == 6
        and same_j == 4
        and x16 == 3
        and extraction == 2
        and submission == 1
        and current_danger3_framed == 0
        and current_submission == 0
        and tuple(item.decision for item in rows) == expected
        and all(item.ok for item in rows)
    )
    return Danger3FiniteIdentityFramingContract(
        evidence_markers=markers,
        rows=rows,
        evidence_markers_ok=markers_ok,
        rejected_rows=rejected,
        source_shape_missing_rows=source_shape_missing,
        policy_or_framing_missing_rows=policy_missing,
        danger3_unblocked_rows=danger3,
        same_j_bridge_rows=same_j,
        x16_surface_rows=x16,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        current_danger3_framed_theorems=current_danger3_framed,
        current_submission_ready=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for marker_row in contract.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("framing_rows")
    for framing_row in contract.rows:
        print(
            "  "
            f"{framing_row.name}: decision={framing_row.decision} "
            f"source_closed={int(framing_row.source_stage_closed)} "
            f"danger3={int(framing_row.danger3_unblocked)} "
            f"same_j={int(framing_row.same_j_bridge_identified)} "
            f"x16={int(framing_row.x16_surface_reached)} "
            f"extraction={int(framing_row.extraction_ready)} "
            f"submission={int(framing_row.submission_ready)}"
        )
        print(f"    payload={framing_row.payload}")
        print(f"    missing_or_falsifier={framing_row.first_missing_or_falsifier}")
    print("counts")
    print(
        f"  evidence_markers_ok={contract.evidence_markers_ok}/"
        f"{len(contract.evidence_markers)}"
    )
    print(f"  rejected_rows={contract.rejected_rows}")
    print(f"  source_shape_missing_rows={contract.source_shape_missing_rows}")
    print(f"  policy_or_framing_missing_rows={contract.policy_or_framing_missing_rows}")
    print(f"  danger3_unblocked_rows={contract.danger3_unblocked_rows}")
    print(f"  same_j_bridge_rows={contract.same_j_bridge_rows}")
    print(f"  x16_surface_rows={contract.x16_surface_rows}")
    print(f"  extraction_ready_rows={contract.extraction_ready_rows}")
    print(f"  submission_ready_rows={contract.submission_ready_rows}")
    print(f"  current_danger3_framed_theorems={contract.current_danger3_framed_theorems}")
    print(f"  current_submission_ready={contract.current_submission_ready}")
    print("interpretation")
    print("  generic_cm_generation_is_not_danger3_framing=1")
    print("  finite_p25_identity_still_needs_non_cm_or_policy_framing=1")
    print("  framing_yes_still_needs_same_j_bridge_x16_halving_and_vpp=1")
    print("  only_official_vpp_verified_A_x0_is_submission_ready=1")
    print(f"p25_v2_danger3_finite_identity_framing_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Yang lift/descent boundary contract for p25 conductor-39 claims.

The conductor-39 object has a real source certificate, but source identity,
Yang lift, Hilbert-90 descent, and finite value/divisor theorem are separate
requirements.  This gate makes that ladder explicit so source snippets do not
get promoted merely for identifying U_chi or a level-507 lift.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


LEVEL = 507
CONDUCTOR = 39
LIFT_LENGTH = 13
SOURCE_SUPPORT = 12
LIFT_SUPPORT = 156
POSITIVE_FACTORS = 78
NEGATIVE_FACTORS = 78
BOUNDARY = "Norm_156(Y_507)"


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class YangLiftClaim:
    name: str
    shape: str
    mixed_unit: bool
    yang_lift: bool
    h90_descent: bool
    finite_theorem: bool
    legal_target: bool
    decision: str
    first_missing_or_falsifier: str
    source_stage_closed: bool
    continue_lane: bool
    ok: bool


@dataclass(frozen=True)
class YangLiftDescentBoundaryContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    level: int
    conductor: int
    lift_length: int
    source_support: int
    lift_support: int
    positive_factors: int
    negative_factors: int
    boundary: str
    claims: tuple[YangLiftClaim, ...]
    evidence_markers_ok: int
    source_closing_rows: int
    repair_rows: int
    reject_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "conductor39_yang_h90_interface",
            "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
            "P25 v2 Conductor-39 Yang/H90 Interface Contract",
        ),
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "unified_source_theorem_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "p25_v2_unified_source_theorem_gap_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def claim(
    name: str,
    shape: str,
    *,
    mixed: bool = False,
    lift: bool = False,
    h90: bool = False,
    finite: bool = False,
    legal: bool = True,
) -> YangLiftClaim:
    if not legal:
        decision = "reject_yang_lift_boundary_or_target_mismatch"
        missing = "legal mixed conductor-39 target with Norm_156(Y_507) boundary"
        closes = False
        continue_lane = False
    elif mixed and lift and h90 and finite:
        decision = "source_stage_win_route_to_extraction_contract"
        missing = "DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py"
        closes = True
        continue_lane = True
    elif mixed and not lift:
        decision = "repair_yang_lift_missing"
        missing = "level-507 Yang lift to the support-156 product"
        closes = False
        continue_lane = True
    elif mixed and lift and not h90:
        decision = "repair_h90_descent_boundary_missing"
        missing = "Hilbert-90 descent with boundary Norm_156(Y_507)"
        closes = False
        continue_lane = True
    elif mixed and lift and h90 and not finite:
        decision = "repair_value_divisor_theorem_missing"
        missing = "finite value/divisor theorem for the selected support-156 row"
        closes = False
        continue_lane = True
    else:
        decision = "repair_incomplete_yang_lift_claim"
        missing = "mixed source object, Yang lift, H90 boundary, and finite theorem"
        closes = False
        continue_lane = True

    return YangLiftClaim(
        name=name,
        shape=shape,
        mixed_unit=mixed,
        yang_lift=lift,
        h90_descent=h90,
        finite_theorem=finite,
        legal_target=legal,
        decision=decision,
        first_missing_or_falsifier=missing,
        source_stage_closed=closes,
        continue_lane=continue_lane,
        ok=True,
    )


def claim_rows() -> tuple[YangLiftClaim, ...]:
    return (
        claim(
            "mixed_unit_without_yang_lift",
            "U_chi/W or mixed chi_3 tensor chi_13 source word, but no level-507 Yang lift",
            mixed=True,
        ),
        claim(
            "mixed_yang_without_h90_descent",
            "mixed conductor-39 Yang lift to level 507, but no H90 descent/boundary",
            mixed=True,
            lift=True,
        ),
        claim(
            "yang_h90_source_without_finite_theorem",
            "legal support-156 Yang/H90 product with Norm_156(Y_507) boundary, but no finite theorem",
            mixed=True,
            lift=True,
            h90=True,
        ),
        claim(
            "yang_h90_with_finite_divisor_theorem",
            "legal support-156 Yang/H90 product plus finite divisor/additive theorem",
            mixed=True,
            lift=True,
            h90=True,
            finite=True,
        ),
        claim(
            "yang_h90_with_period156_value_theorem",
            "legal support-156 Yang/H90 product plus period-156 value theorem",
            mixed=True,
            lift=True,
            h90=True,
            finite=True,
        ),
        claim(
            "projection_or_suborbit_lift",
            "prime-axis projection, proper suborbit, or altered lift used as current target",
            mixed=True,
            lift=True,
            h90=True,
            finite=True,
            legal=False,
        ),
        claim(
            "wrong_boundary_lift",
            "level-507 lift whose boundary is not Norm_156(Y_507)",
            mixed=True,
            lift=True,
            h90=True,
            finite=True,
            legal=False,
        ),
    )


def build_contract() -> YangLiftDescentBoundaryContract:
    markers = evidence_markers()
    rows = claim_rows()
    markers_ok = sum(row.ok for row in markers)
    source_closing = sum(row.source_stage_closed for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    rejects = sum(row.decision.startswith("reject_") for row in rows)
    current_closers = 0
    expected = (
        "repair_yang_lift_missing",
        "repair_h90_descent_boundary_missing",
        "repair_value_divisor_theorem_missing",
        "source_stage_win_route_to_extraction_contract",
        "source_stage_win_route_to_extraction_contract",
        "reject_yang_lift_boundary_or_target_mismatch",
        "reject_yang_lift_boundary_or_target_mismatch",
    )
    row_ok = (
        markers_ok == len(markers)
        and LEVEL == 507
        and CONDUCTOR == 39
        and LIFT_LENGTH == 13
        and SOURCE_SUPPORT == 12
        and LIFT_SUPPORT == 156
        and POSITIVE_FACTORS == 78
        and NEGATIVE_FACTORS == 78
        and BOUNDARY == "Norm_156(Y_507)"
        and len(rows) == 7
        and source_closing == 2
        and repairs == 3
        and rejects == 2
        and current_closers == 0
        and tuple(row.decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    return YangLiftDescentBoundaryContract(
        evidence_markers=markers,
        level=LEVEL,
        conductor=CONDUCTOR,
        lift_length=LIFT_LENGTH,
        source_support=SOURCE_SUPPORT,
        lift_support=LIFT_SUPPORT,
        positive_factors=POSITIVE_FACTORS,
        negative_factors=NEGATIVE_FACTORS,
        boundary=BOUNDARY,
        claims=rows,
        evidence_markers_ok=markers_ok,
        source_closing_rows=source_closing,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for row in contract.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("target")
    print(f"  level={contract.level}")
    print(f"  conductor={contract.conductor}")
    print(f"  lift_length={contract.lift_length}")
    print(f"  source_support={contract.source_support}")
    print(f"  lift_support={contract.lift_support}")
    print(f"  positive_factors={contract.positive_factors}")
    print(f"  negative_factors={contract.negative_factors}")
    print(f"  boundary={contract.boundary}")
    print("claim_rows")
    for row in contract.claims:
        print(
            "  "
            f"{row.name}: decision={row.decision} mixed={int(row.mixed_unit)} "
            f"lift={int(row.yang_lift)} h90={int(row.h90_descent)} "
            f"finite={int(row.finite_theorem)} legal={int(row.legal_target)} "
            f"closes={int(row.source_stage_closed)}"
        )
        print(f"    shape={row.shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  source_closing_rows={contract.source_closing_rows}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  reject_rows={contract.reject_rows}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print("interpretation")
    print("  mixed_unit_identity_is_not_a_source_close=1")
    print("  yang_lift_without_h90_boundary_is_repair=1")
    print("  yang_h90_source_without_finite_theorem_is_repair=1")
    print("  projection_suborbit_or_wrong_boundary_lift_is_reject=1")
    print(f"p25_v2_yang_lift_descent_boundary_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Submission/extraction contract for the v2 unified p25 theorem target.

This gate is deliberately fast.  It does not rerun the heavy exact-P or
H0/conductor-39 producer screens; it checks the promoted evidence markers and
records the downstream DANGER3 obligations that still separate a source-stage
theorem from a submission-ready `(p,A,x0)` triple.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt
from pathlib import Path


P25 = 10**25 + 13
X16_LEVEL = 16
ODD_LEVEL = 507
CROSS_LEVEL = 8112
ACTIVE_MODE = "x16halvenonsplit"
START_DEPTH = 4
FINAL_DEPTH = 42


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SubmissionLadderRow:
    step: int
    name: str
    accepted_payload: str
    current_state: str
    first_missing_clause: str
    current_satisfied: bool
    contract_defined: bool
    ok: bool


@dataclass(frozen=True)
class UnifiedSubmissionExtractionContract:
    p: int
    p_mod_8: int
    k: int
    active_mode: str
    x16_level: int
    odd_level: int
    cross_level: int
    inv_507_mod_16: int
    inv_16_mod_507: int
    normalized_p16_multiplier: int
    normalized_q507_multiplier: int
    normalized_projection_sum_mod_8112: int
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    evidence_markers: tuple[EvidenceMarker, ...]
    ladder_rows: tuple[SubmissionLadderRow, ...]
    evidence_markers_ok: int
    contract_rows_defined: int
    current_satisfied_rows: int
    submission_ready_rows_now: int
    source_theorem_still_missing: bool
    extraction_payload_still_missing: bool
    exactp_is_upstream_not_submission: bool
    row_ok: bool


def compute_k(p: int) -> int:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return bound.bit_length()


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    ok = p.exists() and p.stat().st_size > 0 and needle in p.read_text()
    return EvidenceMarker(name=name, path=p, marker=needle, ok=ok)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_h0_conductor39_target",
            "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
            "p25_v2_h0_conductor39_unified_target_rows=1/1",
        ),
        marker(
            "exactp_to_unified_spine",
            "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
            "p25_v2_exactp_to_unified_target_spine_rows=1/1",
        ),
        marker(
            "h0_theorem_interface",
            "research/p25/evidence/p25_v2_h0_theorem_interface_contract_20260616.md",
            "All nine gates returned their expected `rows=1/1` markers",
        ),
        marker(
            "conductor39_yang_h90_interface",
            "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
            "All seven gates returned their expected `rows=1/1` markers",
        ),
        marker(
            "h0_x18112_bridge_payload",
            "research/p25/archive/notes/p25_ksy_y_h0_x18112_bridge_payload_contract_20260614.md",
            "ksy_y_h0_x18112_bridge_payload_contract_rows=1/1",
        ),
        marker(
            "x1_16_montgomery_chart",
            "research/p25/archive/notes/p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
            "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
        ),
        marker(
            "x1_16_halving_certificate",
            "research/p25/archive/notes/p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
            "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
        ),
        marker(
            "danger3_extraction_surface",
            "research/p25/archive/notes/p25_ksy_y_danger3_extraction_surface_20260614.md",
            "ksy_y_danger3_extraction_surface_rows=1/1",
        ),
        marker(
            "conductor39_to_danger3_ladder",
            "research/p25/archive/notes/p25_ksy_y_conductor39_to_danger3_acceptance_ladder_20260614.md",
            "ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1",
        ),
    )


def ladder_rows() -> tuple[SubmissionLadderRow, ...]:
    return (
        SubmissionLadderRow(
            step=1,
            name="source_stage_theorem",
            accepted_payload=(
                "finite value/divisor theorem for one unified support-156 "
                "H0/conductor-39 product, or stronger exact-P upstream theorem"
            ),
            current_state="target identified; theorem not found",
            first_missing_clause="source-stage finite value/divisor theorem",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
        SubmissionLadderRow(
            step=2,
            name="danger3_framing",
            accepted_payload="DANGER3 finite-identity/non-CM framing for the theorem hit",
            current_state="policy/framing boundary defined; no theorem to frame yet",
            first_missing_clause="DANGER3 framing after source theorem",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
        SubmissionLadderRow(
            step=3,
            name="same_j_x18112_bridge",
            accepted_payload=(
                "same-curve P16/Q507 pair, or order-8112 generator R with "
                "P16=[1521]R and Q507=[6592]R"
            ),
            current_state="bridge payload contract defined; no live bridge values",
            first_missing_clause="same-j X_1(8112) bridge or equivalent fiber product",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
        SubmissionLadderRow(
            step=4,
            name="practical_x1_16_surface",
            accepted_payload="X_1(16) y plus model root x, hence A and xP16, or direct A,xP16",
            current_state="active chart contract defined; no extracted A,xP16",
            first_missing_clause="practical X_1(16) chart specialization",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
        SubmissionLadderRow(
            step=5,
            name="halving_or_direct_x0",
            accepted_payload=(
                "39-point x-coordinate chain x4=xP16 to x42=x0, active "
                "sqrt-witness chain, or direct A,x0"
            ),
            current_state="checkable certificate shape defined; no p25 x-chain/x0",
            first_missing_clause="halving chain or concrete x0",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
        SubmissionLadderRow(
            step=6,
            name="official_vpp_boundary",
            accepted_payload="official src/vpp.py verifies concrete p25 (p,A,x0)",
            current_state="submission boundary defined; no verified p25 triple",
            first_missing_clause="official vpp.py verification",
            current_satisfied=False,
            contract_defined=True,
            ok=True,
        ),
    )


def profile_unified_submission_extraction_contract() -> UnifiedSubmissionExtractionContract:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    normalized_p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    normalized_q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    projection_sum = (normalized_p16 + normalized_q507) % CROSS_LEVEL
    markers = evidence_markers()
    rows = ladder_rows()
    markers_ok = sum(row.ok for row in markers)
    contracts_defined = sum(row.contract_defined for row in rows)
    satisfied = sum(row.current_satisfied for row in rows)
    submission_ready_now = sum(
        row.name == "official_vpp_boundary" and row.current_satisfied for row in rows
    )
    source_missing = not rows[0].current_satisfied
    extraction_missing = not any(
        row.name in {"halving_or_direct_x0", "official_vpp_boundary"}
        and row.current_satisfied
        for row in rows
    )
    exactp_upstream = (
        markers[1].ok
        and "exact-P upstream theorem" in rows[0].accepted_payload
        and not rows[0].current_satisfied
    )

    row_ok = (
        P25 == 10**25 + 13
        and P25 % 8 == 5
        and compute_k(P25) == 42
        and ACTIVE_MODE == "x16halvenonsplit"
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CROSS_LEVEL == 8112
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and inv_507 == 3
        and inv_16 == 412
        and normalized_p16 == 1521
        and normalized_q507 == 6592
        and projection_sum == 1
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and FINAL_DEPTH - START_DEPTH == 38
        and FINAL_DEPTH - START_DEPTH + 1 == 39
        and len(markers) == 9
        and markers_ok == 9
        and len(rows) == 6
        and contracts_defined == 6
        and satisfied == 0
        and submission_ready_now == 0
        and source_missing
        and extraction_missing
        and exactp_upstream
        and all(row.ok for row in rows)
    )

    return UnifiedSubmissionExtractionContract(
        p=P25,
        p_mod_8=P25 % 8,
        k=compute_k(P25),
        active_mode=ACTIVE_MODE,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        cross_level=CROSS_LEVEL,
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        normalized_p16_multiplier=normalized_p16,
        normalized_q507_multiplier=normalized_q507,
        normalized_projection_sum_mod_8112=projection_sum,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=FINAL_DEPTH - START_DEPTH,
        x_chain_points=FINAL_DEPTH - START_DEPTH + 1,
        evidence_markers=markers,
        ladder_rows=rows,
        evidence_markers_ok=markers_ok,
        contract_rows_defined=contracts_defined,
        current_satisfied_rows=satisfied,
        submission_ready_rows_now=submission_ready_now,
        source_theorem_still_missing=source_missing,
        extraction_payload_still_missing=extraction_missing,
        exactp_is_upstream_not_submission=exactp_upstream,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_unified_submission_extraction_contract()
    print("p25 v2 unified submission/extraction contract gate")
    print("arithmetic")
    print(f"  p={profile.p}")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  k={profile.k}")
    print(f"  active_mode={profile.active_mode}")
    print("x18112_projection")
    print(f"  x16_level={profile.x16_level}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  cross_level={profile.cross_level}")
    print(f"  inv_507_mod_16={profile.inv_507_mod_16}")
    print(f"  inv_16_mod_507={profile.inv_16_mod_507}")
    print(f"  normalized_p16_multiplier={profile.normalized_p16_multiplier}")
    print(f"  normalized_q507_multiplier={profile.normalized_q507_multiplier}")
    print(
        "  normalized_projection_sum_mod_8112="
        f"{profile.normalized_projection_sum_mod_8112}"
    )
    print("halving")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print("evidence_markers")
    for row in profile.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} path={row.path}")
    print("submission_ladder")
    for row in profile.ladder_rows:
        print(
            "  "
            f"{row.step}. {row.name}: satisfied={int(row.current_satisfied)} "
            f"defined={int(row.contract_defined)} missing={row.first_missing_clause}"
        )
        print(f"     accepts={row.accepted_payload}")
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}")
    print(f"  contract_rows_defined={profile.contract_rows_defined}")
    print(f"  current_satisfied_rows={profile.current_satisfied_rows}")
    print(f"  submission_ready_rows_now={profile.submission_ready_rows_now}")
    print("interpretation")
    print(
        "  unified_or_exactp_theorem_hit_is_not_submission_without_extraction=1"
    )
    print("  exactp_is_upstream_route_not_a_direct_DANGER3_payload=1")
    print("  same_j_X1_8112_then_X1_16_then_halving_then_vpp_is_required=1")
    print("  no_current_p25_submission_ready_payload=1")
    print(f"p25_v2_unified_submission_extraction_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("unified submission/extraction contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

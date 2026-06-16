#!/usr/bin/env python3
"""External halving/direct-x0 extraction work order after X_1(16) surface.

The external specialization work order reaches the active X_1(16) production
surface for ten bridge/surface variants.  This gate attaches each variant to
the accepted extraction payloads: a checkable x-coordinate chain, an active-path
sqrt-witness chain, or a direct A,x0 payload.  All three are extraction payloads
only after official vpp.py verification; none is current submission evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_x16_specialization_work_order_gate import (
    ExternalX16SpecializationWorkRow,
    profile_external_x16_specialization_work_order,
)
from p25_ksy_y_official_vpp_submission_archive_contract_gate import (
    profile_vpp_submission_archive_contract,
)
from p25_ksy_y_post_surface_halving_vpp_intake_gate import (
    profile_post_surface_halving_vpp_intake,
)
from p25_ksy_y_x1_16_halving_certificate_payload_gate import (
    CertificatePayloadRow,
    profile_halving_certificate_payload_contract,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_x16_specialization_work_order_20260614.md",
        "ksy_y_external_x16_specialization_work_order_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
        "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_post_surface_halving_vpp_intake_20260614.md",
        "ksy_y_post_surface_halving_vpp_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_official_vpp_submission_archive_contract_20260614.md",
        "ksy_y_official_vpp_submission_archive_contract_rows=1/1",
    ),
)

EXTRACTION_VARIANTS = (
    "x_coordinate_chain",
    "sqrt_witness_chain",
    "direct_A_x0",
)


@dataclass(frozen=True)
class ExternalHalvingExtractionWorkRow:
    name: str
    source_specialization_name: str
    source_lane: str
    odd_payload_object: str
    surface_payload_variant: str
    extraction_variant: str
    accepted_shape: str
    decision: str
    first_missing_clause: str
    extraction_ready: bool
    requires_official_vpp: bool
    supplies_active_branch_provenance: bool
    exact75: bool
    curved_corner: bool
    current_evidence: bool
    current_submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExternalHalvingExtractionWorkOrder:
    dependency_markers_present: int
    dependency_markers_total: int
    specialization_work_order_ok: bool
    halving_certificate_contract_ok: bool
    post_surface_halving_vpp_intake_ok: bool
    vpp_archive_contract_ok: bool
    rows: tuple[ExternalHalvingExtractionWorkRow, ...]
    row_count: int
    source_surface_rows: int
    frontdoor_count: int
    x_coordinate_chain_rows: int
    sqrt_witness_chain_rows: int
    direct_A_x0_rows: int
    active_branch_provenance_rows: int
    extraction_ready_rows: int
    requires_official_vpp_rows: int
    exact75_rows: int
    curved_corner_rows: int
    current_evidence_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def payload_by_name(
    rows: tuple[CertificatePayloadRow, ...],
    name: str,
) -> CertificatePayloadRow:
    for row in rows:
        if row.name == name:
            return row
    raise KeyError(name)


def accepted_shape_for(payload: CertificatePayloadRow) -> str:
    if payload.name == "x_coordinate_chain":
        return "A,xP16 plus x_4=xP16 through x_42=x0 with checkable xDBL links"
    if payload.name == "sqrt_witness_chain":
        return "A,xP16 plus square-root witnesses and active branch provenance to x0"
    if payload.name == "direct_A_x0":
        return "direct concrete A,x0 payload"
    return "unsupported extraction payload"


def work_row(
    surface: ExternalX16SpecializationWorkRow,
    payload: CertificatePayloadRow,
) -> ExternalHalvingExtractionWorkRow:
    extraction_ready = payload.decision in {
        "checkable_x_chain_vpp_missing",
        "active_path_provenance_vpp_missing",
        "direct_x0_vpp_missing",
    }
    requires_vpp = payload.first_missing_clause == "official vpp.py verification"
    ok = (
        surface.ok
        and surface.surface_decision.decision == "active_surface_reached_halving_missing"
        and payload.ok
        and extraction_ready
        and requires_vpp
        and not payload.supplies_vpp_verified
        and not surface.current_evidence
        and not surface.current_submission_ready
    )
    return ExternalHalvingExtractionWorkRow(
        name=f"{surface.name}_{payload.name}",
        source_specialization_name=surface.name,
        source_lane=surface.source_lane,
        odd_payload_object=surface.odd_payload_object,
        surface_payload_variant=surface.payload_variant,
        extraction_variant=payload.name,
        accepted_shape=accepted_shape_for(payload),
        decision=payload.decision,
        first_missing_clause=payload.first_missing_clause,
        extraction_ready=extraction_ready,
        requires_official_vpp=requires_vpp,
        supplies_active_branch_provenance=payload.supplies_active_branch_provenance,
        exact75=surface.exact75,
        curved_corner=surface.curved_corner,
        current_evidence=False,
        current_submission_ready=False,
        ok=ok,
    )


def work_rows(
    surfaces: tuple[ExternalX16SpecializationWorkRow, ...],
    payloads: tuple[CertificatePayloadRow, ...],
) -> tuple[ExternalHalvingExtractionWorkRow, ...]:
    selected_payloads = tuple(payload_by_name(payloads, name) for name in EXTRACTION_VARIANTS)
    rows: list[ExternalHalvingExtractionWorkRow] = []
    for surface in surfaces:
        for payload in selected_payloads:
            rows.append(work_row(surface, payload))
    return tuple(rows)


def profile_external_halving_extraction_work_order() -> ExternalHalvingExtractionWorkOrder:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    specialization = profile_external_x16_specialization_work_order()
    certificate = profile_halving_certificate_payload_contract()
    post_surface = profile_post_surface_halving_vpp_intake()
    archive = profile_vpp_submission_archive_contract()
    rows = work_rows(specialization.rows, certificate.payload_rows)
    source_surfaces = len({row.source_specialization_name for row in rows})
    frontdoors = len({row.source_lane for row in rows})
    x_chain = sum(row.extraction_variant == "x_coordinate_chain" for row in rows)
    sqrt_witness = sum(row.extraction_variant == "sqrt_witness_chain" for row in rows)
    direct = sum(row.extraction_variant == "direct_A_x0" for row in rows)
    active_provenance = sum(row.supplies_active_branch_provenance for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    requires_vpp = sum(row.requires_official_vpp for row in rows)
    exact75 = sum(row.exact75 for row in rows)
    curved = sum(row.curved_corner for row in rows)
    current = sum(row.current_evidence for row in rows)
    submission = sum(row.current_submission_ready for row in rows)
    variants = tuple(row.extraction_variant for row in rows[:3])
    decisions = tuple(row.decision for row in rows[:3])
    expected_decisions = (
        "checkable_x_chain_vpp_missing",
        "active_path_provenance_vpp_missing",
        "direct_x0_vpp_missing",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and specialization.row_ok
        and specialization.row_count == 10
        and certificate.row_ok
        and post_surface.row_ok
        and archive.row_ok
        and archive.current_submission_ready_rows == 0
        and len(rows) == 30
        and source_surfaces == 10
        and frontdoors == 5
        and x_chain == 10
        and sqrt_witness == 10
        and direct == 10
        and active_provenance == 10
        and extraction == 30
        and requires_vpp == 30
        and exact75 == 6
        and curved == 6
        and current == 0
        and submission == 0
        and variants == EXTRACTION_VARIANTS
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return ExternalHalvingExtractionWorkOrder(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        specialization_work_order_ok=specialization.row_ok,
        halving_certificate_contract_ok=certificate.row_ok,
        post_surface_halving_vpp_intake_ok=post_surface.row_ok,
        vpp_archive_contract_ok=archive.row_ok,
        rows=rows,
        row_count=len(rows),
        source_surface_rows=source_surfaces,
        frontdoor_count=frontdoors,
        x_coordinate_chain_rows=x_chain,
        sqrt_witness_chain_rows=sqrt_witness,
        direct_A_x0_rows=direct,
        active_branch_provenance_rows=active_provenance,
        extraction_ready_rows=extraction,
        requires_official_vpp_rows=requires_vpp,
        exact75_rows=exact75,
        curved_corner_rows=curved,
        current_evidence_rows=current,
        current_submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_halving_extraction_work_order()
    print("p25 KSY-y external halving/direct-x0 extraction work-order gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  specialization_work_order_ok={int(profile.specialization_work_order_ok)}")
    print(f"  halving_certificate_contract_ok={int(profile.halving_certificate_contract_ok)}")
    print(f"  post_surface_halving_vpp_intake_ok={int(profile.post_surface_halving_vpp_intake_ok)}")
    print(f"  vpp_archive_contract_ok={int(profile.vpp_archive_contract_ok)}")
    print("work_order_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: lane={row.source_lane} odd={row.odd_payload_object} "
            f"surface={row.surface_payload_variant} extraction={row.extraction_variant} "
            f"decision={row.decision} extraction_ready={int(row.extraction_ready)} "
            f"requires_vpp={int(row.requires_official_vpp)} "
            f"active_branch={int(row.supplies_active_branch_provenance)} "
            f"exact75={int(row.exact75)} curved={int(row.curved_corner)} "
            f"current={int(row.current_evidence)} "
            f"submission={int(row.current_submission_ready)}"
        )
        print(f"    accepted={row.accepted_shape}")
        print(f"    missing={row.first_missing_clause}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_surface_rows={profile.source_surface_rows}")
    print(f"  frontdoor_count={profile.frontdoor_count}")
    print(f"  x_coordinate_chain_rows={profile.x_coordinate_chain_rows}")
    print(f"  sqrt_witness_chain_rows={profile.sqrt_witness_chain_rows}")
    print(f"  direct_A_x0_rows={profile.direct_A_x0_rows}")
    print(f"  active_branch_provenance_rows={profile.active_branch_provenance_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  requires_official_vpp_rows={profile.requires_official_vpp_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  curved_corner_rows={profile.curved_corner_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  each_external_X16_surface_has_x_chain_sqrt_witness_and_direct_x0_acceptance_shapes=1")
    print("  extraction_payloads_still_require_official_vpp_and_archive=1")
    print("  current_submission_ready_rows_remain_zero=1")
    print(
        "ksy_y_external_halving_extraction_work_order_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external halving extraction work-order regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

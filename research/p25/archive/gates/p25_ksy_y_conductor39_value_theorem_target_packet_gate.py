#!/usr/bin/env python3
"""Theorem-facing target packet after the conductor-39 source certificate.

The source certificate stack proves the conductor-39 source is a real, legal,
mixed X_1(39) object.  This gate names the next theorem targets precisely:
which finite objects would close the value/divisor theorem stage, and which
downstream DANGER3 extraction obligations would still remain.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research" / "p25"
SOURCE_STACK = RESEARCH / "p25_ksy_y_conductor39_source_certificate_stack_20260614.md"
BRIDGE_SPINE = RESEARCH / "p25_ksy_y_yang_ksy_product_h90_bridge_spine_20260614.md"
SOURCE_STACK_MARKER = "ksy_y_conductor39_source_certificate_stack_rows=1/1"
BRIDGE_SPINE_MARKER = "ksy_y_yang_ksy_product_h90_bridge_spine_rows=1/1"
COUNT_LADDER = (75, 300, 12, 312, 156)
CANONICAL_H0_POSITIVE_RESIDUES = (7, 17, 23, 34, 37, 38)
CANONICAL_H0_NEGATIVE_RESIDUES = (4, 8, 10, 11, 20, 25)
SOURCE_CERTIFIED_ROWS = 6
DIRECT_VALUE_THEOREM_ROWS = 0
H90_BOUNDARY_OK = True
BRIDGE_DIRECT_CLOSER = False


@dataclass(frozen=True)
class ValueTheoremTargetRow:
    name: str
    object_family: str
    support_or_factor_count: int
    source_certified: bool
    bridge_spine_stage: str
    accepted_theorem_shape: str
    rejected_near_miss: str
    theorem_closes_value_stage: bool
    still_needs_danger3_framing: bool
    still_needs_extraction: bool
    still_needs_vpp: bool
    ok: bool


@dataclass(frozen=True)
class ValueTheoremPacketRouteRow:
    name: str
    decision: str
    value_theorem_target_ready: bool
    theorem_source_closed: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class Conductor39ValueTheoremTargetPacket:
    source_stack_ok: bool
    bridge_spine_ok: bool
    count_ladder: tuple[int, int, int, int, int]
    canonical_h0_positive_residues: tuple[int, ...]
    canonical_h0_negative_residues: tuple[int, ...]
    target_rows: tuple[ValueTheoremTargetRow, ...]
    route_rows: tuple[ValueTheoremPacketRouteRow, ...]
    target_ready_rows: int
    theorem_closing_shapes: int
    rejected_near_miss_rows: int
    danger3_remaining_rows: int
    extraction_remaining_rows: int
    submission_ready_rows: int
    positive_payload: str
    remaining_upgrade: str
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def target_rows() -> tuple[ValueTheoremTargetRow, ...]:
    return (
        ValueTheoremTargetRow(
            name="conductor39_U_chi_value_or_divisor",
            object_family="U_chi=-chi_39 on X_1(39)",
            support_or_factor_count=24,
            source_certified=True,
            bridge_spine_stage="source certificate before Yang lift",
            accepted_theorem_shape=(
                "finite-field value/divisor identity for U_chi with Frobenius "
                "anti-invariance or Hilbert-90 descent context"
            ),
            rejected_near_miss="Koo-Shin 6.2 source product alone or Koo-Shin 9.x ray-class generation",
            theorem_closes_value_stage=True,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            still_needs_vpp=True,
            ok=True,
        ),
        ValueTheoremTargetRow(
            name="period_norm_W_or_Norm156_Y507",
            object_family="W=6*U_chi and Norm_156(Y_507)",
            support_or_factor_count=312,
            source_certified=True,
            bridge_spine_stage="12-term Y_507 to 312-cell period norm",
            accepted_theorem_shape=(
                "finite-field value/divisor identity identifying the Yang "
                "13-fiber lift of W with Norm_156(Y_507)"
            ),
            rejected_near_miss="level-507 story without conductor-39 descent or period-156 context",
            theorem_closes_value_stage=True,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            still_needs_vpp=True,
            ok=True,
        ),
        ValueTheoremTargetRow(
            name="canonical_H0_or_translate",
            object_family="legal sparse Hilbert-90 preimage H0",
            support_or_factor_count=156,
            source_certified=True,
            bridge_spine_stage="312-cell period norm to 78-over-78 H0",
            accepted_theorem_shape=(
                "finite-field value/divisor identity for canonical H0 or any "
                "<2>-translate, with (1-Frob_p)H0=Norm_156(Y_507)"
            ),
            rejected_near_miss="formal one-coset H, missing boundary, or ambient-period value",
            theorem_closes_value_stage=True,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            still_needs_vpp=True,
            ok=True,
        ),
        ValueTheoremTargetRow(
            name="exact_P_or_Y507_bridge_identity",
            object_family="75-atom exact P or 12-term Y_507",
            support_or_factor_count=75,
            source_certified=True,
            bridge_spine_stage="75 fixed atoms to 12-term Y_507",
            accepted_theorem_shape=(
                "exact divisor/additive identity for P, or finite-field value "
                "identity for Y_507 carrying the 75->300->12 bridge"
            ),
            rejected_near_miss="formula language, field generation, or C169 projection without mixed graph",
            theorem_closes_value_stage=True,
            still_needs_danger3_framing=True,
            still_needs_extraction=True,
            still_needs_vpp=True,
            ok=True,
        ),
    )


def route_rows() -> tuple[ValueTheoremPacketRouteRow, ...]:
    return (
        ValueTheoremPacketRouteRow(
            name="source_certificate_only",
            decision="target_ready_value_theorem_missing",
            value_theorem_target_ready=True,
            theorem_source_closed=False,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="finite-field value/divisor theorem for a target row",
            ok=True,
        ),
        ValueTheoremPacketRouteRow(
            name="target_value_theorem_without_danger3",
            decision="source_theorem_closed_policy_or_framing_missing",
            value_theorem_target_ready=True,
            theorem_source_closed=True,
            danger3_unblocked=False,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            ok=True,
        ),
        ValueTheoremPacketRouteRow(
            name="danger3_framed_value_theorem",
            decision="danger3_unblocked_extraction_missing",
            value_theorem_target_ready=True,
            theorem_source_closed=True,
            danger3_unblocked=True,
            extraction_ready=False,
            submission_ready=False,
            first_missing_clause="map theorem payload to X_1(16) surface and concrete x0",
            ok=True,
        ),
        ValueTheoremPacketRouteRow(
            name="extracted_unverified_triple",
            decision="ready_to_extract_and_verify_concrete_triple",
            value_theorem_target_ready=True,
            theorem_source_closed=True,
            danger3_unblocked=True,
            extraction_ready=True,
            submission_ready=False,
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        ValueTheoremPacketRouteRow(
            name="vpp_verified_triple",
            decision="submission_ready",
            value_theorem_target_ready=True,
            theorem_source_closed=True,
            danger3_unblocked=True,
            extraction_ready=True,
            submission_ready=True,
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_conductor39_value_theorem_target_packet() -> Conductor39ValueTheoremTargetPacket:
    source_stack_ok = marker_present(SOURCE_STACK, SOURCE_STACK_MARKER)
    bridge_spine_ok = marker_present(BRIDGE_SPINE, BRIDGE_SPINE_MARKER)
    targets = target_rows()
    routes = route_rows()
    count_ladder = COUNT_LADDER
    target_ready = sum(row.source_certified for row in targets)
    theorem_closing = sum(row.theorem_closes_value_stage for row in targets)
    rejected_near = sum(bool(row.rejected_near_miss) for row in targets)
    danger_remaining = sum(row.still_needs_danger3_framing for row in targets)
    extraction_remaining = sum(row.still_needs_extraction for row in targets)
    submission_ready = sum(row.submission_ready for row in routes)
    row_ok = (
        source_stack_ok
        and bridge_spine_ok
        and count_ladder == (75, 300, 12, 312, 156)
        and CANONICAL_H0_POSITIVE_RESIDUES == (7, 17, 23, 34, 37, 38)
        and CANONICAL_H0_NEGATIVE_RESIDUES == (4, 8, 10, 11, 20, 25)
        and len(targets) == 4
        and target_ready == 4
        and theorem_closing == 4
        and rejected_near == 4
        and danger_remaining == 4
        and extraction_remaining == 4
        and submission_ready == 1
        and tuple(row.decision for row in routes)
        == (
            "target_ready_value_theorem_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "ready_to_extract_and_verify_concrete_triple",
            "submission_ready",
        )
        and all(row.ok for row in targets)
        and all(row.ok for row in routes)
        and SOURCE_CERTIFIED_ROWS == 6
        and DIRECT_VALUE_THEOREM_ROWS == 0
        and H90_BOUNDARY_OK
        and BRIDGE_DIRECT_CLOSER is False
    )
    return Conductor39ValueTheoremTargetPacket(
        source_stack_ok=source_stack_ok,
        bridge_spine_ok=bridge_spine_ok,
        count_ladder=count_ladder,
        canonical_h0_positive_residues=CANONICAL_H0_POSITIVE_RESIDUES,
        canonical_h0_negative_residues=CANONICAL_H0_NEGATIVE_RESIDUES,
        target_rows=targets,
        route_rows=routes,
        target_ready_rows=target_ready,
        theorem_closing_shapes=theorem_closing,
        rejected_near_miss_rows=rejected_near,
        danger3_remaining_rows=danger_remaining,
        extraction_remaining_rows=extraction_remaining,
        submission_ready_rows=submission_ready,
        positive_payload=(
            "Four exact finite theorem targets are now named: U_chi/W, "
            "Norm_156(Y_507), canonical H0, and exact P/Y_507 bridge identities."
        ),
        remaining_upgrade=(
            "prove one finite-field value/divisor theorem, settle DANGER3 framing, "
            "extract X_1(16) A/x0, and verify with official vpp.py"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_conductor39_value_theorem_target_packet()
    print("p25 KSY-y conductor-39 value-theorem target packet gate")
    print("dependencies")
    print(f"  source_stack_ok={int(profile.source_stack_ok)}")
    print(f"  bridge_spine_ok={int(profile.bridge_spine_ok)}")
    print("fixed_payload")
    print(f"  count_ladder={profile.count_ladder}")
    print(f"  canonical_h0_positive_residues={profile.canonical_h0_positive_residues}")
    print(f"  canonical_h0_negative_residues={profile.canonical_h0_negative_residues}")
    print("target_rows")
    for row in profile.target_rows:
        print(
            "  "
            f"{row.name}: family={row.object_family} count={row.support_or_factor_count} "
            f"source={int(row.source_certified)} closes_value={int(row.theorem_closes_value_stage)} "
            f"danger3={int(row.still_needs_danger3_framing)} "
            f"extraction={int(row.still_needs_extraction)} "
            f"vpp={int(row.still_needs_vpp)} stage={row.bridge_spine_stage}"
        )
        print(f"    accept={row.accepted_theorem_shape}")
        print(f"    reject={row.rejected_near_miss}")
    print("route_rows")
    for row in profile.route_rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} target={int(row.value_theorem_target_ready)} "
            f"theorem={int(row.theorem_source_closed)} "
            f"danger3={int(row.danger3_unblocked)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  target_ready_rows={profile.target_ready_rows}")
    print(f"  theorem_closing_shapes={profile.theorem_closing_shapes}")
    print(f"  rejected_near_miss_rows={profile.rejected_near_miss_rows}")
    print(f"  danger3_remaining_rows={profile.danger3_remaining_rows}")
    print(f"  extraction_remaining_rows={profile.extraction_remaining_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  conductor39_value_theorem_targets_are_named_and_source_certified=1")
    print("  exact_theorem_hit_still_needs_danger3_and_extraction=1")
    print(f"  remaining_upgrade={profile.remaining_upgrade}")
    print(f"ksy_y_conductor39_value_theorem_target_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Conductor-39 value-theorem target packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

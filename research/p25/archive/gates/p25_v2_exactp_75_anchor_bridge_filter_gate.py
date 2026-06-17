#!/usr/bin/env python3
"""Separate row-power 75 anchors from exact-P 75-atom payloads."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1


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
    object_basis: str
    scalar_test: str
    accepted_if: str
    decision: str
    first_falsifier: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "common_scalar_anchor_filter",
        "evidence/p25_v2_common_scalar_anchor_filter_20260617.md",
        "p25_v2_common_scalar_anchor_filter_rows=1/1",
    ),
    EvidenceMarker(
        "extended_unique_power_intake",
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_finite_geometry_rigidity",
        "evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
        "p25_v2_exactp_finite_geometry_rigidity_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_minimal_hook",
        "evidence/p25_v2_exactp_minimal_hook_20260616.md",
        "p25_v2_exactp_minimal_hook_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_to_unified_target_spine",
        "evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
        "p25_v2_exactp_to_unified_target_spine_rows=1/1",
    ),
    EvidenceMarker(
        "reverse_exactp_information_loss",
        "evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
        "p25_v2_reverse_exactp_information_loss_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_theta2_lookup_row_status",
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
)


def bridge_rows() -> tuple[BridgeRow, ...]:
    return (
        BridgeRow(
            name="row_power_Rm75",
            object_basis="H0/conductor-39 legal row value R_m",
            scalar_test="gcd(75, p-1) = 1",
            accepted_if="exact row-labeled finite theorem for R_m^75 plus boundary or period bridge",
            decision="first_pass_anchor_after_inverse_exponent",
            first_falsifier="rowless 75-power, value up to scalar, or boundary-only powered divisor",
            ok=gcd(75, PM1) == 1,
        ),
        BridgeRow(
            name="equal_weight_75_atom_exactp",
            object_basis="exact-P normalized-y/theta2 atom basis",
            scalar_test="75 atoms have disjoint 4-cell supports and forced equal weights",
            accepted_if="challenge-legal exact 75-atom theorem with orientation and 75->300->12->312->156 bridge",
            decision="heavy_upstream_source_candidate_not_row_power_shortcut",
            first_falsifier="normalized-y vocabulary, finite fixture, nonuniform weights, or atom count without source",
            ok=True,
        ),
        BridgeRow(
            name="compact_cdk_orientation",
            object_basis="exact-P packet C,D,K plus one accepted orientation branch",
            scalar_test="orientation selects theta2 or theta2^-1 branch before bridge",
            accepted_if="arithmetic theorem emits compact packet and exact equal-weight payload",
            decision="heavy_upstream_source_candidate_route_to_unified_then_extraction",
            first_falsifier="branchless orientation word, wrong center, wrong D, or nonprimitive K",
            ok=True,
        ),
        BridgeRow(
            name="theta2_period156_payload",
            object_basis="theta2/theta2-inverse divisor-additive payload",
            scalar_test="period-156 branch is unique in F_p after accepted bridge",
            accepted_if="exact theta2 payload with period-156 branch/root/telescoping and bridge data",
            decision="heavy_upstream_or_value_bridge_candidate",
            first_falsifier="ambient-period-780 value, theta vocabulary, or Sprang D=2 support without sparse packet",
            ok=gcd(pow(4, 156) - 1, PM1) == 1,
        ),
        BridgeRow(
            name="unified_support156_to_exactp",
            object_basis="H0/conductor-39 support-156 target",
            scalar_test="not a reverse exact-P selector",
            accepted_if="explicit reverse reconstruction theorem supplies C,D,K/orientation or 75 atoms",
            decision="reject_reverse_without_extra_selector_structure",
            first_falsifier="unified value/divisor theorem alone or Y_507 bridge alone",
            ok=True,
        ),
        BridgeRow(
            name="atom_count_only",
            object_basis="phrase containing 75 atoms or C_75 without exact payload",
            scalar_test="gcd(75,p-1) is irrelevant without row or bridge basis",
            accepted_if="never by count alone",
            decision="repair_exact_theorem_and_orientation_missing",
            first_falsifier="75 vocabulary, ray-class generation, KL balance, or finite packet without source",
            ok=True,
        ),
    )


def main() -> int:
    rows = bridge_rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    exactp_heavy_candidates = sum("heavy" in row.decision for row in rows)
    first_pass_anchor_rows = sum(row.decision == "first_pass_anchor_after_inverse_exponent" for row in rows)
    reverse_reject_rows = sum(row.decision == "reject_reverse_without_extra_selector_structure" for row in rows)
    repair_rows = sum(row.decision == "repair_exact_theorem_and_orientation_missing" for row in rows)
    current_exactp_source_theorems = 0
    current_row_power_75_theorems = 0
    current_submission_ready = 0
    overall_ok = (
        gcd(75, PM1) == 1
        and gcd(pow(4, 156) - 1, PM1) == 1
        and markers_ok == len(EVIDENCE_MARKERS)
        and len(rows) == 6
        and all(row.ok for row in rows)
        and first_pass_anchor_rows == 1
        and exactp_heavy_candidates == 3
        and reverse_reject_rows == 1
        and repair_rows == 1
        and current_exactp_source_theorems == 0
        and current_row_power_75_theorems == 0
        and current_submission_ready == 0
    )

    print("p25 v2 exact-P 75-anchor bridge filter")
    print(f"p={P25}")
    print(f"gcd_75_pminus1={gcd(75, PM1)}")
    print(f"gcd_4pow156_minus1_pminus1={gcd(pow(4, 156) - 1, PM1)}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    object_basis={row.object_basis}")
        print(f"    scalar_test={row.scalar_test}")
        print(f"    accepted_if={row.accepted_if}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  bridge_rows={len(rows)}")
    print(f"  first_pass_anchor_rows={first_pass_anchor_rows}")
    print(f"  exactp_heavy_candidate_rows={exactp_heavy_candidates}")
    print(f"  reverse_reject_rows={reverse_reject_rows}")
    print(f"  repair_rows={repair_rows}")
    print(f"  current_exactp_source_theorems={current_exactp_source_theorems}")
    print(f"  current_row_power_75_theorems={current_row_power_75_theorems}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  row_power_75_is_not_equal_weight_75_atom_exactp=1")
    print("  exactp_75_atoms_need_orientation_and_bridge=1")
    print("  unified_support156_does_not_reverse_to_exactp_without_selector=1")
    print(f"p25_v2_exactp_75_anchor_bridge_filter_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("exact-P 75-anchor bridge filter failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

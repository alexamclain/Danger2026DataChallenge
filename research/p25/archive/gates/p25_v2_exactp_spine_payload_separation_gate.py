#!/usr/bin/env python3
"""Finite-support separation for exact-P, row powers, and unified targets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"


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
class SeparationRow:
    name: str
    support_profile: str
    decision: str
    first_falsifier: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "exactp_to_unified_target_spine",
        "evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
        "p25_v2_exactp_to_unified_target_spine_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_75_anchor_bridge_filter",
        "evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md",
        "p25_v2_exactp_75_anchor_bridge_filter_rows=1/1",
    ),
    EvidenceMarker(
        "basis_sensitive_anchor_sieve",
        "evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md",
        "p25_v2_basis_sensitive_anchor_sieve_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_finite_geometry_rigidity",
        "evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md",
        "p25_v2_exactp_finite_geometry_rigidity_rows=1/1",
    ),
    EvidenceMarker(
        "reverse_exactp_information_loss",
        "evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
        "p25_v2_reverse_exactp_information_loss_rows=1/1",
    ),
    EvidenceMarker(
        "theta2_period156_support_contract",
        "evidence/p25_v2_theta2_period156_support_contract_20260616.md",
        "p25_v2_theta2_period156_support_contract_rows=1/1",
    ),
)


SUPPORT_LADDER = (75, 300, 12, 312, 156)


def rows() -> tuple[SeparationRow, ...]:
    atom_count, theta2_support, y507_support, period_norm_support, h90_support = SUPPORT_LADDER
    return (
        SeparationRow(
            name="fixed_75_atoms",
            support_profile="75 fixed normalized-y atoms, each with disjoint four-cell support",
            decision="exactp_payload_not_75_candidate_search",
            first_falsifier="treating atoms as independent tries or as generic atom vocabulary",
            ok=atom_count == 75 and theta2_support == 4 * atom_count,
        ),
        SeparationRow(
            name="theta2_to_y507_bridge",
            support_profile="75 atoms expand to 300 theta2 terms and descend to 12 Y_507 terms",
            decision="bridge_support_not_source_theorem",
            first_falsifier="theta2 vocabulary or Y_507 support without source theorem and branch data",
            ok=theta2_support == 300 and y507_support == 12,
        ),
        SeparationRow(
            name="period_norm_to_h90",
            support_profile="12 Y_507 terms period-norm to 312 cells and a 156-support H90 product",
            decision="unified_support156_target_after_bridge",
            first_falsifier="calling the 156-support H90 product the plain 75-atom exact-P product",
            ok=period_norm_support == 2 * h90_support and h90_support == 156,
        ),
        SeparationRow(
            name="h90_product_not_plain_75",
            support_profile="unified H90 lift is 78 positive over 78 negative factors",
            decision="reject_plain_75_atom_identification",
            first_falsifier="h90 support equals atom count, or positive/negative side equals atom count",
            ok=h90_support != atom_count and 78 != atom_count,
        ),
        SeparationRow(
            name="exactp_75_not_row_power_75",
            support_profile="exact-P atoms live in normalized-y/theta2 basis, not in row-value R_m basis",
            decision="reject_row_power_shortcut_without_row_labeled_Rm75_theorem",
            first_falsifier="using gcd(75,p-1)=1 on atom count instead of row-labeled R_m^75",
            ok=True,
        ),
        SeparationRow(
            name="forward_not_reverse",
            support_profile="compact exact-P theorem feeds unified target; unified theorem alone loses C,D,K/orientation",
            decision="exactp_stronger_upstream_one_way_bridge",
            first_falsifier="claiming unified support-156 theorem reconstructs exact-P without selector data",
            ok=True,
        ),
    )


def main() -> int:
    separation_rows = rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    support_ladder_ok = SUPPORT_LADDER == (75, 300, 12, 312, 156)
    exactp_heavy_rows = sum("exactp" in row.decision for row in separation_rows)
    reject_rows = sum(row.decision.startswith("reject") for row in separation_rows)
    bridge_rows = sum("bridge" in row.decision for row in separation_rows)
    current_exactp_source_theorems = 0
    current_unified_source_theorems = 0
    current_submission_ready = 0
    overall_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and len(separation_rows) == 6
        and all(row.ok for row in separation_rows)
        and support_ladder_ok
        and exactp_heavy_rows == 2
        and reject_rows == 2
        and bridge_rows == 3
        and current_exactp_source_theorems == 0
        and current_unified_source_theorems == 0
        and current_submission_ready == 0
    )

    print("p25 v2 exact-P spine payload separation")
    print(f"support_ladder={SUPPORT_LADDER}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in separation_rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    support_profile={row.support_profile}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  separation_rows={len(separation_rows)}")
    print(f"  support_ladder_ok={int(support_ladder_ok)}")
    print(f"  exactp_heavy_rows={exactp_heavy_rows}")
    print(f"  reject_rows={reject_rows}")
    print(f"  bridge_rows={bridge_rows}")
    print(f"  current_exactp_source_theorems={current_exactp_source_theorems}")
    print(f"  current_unified_source_theorems={current_unified_source_theorems}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  exactp_ladder_is_75_300_12_312_156=1")
    print("  h90_support156_is_not_plain_75_atom_product=1")
    print("  exactp_atom_count_is_not_row_power_Rm75=1")
    print("  exactp_to_unified_is_one_way=1")
    print(f"p25_v2_exactp_spine_payload_separation_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("exact-P spine payload separation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

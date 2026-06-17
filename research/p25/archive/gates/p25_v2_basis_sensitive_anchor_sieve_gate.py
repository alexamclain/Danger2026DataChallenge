#!/usr/bin/env python3
"""Basis-sensitive intake sieve for p25 row-anchor claims."""

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
class SieveRow:
    name: str
    object_basis: str
    selector_test: str
    scalar_or_branch_test: str
    accepted_input: str
    decision: str
    first_falsifier: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "edge_lattice_global_minimality",
        "evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
        "p25_v2_edge_lattice_global_minimality_rows=1/1",
    ),
    EvidenceMarker(
        "row_value_reconstruction_basis",
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    EvidenceMarker(
        "common_scalar_anchor_filter",
        "evidence/p25_v2_common_scalar_anchor_filter_20260617.md",
        "p25_v2_common_scalar_anchor_filter_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_75_anchor_bridge_filter",
        "evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md",
        "p25_v2_exactp_75_anchor_bridge_filter_rows=1/1",
    ),
    EvidenceMarker(
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_branch_contract",
        "evidence/p25_v2_period156_value_branch_contract_20260616.md",
        "p25_v2_period156_value_branch_contract_rows=1/1",
    ),
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
)


def rows() -> tuple[SieveRow, ...]:
    return (
        SieveRow(
            name="legal_unit_edge_row",
            object_basis="H0/conductor-39 four-row edge lattice",
            selector_test="coefficient vector is one of e1,e2,e4,e8",
            scalar_or_branch_test="coefficient sum 1 and gcd(1,p-1)=1",
            accepted_input="exact finite source theorem for one oriented legal row",
            decision="first_pass_source_stage_candidate_if_theorem_present",
            first_falsifier="source legality only, no finite scalar-fixed theorem, or no extraction route",
            ok=True,
        ),
        SieveRow(
            name="sum_one_nonunit_row_vector",
            object_basis="H0/conductor-39 four-row edge lattice",
            selector_test="coefficient sum 1 but L1 norm >= 3",
            scalar_or_branch_test="common scalar is visible but boundary-zero selector debt remains",
            accepted_input="nonunit W-boundary theorem plus exact boundary-zero values, or direct unit edge",
            decision="repair_edge_plus_zero_lattice_content",
            first_falsifier="treating any W-boundary vector as one legal row",
            ok=True,
        ),
        SieveRow(
            name="zero_lattice_or_quotient",
            object_basis="H0/conductor-39 four-row edge lattice",
            selector_test="coefficient sum 0",
            scalar_or_branch_test="common F_p^* scalar is invisible",
            accepted_input="transfer data after a row anchor is already known",
            decision="transfer_only_not_first_anchor",
            first_falsifier="quotient/H90 relation presented as first absolute row value",
            ok=True,
        ),
        SieveRow(
            name="row_labeled_unique_power",
            object_basis="H0/conductor-39 legal row value R_m",
            selector_test="one oriented legal row is named",
            scalar_or_branch_test="gcd(e,p-1)=1 for e in {3,5,13,39,75,169,507}",
            accepted_input="exact finite source theorem for R_m^e plus accepted boundary or period bridge",
            decision="normalize_by_inverse_exponent_then_first_pass_intake",
            first_falsifier="rowless power, value up to scalar, boundary-only powered divisor",
            ok=all(gcd(e, PM1) == 1 for e in (3, 5, 13, 39, 75, 169, 507)),
        ),
        SieveRow(
            name="period156_row_value",
            object_basis="support-period-156 value with legal-row bridge",
            selector_test="canonical H0/Y507 or one legal row bridge is supplied",
            scalar_or_branch_test="gcd(4^156-1,p-1)=1",
            accepted_input="finite period-156 value theorem with branch/root/telescoping or additive normalization",
            decision="period_branch_normalized_first_pass_intake",
            first_falsifier="ambient-period value, class-field generation, or value up to scalar",
            ok=gcd(pow(4, 156) - 1, PM1) == 1,
        ),
        SieveRow(
            name="ambient_period780_value",
            object_basis="ambient value without period-156 row branch",
            selector_test="no selected support-period-156 row branch",
            scalar_or_branch_test="gcd(4^780-1,p-1)=11",
            accepted_input="needs period-156 branch/root/telescoping or additive normalization first",
            decision="repair_eleven_branch_ambiguity",
            first_falsifier="mu_11 quotient or ambient-period value treated as one F_p row value",
            ok=gcd(pow(4, 780) - 1, PM1) == 11,
        ),
        SieveRow(
            name="exactp_equal_weight_atoms",
            object_basis="exact-P normalized-y/theta2 75-atom basis",
            selector_test="C,D,K plus accepted orientation, or exact equal-weight 75 atoms",
            scalar_or_branch_test="not a row-lattice coefficient-sum test",
            accepted_input="challenge-legal exact-P theorem with 75->300->12->312->156 bridge",
            decision="heavy_upstream_candidate_not_first_pass_row_shortcut",
            first_falsifier="75 atom count, finite fixture, KL balance, or normalized-y vocabulary only",
            ok=True,
        ),
        SieveRow(
            name="unified_support156_reverse_exactp",
            object_basis="unified H0/conductor-39 support-156 target",
            selector_test="one support-156 row theorem may route to extraction",
            scalar_or_branch_test="does not reconstruct exact-P orientation or atoms",
            accepted_input="explicit reverse theorem supplying C,D,K/orientation, 75 atoms, or theta2 payload",
            decision="route_unified_hit_to_extraction_not_exactp_recovery",
            first_falsifier="Y_507 bridge or unified theorem alone called an exact-P theorem",
            ok=True,
        ),
    )


def main() -> int:
    sieve_rows = rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    first_pass_decisions = {
        "first_pass_source_stage_candidate_if_theorem_present",
        "normalize_by_inverse_exponent_then_first_pass_intake",
        "period_branch_normalized_first_pass_intake",
    }
    first_pass_candidates = sum(row.decision in first_pass_decisions for row in sieve_rows)
    repair_rows = sum(row.decision.startswith("repair") for row in sieve_rows)
    transfer_rows = sum("transfer_only" in row.decision for row in sieve_rows)
    heavy_rows = sum(row.decision.startswith("heavy") for row in sieve_rows)
    reverse_routes = sum(row.decision.startswith("route_unified") for row in sieve_rows)
    current_source_stage_closers = 0
    current_submission_ready = 0
    overall_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and len(sieve_rows) == 8
        and all(row.ok for row in sieve_rows)
        and first_pass_candidates == 3
        and repair_rows == 2
        and transfer_rows == 1
        and heavy_rows == 1
        and reverse_routes == 1
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 basis-sensitive anchor sieve")
    print(f"p={P25}")
    print(f"gcd_75_pminus1={gcd(75, PM1)}")
    print(f"gcd_4pow156_minus1_pminus1={gcd(pow(4, 156) - 1, PM1)}")
    print(f"gcd_4pow780_minus1_pminus1={gcd(pow(4, 780) - 1, PM1)}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in sieve_rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    object_basis={row.object_basis}")
        print(f"    selector_test={row.selector_test}")
        print(f"    scalar_or_branch_test={row.scalar_or_branch_test}")
        print(f"    accepted_input={row.accepted_input}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  sieve_rows={len(sieve_rows)}")
    print(f"  first_pass_candidate_rows={first_pass_candidates}")
    print(f"  repair_rows={repair_rows}")
    print(f"  transfer_only_rows={transfer_rows}")
    print(f"  heavy_upstream_rows={heavy_rows}")
    print(f"  reverse_route_rows={reverse_routes}")
    print(f"  current_source_stage_closers={current_source_stage_closers}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  identify_object_basis_before_scalar_tests=1")
    print("  coefficient_sum_one_requires_unit_edge_or_zero_lattice_repair=1")
    print("  exactp_atom_count_is_not_row_power=1")
    print(f"p25_v2_basis_sensitive_anchor_sieve_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("basis-sensitive anchor sieve failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

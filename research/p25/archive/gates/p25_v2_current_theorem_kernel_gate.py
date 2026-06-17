#!/usr/bin/env python3
"""Current p25 theorem-kernel packet after the basis-sensitive filters."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
UNIQUE_ROW_POWERS = (3, 5, 13, 39, 75, 169, 507)


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
class KernelRow:
    name: str
    object_required: str
    accepted_payload: str
    decision: str
    first_falsifier: str
    route: str
    ok: bool


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "self_contained_theorem_statement",
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    EvidenceMarker(
        "basis_sensitive_anchor_sieve",
        "evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md",
        "p25_v2_basis_sensitive_anchor_sieve_rows=1/1",
    ),
    EvidenceMarker(
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
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
        "period156_lookup_row_status",
        "evidence/p25_v2_period156_lookup_row_status_20260617.md",
        "p25_v2_period156_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_theta2_lookup_row_status",
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_spine_payload_separation",
        "evidence/p25_v2_exactp_spine_payload_separation_20260617.md",
        "p25_v2_exactp_spine_payload_separation_rows=1/1",
    ),
    EvidenceMarker(
        "q_yang_lookup_row_status",
        "evidence/p25_v2_q_yang_lookup_row_status_20260617.md",
        "p25_v2_q_yang_lookup_row_status_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_closure_packet",
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    EvidenceMarker(
        "unified_submission_extraction_contract",
        "evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
        "p25_v2_unified_submission_extraction_contract_rows=1/1",
    ),
)


def kernel_rows() -> tuple[KernelRow, ...]:
    return (
        KernelRow(
            name="unit_edge_divisor_additive",
            object_required="one exact oriented support-156 row R_m, m in {1,2,4,8}",
            accepted_payload="scalar-fixed finite divisor/additive theorem with Norm_156(Y_507) boundary",
            decision="primary_source_stage_candidate_if_theorem_present",
            first_falsifier="source legality, boundary-only, divisor class, or unspecified F_p^* scalar",
            route="source-stage normalization, then DANGER3 framing and extraction",
            ok=True,
        ),
        KernelRow(
            name="row_labeled_unique_power",
            object_required="one exact oriented row R_m plus exponent e in {3,5,13,39,75,169,507}",
            accepted_payload="exact finite source theorem for R_m^e with accepted boundary or period bridge",
            decision="normalize_by_inverse_exponent_then_source_stage",
            first_falsifier="rowless power, value up to scalar, or powered boundary without finite value",
            route="inverse exponent in F_p^*, then ordinary one-row intake",
            ok=all(gcd(exponent, PM1) == 1 for exponent in UNIQUE_ROW_POWERS),
        ),
        KernelRow(
            name="support_period156_value",
            object_required="canonical H0/Y_507 or one legal row with support-period-156 bridge",
            accepted_payload="finite value theorem with branch/root/telescoping or additive normalization",
            decision="period_branch_normalized_source_stage_candidate",
            first_falsifier="ambient-period-780 value, mu_11 quotient, or value up to scalar",
            route="period-156 value hook, then source-stage normalization",
            ok=gcd(pow(4, 156) - 1, PM1) == 1 and gcd(pow(4, 780) - 1, PM1) == 11,
        ),
        KernelRow(
            name="q_yang_support_route",
            object_required="mixed conductor-39 Q/Yang/H90 object tied to one legal row",
            accepted_payload="finite Q or Q^3 theorem plus selector debt paid by oriented split or direct row theorem",
            decision="support_route_only_until_selector_and_finite_theorem_present",
            first_falsifier="Q source language, Q^6 boundary, diagonal aggregate, or Q-square value without extraction map",
            route="period-156/Q lookup, then row normalizer if all debt is paid",
            ok=True,
        ),
        KernelRow(
            name="matched_quotient_aggregate_route",
            object_required="aggregate row product R^v plus target row m and exact matched zero-lattice quotient",
            accepted_payload="arithmetic theorem for R^v and arithmetic theorem for R^(v - (sum v)e_m), with gcd(sum v,p-1)=1",
            decision="support_route_only_until_matched_quotient_and_finite_theorems_present",
            first_falsifier="aggregate-only, quotient-only, unmatched quotient, zero-sum, or nonunit coefficient sum",
            route="matched quotient normalization, then inverse-power one-row intake",
            ok=True,
        ),
        KernelRow(
            name="exactp_theta2_upstream",
            object_required="compact C,D,K/orientation, equal-weight 75 atoms, or accepted theta2 payload",
            accepted_payload="arithmetic theorem carrying exact-P packet and 75->300->12->312->156 bridge",
            decision="heavy_upstream_candidate_if_exact_theorem_present",
            first_falsifier="75 vocabulary, normalized-y/KL/Sprang/theta context, finite fixture, or unified target alone",
            route="exact-P bridge into unified target, then extraction",
            ok=True,
        ),
        KernelRow(
            name="reverse_unified_to_exactp",
            object_required="unified support-156 theorem plus exact-P reverse selector data",
            accepted_payload="explicit reverse reconstruction to C,D,K/orientation, equal-weight atoms, or theta2 payload",
            decision="reject_without_extra_selector_structure",
            first_falsifier="unified support-156 value/divisor theorem or Y_507 bridge alone",
            route="unified theorem routes to extraction, not exact-P recovery",
            ok=True,
        ),
    )


def main() -> int:
    rows = kernel_rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    accepted_source_stage_rows = sum(
        row.decision
        in {
            "primary_source_stage_candidate_if_theorem_present",
            "normalize_by_inverse_exponent_then_source_stage",
            "period_branch_normalized_source_stage_candidate",
        }
        for row in rows
    )
    support_rows = sum("support_route" in row.decision for row in rows)
    heavy_rows = sum("heavy_upstream" in row.decision for row in rows)
    reject_rows = sum(row.decision.startswith("reject") for row in rows)
    current_source_stage_closers = 0
    current_submission_ready = 0
    overall_ok = (
        P25 % 8 == 5
        and markers_ok == len(EVIDENCE_MARKERS)
        and len(rows) == 7
        and all(row.ok for row in rows)
        and accepted_source_stage_rows == 3
        and support_rows == 2
        and heavy_rows == 1
        and reject_rows == 1
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 current theorem kernel")
    print(f"p={P25}")
    print(f"unique_row_powers={UNIQUE_ROW_POWERS}")
    print(f"gcd_4pow156_minus1_pminus1={gcd(pow(4, 156) - 1, PM1)}")
    print(f"gcd_4pow780_minus1_pminus1={gcd(pow(4, 780) - 1, PM1)}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    object_required={row.object_required}")
        print(f"    accepted_payload={row.accepted_payload}")
        print(f"    first_falsifier={row.first_falsifier}")
        print(f"    route={row.route}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  kernel_rows={len(rows)}")
    print(f"  accepted_source_stage_rows={accepted_source_stage_rows}")
    print(f"  support_rows={support_rows}")
    print(f"  heavy_upstream_rows={heavy_rows}")
    print(f"  reject_rows={reject_rows}")
    print(f"  current_source_stage_closers={current_source_stage_closers}")
    print(f"  current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  current_front_door_is_one_row_or_row_power_or_period156_value=1")
    print("  q_yang_is_support_until_selector_debt_paid=1")
    print("  matched_quotient_is_support_until_exact_quotient_debt_paid=1")
    print("  exactp_is_heavy_upstream_not_first_pass_shortcut=1")
    print("  all_routes_still_need_arithmetic_source_theorem_or_hit=1")
    print(f"p25_v2_current_theorem_kernel_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("current theorem kernel failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Drew-facing review packet for the current p25 theorem kernel."""

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
class ReviewRow:
    name: str
    expert_question: str
    positive_answer: str
    first_reject: str
    decision: str
    status: str


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "self_contained_theorem_statement",
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    EvidenceMarker(
        "first_pass_expert_intake_packet",
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
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
        "exactp_spine_payload_separation",
        "evidence/p25_v2_exactp_spine_payload_separation_20260617.md",
        "p25_v2_exactp_spine_payload_separation_rows=1/1",
    ),
    EvidenceMarker(
        "local_source_hook_coverage_audit",
        "evidence/p25_v2_local_source_hook_coverage_audit_20260617.md",
        "p25_v2_local_source_hook_coverage_audit_rows=1/1",
    ),
)


def review_rows() -> tuple[ReviewRow, ...]:
    return (
        ReviewRow(
            name="scalar_fixed_row_theorem",
            expert_question=(
                "Is there a challenge-legal arithmetic theorem giving one exact "
                "oriented support-156 row R_m, m in {1,2,4,8}?"
            ),
            positive_answer=(
                "finite scalar-fixed divisor/additive identity with "
                "Norm_156(Y_507) boundary"
            ),
            first_reject=(
                "source legality, boundary-only, divisor class, or value up to "
                "unspecified F_p^* scalar"
            ),
            decision="source_stage_if_present",
            status="live_not_in_hand",
        ),
        ReviewRow(
            name="row_labeled_unique_power",
            expert_question=(
                "Is there an exact source theorem for R_m^e on one labeled legal "
                "row, with e in {3,5,13,39,75,169,507}?"
            ),
            positive_answer=(
                "exact finite F_p value plus row label and accepted boundary or "
                "period bridge; recover R_m by inverse exponent"
            ),
            first_reject=(
                "rowless power value, powered boundary only, value up to scalar, "
                "or exact-P 75-atom vocabulary"
            ),
            decision="normalize_to_source_stage_if_present",
            status="live_not_in_hand",
        ),
        ReviewRow(
            name="support_period156_value",
            expert_question=(
                "Is there a finite value theorem for canonical H0 or Y_507 with "
                "support-period-156 branch/root/telescoping data?"
            ),
            positive_answer=(
                "finite value theorem plus legal-row bridge and no ambient "
                "period-780 mu_11 ambiguity"
            ),
            first_reject=(
                "H0/Y507 name only, norm identity only, class-field generation, "
                "ambient-period value, or value up to scalar"
            ),
            decision="period_branch_normalize_to_source_stage_if_present",
            status="live_not_in_hand",
        ),
        ReviewRow(
            name="q_yang_support",
            expert_question=(
                "If the theorem is stated for mixed conductor-39 Q/Yang/H90 data, "
                "does it pay selector debt and give finite theorem data?"
            ),
            positive_answer=(
                "finite Q or Q^3 theorem with period-156 context plus oriented "
                "split/direct row normalization"
            ),
            first_reject=(
                "Q source language, Q^6 boundary, diagonal aggregate, Q-square "
                "without extraction map, or selector without finite value"
            ),
            decision="support_only_until_selector_and_finite_theorem_present",
            status="support_not_source_stage",
        ),
        ReviewRow(
            name="matched_quotient_aggregate_support",
            expert_question=(
                "If the theorem is stated for an aggregate row product R^v, "
                "does it also give the exact matched zero-lattice quotient?"
            ),
            positive_answer=(
                "arithmetic theorem for R^v plus arithmetic theorem for "
                "R^(v - (sum v)e_m), with gcd(sum v,p-1)=1"
            ),
            first_reject=(
                "aggregate-only, quotient-only, unmatched quotient, zero-sum, "
                "or nonunit coefficient sum"
            ),
            decision="support_only_until_matched_quotient_packet_present",
            status="support_not_source_stage",
        ),
        ReviewRow(
            name="exactp_theta2_upstream",
            expert_question=(
                "If the theorem is exact-P/theta2 flavored, does it carry the "
                "accepted packet and the 75->300->12->312->156 bridge?"
            ),
            positive_answer=(
                "compact C,D,K/orientation, equal-weight atoms, exact KL mixed "
                "selector, or accepted theta2 payload with bridge"
            ),
            first_reject=(
                "exact-P vocabulary, finite fixture, atom count, normalized-y/KL/"
                "Sprang context, theta word, or unified target alone"
            ),
            decision="heavy_upstream_only_if_exact_theorem_present",
            status="heavy_not_first_pass",
        ),
        ReviewRow(
            name="reverse_unified_to_exactp",
            expert_question=(
                "Can a unified support-156 theorem alone reconstruct exact-P?"
            ),
            positive_answer=(
                "only with explicit reverse selector data to C,D,K/orientation, "
                "equal-weight atoms, or accepted theta2 payload"
            ),
            first_reject="unified value/divisor theorem or Y_507 bridge alone",
            decision="reject_without_extra_selector_structure",
            status="reject_boundary",
        ),
    )


def main() -> int:
    rows = review_rows()
    marker_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    unique_power_ok = all(gcd(exponent, PM1) == 1 for exponent in UNIQUE_ROW_POWERS)
    source_stage_rows = sum("source_stage" in row.decision for row in rows)
    support_rows = sum(row.status.startswith("support") for row in rows)
    heavy_rows = sum(row.status.startswith("heavy") for row in rows)
    reject_rows = sum(row.status.startswith("reject") for row in rows)
    current_positive_answers = 0
    current_submission_ready = 0
    overall_ok = (
        P25 % 8 == 5
        and marker_count == len(EVIDENCE_MARKERS)
        and unique_power_ok
        and len(rows) == 7
        and source_stage_rows == 3
        and support_rows == 2
        and heavy_rows == 1
        and reject_rows == 1
        and current_positive_answers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 drew kernel review packet")
    print(f"p={P25}")
    print(f"unique_row_powers={UNIQUE_ROW_POWERS}")
    print(f"unique_power_gcds={[gcd(exponent, PM1) for exponent in UNIQUE_ROW_POWERS]}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("review_rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision} status={row.status}")
        print(f"    expert_question={row.expert_question}")
        print(f"    positive_answer={row.positive_answer}")
        print(f"    first_reject={row.first_reject}")
    print("counts")
    print(f"  evidence_markers_ok={marker_count}/{len(EVIDENCE_MARKERS)}")
    print(f"  review_rows={len(rows)}")
    print(f"  source_stage_rows={source_stage_rows}")
    print(f"  support_rows={support_rows}")
    print(f"  heavy_rows={heavy_rows}")
    print(f"  reject_rows={reject_rows}")
    print(f"  current_positive_answers={current_positive_answers}")
    print(f"  current_submission_ready={current_submission_ready}")
    print(f"p25_v2_drew_kernel_review_packet_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("drew kernel review packet failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

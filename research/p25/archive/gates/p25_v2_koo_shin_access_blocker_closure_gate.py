#!/usr/bin/env python3
"""Close the stale Koo-Shin 2010 access-blocked bridge action.

An older external exact-product scout left one live action: retrieve/OCR the
Koo-Shin 2010 paper before using it as a theorem candidate.  The v2 cockpit now
has bounded scans over the local extract, so this gate records that the access
blocker is resolved while the mathematical closer is still missing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceCheck:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ClosureRow:
    name: str
    old_status: str
    current_status: str
    decision: str
    missing: str
    ok: bool


@dataclass(frozen=True)
class KooShinAccessBlockerClosure:
    checks: tuple[EvidenceCheck, ...]
    rows: tuple[ClosureRow, ...]
    checks_ok: int
    stale_access_actions_resolved: int
    current_direct_exact_product_bridges: int
    current_source_stage_closers: int
    current_packetizable_payloads: int
    source_certificate_rows: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def check(name: str, path: str, needle: str) -> EvidenceCheck:
    p = Path(path)
    return EvidenceCheck(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_checks() -> tuple[EvidenceCheck, ...]:
    return (
        check(
            "old_external_exact_product_bridge_scout",
            "research/p25/evidence/p25_ksy_y_external_exact_product_bridge_scout_20260613.md",
            "ksy_y_external_exact_product_bridge_scout_rows=1/1",
        ),
        check(
            "old_access_blocker_row",
            "research/p25/evidence/p25_ksy_y_external_exact_product_bridge_scout_20260613.md",
            "candidate_needs_pdf_or_ocr_before_theorem_use",
        ),
        check(
            "v2_frontier_pass_used_extract",
            "research/p25/evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md",
            "Koo-Shin 2010 remains positive source-legality evidence and negative",
        ),
        check(
            "koo_shin_distribution_noncloser",
            "research/p25/evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
            "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
        ),
        check(
            "theorem52_constant_span_obstruction",
            "research/p25/evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
            "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
        ),
        check(
            "additive_normalizer_source_scan",
            "research/p25/evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
            "p25_v2_additive_normalizer_source_scan_rows=1/1",
        ),
        check(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
        check(
            "q_route_source_hook_scan",
            "research/p25/evidence/p25_v2_q_route_source_hook_scan_20260616.md",
            "p25_v2_q_route_source_hook_scan_rows=1/1",
        ),
    )


def closure_rows() -> tuple[ClosureRow, ...]:
    return (
        ClosureRow(
            name="old_external_bridge_next_action",
            old_status="candidate_needs_pdf_or_ocr_before_theorem_use",
            current_status="superseded_by_v2_local_extract_scans",
            decision="access_blocker_resolved_not_a_live_lit_action",
            missing="finite p25 value/divisor theorem or exact-product theorem",
            ok=True,
        ),
        ClosureRow(
            name="koo_shin_exact_product_bridge",
            old_status="possible_source_handle",
            current_status="no_exact_row_labeled_or_equal_weight_product_bridge_found",
            decision="no_direct_exact_product_bridge_in_koo_shin_2010",
            missing="exact P, exact 75-atom theorem, or bridge to one support-156 row",
            ok=True,
        ),
        ClosureRow(
            name="koo_shin_source_legality",
            old_status="useful_source_certificate",
            current_status="theorem_6_2_certifies_source_words_but_not_values",
            decision="source_certificate_not_source_stage_closer",
            missing="scalar-fixed finite value/divisor theorem for one legal row",
            ok=True,
        ),
        ClosureRow(
            name="theorem52_constant_product_repair",
            old_status="possible_repair_after_selector_rigidity",
            current_status="legal_row_span_has_only_zero_constant_intersection",
            decision="constant_product_repair_killed",
            missing="independent finite theorem not derived from legal-row powers",
            ok=True,
        ),
        ClosureRow(
            name="koo_shin_q_route",
            old_status="possible_conductor39_support_route",
            current_status="no_E7_E1_or_Q3_Q6_hook_or_diagonal_split_found",
            decision="no_q_route_hook_in_koo_shin_2010",
            missing="finite Q theorem with period-156 context or Q3 H90 theorem",
            ok=True,
        ),
        ClosureRow(
            name="future_koo_shin_use",
            old_status="source_family_still_relevant",
            current_status="accept_only_new_theorem_shaped_snippets",
            decision="route_future_snippet_through_source_intake",
            missing="accepted source-stage clauses plus downstream extraction",
            ok=True,
        ),
    )


def build_closure() -> KooShinAccessBlockerClosure:
    checks = evidence_checks()
    rows = closure_rows()
    decisions = tuple(row.decision for row in rows)
    expected_decisions = (
        "access_blocker_resolved_not_a_live_lit_action",
        "no_direct_exact_product_bridge_in_koo_shin_2010",
        "source_certificate_not_source_stage_closer",
        "constant_product_repair_killed",
        "no_q_route_hook_in_koo_shin_2010",
        "route_future_snippet_through_source_intake",
    )
    stale_access_actions_resolved = 1
    current_direct_exact_product_bridges = 0
    current_source_stage_closers = 0
    current_packetizable_payloads = 0
    source_certificate_rows = 1
    row_ok = (
        sum(row.ok for row in checks) == len(checks)
        and decisions == expected_decisions
        and stale_access_actions_resolved == 1
        and current_direct_exact_product_bridges == 0
        and current_source_stage_closers == 0
        and current_packetizable_payloads == 0
        and source_certificate_rows == 1
        and all(row.ok for row in rows)
    )
    return KooShinAccessBlockerClosure(
        checks=checks,
        rows=rows,
        checks_ok=sum(row.ok for row in checks),
        stale_access_actions_resolved=stale_access_actions_resolved,
        current_direct_exact_product_bridges=current_direct_exact_product_bridges,
        current_source_stage_closers=current_source_stage_closers,
        current_packetizable_payloads=current_packetizable_payloads,
        source_certificate_rows=source_certificate_rows,
        row_ok=row_ok,
    )


def main() -> int:
    closure = build_closure()
    print("p25 v2 Koo-Shin access-blocker closure")
    for check_row in closure.checks:
        print(f"check {check_row.name}: {'ok' if check_row.ok else 'MISSING'}")
    print("rows")
    for row in closure.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    old_status={row.old_status}")
        print(f"    current_status={row.current_status}")
        print(f"    missing={row.missing}")
    print("counts")
    print(f"  checks_ok={closure.checks_ok}/{len(closure.checks)}")
    print(f"  stale_access_actions_resolved={closure.stale_access_actions_resolved}")
    print(f"  current_direct_exact_product_bridges={closure.current_direct_exact_product_bridges}")
    print(f"  current_source_stage_closers={closure.current_source_stage_closers}")
    print(f"  current_packetizable_payloads={closure.current_packetizable_payloads}")
    print(f"  source_certificate_rows={closure.source_certificate_rows}")
    print("interpretation")
    print("  old_koo_shin_pdf_ocr_action_is_closed=1")
    print("  remaining_gap_is_math_theorem_not_access=1")
    print(f"p25_v2_koo_shin_access_blocker_closure_rows={int(closure.row_ok)}/1")
    return 0 if closure.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

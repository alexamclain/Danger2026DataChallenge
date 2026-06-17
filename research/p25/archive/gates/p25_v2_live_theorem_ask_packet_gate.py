#!/usr/bin/env python3
"""Validate the live theorem ask packet.

The packet is the next-action surface after the source lookup rows were
classified. It should keep future expert, literature, and proof attempts
centered on three theorem-shaped asks instead of reopening broad source
families.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class AskRow:
    name: str
    status: str
    required_object: str
    positive_hook: str
    first_falsifier: str
    next_action: str


EVIDENCE_INPUTS = (
    (
        "source_action_registry",
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
    (
        "first_pass_expert_intake",
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
    (
        "priority1_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "period156_lookup_status",
        "evidence/p25_v2_period156_lookup_row_status_20260617.md",
        "p25_v2_period156_lookup_row_status_rows=1/1",
    ),
    (
        "q_yang_lookup_status",
        "evidence/p25_v2_q_yang_lookup_row_status_20260617.md",
        "p25_v2_q_yang_lookup_row_status_rows=1/1",
    ),
    (
        "normalizer_lookup_status",
        "evidence/p25_v2_normalizer_lookup_row_status_20260617.md",
        "p25_v2_normalizer_lookup_row_status_rows=1/1",
    ),
    (
        "exactp_theta2_lookup_status",
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
    (
        "source_stage_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "matched_quotient_closure_packet",
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    (
        "source_theorem_acceptance_automaton",
        "evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
        "p25_v2_source_theorem_acceptance_automaton_rows=1/1",
    ),
    (
        "source_snippet_intake",
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
    (
        "expert_response_rubric",
        "evidence/p25_v2_current_expert_response_rubric_20260616.md",
        "p25_v2_current_expert_response_rubric_rows=1/1",
    ),
    (
        "post_theorem_extraction_router",
        "evidence/p25_v2_post_theorem_extraction_router_20260616.md",
        "p25_v2_post_theorem_extraction_router_rows=1/1",
    ),
    (
        "unified_submission_contract",
        "evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
        "p25_v2_unified_submission_extraction_contract_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def ask_rows() -> tuple[AskRow, ...]:
    return (
        AskRow(
            "first_pass_row_theorem",
            "live_primary",
            "one oriented legal support-156 row R_m, m in {1,2,4,8}, with Norm_156(Y_507) boundary",
            "scalar-fixed finite divisor/additive theorem, uniquely invertible finite power-value theorem, or aggregate theorem plus exact matched zero-lattice quotient, from an arithmetic source",
            "legality-only, boundary-only, selector-only, aggregate without matched quotient, Q-only without selector debt, or unspecified F_p^* scalar",
            "ask Drew/source/proof attempt for the finite theorem; route positives to source-stage normalization then extraction router",
        ),
        AskRow(
            "period156_h0_y507_value",
            "live_support_value",
            "canonical H0 or Y_507 support-period-156 value with legal-row bridge",
            "finite value theorem with branch/root/telescoping or additive normalization, avoiding ambient-period-780 ambiguity",
            "class-field generation, ambient-period-780 value, mu_11 quotient, degree-6 value without F_p descent, or value up to scalar",
            "use only when a source snippet already names H0/Y_507 period-156 data; otherwise keep as support",
        ),
        AskRow(
            "exactp_theta2_heavy",
            "live_heavy",
            "compact C,D,K,orientation packet, equal-weight 75 atoms, or accepted theta2/theta2-inverse payload",
            "arithmetic theorem emitting the exact packet, primitive KL word or mixed selector, Sprang sparse specialization, or reverse reconstruction",
            "normalized-y vocabulary, raw KL exponent balance, generic modular-unit generation, theta language without period-156 branch, or unified-target-only theorem",
            "keep as second-pass moonshot unless the source/proof already carries one accepted exact-P hook",
        ),
    )


def canonical_pages_ok(root: Path) -> bool:
    checks = (
        ("frontier.md", "Live Theorem Ask Packet"),
        ("lanes/h0.md", "live theorem ask packet"),
        ("lanes/conductor39.md", "live theorem ask packet"),
        ("lanes/exact-p.md", "live theorem ask packet"),
    )
    for rel, needle in checks:
        path = root / rel
        if not path.exists() or needle not in path.read_text():
            return False
    return True


def broad_reread_closed(root: Path) -> bool:
    registry = root / "evidence/p25_v2_source_action_registry_20260616.md"
    lookup = root / "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md"
    text = (registry.read_text() if registry.exists() else "") + "\n"
    text += lookup.read_text() if lookup.exists() else ""
    return (
        "broad_reread_allowed_rows = 0" in text
        and "The next source or expert pass should not ask broadly" in text
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[AskRow, ...], bool]:
    markers = evidence_markers(root)
    rows = ask_rows()
    statuses = {row.status for row in rows}
    row_ok = (
        all(marker.ok for marker in markers)
        and canonical_pages_ok(root)
        and broad_reread_closed(root)
        and len(rows) == 3
        and statuses == {"live_primary", "live_support_value", "live_heavy"}
        and any("extraction router" in row.next_action for row in rows)
        and any("second-pass moonshot" in row.next_action for row in rows)
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 live theorem ask packet")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"canonical_pages_ok={int(canonical_pages_ok(root))}")
    print(f"broad_reread_closed={int(broad_reread_closed(root))}")
    print("ask_rows")
    for row in rows:
        print(f"  {row.name}: status={row.status}")
        print(f"    required_object={row.required_object}")
        print(f"    positive_hook={row.positive_hook}")
        print(f"    first_falsifier={row.first_falsifier}")
        print(f"    next_action={row.next_action}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"live_theorem_asks={len(rows)}")
    print("broad_reread_allowed_rows=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_live_theorem_ask_packet_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

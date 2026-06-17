#!/usr/bin/env python3
"""Validate the compact first-pass expert/source intake packet.

This is a lightweight consistency gate.  It does not recompute the H0 or
conductor-39 payloads; it checks that the expert-facing packet is aligned with
the already promoted theorem statement, minimal ask, positive matcher, and
source-action registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SOURCE_MARKERS = (
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    (
        "evidence/p25_v2_unified_theorem_review_packet_20260616.md",
        "p25_v2_unified_theorem_review_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_minimal_expert_ask_20260616.md",
        "p25_v2_minimal_expert_ask_rows=1/1",
    ),
    (
        "evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
        "p25_v2_positive_theorem_clause_matcher_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_graph_normal_form_20260616.md",
        "p25_v2_source_graph_normal_form_rows=1/1",
    ),
    (
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_constructive_value_payload_contract_20260616.md",
        "p25_v2_constructive_value_payload_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
        "p25_v2_power_normalized_theorem_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
)

ROW_HASHES = (
    "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e",
    "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9",
    "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6",
    "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87",
)

FIRST_PASS_ROUTES = (
    "scalar_fixed_divisor_additive_theorem",
    "period156_value_theorem_with_branch_context",
    "canonical_h0_divisor_additive_identity",
    "quartic_character_finite_theorem",
    "canonical_h0_period156_value_identity",
    "Y_507_period156_value_identity",
    "power_normalized_row_value_theorem",
)

SUPPORT_OR_HEAVY_ROUTES = (
    "exactp_upstream_theorem_via_minimal_hook",
    "norm_one_Q_value_theorem_with_period156_context",
    "explicit_Q3_hilbert90_preimage_with_finite_theorem",
)

REPAIR_OR_REJECT_ROWS = (
    "source_legality_only",
    "boundary_only",
    "unspecified_fp_scalar",
    "period780_or_mu11_only",
    "degree6_value_without_fp_descent",
    "aggregate_or_row_square_only",
    "projector_values_without_fourth_root",
    "two_edge_pair_without_oriented_square_root",
    "exact_quartic_selector_without_finite_theorem",
    "coarse_quartic_phase_or_magnitude_only",
    "ambiguous_power_value_without_selector",
    "finite_payload_without_source",
    "generic_cm_or_class_field_generation",
    "coset_selector_or_Q_source_only",
    "Q_diagonal_value_only",
    "Q_plus_row_quotient_without_root",
    "Q6_boundary_only",
    "pure_character_degree6_norm",
)

PACKET_REQUIRED_LINES = (
    "source_markers_ok = 11/11",
    "intake_rows_ok = 6/6",
    "first_pass_frontdoor_routes = 5",
    "current_source_theorems = 0",
    "submission_ready_rows = 0",
    "p25_v2_first_pass_expert_intake_packet_rows=1/1",
)


@dataclass(frozen=True)
class IntakePacketCheck:
    source_markers_ok: int
    source_markers_total: int
    row_hashes_ok: int
    row_hashes_total: int
    first_pass_routes_ok: int
    first_pass_routes_total: int
    support_routes_ok: int
    support_routes_total: int
    repair_or_reject_ok: int
    repair_or_reject_total: int
    packet_lines_ok: int
    packet_lines_total: int
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text()


def build_check(root: Path) -> IntakePacketCheck:
    source_markers_ok = 0
    source_texts: dict[str, str] = {}
    for rel, marker in SOURCE_MARKERS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        source_texts[rel] = text
        source_markers_ok += int(marker in text)

    combined_sources = "\n".join(source_texts.values())
    row_hashes_ok = sum(hash_value in combined_sources for hash_value in ROW_HASHES)
    first_pass_routes_ok = sum(route in combined_sources for route in FIRST_PASS_ROUTES)
    support_routes_ok = sum(route in combined_sources for route in SUPPORT_OR_HEAVY_ROUTES)
    repair_or_reject_ok = sum(row in combined_sources for row in REPAIR_OR_REJECT_ROWS)

    packet_text = read(root, "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md")
    packet_lines_ok = sum(line in packet_text for line in PACKET_REQUIRED_LINES)

    row_ok = (
        source_markers_ok == len(SOURCE_MARKERS)
        and row_hashes_ok == len(ROW_HASHES)
        and first_pass_routes_ok == len(FIRST_PASS_ROUTES)
        and support_routes_ok == len(SUPPORT_OR_HEAVY_ROUTES)
        and repair_or_reject_ok == len(REPAIR_OR_REJECT_ROWS)
        and packet_lines_ok == len(PACKET_REQUIRED_LINES)
    )

    return IntakePacketCheck(
        source_markers_ok=source_markers_ok,
        source_markers_total=len(SOURCE_MARKERS),
        row_hashes_ok=row_hashes_ok,
        row_hashes_total=len(ROW_HASHES),
        first_pass_routes_ok=first_pass_routes_ok,
        first_pass_routes_total=len(FIRST_PASS_ROUTES),
        support_routes_ok=support_routes_ok,
        support_routes_total=len(SUPPORT_OR_HEAVY_ROUTES),
        repair_or_reject_ok=repair_or_reject_ok,
        repair_or_reject_total=len(REPAIR_OR_REJECT_ROWS),
        packet_lines_ok=packet_lines_ok,
        packet_lines_total=len(PACKET_REQUIRED_LINES),
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(research_root())
    print("p25 v2 first-pass expert intake packet")
    print(f"source_markers_ok={check.source_markers_ok}/{check.source_markers_total}")
    print(f"row_hashes_ok={check.row_hashes_ok}/{check.row_hashes_total}")
    print(
        "first_pass_routes_ok="
        f"{check.first_pass_routes_ok}/{check.first_pass_routes_total}"
    )
    print(f"support_routes_ok={check.support_routes_ok}/{check.support_routes_total}")
    print(
        "repair_or_reject_rows_ok="
        f"{check.repair_or_reject_ok}/{check.repair_or_reject_total}"
    )
    print(f"packet_lines_ok={check.packet_lines_ok}/{check.packet_lines_total}")
    print(f"p25_v2_first_pass_expert_intake_packet_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

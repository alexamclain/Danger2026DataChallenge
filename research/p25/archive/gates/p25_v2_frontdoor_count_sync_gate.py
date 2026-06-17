#!/usr/bin/env python3
"""Check that front-door theorem counts agree after grouping choices.

The p25 v2 handoff has three different presentations of the same theorem
front:

* the clause matcher splits H0, Y_507, quartic-character, and
  power-normalized route variants, so it has five first-pass presentations;
* the expert rubric keeps three direct source-closing row families and routes
  exact unique powers through normalize-then-intake;
* the minimal ask phrases the first-pass math as three questions, while
  treating exact-P as a heavier accepted route and Q/Q3/Q-split as
  support/normalization variants rather than independent front doors. Exact
  Q-square value data is counted as a bounded row-value payload with an
  extraction-map repair, not as a front door.

This gate records that the difference is intentional, not a stale count.
The power route uses the current checked unique-power set
{3,5,13,39,75,169,507}.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class FrontDoorCountSync:
    evidence_markers: tuple[EvidenceMarker, ...]
    positive_matcher_frontdoor_presentations: int
    expert_rubric_frontdoor_families: int
    minimal_ask_accepted_routes: int
    minimal_ask_first_pass_questions: int
    exactp_heavy_routes: int
    current_source_theorems: int
    current_submission_ready: int
    clause_tokens_ok: bool
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def count_value(text: str, key: str) -> int:
    match = re.search(rf"{re.escape(key)}\s*=\s*(\d+)", text)
    return int(match.group(1)) if match else -1


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
    )


def build_sync() -> FrontDoorCountSync:
    positive_text = read("research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md")
    rubric_text = read("research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md")
    minimal_text = read("research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md")
    source_family_text = read("research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md")

    markers = evidence_markers()
    positive_frontdoor = count_value(positive_text, "h0_y507_frontdoor_routes")
    rubric_frontdoor = count_value(rubric_text, "frontdoor_source_closing_rows")
    minimal_routes = count_value(minimal_text, "accepted_routes")
    exactp_heavy = count_value(positive_text, "exactp_heavy_routes")
    current_source = max(
        count_value(positive_text, "current_source_theorems"),
        count_value(rubric_text, "current_source_stage_closers"),
        count_value(source_family_text, "first_pass_closers"),
    )
    current_submission = max(
        count_value(positive_text, "current_submission_ready"),
        count_value(rubric_text, "current_submission_ready"),
        count_value(source_family_text, "current_submission_ready"),
    )

    first_pass_questions = sum(
        (
            "1. a scalar-fixed finite divisor/additive identity" in minimal_text,
            "2. a support-period-156 finite value theorem" in minimal_text,
            "3. an exact finite power-value theorem" in minimal_text,
        )
    )

    required_tokens = (
        "canonical_h0_divisor_additive_identity",
        "quartic_character_finite_theorem",
        "canonical_h0_period156_value_identity",
        "Y_507_period156_value_identity",
        "power_normalized_row_value_theorem",
        "exactp_upstream_bridge_theorem",
        "normalized_divisor_additive_theorem",
        "normalized_period156_value_theorem",
        "quartic_selector_finite_theorem",
        "exact_unique_power_value",
        "exactp_upstream_theorem",
        "norm_one_Q_value_theorem_with_period156_context",
        "explicit_Q3_hilbert90_preimage_with_finite_theorem",
        "Q_plus_explicit_oriented_diagonal_split",
        "ambiguous_power_value_without_selector",
        "Q_square_exact_value_without_extraction_map",
        "repair_extraction_map_missing_after_two_root_row_payload",
        "exact row-antisymmetric `C4_1`",
    )
    combined = "\n".join((positive_text, rubric_text, minimal_text))
    clause_tokens_ok = all(token in combined for token in required_tokens)

    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and positive_frontdoor == 5
        and rubric_frontdoor == 3
        and minimal_routes == 7
        and first_pass_questions == 3
        and exactp_heavy == 1
        and current_source == 0
        and current_submission == 0
        and clause_tokens_ok
    )

    return FrontDoorCountSync(
        evidence_markers=markers,
        positive_matcher_frontdoor_presentations=positive_frontdoor,
        expert_rubric_frontdoor_families=rubric_frontdoor,
        minimal_ask_accepted_routes=minimal_routes,
        minimal_ask_first_pass_questions=first_pass_questions,
        exactp_heavy_routes=exactp_heavy,
        current_source_theorems=current_source,
        current_submission_ready=current_submission,
        clause_tokens_ok=clause_tokens_ok,
        row_ok=row_ok,
    )


def main() -> int:
    sync = build_sync()
    print("p25 v2 frontdoor count sync")
    for marker_row in sync.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("counts")
    print(f"  positive_matcher_frontdoor_presentations={sync.positive_matcher_frontdoor_presentations}")
    print(f"  expert_rubric_frontdoor_families={sync.expert_rubric_frontdoor_families}")
    print(f"  minimal_ask_accepted_routes={sync.minimal_ask_accepted_routes}")
    print(f"  minimal_ask_first_pass_questions={sync.minimal_ask_first_pass_questions}")
    print(f"  exactp_heavy_routes={sync.exactp_heavy_routes}")
    print(f"  current_source_theorems={sync.current_source_theorems}")
    print(f"  current_submission_ready={sync.current_submission_ready}")
    print("interpretation")
    print(f"  clause_tokens_ok={int(sync.clause_tokens_ok)}")
    print("  count_mismatch_is_grouping_not_new_theorem=1")
    print("  current_source_stage_closers_still_zero=1")
    print(f"p25_v2_frontdoor_count_sync_rows={int(sync.row_ok)}/1")
    return 0 if sync.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

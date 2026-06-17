#!/usr/bin/env python3
"""Check that every priority-1 packet clause is actually necessary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

from p25_v2_priority1_packet_fixture_contract_gate import (  # noqa: E402
    FIXTURE_DIR,
    classify,
    read_json,
    research_root,
)


MARKER = "p25_v2_priority1_clause_necessity_matrix_rows=1/1"

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_priority1_packet_fixture_contract_20260617.md",
        "p25_v2_priority1_packet_fixture_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
)


@dataclass(frozen=True)
class MutationRow:
    name: str
    base_fixture: str
    field: str
    value: object
    expected_decision: str
    actual_decision: str
    ok: bool


H0_MUTATIONS = (
    ("h0_missing_theorem_body", "theorem_body_verified", False, "repair_h0_row_or_source_clause_missing"),
    ("h0_wrong_output_kind", "output_kind", "value-only", "repair_h0_row_or_source_clause_missing"),
    ("h0_missing_arithmetic_source", "arithmetic_source_theorem", False, "repair_h0_row_or_source_clause_missing"),
    ("h0_missing_finite_payload", "finite_or_divisor", False, "repair_h0_row_or_source_clause_missing"),
    ("h0_illegal_multiplier", "h0_product_multiplier", 3, "repair_h0_row_or_source_clause_missing"),
    ("h0_missing_residue_exactness", "h0_residue_sets_exact", False, "repair_h0_row_or_source_clause_missing"),
    ("h0_missing_h90_boundary", "h0_h90_boundary", False, "repair_h0_boundary_missing"),
)

CONDUCTOR39_MUTATIONS = (
    ("c39_missing_theorem_body", "theorem_body_verified", False, "repair_conductor39_clause_missing"),
    ("c39_wrong_output_kind", "output_kind", "value-only", "repair_conductor39_clause_missing"),
    ("c39_missing_arithmetic_source", "arithmetic_source_theorem", False, "repair_conductor39_clause_missing"),
    ("c39_missing_finite_payload", "finite_or_divisor", False, "repair_conductor39_clause_missing"),
    ("c39_wrong_source_object", "conductor39_source_object", "projection", "repair_conductor39_clause_missing"),
    ("c39_missing_emitted_object", "conductor39_emits_object", False, "repair_conductor39_clause_missing"),
    ("c39_missing_mixed_tensor", "conductor39_preserves_mixed_tensor", False, "repair_mixed_tensor_missing"),
    ("c39_missing_legal_unit", "conductor39_yang_yu_legal_unit", False, "repair_conductor39_clause_missing"),
    ("c39_missing_yang_lift", "conductor39_yang_distribution_to_507", False, "repair_conductor39_clause_missing"),
    (
        "c39_missing_h90_descent",
        "conductor39_frobenius_or_hilbert90_descent",
        False,
        "repair_conductor39_clause_missing",
    ),
    ("c39_projection_axis_only", "conductor39_projection_or_axis_only", True, "reject_projection_or_axis_only"),
)


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        ok += int(path.exists() and marker in path.read_text())
    return ok, len(EVIDENCE_MARKERS)


def mutation_rows(root: Path) -> tuple[MutationRow, ...]:
    rows: list[MutationRow] = []
    for base_fixture, mutations in (
        ("h0_divisor_close.json", H0_MUTATIONS),
        ("conductor39_divisor_close.json", CONDUCTOR39_MUTATIONS),
    ):
        base = read_json(root / FIXTURE_DIR / base_fixture)
        for name, field, value, expected in mutations:
            data = dict(base)
            data[field] = value
            actual = classify(data)
            rows.append(
                MutationRow(
                    name=name,
                    base_fixture=base_fixture,
                    field=field,
                    value=value,
                    expected_decision=expected,
                    actual_decision=actual,
                    ok=actual == expected and actual != "current_first_pass_positive_packet",
                )
            )
    return tuple(rows)


def main() -> int:
    root = research_root()
    evidence_ok, evidence_total = evidence_markers_ok(root)
    rows = mutation_rows(root)
    h0_rows = sum(row.base_fixture == "h0_divisor_close.json" for row in rows)
    c39_rows = sum(row.base_fixture == "conductor39_divisor_close.json" for row in rows)
    repairs = sum(row.actual_decision.startswith("repair_") for row in rows)
    rejects = sum(row.actual_decision.startswith("reject_") for row in rows)
    positives = sum(row.actual_decision == "current_first_pass_positive_packet" for row in rows)
    row_ok = (
        evidence_ok == evidence_total
        and len(rows) == 18
        and h0_rows == 7
        and c39_rows == 11
        and repairs == 17
        and rejects == 1
        and positives == 0
        and all(row.ok for row in rows)
    )
    print("p25 v2 priority-1 clause necessity matrix")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print("mutation_rows")
    for row in rows:
        print(
            f"  {row.name}: base={row.base_fixture} field={row.field} "
            f"decision={row.actual_decision} expected={row.expected_decision}"
        )
    print("counts")
    print(f"mutation_rows={len(rows)}")
    print(f"h0_clause_rows={h0_rows}")
    print(f"conductor39_clause_rows={c39_rows}")
    print(f"repair_rows={repairs}")
    print(f"reject_rows={rejects}")
    print(f"false_positive_packets={positives}")
    print("current_priority1_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"{MARKER if row_ok else 'p25_v2_priority1_clause_necessity_matrix_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

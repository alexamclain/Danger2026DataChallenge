#!/usr/bin/env python3
"""Classify theorem-shaped replies against the current p25 source-stage kernel."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P = 10000000000000000000000013
MARKER = "p25_v2_source_theorem_acceptance_automaton_rows=1/1"
UNIQUE_POWER_EXPONENTS = (3, 5, 13, 39, 75, 169, 507)

LEGAL_ROWS = {
    1: ("7H -> 4H", "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e"),
    2: ("7H -> H", "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9"),
    4: ("2H -> H", "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6"),
    8: ("2H -> 4H", "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87"),
}

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    (
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_clause_necessity_matrix_20260617.md",
        "p25_v2_priority1_clause_necessity_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_row_binding_overlay_20260617.md",
        "p25_v2_conductor39_row_binding_overlay_rows=1/1",
    ),
    (
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_graph_normal_form_20260616.md",
        "p25_v2_source_graph_normal_form_rows=1/1",
    ),
    (
        "evidence/p25_v2_distribution_relation_closure_screen_20260617.md",
        "p25_v2_distribution_relation_closure_screen_rows=1/1",
    ),
    (
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
)


@dataclass(frozen=True)
class Candidate:
    name: str
    kind: str
    row_m: int | None
    source_theorem: bool
    finite_payload: bool
    boundary: bool
    scalar_or_branch_fixed: bool
    selector_debt_paid: bool = True
    preserves_mixed_tensor: bool = True
    boundary_sign_ok: bool = True
    exponent: int | None = None
    support_period: int | None = None
    exactp_packet: bool = False
    matched_quotient_supplied: bool = True
    coefficient_sum: int | None = None
    expected: str = ""


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        ok += int(path.exists() and marker in path.read_text())
    return ok, len(EVIDENCE_MARKERS)


def classify(c: Candidate) -> str:
    if not c.preserves_mixed_tensor:
        return "reject_lost_mixed_tensor"
    if not c.boundary_sign_ok:
        return "reject_wrong_boundary_sign"
    if c.exactp_packet and c.source_theorem and c.finite_payload:
        return "route_exactp_theta2_heavy_upstream"
    if not c.source_theorem:
        return "repair_arithmetic_source_theorem_missing"
    if not c.finite_payload:
        return "repair_finite_payload_missing"
    if not c.boundary:
        return "repair_norm156_boundary_missing"
    if c.kind == "ambient_period780_value":
        return "repair_period156_branch_missing"
    if not c.scalar_or_branch_fixed:
        return "repair_scalar_or_branch_missing"
    if c.exponent is not None and gcd(c.exponent, P - 1) != 1:
        return "repair_nonunique_power_root"
    if c.kind == "distribution_relation_closure":
        return "repair_even_boundary_distribution_closure"
    if c.kind == "matched_quotient_packet":
        if c.row_m not in LEGAL_ROWS:
            return "repair_row_binding_missing"
        if not c.matched_quotient_supplied or not c.selector_debt_paid:
            return "repair_zero_lattice_value_missing"
        if c.coefficient_sum is None or c.coefficient_sum == 0:
            return "transfer_only_not_first_anchor"
        if gcd(c.coefficient_sum, P - 1) != 1:
            return "repair_root_debt_remaining"
        return "normalize_matched_quotient_then_accept"
    if c.row_m not in LEGAL_ROWS:
        if c.kind == "q_diagonal_or_projector" and not c.selector_debt_paid:
            return "repair_selector_debt_unpaid"
        if c.kind == "all_four_or_diagonal_aggregate":
            return "repair_row_selection_missing"
        return "repair_row_binding_missing"
    if c.kind == "q_diagonal_or_projector" and not c.selector_debt_paid:
        return "repair_selector_debt_unpaid"
    if c.exponent is not None:
        return "accept_via_row_labeled_unique_power"
    if c.support_period == 156:
        return "accept_via_support_period156_value"
    if c.kind == "q_yang_support_paid":
        return "normalize_q_yang_support_then_accept"
    return "accept_direct_row_divisor_additive"


def candidates() -> tuple[Candidate, ...]:
    return (
        Candidate(
            name="direct_m1_divisor_additive",
            kind="direct_row",
            row_m=1,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="accept_direct_row_divisor_additive",
        ),
        *tuple(
            Candidate(
                name=f"m2_unique_power_{exponent}",
                kind="row_labeled_power",
                row_m=2,
                source_theorem=True,
                finite_payload=True,
                boundary=True,
                scalar_or_branch_fixed=True,
                exponent=exponent,
                expected="accept_via_row_labeled_unique_power",
            )
            for exponent in UNIQUE_POWER_EXPONENTS
        ),
        Candidate(
            name="m4_period156_value",
            kind="support_period156_value",
            row_m=4,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            support_period=156,
            expected="accept_via_support_period156_value",
        ),
        Candidate(
            name="q_yang_selector_paid_to_m8",
            kind="q_yang_support_paid",
            row_m=8,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            selector_debt_paid=True,
            expected="normalize_q_yang_support_then_accept",
        ),
        Candidate(
            name="exactp_theta2_packet",
            kind="exactp_theta2",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            exactp_packet=True,
            expected="route_exactp_theta2_heavy_upstream",
        ),
        Candidate(
            name="matched_quotient_unit_power_to_m1",
            kind="matched_quotient_packet",
            row_m=1,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            matched_quotient_supplied=True,
            coefficient_sum=3,
            expected="normalize_matched_quotient_then_accept",
        ),
        Candidate(
            name="aggregate_without_matched_quotient",
            kind="matched_quotient_packet",
            row_m=1,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            matched_quotient_supplied=False,
            selector_debt_paid=False,
            coefficient_sum=1,
            expected="repair_zero_lattice_value_missing",
        ),
        Candidate(
            name="matched_quotient_nonunit_sum",
            kind="matched_quotient_packet",
            row_m=1,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            matched_quotient_supplied=True,
            coefficient_sum=2,
            expected="repair_root_debt_remaining",
        ),
        Candidate(
            name="conductor39_rowless_mixed_packet",
            kind="rowless_mixed_packet",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="repair_row_binding_missing",
        ),
        Candidate(
            name="boundary_only_h90_statement",
            kind="direct_row",
            row_m=1,
            source_theorem=True,
            finite_payload=False,
            boundary=True,
            scalar_or_branch_fixed=False,
            expected="repair_finite_payload_missing",
        ),
        Candidate(
            name="finite_payload_without_source",
            kind="direct_row",
            row_m=1,
            source_theorem=False,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="repair_arithmetic_source_theorem_missing",
        ),
        Candidate(
            name="ambient_period780_value",
            kind="ambient_period780_value",
            row_m=2,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="repair_period156_branch_missing",
        ),
        Candidate(
            name="q_diagonal_without_split",
            kind="q_diagonal_or_projector",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            selector_debt_paid=False,
            expected="repair_selector_debt_unpaid",
        ),
        Candidate(
            name="projector_without_fourth_root",
            kind="q_diagonal_or_projector",
            row_m=4,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            selector_debt_paid=False,
            expected="repair_selector_debt_unpaid",
        ),
        Candidate(
            name="all_four_orbit_aggregate",
            kind="all_four_or_diagonal_aggregate",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="repair_row_selection_missing",
        ),
        Candidate(
            name="distribution_norm_closure_even_boundary",
            kind="distribution_relation_closure",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            expected="repair_even_boundary_distribution_closure",
        ),
        Candidate(
            name="row_power_23",
            kind="row_labeled_power",
            row_m=8,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            exponent=23,
            expected="repair_nonunique_power_root",
        ),
        Candidate(
            name="prime_axis_projection",
            kind="prime_projection",
            row_m=None,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            preserves_mixed_tensor=False,
            expected="reject_lost_mixed_tensor",
        ),
        Candidate(
            name="reciprocal_positive_boundary",
            kind="reciprocal",
            row_m=1,
            source_theorem=True,
            finite_payload=True,
            boundary=True,
            scalar_or_branch_fixed=True,
            boundary_sign_ok=False,
            expected="reject_wrong_boundary_sign",
        ),
    )


def main() -> int:
    root = research_root()
    evidence_ok, evidence_total = evidence_markers_ok(root)
    text = "\n".join(
        (root / rel).read_text()
        for rel, _marker in EVIDENCE_MARKERS
        if (root / rel).exists()
    )
    row_hashes_bound = sum(row_hash in text for _edge, row_hash in LEGAL_ROWS.values())
    rows = candidates()
    classified = tuple((row, classify(row)) for row in rows)
    accepted = sum(actual.startswith("accept_") for _row, actual in classified)
    normalized = sum(actual.startswith("normalize_") for _row, actual in classified)
    heavy = sum(actual.startswith("route_exactp") for _row, actual in classified)
    repairs = sum(actual.startswith("repair_") for _row, actual in classified)
    rejects = sum(actual.startswith("reject_") for _row, actual in classified)
    invertible_powers = sum(
        row.exponent is not None and gcd(row.exponent, P - 1) == 1
        for row in rows
    )
    noninvertible_powers = sum(
        row.exponent is not None and gcd(row.exponent, P - 1) != 1
        for row in rows
    )
    matched_quotient_rows = sum(row.kind == "matched_quotient_packet" for row in rows)
    ok = (
        evidence_ok == evidence_total
        and row_hashes_bound == 4
        and len(rows) == 25
        and accepted == 9
        and normalized == 2
        and heavy == 1
        and repairs == 11
        and rejects == 2
        and invertible_powers == 7
        and noninvertible_powers == 1
        and matched_quotient_rows == 3
        and all(actual == row.expected for row, actual in classified)
    )
    print("p25 v2 source theorem acceptance automaton")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print(f"legal_row_hashes_bound={row_hashes_bound}/4")
    print("rows")
    for row, actual in classified:
        print(
            f"  {row.name}: kind={row.kind} m={row.row_m} "
            f"decision={actual} expected={row.expected}"
        )
    print("counts")
    print(f"candidate_rows={len(rows)}")
    print(f"accepted_source_stage_rows={accepted}")
    print(f"normalize_then_accept_rows={normalized}")
    print(f"heavy_upstream_rows={heavy}")
    print(f"repair_rows={repairs}")
    print(f"reject_rows={rejects}")
    print(f"invertible_power_rows={invertible_powers}")
    print(f"noninvertible_power_rows={noninvertible_powers}")
    print(f"matched_quotient_rows={matched_quotient_rows}")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"{MARKER if ok else 'p25_v2_source_theorem_acceptance_automaton_rows=0/1'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

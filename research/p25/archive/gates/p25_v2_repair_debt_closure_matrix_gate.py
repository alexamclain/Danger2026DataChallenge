#!/usr/bin/env python3
"""Repair-debt closure matrix for p25 first-pass theorem shapes."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
PM1 = P25 - 1


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class DebtRow:
    name: str
    theorem_shape: str
    p25_debt: str
    branch_count: int | str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RepairDebtClosureMatrix:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[DebtRow, ...]
    power_kernels: tuple[tuple[int, int], ...]
    period_branch_gcds: tuple[tuple[int, int], ...]
    evidence_markers_ok: int
    unique_normalization_rows: int
    bounded_branch_repair_rows: int
    scalar_debt_rows: int
    support_only_rows: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "extended_unique_power_intake",
            "research/p25/evidence/p25_v2_extended_unique_power_intake_20260617.md",
            "p25_v2_extended_unique_power_intake_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "zero_lattice_transfer_contract",
            "research/p25/evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
            "p25_v2_zero_lattice_transfer_contract_rows=1/1",
        ),
        marker(
            "row_orientation_candidate_sweep",
            "research/p25/evidence/p25_v2_row_orientation_candidate_sweep_20260617.md",
            "p25_v2_row_orientation_candidate_sweep_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "value_payload_reality_ledger",
            "research/p25/evidence/p25_v2_value_payload_reality_ledger_20260616.md",
            "p25_v2_value_payload_reality_ledger_rows=1/1",
        ),
    )


def power_kernels() -> tuple[tuple[int, int], ...]:
    exponents = (2, 3, 4, 5, 6, 11, 13, 22, 39, 44, 75, 156, 169, 507, 780)
    return tuple((exponent, gcd(exponent, PM1)) for exponent in exponents)


def period_branch_gcds() -> tuple[tuple[int, int], ...]:
    periods = (39, 78, 156, 312, 507, 780)
    return tuple((period, gcd(pow(4, period) - 1, PM1)) for period in periods)


def debt_rows(kernels: dict[int, int], period_gcds: dict[int, int]) -> tuple[DebtRow, ...]:
    unique_powers = all(kernels[exponent] == 1 for exponent in (3, 5, 13, 39, 75, 169, 507))
    return (
        DebtRow(
            name="direct_one_edge_theorem",
            theorem_shape="one exact oriented row with scalar-fixed divisor/additive or period-156 value theorem",
            p25_debt="none at source stage",
            branch_count=1,
            decision="source_stage_candidate_if_theorem_present",
            first_missing_or_falsifier="no such theorem currently in hand",
            ok=True,
        ),
        DebtRow(
            name="row_labeled_orbit_theorem",
            theorem_shape="row-labeled four-row or parametric doubling-orbit theorem containing a legal row",
            p25_debt="choose labeled legal row, then normal source intake",
            branch_count=1,
            decision="normalize_to_one_labeled_row_then_intake",
            first_missing_or_falsifier="no row-labeled finite theorem currently in hand",
            ok=True,
        ),
        DebtRow(
            name="reciprocal_minus_boundary",
            theorem_shape="reciprocal row with explicit -Norm_156(Y_507) boundary",
            p25_debt="reciprocal orientation normalization only",
            branch_count=1,
            decision="normalize_reciprocal_then_intake",
            first_missing_or_falsifier="positive boundary or unspecified orientation is repair/reject",
            ok=True,
        ),
        DebtRow(
            name="bijective_power_value",
            theorem_shape="exact finite value theorem for R_m^e, e in {3,5,13,39,75,169,507}",
            p25_debt="unique F_p^* root because gcd(e,p-1)=1",
            branch_count=1,
            decision="normalize_unique_root_then_intake",
            first_missing_or_falsifier="powered divisor/H90 data without finite value still needs value normalization",
            ok=unique_powers,
        ),
        DebtRow(
            name="support_period156_value",
            theorem_shape="period-156 value theorem for one legal row",
            p25_debt="unique support-period branch because gcd(4^156-1,p-1)=1",
            branch_count=period_gcds[156],
            decision="source_stage_candidate_if_theorem_present",
            first_missing_or_falsifier="ambient-period value without period-156 context is repair",
            ok=period_gcds[156] == 1,
        ),
        DebtRow(
            name="ambient_period780_value",
            theorem_shape="ambient period-780 value, 11th power, or mu_11 quotient",
            p25_debt="mu_11 branch ambiguity",
            branch_count=period_gcds[780],
            decision="repair_period156_branch_context_missing",
            first_missing_or_falsifier="does not select one F_p support-period value",
            ok=period_gcds[780] == 11,
        ),
        DebtRow(
            name="projector_or_four_edge_components",
            theorem_shape="projector/character components reconstructing 4*edge",
            p25_debt="mu_4 fourth-root/scalar ambiguity",
            branch_count=kernels[4],
            decision="repair_selected_fourth_root_missing",
            first_missing_or_falsifier="constant plus boundary-zero components do not choose one oriented edge",
            ok=kernels[4] == 4,
        ),
        DebtRow(
            name="pair_diagonal_or_row_square",
            theorem_shape="two-edge pair, diagonal aggregate plus quotient, or row-square value",
            p25_debt="sign/oriented-square-root ambiguity",
            branch_count=kernels[2],
            decision="repair_oriented_square_root_missing",
            first_missing_or_falsifier="R and -R have same square and same divisor/H90 boundary",
            ok=kernels[2] == 2,
        ),
        DebtRow(
            name="q_square_exact_value",
            theorem_shape="exact scalar-fixed finite value for the Q square / 2*edge payload",
            p25_debt="two row-value roots plus extraction-map debt",
            branch_count=kernels[2],
            decision="bounded_payload_not_source_close_without_oriented_root_or_extraction",
            first_missing_or_falsifier="row-value roots are not A,x0 or vpp.py candidates",
            ok=kernels[2] == 2,
        ),
        DebtRow(
            name="zero_lattice_values_only",
            theorem_shape="exact row quotients or boundary-zero lattice basis values",
            p25_debt="absolute W-boundary row theorem missing",
            branch_count="n/a",
            decision="support_transfer_data_not_first_source_close",
            first_missing_or_falsifier="zero-boundary data compares rows but cannot create first absolute row value",
            ok=True,
        ),
        DebtRow(
            name="divisor_h90_up_to_scalar",
            theorem_shape="right divisor/H90 boundary but value only up to unspecified F_p^* scalar",
            p25_debt="full scalar normalization debt",
            branch_count=PM1,
            decision="repair_additive_or_value_normalization_missing",
            first_missing_or_falsifier="constants have zero divisor and zero H90 boundary",
            ok=PM1 > 10**20,
        ),
        DebtRow(
            name="finite_payload_without_source",
            theorem_shape="local finite row value, fixture, packet, or hash with no arithmetic source theorem",
            p25_debt="source theorem and DANGER3 framing missing",
            branch_count="n/a",
            decision="repair_arithmetic_source_theorem_missing",
            first_missing_or_falsifier="finite payload is verifier target/evidence, not a challenge-legal theorem",
            ok=True,
        ),
    )


def build_matrix() -> RepairDebtClosureMatrix:
    markers = evidence_markers()
    kernels_tuple = power_kernels()
    period_tuple = period_branch_gcds()
    kernels = dict(kernels_tuple)
    period_gcds = dict(period_tuple)
    rows = debt_rows(kernels, period_gcds)
    markers_ok = sum(row.ok for row in markers)
    unique_rows = sum(row.branch_count == 1 and row.decision != "repair_period156_branch_context_missing" for row in rows)
    bounded_rows = sum(row.branch_count in (2, 4, 11) for row in rows)
    scalar_rows = sum(row.branch_count == PM1 for row in rows)
    support_only = sum("support" in row.decision or "bounded_payload" in row.decision for row in rows)
    source_stage = 0
    submission_ready = 0
    row_ok = (
        P25 % 8 == 5
        and kernels_tuple
        == (
            (2, 2),
            (3, 1),
            (4, 4),
            (5, 1),
            (6, 2),
            (11, 11),
            (13, 1),
            (22, 22),
            (39, 1),
            (44, 44),
            (75, 1),
            (156, 4),
            (169, 1),
            (507, 1),
            (780, 4),
        )
        and period_tuple == ((39, 1), (78, 1), (156, 1), (312, 1), (507, 1), (780, 11))
        and markers_ok == len(markers)
        and len(rows) == 12
        and all(row.ok for row in rows)
        and unique_rows == 5
        and bounded_rows == 4
        and scalar_rows == 1
        and support_only == 2
        and source_stage == 0
        and submission_ready == 0
    )
    return RepairDebtClosureMatrix(
        markers=markers,
        rows=rows,
        power_kernels=kernels_tuple,
        period_branch_gcds=period_tuple,
        evidence_markers_ok=markers_ok,
        unique_normalization_rows=unique_rows,
        bounded_branch_repair_rows=bounded_rows,
        scalar_debt_rows=scalar_rows,
        support_only_rows=support_only,
        current_source_stage_closers=source_stage,
        current_submission_ready=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    matrix = build_matrix()
    print("p25 v2 repair-debt closure matrix")
    print(f"p={P25}")
    print(f"p_mod_8={P25 % 8}")
    print("power_kernels")
    for exponent, kernel in matrix.power_kernels:
        print(f"  e={exponent}: kernel={kernel}")
    print("period_branch_gcds")
    for period, value in matrix.period_branch_gcds:
        print(f"  period={period}: gcd={value}")
    print("markers")
    for marker_row in matrix.markers:
        print(f"  {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in matrix.rows:
        print(f"  {row.name}: decision={row.decision} branch_count={row.branch_count}")
        print(f"    shape={row.theorem_shape}")
        print(f"    debt={row.p25_debt}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={matrix.evidence_markers_ok}/{len(matrix.markers)}")
    print(f"  unique_normalization_rows={matrix.unique_normalization_rows}")
    print(f"  bounded_branch_repair_rows={matrix.bounded_branch_repair_rows}")
    print(f"  scalar_debt_rows={matrix.scalar_debt_rows}")
    print(f"  support_only_rows={matrix.support_only_rows}")
    print(f"  current_source_stage_closers={matrix.current_source_stage_closers}")
    print(f"  current_submission_ready={matrix.current_submission_ready}")
    print(f"p25_v2_repair_debt_closure_matrix_rows={int(matrix.row_ok)}/1")
    return 0 if matrix.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

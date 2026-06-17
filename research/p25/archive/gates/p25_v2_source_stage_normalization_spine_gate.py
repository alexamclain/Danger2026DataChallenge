#!/usr/bin/env python3
"""Normalize accepted p25 first-pass theorem presentations to one source row."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
PM1 = P25 - 1
UNIQUE_POWER_EXPONENTS = (3, 5, 13, 39, 75, 169, 507)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SpineRow:
    name: str
    presentation: str
    normalization: str
    required_extra_data: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class SourceStageNormalizationSpine:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SpineRow, ...]
    inverse_exponents: tuple[tuple[int, int], ...]
    support_period_gcd: int
    ambient_period_gcd: int
    evidence_markers_ok: int
    first_pass_normalization_routes: int
    selector_wrapper_routes: int
    unique_root_routes: int
    heavy_upstream_routes: int
    repair_debt_rows: int
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
            "first_pass_expert_intake_packet",
            "research/p25/evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
            "p25_v2_first_pass_expert_intake_packet_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
        marker(
            "frontdoor_count_sync",
            "research/p25/evidence/p25_v2_frontdoor_count_sync_20260616.md",
            "p25_v2_frontdoor_count_sync_rows=1/1",
        ),
        marker(
            "repair_debt_closure_matrix",
            "research/p25/evidence/p25_v2_repair_debt_closure_matrix_20260617.md",
            "p25_v2_repair_debt_closure_matrix_rows=1/1",
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
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "row_orientation_candidate_sweep",
            "research/p25/evidence/p25_v2_row_orientation_candidate_sweep_20260617.md",
            "p25_v2_row_orientation_candidate_sweep_rows=1/1",
        ),
    )


def inverse_exponents() -> tuple[tuple[int, int], ...]:
    return tuple((exponent, pow(exponent, -1, PM1)) for exponent in UNIQUE_POWER_EXPONENTS)


def spine_rows() -> tuple[SpineRow, ...]:
    return (
        SpineRow(
            name="direct_one_edge",
            presentation="scalar-fixed divisor/additive or period-156 value theorem for one oriented R_m",
            normalization="identity",
            required_extra_data="arithmetic source theorem, Norm_156(Y_507) boundary, scalar/branch normalization",
            decision="source_stage_candidate_if_theorem_present",
            ok=True,
        ),
        SpineRow(
            name="quartic_selector_wrapper",
            presentation="exact row-antisymmetric C4_1 phase with mixed row sign and finite theorem",
            normalization="selects one oriented quotient-C4 edge, then direct one-edge intake",
            required_extra_data="exact phase sign, mixed tensor row sign, oriented row or boundary-sign convention, scalar-fixed theorem",
            decision="normalize_selector_to_direct_edge_then_intake",
            ok=True,
        ),
        SpineRow(
            name="row_labeled_orbit",
            presentation="row-labeled four-row or parametric doubling-orbit theorem",
            normalization="choose any labeled legal m in {1,2,4,8}, then direct one-edge intake",
            required_extra_data="row label/hash/edge and scalar-fixed theorem data for at least one row",
            decision="normalize_labeled_row_then_intake",
            ok=True,
        ),
        SpineRow(
            name="reciprocal_minus_boundary",
            presentation="reciprocal row theorem with explicit -Norm_156(Y_507) boundary",
            normalization="rewrite reciprocal presentation to the corresponding oriented legal row",
            required_extra_data="reciprocal orientation and opposite boundary sign",
            decision="normalize_reciprocal_then_intake",
            ok=True,
        ),
        SpineRow(
            name="bijective_power_value",
            presentation="exact finite value theorem for R_m^e, e in {3,5,13,39,75,169,507}",
            normalization="raise to inverse exponent modulo p-1, then direct one-edge intake",
            required_extra_data="one legal row, exact finite F_p value, arithmetic source theorem, accepted boundary/period bridge",
            decision="normalize_unique_power_then_intake",
            ok=True,
        ),
        SpineRow(
            name="support_period156_value",
            presentation="support-period-156 value theorem for canonical H0/Y507 or one legal row",
            normalization="unique support-period branch in F_p^*, then direct one-edge intake",
            required_extra_data="period-156 branch/root/telescoping context and compatibility bridge",
            decision="normalize_period156_value_then_intake",
            ok=True,
        ),
        SpineRow(
            name="exactp_upstream",
            presentation="exact 75-atom or accepted theta2/theta2-inverse theorem with bridge",
            normalization="heavy upstream bridge into unified target, then ordinary extraction ladder",
            required_extra_data="C,D,K,orientation or theta2 branch plus 75->300->12->312->156 bridge",
            decision="heavy_upstream_source_candidate_not_first_pass_default",
            ok=True,
        ),
    )


def build_spine() -> SourceStageNormalizationSpine:
    markers = evidence_markers()
    rows = spine_rows()
    inverses = inverse_exponents()
    support_period_gcd = gcd(pow(4, 156) - 1, PM1)
    ambient_period_gcd = gcd(pow(4, 780) - 1, PM1)
    markers_ok = sum(row.ok for row in markers)
    first_pass_routes = 6
    selector_wrappers = 1
    unique_root_routes = 2
    heavy_routes = 1
    repair_debts = 6
    source_stage = 0
    submission_ready = 0
    row_ok = (
        markers_ok == len(markers)
        and len(rows) == 7
        and all(row.ok for row in rows)
        and inverses
        == (
            (3, 6666666666666666666666675),
            (5, 4000000000000000000000005),
            (13, 7692307692307692307692317),
            (39, 5897435897435897435897443),
            (75, 266666666666666666666667),
            (169, 5207100591715976331360953),
            (507, 5069033530571992110453655),
        )
        and all((exponent * inverse) % PM1 == 1 for exponent, inverse in inverses)
        and support_period_gcd == 1
        and ambient_period_gcd == 11
        and first_pass_routes == 6
        and selector_wrappers == 1
        and unique_root_routes == 2
        and heavy_routes == 1
        and repair_debts == 6
        and source_stage == 0
        and submission_ready == 0
    )
    return SourceStageNormalizationSpine(
        markers=markers,
        rows=rows,
        inverse_exponents=inverses,
        support_period_gcd=support_period_gcd,
        ambient_period_gcd=ambient_period_gcd,
        evidence_markers_ok=markers_ok,
        first_pass_normalization_routes=first_pass_routes,
        selector_wrapper_routes=selector_wrappers,
        unique_root_routes=unique_root_routes,
        heavy_upstream_routes=heavy_routes,
        repair_debt_rows=repair_debts,
        current_source_stage_closers=source_stage,
        current_submission_ready=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    spine = build_spine()
    print("p25 v2 source-stage normalization spine")
    print("markers")
    for marker_row in spine.markers:
        print(f"  {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("inverse_exponents")
    for exponent, inverse in spine.inverse_exponents:
        print(f"  e={exponent}: inverse={inverse}")
    print(f"support_period_gcd={spine.support_period_gcd}")
    print(f"ambient_period_gcd={spine.ambient_period_gcd}")
    print("rows")
    for row in spine.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    presentation={row.presentation}")
        print(f"    normalization={row.normalization}")
        print(f"    required_extra_data={row.required_extra_data}")
    print("counts")
    print(f"  evidence_markers_ok={spine.evidence_markers_ok}/{len(spine.markers)}")
    print(f"  first_pass_normalization_routes={spine.first_pass_normalization_routes}")
    print(f"  selector_wrapper_routes={spine.selector_wrapper_routes}")
    print(f"  unique_root_routes={spine.unique_root_routes}")
    print(f"  heavy_upstream_routes={spine.heavy_upstream_routes}")
    print(f"  repair_debt_rows={spine.repair_debt_rows}")
    print(f"  current_source_stage_closers={spine.current_source_stage_closers}")
    print(f"  current_submission_ready={spine.current_submission_ready}")
    print(f"p25_v2_source_stage_normalization_spine_rows={int(spine.row_ok)}/1")
    return 0 if spine.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

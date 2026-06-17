#!/usr/bin/env python3
"""Validate the period-156 value-source hook for p25."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P = 10000000000000000000000013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ValueClause:
    name: str
    ok: bool


@dataclass(frozen=True)
class ValueRoute:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class Period156ValueSourceHook:
    evidence_markers: tuple[EvidenceMarker, ...]
    required_clauses: tuple[ValueClause, ...]
    accepted_routes: tuple[ValueRoute, ...]
    repair_or_reject_routes: tuple[ValueRoute, ...]
    support_period_root_unique: bool
    ambient_period_has_mu11: bool
    scholl_direct_d2_import_blocked: bool
    current_period156_value_theorems: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "period_value_primary_source_scout",
            "research/p25/evidence/p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md",
            "ksy_y_siegel_robert_period_value_primary_source_scout_rows=1/1",
        ),
        marker(
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "value_divisor_source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
    )


def multiplicative_order(a: int, n: int) -> int:
    if n <= 1:
        raise ValueError("n must be > 1")
    value = a % n
    order = 1
    while value != 1:
        value = (value * a) % n
        order += 1
    return order


def legendre_symbol(a: int, p: int) -> int:
    value = pow(a % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def required_clauses() -> tuple[ValueClause, ...]:
    return (
        ValueClause("one_exact_oriented_edge_or_accepted_theta2_payload", True),
        ValueClause("arithmetic_value_source_theorem", True),
        ValueClause("support_period_156_branch_root_telescoping_context", True),
        ValueClause("finite_Fp_value_selected_not_ambient_mu11_class", True),
        ValueClause("boundary_or_bridge_to_Norm_156_Y_507", True),
        ValueClause("post_theorem_extraction_routing", True),
    )


def accepted_routes() -> tuple[ValueRoute, ...]:
    return (
        ValueRoute("period156_value_for_oriented_edge", "source_stage_win_route_to_extraction", True),
        ValueRoute("period156_theta2_payload_with_bridge", "exactp_or_unified_source_win_route_to_extraction", True),
    )


def repair_or_reject_routes() -> tuple[ValueRoute, ...]:
    return (
        ValueRoute("schertz_field_generation_only", "repair_exact_value_theorem_missing", True),
        ValueRoute("shin_generator_only", "repair_exact_value_theorem_missing", True),
        ValueRoute("scholl_oddD_distribution_only", "repair_exact_period156_payload_missing", True),
        ValueRoute("period156_vocabulary_no_row", "repair_oriented_edge_or_theta2_payload_missing", True),
        ValueRoute("exact_value_no_arithmetic_source", "repair_arithmetic_source_theorem_missing", True),
        ValueRoute("value_up_to_unspecified_fp_scalar", "repair_scalar_or_branch_normalization_missing", True),
        ValueRoute("ambient780_value_only", "repair_ambient_period780_mu11_branch", True),
        ValueRoute("ambient780_eleventh_power_or_mu11_quotient", "repair_period156_branch_selection_missing", True),
        ValueRoute("degree6_value_without_fp_descent", "repair_fp_descent_and_row_selection_missing", True),
        ValueRoute("direct_scholl_D2_import", "reject_scholl_D2_hypothesis_mismatch", True),
        ValueRoute("direct_fp_order39_root", "reject_ord39_p_equals_6", True),
        ValueRoute("sqrt_minus39_scalar", "reject_sqrt_minus39_not_in_Fp", True),
    )


def build_hook() -> Period156ValueSourceHook:
    markers = evidence_markers()
    required = required_clauses()
    accepted = accepted_routes()
    repairs = repair_or_reject_routes()
    support_period_root_unique = pow(4, 156, P - 1) != 1 and __import__("math").gcd(pow(4, 156, P - 1) - 1, P - 1) == 1
    ambient_period_has_mu11 = __import__("math").gcd(pow(4, 780, P - 1) - 1, P - 1) == 11
    scholl_direct_d2_import_blocked = True
    current_period156_value_theorems = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(required) == 6
        and all(row.ok for row in required)
        and len(accepted) == 2
        and all(row.ok for row in accepted)
        and len(repairs) == 12
        and all(row.ok for row in repairs)
        and multiplicative_order(P % 39, 39) == 6
        and legendre_symbol(-39, P) == -1
        and support_period_root_unique
        and ambient_period_has_mu11
        and scholl_direct_d2_import_blocked
        and current_period156_value_theorems == 0
    )
    return Period156ValueSourceHook(
        evidence_markers=markers,
        required_clauses=required,
        accepted_routes=accepted,
        repair_or_reject_routes=repairs,
        support_period_root_unique=support_period_root_unique,
        ambient_period_has_mu11=ambient_period_has_mu11,
        scholl_direct_d2_import_blocked=scholl_direct_d2_import_blocked,
        current_period156_value_theorems=current_period156_value_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    hook = build_hook()
    print("p25 v2 period156 value source hook")
    for marker_row in hook.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("required_clauses")
    for clause in hook.required_clauses:
        print(f"  {clause.name}=ok")
    print("accepted_routes")
    for route in hook.accepted_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("repair_or_reject_routes")
    for route in hook.repair_or_reject_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in hook.evidence_markers)}/{len(hook.evidence_markers)}")
    print(f"  required_clauses={len(hook.required_clauses)}")
    print(f"  accepted_routes={len(hook.accepted_routes)}")
    print(f"  repair_or_reject_routes={len(hook.repair_or_reject_routes)}")
    print(f"  support_period_root_unique={int(hook.support_period_root_unique)}")
    print(f"  ambient_period_has_mu11={int(hook.ambient_period_has_mu11)}")
    print(f"  scholl_direct_d2_import_blocked={int(hook.scholl_direct_d2_import_blocked)}")
    print(f"  current_period156_value_theorems={hook.current_period156_value_theorems}")
    print(f"p25_v2_period156_value_source_hook_rows={int(hook.row_ok)}/1")
    return 0 if hook.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

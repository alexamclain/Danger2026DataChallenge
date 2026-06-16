#!/usr/bin/env python3
"""Source-theorem obligation matrix for the external p25 moonshot.

The external end-to-end audit shows that the first missing item is still an
actual source-stage theorem.  This gate turns the five live source front doors
into explicit theorem obligations and a conservative search order.  H0 and
conductor-39 are first-pass targets because their source objects are already
certified and the desired divisor/additive theorem avoids the period-156 value
branch.  Exact-P remains a high-payoff heavier target; twisted/H90 and the
curved corner remain live but carry period-156 context.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_bridge_resolution_queue_gate import (
    profile_external_bridge_resolution_queue,
)
from p25_ksy_y_external_end_to_end_route_audit_gate import (
    profile_external_end_to_end_route_audit,
)
from p25_ksy_y_external_frontdoor_query_packet_gate import (
    profile_external_frontdoor_query_packet,
)
from p25_ksy_y_frontdoor_local_source_scan_gate import (
    profile_frontdoor_local_source_scan,
)
from p25_ksy_y_source_frontdoor_router_gate import (
    profile_source_frontdoor_router,
)
from p25_ksy_y_source_theorem_priority_selector_gate import (
    profile_source_theorem_priority_selector,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_end_to_end_route_audit_20260614.md",
        "ksy_y_external_end_to_end_route_audit_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_bridge_resolution_queue_20260614.md",
        "ksy_y_external_bridge_resolution_queue_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_source_frontdoor_router_20260614.md",
        "ksy_y_source_frontdoor_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_source_theorem_priority_selector_20260614.md",
        "ksy_y_source_theorem_priority_selector_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_query_packet_20260614.md",
        "ksy_y_external_frontdoor_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_frontdoor_local_source_scan_20260614.md",
        "ksy_y_frontdoor_local_source_scan_rows=1/1",
    ),
)


@dataclass(frozen=True)
class SourceTheoremObligationRow:
    name: str
    frontdoor: str
    odd_target: str
    search_order: int
    source_object_certified: bool
    exact_object_named: bool
    divisor_additive_preferred: bool
    needs_period156_context: bool
    local_source_direct_hit: bool
    current_source_theorem_exists: bool
    source_stage_closes_if_yes: bool
    downstream_route_ready: bool
    selected_first_pass: bool
    high_payoff_heavy: bool
    required_clauses: tuple[str, ...]
    first_falsifier: str
    candidate_intake_gate: str
    next_probe: str
    ok: bool


@dataclass(frozen=True)
class ExternalSourceTheoremObligationMatrix:
    dependency_markers_present: int
    dependency_markers_total: int
    external_end_to_end_ok: bool
    external_resolution_ok: bool
    source_frontdoor_router_ok: bool
    priority_selector_ok: bool
    external_query_packet_ok: bool
    local_source_scan_ok: bool
    rows: tuple[SourceTheoremObligationRow, ...]
    row_count: int
    source_object_certified_rows: int
    exact_object_named_rows: int
    divisor_additive_preferred_rows: int
    needs_period156_context_rows: int
    local_source_direct_hit_rows: int
    current_source_theorem_rows: int
    source_stage_closes_if_yes_rows: int
    downstream_route_ready_rows: int
    selected_first_pass_rows: int
    high_payoff_heavy_rows: int
    total_required_clause_count: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def obligation_rows() -> tuple[SourceTheoremObligationRow, ...]:
    return (
        SourceTheoremObligationRow(
            name="h0_divisor_additive_boundary",
            frontdoor="H0/Yang/Kubert-Lang",
            odd_target="canonical_H0/H0_translate/Y_507",
            search_order=1,
            source_object_certified=True,
            exact_object_named=True,
            divisor_additive_preferred=True,
            needs_period156_context=False,
            local_source_direct_hit=False,
            current_source_theorem_exists=False,
            source_stage_closes_if_yes=True,
            downstream_route_ready=True,
            selected_first_pass=True,
            high_payoff_heavy=False,
            required_clauses=(
                "one exact legal 78-over-78 H0 or H0-translate product",
                "finite divisor/additive identity",
                "Hilbert-90 boundary to Norm_156(Y_507)",
                "challenge-legal arithmetic source theorem",
            ),
            first_falsifier="source legality only, value without period-156 context, or missing H90 boundary",
            candidate_intake_gate="p25_ksy_y_h0_candidate_packet_intake_gate.py",
            next_probe="search/ask for exact H0 divisor-additive identity with H90 boundary",
            ok=True,
        ),
        SourceTheoremObligationRow(
            name="conductor39_divisor_additive_identity",
            frontdoor="mixed conductor-39 unit / Yang distribution",
            odd_target="conductor39_U_chi",
            search_order=1,
            source_object_certified=True,
            exact_object_named=True,
            divisor_additive_preferred=True,
            needs_period156_context=False,
            local_source_direct_hit=False,
            current_source_theorem_exists=False,
            source_stage_closes_if_yes=True,
            downstream_route_ready=True,
            selected_first_pass=True,
            high_payoff_heavy=False,
            required_clauses=(
                "U_chi/W mixed conductor-39 object",
                "chi_3 tensor chi_13 non-projection structure",
                "Yang lift to the level-507 period norm",
                "Hilbert-90 or ratio descent",
                "finite divisor/additive identity",
            ),
            first_falsifier="prime projection, axis-only statement, or source certification without finite theorem",
            candidate_intake_gate="p25_ksy_y_conductor39_source_theorem_intake_gate.py",
            next_probe="search/ask for U_chi/W divisor-additive theorem preserving Yang lift and descent",
            ok=True,
        ),
        SourceTheoremObligationRow(
            name="exact75_product_divisor_theorem",
            frontdoor="Kubert-Lang / KSY exact normalized-y product",
            odd_target="exact_P",
            search_order=2,
            source_object_certified=False,
            exact_object_named=True,
            divisor_additive_preferred=True,
            needs_period156_context=False,
            local_source_direct_hit=False,
            current_source_theorem_exists=False,
            source_stage_closes_if_yes=True,
            downstream_route_ready=True,
            selected_first_pass=False,
            high_payoff_heavy=True,
            required_clauses=(
                "exact P product",
                "mixed C_3 x C_169 source graph",
                "all 75 K-traced normalized-y atoms with equal weight",
                "theta2/theta2-inverse orientation branch",
                "finite divisor/additive theorem from an arithmetic source",
            ),
            first_falsifier="field generation, one y-value, subset/nonuniform atom product, or missing orientation",
            candidate_intake_gate=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py"
            ),
            next_probe="search/ask only for an all-75 exact product theorem, not an atom enumeration",
            ok=True,
        ),
        SourceTheoremObligationRow(
            name="twisted_h90_period156_theorem",
            frontdoor="twisted ratio / Hilbert-90",
            odd_target="U_507/Y_507",
            search_order=3,
            source_object_certified=True,
            exact_object_named=True,
            divisor_additive_preferred=True,
            needs_period156_context=True,
            local_source_direct_hit=False,
            current_source_theorem_exists=False,
            source_stage_closes_if_yes=True,
            downstream_route_ready=True,
            selected_first_pass=False,
            high_payoff_heavy=False,
            required_clauses=(
                "twisted ratio or Hilbert-90 object",
                "finite value or divisor theorem",
                "support-period-156 branch/root/telescoping context",
                "arithmetic source theorem",
            ),
            first_falsifier="H90 vocabulary without finite theorem and period-156 bridge context",
            candidate_intake_gate="p25_ksy_y_twisted_h90_candidate_packet_intake_gate.py",
            next_probe="search/ask for twisted/H90 finite theorem with explicit period-156 context",
            ok=True,
        ),
        SourceTheoremObligationRow(
            name="curved_corner_period156_theorem",
            frontdoor="unit-triangle curved K-traced corner",
            odd_target="curved_corner",
            search_order=3,
            source_object_certified=False,
            exact_object_named=True,
            divisor_additive_preferred=True,
            needs_period156_context=True,
            local_source_direct_hit=False,
            current_source_theorem_exists=False,
            source_stage_closes_if_yes=True,
            downstream_route_ready=True,
            selected_first_pass=False,
            high_payoff_heavy=False,
            required_clauses=(
                "exact unit-triangle curved K-traced corner",
                "finite value or divisor theorem",
                "support-period-156 context",
                "challenge-legal arithmetic source theorem",
            ),
            first_falsifier="curved helper only, wrong unit triangle, or theorem without period-156 context",
            candidate_intake_gate="p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py",
            next_probe="search/ask for unit-triangle curved-corner theorem, not helper-only geometry",
            ok=True,
        ),
    )


def profile_external_source_theorem_obligation_matrix() -> ExternalSourceTheoremObligationMatrix:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    external_end_to_end = profile_external_end_to_end_route_audit()
    resolution = profile_external_bridge_resolution_queue()
    frontdoor = profile_source_frontdoor_router()
    priority = profile_source_theorem_priority_selector()
    query = profile_external_frontdoor_query_packet()
    local_scan = profile_frontdoor_local_source_scan()
    rows = obligation_rows()
    certified = sum(row.source_object_certified for row in rows)
    exact_named = sum(row.exact_object_named for row in rows)
    divisor = sum(row.divisor_additive_preferred for row in rows)
    period = sum(row.needs_period156_context for row in rows)
    local_hit = sum(row.local_source_direct_hit for row in rows)
    current_source = sum(row.current_source_theorem_exists for row in rows)
    closes = sum(row.source_stage_closes_if_yes for row in rows)
    downstream = sum(row.downstream_route_ready for row in rows)
    first_pass = sum(row.selected_first_pass for row in rows)
    heavy = sum(row.high_payoff_heavy for row in rows)
    clause_count = sum(len(row.required_clauses) for row in rows)
    search_orders = tuple(row.search_order for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and external_end_to_end.row_ok
        and external_end_to_end.current_evidence_rows == 1
        and external_end_to_end.active_frontdoor_rows == 5
        and external_end_to_end.current_submission_ready_rows == 0
        and resolution.row_ok
        and resolution.active_frontdoor_rows == 5
        and resolution.direct_closing_rows == 0
        and frontdoor.row_ok
        and frontdoor.source_closing_shape_rows == 5
        and frontdoor.current_source_theorem_rows == 0
        and priority.row_ok
        and priority.priority1_rows == 3
        and query.row_ok
        and query.closing_query_rows == 5
        and query.current_source_theorem_rows == 0
        and local_scan.row_ok
        and local_scan.local_source_closing_hits == 0
        and len(rows) == 5
        and certified == 3
        and exact_named == 5
        and divisor == 5
        and period == 2
        and local_hit == 0
        and current_source == 0
        and closes == 5
        and downstream == 5
        and first_pass == 2
        and heavy == 1
        and clause_count == 22
        and search_orders == (1, 1, 2, 3, 3)
        and all(row.ok for row in rows)
    )
    return ExternalSourceTheoremObligationMatrix(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_end_to_end_ok=external_end_to_end.row_ok,
        external_resolution_ok=resolution.row_ok,
        source_frontdoor_router_ok=frontdoor.row_ok,
        priority_selector_ok=priority.row_ok,
        external_query_packet_ok=query.row_ok,
        local_source_scan_ok=local_scan.row_ok,
        rows=rows,
        row_count=len(rows),
        source_object_certified_rows=certified,
        exact_object_named_rows=exact_named,
        divisor_additive_preferred_rows=divisor,
        needs_period156_context_rows=period,
        local_source_direct_hit_rows=local_hit,
        current_source_theorem_rows=current_source,
        source_stage_closes_if_yes_rows=closes,
        downstream_route_ready_rows=downstream,
        selected_first_pass_rows=first_pass,
        high_payoff_heavy_rows=heavy,
        total_required_clause_count=clause_count,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_source_theorem_obligation_matrix()
    print("p25 KSY-y external source-theorem obligation matrix gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_end_to_end_ok={int(profile.external_end_to_end_ok)}")
    print(f"  external_resolution_ok={int(profile.external_resolution_ok)}")
    print(f"  source_frontdoor_router_ok={int(profile.source_frontdoor_router_ok)}")
    print(f"  priority_selector_ok={int(profile.priority_selector_ok)}")
    print(f"  external_query_packet_ok={int(profile.external_query_packet_ok)}")
    print(f"  local_source_scan_ok={int(profile.local_source_scan_ok)}")
    print("obligation_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: order={row.search_order} frontdoor={row.frontdoor} "
            f"odd={row.odd_target} certified={int(row.source_object_certified)} "
            f"exact={int(row.exact_object_named)} divisor={int(row.divisor_additive_preferred)} "
            f"period156={int(row.needs_period156_context)} "
            f"local_hit={int(row.local_source_direct_hit)} "
            f"current={int(row.current_source_theorem_exists)} "
            f"closes={int(row.source_stage_closes_if_yes)} "
            f"downstream={int(row.downstream_route_ready)} "
            f"first_pass={int(row.selected_first_pass)} heavy={int(row.high_payoff_heavy)}"
        )
        print(f"    clauses={'; '.join(row.required_clauses)}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    intake={row.candidate_intake_gate}")
        print(f"    next={row.next_probe}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_object_certified_rows={profile.source_object_certified_rows}")
    print(f"  exact_object_named_rows={profile.exact_object_named_rows}")
    print(f"  divisor_additive_preferred_rows={profile.divisor_additive_preferred_rows}")
    print(f"  needs_period156_context_rows={profile.needs_period156_context_rows}")
    print(f"  local_source_direct_hit_rows={profile.local_source_direct_hit_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  source_stage_closes_if_yes_rows={profile.source_stage_closes_if_yes_rows}")
    print(f"  downstream_route_ready_rows={profile.downstream_route_ready_rows}")
    print(f"  selected_first_pass_rows={profile.selected_first_pass_rows}")
    print(f"  high_payoff_heavy_rows={profile.high_payoff_heavy_rows}")
    print(f"  total_required_clause_count={profile.total_required_clause_count}")
    print("interpretation")
    print("  h0_and_conductor39_are_first_pass_source_theorem_targets=1")
    print("  exactP_is_high_payoff_but_heavier_than_certified_source_objects=1")
    print("  twisted_and_curved_routes_remain_live_with_period156_context=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(
        "ksy_y_external_source_theorem_obligation_matrix_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("external source-theorem obligation matrix regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

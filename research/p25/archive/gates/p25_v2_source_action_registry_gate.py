#!/usr/bin/env python3
"""Current source-action registry for p25 v2.

This gate consolidates the post-reorganization source-search state.  It is not
a new source scan; it records which source actions are still live after the
Koo-Shin access closure, external KL/Schertz boundaries, Sprang theta2 intake,
Q-route source scan, and current expert/snippet routers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceActionRow:
    name: str
    status: str
    live_action: str
    discard_condition: str
    source_stage_closer: bool
    broad_reread_allowed: bool
    ok: bool


@dataclass(frozen=True)
class SourceActionRegistry:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceActionRow, ...]
    markers_ok: int
    live_theorem_asks: int
    stale_actions_closed: int
    support_only_rows: int
    broad_reread_allowed_rows: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "value_divisor_source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "koo_shin_access_blocker_closure",
            "research/p25/evidence/p25_v2_koo_shin_access_blocker_closure_20260616.md",
            "p25_v2_koo_shin_access_blocker_closure_rows=1/1",
        ),
        marker(
            "kubert_lang_external_source_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
            "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
        ),
        marker(
            "schertz_scholl_external_source_boundary",
            "research/p25/evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
            "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
        ),
        marker(
            "sprang_theta2_source_intake",
            "research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
            "p25_v2_sprang_theta2_source_intake_rows=1/1",
        ),
        marker(
            "q_route_source_hook_scan",
            "research/p25/evidence/p25_v2_q_route_source_hook_scan_20260616.md",
            "p25_v2_q_route_source_hook_scan_rows=1/1",
        ),
        marker(
            "support_lane_router",
            "research/p25/evidence/p25_v2_support_lane_router_20260616.md",
            "p25_v2_support_lane_router_rows=1/1",
        ),
        marker(
            "primitive_character_power_recheck",
            "research/p25/evidence/p25_v2_primitive_character_power_recheck_20260617.md",
            "p25_v2_primitive_character_power_recheck_rows=1/1",
        ),
    )


def source_action_rows() -> tuple[SourceActionRow, ...]:
    return (
        SourceActionRow(
            name="first_pass_h0_conductor39",
            status="live_primary_theorem_ask",
            live_action="find scalar-fixed finite divisor/additive theorem, or exact uniquely invertible power-value theorem, for one legal support-156 row with Norm_156(Y_507) boundary",
            discard_condition="source legality, boundary-only, selector-only, ambiguous power value, finite payload without source, or broad source-family reread",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="period156_h0_y507_value",
            status="live_support_theorem_ask",
            live_action="find period-156 H0/Y507 value theorem with branch/root/telescoping or additive normalization",
            discard_condition="Schertz/Shin/Scholl generator language, ambient period-780 value, mu_11 quotient, or direct Scholl D=2 import",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="exactp_heavy_route",
            status="live_heavy_theorem_ask",
            live_action="find exact 75-atom, compact C,D,K,orientation, primitive-word, mixed-selector, or theta2 payload theorem",
            discard_condition="KSY vocabulary, raw KL exponent balance, generic modular-unit generation, or branchless orientation",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="koo_shin_2010",
            status="stale_access_action_closed",
            live_action="accept only a new theorem-shaped Koo-Shin snippet through source-snippet intake",
            discard_condition="treating PDF/OCR retrieval as live or treating Theorem 5.2/6.1/6.2 as finite p25 theorem without new clauses",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="sprang_d2_theta",
            status="support_only",
            live_action="continue only on exact p25 theta2/theta2-inverse divisor-additive specialization with period-156 bridge",
            discard_condition="broad D=2, p-adic theta, de Rham polylog, kernel distribution, or cohomology vocabulary",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="kubert_lang",
            status="support_only",
            live_action="continue only on exact primitive word, mixed C3 x C169 selector, or accepted theta2 payload theorem",
            discard_condition="KL generator theory, generic unit generation, theorem-K congruence context, or C169 projection data",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="conductor39_q_route",
            status="support_only",
            live_action="continue only on finite Q value theorem with period-156 context, Q3 H90 theorem, oriented diagonal split, or exact primitive-unit value theorem tied to one legal row",
            discard_condition="Q source-only, Q6 boundary-only, primitive-power-only, U_chi/V_bal exponent relation only, pure degree-6 norm, or local generic Q language",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
        SourceActionRow(
            name="twisted_h90_curved_corner",
            status="support_only",
            live_action="route exact support-lane snippets through period-156 value hook and source-snippet intake",
            discard_condition="broad H90, norm, curved product, or unit-triangle vocabulary without exact source object and period-156 data",
            source_stage_closer=False,
            broad_reread_allowed=False,
            ok=True,
        ),
    )


def build_registry() -> SourceActionRegistry:
    markers = evidence_markers()
    rows = source_action_rows()
    live_theorem_asks = sum("theorem_ask" in row.status for row in rows)
    stale_actions_closed = sum(row.status == "stale_access_action_closed" for row in rows)
    support_only_rows = sum(row.status == "support_only" for row in rows)
    broad_reread_allowed_rows = sum(row.broad_reread_allowed for row in rows)
    current_source_stage_closers = sum(row.source_stage_closer for row in rows)
    current_submission_ready = 0
    expected_statuses = (
        "live_primary_theorem_ask",
        "live_support_theorem_ask",
        "live_heavy_theorem_ask",
        "stale_access_action_closed",
        "support_only",
        "support_only",
        "support_only",
        "support_only",
    )
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and tuple(row.status for row in rows) == expected_statuses
        and live_theorem_asks == 3
        and stale_actions_closed == 1
        and support_only_rows == 4
        and broad_reread_allowed_rows == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
        and all(row.ok for row in rows)
    )
    return SourceActionRegistry(
        markers=markers,
        rows=rows,
        markers_ok=sum(marker_row.ok for marker_row in markers),
        live_theorem_asks=live_theorem_asks,
        stale_actions_closed=stale_actions_closed,
        support_only_rows=support_only_rows,
        broad_reread_allowed_rows=broad_reread_allowed_rows,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    registry = build_registry()
    print("p25 v2 source-action registry")
    for marker_row in registry.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in registry.rows:
        print(f"  {row.name}: status={row.status}")
        print(f"    live_action={row.live_action}")
        print(f"    discard_condition={row.discard_condition}")
        print(f"    source_stage_closer={int(row.source_stage_closer)}")
        print(f"    broad_reread_allowed={int(row.broad_reread_allowed)}")
    print("counts")
    print(f"  markers_ok={registry.markers_ok}/{len(registry.markers)}")
    print(f"  live_theorem_asks={registry.live_theorem_asks}")
    print(f"  stale_actions_closed={registry.stale_actions_closed}")
    print(f"  support_only_rows={registry.support_only_rows}")
    print(f"  broad_reread_allowed_rows={registry.broad_reread_allowed_rows}")
    print(f"  current_source_stage_closers={registry.current_source_stage_closers}")
    print(f"  current_submission_ready={registry.current_submission_ready}")
    print("interpretation")
    print("  no_broad_source_reread_is_currently_actionable=1")
    print("  source_queue_is_theorem_shaped=1")
    print(f"p25_v2_source_action_registry_rows={int(registry.row_ok)}/1")
    return 0 if registry.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

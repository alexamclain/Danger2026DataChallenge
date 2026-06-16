#!/usr/bin/env python3
"""Post-local-source queue for the p25 value-side theorem hunt.

The local product-source queue covers KSY, Kubert-Lang, Sprang, and Koo-Shin
as exact-product sources.  Schertz/Shin live on the adjacent value side: they
are useful as Siegel-Robert/Siegel-Ramachandra vocabulary, but only an exact
finite-field value identity for the p25 product P with period-156 context can
advance the moonshot.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class ValueSideBoundaryRow:
    name: str
    boundary_artifact: Path
    current_status: str
    decision: str
    killed_as_direct_closer: bool
    conditional_only: bool
    active_closing_target: bool
    ambient_780_rejected: bool
    first_acceptable_upgrade: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ValueSideRouterRow:
    name: str
    router_artifact: Path
    accepted_payload: str
    reject_clause: str
    ok: bool


@dataclass(frozen=True)
class PostLocalSourceValueSideQueue:
    source_rows: tuple[ValueSideBoundaryRow, ...]
    router_rows: tuple[ValueSideRouterRow, ...]
    killed_direct_rows: int
    conditional_rows: int
    active_closing_target_rows: int
    ambient_780_rejected_rows: int
    router_rows_present: int
    heavy_value_harness_required_for_queue_gate: bool
    row_ok: bool


def value_side_boundary_rows() -> tuple[ValueSideBoundaryRow, ...]:
    scout = RESEARCH / "p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md"
    return (
        ValueSideBoundaryRow(
            name="schertz_shin_generator_boundary",
            boundary_artifact=scout,
            current_status="class-field generators from elliptic units / Siegel-Ramachandra invariants",
            decision="reject_field_generation_not_value_theorem",
            killed_as_direct_closer=True,
            conditional_only=False,
            active_closing_target=False,
            ambient_780_rejected=False,
            first_acceptable_upgrade="exact finite-field value identity for P, preserving the mixed graph",
            first_falsifier="field generation, invariant generation, or generic unit vocabulary without exact P",
            ok=True,
        ),
        ValueSideBoundaryRow(
            name="siegel_robert_bare_exact_value",
            boundary_artifact=scout,
            current_status="hypothetical exact value without support-period branch/root context",
            decision="conditional_missing_period_156_context",
            killed_as_direct_closer=False,
            conditional_only=True,
            active_closing_target=False,
            ambient_780_rejected=False,
            first_acceptable_upgrade="period-156 branch/root/telescoping context for the exact P value",
            first_falsifier="bare finite-field value that leaves the p25 root branch unspecified",
            ok=True,
        ),
        ValueSideBoundaryRow(
            name="siegel_robert_ambient_780_value",
            boundary_artifact=scout,
            current_status="ambient period-780 value has an 11-branch F_p^* ambiguity",
            decision="reject_ambient_780_mu11_branch",
            killed_as_direct_closer=True,
            conditional_only=False,
            active_closing_target=False,
            ambient_780_rejected=True,
            first_acceptable_upgrade="support-period 156 fixedness, where gcd(4^156 - 1, p - 1) = 1",
            first_falsifier="ambient-period value only, where gcd(4^780 - 1, p - 1) = 11",
            ok=True,
        ),
        ValueSideBoundaryRow(
            name="siegel_robert_exact_value_with_period_156",
            boundary_artifact=scout,
            current_status="active value-side theorem target, not yet supplied by inspected sources",
            decision="active_value_side_target",
            killed_as_direct_closer=False,
            conditional_only=False,
            active_closing_target=True,
            ambient_780_rejected=False,
            first_acceptable_upgrade="named source theorem giving exact P as a finite-field value with period-156 context",
            first_falsifier="exact value theorem that drops the mixed graph, orientation, P, or finite-field framing",
            ok=True,
        ),
    )


def value_side_router_rows() -> tuple[ValueSideRouterRow, ...]:
    return (
        ValueSideRouterRow(
            name="period_value_upgrade",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py",
            accepted_payload="exact P value, mixed graph, finite-field identity, and period-156 context",
            reject_clause="field generation, bare value, ambient 780 value, or missing mixed graph",
            ok=True,
        ),
        ValueSideRouterRow(
            name="source_claim_intake",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py",
            accepted_payload="exact finite-field value P with mixed graph and period-156 context",
            reject_clause="source language that is not an exact P closure theorem",
            ok=True,
        ),
        ValueSideRouterRow(
            name="theorem_hit_router_raw_value",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py",
            accepted_payload="raw-value theorem hit with raw C/D/K geometry and period-156 context",
            reject_clause="ambient value, wrong raw geometry, or exponent balance only",
            ok=True,
        ),
        ValueSideRouterRow(
            name="exact_product_intake",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py",
            accepted_payload="exact P payload with mixed graph, equal weights, orientation, and legal framing",
            reject_clause="finite verifier payload without an arithmetic source theorem",
            ok=True,
        ),
        ValueSideRouterRow(
            name="closing_theorem_obligation",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py",
            accepted_payload="source theorem, DANGER3 framing, extraction path, and vpp-verified triple",
            reject_clause="value theorem alone without policy/extraction/submission closure",
            ok=True,
        ),
    )


def profile_post_local_source_value_side_queue() -> PostLocalSourceValueSideQueue:
    sources = value_side_boundary_rows()
    routers = value_side_router_rows()
    killed = sum(row.killed_as_direct_closer for row in sources)
    conditional = sum(row.conditional_only for row in sources)
    active = sum(row.active_closing_target for row in sources)
    ambient = sum(row.ambient_780_rejected for row in sources)
    source_present = all(
        row.boundary_artifact.exists() and row.boundary_artifact.stat().st_size > 0
        for row in sources
    )
    router_present = sum(
        row.router_artifact.exists() and row.router_artifact.stat().st_size > 0
        for row in routers
    )
    row_ok = (
        source_present
        and router_present == 5
        and killed == 2
        and conditional == 1
        and active == 1
        and ambient == 1
        and all(row.ok for row in sources)
        and all(row.ok for row in routers)
    )
    return PostLocalSourceValueSideQueue(
        source_rows=sources,
        router_rows=routers,
        killed_direct_rows=killed,
        conditional_rows=conditional,
        active_closing_target_rows=active,
        ambient_780_rejected_rows=ambient,
        router_rows_present=router_present,
        heavy_value_harness_required_for_queue_gate=False,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_local_source_value_side_queue()
    print("p25 KSY-y post-local-source value-side queue gate")
    print("source_boundaries")
    for row in profile.source_rows:
        print(
            "  "
            f"{row.name}: killed={int(row.killed_as_direct_closer)} "
            f"conditional={int(row.conditional_only)} "
            f"active={int(row.active_closing_target)} "
            f"ambient_reject={int(row.ambient_780_rejected)} "
            f"artifact={row.boundary_artifact}"
        )
        print(f"    decision={row.decision}")
        print(f"    status={row.current_status}")
        print(f"    upgrade={row.first_acceptable_upgrade}")
        print(f"    falsifier={row.first_falsifier}")
    print("value_side_routers")
    for row in profile.router_rows:
        print(f"  {row.name}: artifact={row.router_artifact}")
        print(f"    accept={row.accepted_payload}")
        print(f"    reject={row.reject_clause}")
    print("counts")
    print(f"  killed_direct_rows={profile.killed_direct_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  active_closing_target_rows={profile.active_closing_target_rows}")
    print(f"  ambient_780_rejected_rows={profile.ambient_780_rejected_rows}")
    print(f"  router_rows_present={profile.router_rows_present}")
    print(
        "  heavy_value_harness_required_for_queue_gate="
        f"{int(profile.heavy_value_harness_required_for_queue_gate)}"
    )
    print("interpretation")
    print("  schertz_shin_are_boundary_artifacts_not_broad_reread_targets=1")
    print("  value_side_win_requires_exact_P_value_with_period_156_context=1")
    print("  ambient_780_value_is_not_a_closing_theorem_due_to_mu11_branch=1")
    print(
        "ksy_y_post_local_source_value_side_queue_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("post-local-source value-side queue regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

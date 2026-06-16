#!/usr/bin/env python3
"""Post-local-source queue for the exact p25 product theorem hunt.

The local Sprang, KL, KSY, and Koo-Shin source passes have now separated source
vocabulary from actual p25 payloads.  This gate records the remaining search
queue and the intake routers for any future theorem/literature hit.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class SourceBoundaryRow:
    name: str
    boundary_artifact: Path
    current_status: str
    killed_as_direct_closer: bool
    watchlist_only: bool
    first_acceptable_upgrade: str
    first_falsifier: str
    ok: bool


@dataclass(frozen=True)
class IntakeRouterRow:
    name: str
    router_artifact: Path
    accepted_payload: str
    reject_clause: str
    ok: bool


@dataclass(frozen=True)
class PostLocalSourceExactProductQueue:
    source_rows: tuple[SourceBoundaryRow, ...]
    router_rows: tuple[IntakeRouterRow, ...]
    killed_direct_rows: int
    watchlist_rows: int
    active_external_search_rows: int
    router_rows_present: int
    heavy_finite_harness_required_for_queue_gate: bool
    row_ok: bool


def source_boundary_rows() -> tuple[SourceBoundaryRow, ...]:
    return (
        SourceBoundaryRow(
            name="ksy_1007_2307_local_source",
            boundary_artifact=RESEARCH / "p25_ksy_y_normalized_y_product_upgrade_frontier_20260614.md",
            current_status="atom formula plus generation/single-value theorems, no exact p25 product theorem",
            killed_as_direct_closer=True,
            watchlist_only=False,
            first_acceptable_upgrade="exact 75-atom normalized-y product/distribution identity for P",
            first_falsifier="formula language, field generation, or single y-value without full P",
            ok=True,
        ),
        SourceBoundaryRow(
            name="kubert_lang_iv_v_local_visual_source",
            boundary_artifact=RESEARCH / "p25_ksy_y_kubert_lang_visual_theorem_boundary_20260614.md",
            current_status="dependence/generation/Iwasawa source vocabulary, no row labels/reflection/raw product",
            killed_as_direct_closer=True,
            watchlist_only=False,
            first_acceptable_upgrade="exact C3 x C169 row labels, reflection center, or raw equal-weight K-traced product",
            first_falsifier="KL congruence, dependence, freeness, or Iwasawa tower language alone",
            ok=True,
        ),
        SourceBoundaryRow(
            name="sprang_kronecker_local_source",
            boundary_artifact=RESEARCH / "p25_ksy_y_sprang_exact_specialization_frontier_20260614.md",
            current_status="even-D/Kronecker vocabulary drained as direct closer",
            killed_as_direct_closer=False,
            watchlist_only=True,
            first_acceptable_upgrade="named exact mixed row-labeled Sprang theorem/formula hit",
            first_falsifier="omega^D, kernel/torsion distribution, or cohomology formula without exact payload",
            ok=True,
        ),
        SourceBoundaryRow(
            name="koo_shin_2010_full_surface",
            boundary_artifact=RESEARCH / "p25_ksy_y_koo_shin_2010_full_surface_screen_20260614.md",
            current_status=(
                "full supplied paper screened: Theorem 3.9 gives integrality "
                "hygiene, Theorem 6.2 is one-axis, 9.x are CM generators; no "
                "mixed p25 product"
            ),
            killed_as_direct_closer=True,
            watchlist_only=False,
            first_acceptable_upgrade="mixed-level theorem preserving C3 row graph and T edge",
            first_falsifier="orbit-sum hygiene, one-axis products, CM generation, or C169 projection without mixed lift",
            ok=True,
        ),
    )


def router_rows() -> tuple[IntakeRouterRow, ...]:
    return (
        IntakeRouterRow(
            name="source_claim_intake",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py",
            accepted_payload="exact divisor/additive P, or exact finite-field value P with period-156 context",
            reject_clause="field generation, exponent hygiene, ambient value, missing exact P, or missing mixed graph",
            ok=True,
        ),
        IntakeRouterRow(
            name="exact_product_intake",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py",
            accepted_payload="exact P with mixed graph, equal weights, orientation, arithmetic producer, legal framing",
            reject_clause="generic field generation, subgroup shortcut, exponent hygiene, or finite verifier without theorem",
            ok=True,
        ),
        IntakeRouterRow(
            name="closing_theorem_obligation",
            router_artifact=RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py",
            accepted_payload="source theorem closed, DANGER3 framing unblocked, extraction ready, then vpp-verified triple",
            reject_clause="anything short of exact P, mixed graph, equal weights, orientation, and source theorem",
            ok=True,
        ),
    )


def profile_post_local_source_exact_product_queue() -> PostLocalSourceExactProductQueue:
    sources = source_boundary_rows()
    routers = router_rows()
    killed = sum(row.killed_as_direct_closer for row in sources)
    watchlist = sum(row.watchlist_only for row in sources)
    active_external = 1
    router_present = sum(row.router_artifact.exists() and row.router_artifact.stat().st_size > 0 for row in routers)
    source_present = all(row.boundary_artifact.exists() and row.boundary_artifact.stat().st_size > 0 for row in sources)
    row_ok = (
        source_present
        and router_present == 3
        and killed == 3
        and watchlist == 1
        and active_external == 1
        and all(row.ok for row in sources)
        and all(row.ok for row in routers)
    )
    return PostLocalSourceExactProductQueue(
        source_rows=sources,
        router_rows=routers,
        killed_direct_rows=killed,
        watchlist_rows=watchlist,
        active_external_search_rows=active_external,
        router_rows_present=router_present,
        heavy_finite_harness_required_for_queue_gate=False,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_post_local_source_exact_product_queue()
    print("p25 KSY-y post-local-source exact-product queue gate")
    print("source_boundaries")
    for row in profile.source_rows:
        print(
            "  "
            f"{row.name}: killed={int(row.killed_as_direct_closer)} "
            f"watchlist={int(row.watchlist_only)} artifact={row.boundary_artifact}"
        )
        print(f"    status={row.current_status}")
        print(f"    upgrade={row.first_acceptable_upgrade}")
        print(f"    falsifier={row.first_falsifier}")
    print("intake_routers")
    for row in profile.router_rows:
        print(f"  {row.name}: artifact={row.router_artifact}")
        print(f"    accept={row.accepted_payload}")
        print(f"    reject={row.reject_clause}")
    print("counts")
    print(f"  killed_direct_rows={profile.killed_direct_rows}")
    print(f"  watchlist_rows={profile.watchlist_rows}")
    print(f"  active_external_search_rows={profile.active_external_search_rows}")
    print(f"  router_rows_present={profile.router_rows_present}")
    print(
        "  heavy_finite_harness_required_for_queue_gate="
        f"{int(profile.heavy_finite_harness_required_for_queue_gate)}"
    )
    print("interpretation")
    print("  local_sources_are_now_boundary_artifacts_not_broad_reread_targets=1")
    print("  next_progress_requires_external_or_new_exact_product_theorem_hit=1")
    print("  any_hit_must_route_through_existing_intake_and_closing_obligation_gates=1")
    print(
        "ksy_y_post_local_source_exact_product_queue_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("post-local-source exact-product queue regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

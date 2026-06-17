#!/usr/bin/env python3
"""Route p25 support lanes and microscopes after the McCarthy endpoint pass."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path(__file__).resolve().parents[2]
MARKER = "p25_v2_support_microscope_router_rows=1/1"


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


@dataclass(frozen=True)
class SupportRoute:
    name: str
    role: str
    route: str
    decision: str
    first_missing_or_falsifier: str
    page_rel_path: str
    required_terms: tuple[str, ...]
    current_source_closer: bool

    @property
    def page_ok(self) -> bool:
        path = RESEARCH / self.page_rel_path
        if not path.exists():
            return False
        text = path.read_text(errors="replace")
        return all(term in text for term in self.required_terms)


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "support_lane_router",
        "evidence/p25_v2_support_lane_router_20260616.md",
        "p25_v2_support_lane_router_rows=1/1",
    ),
    EvidenceMarker(
        "support_lane_status_demotion",
        "evidence/p25_v2_support_lane_status_demotion_20260616.md",
        "p25_v2_support_lane_status_demotion_rows=1/1",
    ),
    EvidenceMarker(
        "period156_value_source_hook",
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_minimal_hook",
        "evidence/p25_v2_exactp_minimal_hook_20260616.md",
        "p25_v2_exactp_minimal_hook_rows=1/1",
    ),
    EvidenceMarker(
        "exactp_closure_template_replay_boundary",
        "evidence/p25_v2_exactp_closure_template_replay_boundary_20260616.md",
        "p25_v2_exactp_closure_template_replay_boundary_rows=1/1",
    ),
    EvidenceMarker(
        "mccarthy_endpoint_stability_router",
        "evidence/p25_v2_mccarthy_endpoint_stability_router_20260617.md",
        "p25_v2_mccarthy_endpoint_stability_router_rows=1/1",
    ),
)


def routes() -> tuple[SupportRoute, ...]:
    return (
        SupportRoute(
            name="twisted_h90",
            role="period156_support_surface",
            route="period156_value_source_hook_then_source_snippet_intake",
            decision="support_surface_not_frontdoor",
            first_missing_or_falsifier=(
                "exact twisted/H90 source object with period-156 context and "
                "arithmetic source theorem"
            ),
            page_rel_path="lanes/twisted-h90.md",
            required_terms=(
                "status: background",
                "support surface, not a first-pass front door",
                "period-156 branch/root/telescoping context",
                "challenge-legal arithmetic source theorem",
            ),
            current_source_closer=False,
        ),
        SupportRoute(
            name="curved_corner",
            role="period156_support_surface",
            route="period156_value_source_hook_then_source_snippet_intake",
            decision="support_surface_not_frontdoor",
            first_missing_or_falsifier=(
                "exact unit-triangle curved K-traced payload with period-156 "
                "context and arithmetic source theorem"
            ),
            page_rel_path="lanes/curved-corner.md",
            required_terms=(
                "status: background",
                "support surface, not a first-pass front door",
                "exact unit-triangle curved K-traced corner payload",
                "period-156 branch/root/telescoping context",
            ),
            current_source_closer=False,
        ),
        SupportRoute(
            name="lane_b_c_generic_microscopes",
            role="attached_support_microscope",
            route="only_when_tied_to_H0_conductor39_or_exactP_theorem_idea",
            decision="not_standalone_moonshot",
            first_missing_or_falsifier=(
                "probe is not attached to a concrete theorem idea or produces "
                "only broad count/vocabulary data"
            ),
            page_rel_path="concepts/transfer-matrix.md",
            required_terms=(
                "Fixed-frequency/Jacobi and low-moment/W-axis still matter only",
                "p25-specific support microscopes tied to H0, conductor 39, or exact-P",
                "not independent",
                "front-door lanes",
            ),
            current_source_closer=False,
        ),
        SupportRoute(
            name="mccarthy_square_axis_endpoint",
            role="exactp_endpoint_test_microscope",
            route="sparse_endpoint_theorem_or_invariant_cancellation_only",
            decision="endpoint_test_not_frontdoor",
            first_missing_or_falsifier=(
                "arithmetic theorem producing e_138, or nontrivial "
                "auxiliary-prime-invariant quotient cancellation"
            ),
            page_rel_path="lanes/exact-p.md",
            required_terms=(
                "McCarthy square-axis endpoint is now a support-microscope test object",
                "raw `R(138)^2029` projection is not auxiliary-prime invariant",
                "236 scans",
                "sparse `e_138` endpoint",
            ),
            current_source_closer=False,
        ),
        SupportRoute(
            name="exact_p",
            role="heavy_upstream_route",
            route="exactp_minimal_hook_then_extraction_contract",
            decision="heavy_route_not_first_pass_default",
            first_missing_or_falsifier=(
                "compact C,D,K,orientation, equal-weight 75 atoms, accepted "
                "theta2 payload, or explicit reverse reconstruction theorem"
            ),
            page_rel_path="lanes/exact-p.md",
            required_terms=(
                "not the first-pass front door",
                "equal-weight 75-atom theorem",
                "accepted theta2/theta2-inverse payload",
                "DANGER3 finite-identity or non-CM framing",
            ),
            current_source_closer=False,
        ),
    )


def main() -> int:
    route_rows = routes()
    marker_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    period156_surfaces = sum(row.role == "period156_support_surface" for row in route_rows)
    support_microscopes = sum("microscope" in row.role for row in route_rows)
    heavy_routes = sum(row.role == "heavy_upstream_route" for row in route_rows)
    frontdoor_support_rows = sum(row.decision not in {"support_surface_not_frontdoor", "not_standalone_moonshot", "endpoint_test_not_frontdoor", "heavy_route_not_first_pass_default"} for row in route_rows)
    current_source_closers = sum(row.current_source_closer for row in route_rows)
    row_ok = (
        marker_ok == len(EVIDENCE_MARKERS)
        and len(route_rows) == 5
        and period156_surfaces == 2
        and support_microscopes == 2
        and heavy_routes == 1
        and frontdoor_support_rows == 0
        and current_source_closers == 0
        and all(row.page_ok for row in route_rows)
    )

    print("p25 v2 support microscope router")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("routes")
    for row in route_rows:
        print(f"  {row.name}: role={row.role} decision={row.decision} ok={int(row.page_ok)}")
        print(f"    route={row.route}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={marker_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"route_rows={len(route_rows)}")
    print(f"period156_support_surfaces={period156_surfaces}")
    print(f"support_microscopes={support_microscopes}")
    print(f"heavy_routes={heavy_routes}")
    print(f"frontdoor_support_rows={frontdoor_support_rows}")
    print(f"current_source_closers={current_source_closers}")
    print("interpretation")
    print("  support_surfaces_do_not_change_lane_status_without_exact_source_theorem=1")
    print("  generic_lane_b_c_probes_must_attach_to_a_theorem_idea=1")
    print("  mccarthy_endpoint_is_a_test_object_not_a_frontdoor=1")
    print(MARKER if row_ok else "p25_v2_support_microscope_router_rows=0/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

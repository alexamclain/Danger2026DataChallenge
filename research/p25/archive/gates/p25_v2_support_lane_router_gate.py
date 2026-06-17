#!/usr/bin/env python3
"""Route support lanes through the v2 theorem front doors.

Twisted-H90 and curved-corner are still useful names for possible source
snippets, but they are no longer independent front-door moonshots.  This gate
checks that both lanes are routed through the same period-156 value/divisor
source hook, while exact-P remains the separate heavy upstream route.
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
class SupportLaneRow:
    name: str
    lane_page: Path
    role: str
    required_terms: tuple[str, ...]
    routes_through: str
    current_source_closer: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class SupportLaneRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SupportLaneRow, ...]
    support_lanes: int
    frontdoor_support_lanes: int
    heavy_routes: int
    current_source_closers: int
    row_ok: bool


def read(path: Path | str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def has_all(text: str, terms: tuple[str, ...]) -> bool:
    return all(term in text for term in terms)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "period156_value_source_hook",
            "research/p25/evidence/p25_v2_period156_value_source_hook_20260616.md",
            "p25_v2_period156_value_source_hook_rows=1/1",
        ),
        marker(
            "theta2_period156_support_contract",
            "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            "p25_v2_theta2_period156_support_contract_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "frontdoor_count_sync",
            "research/p25/evidence/p25_v2_frontdoor_count_sync_20260616.md",
            "p25_v2_frontdoor_count_sync_rows=1/1",
        ),
    )


def support_rows() -> tuple[SupportLaneRow, ...]:
    twisted_path = Path("research/p25/lanes/twisted-h90.md")
    twisted = read(twisted_path)
    curved_path = Path("research/p25/lanes/curved-corner.md")
    curved = read(curved_path)
    exactp_path = Path("research/p25/lanes/exact-p.md")
    exactp = read(exactp_path)
    transfer = read("research/p25/concepts/transfer-matrix.md")

    twisted_terms = (
        "twisted quotient/ratio or Hilbert-90 finite value/divisor theorem",
        "period-156 branch/root/telescoping context",
        "challenge-legal arithmetic source theorem",
        "not a source-stage close",
    )
    curved_terms = (
        "finite value/divisor theorem",
        "exact unit-triangle curved K-traced corner payload",
        "period-156 branch/root/telescoping context",
        "not a",
        "closer",
    )
    exactp_terms = (
        "not the first-pass front door",
        "equal-weight 75-atom theorem",
        "accepted theta2/theta2-inverse payload",
        "DANGER3 finite-identity or non-CM framing",
    )

    return (
        SupportLaneRow(
            name="twisted_h90",
            lane_page=twisted_path,
            role="support value/divisor surface",
            required_terms=twisted_terms,
            routes_through="period156_value_source_hook_then_source_snippet_intake",
            current_source_closer=False,
            decision="support_lane_not_frontdoor",
            first_missing_or_falsifier=(
                "exact twisted/H90 source object plus period-156 branch/root/telescoping "
                "and arithmetic source theorem"
            ),
            ok=has_all(twisted, twisted_terms) and "Twisted-H90 and curved-corner remain live only" in transfer,
        ),
        SupportLaneRow(
            name="curved_corner",
            lane_page=curved_path,
            role="support value/divisor surface",
            required_terms=curved_terms,
            routes_through="period156_value_source_hook_then_source_snippet_intake",
            current_source_closer=False,
            decision="support_lane_not_frontdoor",
            first_missing_or_falsifier=(
                "exact unit-triangle curved K-traced payload plus period-156 "
                "branch/root/telescoping and arithmetic source theorem"
            ),
            ok=has_all(curved, curved_terms) and "Twisted-H90 and curved-corner remain live only" in transfer,
        ),
        SupportLaneRow(
            name="exact_p",
            lane_page=exactp_path,
            role="heavy upstream route",
            required_terms=exactp_terms,
            routes_through="exactp_minimal_hook_then_extraction_contract",
            current_source_closer=False,
            decision="heavy_route_not_first_pass_default",
            first_missing_or_falsifier=(
                "compact C,D,K,orientation packet, exact equal-weight 75 atoms, "
                "accepted theta2 payload, or explicit reverse reconstruction theorem"
            ),
            ok=has_all(exactp, exactp_terms) and "Exact-P remains the high-payoff heavy route" in transfer,
        ),
    )


def build_router() -> SupportLaneRouter:
    markers = evidence_markers()
    rows = support_rows()
    support_lanes = sum(row.role == "support value/divisor surface" for row in rows)
    heavy_routes = sum(row.role == "heavy upstream route" for row in rows)
    frontdoor_support_lanes = sum(
        row.role == "support value/divisor surface" and row.decision != "support_lane_not_frontdoor"
        for row in rows
    )
    current_source_closers = sum(row.current_source_closer for row in rows)
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 3
        and support_lanes == 2
        and heavy_routes == 1
        and frontdoor_support_lanes == 0
        and current_source_closers == 0
        and all(row.ok for row in rows)
    )
    return SupportLaneRouter(
        evidence_markers=markers,
        rows=rows,
        support_lanes=support_lanes,
        frontdoor_support_lanes=frontdoor_support_lanes,
        heavy_routes=heavy_routes,
        current_source_closers=current_source_closers,
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    print("p25 v2 support lane router")
    for marker_row in router.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in router.rows:
        print(f"  {row.name}: role={row.role} decision={row.decision} ok={int(row.ok)}")
        print(f"    routes_through={row.routes_through}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in router.evidence_markers)}/{len(router.evidence_markers)}")
    print(f"  support_lanes={router.support_lanes}")
    print(f"  frontdoor_support_lanes={router.frontdoor_support_lanes}")
    print(f"  heavy_routes={router.heavy_routes}")
    print(f"  current_source_closers={router.current_source_closers}")
    print("interpretation")
    print("  twisted_h90_and_curved_corner_are_support_surfaces_not_frontdoors=1")
    print("  exactp_remains_heavy_route_not_first_pass_default=1")
    print("  support_lane_status_changes_require_period156_or_exactp_hook=1")
    print(f"p25_v2_support_lane_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

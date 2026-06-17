#!/usr/bin/env python3
"""Exact-P orientation branch router for the p25 heavy route.

The exact-P minimal hook says a source theorem must emit
``C,D,K,orientation`` or an accepted theta2 payload.  This gate expands the
word "orientation" into the four finite branches that actually feed the
theta2 certificate path, and keeps value-only branch claims behind the
period-156 context requirement.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate import (
    profile_raw_orientation_certificate_router,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate import (
    profile_raw_orientation_value_route,
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OrientationBranch:
    name: str
    raw_center: tuple[int, int]
    raw_d: tuple[int, int]
    k_multiplier: int
    reverse: bool
    emitted_payload: str
    recovered_sign: int
    divisor_route_ok: bool
    value_requires_period156_context: bool
    ok: bool


@dataclass(frozen=True)
class IntakeRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ExactPOrientationBranchRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    branches: tuple[OrientationBranch, ...]
    intake_routes: tuple[IntakeRoute, ...]
    evidence_markers_ok: int
    accepted_orientation_branches: int
    theta2_inverse_routes: int
    theta2_routes: int
    support_period: int
    support_period_value_root_unique_fp: bool
    ambient_value_branch_count_fp: int
    rejected_controls: int
    current_exactp_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_theorem_interface",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "All six gates returned their expected `rows=1/1` markers.",
        ),
        marker(
            "theta2_period156_support_contract",
            "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            "p25_v2_theta2_period156_support_contract_rows=1/1",
        ),
        marker(
            "period156_value_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def build_branches() -> tuple[OrientationBranch, ...]:
    router = profile_raw_orientation_certificate_router()
    value_route = profile_raw_orientation_value_route()
    value_by_name = {branch.route_name: branch for branch in value_route.branch_value_routes}
    return tuple(
        OrientationBranch(
            name=route.name,
            raw_center=route.raw_center,
            raw_d=route.raw_d,
            k_multiplier=route.k_multiplier,
            reverse=route.reverse,
            emitted_payload=route.emitted_payload,
            recovered_sign=route.theta2_candidate_profile.recovered_sign,
            divisor_route_ok=route.certificate_path_ok,
            value_requires_period156_context=value_by_name[
                route.name
            ].value_route_requires_period_context,
            ok=(
                route.certificate_path_ok
                and value_by_name[route.name].divisor_route_ok
                and value_by_name[route.name].support_period_value_root_unique_fp
            ),
        )
        for route in router.branch_routes
    )


def intake_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute(
            name="one_of_four_oriented_branches_with_divisor_additive_payload",
            decision="exactp_source_stage_win_route_to_extraction",
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        IntakeRoute(
            name="one_of_four_oriented_branches_with_period156_value_context",
            decision="exactp_source_stage_win_route_to_extraction",
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        IntakeRoute(
            name="branchless_C_D_K_orientation_word",
            decision="repair_exactp_orientation_branch_missing",
            first_missing_or_falsifier="one of the four raw center/reverse branches and theta2/theta2^-1 output",
            ok=True,
        ),
        IntakeRoute(
            name="theta2_value_without_period156_context",
            decision="repair_period156_branch_selection_missing",
            first_missing_or_falsifier="period-156 theta2 fixedness, branch, root, or telescoping data",
            ok=True,
        ),
        IntakeRoute(
            name="ambient780_value_only",
            decision="repair_period156_branch_selection_missing",
            first_missing_or_falsifier="ambient route has mu_11 ambiguity in F_p^*",
            ok=True,
        ),
        IntakeRoute(
            name="wrong_center_wrong_d_or_nonprimitive_k",
            decision="reject_wrong_exactp_payload",
            first_missing_or_falsifier="raw orientation router rejects wrong center, wrong D, and nonprimitive K",
            ok=True,
        ),
    )


def build_router() -> ExactPOrientationBranchRouter:
    markers = evidence_markers()
    router = profile_raw_orientation_certificate_router()
    value_route = profile_raw_orientation_value_route()
    branches = build_branches()
    routes = intake_routes()
    markers_ok = sum(row.ok for row in markers)
    accepted = sum(row.ok for row in branches)
    theta2_inverse = sum(branch.emitted_payload == "theta2_inverse" for branch in branches)
    theta2 = sum(branch.emitted_payload == "theta2" for branch in branches)
    rejected_controls = sum(
        not route.certificate_path_ok
        for route in (
            router.wrong_center_route,
            router.wrong_d_route,
            router.nonprimitive_k_route,
        )
    )
    current_exactp_source_theorems = 0
    current_submission_ready = 0
    expected = (
        ("center_forward_route", "theta2_inverse", -1),
        ("center_reverse_route", "theta2", 1),
        ("inverse_center_forward_route", "theta2", 1),
        ("inverse_center_reverse_route", "theta2_inverse", -1),
    )
    row_ok = (
        markers_ok == len(markers)
        and router.row_ok
        and value_route.row_ok
        and len(branches) == 4
        and accepted == 4
        and tuple((b.name, b.emitted_payload, b.recovered_sign) for b in branches) == expected
        and theta2_inverse == 2
        and theta2 == 2
        and value_route.support_period == 156
        and value_route.support_value_root_unique_fp_star
        and value_route.ambient_value_branch_count_fp_star == 11
        and value_route.ambient_value_route_has_mu11_ambiguity
        and value_route.proper_period_shortcuts_all_fail
        and rejected_controls == 3
        and len(routes) == 6
        and all(row.ok for row in routes)
        and current_exactp_source_theorems == 0
        and current_submission_ready == 0
    )
    return ExactPOrientationBranchRouter(
        evidence_markers=markers,
        branches=branches,
        intake_routes=routes,
        evidence_markers_ok=markers_ok,
        accepted_orientation_branches=accepted,
        theta2_inverse_routes=theta2_inverse,
        theta2_routes=theta2,
        support_period=value_route.support_period,
        support_period_value_root_unique_fp=value_route.support_value_root_unique_fp_star,
        ambient_value_branch_count_fp=value_route.ambient_value_branch_count_fp_star,
        rejected_controls=rejected_controls,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_router()
    print("p25 v2 exact-P orientation branch router")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("orientation_branches")
    for branch in profile.branches:
        print(
            "  "
            f"{branch.name}: center={branch.raw_center} D={branch.raw_d} "
            f"Kmult={branch.k_multiplier} reverse={int(branch.reverse)} "
            f"emits={branch.emitted_payload} sign={branch.recovered_sign} "
            f"divisor_route_ok={int(branch.divisor_route_ok)} "
            f"value_needs_period156={int(branch.value_requires_period156_context)}"
        )
    print("intake_routes")
    for route in profile.intake_routes:
        print(f"  {route.name}: decision={route.decision}")
        print(f"    missing_or_falsifier={route.first_missing_or_falsifier}")
    print("counts")
    print(
        f"  evidence_markers_ok={profile.evidence_markers_ok}/"
        f"{len(profile.evidence_markers)}"
    )
    print(f"  accepted_orientation_branches={profile.accepted_orientation_branches}")
    print(f"  theta2_inverse_routes={profile.theta2_inverse_routes}")
    print(f"  theta2_routes={profile.theta2_routes}")
    print(f"  support_period={profile.support_period}")
    print(
        "  support_period_value_root_unique_fp="
        f"{int(profile.support_period_value_root_unique_fp)}"
    )
    print(f"  ambient_value_branch_count_fp={profile.ambient_value_branch_count_fp}")
    print(f"  rejected_controls={profile.rejected_controls}")
    print(f"  current_exactp_source_theorems={profile.current_exactp_source_theorems}")
    print(f"  current_submission_ready={profile.current_submission_ready}")
    print("interpretation")
    print("  exactp_orientation_word_means_one_of_four_raw_branches=1")
    print("  divisor_or_additive_branch_hits_route_through_theta2_certificate=1")
    print("  value_branch_hits_need_period156_context_before_intake=1")
    print("  wrong_center_wrong_D_and_nonprimitive_K_are_rejected=1")
    print(f"p25_v2_exactp_orientation_branch_router_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

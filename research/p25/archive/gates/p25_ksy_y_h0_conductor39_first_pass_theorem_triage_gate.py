#!/usr/bin/env python3
"""First-pass theorem triage for the H0 and conductor-39 source lanes.

The external source-theorem obligation matrix selects H0 and conductor-39 as
the first source-theorem targets.  This gate is the small operational intake
surface for those targets: it routes theorem snippets into the existing H0
product-file classifier or conductor-39 source-theorem classifier, records the
first repair/falsifier, and keeps source-stage closure separate from DANGER3
policy, bridge, X_1(16), halving, and official vpp.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    Conductor39SourceTheoremClaim,
    Conductor39SourceTheoremDecision,
    classify_claim as classify_conductor39_claim,
)
from p25_ksy_y_h0_product_file_claim_intake_gate import (
    FIXTURE_DIR as H0_FIXTURE_DIR,
    ProductFileClaim,
    ProductFileDecision,
    classify_product_file_claim,
)
from p25_ksy_y_h0_translate_exact_product_query_packet_gate import (
    profile_h0_translate_exact_product_query_packet,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_source_theorem_obligation_matrix_20260614.md",
        "ksy_y_external_source_theorem_obligation_matrix_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_product_file_claim_intake_20260614.md",
        "ksy_y_h0_product_file_claim_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_source_theorem_intake_20260614.md",
        "ksy_y_conductor39_source_theorem_intake_rows=1/1",
    ),
)


@dataclass(frozen=True)
class FirstPassTheoremTriageRow:
    name: str
    lane: str
    snippet_shape: str
    candidate_command: str
    expected_decision: str
    actual_decision: str
    source_stage_closes: bool
    source_certified_only: bool
    period156_repair: bool
    boundary_repair: bool
    kill_route: bool
    selected_positive_target: bool
    avoids_period_value_branch: bool
    current_source_theorem: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0Conductor39FirstPassTheoremTriage:
    dependency_markers_present: int
    dependency_markers_total: int
    obligation_matrix_ok: bool
    h0_product_intake_ok: bool
    conductor39_intake_ok: bool
    h0_exact_query_ok: bool
    rows: tuple[FirstPassTheoremTriageRow, ...]
    row_count: int
    h0_rows: int
    conductor39_rows: int
    candidate_command_rows: int
    source_stage_closing_rows: int
    source_certified_only_rows: int
    period156_repair_rows: int
    boundary_repair_rows: int
    kill_route_rows: int
    selected_positive_target_rows: int
    avoids_period_value_branch_rows: int
    current_source_theorem_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def h0_command(
    *,
    name: str,
    product_file: Path,
    output_kind: str,
    period156: bool = False,
    h90_boundary: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_h0_product_file_claim_intake_gate.py",
        f"--product-file {product_file}",
        f"--name {name}",
        "--theorem-body",
        "--source-theorem",
        f"--output-kind {output_kind}",
    ]
    if period156:
        parts.append("--period-156")
    if h90_boundary:
        parts.append("--h90-boundary")
    return " ".join(parts)


def h0_claim(
    *,
    name: str,
    product_file: Path,
    output_kind: str,
    period156: bool = False,
    h90_boundary: bool = False,
) -> ProductFileClaim:
    return ProductFileClaim(
        name=name,
        product_file=product_file,
        theorem_body_verified=True,
        arithmetic_source_theorem=True,
        output_kind=output_kind,
        period156_context=period156,
        h90_boundary=h90_boundary,
        danger3_framing=False,
        same_j_x18112_bridge=False,
        x16_surface=False,
        concrete_x0=False,
        official_vpp=False,
    )


def conductor39_command(
    *,
    name: str,
    source_object: str = "U_chi",
    output_kind: str = "divisor-additive",
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    yang_lift: bool = True,
    descent: bool = True,
    finite_or_divisor: bool = False,
    period156: bool = False,
    projection: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--source-object {source_object}",
        f"--output-kind {output_kind}",
        "--theorem-body",
    ]
    if emits:
        parts.append("--emits-conductor39")
    if mixed:
        parts.append("--mixed-tensor")
    if legal:
        parts.append("--legal-unit")
    if yang_lift:
        parts.append("--yang-lift")
    if descent:
        parts.append("--descent")
    if finite_or_divisor:
        parts.append("--finite-or-divisor")
    if period156:
        parts.append("--period-156")
    if projection:
        parts.append("--proper-axis-projection")
    return " ".join(parts)


def conductor39_claim(
    *,
    name: str,
    source_object: str = "U_chi",
    output_kind: str = "divisor-additive",
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    yang_lift: bool = True,
    descent: bool = True,
    finite_or_divisor: bool = False,
    period156: bool = False,
    projection: bool = False,
) -> Conductor39SourceTheoremClaim:
    return Conductor39SourceTheoremClaim(
        name=name,
        theorem_body_verified=True,
        source_object=source_object,
        emits_conductor39_object=emits,
        preserves_mixed_tensor=mixed,
        yang_yu_legal_unit=legal,
        sparse_formal_gauge_only=False,
        proper_axis_or_projection_only=projection,
        additive_separated=False,
        yang_distribution_to_507=yang_lift,
        frobenius_or_hilbert90_descent=descent,
        output_kind=output_kind,
        finite_field_identity_or_divisor_theorem=finite_or_divisor,
        period_156_context=period156,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def row_from_h0(
    *,
    name: str,
    snippet_shape: str,
    product_file: Path,
    output_kind: str,
    expected_decision: str,
    period156: bool = False,
    h90_boundary: bool = False,
    source_certified_only: bool = False,
    period156_repair: bool = False,
    boundary_repair: bool = False,
    selected_positive: bool = False,
    avoids_period_branch: bool = False,
    target_rows,
) -> FirstPassTheoremTriageRow:
    decision = classify_product_file_claim(
        h0_claim(
            name=name,
            product_file=product_file,
            output_kind=output_kind,
            period156=period156,
            h90_boundary=h90_boundary,
        ),
        target_rows,
    )
    return FirstPassTheoremTriageRow(
        name=name,
        lane="H0",
        snippet_shape=snippet_shape,
        candidate_command=h0_command(
            name=name,
            product_file=product_file,
            output_kind=output_kind,
            period156=period156,
            h90_boundary=h90_boundary,
        ),
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        source_stage_closes=decision.source_stage_closed,
        source_certified_only=source_certified_only,
        period156_repair=period156_repair,
        boundary_repair=boundary_repair,
        kill_route=decision.decision.startswith("reject_"),
        selected_positive_target=selected_positive,
        avoids_period_value_branch=avoids_period_branch,
        current_source_theorem=False,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        next_action=decision.next_action,
        ok=decision.ok and decision.decision == expected_decision,
    )


def row_from_conductor39(
    *,
    name: str,
    snippet_shape: str,
    expected_decision: str,
    source_object: str = "U_chi",
    output_kind: str = "divisor-additive",
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    yang_lift: bool = True,
    descent: bool = True,
    finite_or_divisor: bool = False,
    period156: bool = False,
    projection: bool = False,
    source_certified_only: bool = False,
    period156_repair: bool = False,
    selected_positive: bool = False,
    avoids_period_branch: bool = False,
) -> FirstPassTheoremTriageRow:
    decision = classify_conductor39_claim(
        conductor39_claim(
            name=name,
            source_object=source_object,
            output_kind=output_kind,
            emits=emits,
            mixed=mixed,
            legal=legal,
            yang_lift=yang_lift,
            descent=descent,
            finite_or_divisor=finite_or_divisor,
            period156=period156,
            projection=projection,
        )
    )
    return FirstPassTheoremTriageRow(
        name=name,
        lane="conductor39",
        snippet_shape=snippet_shape,
        candidate_command=conductor39_command(
            name=name,
            source_object=source_object,
            output_kind=output_kind,
            emits=emits,
            mixed=mixed,
            legal=legal,
            yang_lift=yang_lift,
            descent=descent,
            finite_or_divisor=finite_or_divisor,
            period156=period156,
            projection=projection,
        ),
        expected_decision=expected_decision,
        actual_decision=decision.decision,
        source_stage_closes=decision.theorem_source_closed,
        source_certified_only=source_certified_only,
        period156_repair=period156_repair,
        boundary_repair=False,
        kill_route=decision.decision.startswith("reject_"),
        selected_positive_target=selected_positive,
        avoids_period_value_branch=avoids_period_branch,
        current_source_theorem=False,
        first_missing_or_falsifier=decision.first_missing_clause,
        next_action=decision.next_action,
        ok=decision.row_ok and decision.decision == expected_decision,
    )


def triage_rows(target_rows) -> tuple[FirstPassTheoremTriageRow, ...]:
    h0_m1 = H0_FIXTURE_DIR / "h0_m1_canonical_lifted_product.txt"
    h0_m2 = H0_FIXTURE_DIR / "h0_m2_translate_lifted_product.txt"
    h0_m4 = H0_FIXTURE_DIR / "h0_m4_translate_lifted_product.txt"
    return (
        row_from_h0(
            name="h0_source_certification_only",
            snippet_shape="exact H0 product legality/source certification only",
            product_file=h0_m1,
            output_kind="source-certification",
            expected_decision="source_certified_value_or_divisor_missing",
            source_certified_only=True,
            target_rows=target_rows,
        ),
        row_from_h0(
            name="h0_value_without_period156",
            snippet_shape="exact H0 finite value with no support-period-156 context",
            product_file=h0_m2,
            output_kind="value",
            h90_boundary=True,
            expected_decision="conditional_missing_period_156_context",
            period156_repair=True,
            target_rows=target_rows,
        ),
        row_from_h0(
            name="h0_divisor_missing_h90_boundary",
            snippet_shape="exact H0 divisor/additive statement with no H90 boundary",
            product_file=h0_m4,
            output_kind="divisor-additive",
            expected_decision="conditional_divisor_identity_missing_h90_boundary",
            boundary_repair=True,
            target_rows=target_rows,
        ),
        row_from_h0(
            name="h0_divisor_additive_source_yes",
            snippet_shape="exact H0 divisor/additive theorem with H90 boundary",
            product_file=h0_m4,
            output_kind="divisor-additive",
            h90_boundary=True,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            selected_positive=True,
            avoids_period_branch=True,
            target_rows=target_rows,
        ),
        row_from_conductor39(
            name="conductor39_source_object_only",
            snippet_shape="legal U_chi/W source object with Yang lift/descent but no finite theorem",
            expected_decision="conductor39_source_identified_value_or_divisor_theorem_missing",
            source_certified_only=True,
        ),
        row_from_conductor39(
            name="conductor39_value_without_period156",
            snippet_shape="finite conductor-39 value with no support-period-156 context",
            output_kind="value",
            finite_or_divisor=True,
            expected_decision="conditional_missing_period_156_context",
            period156_repair=True,
        ),
        row_from_conductor39(
            name="conductor39_projection_shortcut",
            snippet_shape="prime projection or axis-only conductor-39 shortcut",
            source_object="projection",
            emits=False,
            mixed=False,
            legal=False,
            yang_lift=False,
            descent=False,
            finite_or_divisor=False,
            projection=True,
            expected_decision="reject_loses_mixed_tensor",
        ),
        row_from_conductor39(
            name="conductor39_divisor_additive_source_yes",
            snippet_shape="U_chi/W mixed divisor/additive theorem preserving Yang lift and descent",
            finite_or_divisor=True,
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            selected_positive=True,
            avoids_period_branch=True,
        ),
    )


def profile_h0_conductor39_first_pass_theorem_triage() -> H0Conductor39FirstPassTheoremTriage:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    matrix_ok = marker_present(*DEPENDENCY_MARKERS[0])
    h0_intake_ok = marker_present(*DEPENDENCY_MARKERS[1])
    conductor39_intake_ok = marker_present(*DEPENDENCY_MARKERS[2])
    query = profile_h0_translate_exact_product_query_packet()
    rows = triage_rows(query.exact_product_rows)
    h0_rows = sum(row.lane == "H0" for row in rows)
    conductor_rows = sum(row.lane == "conductor39" for row in rows)
    commands = sum(bool(row.candidate_command) for row in rows)
    closes = sum(row.source_stage_closes for row in rows)
    source_cert = sum(row.source_certified_only for row in rows)
    period_repair = sum(row.period156_repair for row in rows)
    boundary_repair = sum(row.boundary_repair for row in rows)
    kill = sum(row.kill_route for row in rows)
    selected = sum(row.selected_positive_target for row in rows)
    avoids_period = sum(row.avoids_period_value_branch for row in rows)
    current_source = sum(row.current_source_theorem for row in rows)
    decisions = tuple(row.actual_decision for row in rows)
    expected_decisions = (
        "source_certified_value_or_divisor_missing",
        "conditional_missing_period_156_context",
        "conditional_divisor_identity_missing_h90_boundary",
        "source_theorem_closed_policy_or_framing_missing",
        "conductor39_source_identified_value_or_divisor_theorem_missing",
        "conditional_missing_period_156_context",
        "reject_loses_mixed_tensor",
        "source_theorem_closed_policy_or_framing_missing",
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and matrix_ok
        and h0_intake_ok
        and conductor39_intake_ok
        and query.row_ok
        and len(query.exact_product_rows) == 4
        and len(rows) == 8
        and h0_rows == 4
        and conductor_rows == 4
        and commands == 8
        and closes == 2
        and source_cert == 2
        and period_repair == 2
        and boundary_repair == 1
        and kill == 1
        and selected == 2
        and avoids_period == 2
        and current_source == 0
        and decisions == expected_decisions
        and all(row.ok for row in rows)
    )
    return H0Conductor39FirstPassTheoremTriage(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        obligation_matrix_ok=matrix_ok,
        h0_product_intake_ok=h0_intake_ok,
        conductor39_intake_ok=conductor39_intake_ok,
        h0_exact_query_ok=query.row_ok,
        rows=rows,
        row_count=len(rows),
        h0_rows=h0_rows,
        conductor39_rows=conductor_rows,
        candidate_command_rows=commands,
        source_stage_closing_rows=closes,
        source_certified_only_rows=source_cert,
        period156_repair_rows=period_repair,
        boundary_repair_rows=boundary_repair,
        kill_route_rows=kill,
        selected_positive_target_rows=selected,
        avoids_period_value_branch_rows=avoids_period,
        current_source_theorem_rows=current_source,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_conductor39_first_pass_theorem_triage()
    print("p25 KSY-y H0/conductor-39 first-pass theorem triage gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  obligation_matrix_ok={int(profile.obligation_matrix_ok)}")
    print(f"  h0_product_intake_ok={int(profile.h0_product_intake_ok)}")
    print(f"  conductor39_intake_ok={int(profile.conductor39_intake_ok)}")
    print(f"  h0_exact_query_ok={int(profile.h0_exact_query_ok)}")
    print("triage_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: lane={row.lane} decision={row.actual_decision} "
            f"closes={int(row.source_stage_closes)} cert_only={int(row.source_certified_only)} "
            f"period_repair={int(row.period156_repair)} "
            f"boundary_repair={int(row.boundary_repair)} kill={int(row.kill_route)} "
            f"selected={int(row.selected_positive_target)} "
            f"avoids_period={int(row.avoids_period_value_branch)} "
            f"current={int(row.current_source_theorem)}"
        )
        print(f"    shape={row.snippet_shape}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  h0_rows={profile.h0_rows}")
    print(f"  conductor39_rows={profile.conductor39_rows}")
    print(f"  candidate_command_rows={profile.candidate_command_rows}")
    print(f"  source_stage_closing_rows={profile.source_stage_closing_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  period156_repair_rows={profile.period156_repair_rows}")
    print(f"  boundary_repair_rows={profile.boundary_repair_rows}")
    print(f"  kill_route_rows={profile.kill_route_rows}")
    print(f"  selected_positive_target_rows={profile.selected_positive_target_rows}")
    print(f"  avoids_period_value_branch_rows={profile.avoids_period_value_branch_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  first_pass_positive_targets_are_H0_and_conductor39_divisor_additive_theorems=1")
    print("  source_certification_only_is_not_source_stage_closure=1")
    print("  value_hits_need_period156_context=1")
    print("  h0_divisor_hits_need_h90_boundary=1")
    print("  conductor39_projection_shortcuts_are_killed=1")
    print(
        "ksy_y_h0_conductor39_first_pass_theorem_triage_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("H0/conductor-39 first-pass theorem triage regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

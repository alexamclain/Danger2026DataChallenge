#!/usr/bin/env python3
"""KSY Theorem 5.3 verdict against the X_1(8112) bridge contract.

The exact-P scout already kills Koo-Shin-Yoon Theorem 5.3 as a direct
75-atom product theorem.  After the cross-level bridge packet, there is a
newer and more precise question: does Theorem 5.3 at N=8112 supply the
same-j bridge to the practical X_1(16) extractor?

Verdict: it supplies useful normalized-y and torsion-generation vocabulary,
and at N=8112 it has the right abstract order-8112 shape, but it does not
specialize to the p25 odd target, the production A,xP16 chart, a halving chain,
or a verified DANGER3 triple.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")
P25 = 10**25 + 13
X16_LEVEL = 16
ODD_LEVEL = 507
CROSS_LEVEL = 8112


@dataclass(frozen=True)
class Ksy53BridgeVerdictRow:
    name: str
    source_clause: str
    source_window: str
    positive_payload: str
    local_command: str
    expected_decision: str
    first_missing_clause: str
    actual_ksy_clause: bool
    abstract_order8112_shape: bool
    ties_to_p25_odd_target: bool
    same_j_bridge_identified: bool
    practical_x16_surface: bool
    halving_or_x0: bool
    submission_ready: bool
    recommendation: str
    ok: bool


@dataclass(frozen=True)
class Ksy53BridgeVerdictProfile:
    p: int
    x16_level: int
    odd_level: int
    cross_level: int
    prerequisite_markers_present: int
    rows: tuple[Ksy53BridgeVerdictRow, ...]
    actual_source_rows: int
    actual_closing_rows: int
    abstract_order8112_rows: int
    p25_odd_target_rows: int
    same_j_bridge_rows: int
    practical_x16_surface_rows: int
    halving_rows: int
    submission_ready_rows: int
    hypothetical_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def source_claim_command(name: str, anchor: str, output_kind: str) -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py "
        f"--candidate --name {name} --anchor {anchor} --output-kind {output_kind}"
    )


def x1_8112_command(
    name: str,
    *,
    exact_p25: bool = False,
    odd_value: bool = False,
    fiber_product: bool = False,
    x16_relation: bool = False,
    danger3_framing: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        "--odd-payload-object Y_507",
        "--theorem-body",
    ]
    if exact_p25:
        parts.append("--exact-p25")
    if odd_value:
        parts.append("--odd-value-or-divisor")
    if fiber_product:
        parts.extend(("--fiber-product", "--j-gluing"))
    if x16_relation:
        parts.extend(("--x16-relation", "--emit-y", "--emit-model-root-xp16"))
    if danger3_framing:
        parts.append("--danger3-framing")
    return " ".join(parts)


def verdict_rows() -> tuple[Ksy53BridgeVerdictRow, ...]:
    return (
        Ksy53BridgeVerdictRow(
            name="ksy_equation_3_4_normalized_y_language",
            source_clause="Equation (3.4)",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:420-466",
            positive_payload="normalized y(Q)=-g(2Q)/g(Q)^4 Siegel-function vocabulary",
            local_command=source_claim_command(
                "ksy_equation_3_4_normalized_y_language",
                "ksy_normalized_y_siegel_formula",
                "value",
            ),
            expected_decision="conditional_missing_exact_product",
            first_missing_clause="exact product P with C=(47,28), D=(22,3), K=(57,0)",
            actual_ksy_clause=True,
            abstract_order8112_shape=False,
            ties_to_p25_odd_target=False,
            same_j_bridge_identified=False,
            practical_x16_surface=False,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="continue only as formula vocabulary until it emits an exact p25 product or bridge",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_theorem_5_3_family_generation",
            source_clause="Theorem 5.3, family-level statement",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1000-1080",
            positive_payload="K_(N) ray-class generation from x(0,1/N) and normalized y(0,1/N)",
            local_command=x1_8112_command(
                "ksy_theorem_5_3_family_generation",
                fiber_product=True,
            ),
            expected_decision="conditional_missing_exact_p25_specialization",
            first_missing_clause="p25-specialized target, not a family-level possibility",
            actual_ksy_clause=True,
            abstract_order8112_shape=False,
            ties_to_p25_odd_target=False,
            same_j_bridge_identified=False,
            practical_x16_surface=False,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="do not count family-level K_(N) generation as p25 bridge progress",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_theorem_5_3_generation_only_source_claim",
            source_clause="Theorem 5.3, source-claim classifier",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1000-1080",
            positive_payload="single torsion point generates the ray class field when 4 divides N",
            local_command=source_claim_command(
                "ksy_theorem_5_3_generation_only",
                "ksy_theorem_5_3_ray_class_generation",
                "field-generation",
            ),
            expected_decision="reject_not_closure_theorem",
            first_missing_clause="not an exact finite-field identity for P",
            actual_ksy_clause=True,
            abstract_order8112_shape=True,
            ties_to_p25_odd_target=False,
            same_j_bridge_identified=False,
            practical_x16_surface=False,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="kill as source closure; keep only as torsion-generation context",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_n8112_abstract_R_not_odd_target",
            source_clause="Theorem 5.3 specialized to N=8112, optimistic bridge reading",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1000-1080",
            positive_payload="abstract order-8112 torsion point shape on one CM elliptic curve",
            local_command=x1_8112_command(
                "ksy_n8112_abstract_R_not_odd_target",
                exact_p25=True,
                fiber_product=True,
            ),
            expected_decision="reject_generic_x16_not_ksy_bridge",
            first_missing_clause="odd-level KSY/Yang/H90 value or divisor payload",
            actual_ksy_clause=False,
            abstract_order8112_shape=True,
            ties_to_p25_odd_target=False,
            same_j_bridge_identified=False,
            practical_x16_surface=False,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="requires an explicit projection to the recorded Y_507/H0/conductor-39 target",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_n8112_bridge_after_odd_target_hypothetical",
            source_clause="hypothetical strengthening of Theorem 5.3",
            source_window="not supplied by KSY; local bridge contract calibration",
            positive_payload="order-8112 same-j bridge tied to the exact p25 odd target",
            local_command=x1_8112_command(
                "ksy_n8112_bridge_after_odd_target_hypothetical",
                exact_p25=True,
                odd_value=True,
                fiber_product=True,
            ),
            expected_decision="cross_level_target_identified_specialization_missing",
            first_missing_clause="specialized relation yielding X_1(16) y, A, xP16, or x0",
            actual_ksy_clause=False,
            abstract_order8112_shape=True,
            ties_to_p25_odd_target=True,
            same_j_bridge_identified=True,
            practical_x16_surface=False,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="would be real bridge progress, but still needs the production X_1(16) chart",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_n8112_x16_surface_hypothetical",
            source_clause="hypothetical strengthened bridge plus production chart",
            source_window="not supplied by KSY; local bridge contract calibration",
            positive_payload="same-j bridge emits X_1(16) y, model root, A, and xP16",
            local_command=x1_8112_command(
                "ksy_n8112_x16_surface_hypothetical",
                exact_p25=True,
                odd_value=True,
                fiber_product=True,
                x16_relation=True,
            ),
            expected_decision="cross_level_surface_policy_or_framing_missing",
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            actual_ksy_clause=False,
            abstract_order8112_shape=True,
            ties_to_p25_odd_target=True,
            same_j_bridge_identified=True,
            practical_x16_surface=True,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="would reach the production surface but still needs policy/framing and halving",
            ok=True,
        ),
        Ksy53BridgeVerdictRow(
            name="ksy_n8112_policy_surface_hypothetical",
            source_clause="hypothetical DANGER3-framed bridge surface",
            source_window="not supplied by KSY; local bridge contract calibration",
            positive_payload="DANGER3-framed X_1(16) A,xP16 surface tied to the odd target",
            local_command=x1_8112_command(
                "ksy_n8112_policy_surface_hypothetical",
                exact_p25=True,
                odd_value=True,
                fiber_product=True,
                x16_relation=True,
                danger3_framing=True,
            ),
            expected_decision="x16_surface_reached_halving_or_vpp_missing",
            first_missing_clause="valid halving chain from xP16 to concrete x0",
            actual_ksy_clause=False,
            abstract_order8112_shape=True,
            ties_to_p25_odd_target=True,
            same_j_bridge_identified=True,
            practical_x16_surface=True,
            halving_or_x0=False,
            submission_ready=False,
            recommendation="would still require x_4..x_42 or direct x0 plus official vpp.py",
            ok=True,
        ),
    )


def profile_ksy53_bridge_verdict() -> Ksy53BridgeVerdictProfile:
    rows = verdict_rows()
    prerequisite_markers = sum(
        (
            marker_present(
                RESEARCH / "p25_ksy_y_ksy_exact_p_primary_source_scout_20260613.md",
                "ksy_y_ksy_exact_p_primary_source_scout_rows=1/1",
            ),
            marker_present(
                RESEARCH / "p25_ksy_y_cross_level_bridge_source_route_packet_20260614.md",
                "ksy_y_cross_level_bridge_source_route_packet_rows=1/1",
            ),
        )
    )
    actual_source = sum(row.actual_ksy_clause for row in rows)
    actual_closing = sum(row.actual_ksy_clause and row.submission_ready for row in rows)
    abstract_order = sum(row.abstract_order8112_shape for row in rows)
    odd_target = sum(row.ties_to_p25_odd_target for row in rows)
    same_j = sum(row.same_j_bridge_identified for row in rows)
    x16_surface = sum(row.practical_x16_surface for row in rows)
    halving = sum(row.halving_or_x0 for row in rows)
    submission = sum(row.submission_ready for row in rows)
    hypothetical = sum(not row.actual_ksy_clause for row in rows)
    row_ok = (
        P25 == 10000000000000000000000013
        and X16_LEVEL == 16
        and ODD_LEVEL == 507
        and CROSS_LEVEL == 8112
        and prerequisite_markers == 2
        and len(rows) == 7
        and actual_source == 3
        and actual_closing == 0
        and abstract_order == 5
        and odd_target == 3
        and same_j == 3
        and x16_surface == 2
        and halving == 0
        and submission == 0
        and hypothetical == 4
        and tuple(row.expected_decision for row in rows)
        == (
            "conditional_missing_exact_product",
            "conditional_missing_exact_p25_specialization",
            "reject_not_closure_theorem",
            "reject_generic_x16_not_ksy_bridge",
            "cross_level_target_identified_specialization_missing",
            "cross_level_surface_policy_or_framing_missing",
            "x16_surface_reached_halving_or_vpp_missing",
        )
        and all(row.ok for row in rows)
    )
    return Ksy53BridgeVerdictProfile(
        p=P25,
        x16_level=X16_LEVEL,
        odd_level=ODD_LEVEL,
        cross_level=CROSS_LEVEL,
        prerequisite_markers_present=prerequisite_markers,
        rows=rows,
        actual_source_rows=actual_source,
        actual_closing_rows=actual_closing,
        abstract_order8112_rows=abstract_order,
        p25_odd_target_rows=odd_target,
        same_j_bridge_rows=same_j,
        practical_x16_surface_rows=x16_surface,
        halving_rows=halving,
        submission_ready_rows=submission,
        hypothetical_rows=hypothetical,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_ksy53_bridge_verdict()
    print("p25 KSY-y KSY Theorem 5.3 X1(8112) bridge verdict gate")
    print("levels")
    print(f"  p={profile.p}")
    print(f"  odd_level={profile.odd_level}")
    print(f"  x16_level={profile.x16_level}")
    print(f"  cross_level={profile.cross_level}")
    print(f"prerequisite_markers_present={profile.prerequisite_markers_present}")
    print("verdict_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: clause={row.source_clause} actual={int(row.actual_ksy_clause)} "
            f"order8112={int(row.abstract_order8112_shape)} "
            f"odd_target={int(row.ties_to_p25_odd_target)} "
            f"same_j={int(row.same_j_bridge_identified)} "
            f"x16_surface={int(row.practical_x16_surface)} "
            f"halving={int(row.halving_or_x0)} "
            f"submission={int(row.submission_ready)} "
            f"decision={row.expected_decision} missing={row.first_missing_clause}"
        )
        print(f"    window={row.source_window}")
        print(f"    positive={row.positive_payload}")
        print(f"    recommendation={row.recommendation}")
        print(f"    command={row.local_command}")
    print("counts")
    print(f"  actual_source_rows={profile.actual_source_rows}")
    print(f"  actual_closing_rows={profile.actual_closing_rows}")
    print(f"  abstract_order8112_rows={profile.abstract_order8112_rows}")
    print(f"  p25_odd_target_rows={profile.p25_odd_target_rows}")
    print(f"  same_j_bridge_rows={profile.same_j_bridge_rows}")
    print(f"  practical_x16_surface_rows={profile.practical_x16_surface_rows}")
    print(f"  halving_rows={profile.halving_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  hypothetical_rows={profile.hypothetical_rows}")
    print("interpretation")
    print("  ksy_theorem_5_3_has_order8112_vocabulary_but_not_p25_bridge=1")
    print("  actual_ksy_rows_do_not_emit_odd_target_x16_surface_halving_or_submission=1")
    print("  strengthened_ksy_bridge_would_still_need_chart_policy_halving_vpp=1")
    print(f"ksy_y_ksy_theorem53_x18112_bridge_verdict_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("KSY Theorem 5.3 X1(8112) bridge verdict regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

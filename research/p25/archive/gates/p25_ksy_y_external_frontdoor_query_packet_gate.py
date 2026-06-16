#!/usr/bin/env python3
"""Exact external front-door query packet for the p25 KSY-y moonshot.

This converts the external source scout into concrete expert/literature
questions.  The first four questions reuse the priority-1 packet fixtures.
The fifth adds the exact 75-atom product front door via the closing-theorem
obligation classifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_external_frontdoor_source_scout_gate import (
    profile_external_frontdoor_source_scout,
)
from p25_ksy_y_priority1_source_query_packet_gate import (
    profile_priority1_source_query_packet,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate import (
    ClosingTheoremClaim,
    classify_claim as classify_exact_product_claim,
)


RESEARCH = Path("research/p25")
FIXTURES = RESEARCH / "priority1_divisor_additive_packet_fixtures"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_frontdoor_source_scout_20260614.md",
        "ksy_y_external_frontdoor_source_scout_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_source_query_packet_20260614.md",
        "ksy_y_priority1_source_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_divisor_additive_intake_20260614.md",
        "ksy_y_priority1_divisor_additive_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH / "subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation.md",
        "robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalFrontdoorQueryRow:
    name: str
    query_kind: str
    source_family: str
    source_urls: tuple[str, ...]
    question_for_source: str
    accepted_answer_shape: str
    first_falsifier: str
    local_command: str
    expected_decision: str
    actual_decision: str
    closes_source_stage_if_yes: bool
    current_source_theorem_exists: bool
    priority_rank: int
    exact_p25_specialization_required: bool
    ok: bool


@dataclass(frozen=True)
class ExternalFrontdoorQueryPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    external_scout_ok: bool
    priority1_query_packet_ok: bool
    rows: tuple[ExternalFrontdoorQueryRow, ...]
    row_count: int
    closing_query_rows: int
    falsifier_rows: int
    current_source_theorem_rows: int
    priority1_rows: int
    exact75_rows: int
    fixture_backed_rows: int
    exact_p25_required_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def packet_command(path: Path) -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py "
        f"--packet-json {path}"
    )


def exact_product_command(*, name: str, output_kind: str, period156: bool = False) -> str:
    flags = [
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3",
        "research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py",
        "--candidate",
        f"--name {name}",
        "--source-family Kubert-Lang-KSY-exact-P",
        f"--output-kind {output_kind}",
        "--exact-p",
        "--mixed-graph",
        "--equal-weight",
        "--orientation",
        "--arithmetic-source",
        "--finite-identity",
    ]
    if period156:
        flags.append("--period-156")
    return " ".join(flags)


def exact_product_decision(*, name: str, output_kind: str, period156: bool = False):
    return classify_exact_product_claim(
        ClosingTheoremClaim(
            name=name,
            source_family="Kubert-Lang/KSY exact normalized-y product",
            emits_exact_p=True,
            preserves_mixed_graph=True,
            equal_weight_atoms=True,
            orientation_recorded=True,
            arithmetic_source_theorem=True,
            output_kind=output_kind,
            finite_field_identity_for_p=True,
            period_156_context=period156,
            danger3_policy_or_non_cm_framing=False,
            extraction_to_A_x0=False,
            concrete_vpp_verified_triple=False,
        )
    )


def exact_product_missing_period_decision():
    return exact_product_decision(
        name="exact_75_atom_value_without_period156",
        output_kind="value",
        period156=False,
    )


def row(
    *,
    name: str,
    query_kind: str,
    source_family: str,
    source_urls: tuple[str, ...],
    question: str,
    accepted_shape: str,
    falsifier: str,
    local_command: str,
    expected_decision: str,
    actual_decision: str,
    closes: bool,
    priority_rank: int,
    fixture_backed: bool,
) -> ExternalFrontdoorQueryRow:
    return ExternalFrontdoorQueryRow(
        name=name,
        query_kind=query_kind,
        source_family=source_family,
        source_urls=source_urls,
        question_for_source=question,
        accepted_answer_shape=accepted_shape,
        first_falsifier=falsifier,
        local_command=local_command,
        expected_decision=expected_decision,
        actual_decision=actual_decision,
        closes_source_stage_if_yes=closes,
        current_source_theorem_exists=False,
        priority_rank=priority_rank,
        exact_p25_specialization_required=True,
        ok=actual_decision == expected_decision
        and (not fixture_backed or "priority1_divisor_additive_packet_fixtures" in local_command),
    )


def query_rows() -> tuple[ExternalFrontdoorQueryRow, ...]:
    exact75_close = exact_product_decision(
        name="exact_75_atom_product_divisor_theorem",
        output_kind="divisor-additive",
    )
    exact75_value_no_period = exact_product_missing_period_decision()
    return (
        row(
            name="ask_h0_divisor_boundary_identity",
            query_kind="closing_query",
            source_family="H0/Yang/Kubert-Lang",
            source_urls=(
                "https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf",
                "https://eudml.org/doc/162791",
            ),
            question=(
                "Does the source prove an exact divisor/additive identity for "
                "one of the four legal 78-over-78 H0 products, with the "
                "Hilbert-90 boundary to Norm_156(Y_507)?"
            ),
            accepted_shape="exact legal H0 product + divisor/additive identity + H90 boundary",
            falsifier="source legality, value-only data, or divisor statement without the H90 boundary",
            local_command=packet_command(FIXTURES / "h0_divisor_close.json"),
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            actual_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="ask_conductor39_divisor_identity",
            query_kind="closing_query",
            source_family="mixed conductor-39 unit / Yang distribution",
            source_urls=(
                "https://eudml.org/doc/162791",
                "https://books.google.com/books/about/Modular_Units.html?id=BwwzmZjjVdgC",
            ),
            question=(
                "Does the source prove an exact divisor/additive identity for "
                "the legal mixed conductor-39 source U_chi/W, preserving the "
                "chi_3 tensor chi_13 object, Yang lift, and descent?"
            ),
            accepted_shape="U_chi/W + mixed tensor + Yang lift + H90/ratio descent + divisor/additive theorem",
            falsifier="prime projection, axis-only statement, or source certification without finite theorem",
            local_command=packet_command(FIXTURES / "conductor39_divisor_close.json"),
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            actual_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="ask_twisted_h90_divisor_identity",
            query_kind="closing_query",
            source_family="twisted ratio / Hilbert-90",
            source_urls=(
                "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
                "https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf",
            ),
            question=(
                "Does the source prove a finite divisor/additive theorem for "
                "the twisted ratio/Hilbert-90 object, with the period-156 "
                "bridge context required by the current router?"
            ),
            accepted_shape="twisted ratio/H90 object + finite divisor theorem + arithmetic source + period-156 bridge context",
            falsifier="H90 boundary or quotient vocabulary without finite theorem and period-156 bridge context",
            local_command=packet_command(FIXTURES / "twisted_divisor_close.json"),
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            actual_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="ask_curved_corner_divisor_identity",
            query_kind="closing_query",
            source_family="unit-triangle curved K-traced corner",
            source_urls=(
                "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
                "https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf",
            ),
            question=(
                "Does the source prove a finite divisor/additive theorem for "
                "the exact unit-triangle curved K-traced corner, with the "
                "period-156 context required by the current curved-corner router?"
            ),
            accepted_shape="unit-triangle curved corner + finite divisor theorem + arithmetic source + period-156 context",
            falsifier="curved helper only, wrong unit triangle, or theorem without period-156 context",
            local_command=packet_command(FIXTURES / "curved_corner_divisor_close.json"),
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            actual_decision="source_theorem_closed_policy_or_framing_missing",
            closes=True,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="ask_exact_75_atom_product_divisor_theorem",
            query_kind="closing_query",
            source_family="Kubert-Lang / KSY normalized-y",
            source_urls=(
                "https://arxiv.org/abs/1007.2307",
                "https://eudml.org/doc/162791",
            ),
            question=(
                "Does the source prove an exact divisor/additive theorem for "
                "P = prod_{j=-1..1,k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
                "with the mixed C3 x C169 graph, equal atom weights, and orientation?"
            ),
            accepted_shape="exact P + mixed graph + 75 equal K-traced atoms + orientation + arithmetic source theorem",
            falsifier="formula language, field generation, one y-value, or product missing mixed graph/orientation",
            local_command=exact_product_command(
                name="exact_75_atom_product_divisor_theorem",
                output_kind="divisor-additive",
            ),
            expected_decision="source_theorem_closed_policy_or_framing_missing",
            actual_decision=exact75_close.decision,
            closes=True,
            priority_rank=1,
            fixture_backed=False,
        ),
        row(
            name="falsify_h0_boundary_missing",
            query_kind="falsifier",
            source_family="H0/Yang/Kubert-Lang",
            source_urls=("https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf",),
            question="Does the answer omit the exact Hilbert-90 boundary to Norm_156(Y_507)?",
            accepted_shape="boundary omission routes as conditional, not closure",
            falsifier="Hilbert-90 boundary to Norm_156(Y_507) is missing",
            local_command=packet_command(FIXTURES / "h0_missing_boundary.json"),
            expected_decision="conditional_divisor_identity_missing_h90_boundary",
            actual_decision="conditional_divisor_identity_missing_h90_boundary",
            closes=False,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="falsify_projection_or_axis_only",
            query_kind="falsifier",
            source_family="conductor-39 projection/axis shadow",
            source_urls=("https://eudml.org/doc/162791",),
            question="Does the answer collapse to prime-13, C169, projection, or axis-only data?",
            accepted_shape="projection or axis-only data is rejected",
            falsifier="mixed chi_3 tensor chi_13 source on X_1(39) is missing",
            local_command=packet_command(FIXTURES / "projection_reject.json"),
            expected_decision="reject_loses_mixed_tensor",
            actual_decision="reject_loses_mixed_tensor",
            closes=False,
            priority_rank=0,
            fixture_backed=True,
        ),
        row(
            name="falsify_twisted_missing_period_bridge",
            query_kind="falsifier",
            source_family="twisted ratio / Hilbert-90",
            source_urls=("https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",),
            question="Does the twisted/H90 answer omit period-156 bridge context?",
            accepted_shape="twisted/H90 theorem without period-156 context remains conditional",
            falsifier="period-156 branch/root/telescoping context is missing",
            local_command=packet_command(FIXTURES / "twisted_missing_period.json"),
            expected_decision="conditional_value_theorem_missing_period156_context",
            actual_decision="conditional_value_theorem_missing_period156_context",
            closes=False,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="falsify_curved_missing_period_context",
            query_kind="falsifier",
            source_family="unit-triangle curved K-traced corner",
            source_urls=("https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",),
            question="Does the curved-corner answer omit period-156 context?",
            accepted_shape="curved-corner finite theorem without period-156 context remains conditional",
            falsifier="period-156 branch/root/telescoping context is missing",
            local_command=packet_command(FIXTURES / "curved_missing_period.json"),
            expected_decision="conditional_missing_period156_context",
            actual_decision="conditional_missing_period156_context",
            closes=False,
            priority_rank=1,
            fixture_backed=True,
        ),
        row(
            name="falsify_exact_75_value_without_period156",
            query_kind="falsifier",
            source_family="Kubert-Lang / KSY normalized-y",
            source_urls=("https://arxiv.org/abs/1007.2307",),
            question="Does the answer give only an exact value theorem for P without support-period-156 context?",
            accepted_shape="value theorem without period-156 context remains conditional",
            falsifier="period-156 fixedness/telescoping for value output is missing",
            local_command=exact_product_command(
                name="exact_75_atom_value_without_period156",
                output_kind="value",
                period156=False,
            ),
            expected_decision="conditional_value_missing_period_156",
            actual_decision=exact75_value_no_period.decision,
            closes=False,
            priority_rank=2,
            fixture_backed=False,
        ),
    )


def profile_external_frontdoor_query_packet() -> ExternalFrontdoorQueryPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    scout = profile_external_frontdoor_source_scout()
    priority = profile_priority1_source_query_packet()
    rows = query_rows()
    closing = sum(row.query_kind == "closing_query" for row in rows)
    falsifier = sum(row.query_kind == "falsifier" for row in rows)
    current = sum(row.current_source_theorem_exists for row in rows)
    priority1 = sum(row.priority_rank == 1 for row in rows)
    exact75 = sum("exact_75" in row.name for row in rows)
    fixture_backed = sum("priority1_divisor_additive_packet_fixtures" in row.local_command for row in rows)
    exact_required = sum(row.exact_p25_specialization_required for row in rows)
    expected = (
        "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_divisor_identity_missing_h90_boundary",
            "reject_loses_mixed_tensor",
            "conditional_value_theorem_missing_period156_context",
            "conditional_missing_period156_context",
            "conditional_value_missing_period_156",
        )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and scout.row_ok
        and priority.row_ok
        and len(rows) == 10
        and closing == 5
        and falsifier == 5
        and current == 0
        and priority1 == 8
        and exact75 == 2
        and fixture_backed == 8
        and exact_required == 10
        and tuple(row.actual_decision for row in rows) == expected
        and tuple(row.expected_decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    return ExternalFrontdoorQueryPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        external_scout_ok=scout.row_ok,
        priority1_query_packet_ok=priority.row_ok,
        rows=rows,
        row_count=len(rows),
        closing_query_rows=closing,
        falsifier_rows=falsifier,
        current_source_theorem_rows=current,
        priority1_rows=priority1,
        exact75_rows=exact75,
        fixture_backed_rows=fixture_backed,
        exact_p25_required_rows=exact_required,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_frontdoor_query_packet()
    print("p25 KSY-y external front-door query packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  external_scout_ok={int(profile.external_scout_ok)}")
    print(f"  priority1_query_packet_ok={int(profile.priority1_query_packet_ok)}")
    print("query_rows")
    for query in profile.rows:
        print(
            "  "
            f"{query.name}: kind={query.query_kind} source={query.source_family} "
            f"rank={query.priority_rank} closes={int(query.closes_source_stage_if_yes)} "
            f"decision={query.actual_decision} exact_required={int(query.exact_p25_specialization_required)}"
        )
        print(f"    question={query.question_for_source}")
        print(f"    accept={query.accepted_answer_shape}")
        print(f"    falsifier={query.first_falsifier}")
        print(f"    urls={'; '.join(query.source_urls)}")
        print(f"    command={query.local_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  closing_query_rows={profile.closing_query_rows}")
    print(f"  falsifier_rows={profile.falsifier_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  exact75_rows={profile.exact75_rows}")
    print(f"  fixture_backed_rows={profile.fixture_backed_rows}")
    print(f"  exact_p25_required_rows={profile.exact_p25_required_rows}")
    print("interpretation")
    print("  external_query_packet_has_five_closing_questions=1")
    print("  exact75_frontdoor_is_now_first_class=1")
    print("  all_answers_must_be_exact_p25_specializations=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print(f"ksy_y_external_frontdoor_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("external front-door query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
